"""Record scientific method events and resolve their published state at a Git revision."""

import argparse
from contextlib import contextmanager
import csv
from datetime import date
import hashlib
import io
import json
import os
from pathlib import Path
import re
import subprocess
import sys
from tempfile import NamedTemporaryFile
from urllib.parse import quote, unquote, urlsplit
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
BASELINE = "decisions/baseline.json"
EVENTS = "decisions/events.csv"
CURRENT = "decisions/current.csv"
EVENT_FIELDS = "decision_id sequence action recorded_on scope statement source_ref supersedes implementation_ref".split()
CURRENT_FIELDS = (
    "decision_id event_type status scope question ruling proposal_ref decision_ref decision_recorded_on "
    "implementation_status implementation_ref implementation_recorded_on supersedes superseded_by latest_sequence legacy_ref"
).split()
LEGACY_FIELDS = "decision_id status raised question options recommendation decided decided_on record".split()
SHA = re.compile(r"[0-9a-f]{40}")
CODE = re.compile(r"[a-zA-Z0-9][a-zA-Z0-9_.-]*")
IMPLEMENTATION = re.compile(
    r"https://github\.com/([\w.-]+/[\w.-]+)/(?:commit/([0-9a-f]{40})|blob/([0-9a-f]{40})/([^?#]+))(?:#L[1-9][0-9]*(?:-L[1-9][0-9]*)?)?"
)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def git(repo, *args):
    return subprocess.check_output(["git", "-C", str(repo), *args])


def read_file(root, path, revision=None):
    if revision is None:
        return (root / path).read_bytes()
    require(SHA.fullmatch(revision), "Supply a full Git revision")
    return git(root, "show", f"{revision}:{path}")


def read_csv(data, fields):
    stream = io.StringIO(data.decode("utf-8"), newline="")
    reader = csv.DictReader(stream, strict=True)
    require(reader.fieldnames == fields, "Unexpected CSV columns")
    for row in reader:
        require(
            None not in row and None not in row.values(),
            f"Incomplete CSV row at line {reader.line_num}",
        )
        yield row, reader.line_num


def csv_bytes(fields, rows, header=True):
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(stream, fields, lineterminator="\n")
    if header:
        writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def seed(root, evidence_repo, revision=None):
    pin = json.loads(read_file(root, BASELINE, revision))
    require(
        pin["repository"] == "RuralScan/evidence"
        and SHA.fullmatch(pin["revision"])
        and pin["path"] == "registers/methodology/decisions/method_decisions.csv",
        "Invalid evidence baseline",
    )
    if evidence_repo:
        data = read_file(evidence_repo, pin["path"], pin["revision"])
    else:
        url = f"https://raw.githubusercontent.com/{pin['repository']}/{pin['revision']}/{pin['path']}"
        with urlopen(url, timeout=30) as response:
            data = response.read()
    require(
        hashlib.sha256(data).hexdigest() == pin["sha256"],
        "Historical scientific ledger hash mismatch",
    )
    records, legacy = {}, {}
    first_line = 2
    for row, last_line in read_csv(data, LEGACY_FIELDS):
        code = row["decision_id"]
        require(code not in records, f"Duplicate historical decision {code}")
        url = f"https://github.com/{pin['repository']}/blob/{pin['revision']}/{pin['path']}#L{first_line}"
        first_line = last_line + 1
        records[code] = dict.fromkeys(CURRENT_FIELDS, "")
        records[code].update(
            decision_id=code,
            event_type="method_decision",
            status=row["status"],
            decision_ref=url if row["status"] == "decided" else "",
            decision_recorded_on=row["decided_on"]
            if row["status"] == "decided"
            else "",
            legacy_ref=url,
            latest_sequence="0",
            proposal_ref=url,
            implementation_status="unverified"
            if row["status"] == "decided"
            else "not_applicable",
        )
        legacy[code] = row
    require(
        len(legacy) == pin["rows"], "Historical scientific ledger row count mismatch"
    )
    return records, legacy


