"""Overview, section indexes, authored chapters, editions, status and glossary."""

import json
import subprocess
from collections import Counter
from itertools import pairwise

import data
from chapters import (
    EVIDENCE_CH,
    METHOD_CH,
    TITLES,
    WORDS,
    chapter_body,
    chapter_file,
    summary,
)
from core import (
    CIAT,
    CIAT_URL,
    CONTACTS,
    EVIDENCE,
    EVIDENCE_LIVE,
    EVIDENCE_REV,
    EVIDENCE_URL,
    LIVE_LABEL,
    LIVE_RATING_STATUS,
    LIVE_REVIEWS,
    LIVE_SNAPSHOT,
    METHOD,
    METHOD_REV,
    PIN,
    PRACTICE_IDS,
    PRACTICE_TEXT,
    PRODUCER,
    PRODUCTS,
    RELEASE,
    REVIEW_QUEUES,
    ROW_TABLES,
    RUNTIME,
    RUNTIME_URL,
    SIDE,
    SITE_REV,
    TABLE_NAMES,
    VISUAL_URL,
    badge,
    code,
    esc,
    link,
    live,
    page,
    practice_name,
    source_file,
    table,
    words,
)
from core import family_name as core_family_name
from pages_evidence import practices_of

MODULES = [
    ("M0", "Setup and scope", "m0-setup", ["T0", "T1", "T7"]),
    ("M1", "Suitability to opportunity space", "m1-suitability", ["T1", "T4", "T7"]),
    ("M2", "Climate risk to livelihoods", "m2-climate-risk", ["T1", "T2"]),
    ("M2b", "Project disaster risk screen", "m2b-project-risk", ["T2", "T3"]),
    ("M3", "Opportunity-space characterisation", "m3-characterisation", ["T1", "T5"]),
    ("M4", "Priority hotspots", "m4-hotspots", ["T5"]),
    ("M5", "Scorecard and response", "m5-scorecard", ["T3", "T6"]),
    ("M6", "Implementation hand-off", "m6-handoff", ["T0", "T6"]),
]
TERRACE = "water_harvesting__terracing__annual_precipitation"


STAGES = [
    ("01-setup.html", "Setup", "m0-setup"),
    ("02-practices.html", "Explore the practices", "scoping-walkthrough"),
    ("03-opportunity.html", "Opportunity space", "m1-suitability"),
    ("04-risk.html", "Project risk", "m2b-project-risk"),
    ("05-hotspots.html", "Priority hotspots", "m4-hotspots"),
    ("06-comparison.html", "NbS comparison", "m5-scorecard"),
    ("07-next.html", "Next steps", "m6-handoff"),
]


def review_queues():
    """Entry points to the live review queues, kept visible wherever review is mentioned."""
    items = [f'<li><a href="{live("review-queue")}">Review queue</a></li>'] + [
        f'<li><a href="{live(anchor)}">{t} · {esc(label)}</a></li>'
        for t, anchor, label in REVIEW_QUEUES
    ]
    return f'<ul class="queues">{"".join(items)}</ul>'


def _committed(revision, repo=CIAT):
    """Commit date of a revision, when the checkout has it. The producer checkout by default."""
    try:
        return subprocess.check_output(
            ["git", "-C", str(repo), "log", "-1", "--format=%cs", revision],
            text=True,
            stderr=subprocess.DEVNULL,
        ).strip()
    except (subprocess.CalledProcessError, OSError):
        return ""


def live_pins():
    ciat = "https://github.com/CIAT/nbs_ruralscan/tree/"
    seed = json.loads((EVIDENCE / "registers/manifest.json").read_text())[
        "source_revision"
    ]
    return table(
        ["What", "Revision", "Committed", "Used for"],
        [
            [
                "This reference",
                link(ciat + PRODUCER, code(PRODUCER[:12])),
                _committed(PRODUCER),
                "Every row, finding, source and count on these pages",
            ],
            [
                "Live dashboard, analytical snapshot",
                link(ciat + LIVE_SNAPSHOT, code(LIVE_SNAPSHOT[:12])),
                _committed(LIVE_SNAPSHOT),
                "Tables, progress and evidence shown outside the review queues",
            ],
            [
                "Live dashboard, review records",
                link(
                    EVIDENCE_LIVE + "publication/review-queue.json",
                    "Evidence repository, current main branch",
                ),
                "Read when the page loads",
                (
                    "Findings, sources, finding and rating review histories and the membership of review batches "
                    "shown in the review queues"
                ),
            ],
            [
                "Live dashboard, archived reviews and review batches",
                link(ciat + LIVE_REVIEWS, code(LIVE_REVIEWS[:12])),
                _committed(LIVE_REVIEWS),
                (
                    "Archived finding reviews, the base list of review batches, suitability review notes and links to "
                    "earlier tables, built into the site"
                ),
            ],
            [
                "Live dashboard, hazard-rating review status",
                link(ciat + LIVE_RATING_STATUS, code(LIVE_RATING_STATUS[:12])),
                _committed(LIVE_RATING_STATUS),
                (
                    "Provisional status of hazard ratings, used after checking that the effect evidence "
                    "is unchanged at the analytical snapshot"
                ),
            ],
            [
                "Published site",
                link(
                    "https://github.com/RuralScan/method/tree/" + SITE_REV,
                    code(SITE_REV[:12]),
                ),
                _committed(SITE_REV, METHOD),
                f"The site revision that serves the live “{esc(LIVE_LABEL)}”",
            ],
            [
                "Evidence repository, starting registers",
                link(ciat + seed, code(seed[:12])),
                _committed(seed),
                "The records the evidence repository started from when it took over writing evidence and review records",
            ],
        ],
        caption="Three producer revisions and the evidence repository’s current records are in play. "
        "This reference does not combine counts from different sources.",
        ident="pins",
    )


def stages_block():
    """The seven stages of the visual methodology, each with its screen and its chapter."""
    items = "".join(
        f"<li><strong>{esc(name)}</strong> {link(VISUAL_URL + screen, 'screen')} · "
        f"{link(chapter_file(slug_), 'method')}</li>"
        for screen, name, slug_ in STAGES
    )
    return (
        "<p>The same method is also shown as seven stages a task team would walk through, in the "
        f"{link(VISUAL_URL + 'index.html', 'visual methodology')}: an interactive mock-up of what a full "
        "realisation of the method could look like. Every number and map on its screens is example data, "
        "not a result. "
        f"{link(chapter_file('scoping-walkthrough'), 'The scoping walkthrough')} follows the stages one by one, "
        "links each to the chapter behind it and records where the screens and the written specification differ. "
        f"{link(chapter_file('implementing-the-method'), 'Implementing the method')} states what any software "
        f"implementation must respect and points to the {link(RUNTIME_URL + 'README.md', 'runtime repository')}.</p>"
        f'<ol class="pipeline">{items}</ol>'
    )


