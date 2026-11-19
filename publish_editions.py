"""Publish pinned editions, the active review workspace and the selected methodology home."""
import csv
from review.build import compose as compose_review
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


# The dashboard is a page of its own, so it has its own entry in the version menu and its own tab symbol.
DASHBOARD_LABEL = "Evidence dashboard · current"
_TILE = ("<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24'><rect width='24' height='24' rx='5' fill='#0b0f19'/>"
         "<g fill='none' stroke='#10b981' stroke-width='{width}' stroke-linecap='round' stroke-linejoin='round'{place}>"
         "{glyph}</g></svg>")
TAB_ICONS = {
    # An open book: the methodology and its earlier drafts.
    "methodology": _TILE.format(width="2", place=" transform='translate(2.6 2.6) scale(0.78)'",
                                glyph="<path d='M2 3h6a4 4 0 0 1 4 4v14a3 3 0 0 0-3-3H2z'/>"
                                      "<path d='M22 3h-6a4 4 0 0 0-4 4v14a3 3 0 0 1 3-3h7z'/>"),
    # Three bars on a baseline: the evidence dashboard.
    "dashboard": _TILE.format(width="2.6", place="", glyph="<path d='M7.5 16.5v-3.5M12 16.5v-9M16.5 16.5v-6'/>"
                                                           "<path d='M5 19.5h14' stroke-width='1.4'/>"),
}


def dashboard_forward():
    """The old address of the superseded overview. It was the same dashboard under a notice, so it forwards
    to the dashboard and keeps the view that was asked for."""
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Evidence dashboard</title>'
            '<link rel="canonical" href="dashboard.html">' + tab_icon("dashboard")
            + '<script>location.replace("dashboard.html" + location.search + location.hash)</script>'
            '<noscript><meta http-equiv="refresh" content="0;url=dashboard.html"></noscript></head>'
            '<body><a href="dashboard.html">Open the evidence dashboard</a></body></html>')


def tab_icon(kind):
    """A link element that gives a page its browser-tab symbol. The image is inline, so no path can break."""
    return f'<link rel="icon" type="image/svg+xml" href="data:image/svg+xml,{quote(TAB_ICONS[kind], safe="")}">'


def reference_version(site, reference):
    """The methodology states its own version and date. The site reads them and never retypes them."""
    try:
        stated = json.loads((site / reference["href"]).with_name("version.json").read_text())
        number, status = stated["version"], stated["status"]
        day = date.fromisoformat(stated["date"])
    except (OSError, ValueError, KeyError, TypeError):
        raise ValueError("Default Methodology states no version; stop publication and retain the deployed site") from None
    if not re.fullmatch(r"(0|[1-9]\d*)(\.(0|[1-9]\d*)){2}", number) or status not in {"draft", "released"}:
        raise ValueError("Default Methodology states no version; stop publication and retain the deployed site")
    label = f'{escape(reference["label"])} v{number} · {day:%d %b %Y}'
    return label, "Current draft" if status == "draft" else "Current release"


def publish_reference_menu(site, reference, labels, label, note):
    """The publishing branch owns navigation, even when reference content is pinned earlier."""
    for path in (site / "reference").rglob("*.html"):
        base = "../" * len(path.parent.relative_to(site).parts)
        row = re.match(r"row-(t3|t4|t6)-", path.name)
        dashboard_route = "review-" + row[1] if row else "overview"
        groups = [
            ("Live", [(base + reference["href"], label, True),
                      (base + "dashboard.html#" + dashboard_route, DASHBOARD_LABEL, False)]),
            ("Earlier drafts", [(base + f"editions/{key}/index.html", escape(value), False)
                                for key, value in reversed(labels.items())]),
        ]
        menu = "".join(f'<optgroup label="{group}">' + "".join(
            f'<option value="{escape(url, quote=True)}"' + (" selected" if selected else "") + f'>{text}</option>'
            for url, text, selected in items) + '</optgroup>' for group, items in groups)
        links = " · ".join(f'<strong>{group}</strong> ' + " · ".join(
            f'<a href="{escape(url, quote=True)}">{text}</a>' for url, text, _ in items) for group, items in groups)
        contents = path.read_text()
        substitutions = [
            (r'(<select id="dashboard-version"[^>]*>).*?</select>', lambda m: m[1] + menu + '</select>'),
            (r'<span id="dashboard-version-note">.*?</span>', f'<span id="dashboard-version-note">{note}</span>'),
            (r'<a class="vb-live" href="[^"]*">[^<]*</a>', f'<a class="vb-live" href="{base}dashboard.html#review-queue">Review queue</a>'),
            (r'<a class="review-entry" href="[^"]*">Review queue</a>'
             r'(?:\s*<a class="help-entry github-entry"[^>]*>GitHub</a>)?',
             f'<a class="review-entry" href="{base}dashboard.html#review-queue">Review queue</a> '
             '<a class="help-entry github-entry" href="https://github.com/RuralScan/method" target="_blank" '
             'rel="noopener" title="RuralScan methodology on GitHub (opens a new tab)">GitHub</a>'),
            (r'<noscript>.*?</noscript>', '<noscript>' + links + '</noscript>'),
        ]
        for pattern, replacement in substitutions:
            contents, count = re.subn(pattern, replacement, contents, flags=re.S)
            if count != 1:
                raise ValueError(f"Expected one shared navigation element in {path}: {pattern}")
        if 'rel="icon"' not in contents:
            contents = contents.replace("</head>", tab_icon("methodology") + "</head>", 1)
        path.write_text(contents)


