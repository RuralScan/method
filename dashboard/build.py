"""Build the standalone, immutable public dashboard edition from pinned inputs."""

import argparse
import json
import shutil
from hashlib import sha256
from html import escape
from pathlib import Path

import progress
import recipes
import reference

HERE = Path(__file__).resolve().parent
METHOD = HERE.parent
TABS = [
    ("overview", "Overview", "index.html"),
    ("methods", "Methods", "methods.html"),
    ("recipes", "Practice recipes", "recipes.html"),
    ("synthesis", "Evidence synthesis", "synthesis.html"),
    ("evidence", "Evidence", "evidence.html"),
    ("progress", "Progress", "progress.html"),
]
SUBTABS = {
    "methods": [
        ("Scan method", "methods.html"),
        ("Data model", "model.html"),
        ("Table dictionary", "dictionary.html"),
        ("AI workflow & human review", "ai.html"),
    ],
    "synthesis": [
        ("Worked example", "terrace.html"),
        ("Site suitability", "synthesis-t4.html"),
        ("Hazard effects", "synthesis-t3.html"),
        ("Scorecard", "synthesis-t6.html"),
        ("Costs", "synthesis-t6e.html"),
    ],
    "evidence": [
        ("Findings & sources", "evidence.html"),
        ("Recorded searches", "searches.html"),
    ],
}
REVIEW = "https://ciat.github.io/nbs_ruralscan/dashboard.html#review-queue"


def edition_id():
    digest = sha256()
    for path in sorted(
        [p for p in HERE.iterdir() if p.suffix in {".py", ".css", ".js", ".html"}]
        + [METHOD / "design/tables.css", METHOD / "cookbook/pages.py"]
    ):
        digest.update(path.name.encode() + b"\0" + path.read_bytes() + b"\0")
    return "2ff6f85e-" + digest.hexdigest()[:12]


def nav_link(href, label, active):
    current = ' aria-current="page"' if active else ""
    return f'<a href="{href}"{current}>{escape(label)}</a>'


def document(title, content):
    return f'<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(title)} · RuralScan</title><link rel="stylesheet" href="site.css"><link rel="stylesheet" href="tables.css"><script src="site.js" defer></script></head><body>{content}</body></html>'


def shell(filename, section, title, body, edition):
    section = section.lower()
    number = [t[0] for t in TABS].index(section) + 1
    nav = "".join(
        nav_link(url, f"{i}. {label}", key == section)
        for i, (key, label, url) in enumerate(TABS, 1)
    )
    active = filename
    if filename.startswith("table-"):
        active = "dictionary.html"
    if filename.startswith("search-"):
        active = "searches.html"
    if filename.startswith(("claim-", "source-")):
        active = "evidence.html"
    if filename.startswith("row-"):
        active = "synthesis-" + filename.split("-")[1] + ".html"
    sub = "".join(
        nav_link(href, f"{number}.{i} {name}", active == href)
        for i, (name, href) in enumerate(SUBTABS.get(section, []), 1)
    )
    subnav = (
        f'<nav aria-label="Section topics" class="subtabs">{sub}</nav>' if sub else ""
    )
    return document(
        title,
        f'<a class="skip" href="#main">Skip to content</a><header class="mast"><div class="wrap"><a class="brand" href="index.html">RuralScan</a><small>Rural nature-based solutions · Methodology dashboard</small><a class="review" href="{REVIEW}">Reviewer workspace ↗</a></div></header><div class="bar"><div class="wrap"><nav class="tabs" aria-label="Dashboard sections">{nav}</nav>{subnav}</div></div><main id="main"><h1>{escape(title)}</h1>{body}</main><footer>Candidate cookbook 2ff6f85e · Progress bec50bc0 · {reference.link("edition.html", "Edition and build sources")} · {escape(edition)}</footer>',
    )


def overview(ciat, practices, coverage):
    choices = "".join(
        reference.link(recipes.recipe_file(p), recipes.practice_name(p))
        for p in practices
    )
    steps = [
        (
            "Define the question",
            "Select the area, practices and project priorities. A shared framework sets the steps; each practice has its own recipe.",
        ),
        (
            "Find the opportunity space",
            "Combine practice requirements with spatial data, host-system gates and hard exclusions.",
        ),
        (
            "Assess risk and priorities",
            "Distinguish risks to livelihoods from risks to the investment. Examine who and what overlaps candidate locations.",
        ),
        (
            "Compare and hand over",
            "Compare expected benefits, limitations and evidence gaps. Identify local feasibility checks.",
        ),
    ]
    figure = "".join(
        f"<li><b>{name}</b><span>{text}</span></li>" for name, text in steps
    )
    return f"""<div class="hero"><div><p class="lead">Shortlist practices and locations for local assessment across rural, agricultural and forestry landscapes.</p><p>This candidate cookbook covers six practices. Use the recipe to see what supports a siting decision and what still needs local investigation.</p><p><a href="methods.html#M6">Country pilot and implementation handoff →</a></p></div>
    <aside class="walk"><h2>Can bench terraces work at 350 mm/year?</h2><p>Forward-sloping benches have been documented in this rainfall range. Their rainfall suitability score remains unassigned.</p><a class="action" href="terrace.html">Follow the evidence →</a></aside></div>
    <h2>Choose a practice</h2><nav class="tiles" aria-label="Practice recipes">{choices}</nav>
    <h2>Research effort</h2>{progress.summary(ciat)}{coverage}
    <figure><h2>How the scan works</h2><ol class="steps">{figure}</ol><figcaption>Figure 1.1. Evidence supports the recipes. The country runtime applies them to an area.</figcaption></figure>
    <p><a href="ai.html">How people and AI maintain the evidence</a> · <a href="model.html">Explore the data model</a></p>"""