def flow_figure():
    """Module flow. Geometry is fixed; labels and links come from MODULES."""
    w, h, bw, bh = 1080, 320, 158, 76
    main = ["M0", "M1", "M3", "M4", "M5", "M6"]
    x = {m: 14 + i * 178 for i, m in enumerate(main)}
    y1, y2 = 36, 214
    pos = {m: (x[m], y1) for m in main}
    pos["M2b"] = (x["M1"] + 60, y2)
    pos["M2"] = (x["M3"] + 90, y2)
    info = {m[0]: m for m in MODULES}
    out = [
        f'<svg viewBox="0 0 {w} {h}" role="img" aria-labelledby="flow-t flow-d" class="flow">',
        '<title id="flow-t">How the modules connect</title>',
        (
            '<desc id="flow-d">Setup feeds suitability, which produces the opportunity space. The opportunity space is characterised, '
            "prioritised into hotspots, summarised in a scorecard and handed off. Climate risk to livelihoods enters hotspot "
            "prioritisation as a need layer. The project disaster risk screen is applied to the opportunity space as a filter and is never summed.</desc>"
        ),
        (
            '<defs><marker id="arr" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
            '<path d="M0,0 L10,5 L0,10 z" class="arrowhead"/></marker></defs>'
        ),
    ]
    for a, b in pairwise(main):
        out.append(
            f'<line x1="{pos[a][0] + bw}" y1="{y1 + bh / 2}" x2="{pos[b][0] - 3}" y2="{y1 + bh / 2}" class="arrow" marker-end="url(#arr)"/>'
        )
    mx, my = pos["M2"]
    out.append(
        f'<path d="M{mx + bw / 2},{my} L{mx + bw / 2},{y1 + bh + 34} L{x["M4"] + bw / 2},{y1 + bh + 34} L{x["M4"] + bw / 2},{y1 + bh + 4}" class="arrow" marker-end="url(#arr)" fill="none"/>'
    )
    out.append(
        f'<text x="{mx + bw / 2 + 8}" y="{my - 12}" class="note">need layer</text>'
    )
    bx, by = pos["M2b"]
    tx = x["M1"] + bw + 10
    out.append(
        f'<path d="M{bx + bw / 2},{by} L{bx + bw / 2},{y1 + bh + 34} L{tx},{y1 + bh + 34} L{tx},{y1 + bh / 2 + 6}" class="arrow dashed" marker-end="url(#arr)" fill="none"/>'
    )
    out.append(
        f'<text x="{bx - 4}" y="{by - 12}" class="note" text-anchor="end">filter, never summed</text>'
    )
    for mid, (px, py) in pos.items():
        _, name, slug_, tables = info[mid]
        lines, line = [], ""
        for word in name.split():
            if line and len(line) + len(word) + 1 > 22:
                lines.append(line)
                line = word
            else:
                line = f"{line} {word}".strip()
        lines.append(line)
        label = "".join(
            f'<tspan x="{px + 10}" dy="{0 if i == 0 else 13}">{esc(t)}</tspan>'
            for i, t in enumerate(lines[:2])
        )
        out.append(
            f'<a href="{chapter_file(slug_)}"><g class="mod"><rect x="{px}" y="{py}" width="{bw}" height="{bh}" rx="6"/>'
            f'<text x="{px + 10}" y="{py + 19}" class="mid">{esc(mid)}</text>'
            f'<text x="{px + 10}" y="{py + 35}" class="mname">{label}</text>'
            f'<text x="{px + 10}" y="{py + 66}" class="mtab">{esc(" · ".join(tables))}</text></g></a>'
        )
    out.append("</svg>")
    return "".join(out)


def t4_status():
    rows = [r for r in data.ROWS if r["table"] == "T4"]
    ready = [data.readiness(r) or {} for r in rows]
    return {
        "total": len(rows),
        "held": sum(1 for x in ready if x.get("calibration") == "Held"),
        "not_recorded": sum(1 for x in ready if x.get("calibration") == "Not recorded"),
        "approved": sum(
            1 for x in ready if x.get("calibration") not in ("Held", "Not recorded")
        ),
        "options": sum(1 for x in ready if x.get("options") not in ("0", "", None)),
        "selected": sum(1 for x in ready if x.get("selected") == "Yes"),
        "validated": sum(1 for x in ready if x.get("validated") == "Yes"),
        "roles": Counter(x.get("role", "Not recorded") for x in ready),
    }


def pilot_pin():
    try:
        raw = subprocess.check_output(
            ["git", "-C", str(RUNTIME), "show", "HEAD:src/nbs_runtime/recipe_pin.json"],
            stderr=subprocess.DEVNULL,
        )
        return json.loads(raw)
    except (subprocess.CalledProcessError, OSError, ValueError):
        return None


def chapter_pages(section, slugs, number):
    for i, slug_ in enumerate(slugs):
        html, toc = chapter_body(slug_)
        nav = []
        if i:
            nav.append(
                f'<a rel="prev" href="{chapter_file(slugs[i - 1])}">← {esc(TITLES.get(slugs[i - 1], ""))}</a>'
            )
        if i + 1 < len(slugs):
            nav.append(
                f'<a rel="next" href="{chapter_file(slugs[i + 1])}">{esc(TITLES.get(slugs[i + 1], ""))} →</a>'
            )
        html = f'<section class="chapter">{html}</section><nav class="prevnext" aria-label="Chapter">{"".join(nav)}</nav>'
        page(
            chapter_file(slug_),
            section,
            TITLES.get(slug_, words(slug_)),
            html,
            crumbs=[
                (section, "Method" if section == "method.html" else "Evidence methods"),
                ("", f"{number}.{i + 1}"),
            ],
            lead=esc(summary(slug_)),
            toc=toc,
        )


def chapter_index(slugs, number):
    rows = []
    for i, slug_ in enumerate(slugs, 1):
        rows.append(
            [
                f"{number}.{i}",
                link(chapter_file(slug_), esc(TITLES.get(slug_, slug_))),
                esc(summary(slug_)),
                f"{WORDS.get(slug_, 0):,}",
            ]
        )
    return table(
        ["", "Chapter", "After reading it you can", "Words"],
        rows,
        caption="Chapters in this part",
        numeric=(3,),
    )


# The method told as the questions a task team asks, in order. Each entry: question, plain answer,
# what the step produces, the chapters behind it, and the visual-methodology screen where one exists.
QUESTIONS = [
    (
        "Which landscape, and which practices?",
        (
            "A task team sets the area it is scoping and chooses the practices to compare. Each practice is "
            "split into families of sub-practices that are limited by the same thing, because a bench terrace "
            "and a rooftop tank are not sited by the same rules."
        ),
        "An area of interest and a list of practices and families.",
        ["m0-setup"],
        "01-setup.html",
    ),
    (
        "Where could each practice work?",
        (
            "For each family, published evidence says which site conditions matter: climate, terrain, soils and "
            "the farming already there. Places that meet them form the opportunity space. Legal exclusions such as "
            "protected areas are applied as masks supplied for each country."
        ),
        "An opportunity space for each family.",
        ["m1-suitability"],
        "03-opportunity.html",
    ),
    (
        "What could threaten the investment itself?",
        (
            "A separate screen asks whether climate hazards such as flood, drought or fire could damage the "
            "practice once it is in place, and whether access, tenure or conflict could block delivery. It works "
            "as a filter or a flag. It is never added into a score."
        ),
        "A project-risk filter on the opportunity space.",
        ["m2b-project-risk"],
        "04-risk.html",
    ),
    (
        "Who and what is at risk there?",
        (
            "Climate hazard is combined with the people and production exposed to it, giving risk to rural "
            "livelihoods. The opportunity space is also described by what a task team cares about: poverty, food "
            "insecurity, production gaps, biodiversity and equity."
        ),
        "Need layers that describe the opportunity space.",
        ["m2-climate-risk", "m3-characterisation"],
        None,
    ),
    (
        "Where do need and opportunity coincide?",
        (
            "The need layers are weighted and combined to show priority hotspots inside the opportunity space. "
            "Variables that say the same thing are grouped first, so nothing is counted twice, and the grouping "
            "and the weights are shown."
        ),
        "Priority hotspots.",
        ["m4-hotspots"],
        "05-hotspots.html",
    ),
    (
        "What is each practice likely to deliver, and how sure are we?",
        (
            "A scorecard rates each practice against each hazard and each priority. Every rating pools all the "
            "findings for that question and states a strength, a confidence level and where the evidence comes "
            "from. Indicative costs sit beside it."
        ),
        "A scorecard and an indicative cost profile per practice.",
        ["m5-scorecard"],
        "06-comparison.html",
    ),
    (
        "What happens next?",
        (
            "The scan flags where to look. It ends by listing what a feasibility study must settle locally: "
            "design, costs, national data and safeguards."
        ),
        "A hand-off to feasibility work.",
        ["m6-handoff"],
        "07-next.html",
    ),
]


