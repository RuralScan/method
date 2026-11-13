"""Rebuild every shared dashboard edition, then publish the November 10 evidence dashboard at the site root."""
import csv
from datetime import date
from html import escape
import io
import json
from pathlib import Path
import re
from shutil import copyfile
import subprocess
import sys
from tempfile import TemporaryDirectory
from urllib.parse import quote


def git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True)


def repository(parent, name, remote):
    repo = parent / name
    repo.mkdir()
    git(repo, "init", "--quiet")
    git(repo, "remote", "add", "origin", "https://github.com/" + remote + ".git")
    git(repo, "config", "remote.origin.promisor", "true")
    git(repo, "config", "remote.origin.partialclonefilter", "blob:none")
    return repo


def fetch(repo, revision):
    if not re.fullmatch("[0-9a-f]{40}", revision):
        raise ValueError(f"Expected full commit: {revision}")
    exists = subprocess.run(["git", "-C", str(repo), "cat-file", "-e", revision + "^{commit}"],
                            stderr=subprocess.DEVNULL).returncode == 0
    if not exists:
        git(repo, "fetch", "--no-tags", "--depth=1", "--filter=blob:none", "origin", revision)


LIVE_PIN = "bec50bc0f9dc74b3d5ffafcf881571a8a8ec5c06"
LIVE_REVIEW_EDITION = "2ff6f85e-a3151a5dbc32"
LIVE_REVIEW_PIN = "e5c8da02e72810956cfd179cb32cd137fc4ba398"


# Public review queues track a separate CIAT revision from the analytical dashboard.
QUEUE_PIN = "e43c42bd581dba791ce1f1697b6b41952ab0cfe3"
REVIEW_TABLES = {"T3": "T3_nbs_hazard_farming", "T6": "T6_nbs_scorecard"}


def archived_citations(ciat, membership):
    """Find the most recent mainline table that cited each formerly used finding."""
    def output(*args):
        return subprocess.check_output(["git", "-C", str(ciat), *args])

    # A shallow edition checkout cannot establish when a finding disappeared.
    with TemporaryDirectory() as tmp:
        if output("rev-parse", "--is-shallow-repository").strip() == b"true":
            ciat = repository(Path(tmp), "history", "CIAT/nbs_ruralscan")
            git(ciat, "fetch", "--no-tags", "--filter=blob:none", "origin", QUEUE_PIN)
        table_for = {f"{key}.csv": table for table, key in REVIEW_TABLES.items()}
        versions = output("log", "--first-parent", "--raw", "--no-renames", "--no-abbrev", "--format=%H", QUEUE_PIN,
                          "--", *(f"schema/recipes/*/{name}" for name in table_for)).decode().splitlines()
        blobs = {}
        for line in versions:
            if line.startswith(":"):
                change, path = line.split("\t")
                oid = change.split()[3]
                if oid.strip("0"):
                    blobs.setdefault((oid, table_for[Path(path).name]), (revision, path))
            elif line:
                revision = line

        # Fetch all historical table blobs together in a partial checkout.
        promisor = subprocess.run(["git", "-C", str(ciat), "config", "--get", "remote.origin.promisor"],
                                  capture_output=True).stdout.strip()
        if promisor == b"true" and blobs:
            git(ciat, "fetch", "--no-tags", "--no-write-fetch-head", "origin", *sorted({oid for oid, _ in blobs}))
        current = {key: set(ids) for key, ids in membership.items()}
        former = {key: {} for key in REVIEW_TABLES}
        for (oid, table), (revision, path) in blobs.items():
            for row in csv.DictReader(io.StringIO(output("cat-file", "blob", oid).decode())):
                for eid in json.loads(row.get("evidence_ids") or "[]"):
                    if eid not in current[table]:
                        former[table].setdefault(eid, f"{revision}/{path}")
        return former


