"""Shared loaders, text handling and page shell for the methodology reference.

Everything analytical is read from pinned Git objects. Nothing here writes outside the
output directory passed to the build.
"""

import ast
import csv
import io
import json
import os
import re
import subprocess
from datetime import date
from functools import cache
from html import escape
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# Inside the method repository the reference sits at its root; otherwise the method, evidence and
# runtime checkouts are siblings two levels up. Each location can be overridden.
_INSIDE_METHOD = (ROOT.parent / "cookbook" / "pages.py").is_file()
WORKSPACE = ROOT.parents[1]
METHOD = Path(
    os.environ.get(
        "RURALSCAN_METHOD", ROOT.parent if _INSIDE_METHOD else WORKSPACE / "method"
    )
)
EVIDENCE = Path(os.environ.get("RURALSCAN_EVIDENCE", WORKSPACE / "evidence"))
RUNTIME = Path(os.environ.get("RURALSCAN_RUNTIME", WORKSPACE / "runtime"))
# The producer repository (recipe tables and evidence registers at the pinned revision).
CIAT = Path(os.environ.get("RURALSCAN_CIAT", WORKSPACE.parent / "nbs_ruralscan"))
CONTENT = ROOT / "content"

PIN = json.loads((EVIDENCE / "workflows/recipe_release/pin.json").read_text())
PRODUCER = PIN["source_revision"]
RELEASE = PIN["release_id"]
PRACTICE_IDS = list(PIN["practices"])


def _head(repo):
    return subprocess.check_output(
        ["git", "-C", str(repo), "rev-parse", "HEAD"], text=True
    ).strip()


METHOD_REV = _head(METHOD)
EVIDENCE_REV = _head(EVIDENCE)
CIAT_URL = f"https://github.com/CIAT/nbs_ruralscan/blob/{PRODUCER}/"
METHOD_URL = f"https://github.com/RuralScan/method/blob/{METHOD_REV}/"
EVIDENCE_URL = f"https://github.com/RuralScan/evidence/blob/{EVIDENCE_REV}/"


