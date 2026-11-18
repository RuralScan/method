"""Version numbers and the change history, read from VERSION.json and CHANGELOG.md.

Nothing else states a version. This module has no dependencies and needs no other checkout, so the
build, the pull-request check and the release workflow all read the same two files through it.

    python3 build/versioning.py version          the methodology version, for example 0.8.0
    python3 build/versioning.py status           draft or released
    python3 build/versioning.py notes            release notes for that version, as Markdown
    python3 build/versioning.py check-bump REF   fail if pages changed since REF and the version did not move
"""

import json
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION_FILE = ROOT / "VERSION.json"
CHANGELOG_FILE = ROOT / "CHANGELOG.md"
# Paths under the reference whose change alters a published page.
PAGE_PATHS = ("build/", "content/", "CHANGELOG.md")

_SEMVER = re.compile(r"(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)")
_CALVER = re.compile(r"(20\d\d)\.(1[0-2]|[1-9])\.([1-9]\d*)")
_RELEASE_ID = re.compile(r"[0-9a-f]{64}")


def parts(version):
    """A methodology version as three integers, so versions compare in order."""
    found = _SEMVER.fullmatch(version)
    if not found:
        raise SystemExit(f"{version!r} is not a version of the form major.minor.patch")
    return tuple(int(n) for n in found.groups())


def long_date(day):
    """18 November 2026."""
    d = date.fromisoformat(day)
    return f"{d.day} {d:%B %Y}"


def short_date(day):
    """18 Nov 2026."""
    d = date.fromisoformat(day)
    return f"{d.day} {d:%b %Y}"


def load(text=None):
    """The version file, checked. Raises SystemExit with the reason if it is malformed."""
    record = json.loads(VERSION_FILE.read_text() if text is None else text)
    own = record["methodology"]
    major = parts(own["version"])[0]
    date.fromisoformat(own["date"])
    if own["status"] not in ("draft", "released"):
        raise SystemExit("VERSION.json: status must be draft or released")
    if (major == 0) != (own["status"] == "draft"):
        raise SystemExit(
            "VERSION.json: versions before 1.0.0 are drafts, and versions from 1.0.0 are released"
        )
    seen = set()
    for base in record["evidence_base"]:
        if not _CALVER.fullmatch(base["version"]):
            raise SystemExit(
                f"VERSION.json: evidence base {base['version']!r} is not of the form year.month.release"
            )
        year, month, _ = base["version"].split(".")
        stamped = date.fromisoformat(base["date"])
        if (stamped.year, stamped.month) != (int(year), int(month)):
            raise SystemExit(
                f"VERSION.json: evidence base {base['version']} is dated {base['date']}, a different month"
            )
        if not _RELEASE_ID.fullmatch(base["release_id"]):
            raise SystemExit(
                f"VERSION.json: evidence base {base['version']} needs the full release identifier"
            )
        for key in (base["version"], base["release_id"]):
            if key in seen:
                raise SystemExit(f"VERSION.json: {key} is listed twice")
            seen.add(key)
    return record


def evidence_base(release_id):
    """The numbered evidence base that stands for one release identifier."""
    found = [b for b in load()["evidence_base"] if b["release_id"] == release_id]
    if len(found) != 1:
        raise SystemExit(
            f"VERSION.json gives no evidence base number for release {release_id[:8]}. "
            "A new release pin needs a new number: add it to evidence_base."
        )
    return found[0]


def changelog(text=None):
    """The change history as (versions, earlier).

    versions: [(version, iso date, [item, ...])], newest first.
    earlier:  [(heading, [item, ...])], the dated entries from before version numbers.
    """
    lines = (CHANGELOG_FILE.read_text() if text is None else text).splitlines()
    versions, earlier, items, in_earlier = [], [], None, False
    for line in lines:
        numbered = re.fullmatch(r"## \[([^\]]+)\] - (\d{4}-\d\d-\d\d)", line)
        if numbered:
            if in_earlier:
                raise SystemExit(
                    "CHANGELOG.md: numbered versions go above 'Before version numbers'"
                )
            parts(numbered[1])
            date.fromisoformat(numbered[2])
            items = []
            versions.append((numbered[1], numbered[2], items))
        elif line.startswith("## "):
            in_earlier, items = True, None
        elif line.startswith("### ") and in_earlier:
            items = []
            earlier.append((line[4:].strip(), items))
        elif line.startswith("- ") and items is not None:
            items.append(line[2:].strip())
        elif line.startswith("  ") and line.strip() and items:
            items[-1] += " " + line.strip()
    order = [parts(v) for v, _, _ in versions]
    if order != sorted(set(order), reverse=True):
        raise SystemExit(
            "CHANGELOG.md: versions must be listed once each, newest first"
        )
    for version, _, entry in versions:
        if not entry:
            raise SystemExit(f"CHANGELOG.md: version {version} lists no change")
    return versions, earlier


def current():
    """(version, iso date, status), after checking the change history opens with the same version."""
    own = load()["methodology"]
    versions, _ = changelog()
    if not versions or versions[0][:2] != (own["version"], own["date"]):
        top = f"{versions[0][0]} dated {versions[0][1]}" if versions else "no version"
        raise SystemExit(
            f"VERSION.json says {own['version']} dated {own['date']}; CHANGELOG.md opens with {top}. "
            "The top entry of the change history must be the version in the version file."
        )
    return own["version"], own["date"], own["status"]


def release_notes():
    _version, day, status = current()
    items = changelog()[0][0][2]
    state = "Draft version" if status == "draft" else "Released version"
    return (
        f"{state} of the Rural NbS Scan methodology, {long_date(day)}.\n\n"
        + "\n".join(f"- {item}" for item in items)
        + "\n"
    )


def check_bump(base):
    """Fail if a page source changed since `base` and the version number did not go up."""
    repo = ROOT.parent
    prefix = ROOT.name + "/"

    def git(*args):
        return subprocess.run(
            ["git", "-C", str(repo), *args],
            check=False,
            capture_output=True,
            text=True,
        )

    changed = [
        path
        for path in git(
            "diff", "--name-only", base, "HEAD", "--", ROOT.name
        ).stdout.split()
        if path.removeprefix(prefix).startswith(PAGE_PATHS)
    ]
    before = git("show", f"{base}:{prefix}VERSION.json")
    version = current()[0]
    if not changed or before.returncode != 0:
        print(f"Version {version}: no check needed.")
        return
    was = load(before.stdout)["methodology"]["version"]
    if parts(version) <= parts(was):
        raise SystemExit(
            f"Page sources changed ({changed[0]}; {len(changed)} in all) but the version is still {was}. "
            "Raise the number in VERSION.json and add its entry at the top of CHANGELOG.md. "
            "README.md says which part of the number to raise."
        )
    print(f"Version raised from {was} to {version}.")


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else ""
    if command == "version":
        print(current()[0])
    elif command == "status":
        print(current()[2])
    elif command == "notes":
        print(release_notes(), end="")
    elif command == "check-bump" and len(sys.argv) == 3:
        check_bump(sys.argv[2])
    else:
        raise SystemExit(__doc__)