def entry(overview_html, edition):
    base = f"editions/{edition}/"
    routes = {
        "overview": "index.html",
        "progress": "progress.html",
        "methods/rural": "methods.html",
        "methods/evidence": "ai.html",
        "methods/search": "searches.html",
        "datasets": "table-T1.html",
    }
    # Granular historical URLs keep their original record population and hash.
    bridge = f"""<base href="{base}"><script>
const oldHash=location.hash.slice(1), routes={json.dumps(routes)};
if(oldHash) location.replace(Object.hasOwn(routes,oldHash) ? new URL(routes[oldHash],document.baseURI) : new URL("../../legacy.html"+location.hash,document.baseURI));
</script>"""
    return overview_html.replace(
        '<meta charset="utf-8">', '<meta charset="utf-8">' + bridge
    )


def build(out, evidence, ciat):
    edition = edition_id()
    target = out / "editions" / edition
    target.mkdir(parents=True, exist_ok=True)
    seen = set()

    def write(relative, section, title, body):
        if relative in seen or Path(relative).name != relative:
            raise ValueError(relative)
        seen.add(relative)
        if relative == "evidence.html":
            body = '<section id="find">' + body + "</section>"
        if relative == "progress.html":
            body = (
                "<h2>Cookbook coverage</h2>"
                + coverage
                + "<h2>Recorded research effort</h2>"
                + body
            )
        (target / relative).write_text(shell(relative, section, title, body, edition))

    pub = recipes.generate(target, evidence, ciat, write)
    family_rows = sum(bool(row["family"]) for row in pub["rows"])
    total = len(pub["rows"])
    coverage = (
        f"<p><strong>{total:,} candidate analytical rows</strong> in cookbook edition {pub['release_id'][:8]}. "
        f"{family_rows} carry family IDs, including cross-family context; {total - family_rows} apply practice-wide, "
        'with their recorded conditions. <a href="edition.html">Inspect edition coverage</a>.</p>'
    )
    suitability = [row["fields"] for row in pub["rows"] if row["table"] == "T4"]
    totals = pub["totals"]
    readiness = (
        sum(int(f["Function options"]) > 0 for f in suitability),
        sum(f["Function selected"] == "Yes" for f in suitability),
        sum(f["Spatially validated"] == "Yes" for f in suitability),
    )
    reference.generate(METHOD, ciat, write)
    progress.generate(target, evidence, ciat, write)
    write(
        "ai.html",
        "Methods",
        "AI workflow and human review",
        (HERE / "ai.html").read_text()
        + '<p><a href="searches.html">Inspect actual search runs</a> · <a href="terrace.html">Inspect the resulting terrace decision</a></p>',
    )
    pin = json.loads(
        recipes.snapshot(
            evidence, recipes.EVIDENCE, "workflows/recipe_release/pin.json"
        )
    )
    if (
        sha256(
            (METHOD / "data-model/definition-snapshot.json").read_bytes()
        ).hexdigest()
        != pin["method"]["sha256"]
        or pin["method"]["revision"] != reference.METHOD
        or pin["source_revision"] != reference.PRODUCER
    ):
        raise ValueError("Definition or producer revision differs from release pin")
    write(
        "index.html",
        "Overview",
        "Where could rural nature-based solutions work?",
        overview(ciat, pin["practices"], coverage),
    )
    editions = [
        (
            "Candidate workbook",
            recipes.EVIDENCE_BASE + "workflows/recipe_release/pin.json",
            pin["release_id"],
        ),
        (
            "Candidate analytical records",
            "https://github.com/CIAT/nbs_ruralscan/tree/" + reference.PRODUCER,
            reference.PRODUCER,
        ),
        (
            "Method definitions",
            reference.BASE + "/definition-snapshot.json",
            reference.METHOD,
        ),
        (
            "Progress snapshot",
            progress.SOURCE + "/docs/dashboard_data.json",
            progress.REVISION,
        ),
        (
            "Historical terrace replay",
            recipes.EVIDENCE_BASE + "examples/terrace-rainfall/README.md",
            "2023cb82",
        ),
        (
            "Evidence publication",
            "https://github.com/RuralScan/evidence/tree/" + recipes.EVIDENCE,
            recipes.EVIDENCE,
        ),
    ]
    provenance = "".join(
        f"<dt>{name}</dt><dd>{reference.link(url, value)}</dd>"
        for name, url, value in editions
    )
    write(
        "edition.html",
        "Overview",
        "Edition and build sources",
        f'<p>Dashboard build <code>{edition}</code>. Edition-specific record URLs retain this build when shared. The historical search and progress snapshot has its own counting basis.</p><dl>{provenance}</dl><h2>Candidate coverage</h2><p>{totals["T3"]} hazard responses, {totals["T4"]} suitability mappings, {totals["T6"]} scorecard effects and {totals["T6E"]} economic records. Of the {len(suitability)} suitability mappings, {readiness[0]} have function options, {readiness[1]} have selected functions and {readiness[2]} carry producer-recorded spatial validation. These categories overlap.</p><p><a href="workbook.html" download>Download the candidate workbook</a> · <a href="../../legacy.html#overview">Open the previous dashboard edition</a></p>',
    )
    for path in [HERE / "site.css", HERE / "site.js", METHOD / "design/tables.css"]:
        shutil.copyfile(path, target / path.name)
    home = entry((target / "index.html").read_text(), edition)
    for name in ["index.html", "dashboard.html"]:
        (out / name).write_text(home)
    print(f"{edition} · {len(seen):,} static pages")
    return target


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    for argument in ("out", "evidence", "ciat"):
        parser.add_argument("--" + argument, type=Path, required=True)
    args = parser.parse_args()
    build(args.out, args.evidence, args.ciat)