def _published(repo):
    """Revision of the published default branch, so links never point at local work."""
    try:
        return subprocess.check_output(
            ["git", "-C", str(repo), "rev-parse", "origin/main"],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (subprocess.CalledProcessError, OSError):
        return "main"


RUNTIME_REV = _published(RUNTIME)
RUNTIME_URL = f"https://github.com/RuralScan/runtime/blob/{RUNTIME_REV}/"
REPO_URLS = {"method:": METHOD_URL, "evidence:": EVIDENCE_URL, "runtime:": RUNTIME_URL}
# The visual methodology is published from the producer repository's documentation site.
VISUAL_URL = "https://ciat.github.io/nbs_ruralscan/redesign/"

# The live evidence dashboard. Everything about it is read from one published site revision,
# so its label, its two producer revisions and the list of drafts are never retyped here.
SITE_URL = "https://ruralscan.github.io/method/"
SITE_REV = "146b19f1285927a1d6c9ac51331e7d14686efef3"
# How this draft would be listed beside the others (same fields as the site's edition catalogue).
DRAFT_LABEL = "Methodology reference"
DRAFT_DATE = "2026-11-13"


def _site(path):
    try:
        return subprocess.check_output(
            ["git", "-C", str(METHOD), "show", f"{SITE_REV}:{path}"],
            text=True,
            stderr=subprocess.DEVNULL,
        )
    except (subprocess.CalledProcessError, OSError):
        raise SystemExit(
            f"Published site revision {SITE_REV[:8]} is not in {METHOD}. "
            "Run: git fetch origin gh-pages"
        ) from None


def _site_constant(name, script):
    found = re.search(rf'^\s*{name} = "([^"]+)"', script, re.MULTILINE)
    if not found:
        raise SystemExit(f"{name} is not defined in the published site build script")
    return found.group(1)


def _draft_label(label, day):
    return f"Draft · {label} · {date.fromisoformat(day):%d %b %Y}"


_SITE_SCRIPT = _site("publish_editions.py")
LIVE_LABEL = _site_constant("legacy_title", _SITE_SCRIPT)
LIVE_SNAPSHOT = _site_constant(
    "LIVE_PIN", _SITE_SCRIPT
)  # analytical snapshot of the live dashboard
LIVE_REVIEWS = _site_constant(
    "QUEUE_PIN", _SITE_SCRIPT
)  # review history shown in its queues
# Newest first, as the live selector lists them.
SITE_DRAFTS = [
    (
        f"{SITE_URL}editions/{e['edition']}/index.html",
        _draft_label(e["label"], e["date"]),
    )
    for e in reversed(json.loads(_site("editions.json")))
]
THIS_DRAFT = _draft_label(DRAFT_LABEL, DRAFT_DATE)
REVIEW_QUEUES = [
    ("T3", "review-t3", "Hazard findings"),
    ("T4", "review-t4", "Suitability findings"),
    ("T6", "review-t6", "Scorecard findings"),
]


def live(fragment="overview"):
    return f"{SITE_URL}dashboard.html#{fragment}"


TABLE_FILES = {
    "T4": "T4_suitability_mappings.json",
    "T3": "T3_nbs_hazard_farming.json",
    "T6": "T6_nbs_scorecard.json",
    "T6E": "T6E_economic_profile.json",
}
# One display name per table, used everywhere.
TABLE_NAMES = {
    "T0": "Practice registry",
    "T1": "Data registry",
    "T2": "Climate risk formulation",
    "T3": "Hazard responses",
    "T4": "Suitability mappings",
    "T5": "Opportunity-space variables",
    "T6": "Scorecard effects",
    "T6E": "Indicative economic profiles",
    "T7": "Geographic context",
    "SRC": "Source register",
    "EV": "Evidence register",
    "VONT": "Variable ontology",
    "FAM": "Suitability-family registry",
    "BIND": "Dataset bindings",
    "SRCH": "Search register",
    "XW": "Outcome crosswalk",
    "BANDS": "Magnitude bands",
    "TOOL": "Tool registry",
    "T4_RUN": "Suitability run policy",
    "T4_NUMERIC_POLICY": "Numeric compilation policy",
}
ROW_TABLES = ("T4", "T3", "T6", "T6E")


# ---------------------------------------------------------------- pinned reads


@cache
def pinned(path):
    return subprocess.check_output(
        ["git", "-C", str(CIAT), "show", f"{PRODUCER}:{path}"]
    )


def pinned_exists(path):
    return (
        subprocess.run(
            ["git", "-C", str(CIAT), "cat-file", "-e", f"{PRODUCER}:{path}"],
            capture_output=True,
            check=False,
        ).returncode
        == 0
    )


@cache
def pinned_json(path):
    return json.loads(pinned(path))


@cache
def pinned_csv(path):
    return list(csv.DictReader(io.StringIO(pinned(path).decode("utf-8"), newline="")))


def pinned_list(directory):
    out = subprocess.check_output(
        ["git", "-C", str(CIAT), "ls-tree", "-r", "--name-only", PRODUCER, directory],
        text=True,
    )
    return out.split("\n")[:-1]


# ---------------------------------------------------------------- text hygiene

# Fields that record who did something. The public reference shows what was decided, not who.
BLOCKED_KEYS = re.compile(
    r"(^|_)(reviewer|reviewed_by|reviewed_date|review_date|ratified_by|ratified_date|"
    r"searched_by|raised_by|extractor|library_path|extraction_run_id|mapping_reviewer|"
    r"mapping_review_date)$"
)


def _people():
    """Names to remove from recorded free text, kept in a local file that is not committed.

    One name per line; `name => replacement` overrides the default replacement.
    """
    path = Path(
        os.environ.get("RURALSCAN_PEOPLE", Path(__file__).with_name("people.local.txt"))
    )
    if not path.is_file():
        raise SystemExit(
            f"Missing {path.name}. Copy people.example.txt to people.local.txt and list the personal "
            "names that appear in recorded review notes, so they can be removed from public pages."
        )
    table = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#"):
            name, _, swap = line.partition("=>")
            table[name.strip()] = swap.strip() or "a reviewer"
    return table


PEOPLE = _people()
_NAMES = (
    "|".join(re.escape(n) for n in sorted(PEOPLE, key=len, reverse=True)) or r"(?!x)x"
)
_RULING = re.compile(r"(?:" + _NAMES + r")(?:[,:]?\s*\d{4}-\d{2}-\d{2})")
_PERSON = re.compile(r"\b(?:" + _NAMES + r")\b")
_START = re.compile(r"(^|[.!?]\s+|\"\s*)a reviewer")


def scrub(text):
    """Remove personal attributions from recorded free text."""
    if not isinstance(text, str) or not text:
        return text
    text = _RULING.sub("project ruling", text)
    text = _PERSON.sub(lambda m: PEOPLE[m.group(0)], text)
    text = re.sub(r"/Claude\b|\bClaude(?:-[a-z0-9.-]+)?\b", "", text)
    return _START.sub(lambda m: m.group(1) + "A reviewer", text)


def esc(value):
    return escape(str(value), quote=True)


def text(value):
    return esc(scrub(value) if isinstance(value, str) else value)


def words(value):
    """Turn an identifier into readable words without changing its meaning."""
    if value is None or value == "":
        return "Not recorded"
    out = str(value).replace("__", " · ").replace("_", " ")
    return out[:1].upper() + out[1:]


def link(href, label, cls=None):
    c = f' class="{cls}"' if cls else ""
    return f'<a href="{esc(href)}"{c}>{label}</a>'


def code(value):
    return f"<code>{esc(value)}</code>"


def badge(table):
    key = (
        table
        if table in {"T0", "T1", "T2", "T3", "T4", "T5", "T6", "T6E", "T7"}
        else "register"
    )
    return f'<span class="tb" data-t="{key}">{esc(table)}</span>'


def slug(value):
    return re.sub(r"[^a-zA-Z0-9_.-]+", "-", str(value)).strip("-")


def table(headers, rows, caption=None, cls="", ident=None, numeric=()):
    """Accessible data table. `rows` are lists of already-escaped HTML cells."""
    cap = f"<caption>{caption}</caption>" if caption else ""
    head = "".join(f'<th scope="col">{h}</th>' for h in headers)
    body = []
    for row in rows:
        cells = "".join(
            f'<td class="num">{c}</td>' if i in numeric else f"<td>{c}</td>"
            for i, c in enumerate(row)
        )
        body.append(f"<tr>{cells}</tr>")
    label = re.sub(r"<[^>]+>", "", caption) if caption else "Data table"
    i = f' id="{ident}"' if ident else ""
    return (
        f'<div class="tablewrap" role="region" aria-label="{esc(label)}" tabindex="0">'
        f'<table class="{cls}"{i}>{cap}<thead><tr>{head}</tr></thead>'
        f"<tbody>{''.join(body)}</tbody></table></div>"
    )


def dl(pairs, cls="facts"):
    items = "".join(
        f"<div><dt>{k}</dt><dd>{v}</dd></div>" for k, v in pairs if v not in (None, "")
    )
    return f'<dl class="{cls}">{items}</dl>'


def render_value(value, depth=0):
    """Render any recorded JSON value. Personal-attribution keys are left out."""
    if value is None or value == "" or value == [] or value == {}:
        return '<span class="none">Not recorded</span>'
    if isinstance(value, bool):
        return "Yes" if value else "No"
    if isinstance(value, (int, float)):
        return esc(value)
    if isinstance(value, str):
        return text(value)
    if isinstance(value, list):
        if all(not isinstance(v, (dict, list)) for v in value):
            return ", ".join(render_value(v) for v in value)
        return (
            "<ol class='nested'>"
            + "".join(f"<li>{render_value(v, depth + 1)}</li>" for v in value)
            + "</ol>"
        )
    if isinstance(value, dict):
        pairs = [
            (esc(words(k)), render_value(v, depth + 1))
            for k, v in value.items()
            if not BLOCKED_KEYS.search(k)
        ]
        return dl(pairs, "nested")
    return esc(value)


# ---------------------------------------------------------------- page shell

NAV = [
    ("index.html", "Overview"),
    ("method.html", "Method"),
    ("evidence-methods.html", "Evidence methods"),
    ("data-model.html", "Data model"),
    ("practices.html", "Practices"),
    ("evidence-base.html", "Evidence base"),
    ("editions.html", "Editions and checks"),
]
SIDE = {}  # section file -> [(href, label)], filled by the build before pages are written
PAGES = {}  # filename -> html, written at the end


def edition_line():
    return (
        f"Draft recipe edition <code>{RELEASE[:8]}</code> (candidate, not released) · "
        f"evidence registers at <code>{PRODUCER[:8]}</code>"
    )


def version_bar(filename):
    """The site's version selector: live dashboard first, every draft labelled Draft."""
    match = re.match(r"row-(t3|t4|t6)-", filename)
    target = live(f"review-{match.group(1)}" if match else "overview")
    name = LIVE_LABEL + (
        "" if match or filename == "index.html" else " (opens overview)"
    )
    options = [f'<option value="{esc(target)}">{esc(name)}</option>']
    options.append(
        f'<option value="{esc(filename)}" selected>{esc(THIS_DRAFT)} (this page)</option>'
    )
    options += [
        f'<option value="{esc(url)}">{esc(label)}</option>'
        for url, label in SITE_DRAFTS
    ]
    links = [link(target, esc(LIVE_LABEL))] + [
        link(url, esc(label)) for url, label in SITE_DRAFTS
    ]
    return (
        '<div class="edition-selector"><label for="dashboard-version">View version</label>'
        f'<select id="dashboard-version" aria-describedby="dashboard-version-note">{"".join(options)}</select>'
        '<span id="dashboard-version-note">Design preview. Draft for approval, not published.</span> '
        f'<a href="{esc(target)}">Return to live dashboard</a>'
        f"<noscript>{' · '.join(links)}</noscript></div>"
    )


def page(filename, section, title, body, crumbs=(), lead=None, toc=None):
    """Register one page. `section` is the nav file the page belongs to."""
    nav = []
    for i, (href, label) in enumerate(NAV, 1):
        cur = ' aria-current="page"' if href == section else ""
        nav.append(f'<a href="{href}"{cur}><span class="n">{i}</span> {esc(label)}</a>')
    side = ""
    entries = SIDE.get(section, [])
    if entries:
        number = [h for h, _ in NAV].index(section) + 1
        items = []
        for j, (href, label) in enumerate(entries, 1):
            cur = ' aria-current="page"' if href == filename else ""
            items.append(
                f'<li><a href="{href}"{cur}><span class="n">{number}.{j}</span> {esc(label)}</a></li>'
            )
        side = (
            '<nav class="side" aria-label="Section contents"><details open>'
            f"<summary>In this section</summary><ol>{''.join(items)}</ol></details></nav>"
        )
    trail = ""
    if crumbs:
        parts = [
            link(h, esc(lab)) if h else f"<span>{esc(lab)}</span>" for h, lab in crumbs
        ]
        trail = f'<nav class="crumbs" aria-label="Breadcrumb">{" › ".join(parts)}</nav>'
    onpage = ""
    if toc:
        onpage = (
            '<nav class="onpage" aria-label="On this page"><h2>On this page</h2><ul>'
            + "".join(f'<li><a href="#{i}">{esc(t)}</a></li>' for i, t in toc)
            + "</ul></nav>"
        )
    intro = f'<p class="lead">{lead}</p>' if lead else ""
    html = f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)} · Rural NbS Scan methodology reference</title>