def question_cards():
    """The method as seven questions, each with its plain answer and its technical chapter."""
    items = []
    for i, (question, answer, output, slugs, screen) in enumerate(QUESTIONS, 1):
        links = [link(chapter_file(s), esc(TITLES.get(s, s))) for s in slugs]
        if screen:
            links.append(link(VISUAL_URL + screen, "See the screen"))
        items.append(
            f'<li class="qcard"><span class="qn" aria-hidden="true">{i}</span><h3>{esc(question)}</h3>'
            f"<p>{esc(answer)}</p>"
            f'<p class="qout"><b>You get</b> {esc(output)}</p>'
            f'<p class="qlinks"><span>Technical detail:</span> {" · ".join(links)}</p></li>'
        )
    return f'<ol class="qgrid">{"".join(items)}</ol>'


def practice_facts():
    """Counts per practice, with the same definitions as the counts page."""
    kept = [u for u in data.EV if data.retained(u)]
    facts = []
    for p in PRACTICE_IDS:
        facts.append(
            {
                "practice": p,
                "families": len(
                    {f["suitability_family_id"] for f in data.FAM if f["nbs_id"] == p}
                ),
                "searches": sum(1 for x in data.SRCH if x.get("nbs_id") == p),
                "sources": sum(1 for x in data.SRC if p in practices_of(x)),
                "findings": sum(1 for u in kept if u.get("nbs_id") == p),
                "rows": {t: data.ROW_COUNTS[(p, t)] for t in ROW_TABLES},
            }
        )
    return facts


def practice_cards():
    """One card per practice: what it is, and how much evidence the edition holds for it."""
    facts = practice_facts()
    top = max(f["findings"] for f in facts)
    cards = []
    for f in facts:
        p = f["practice"]
        name = esc(practice_name(p))
        share = round(100 * f["findings"] / top)
        rows = "".join(
            f"<li>{badge(t)} {esc(TABLE_NAMES[t])} "
            + (f"<b>{n}</b>" if n else '<b class="none">none yet</b>')
            + "</li>"
            for t, n in f["rows"].items()
        )
        cards.append(
            f'<article class="pcard"><h3>{link(f"practice-{p}.html", name)}</h3>'
            f'<p class="pdesc">{esc(PRACTICE_TEXT[p][0])}</p>'
            f'<p class="pmain"><b>{f["findings"]:,}</b> findings from <b>{f["sources"]:,}</b> sources</p>'
            f'<div class="meter" role="img" aria-label="{f["findings"]:,} findings, {share} percent of the '
            f'largest practice" title="{f["findings"]:,} findings retained"><span style="width:{share}%"></span></div>'
            f'<p class="pmeta">{f["families"]} {"family" if f["families"] == 1 else "families"} · '
            f"{f['searches']} recorded searches · {sum(f['rows'].values())} compiled rows</p>"
            f'<ul class="prows">{rows}</ul></article>'
        )
    return f'<div class="pgrid">{"".join(cards)}</div>'


def evidence_chain(kept):
    """How a rating is backed, as five steps with the count each step holds."""
    dropped = len(data.EV) - len(kept)
    steps = [
        (
            f"{len(data.SRCH):,}",
            "searches recorded",
            "Every search is logged with its terms, limits and counts, so it can be repeated.",
            "ch-discovery.html",
        ),
        (
            f"{len(data.SRC):,}",
            "sources registered",
            "Each source that passes screening is registered with its citation, type and credibility tier.",
            "ch-acquisition.html",
        ),
        (
            f"{len(data.EV):,}",
            "findings extracted",
            "A finding is one claim from one source, stored with the exact quote and where it sits.",
            "ch-extraction.html",
        ),
        (
            f"{dropped:,}",
            "findings set aside",
            (
                "Automated checks and reviewers drop findings that are off scope or wrong. They are kept for "
                "audit and never deleted."
            ),
            "ch-review-and-quality.html",
        ),
        (
            f"{len(data.ROWS):,}",
            "rows compiled",
            "Findings on the same question are pooled by a fixed rule into one row with a stated confidence.",
            "ch-effect-synthesis.html",
        ),
    ]
    items = "".join(
        f'<li><a href="{h}"><b>{n}</b><span class="clabel">{esc(label)}</span></a><p>{esc(text_)}</p></li>'
        for n, label, text_, h in steps
    )
    return f'<ol class="chain">{items}</ol>'