def publish_review_queue(site, ciat, base):
    """Package current queue inputs as a delta against the immutable dashboard data."""
    fetch(ciat, QUEUE_PIN)

    def blob(path):
        return subprocess.check_output(["git", "-C", str(ciat), "show", f"{QUEUE_PIN}:{path}"])

    data = json.loads(blob("docs/dashboard_data.json"))
    logged = list(csv.DictReader(io.StringIO(blob("pipeline/metrics/review_log.csv").decode())))
    fields = ("date", "evidence_id", "reviewer", "decision")
    if [[r.get(k, "") for k in fields] for r in data["review_log"]] != [[r[k] for k in fields] for r in logged]:
        raise ValueError("CIAT dashboard history differs from the committed finding review log")
    payload = {key: data[key] for key in ("review_priorities", "gaps", "t4_review_notes", "qaqc_stats", "decoded_classes")}
    payload["review_log"] = logged
    payload["row_reviews"] = [
        {k: r[k] for k in ("date", "record_id", "nbs_id", "table", "decision", "reviewer", "reason", "note")}
        for r in csv.DictReader(io.StringIO(blob("pipeline/metrics/row_review_log.csv").decode()))
    ]
    payload["membership"] = {
        table: sorted({eid for recipe in data["recipes"].values() for row in recipe[key] for eid in row.get("evidence_ids", [])})
        for table, key in REVIEW_TABLES.items()
    }
    payload["formerly_cited"] = archived_citations(ciat, payload["membership"])
    # The September archive records pre-synthesis T3/T6 lane assignments.
    # Keep its review history separate from findings demonstrably cited by a rating.
    archive = "schema/registers/_deferred/EV_T3_T6_deferred_2026-09.csv"
    deferred = {row["evidence_id"]: row for row in csv.DictReader(io.StringIO(blob(archive).decode()))}
    known = {table: set(ids) | payload["formerly_cited"][table].keys()
             for table, ids in payload["membership"].items()}
    payload["deferred_reviews"] = []
    for event in logged:
        row = deferred.get(event["evidence_id"])
        if not row or event["date"][:10] > "2026-09-17":
            continue
        table = {"climate_risk": "T3", "nbs_effect": "T6"}[row["use_role"]]
        if row["evidence_id"] not in known[table]:
            payload["deferred_reviews"].append({**event, "table": table, "nbs_id": row["nbs_id"]})
    payload["deferred_register"] = archive
    payload["register_changes"] = {}
    for name, key in (("EV_evidence_register", "evidence_id"), ("SRC_source_register", "source_id")):
        old = {r[key]: r for r in base["registers"][name]}
        new = {r[key]: r for r in data["registers"][name]}
        payload["register_changes"][name] = {
            "changed": [row for rid, row in new.items() if old.get(rid) != row],
            "removed": sorted(old.keys() - new.keys()),
        }
    payload.update(revision=QUEUE_PIN, base_revision=LIVE_PIN)
    name = f"data/review-{QUEUE_PIN[:12]}-{LIVE_PIN[:12]}.json"
    (site / name).write_text(json.dumps(payload, separators=(",", ":")))
    return name


def live_rating_reviews(site, ciat, recipes):
    """Reuse the assessed ratings only after proving the producer inputs match."""
    assessed = json.loads((site / "editions" / LIVE_REVIEW_EDITION / "review-status.json").read_text())
    if assessed["producer_revision"] != LIVE_REVIEW_PIN:
        raise ValueError("Unexpected historical assessment revision")
    # The later CIAT commit changed structural T4 records. The effect compiler
    # reads only nbs_effect and asset_vulnerability units. Verify both populations.
    ev = "schema/registers/EV_evidence_register"
    git(ciat, "diff", "--quiet", LIVE_REVIEW_PIN, LIVE_PIN, "--", "schema",
        "src/nbs_ruralscan/recipe", "scripts/synthesise-t3t6.py", "pipeline/metrics/review_log.csv",
        "pipeline/metrics/row_review_log.csv", f":(exclude){ev}.csv", f":(exclude){ev}.json")
    def effect_units(pin):
        raw = subprocess.check_output(["git", "-C", str(ciat), "show", f"{pin}:{ev}.json"])
        return [unit for unit in json.loads(raw) if unit.get("use_role") in {"nbs_effect", "asset_vulnerability"}]
    if effect_units(LIVE_PIN) != effect_units(LIVE_REVIEW_PIN):
        raise ValueError("Live T3 evidence differs from the assessed population")
    statuses = {}
    for recipe in recipes.values():
        for row in recipe["T3_nbs_hazard_farming"]:
            key = row["record_id"]
            review = assessed["rows"][key]
            rating = row.get("asset_sensitivity") or row.get("mitigation_potential")
            if (review["table"] != "T3" or review["producer_revision"] != LIVE_REVIEW_PIN
                    or review["evidence_ids"] != row["evidence_ids"] or review["rating"] != rating
                    or review["confidence"] != row["confidence"]):
                raise ValueError(f"Live hazard rating differs from assessed row {key}")
            statuses[key] = {"provisional": review["provisional"], "coverage": review["coverage"],
                             "unresolved": len(review["unresolved_setter_ids"])}
    return statuses


HUMAN_REVIEW_CORRECTION = "2ff6f85e-d1568d72ffa3"


# Routes common to the pre-cookbook dashboard and edition-based dashboard.
LEGACY = {
    "index.html": "#overview",
    "review.html": "#review-queue",
    "review-t3.html": "#review-t3",
    "review-t4.html": "#review-t4",
    "review-t6.html": "#review-t6",
    "progress.html": "#progress",
    "methods.html": "#methods/rural",
    "ai.html": "#methods/evidence",
    "searches.html": "#methods/search",
    "table-T1.html": "#datasets",
}