<link rel="stylesheet" href="site.css"></head>
<body>
<a class="skip" href="#main">Skip to content</a>
{version_bar(filename)}
<header class="mast"><div class="wrap">
<a class="brand" href="index.html">Rural NbS Scan</a>
<span class="sub">Methodology reference</span>
<span class="ed">{edition_line()} · <a href="editions.html">about editions</a></span>
<a class="review-entry" href="{live("review-queue")}">Review queue</a>
</div>
<nav class="tabs" aria-label="Sections"><div class="wrap">{"".join(nav)}</div></nav></header>
<div class="wrap layout{" with-side" if side else ""}">
{side}
<main id="main">{trail}<h1>{esc(title)}</h1>{intro}{onpage}
{body}
</main></div>
<footer><div class="wrap"><p>{edition_line()} · method definitions <code>{METHOD_REV[:8]}</code> ·
evidence workflows <code>{EVIDENCE_REV[:8]}</code>. Scoping reference: it flags where to look;
local feasibility assessment validates. <a href="editions.html">Editions and checks</a> ·
<a href="glossary.html">Glossary</a></p></div></footer>
<script src="site.js" defer></script>
</body></html>
"""
    if filename in PAGES:
        raise ValueError(f"Duplicate page {filename}")
    PAGES[filename] = html


# ---------------------------------------------------------------- shared naming


def _cookbook_names():
    """Read practice, product and family display names from the method cookbook (single home)."""
    source = (METHOD / "cookbook/pages.py").read_text()
    start = source.index("PRACTICES = {")
    end = source.index("\ndef ", start)
    scope = {}

    def value(node):
        # Literal dictionaries, tuples and strings, plus names assigned earlier in the slice.
        if isinstance(node, ast.Constant):
            return node.value
        if isinstance(node, ast.Tuple):
            return tuple(value(e) for e in node.elts)
        if isinstance(node, ast.Dict):
            return {
                value(k): value(v) for k, v in zip(node.keys, node.values, strict=True)
            }
        if isinstance(node, ast.Name) and node.id in scope:
            return scope[node.id]
        raise ValueError(
            f"Unexpected expression in cookbook names: {ast.dump(node)[:80]}"
        )

    for node in ast.parse(source[start:end]).body:
        if isinstance(node, ast.Assign) and isinstance(node.targets[0], ast.Name):
            scope[node.targets[0].id] = value(node.value)
    return scope["PRACTICES"], scope["PRODUCTS"], scope["FAMILIES"]


PRACTICE_TEXT, PRODUCTS, FAMILY_TEXT = _cookbook_names()


def practice_name(nbs_id):
    row = pinned_json(f"schema/recipes/{nbs_id}/T0_nbs_registry.json")[0]
    return row["nbs_name"]


def family_name(family_id):
    if family_id in FAMILY_TEXT:
        return FAMILY_TEXT[family_id][0]
    return words(family_id.split("__", 1)[-1]) if family_id else "Practice-wide"


def row_id(row):
    return row.get("mapping_id") or row["record_id"]


def row_file(table_id, row):
    return f"row-{table_id.lower()}-{slug(row_id(row))}.html"


def source_file(source_id):
    return f"source-{slug(source_id)}.html"