def transition(records, event):
    code, action = event["decision_id"], event["action"]
    require(CODE.fullmatch(code), "Invalid decision ID")
    require(
        date.fromisoformat(event["recorded_on"]).isoformat() == event["recorded_on"],
        "Use YYYY-MM-DD",
    )
    source = urlsplit(event["source_ref"])
    require(
        source.scheme == "https"
        and source.hostname
        and not source.username
        and not source.password
        and not any(c.isspace() for c in event["source_ref"]),
        "Supply a public HTTPS source reference",
    )
    require(
        event["scope"].strip() and event["statement"].strip(),
        "Supply the affected scope and scientific statement",
    )
    row = records.get(code)
    sequence = int(row["latest_sequence"]) + 1 if row else 1
    require(event["sequence"] == str(sequence), f"{code}: expected sequence {sequence}")
    status = row["status"] if row else None
    allowed = {
        "propose": {None},
        "decide": {"open", "parked"},
        "park": {"open"},
        "reopen": {"parked"},
        "implement": {"decided"},
    }
    require(
        action in allowed and status in allowed[action],
        f"{code}: cannot {action} from {status}",
    )
    targets = event["supersedes"].split()  # space-separated stable decision IDs
    require(
        not targets or action == "decide",
        "Only a decision can supersede an earlier ruling",
    )
    require(len(targets) == len(set(targets)), "Duplicate supersession target")
    for target in targets:
        require(
            target != code
            and target in records
            and records[target]["status"] == "decided",
            f"Supersession target must be a current decided code: {target}",
        )
    ref = event["implementation_ref"]
    if action == "implement":
        require(
            IMPLEMENTATION.fullmatch(ref),
            "Implementation needs a GitHub file or commit at a full SHA",
        )
        require(
            not row["scope"] or row["scope"] == event["scope"],
            "Implementation must cover the decided scope",
        )
    else:
        require(not ref, "Use a separate implement event for the implementing change")

    if row is None:
        row = records[code] = dict.fromkeys(CURRENT_FIELDS, "")
        row.update(
            decision_id=code,
            event_type="method_decision",
            question=event["statement"],
            proposal_ref=event["source_ref"],
            implementation_status="not_applicable",
        )
    row["latest_sequence"] = event["sequence"]
    if action in {"propose", "decide"} or not row["scope"]:
        row["scope"] = event["scope"]
    if action == "decide":
        row.update(
            status="decided",
            ruling=event["statement"],
            decision_ref=event["source_ref"],
            decision_recorded_on=event["recorded_on"],
            supersedes=" ".join(targets),
            implementation_status="pending",
        )
        for target in targets:
            records[target].update(status="superseded", superseded_by=code)
    elif action == "implement":
        row.update(
            implementation_status="implemented",
            implementation_ref=ref,
            implementation_recorded_on=event["recorded_on"],
        )
    else:
        row["status"] = "parked" if action == "park" else "open"


def replay(root, evidence_repo, event_bytes, revision=None):
    records, legacy = seed(root, evidence_repo, revision)
    history = {}
    for event, _ in read_csv(event_bytes, EVENT_FIELDS):
        code = event["decision_id"]
        prior = history.setdefault(code, [])
        previous_date = (
            prior[-1]["recorded_on"]
            if prior
            else (
                legacy.get(code, {}).get("decided_on")
                or legacy.get(code, {}).get("raised", "")
            )
        )
        require(
            event["recorded_on"] >= previous_date,
            f"{code}: event predates its previous record",
        )
        for target in event["supersedes"].split():
            if target in records:
                require(
                    event["recorded_on"] >= records[target]["decision_recorded_on"],
                    f"{code}: supersession predates the ruling it replaces",
                )
        transition(records, event)
        prior.append(event)
    return records, legacy, history


def projection(records):
    return csv_bytes(CURRENT_FIELDS, [records[k] for k in sorted(records)])


def verify_implementation(ref):
    """Check the named public Git object. Scientific relevance is reviewed on the PR."""
    match = IMPLEMENTATION.fullmatch(ref)
    require(match, "Expected a commit-pinned implementation")
    repo, commit_sha, file_sha, path = match.groups()
    path = unquote(path) if path else None
    endpoint = (
        f"commits/{commit_sha}"
        if commit_sha
        else f"contents/{quote(path, safe='/')}?ref={file_sha}"
    )
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "RuralScan-method-register",
    }
    token = os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = "Bearer " + token
    with urlopen(
        Request(f"https://api.github.com/repos/{repo}/{endpoint}", headers=headers),
        timeout=30,
    ) as response:
        obj = json.load(response)
    require(
        isinstance(obj, dict)
        and (
            obj.get("sha") == commit_sha
            if commit_sha
            else obj.get("type") == "file" and obj.get("path") == path
        ),
        "Implementation reference did not resolve",
    )


def check(root, evidence_repo, base=None, verify_refs=False):
    events = read_file(root, EVENTS)
    prior_records = 0
    if base:
        require(SHA.fullmatch(base), "Use a full base revision")
        files = set(
            git(root, "ls-tree", "-r", "--name-only", base, "--", BASELINE, EVENTS)
            .decode()
            .splitlines()
        )
        if BASELINE in files:
            require(
                read_file(root, BASELINE) == read_file(root, BASELINE, base),
                "Historical baseline changed",
            )
        if EVENTS in files:
            previous = read_file(root, EVENTS, base)
            require(events.startswith(previous), "Previously published events changed")
            prior_records = sum(1 for _ in read_csv(previous, EVENT_FIELDS))
    records, _, _ = replay(root, evidence_repo, events)
    require(
        projection(records) == read_file(root, CURRENT),
        "Published method projection differs. Run build.",
    )
    if verify_refs:
        refs = {
            event["implementation_ref"]
            for i, (event, _) in enumerate(read_csv(events, EVENT_FIELDS))
            if i >= prior_records and event["action"] == "implement"
        }
        for ref in sorted(refs):
            verify_implementation(ref)
    return len(records)


