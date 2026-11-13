"""Rebuild every shared dashboard edition, then leave the latest at the site root."""
from datetime import date
from html import escape
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


HUMAN_REVIEW_CORRECTION = "2ff6f85e-d1568d72ffa3"


# Routes common to the pre-cookbook dashboard and edition-based dashboard.
LEGACY = {
    "index.html": "#overview",
    "progress.html": "#progress",
    "methods.html": "#methods/rural",
    "ai.html": "#methods/evidence",
    "searches.html": "#methods/search",
    "table-T1.html": "#datasets",
}


def add_version_selectors(site, editions):
    """Decorate the published dashboard shell after all pinned builds complete."""
    pages = {}
    labels = {}
    for item in editions:
        key = item["edition"]
        labels[key] = f'{item["label"]} · {date.fromisoformat(item["date"]):%d %b %Y}'
        pages[key] = {p.name for p in (site / "editions" / key).glob("*.html")}
        if "index.html" not in pages[key]:
            raise ValueError(f"No dashboard entry for {key}")
    # The legacy source drawer accepts progress source keys, IDs and aliases.
    legacy_snapshot = site / "data/bec50bc0f9dc/dashboard_data.json"
    sources = json.loads(legacy_snapshot.read_text())["progress_overview"]["sources"]
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
    labels[latest] += " (latest)"
    legacy_title = "Original evidence dashboard · 10 Nov 2026"
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
        if page.startswith("source-") and page.endswith(".html"):
            source_id = page.removeprefix("source-").removesuffix(".html")
            if source_id in legacy_keys:
                legacy_dest = "#source=" + quote(legacy_keys[source_id], safe="")
        legacy_match = legacy_dest is not None
        legacy_dest = legacy_dest or "#overview"
        legacy_url = base + "legacy.html" + legacy_dest
        legacy_label = legacy_title
        if not legacy and not legacy_match:
            legacy_label += " (opens overview)"
        selected = " selected" if legacy else ""
        fallback = "" if legacy_match else " data-fallback"
        options.append(f'<option value="{legacy_url}"{selected}{fallback}>{legacy_label}</option>')
        links.append(f'<a href="{legacy_url}">{legacy_label}</a>')
        kind = ' data-legacy="true"' if legacy else ""
        note = ("Switching opens the matching section when available, otherwise the overview."
                if legacy else "Switching opens the same page when available.")
        control = (
            '<div class="edition-selector"><label for="dashboard-version">View version</label>'
            f'<select id="dashboard-version" aria-describedby="dashboard-version-note"{kind}>'
            + "".join(options) + f'</select><span id="dashboard-version-note">{note}</span>'
            + "<noscript>" + " · ".join(links) + "</noscript></div>"
        )
        review_record = (page.startswith(("review", "claim-", "row-"))
                         or page in {"terrace.html", "method-decisions.html"})
        if not legacy and current != latest and page.startswith("review"):
            control += (
                '<nav class="archived-review-links" aria-label="Live reviewer workspace">'
                '<a href="https://ciat.github.io/nbs_ruralscan/dashboard.html#review-queue">Open the CIAT review queue</a>'
                f'<a href="{base}editions/{latest}/review.html">Choose a finding review batch</a>'
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
        assets = (f'<link rel="stylesheet" href="{base}edition-selector.css">'
                  f'<script defer src="{base}edition-selector.js"></script>')
        path.write_text(contents.replace("</head>", assets + "</head>", 1))

    for key, names in pages.items():
        # workbook.html is also the downloadable, byte-verified release artefact.
        for name in names - {"workbook.html"}:
            decorate(site / "editions" / key / name, key, name)
    for name in ("index.html", "dashboard.html"):
        decorate(site / name, latest, "index.html")
    decorate(site / "legacy.html", "legacy", "index.html")


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

        add_version_selectors(site, editions)


if __name__ == "__main__":
    main()
