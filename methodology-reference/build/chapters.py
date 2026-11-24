"""Render authored chapters: front matter, directives, links, citations, pinned rule tables."""

import re
import json

import markdown
from core import (
    BLOCKED_KEYS,
    CIAT_URL,
    CONTENT,
    METHOD,
    PRACTICE_IDS,
    REPO_URLS,
    TABLE_NAMES,
    esc,
    pinned_csv,
    pinned_exists,
    table,
    text,
    words,
)

METHOD_CH = [
    "scope-and-framework",
    "scoping-walkthrough",
    "m0-setup",
    "m1-suitability",
    "farming-systems-and-data",
    "m2-climate-risk",
    "m2b-project-risk",
    "m3-characterisation",
    "m4-hotspots",
    "m5-scorecard",
    "m6-handoff",
    "implementing-the-method",
]
EVIDENCE_CH = [
    "evidence-principles",
    "discovery",
    "acquisition",
    "extraction",
    "review-and-quality",
    "compiling-evidence",
    "suitability-synthesis",
    "effect-synthesis",
    "cost-profiles",
]
PRACTICE_CH = [f"practice-{p}" for p in PRACTICE_IDS]
GENERATED = {
    "editions": "editions.html",
    "glossary": "glossary.html",
    "evidence-base": "evidence-base.html",
    "reproduce": "reproduce.html",
    "status": "status.html",
}
ATTRIBUTION = (
    "These framework primitives are inherited from earlier Alliance of Bioversity International and "
    "CIAT work by B. Kenduiywo: the five fuzzy membership functions and the hybrid AHP + CRITIC + "
    "Entropy weighting scheme from the version 2 methodology plan (sections 4 and 7); the "
    "recipe-template and sub-practice-family patterns from the water-harvesting recipe (sections 2.2 "
    "and 1); and the reference MCDA implementation, <code>reference/R/spatMCDA.R</code>."
)
PROBLEMS = []  # collected for the build check
WORDS = {}


def chapter_file(slug):
    if slug in GENERATED:
        return GENERATED[slug]
    if slug.startswith("practice-"):
        return slug + ".html"
    return f"ch-{slug}.html"


def read(slug):
    path = CONTENT / f"{slug}.md"
    if not path.is_file():
        return None, None
    raw = path.read_text()
    meta = {}
    if raw.startswith("---"):
        head, _, raw = raw[3:].partition("\n---")
        key = None
        for line in head.splitlines():
            if re.match(r"^[a-z_]+:", line):
                key, _, value = line.partition(":")
                meta[key] = value.strip().strip("\"'")
            elif line.strip().startswith("- ") and key:
                meta.setdefault(key + "_list", []).append(line.strip()[2:].strip())
    return meta, raw.strip()


def priority_workflow():
    policy = json.loads((METHOD / "data-model/priority-contract.json").read_text())
    scores = " · ".join(f"{name.title()} {score:g}" for name, score in policy["class_scores"].items())
    steps = [
        ("M1 · Candidate area", "Opportunity space", "Keep excluded and unknown areas separate."),
        ("M2 / M3 · Inputs", "T2 + T5 variables", "Read each concern in its native unit."),
        ("M3 · Classification", "Problem classes", scores),
        ("M3 · Overlap check", "One concern, one entry", "Check correlations; record representative choices."),
        ("M4 · User priorities", "Choose weights", "Show each weight; zero excludes a concern."),
        ("M4 · Priority map", "Sum ÷ total weight", "Add weight × class score; divide by the sum of weights."),
    ]
    items = "".join(f'<li><small>{esc(stage)}</small><strong>{esc(title)}</strong><span>{esc(note)}</span></li>'
                    for stage, title, note in steps)
    return ('<figure class="priority-workflow"><ol class="priority-flow">' + items + '</ol>'
            '<figcaption>Figure 1. Classify concerns, check overlap, then apply user weights inside '
            'the opportunity space. M2b investment-risk screening stays separate.</figcaption></figure>')


def _csv_table(spec, slug):
    parts = spec.split("|")
    path = parts[0].strip()
    options = dict(p.split("=", 1) for p in parts[1:] if "=" in p)
    if not pinned_exists(path):
        PROBLEMS.append(f"{slug}: csv directive path not found at the pin: {path}")
        return f'<p class="empty">Rule table not found at the pinned revision: {esc(path)}</p>'
    rows = pinned_csv(path)
    if "where" in options:
        col, _, val = options["where"].partition("=")
        rows = [r for r in rows if r.get(col.strip()) == val.strip()]
    if "exclude" in options:
        col, separator, val = options["exclude"].partition("=")
        if not separator or (rows and col.strip() not in rows[0]):
            PROBLEMS.append(f"{slug}: invalid csv exclusion {options['exclude']!r} in {path}")
        else:
            rows = [r for r in rows if r.get(col.strip()) != val.strip()]
    columns = [
        c
        for c in (rows[0].keys() if rows else [])
        if not BLOCKED_KEYS.search(c) and c not in {"date", "ruled_by"}
    ]
    if "cols" in options:
        wanted = [c.strip() for c in options["cols"].split(",")]
        missing = [c for c in wanted if rows and c not in rows[0]]
        if missing:
            PROBLEMS.append(
                f"{slug}: csv directive names unknown columns {missing} in {path}"
            )
        columns = [c for c in wanted if c in columns]
    total = len(rows)
    if "limit" in options:
        rows = rows[: int(options["limit"])]
    body = [[text(r.get(c, "")) for c in columns] for r in rows]
    more = (
        f" (first {len(rows)} of {total} rows)"
        if len(rows) < total
        else f" ({total} rows)"
    )
    caption = f'{esc(options.get("caption", "Pinned rule table"))} <a href="{CIAT_URL}{esc(path)}"><code>{esc(path)}</code></a>{more}'
    return table([esc(words(c)) for c in columns], body, caption=caption, cls="rule")