def add_version_selectors(site, editions, ciat):
    """Decorate the published dashboard shell after all pinned builds complete."""
    pages = {}
    labels = {}
    for item in editions:
        key = item["edition"]
        labels[key] = f'Draft · {item["label"]} · {date.fromisoformat(item["date"]):%d %b %Y}'
        pages[key] = {p.name for p in (site / "editions" / key).glob("*.html")}
        if "index.html" not in pages[key]:
            raise ValueError(f"No dashboard entry for {key}")
    # The legacy source drawer accepts progress source keys, IDs and aliases.
    legacy_snapshot = site / "data/bec50bc0f9dc/dashboard_data.json"
    snapshot = json.loads(legacy_snapshot.read_text())
    sources = snapshot["progress_overview"]["sources"]
    legacy_keys = {}
    candidates = {}
    for source in sources:
        key = source["key"]
        ids = [s for s in dict.fromkeys([source.get("source_id"), key, *source.get("aliases", [])]) if s]
        candidates[key] = ids
        for identifier in ids:
            legacy_keys.setdefault(identifier, key)
    legacy_routes = {}
    for edition, names in pages.items():
        routes = {}
        for key, ids in candidates.items():
            destination = next((f"source-{i}.html" for i in ids if f"source-{i}.html" in names), None)
            if destination:
                for identifier in ids:
                    exact = f"source-{identifier}.html"
                    routes.setdefault("#source=" + identifier, exact if exact in names else destination)
        routes.update({fragment: path for path, fragment in LEGACY.items() if path in names})
        legacy_routes[edition] = routes
    latest = editions[-1]["edition"]
    legacy_title = "Live · Evidence dashboard · 10 Nov 2026"
    for asset in ("edition-selector.css", "edition-selector.js"):
        copyfile(Path(__file__).with_name(asset), site / asset)

    def decorate(path, current, page):
        legacy = current == "legacy"
        base = "" if legacy else "../../"
        options, links = [], []
        for target, label in reversed(labels.items()):
            match = not legacy and page in pages[target]
            dest = page if match else "index.html"
            suffix = " (opens overview)" if not match and not legacy else ""
            href = f"{base}editions/{target}/{dest}"
            name = escape(label + suffix)
            selected = " selected" if target == current else ""
            same = " data-match" if match else ("" if legacy else " data-fallback")
            options.append(f'<option value="{href}" data-edition="{target}"{selected}{same}>{name}</option>')
            links.append(f'<a href="{href}">{name}</a>')
        legacy_dest = LEGACY.get(page)
        practice_review = re.fullmatch(r"review-(t[346])-[a-z_]+\.html", page)
        if practice_review:
            legacy_dest = "#review-" + practice_review[1]
        if page.startswith("source-") and page.endswith(".html"):
            source_id = page.removeprefix("source-").removesuffix(".html")
            if source_id in legacy_keys:
                legacy_dest = "#source=" + quote(legacy_keys[source_id], safe="")
        legacy_match = legacy_dest is not None
        legacy_dest = legacy_dest or "#overview"
        legacy_url = base + "dashboard.html" + legacy_dest
        legacy_label = legacy_title
        if not legacy and not legacy_match:
            legacy_label += " (opens overview)"
        selected = " selected" if legacy else ""
        fallback = "" if legacy_match else " data-fallback"
        options.insert(0, f'<option value="{legacy_url}"{selected}{fallback}>{legacy_label}</option>')
        links.insert(0, f'<a href="{legacy_url}">{legacy_label}</a>')
        kind = ' data-legacy="true"' if legacy else ""
        note = "" if legacy else "Design preview."
        control = (
            '<div class="edition-selector"><label for="dashboard-version">View version</label>'
            f'<select id="dashboard-version" aria-describedby="dashboard-version-note"{kind}>'
            + "".join(options) + f'</select><span id="dashboard-version-note">{note}</span>'
            + ("" if legacy else f' <a href="{legacy_url}">Return to live dashboard</a>')
            + "<noscript>" + " · ".join(links) + "</noscript></div>"
        )
        review_record = (page.startswith(("review", "claim-", "row-"))
                         or page in {"terrace.html", "method-decisions.html"})
        if not legacy and current != latest and page.startswith("review"):
            control += (
                '<nav class="archived-review-links" aria-label="Live reviewer workspace">'
                '<a href="https://ciat.github.io/nbs_ruralscan/dashboard.html#review-queue">Open the CIAT review queue</a>'
                f'<a href="{base}dashboard.html#review-queue">Review findings by table</a>'
                '</nav>'
            )
        if current == HUMAN_REVIEW_CORRECTION and latest != current and review_record:
            if page in pages[latest]:
                corrected_path, caption = page, "Open this page in the corrected edition"
            else:
                corrected_path, caption = "review.html", "Open Review in the corrected edition"
            if corrected_path not in pages[latest]:
                raise ValueError(f"Corrected edition lacks a review destination for {page}")
            control += (
                '<aside class="edition-correction" aria-label="Correction to review status">'
                '<strong>Correction to human review status.</strong> This archived edition counted '
                'automated checks as human sign-offs for some findings. '
                f'<a href="{base}editions/{latest}/{corrected_path}">{caption}</a>.</aside>'
            )
        if legacy:
            route_data = json.dumps(legacy_routes, separators=(",", ":")).replace("<", "\\u003c")
            control += f'<script type="application/json" id="legacy-version-routes">{route_data}</script>'
        contents = path.read_text()
        header = contents.find("<header")
        if header < 0 or "</head>" not in contents:
            raise ValueError(f"Missing dashboard shell in {path}")
        contents = contents[:header] + control + contents[header:]
        assets = (f'<link rel="stylesheet" href="{base}edition-selector.css?v=2">'
                  f'<script defer src="{base}edition-selector.js"></script>')
        path.write_text(contents.replace("</head>", assets + "</head>", 1))

    for key, names in pages.items():
        # workbook.html is also the downloadable, byte-verified release artefact.
        for name in names - {"workbook.html"}:
            decorate(site / "editions" / key / name, key, name)
    # Draft builders write their own root entry points. Publish the live shell last:
    # adding an edition never promotes a design or invalidates a shared draft URL.
    live = site / "legacy.html"
    decorate(live, "legacy", "index.html")
    # Navigation can use a later edition. Rating status uses a separately verified assessment.
    status = json.loads((site / "editions" / latest / "review-status.json").read_text())
    batches = {eid: finding["live_batch"] for eid, finding in status["findings"].items()
               if finding.get("live_batch")}
    navigation = json.dumps(batches, separators=(",", ":")).replace("<", "\\u003c")
    batch_data = f'<script type="application/json" id="ciat-review-batches">{navigation}</script>'
    t3 = json.dumps(live_rating_reviews(site, ciat, snapshot["recipes"]), separators=(",", ":")).replace("<", "\\u003c")
    rating_data = f'<script type="application/json" id="live-t3-reviews">{t3}</script>'
    link = f'<link rel="describedby" type="application/ld+json" href="editions/{latest}/catalog.json">'
    queue_file = publish_review_queue(site, ciat, snapshot)
    queue_meta = f'<meta name="ciat-review-snapshot" content="{queue_file}">'
    live.write_text(live.read_text().replace("</head>", link + batch_data + rating_data + queue_meta + "</head>", 1))
    for name in ("index.html", "dashboard.html"):
        copyfile(live, site / name)
    (site / "review.html").write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Evidence review queue</title>'
        '<meta http-equiv="refresh" content="0;url=dashboard.html#review-queue"></head>'
        '<body><a href="dashboard.html#review-queue">Open the evidence review queue</a></body></html>'
    )
    for name in ("index.html", "dashboard.html", "legacy.html"):
        contents = (site / name).read_text()
        if ('id="tab-qaqc"' not in contents or 'href="#review-t3"' not in contents
                or 'href="#review-t4"' not in contents or f' selected>{legacy_title}</option>' not in contents):
            raise ValueError(f"{name} must open the live evidence dashboard with T3 and T4 review")



def main():
    site = Path("site").resolve()
    ciat = Path("producer").resolve()
    with TemporaryDirectory() as tmp:
        method = repository(Path(tmp), "method", "RuralScan/method")
        evidence = repository(Path(tmp), "evidence", "RuralScan/evidence")
        editions = json.loads(Path("editions.json").read_text())
        for edition in editions:
            fetch(method, edition["method"])
            git(method, "checkout", "--quiet", "--detach", edition["method"])
            fetch(evidence, edition["evidence"])
            fetch(ciat, edition["producer"])
            fetch(ciat, edition["progress"])
            target = site / "editions" / edition["edition"]
            if target.exists():
                raise ValueError(f"Repeated edition: {target}")
            subprocess.run([sys.executable, "-B", str(method/"dashboard/build.py"),
                            "--out", str(site), "--evidence", str(evidence), "--ciat", str(ciat)], check=True)
            subprocess.run([sys.executable, "-B", str(method/"dashboard/check.py"), str(target)], check=True)

        add_version_selectors(site, editions, ciat)


if __name__ == "__main__":
    main()