def build():
    SIDE["method.html"] = [(chapter_file(s), TITLES.get(s, s)) for s in METHOD_CH]
    SIDE["evidence-methods.html"] = [
        (chapter_file(s), TITLES.get(s, s)) for s in EVIDENCE_CH
    ]
    SIDE["editions.html"] = [
        ("editions.html", "Editions"),
        ("status.html", "What is established"),
        ("reproduce.html", "Reproduce and check"),
        ("glossary.html", "Glossary"),
    ]
    chapter_pages("method.html", METHOD_CH, 2)
    chapter_pages("evidence-methods.html", EVIDENCE_CH, 3)

    s = t4_status()
    kept = [u for u in data.EV if data.retained(u)]
    fam_registered = sorted({f["suitability_family_id"] for f in data.FAM})
    effect_rows = [r for r in data.ROWS if r["table"] != "T4"]
    total_words = sum(WORDS.values())

    # ------------------------------------------------------------ method index
    body = (
        "<p>The scan answers a scoping question in a fixed order. It first asks where a practice could fit "
        "(suitability, giving an opportunity space), then what that space intersects (climate risk to "
        "livelihoods, people, production, equity), then where need and opportunity coincide (hotspots), and "
        "finally what each practice is likely to deliver (scorecard) and its indicative cost (economic profiles). "
        "A separate screen asks what could threaten the investment itself. Analytical rules are configured in "
        "tables and lookups so that each step can be inspected. Some synthesis constants remain in code and are "
        "stated in the chapters, and the runtime that reads the tables for a country application is maintained separately.</p>"
        f"<figure>{flow_figure()}<figcaption>Seven modules and one addendum. Each box lists the tables that configure it. "
        "Select a module to read its chapter.</figcaption></figure>"
        + stages_block()
        + chapter_index(METHOD_CH, 2)
        + "<p>Each module chapter follows the same order: the question it answers, inputs, method with formulas, "
        "outputs, assumptions and limits, and where its rules are configured. Each states what is specified, "
        "what is implemented, and what is left to a country application.</p>"
    )
    page(
        "method.html",
        "method.html",
        "Method",
        body,
        lead="The scan method, module by module: questions, inputs, formulas, outputs and limits.",
    )

    body = (
        "<p>No threshold, weight or effect in this method is taken from a document in one step. A source is "
        "found by a recorded search, acquired as a cached artefact, read into evidence units that each carry "
        "a verbatim quote and a locator, checked by deterministic gates, reviewed by a person, and only then "
        "pooled by a synthesis rule into a recipe row. Every row can be followed back along that chain.</p>"
        '<ol class="pipeline">'
        f"<li><strong>Discover</strong> {link('ch-discovery.html', 'recorded searches, screening and credibility')}</li>"
        f"<li><strong>Acquire</strong> {link('ch-acquisition.html', 'verified metadata, cached artefacts, locators')}</li>"
        f"<li><strong>Extract</strong> {link('ch-extraction.html', 'evidence units and deterministic checks')}</li>"
        f"<li><strong>Review</strong> {link('ch-review-and-quality.html', 'human decisions, soft-delete, plausibility')}</li>"
        f"<li><strong>Synthesise</strong> {link('ch-suitability-synthesis.html', 'site suitability')}, "
        f"{link('ch-effect-synthesis.html', 'hazard responses and scorecard effects')}, {link('ch-cost-profiles.html', 'indicative costs')}</li>"
        f"<li><strong>Version</strong> {link('ch-rulesets-and-learning.html', 'rulesets and the learning loop')}</li></ol>"
        + chapter_index(EVIDENCE_CH, 3)
        + f"<p>The result of applying these methods is counted in {link('evidence-base.html', 'the evidence base')} "
        f"and shown row by row under {link('practices.html', 'Practices')}.</p>"
    )
    page(
        "evidence-methods.html",
        "evidence-methods.html",
        "Evidence methods",
        body,
        lead="How literature, practitioner databases and tool code become traceable recipe rows.",
    )

    # ------------------------------------------------------------ overview
    terrace = next(r for r in data.ROWS if r["id"] == TERRACE)
    terrace_finding = terrace["raw"]["evidence_ids"][0]
    stats = [
        (
            f"{len(METHOD_CH) + len(EVIDENCE_CH) + len(PRACTICE_IDS)}",
            "method chapters",
            "method.html",
        ),
        (f"{total_words:,}", "words of method text", "method.html"),
        (f"{len(MODULES)}", "modules specified", "method.html"),
        ("20", "tables defined", "data-model.html"),
        (f"{len(data.VONT)}", "variables harmonised", "variables.html"),
        (f"{len(data.T1)}", "datasets registered", "datasets.html"),
        (f"{len(PRACTICE_IDS)}", "practices", "practices.html"),
        (f"{len(fam_registered)}", "suitability families", "practices.html"),
        (f"{len(data.SRCH)}", "recorded searches", "searches.html"),
        (f"{len(data.SRC)}", "sources registered", "sources.html"),
        (f"{len(kept):,}", "findings retained", "evidence-counts.html"),
        (f"{len(data.ROWS)}", "recipe rows", "practices.html"),
    ]
    overview_lead = (
        "The Rural NbS Scan is a method for scoping nature-based solutions in rural, "
        "agricultural and forestry landscapes. It shows where each practice could fit, what that area "
        "intersects, where need and opportunity coincide, and how strong the evidence is for what the "
        "practice delivers. It flags where to look. Local feasibility assessment validates."
    )
    headline = [
        (f"{len(PRACTICE_IDS)}", "practices covered", "#practices"),
        (f"{len(fam_registered)}", "families of sub-practices", "practices.html"),
        (f"{len(data.SRC):,}", "sources registered", "sources.html"),
        (f"{len(kept):,}", "findings retained", "evidence-counts.html"),
        (f"{len(data.ROWS)}", "rows compiled", "practices.html"),
    ]
    body = (
        '<div class="hero"><div class="stats big">'
        + "".join(
            f'<a href="{h}"><b>{n}</b><span>{esc(label)}</span></a>'
            for n, label, h in headline
        )
        + '</div><p class="routes"><a class="go" href="#story">Read the method as a story</a>'
        '<a href="#practices">See the practices and their evidence</a>'
        '<a href="method.html">Go to the technical specification</a></p>'
        "<p>This reference is written for two readers. The sections on this page tell the method in plain "
        "words. Behind every sentence sits the technical version: the modules and their formulas, the tables "
        "that hold every rule, the evidence methods, and every compiled row with the findings and sources "
        "behind it, in enough detail for an analyst to audit a result or re-implement a step.</p></div>"
        '<h2 id="practices">Practices covered, and how much evidence each has</h2>'
        f"<p>This draft edition holds evidence for {len(PRACTICE_IDS)} nature-based practices. For each one the "
        "team searched the literature and practitioner databases, read the sources, extracted findings with "
        "their quotes, and compiled them into rows: where the practice fits, how it responds to hazards, what "
        "it delivers, and what it costs.</p>"
        + practice_cards()
        + '<p class="basis">Bars compare findings retained across practices. Counts show coverage and effort, '
        "not strength of evidence: a row built on many findings can still carry low confidence, and each row "
        "states its own. A source that serves two practices is counted under both. "
        f"{link('evidence-counts.html#practice', 'The same counts as a table, with definitions')}.</p>"
        '<h2 id="story">The method in seven questions</h2>'
        "<p>The scan answers the questions a task team asks when deciding where a practice is worth a closer "
        "look. It works in a fixed order, and each step can be inspected.</p>"
        + question_cards()
        + '<p class="basis">The same seven steps are shown as screens in the '
        f"{link(VISUAL_URL + 'index.html', 'visual methodology')}, a mock-up of what a working tool could look "
        "like. Its numbers and maps are example data, not results.</p>"
        '<h2 id="chain">How every rating is backed</h2>'
        "<p>No threshold or rating is taken from a document in one step. Each one can be followed back from "
        "the compiled row, to the findings, to the quoted passage in the source.</p>"
        + evidence_chain(kept)
        + '<p class="basis">These are different units, not a funnel: one source yields many findings and feeds '
        f"several rows. {link('evidence-methods.html', 'Evidence methods in full')} · "
        f"{link('evidence-base.html', 'Download and query the data')}.</p>"
        + '<h2 id="status">What is established in this edition</h2>'
        + table(
            ["Component", "State in this edition"],
            [
                [
                    "Method specification",
                    f"Seven modules and the project-risk addendum are specified in {len(METHOD_CH)} chapters, with formulas and limits. Each chapter states what is implemented and what a country application must still supply.",
                ],
                [
                    "Evidence pipeline",
                    f"{len(data.SRCH)} recorded searches, {len(data.SRC)} registered sources, {len(data.EV):,} findings of which {len(kept):,} are retained and {len(data.EV) - len(kept):,} were dropped (by a reviewer or by the automated off-scope quarantine) and kept for audit.",
                ],
                [
                    f"{TABLE_NAMES['T4']}",
                    f"{s['total']} mappings: {s['held']} with calibration held, {s['not_recorded']} with no calibration recorded, {s['approved']} approved. "
                    f"{s['selected']} have a function selected for a named target or default design. {s['validated']} are execution-ready (published as “spatially validated”). These categories overlap. "
                    f"By role: {', '.join(f'{v} {k.lower()}' for k, v in s['roles'].most_common())}. "
                    + ", ".join(
                        practice_name(p)
                        for p in PRACTICE_IDS
                        if data.ROW_COUNTS[(p, "T4")] == 0
                    )
                    + " have none compiled.",
                ],
                [
                    "Effect rows",
                    f"{data.TABLE_TOTALS['T3']} hazard responses, {data.TABLE_TOTALS['T6']} scorecard effects and {data.TABLE_TOTALS['T6E']} indicative economic profiles, generated by synthesis, each with two-axis confidence and a transfer class.",
                ],
                [
                    "Country application",
                    "Maintained separately as a pilot with its own pinned release. Maps and country results are not part of this reference.",
                ],
            ],
            caption="State by component. Draft edition, candidate and not released.",
        )
        + f"<p>{link('status.html', 'Full status tables')} · {link('editions.html', 'Edition identifiers')}</p>"
        '<h2 id="walkthrough">Try it: one finding, end to end</h2>'
        "<p><strong>Can annual rainfall alone set a bench-terrace suitability score?</strong> One source documents a use range "
        "for forward-sloping benches. The finding is retained as extracted; its review is not yet recorded in the finding review log. No response curve is supported, so the numerical "
        "calibration is held and no score is assigned. Approving a finding confirms the extraction; it does not approve a score.</p><ol>"
        f"<li>{link(live('review-evidence=' + terrace_finding), 'The rainfall finding as reviewers see it')}, in the live dashboard: "
        "the extracted values, the quoted passage and page, and its review status.</li>"
        f"<li>{link(source_file(data.EV_BY_ID[terrace_finding]['source_id']), 'The source')} and where in it the finding sits.</li>"
        f"<li>{link('practice-water_harvesting_conservation.html#fam-water_harvesting__terracing', 'The terracing family')} and its mappings.</li>"
        f"<li>{link(terrace['file'], 'The annual precipitation row')}: role, status, why the calibration is held.</li>"
        f"<li>{link('ch-suitability-synthesis.html', 'Suitability synthesis')}: the rule that keeps a held calibration from becoming a score.</li></ol>"
        '<p class="basis">Step 1 opens the live dashboard. Its review queue reads the current records of the evidence repository '
        "each time the page loads, so it can show a later state than this reference. "
        f"{link('review.html#pins', 'Which revision is which')}.</p>"
        '<h2 id="review">Review queues</h2>'
        "<p>At this site revision, finding reviews are submitted from the live dashboard as public issues in the evidence "
        "repository and are recorded there once applied. The producer repository keeps the earlier records. Choose a reviewer "
        "in the live dashboard to filter that reviewer’s history under “My reviewed”; a submission is credited to the GitHub "
        "account that creates it.</p>"
        + review_queues()
        + f"<p>{link('review.html', 'How finding reviews, archived finding reviews and rating decisions are kept apart')}.</p>"
        '<h2 id="contents">What this reference contains</h2><div class="stats">'
        + "".join(
            f'<a href="{h}"><b>{n}</b><span>{esc(label)}</span></a>'
            for n, label, h in stats
        )
        + '</div><p class="basis">Counts are taken from the registers and recipe tables at one pinned revision '
        f"({code(PRODUCER[:8])}). They describe coverage and effort, not evidence strength. "
        f"{link('evidence-counts.html', 'Definitions of each count')}. "
        f"{link('evidence-base.html', 'Download and query the tables')}.</p>"
        '<h2 id="method">The method in one figure</h2>'
        f"<figure>{flow_figure()}<figcaption>Modules M0 to M6 and the M2b addendum. Risk to livelihoods (M2) is a need layer. "
        "Risk to the investment (M2b) is a filter. The two are never summed.</figcaption></figure>"
        '<h2 id="stages">The method as seven stages</h2>'
        + stages_block()
        + '<h2 id="parts">Parts of the reference</h2>'
        + table(
            ["Part", "What it holds", "Start here if you want to"],
            [
                [
                    link("method.html", "2 Method"),
                    f"{len(METHOD_CH)} chapters: scope, a stage-by-stage walkthrough, the seven modules and the project-risk addendum, farming systems and data, implementation requirements.",
                    "understand or re-implement the analysis",
                ],
                [
                    link("evidence-methods.html", "3 Evidence methods"),
                    f"{len(EVIDENCE_CH)} chapters: discovery, acquisition, extraction, review, three synthesis methods, versioning, and how to continue the work with an AI system and human approval.",
                    "judge whether a rule is defensible",
                ],
                [
                    link("data-model.html", "4 Data model"),
                    f"20 tables with every field, {len(data.VONT)} variables, {len(data.T1)} datasets, all rule tables in full.",
                    "read or write the tables",
                ],
                [
                    link("practices.html", "5 Practices"),
                    f"{len(PRACTICE_IDS)} practices, {len(fam_registered)} suitability families, {len(data.ROWS)} rows each with a detail page.",
                    "see what the method says about a practice",
                ],
                [
                    link("evidence-base.html", "6 Evidence base"),
                    f"Downloads of every evidence table with a field guide and tested queries. {len(data.SRC)} sources, {len(kept):,} retained findings, {len(data.SRCH)} search records, with definitions.",
                    "download or query the data, or follow a row to its source",
                ],
                [
                    link("editions.html", "7 Editions and checks"),
                    "Edition identifiers, what is established and what is not, how to reproduce, glossary.",
                    "cite or rebuild this edition",
                ],
            ],
            caption="Six parts after this overview",
        )
        + '<h2 id="routes">Follow the method</h2>'
        "<ol>"
        f"<li>{link('ch-scope-and-framework.html', 'Scope and framework')}: what the scan decides and what it leaves to feasibility.</li>"
        f"<li>{link('ch-m1-suitability.html', 'Suitability')}: families, membership functions, gates and masks.</li>"
        f"<li>{link('ch-effect-synthesis.html', 'Effect synthesis')}: how pooled findings become a class with a confidence.</li>"
        f"<li>{link('table-T4.html', 'A table definition')}: the fields a pipeline reads.</li></ol>"
    )
    page(
        "index.html",
        "index.html",
        "Rural NbS Scan methodology reference",
        body,
        lead=overview_lead,
    )

    # ------------------------------------------------------------ help and change history
    issues = "https://github.com/RuralScan/method/issues"
    body = (
        "<p>This reference documents the Rural NbS Scan method in full. It is a scoping reference: it shows "
        "where to look and how strong the evidence is. It holds no maps and no country results, and local "
        "feasibility work is still needed before any investment decision.</p>"
        '<h2 id="start">Finding your way</h2><dl class="glossary">'
        "<div><dt>Where should I start?</dt><dd>On the "
        f"{link('index.html', 'overview')}. It lists the practices covered and how much evidence each has, then "
        f"tells the method as {link('index.html#story', 'seven questions')}. Each question links to its technical chapter.</dd></div>"
        "<div><dt>How do I see the evidence for one practice?</dt><dd>Open "
        f"{link('practices.html', 'Practices')} and choose one. Every compiled row has its own page listing the "
        "findings behind it, each with its source and the place in the source it was taken from.</dd></div>"
        "<div><dt>Are the numbers results?</dt><dd>No. Counts of searches, sources, findings and rows describe "
        "coverage and effort. Ratings are the method’s reading of published evidence, each with a stated "
        f"confidence. {link('index.html#status', 'What is established in this edition')}.</dd></div>"
        "<div><dt>How does this relate to the visual methodology?</dt><dd>The "
        f"{link(VISUAL_URL + 'index.html', 'visual methodology')} shows what a working tool could look like, "
        "using example data. This reference is the written method and the evidence behind it. "
        f"{link(chapter_file('scoping-walkthrough'), 'The scoping walkthrough')} connects the two, screen by screen.</dd></div>"
        "<div><dt>Which version am I looking at?</dt><dd>The bar at the top of every page names it. The version "
        "menu lists the live evidence dashboard first, then this reference, then earlier drafts.</dd></div>"
        "<div><dt>Can I download the data?</dt><dd>Yes. "
        f"{link('evidence-base.html', 'Get and use the data')} lists every table with its address and checksum, a "
        "field guide and tested queries.</dd></div></dl>"
        '<h2 id="feedback">Giving feedback</h2>'
        "<p>Choose <strong>Review</strong> in the bar at the top of any page. You can pin a comment to a table, "
        "figure or paragraph, highlight text, or capture part of the screen, and give each note a type and a "
        "severity. The same review tool is used on the visual methodology and on the live evidence dashboard.</p><ul>"
        "<li>Notes stay in your browser. Nothing is sent until you choose to share.</li>"
        "<li>Use Export to save your notes as a file or a readable report, or to open them as a public issue.</li>"
        "<li>Say what you expected and what needs to change. The page and the item are recorded for you.</li></ul>"
        "<p>Reviewing an extracted finding or a compiled rating is a different task, done in the "
        f"{link(live('review-queue'), 'review queue')} of the live dashboard. "
        f"{link('review.html', 'How review records are kept')}.</p>"
        f"<p>You can also {link(issues, 'raise a question or a correction as an issue')} in the method repository.</p>"
        + CONTACTS
    )
    page(
        "help.html",
        "index.html",
        "Help, contact and team",
        body,
        lead="How to find your way around this reference, how to give feedback, and who to contact.",
    )

    changes = [
        (
            "17 November 2026",
            [
                (
                    "Listed in the site’s version menu under “Under review”. The menu on these pages now has the same "
                    "three groups as the live dashboard: Live, Under review and Earlier drafts."
                ),
                "The help page names the project contacts and team.",
            ],
        ),
        (
            "16 November 2026",
            [
                "Front page rebuilt: the practices covered, how much evidence each has, and the method told as seven questions.",
                "The reference takes the live evidence dashboard’s look, and that house style is recorded and checked by the build.",
                (
                    "One top bar shared with the visual methodology: version menu, theme switch, review tool and change history. "
                    "Programme logo and a help page added."
                ),
                (
                    "The chapter on continuing the evidence base with an AI system now describes the routes for recording work "
                    "in the evidence and method repositories."
                ),
                "Published at an address that is not yet listed, with a request to search engines not to index it.",
            ],
        ),
        (
            "14 November 2026",
            [
                "Evidence base rebuilt for use: downloads of every table, a field guide, and queries that the build runs.",
                "New chapter: continue the evidence base with an AI system.",
                "Review page updated: finding reviews are submitted from the live dashboard and recorded in the evidence repository.",
            ],
        ),
        (
            "12 November 2026",
            [
                (
                    "Added the scoping walkthrough, which follows the visual methodology stage by stage, and the chapter on "
                    "implementing the method."
                ),
            ],
        ),
        (
            "11 November 2026",
            [
                "First build: the method by module, the evidence methods, the data model, every practice and every compiled row.",
            ],
        ),
    ]
    body = (
        "<p>What changed in this reference, newest first. The evidence and the ratings it reports are those of "
        f"one pinned edition, described under {link('editions.html', 'Editions and checks')}; they do not change "
        "between these entries unless an entry says so.</p>"
        + "".join(
            f"<h2>{esc(day)}</h2><ul>{''.join(f'<li>{esc(x)}</li>' for x in items)}</ul>"
            for day, items in changes
        )
        + '<h2 id="feedback">Feedback</h2>'
        "<p>Choose <strong>Review</strong> in the bar at the top of any page to leave notes on what you see. "
        f"{link('help.html#feedback', 'How the review tool works')}. Feedback that has been acted on appears "
        "in the entries above.</p>"
    )
    page(
        "changes.html",
        "index.html",
        "What changed",
        body,
        lead="History of this reference and how to give feedback on it.",
    )

    # ------------------------------------------------------------ status
    by_practice = []
    for p in PRACTICE_IDS:
        rows = [r for r in data.ROWS if r["practice"] == p and r["table"] == "T4"]
        ready = [data.readiness(r) or {} for r in rows]
        by_practice.append(
            [
                link(f"practice-{p}.html#T4", esc(practice_name(p))),
                str(len(rows)),
                str(sum(1 for x in ready if x.get("calibration") == "Held")),
                str(sum(1 for x in ready if x.get("calibration") == "Not recorded")),
                str(
                    sum(
                        1
                        for x in ready
                        if x.get("calibration") not in ("Held", "Not recorded")
                    )
                ),
                str(sum(1 for x in ready if x.get("options") not in ("0", "", None))),
                str(sum(1 for x in ready if x.get("selected") == "Yes")),
                str(sum(1 for x in ready if x.get("validated") == "Yes")),
            ]
        )
    by_practice.append(
        ["<strong>All practices</strong>"]
        + [
            f"<strong>{v}</strong>"
            for v in (
                s["total"],
                s["held"],
                s["not_recorded"],
                s["approved"],
                s["options"],
                s["selected"],
                s["validated"],
            )
        ]
    )

    def conf(r):
        return (
            r["raw"].get("confidence")
            or r["raw"].get("effect_confidence")
            or "not recorded"
        )

    order = [
        "very_high",
        "high",
        "medium",
        "moderate",
        "low",
        "very_low",
        "not recorded",
    ]
    conf_counts = {
        t: Counter(conf(r) for r in effect_rows if r["table"] == t)
        for t in ("T3", "T6", "T6E")
    }
    levels = [
        c for c in order if any(conf_counts[t].get(c) for t in conf_counts)
    ] + sorted({c for t in conf_counts for c in conf_counts[t]} - set(order))
    conf_rows = [
        [esc(words(c))] + [str(conf_counts[t].get(c, 0)) for t in ("T3", "T6", "T6E")]
        for c in levels
    ]
    transfer = Counter(
        (r["raw"].get("applicability") or {}).get("transfer_class") or "not recorded"
        for r in effect_rows
    )

    def just(r):
        j = r["raw"].get("justification")
        return j if isinstance(j, dict) else {}

    signals = [
        [
            "Rows with measured harm recorded",
            sum(
                1
                for r in effect_rows
                if (just(r).get("maladaptation") or {}).get("n_units")
            ),
        ],
        [
            f"Rows flagged for the hazard-intensity discount (class lowered in {sum(1 for r in effect_rows if just(r).get('intensity_discounted_from'))})",
            sum(1 for r in effect_rows if just(r).get("intensity_limited")),
        ],
        [
            "Rows flagged with an off-site effect locus",
            sum(1 for r in effect_rows if r["raw"].get("landscape_scale_only")),
        ],
        [
            "Rows with the size-sparse cap applied",
            sum(1 for r in effect_rows if just(r).get("size_sparse")),
        ],
        [
            "Rows with the modelled-only cap applied",
            sum(1 for r in effect_rows if just(r).get("modelled_capped")),
        ],
        [
            "Rows whose direction or potential is “conflicting evidence”",
            sum(
                1
                for r in effect_rows
                if "conflicting_evidence"
                in (
                    r["raw"].get("mitigation_potential"),
                    r["raw"].get("effect_direction"),
                )
            ),
        ],
    ]
    products = Counter()
    parked = []
    for f in fam_registered:
        if f.endswith("__cross_family"):
            products["cross_family"] += 1
            continue
        for k in data.family_product(f):
            products[k] += 1
            if k == "qualitative_only":
                parked.append(core_family_name(f))
    fam_rows = [
        [esc(PRODUCTS[k][0]), str(v), esc(PRODUCTS[k][1])]
        if k in PRODUCTS
        else [
            "Cross-family context",
            str(v),
            "Not a spatial product. A tag for evidence pooled across a practice's families.",
        ]
        for k, v in products.most_common()
    ]
    body = (
        "<p>A scoping method is only useful if its reader knows which parts are settled. This page states, "
        "from the data of this edition, what has been compiled, what has been reviewed, and what has not. "
        "Nothing here is a judgement added by the page: each figure is a count of a recorded field.</p>"
        '<h2 id="suitability">Suitability mappings</h2>'
        "<p>A mapping passes through separate states. Sources are cited. Function options may be compiled from "
        "them. A function may be selected. Its numerical calibration may be reviewed. It may be validated "
        "spatially. “Held” records that a calibration was reviewed and no score is assigned: no supported breakpoints "
        "were approved, or the row is kept only as a design reference, or it awaits an input layer that matches the "
        "quantity the source reports. “Not recorded” means no calibration status is on the row. It is not an approval "
        "and does not show whether a review took place. “Function selected” records a choice for a named target or a "
        "gate's default design, not a global approval. “Execution-ready” is the producer's flag, published as “spatially validated”.</p>"
        + table(
            [
                "Practice",
                "Mappings",
                "Calibration held",
                "Calibration not recorded",
                "Calibration approved",
                "With function options",
                "Function selected",
                "Execution-ready",
            ],
            by_practice,
            caption="Readiness of suitability mappings, by practice. Columns describe the same rows and overlap.",
            numeric=(1, 2, 3, 4, 5, 6, 7),
        )
        + table(
            ["Function role", "Mappings", "Meaning"],
            [
                [
                    esc(k),
                    str(v),
                    esc(
                        {
                            "Suitability score": "Intended to contribute a membership value once a function is selected and calibrated. None is execution-ready in this edition.",
                            "Eligibility gate": "Admits or removes a location before scoring.",
                            "Hard exclusion": "Defines a mask interface. No mask is applied until an assessed mask for the jurisdiction is supplied.",
                            "Operational scenario": "An implementation factor that investment can change; screened through project risk, not suitability.",
                        }.get(k, "")
                    ),
                ]
                for k, v in s["roles"].most_common()
            ],
            caption="Suitability mappings by function role",
            numeric=(1,),
        )
        + '<h2 id="effects">Effect rows</h2>'
        "<p>Hazard responses, scorecard effects and indicative economic profiles are generated by synthesis over pooled "
        'findings. Confidence is derived from evidence level and agreement level, never authored.</p><div class="grid2">'
        + table(
            ["Confidence", TABLE_NAMES["T3"], TABLE_NAMES["T6"], TABLE_NAMES["T6E"]],
            conf_rows,
            caption="Effect rows by derived confidence",
            numeric=(1, 2, 3),
            cls="narrow",
        )
        + table(
            ["Transfer class", "Rows"],
            [[esc(words(k)), str(v)] for k, v in transfer.most_common()],
            caption="Effect rows by transfer class (distance of the evidence from the target context)",
            numeric=(1,),
            cls="narrow",
        )
        + "</div>"
        + table(
            ["Signal", "Rows"],
            [[esc(a), str(b)] for a, b in signals],
            caption=f"Synthesis signals across the {len(effect_rows)} effect rows. A row can carry several.",
            numeric=(1,),
            cls="narrow",
        )
        + '<h2 id="families">Families and spatial products</h2>'
        + table(
            ["Spatial product", "Registered families", "What may be reported"],
            fam_rows,
            caption=f"{len(fam_registered)} registered family identifiers by spatial product",
            numeric=(1,),
        )
        + "<p>Linear and zonal products are reported as length or zone, never as pixel area. Qualitative sub-practice families ("
        + esc(", ".join(parked))
        + ") are parked out of the generated effect tables; their evidence remains in the register for "
        "hand-off guidance. Cross-family tags hold evidence pooled across a practice's families and are not parked.</p>"
        '<h2 id="review">Human review of findings</h2>'
        f"<p>{sum(1 for u in kept if u.get('reviewer_ok') is True):,} of {len(kept):,} retained findings were kept or reclassified by a reviewer after being flagged. "
        "That decision confirms the finding against its quote; it is not a review of its numbers or of any calibration. "
        "Findings that were never flagged may not have been seen by a reviewer. "
        f"{len(data.EV) - len(kept):,} findings were dropped, by a reviewer or by the automated off-scope quarantine, and are kept for audit. The automated provenance gates and the "
        f"review process are described in {link('ch-review-and-quality.html', 'review and quality')}.</p>"
        '<h2 id="not">What this edition does not establish</h2><ul>'
        "<li>No suitability mapping has an approved numerical calibration, and none is execution-ready.</li>"
        "<li>Country results, maps and pilot outputs are outside this reference.</li>"
        "<li>Economic profiles are indicative and ordinal. No cost-benefit analysis is made.</li>"
        "<li>Practices outside the six listed are not covered by this edition.</li></ul>"
    )
    page(
        "status.html",
        "editions.html",
        "What is established",
        body,
        crumbs=[("editions.html", "Editions and checks"), ("", "What is established")],
        lead="What has been compiled, what has been reviewed and what has not, from the data of this edition.",
        toc=[
            ("suitability", "Suitability mappings"),
            ("effects", "Effect rows"),
            ("families", "Families and spatial products"),
            ("review", "Human review of findings"),
            ("not", "What this edition does not establish"),
        ],
    )

    # ------------------------------------------------------------ review records
    archive = "https://github.com/CIAT/nbs_ruralscan/blob/" + LIVE_REVIEWS + "/"
    log = EVIDENCE_LIVE + "registers/"
    body = (
        "<p>Reviewers check each extracted finding against its source, and check each compiled rating. "
        "Finding decisions are recorded in the evidence repository. The live dashboard shows the queues and reviewers’ "
        "histories from that repository and lets a signed-in reviewer submit a finding review. This reference shows the "
        "result at its own revision and links to the queues.</p>"
        + review_queues()
        + "<p>In the live dashboard, choose a reviewer to see that reviewer’s history under “My reviewed”. "
        "This choice only filters the history; a submission is credited to the GitHub account that creates it. "
        "The history lists three kinds of record separately.</p>"
        '<h2 id="kinds">Three kinds of review record</h2>'
        + table(
            [
                "Record",
                "What was reviewed",
                "What the decision changes",
                "Where it is logged",
            ],
            [
                [
                    "<strong>Finding review</strong>",
                    (
                        "One extracted finding: its values, quote, page and scope, checked against the source. "
                        "Includes findings that an earlier version of a hazard or scorecard table cited; those are marked as previously cited."
                    ),
                    (
                        "Whether the finding stays in the evidence that synthesis reads: Drop removes it from synthesis and keeps it as a record; Keep and Hold leave it in. In earlier records, Query is the same as Hold, and Reclassify changed the finding’s scope. Keeping a finding confirms the extraction. "
                        "It does not approve a score or a rating."
                    ),
                    link(log + "pipeline/metrics/review_log.csv", "Finding review log"),
                ],
                [
                    "<strong>Archived finding review</strong>",
                    (
                        "A finding reviewed before effect ratings were generated by synthesis, from the evidence archived when hazard and scorecard extraction was paused. "
                        "No version of the hazard or scorecard table has cited it."
                    ),
                    (
                        "No current rating. Where the finding was later restored to the live evidence register, the earlier decision "
                        "still applies to it there. It is listed so that a reviewer’s earlier work stays visible."
                    ),
                    link(
                        archive
                        + "schema/registers/_deferred/EV_T3_T6_deferred_2026-09.csv",
                        "Archive register",
                    )
                    + " in the producer repository, with decisions in "
                    + link(
                        archive + "pipeline/metrics/review_log.csv",
                        "its finding review log",
                    )
                    + " at the same revision",
                ],
                [
                    "<strong>Rating decision</strong>",
                    "One compiled rating: a hazard response or scorecard row, not a single finding.",
                    (
                        "Nothing in the tables or registers. The decision is logged against the rating. A hold or reject is followed up "
                        "by correcting the evidence, routing or wording and regenerating the rating."
                    ),
                    link(
                        log + "pipeline/metrics/row_review_log.csv", "Rating review log"
                    ),
                ],
            ],
            caption="The three kinds are counted and listed separately. They are never added together.",
        )
        + '<h2 id="writer">Where decisions are written</h2>'
        "<p>At this site revision, finding decisions are written in the evidence repository. The producer repository has "
        "stopped writing evidence and review records for the hazard, suitability and scorecard tables and keeps its earlier "
        "records unchanged.</p><ol>"
        "<li><strong>Submit.</strong> In the live dashboard, Submit review on a finding opens a public issue in the evidence "
        "repository under the reviewer’s GitHub account. The vote, the note and the account name are public. A file of votes "
        "or an extraction proposal is submitted the same way through the evidence repository’s submission desk.</li>"
        "<li><strong>A submission is a receipt.</strong> It is not yet a recorded decision.</li>"
        "<li><strong>Apply.</strong> A maintainer applies submissions through a protected pull request. The tool checks that "
        "the reviewer is eligible, that the submission was not edited, that the finding and its source are unchanged, that "
        "eligible reviewers agree, and that the receipt has not been applied before. Opposing votes stay pending. "
        "The pull request needs approval and passing checks.</li>"
        "<li><strong>Recorded.</strong> Once merged, the decision is in the evidence repository’s finding review log, "
        "and the live queue shows it the next time the page loads.</li></ol>"
        "<p><strong>Rating decisions</strong> have a route too, but not yet from the live dashboard. A reviewer starts the "
        "evidence repository’s local desk on their own computer, opens the row, and chooses Review this rating (approve, "
        "hold or reject) or Suggest clearer wording. Each creates a public issue under the reviewer’s account, and a "
        "protected pull request applies it: a rating is appended to the rating review log, and wording is recorded as an "
        "authored input beside the compiled row. A rating review approves no finding and changes no threshold. The live "
        "dashboard’s row cards do not yet link to the desk; its My reviewed list already reads applied rating history for "
        "the hazard, suitability and scorecard tables. At the evidence revision this reference was built against, the "
        "rating log held only the events copied from the producer repository. This reference does not write decisions.</p>"
        f"<p>{link(EVIDENCE_LIVE + 'workflows/submissions/README.md', 'How to submit a finding vote or an extraction proposal')} · "
        f"{link(EVIDENCE_LIVE + 'workflows/submissions/recipe-rows.md', 'How to review a rating or suggest row wording')} · "
        f"{link('ch-continue-with-ai.html', 'Continue the evidence base with an AI system')}.</p>"
        '<h2 id="pins">Which revision is which</h2>'
        "<p>The live dashboard pins its analytical snapshot to a producer revision later than this reference’s. Its review "
        "history is not pinned: it is read from the evidence repository’s current main branch when the page loads. Only the "
        "provisional status of hazard ratings is taken from the same revision as this reference. "
        "A review state shown on a row or finding page here is the state at this reference’s revision and can be older "
        "than the live queues, which change whenever a decision is applied.</p>"
        + live_pins()
        + f"<p>The country pilot is separate again and pins its own release. {link('editions.html#pilot', 'Editions')}.</p>"
    )
    page(
        "review.html",
        "evidence-base.html",
        "Review queues and review records",
        body,
        crumbs=[("evidence-base.html", "Evidence base"), ("", "Review")],
        lead="Where human review happens, how a decision becomes a record, and how three kinds of review record are kept apart.",
        toc=[
            ("kinds", "Three kinds of review record"),
            ("writer", "Where decisions are written"),
            ("pins", "Which revision is which"),
        ],
    )

    # ------------------------------------------------------------ editions
    pilot = pilot_pin()
    rows = [
        [
            "Recipe edition",
            "Draft: candidate, not released",
            code(RELEASE),
            f"{len(data.ROWS)} rows: "
            + ", ".join(f"{data.TABLE_TOTALS[t]} {t}" for t in ROW_TABLES),
        ],
        [
            "Producer revision",
            "Recipe tables and evidence registers are read from this one revision",
            link(CIAT_URL, code(PRODUCER)),
            "All counts in this reference",
        ],
        [
            "Method definitions pinned by the release",
            "Definition snapshot named in the release pin",
            code(PIN["method"]["revision"]),
            f"sha256 {code(PIN['method']['sha256'][:16])}…",
        ],
        [
            "Method repository",
            "Cookbook names, data-model specification",
            code(METHOD_REV),
            "Display names, specification text",
        ],
        [
            "Evidence workflows repository",
            "Release pin, published recipe tables (function role, readiness)",
            link(
                EVIDENCE_URL + "workflows/recipe_release/pin.json", code(EVIDENCE_REV)
            ),
            "Function role and readiness columns",
        ],
    ]
    body = (
        "<p>An edition is one fixed set of inputs. Everything in this reference is read from the identifiers "
        "below, so a number here can be reproduced exactly. Counts from different editions are never added, "
        "subtracted or turned into a rate.</p>"
        + table(
            ["Input", "Role", "Identifier", "Used for"],
            rows,
            caption="Inputs to this reference",
        )
    )
    body += (
        '<h2 id="live">The live dashboard pins its analytical revisions and reads current review records</h2>'
        "<p>The live evidence dashboard is a separate product from this reference. It pins the revision of its analytical "
        "snapshot, which is later than the revision this reference is built on. Its review history is read from the evidence "
        "repository’s current records when the page loads. "
        "Its hazard-rating review status is taken from an assessment made at this reference’s revision, after checking that "
        "the effect evidence is unchanged at the analytical snapshot.</p>"
        + live_pins()
        + f"<p>{link('review.html', 'Review queues and review records')}.</p>"
    )
    if pilot:
        body += (
            '<h2 id="pilot">The country pilot uses its own release</h2>'
            f"<p>The country pilot is maintained separately and pins a release of its own: {code(pilot['release_id'])}, "
            f"built from revision {code(pilot['source_revision'][:8])}. That is a different edition from the recipe edition shown here. "
            "The two are listed side by side so that a reader comparing them knows they differ; no arithmetic is made between them. "
            "In either release, a mapping whose calibration is held has no approved breakpoints.</p>"
        )
    body += (
        '<h2 id="words">Terms</h2>'
        "<p><strong>Edition</strong> is used for a fixed set of inputs. <strong>Release</strong> is the content-addressed build of the "
        "recipe tables. <strong>Candidate</strong> means built and checked but not yet released. <strong>Draft</strong> is the plain word "
        "used on the first screen for the same state. Schema and ruleset versions are separate and are named as versions. "
        f"See the {link('glossary.html', 'glossary')}.</p>"
    )
    page(
        "editions.html",
        "editions.html",
        "Editions",
        body,
        lead="Which inputs this reference was built from, and how they differ from the country pilot's.",
    )

    # ------------------------------------------------------------ glossary
    terms = [
        (
            "Agreement level",
            "How far independent findings in a cell point the same way. One of the two axes of confidence.",
        ),
        (
            "Applicability envelope",
            "The income groups, zones, farming systems and countries of the evidence behind a row, recorded on the row.",
        ),
        (
            "Asset threat",
            "A hazard-response row describing how a hazard threatens the investment itself. Read by the project disaster risk screen.",
        ),
        (
            "Calibration held",
            "A numerical calibration was reviewed and no score is assigned. Either no supported breakpoints were approved, or the row is kept only as a design or planning reference, or it awaits an input layer that matches the quantity the source reports. Source values are kept.",
        ),
        (
            "Calibration not recorded",
            "No calibration status is recorded on the row. It is not an approval and does not show whether any review occurred.",
        ),
        (
            "Candidate",
            "A release that has been built and checked but not released. Shown as “draft” on first screens.",
        ),
        (
            "Cell",
            "The unit of effect synthesis. Hazard responses for livelihoods: practice, hazard and farming system. Threats to the investment: practice and hazard. Scorecard effects: practice and priority. Indicative economic profiles: practice and economic indicator. Each is also synthesised per family.",
        ),
        (
            "Claim scope",
            "Whether a finding is about the practice, a species or a crop. Species and crop findings are kept but routed away from practice rows.",
        ),
        (
            "Confidence",
            "Derived from evidence level and agreement level using a pinned matrix. Never authored.",
        ),
        (
            "Edition",
            "One fixed set of inputs from which numbers are computed. Counts from different editions are never combined.",
        ),
        (
            "Effect locus",
            "Where an effect is felt: on the treated land, mixed, or off-site.",
        ),
        (
            "Eligibility gate",
            "A suitability mapping that admits or removes a location before scoring.",
        ),
        (
            "Evidence level",
            "The amount and quality of evidence in a cell. One of the two axes of confidence.",
        ),
        (
            "Finding (evidence unit)",
            "One variable and relationship at one locator in one source, with a verbatim quote.",
        ),
        (
            "Function role",
            "What a suitability mapping does: suitability score, eligibility gate, hard exclusion or operational scenario.",
        ),
        (
            "Hard exclusion",
            "A legal or physical exclusion on the opportunity space, such as protected areas, water bodies and urban footprints. The mapping defines the mask interface; an assessed mask must be supplied.",
        ),
        (
            "Locator",
            "Where in a source a finding sits: a page, a section, or a file and line at a pinned commit.",
        ),
        (
            "Maladaptation signal",
            "Findings that measured harm, listed on a row even when they are a minority.",
        ),
        (
            "Operational scenario",
            "An implementation factor that investment can change, such as access or tenure. Screened through project risk, not suitability.",
        ),
        (
            "Opportunity space",
            "The area where a suitability family could be applied, after gates and exclusions.",
        ),
        (
            "Practice",
            "A nature-based solution treated by the method, such as agroforestry.",
        ),
        (
            "Practice-level roll-up",
            "An effect row for the practice as a whole, pooled over all the practice's findings rather than averaged from family rows. Always emitted, shown once, and may have scope rows.",
        ),
        (
            "Recipe",
            "The per-practice configuration: its registry record, families, mappings, hazard responses, scorecard effects and costs.",
        ),
        (
            "Ruleset",
            "The versioned instructions for search and extraction. Each search record and finding names the version in force.",
        ),
        (
            "Scope row",
            "An additional row for one context. Emitted when at least two independent sources sit in that context and its class differs from the global row, or the global row is out of context there, or global agreement is low.",
        ),
        (
            "Spatial product type",
            "What a family may be reported as: area suitability, applicability zone, linear corridor or qualitative guidance.",
        ),
        ("Sub-practice", "A registered variant of a practice, such as bench terraces."),
        (
            "Suitability family",
            "A group of sub-practices that share a dominant limiting factor and therefore one suitability logic and one spatial product.",
        ),
        (
            "Transfer class",
            "How the evidence behind a row compares with that row's target, by share of evidence weight: in context, adjacent, mixed or out of context. Global rows target low and lower-middle income settings; a scope row targets its own scope. Always shown.",
        ),
    ]
    body = (
        '<dl class="glossary">'
        + "".join(
            f'<div><dt id="{esc(t.lower().replace(" ", "-").replace("(", "").replace(")", ""))}">{esc(t)}</dt><dd>{esc(d)}</dd></div>'
            for t, d in terms
        )
        + "</dl>"
    )
    page(
        "glossary.html",
        "editions.html",
        "Glossary",
        body,
        crumbs=[("editions.html", "Editions and checks"), ("", "Glossary")],
        lead="Terms as this reference uses them.",
    )