def add_version_selectors(site, editions, ciat, reference):
    """Decorate the published dashboard shell after all pinned builds complete."""
    pages = {}
    labels = {}
    for item in editions:
        key = item["edition"]
        number = f'v{item["version"]} · ' if item.get("version") else ""
        labels[key] = f'{number}{item["label"]} · {date.fromisoformat(item["date"]):%d %b %Y}'
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
    legacy_title = "Evidence dashboard · 10 Nov 2026"
    reference_available = reference is not None and (site / reference["href"]).is_file()
    promoted = bool(reference and reference.get("default"))
    if promoted and (not reference_available or (site / "reference/NOT-FOR-PUBLICATION.txt").exists()):
        raise ValueError("Default Methodology is unavailable; stop publication and retain the deployed site")
    if promoted and any('<meta name="robots" content="noindex">' in p.read_text()
                        for p in (site / "reference").rglob("*.html")):
        raise ValueError("Default Methodology is not approved for public listing")
    reference_label, reference_note = reference_version(site, reference) if reference_available else (None, None)
    for asset in ("edition-selector.css", "edition-selector.js"):
        copyfile(Path(__file__).with_name(asset), site / asset)

    def decorate(path, current, page):
        legacy = current == "legacy"
        root_shell = current in {"legacy", "review"}
        base = "" if root_shell else "../../"
        options, links = [], []
        for target, label in reversed(labels.items()):
            match = not root_shell and page in pages[target]
            dest = page if match else "index.html"
            suffix = " (opens overview)" if not match and not root_shell else ""
            href = f"{base}editions/{target}/{dest}"
            name = escape(label + suffix)
            selected = " selected" if target == current else ""
            same = " data-match" if match else ("" if root_shell else " data-fallback")
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
        if promoted:
            # One dashboard, one entry. An earlier draft's page opens the matching dashboard view.
            href = base + escape(reference["href"], quote=True)
            dashboard_url = base + "dashboard.html" + ("" if root_shell else legacy_dest)
            unmatched = not root_shell and not legacy_match
            dashboard_label = DASHBOARD_LABEL + (" (opens overview)" if unmatched else "")
            # The dashboard is not the methodology: it selects its own entry, never the methodology's.
            selected = " selected" if current == "review" else ""
            fallback = " data-fallback" if unmatched else ""
            groups = [(reference["group"],
                       f'<option value="{href}">{reference_label}</option>'
                       f'<option value="{dashboard_url}"{selected}{fallback}>{dashboard_label}</option>',
                       f'<a href="{href}">{reference_label}</a> · <a href="{dashboard_url}">{dashboard_label}</a>')]
        else:
            legacy_url = base + "legacy.html" + legacy_dest
            legacy_label = legacy_title
            if not root_shell and not legacy_match:
                legacy_label += " (opens overview)"
            selected = " selected" if legacy else ""
            fallback = "" if legacy_match else " data-fallback"
            groups = [("Live", f'<option value="{legacy_url}"{selected}{fallback}>{legacy_label}</option>',
                       f'<a href="{legacy_url}">{legacy_label}</a>')]
            if reference_available:
                href = base + escape(reference["href"], quote=True)
                groups.append((reference["group"], f'<option value="{href}">{reference_label}</option>',
                               f'<a href="{href}">{reference_label}</a>'))
        groups.append(("Earlier drafts", "".join(options), " · ".join(links)))
        menu = "".join(f'<optgroup label="{escape(group)}">{items}</optgroup>' for group, items, _ in groups)
        plain_links = " · ".join(f'<strong>{escape(group)}</strong> {items}' for group, _, items in groups)
        kind = ' data-legacy="true"' if root_shell else ""
        label = "Version" if root_shell else "View version"
        if current == "review":
            note = ""
        elif legacy:
            note = "Review findings against their sources."
        else:
            note = "Design preview."
        note_visibility = "" if note else " hidden"
        control = (
            f'<label for="dashboard-version">{label}</label>'
            f'<select id="dashboard-version" aria-describedby="dashboard-version-note"{kind}>'
            + menu + f'</select><span id="dashboard-version-note"{note_visibility}>{note}</span>'
            + ("" if root_shell else f' <a href="{base}dashboard.html#review-queue">Open review queue</a>')
            + f"<noscript>{plain_links}</noscript>"
        )
        if not root_shell:
            control = '<div class="edition-selector">' + control + '</div>'
        review_record = (page.startswith(("review", "claim-", "row-"))
                         or page in {"terrace.html", "method-decisions.html"})
        if not root_shell and current != latest and page.startswith("review"):
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
        if root_shell:
            route_data = json.dumps(legacy_routes, separators=(",", ":")).replace("<", "\\u003c")
            control += f'<script type="application/json" id="legacy-version-routes">{route_data}</script>'
        contents = path.read_text()
        header = contents.find("<header")
        if header < 0 or "</head>" not in contents:
            raise ValueError(f"Missing dashboard shell in {path}")
        if root_shell:
            marker = "<!-- Published version menu -->"
            if contents.count(marker) != 1:
                raise ValueError("Live dashboard must have one version menu slot")
            contents = contents.replace(marker, control)
            if (site / "reference/help.html").is_file():
                contents = contents.replace('href="https://ciat.github.io/nbs_ruralscan/redesign/help.html"',
                                            'href="reference/help.html"')
        else:
            contents = contents[:header] + control + contents[header:]
        assets = (f'<link rel="stylesheet" href="{base}edition-selector.css?v=2">'
                  f'<script defer src="{base}edition-selector.js"></script>')
        if 'rel="icon"' not in contents:
            assets += tab_icon("methodology")
        path.write_text(contents.replace("</head>", assets + "</head>", 1))

    for key, names in pages.items():
        # workbook.html is also the downloadable, byte-verified release artefact.
        for name in names - {"workbook.html"}:
            decorate(site / "editions" / key / name, key, name)
    # Draft builders write root entry points. Install the review shell last, then
    # promote only the explicitly selected home. Existing hash bookmarks retain their route.
    live = site / "legacy.html"
    # Navigation can use a later edition. Rating status uses a separately verified assessment.
    status = json.loads((site / "editions" / latest / "review-status.json").read_text())
    batches = {eid: finding["live_batch"] for eid, finding in status["findings"].items()
               if finding.get("live_batch")}
    navigation = json.dumps(batches, separators=(",", ":")).replace("<", "\\u003c")
    batch_data = f'<script type="application/json" id="ciat-review-batches">{navigation}</script>'
    t3 = json.dumps(live_rating_reviews(site, ciat, snapshot["recipes"]), separators=(",", ":")).replace("<", "\\u003c")
    rating_data = f'<script type="application/json" id="live-t3-reviews">{t3}</script>'
    link = f'<link rel="describedby" type="application/ld+json" href="editions/{latest}/catalog.json">'
    live.write_text(compose_review(live.read_text()))
    queue_file = publish_review_queue(site, ciat, snapshot)
    queue_meta = f'<meta name="ciat-review-snapshot" content="{queue_file}">'
    live.write_text(live.read_text().replace("</head>", link + batch_data + rating_data + queue_meta + "</head>", 1))
    copyfile(live, site / "dashboard.html")
    if promoted:
        # One dashboard. The old address of its superseded overview forwards to it.
        decorate(site / "dashboard.html", "review", "index.html")
        live.write_text(dashboard_forward())
        publish_reference_menu(site, reference, labels, reference_label, reference_note)
        for name in ("index.html", "home-route.js"):
            copyfile(Path(__file__).with_name(name), site / name)
    else:
        decorate(live, "legacy", "index.html")
        decorate(site / "dashboard.html", "legacy", "index.html")
        copyfile(site / "dashboard.html", site / "index.html")
    (site / "review.html").write_text(
        '<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Evidence review queue</title>'
        '<meta http-equiv="refresh" content="0;url=dashboard.html#review-queue"></head>'
        '<body><a href="dashboard.html#review-queue">Open the evidence review queue</a></body></html>'
    )
    for name in (("dashboard.html",) if promoted else ("index.html", "dashboard.html", "legacy.html")):
        contents = (site / name).read_text()
        expected_title = DASHBOARD_LABEL if promoted and name == "dashboard.html" else legacy_title
        if ('id="tab-qaqc"' not in contents or 'id="vf-scope"' not in contents
                or 'src="dashboard-tables.js?' not in contents or f' selected>{expected_title}</option>' not in contents):
            raise ValueError(f"{name} must retain evidence review and select its own edition")



def main():
    site = Path("site").resolve()
    ciat = Path("producer").resolve()
    with TemporaryDirectory() as tmp:
        method = repository(Path(tmp), "method", "RuralScan/method")
        evidence = repository(Path(tmp), "evidence", "RuralScan/evidence")
        catalog = json.loads(Path("editions.json").read_text())
        editions = [entry for entry in catalog if "edition" in entry]
        reference = next((entry for entry in catalog if entry.get("href") == "reference/index.html"), None)
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

        add_version_selectors(site, editions, ciat, reference)


if __name__ == "__main__":
    main()