def replace_file(path, data):
    with NamedTemporaryFile(dir=path.parent, delete=False) as out:
        try:
            out.write(data)
            out.flush()
            os.fsync(out.fileno())
            tmp = Path(out.name)
        except BaseException:
            Path(out.name).unlink(missing_ok=True)
            raise
    try:
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)


@contextmanager
def writer_lock(root):
    # The lock lives outside tracked data and works in linked worktrees.
    lock = (
        Path(git(root, "rev-parse", "--absolute-git-dir").decode().strip())
        / "method-decisions.lock"
    )
    try:
        with lock.open("x") as stream:
            stream.write(str(os.getpid()) + "\n")
    except FileExistsError:
        raise ValueError(
            f"Another writer holds {lock}. Check the recorded PID before removing an abandoned lock."
        ) from None
    try:
        yield
    finally:
        lock.unlink()


def record(root, evidence_repo, payload):
    require(
        isinstance(payload, dict) and set(payload) <= set(EVENT_FIELDS),
        "Unexpected event fields",
    )
    event = {k: payload.get(k, "") for k in EVENT_FIELDS}
    require(
        all(isinstance(v, str) for k, v in event.items() if k != "sequence"),
        "Event fields must be text",
    )
    require(type(event["sequence"]) in (str, int), "Supply a positive sequence number")
    event["sequence"] = str(event["sequence"])
    with writer_lock(root):
        original = read_file(root, EVENTS)
        known = [
            r
            for r, _ in read_csv(original, EVENT_FIELDS)
            if (r["decision_id"], r["sequence"])
            == (event["decision_id"], event["sequence"])
        ]
        require(
            not known or known == [event], "Sequence already records a different event"
        )
        data = (
            original
            if known
            else original + csv_bytes(EVENT_FIELDS, [event], header=False)
        )
        records, _, _ = replay(root, evidence_repo, data)
        if not known:
            replace_file(root / EVENTS, data)
        # Retrying also repairs a projection interrupted after the event write.
        current = projection(records)
        if not (root / CURRENT).exists() or current != read_file(root, CURRENT):
            replace_file(root / CURRENT, current)
        return not known


def resolve(root, evidence_repo, revision, code):
    events = read_file(root, EVENTS, revision)
    records, legacy, history = replay(root, evidence_repo, events, revision)
    require(
        projection(records) == read_file(root, CURRENT, revision),
        "Invalid projection at selected revision",
    )
    require(code in records, f"Unknown method decision {code}")
    return {
        "method_revision": revision,
        "decision": records[code],
        "events": history.get(code, []),
        "historical_record": legacy.get(code),
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--evidence-repo",
        type=Path,
        help="Read the pinned historical ledger from a local evidence clone",
    )
    sub = parser.add_subparsers(dest="command", required=True)
    add = sub.add_parser("record", help="Prepare an event on a proposal branch")
    add.add_argument("event", type=Path, help="JSON file of event fields")
    verify = sub.add_parser(
        "check", help="Replay history and compare the published projection"
    )
    verify.add_argument(
        "--base", help="Compare previous event bytes at this full Git SHA"
    )
    verify.add_argument(
        "--verify-implementations",
        action="store_true",
        help="Verify links to newly cited implementation commits and files on GitHub",
    )
    sub.add_parser("build", help="Rebuild current.csv from recorded events")
    read = sub.add_parser(
        "show", help="Resolve one decision from an immutable method edition"
    )
    read.add_argument("decision_id")
    read.add_argument(
        "--revision", required=True, help="Full RuralScan/method commit SHA"
    )
    args = parser.parse_args()
    if args.command == "record":
        added = record(ROOT, args.evidence_repo, json.loads(args.event.read_bytes()))
        print(
            "Recorded on this branch." if added else "Identical event already recorded."
        )
    elif args.command == "check":
        print(
            f"Verified {check(ROOT, args.evidence_repo, args.base, args.verify_implementations)} method decisions."
        )
    elif args.command == "build":
        with writer_lock(ROOT):
            records, _, _ = replay(ROOT, args.evidence_repo, read_file(ROOT, EVENTS))
            replace_file(ROOT / CURRENT, projection(records))
    else:
        print(
            json.dumps(
                resolve(ROOT, args.evidence_repo, args.revision, args.decision_id),
                ensure_ascii=False,
                indent=2,
            )
        )


if __name__ == "__main__":
    try:
        main()
    except (
        ValueError,
        KeyError,
        OSError,
        csv.Error,
        subprocess.CalledProcessError,
    ) as exc:
        sys.exit(f"Method decision register: {exc}")