def _locate(target):
    """Return (url, path) for a source path, honouring the method:/evidence:/runtime: prefixes."""
    for prefix, base in REPO_URLS.items():
        if target.startswith(prefix):
            return base + target[len(prefix) :], target[len(prefix) :]
    return CIAT_URL + target, target


def _src(match):
    target = match.group(1).strip()
    section = (match.group(2) or "").strip()
    href, label = _locate(target)
    tail = f" §{esc(section)}" if section else ""
    return f'<cite class="src"><a href="{esc(href)}">{esc(label.split("/")[-1])}</a>{tail}</cite>'


def _wiki(match, slug):
    kind, _, rest = match.group(1).partition(":")
    target, _, label = rest.partition("|")
    target, label = target.strip(), label.strip()
    if kind == "ch":
        known = set(METHOD_CH) | set(EVIDENCE_CH) | set(PRACTICE_CH) | set(GENERATED)
        if target not in known:
            PROBLEMS.append(f"{slug}: link to unknown chapter {target}")
            return esc(label or target)
        return f'<a href="{chapter_file(target)}">{esc(label or TITLES.get(target, words(target.replace("-", " "))))}</a>'
    if kind == "table":
        if target not in TABLE_NAMES:
            PROBLEMS.append(f"{slug}: link to unknown table {target}")
            return esc(label or target)
        return f'<a href="table-{target}.html">{esc(label or f"{TABLE_NAMES[target]} ({target})")}</a>'
    if kind == "var":
        return f'<a href="variables.html#var-{esc(target)}"><code>{esc(label or target)}</code></a>'
    if kind == "practice":
        return (
            f'<a href="practice-{esc(target)}.html">{esc(label or words(target))}</a>'
        )
    PROBLEMS.append(f"{slug}: unknown link kind {kind}")
    return esc(label or target)


TITLES = {}


def titles():
    for slug in METHOD_CH + EVIDENCE_CH + PRACTICE_CH:
        meta, _ = read(slug)
        if meta:
            TITLES[slug] = meta.get("title", words(slug))
    TITLES.update(
        {
            "editions": "Versions and editions",
            "glossary": "Glossary",
            "evidence-base": "Evidence base",
            "reproduce": "Reproduce and check",
            "status": "What is established",
        }
    )


def chapter_body(slug):
    """Return (html, [(heading id, heading text)]) for one authored chapter."""
    meta, raw = read(slug)
    if raw is None:
        PROBLEMS.append(f"{slug}: chapter file missing")
        return '<p class="empty">This chapter has not been written yet.</p>', []
    WORDS[slug] = len(re.findall(r"\w+", raw))
    if re.search(
        r"<[a-zA-Z/][^>]*>", re.sub(r"```.*?```|`[^`]*`", "", raw, flags=re.DOTALL)
    ):
        PROBLEMS.append(f"{slug}: raw HTML in chapter text")

    blocks = {}

    def stash(html):
        key = f"\n\nXXBLOCK{len(blocks)}XX\n\n"
        blocks[key.strip()] = html
        return key

    raw = re.sub(
        r"^\{\{csv:([^}]+)\}\}\s*$",
        lambda m: stash(_csv_table(m.group(1), slug)),
        raw,
        flags=re.MULTILINE,
    )
    raw = re.sub(
        r"^\{\{attribution:primitives\}\}\s*$",
        lambda m: stash(f'<p class="attribution">{ATTRIBUTION}</p>'),
        raw,
        flags=re.MULTILINE,
    )
    raw = re.sub(r"^\{\{priority-workflow\}\}\s*$", lambda m: stash(priority_workflow()),
                 raw, flags=re.MULTILINE)
    leftover = re.findall(r"\{\{[^}]*\}\}", raw)
    if leftover:
        PROBLEMS.append(f"{slug}: unresolved directives {leftover[:3]}")
    inline = {}

    def keep(html):
        key = f"XXINLINE{len(inline)}XX"
        inline[key] = html
        return key

    raw = re.sub(r"\[\[([^\]]+)\]\]", lambda m: keep(_wiki(m, slug)), raw)
    raw = re.sub(
        r"\[src:\s*([^\]§]+?)\s*(?:§\s*([^\]]+))?\]", lambda m: keep(_src(m)), raw
    )
    md = markdown.Markdown(
        extensions=["tables", "fenced_code", "toc", "sane_lists"],
        extension_configs={"toc": {"toc_depth": "2-3"}},
    )
    html = md.convert(raw)
    html = re.sub(r"<p>Table: (.*?)</p>\s*<table>", r"<table><caption>\1</caption>", html, flags=re.S)
    html = html.replace(
        "<table>", '<div class="tablewrap" tabindex="0"><table>'
    ).replace("</table>", "</table></div>")
    for key, value in blocks.items():
        html = html.replace(f"<p>{key}</p>", value).replace(key, value)
    for key, value in inline.items():
        html = html.replace(key, value)
    html = html.replace(
        '<pre><code class="language-formula">', '<pre class="formula"><code>'
    )
    toc = [(t["id"], t["name"]) for t in md.toc_tokens if t["level"] == 2]
    sources = meta.get("sources_list") or []
    if sources:
        items = []
        for s in sources:
            items.append(
                f'<li><a href="{esc(_locate(s)[0])}"><code>{esc(s)}</code></a></li>'
            )
        html += f'<h2 id="chapter-sources">Sources for this chapter</h2><ul class="sources">{"".join(items)}</ul>'
        toc.append(("chapter-sources", "Sources for this chapter"))
    return html, toc


def summary(slug):
    meta, _ = read(slug)
    return (meta or {}).get("summary", "")
