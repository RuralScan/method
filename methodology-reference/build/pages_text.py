"""Overview, section indexes, authored chapters, editions, status and glossary."""

import json
import subprocess
from collections import Counter
from itertools import pairwise

import data
import versioning
from chapters import (
    EVIDENCE_CH,
    METHOD_CH,
    TITLES,
    chapter_body,
    chapter_file,
    summary,
)
from core import (
    CIAT,
    CIAT_URL,
    CONTACTS,
    EVIDENCE,
    EVIDENCE_BASE,
    EVIDENCE_BASE_DATE,
    EVIDENCE_LIVE,
    EVIDENCE_REV,
    EVIDENCE_URL,
    LIVE_LABEL,
    LIVE_RATING_STATUS,
    LIVE_REVIEWS,
    LIVE_SNAPSHOT,
    METHOD,
    METHOD_REV,
    NAV,
    NAV_TIP,
    PIN,
    PAGES,
    PRACTICE_IDS,
    PRACTICE_TEXT,
    PRODUCER,
    PRODUCTS,
    RELEASE,
    RELEASES_URL,
    REVIEW_QUEUES,
    ROW_TABLES,
    RUNTIME,
    RUNTIME_URL,
    SIDE,
    SITE_NAME,
    SITE_REV,
    TABLE_NAMES,
    VERSION,
    VERSION_DATE,
    VERSION_STATUS,
    VISUAL_URL,
    badge,
    code,
    esc,
    link,
    live,
    page,
    practice_name,
    table,
    words,
)
from core import family_name as core_family_name

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
                "This methodology",
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
        "This methodology does not combine counts from different sources.",
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
            ]
        )
    return table(
        ["", "Chapter", "After reading it you can"],
        rows,
        caption="Chapters in this part",
    )


# The method told as the questions a task team asks, in order. Each entry: question, plain answer,
# what the step produces, the chapters behind it, and the visual-methodology screen where one exists.
EVIDENCE_STEPS = [
    (
        "Search",
        "Research papers, practitioner databases and existing tools are searched.",
        "Every search is recorded with its terms, limits and counts, so it can be repeated.",
        "ch-discovery.html",
    ),
    (
        "Collect",
        "Each source is obtained, its identity confirmed, and a copy filed.",
        "A source that cannot be obtained and checked is left out.",
        "ch-acquisition.html",
    ),
    (
        "Extract",
        "An AI system pulls out each finding with the exact quote and where it sits.",
        "A finding is one claim from one source. Nothing is typed from memory or a summary.",
        "ch-extraction.html",
    ),
    (
        "Check",
        "Every extracted finding receives automated/AI quality checks. Human Keep, Drop or Query decisions are recorded separately.",
        "Dropped findings are kept for audit and never deleted.",
        "ch-review-and-quality.html",
    ),
    (
        "Compile",
        "Compatible findings are interpreted under the method for their target table; unresolved choices remain visible.",
        "Suitability rules, effect classes and cost profiles have different eligibility and synthesis rules.",
        "ch-compiling-evidence.html",
    ),
]
RULE_KINDS = [
    (
        "T4",
        "Where a practice fits",
        "The site conditions each family of sub-practices needs.",
    ),
    (
        "T3",
        "How it responds to climate hazards",
        "What the practice does for livelihoods under a hazard, and what threatens the practice itself.",
    ),
    (
        "T6",
        "What it delivers",
        "The effect of the practice on each priority, with a confidence level.",
    ),
    (
        "T6E",
        "What it costs",
        "Indicative costs from the literature. Not a cost-benefit analysis.",
    ),
]
STAGE_TEXT = [
    (
        "Which area, and which practices?",
        "The team sets the area it is scoping and the practices to compare.",
    ),
    (
        "What is each practice, and what does the evidence say?",
        "Each practice and its families of sub-practices, with the evidence held for each.",
    ),
    (
        "Where could each practice work?",
        "Places that meet the site conditions form the opportunity space. Legal exclusions are applied as masks.",
    ),
    (
        "What could threaten the investment?",
        "Hazards that could damage the practice, and barriers to delivery. Used as a filter or a flag, never added into a score.",
    ),
    (
        "Where do need and opportunity coincide?",
        "Climate risk to livelihoods and the team's priorities are weighted and combined inside the opportunity space.",
    ),
    (
        "What would each practice deliver, and how sure are we?",
        "Practices side by side: effect on each hazard and priority, confidence, and indicative cost.",
    ),
    (
        "What must feasibility work settle?",
        "Design, costs, national data and safeguards that only local work can settle.",
    ),
]


# Who does each evidence step and what it leaves behind, in the order of EVIDENCE_STEPS.
EVIDENCE_FLOW = [
    (
        "discovery",
        "An AI system, to a recorded protocol. People settle borderline papers.",
        "A search record",
    ),
    (
        "acquisition",
        "An AI system. Identity is checked automatically; people check what a tool cannot.",
        "A verified source file",
    ),
    (
        "extraction",
        "An AI system. Every quote and number is checked automatically.",
        "A finding, with its quote and page",
    ),
    (
        "review-and-quality",
        "Automated/AI checks on every extracted finding; human review recorded separately.",
        "A reviewed finding",
    ),
    (
        "compiling-evidence",
        "T4: agent synthesis and scientific review, followed by validation and packaging. Published rows retain their historical provenance.",
        "A row of a rule table",
    ),
]


def evidence_flow():
    """The evidence steps in order: what happens, who does it and what each step leaves."""
    steps = []
    for (name, text_, _tip, _href), (slug_, by, leaves) in zip(
        EVIDENCE_STEPS, EVIDENCE_FLOW, strict=True
    ):
        first = EVIDENCE_CH.index(slug_) + 1
        last = len(EVIDENCE_CH) if slug_ == "compiling-evidence" else first
        number = f"3.{first}" if first == last else f"3.{first} to 3.{last}"
        steps.append(
            f'<li><div class="estep"><p class="ename"><span class="mnum">{number}</span>'
            f"<b>{link(chapter_file(slug_), esc(name))}</b></p><p>{esc(text_)}</p>"
            f'<p><span class="elab">Done by</span>{esc(by)}</p></div>'
            f'<p class="ehand"><span class="elab">leaves</span><span class="erec">{esc(leaves)}</span></p></li>'
        )
    return (
        '<figure class="eflow" id="evidence-flow">'
        f'<ol class="esteps">{"".join(steps)}</ol>'
        "<figcaption>From a search to a rule, in five steps. Each step leaves a record that the next one reads, "
        "so any rule can be followed back to the page it came from. Select a step to read its chapter.</figcaption>"
        "</figure>"
    )


def method_map():
    """The method in one figure: how evidence becomes rules, then the seven stages that apply them."""
    evidence = "".join(
        f'<li title="{esc(tip)}"><b>{link(href, esc(name))}</b><span>{esc(text_)}</span></li>'
        for name, text_, tip, href in EVIDENCE_STEPS
    )
    rules = "".join(
        f'<li><a href="table-{t}.html" title="{esc(tip)}">{badge(t)} {esc(label)}</a></li>'
        for t, label, tip in RULE_KINDS
    )
    stages = "".join(
        f'<li title="{esc(tip)}"><span class="mnum">Stage {i}</span><b>{link(chapter_file(slug_), esc(name))}</b>'
        f"<span>{esc(question)}</span>"
        f'<span class="mlinks">{link(VISUAL_URL + screen, "See the screen")}</span></li>'
        for i, ((screen, name, slug_), (question, tip)) in enumerate(
            zip(STAGES, STAGE_TEXT, strict=True), 1
        )
    )
    return (
        '<figure class="mmap" id="method-map">'
        '<div class="mband"><div class="mhead"><span class="mtag" aria-hidden="true">A</span>'
        '<p class="mtitle">Build the evidence base</p>'
        "<p>Done once for each practice. An AI system does the reading. People check its work and decide.</p></div>"
        f'<ol class="msteps">{evidence}</ol></div>'
        f'<div class="mlink">which gives rules, written as tables<ul class="mrules">{rules}</ul></div>'
        '<div class="mband"><div class="mhead"><span class="mtag" aria-hidden="true">B</span>'
        '<p class="mtitle">Apply the rules to a landscape</p>'
        "<p>Seven stages a project team walks through, using public spatial data.</p></div>"
        f'<ol class="msteps seven">{stages}</ol></div>'
        '<div class="mlink out">which gives<p>Traceable, citable evidence on where each practice could work '
        "and what it would deliver, to inform planning and investment decisions.</p></div>"
        "<figcaption>The method in one figure. Select a step to read its chapter. Hover over a box for one more "
        "line of detail. “See the screen” opens that stage in the visual methodology.</figcaption></figure>"
    )


def build():
    SIDE["method.html"] = [(chapter_file(s), TITLES.get(s, s)) for s in METHOD_CH]
    SIDE["evidence-methods.html"] = [
        (chapter_file(s), TITLES.get(s, s)) for s in EVIDENCE_CH
    ]
    SIDE["editions.html"] = [
        ("editions.html", "About versions and changes"),
        ("status.html", "What is established"),
        ("reproduce.html", "Reproduce and check"),
        ("glossary.html", "Glossary"),
    ]
    chapter_pages("method.html", METHOD_CH, 2)
    chapter_pages("evidence-methods.html", EVIDENCE_CH, 3)
    # Preserve the published guide addresses without retaining duplicate chapters in navigation.
    for old, target in (("evidence-registry", "evidence-principles"),
                        ("combining-t4-evidence", "compiling-evidence"),
                        ("t4-legacy-compiler", "suitability-synthesis")):
        destination = chapter_file(target)
        filename = chapter_file(old)
        page(filename, "evidence-methods.html", "Evidence guidance has moved",
             f'<p>This guidance is now integrated into {link(destination, esc(TITLES[target]))}.</p>')
        PAGES[filename] = PAGES[filename].replace(
            "</head>", f'<link rel="canonical" href="{destination}">'
            f'<meta http-equiv="refresh" content="0;url={destination}"></head>', 1)

    s = t4_status()
    kept = [u for u in data.EV if data.retained(u)]
    fam_registered = sorted({f["suitability_family_id"] for f in data.FAM})
    effect_rows = [r for r in data.ROWS if r["table"] != "T4"]

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
        "<p>These methods explain how sources become evidence and how reviewed claims support different "
        "analytical decisions. Start with "
        + link(chapter_file("evidence-principles"), "Evidence records and source appraisal")
        + " for the shared concepts, source limitations and roles of the analytical tables. "
        "Then follow the preparation steps below.</p>"
        + evidence_flow()
        + "<p>After review, " + link(chapter_file("compiling-evidence"), "Combining evidence into analytical tables")
        + " covers compatibility, repeated observations, shared sources, weighting and uncertainty. "
        "The following chapters describe agent-led suitability synthesis (T4) and the separate methods for hazard and scorecard effects "
        "(T3/T6), and economic profiles (T6E). Dataset, hazard, context and priority configuration have different "
        "requirements, linked from the opening chapter.</p>"
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
    overview_lead = (
        "Where in a rural landscape could nature-based solutions work, what would they deliver there, and "
        "how strong is the evidence? The Rural NbS Scan is a method for answering those questions early, "
        "before detailed studies are commissioned."
    )
    visual = VISUAL_URL + "index.html"
    none_yet = [
        practice_name(p) for p in PRACTICE_IDS if data.ROW_COUNTS[(p, "T4")] == 0
    ]
    body = (
        '<p class="routes"><a class="go" href="#how">How the method works</a>'
        f'<a href="{visual}">Open the visual methodology</a>'
        '<a href="practices.html">Practices and their evidence</a>'
        '<a href="method.html">Technical specification</a></p>'
        '<p>' + link('help.html#citation', 'Cite this edition') + ' · ' + link('help.html#team', 'Project team and counterparts') + '</p>'
        '<h2 id="problem">The problem</h2>'
        "<p>Nature-based solutions are practices that work with natural processes to protect land, water and "
        "livelihoods: growing trees on farms, harvesting rainwater, restoring forests, wetlands, riverbanks "
        "and mangroves.</p>"
        "<p>A team preparing a rural investment that wants to use them faces a scoping question first. Across "
        "a country or a large landscape, where is each practice worth a closer look, and what is it likely to "
        "achieve there? Answering it means bringing together three things that rarely sit in one place:</p><ul>"
        "<li>what research and field experience say about where a practice works and what it delivers;</li>"
        "<li>maps of the conditions that matter, such as rainfall, slope, soils and current land use;</li>"
        "<li>the priorities of the investment, such as poverty, food security, climate risk and biodiversity.</li></ul>"
        "<p><strong>The bottleneck is the first of these.</strong> The evidence is spread across thousands of "
        "studies, practitioner databases and earlier tools. They report different measures, in different units, "
        "for different places. Turning that into rules that can be put on a map takes specialist time, and it "
        "has to be done again for each practice. Early scoping therefore tends to rest on expert judgement "
        "applied differently each time, or on tools whose thresholds cannot be traced to a source.</p>"
        '<h2 id="answer">What the method does about it</h2>'
        "<p>The method removes that bottleneck in two moves.</p><ol>"
        "<li><strong>It does the evidence work once, in the open.</strong> For each practice, sources are "
        "searched, read and broken into individual findings, each stored with the exact quote and the page it "
        "came from. An AI system does the reading. Every extracted finding receives automated/AI quality checks; human review is recorded separately. "
        "The findings are then pooled into rules: where the practice fits, how it responds to climate hazards, "
        "what it delivers and what it costs.</li>"
        "<li><strong>It applies those rules in a fixed order.</strong> Seven stages take a team from choosing "
        "an area to a shortlist of places and practices, using public spatial data. Each stage answers one "
        "question, and each result can be followed back to the rule and the evidence behind it.</li></ol>"
        "<p>What this makes possible:</p><ul>"
        "<li><strong>A consistent first screen.</strong> Practices and places are compared on the same basis.</li>"
        "<li><strong>Better-aimed feasibility work.</strong> Detailed studies go where they are most likely to pay off.</li>"
        "<li><strong>Visible gaps.</strong> Where evidence is thin, comes only from other regions, or disagrees, the result says so.</li>"
        "<li><strong>Reuse.</strong> Adding a practice or updating the evidence changes the rules, not the software.</li></ul>"
        '<p class="callout">The scan is a scoping method. It flags where to look. It does not show that a '
        "practice will succeed on a given site, and local feasibility assessment is still needed before any "
        "investment decision.</p>"
        '<h2 id="audience">Who it is for</h2>'
        + table(
            ["", "Reader or task", "Detail"],
            [
                [
                    "For",
                    "Teams scoping a rural investment, and their government counterparts",
                    "Early in project preparation: to shortlist landscapes and practices and to brief feasibility work.",
                ],
                [
                    "For",
                    "Technical reviewers",
                    "To check where a rule or a rating came from.",
                ],
                [
                    "For",
                    "Analysts",
                    "To run the scan for a country, or to build software that does.",
                ],
                [
                    "Not for",
                    "Site design",
                    "Designing a site, sizing a structure or choosing species.",
                ],
                [
                    "Not for",
                    "Economic appraisal",
                    "Cost-benefit analysis, or detailed modelling of ecosystem services.",
                ],
                [
                    "Not for",
                    "Standing in for local sources",
                    (
                        "Replacing national data, local knowledge or consultation. Where national data should be "
                        "used, the scan says so."
                    ),
                ],
            ],
            caption="Who the method is for, and what it is not for",
        )
        + '<h2 id="how">How the method works</h2>'
        "<p>The method has two halves. The first builds the evidence base and turns it into rules. The second "
        "applies those rules to a landscape. The figure shows both, in order.</p>"
        + method_map()
        + "<p>In the lower row, each stage narrows the question for the next. Setup fixes the area and the "
        "practices. Exploring the practices shows what each one is and what the evidence says about it. The "
        "opportunity space shows where each could work. The project-risk screen removes or flags places where "
        "the investment itself would be exposed. Priority hotspots show where need is greatest inside what "
        "remains. The comparison sets the practices side by side on what they deliver. Next steps list what "
        "feasibility work must settle.</p>"
        f"<p>The {link(visual, 'visual methodology')} shows the same seven stages as screens: an interactive "
        "mock-up of how the method could run as a geospatial prioritisation platform, with the maps, controls "
        "and outputs of each stage. Every map and number on its screens is example data, not a result. "
        f"The {link(chapter_file('scoping-walkthrough'), 'stage-by-stage guide')} describes each screen.</p>"
        '<p class="basis">The technical chapters call the analysis steps modules (M0 to M6) and number the '
        f"rule tables (T0 to T7). {link('method.html', 'Method')} explains each module. "
        f"{link('data-model.html', 'Data model')} defines each table.</p>"
        '<h2 id="origins">How the method was built</h2>'
        "<p>The method starts from what exists. A stocktake of published spatial-suitability studies and tools "
        "gave the first set of sources. The scoring and weighting techniques are established ones, inherited "
        "from an earlier water-harvesting method.</p>"
        "<p>No threshold or rating goes from a document to a rule in one step. Each passes through a finding "
        "that carries its quote. The rules themselves are written as tables, so people and software read the "
        "same thing and a rule can change without rewriting software. A few synthesis constants remain in code "
        "and are stated in the chapters.</p>"
        "<p>A bench terrace and a sand dam are not sited by the same rules, so each practice is split into "
        "families of sub-practices that share a limiting factor.</p>"
        "<p>Risk to rural livelihoods and risk to the investment are kept apart. The first measures need. The "
        "second is a filter. They are never added together.</p>"
        f"<p>{link('ch-scope-and-framework.html', 'Scope and framework')} sets these principles out in full.</p>"
        '<h2 id="coverage">What it covers today</h2>'
        f"<p>This edition holds evidence for {len(PRACTICE_IDS)} practices, split into {len(fam_registered)} "
        'families of sub-practices.</p><ul class="plist">'
        + "".join(
            f"<li>{link(f'practice-{p}.html', esc(practice_name(p)))}. {esc(PRACTICE_TEXT[p][0])}</li>"
            for p in PRACTICE_IDS
        )
        + f"</ul><p>{link('practices.html', 'How much evidence each practice has, and every compiled rule')}.</p>"
        '<h2 id="status">What is settled, and what is not</h2>'
        + table(
            ["State", "What it covers"],
            [
                [
                    "Written down",
                    (
                        "The full method: seven analysis steps and the project-risk screen, each with its formulas "
                        "and limits."
                    ),
                ],
                [
                    "Compiled",
                    (
                        f"Evidence for all {len(PRACTICE_IDS)} practices: {len(data.SRC):,} sources, {len(kept):,} "
                        f"findings retained (excluding dropped records) and {len(data.ROWS):,} compiled rows. These counts show coverage and effort, "
                        "not strength of evidence. Each rating states its own confidence."
                    ),
                ],
                [
                    "Not yet settled",
                    (
                        (
                            f"Only {s['approved']} of {s['total']} suitability rules have an approved numerical score. "
                            if s["approved"]
                            else "No suitability rule has an approved numerical score. "
                        )
                        + "The method can say which conditions matter for a practice, and in which direction, but "
                        "cannot yet score a place. "
                        + (
                            f"{' and '.join(none_yet)} {'has' if len(none_yet) == 1 else 'have'} no suitability "
                            "rules yet."
                            if none_yet
                            else ""
                        )
                    ),
                ],
                [
                    "Planned change",
                    (
                        "New T4 mappings will be derived by an AI agent and reviewed before validation and packaging. "
                        "The production route is not certified by this edition; its displayed rows retain their historical provenance. "
                        f"{link('ch-suitability-synthesis.html', 'Agent-led suitability synthesis')}."
                    ),
                ],
                [
                    "Not in this edition",
                    "Maps and country results. A country application is run separately as a pilot.",
                ],
            ],
            caption="What is settled in this edition, and what is not",
        )
        + "<p>Review happens in the live dashboard. Each finding is shown beside the passage it was taken from, "
        "and a reviewer keeps it, drops it or raises a query.</p>"
        + review_queues()
        + f"<p>{link('status.html', 'Full status tables')} · {link('review.html', 'How review records are kept')}</p>"
        '<h2 id="parts">Where to find the detail</h2>'
        + table(
            ["Part", "What you will find"],
            [
                [link(href, f"{i} {esc(label)}"), esc(NAV_TIP[href])]
                for i, (href, label) in enumerate(NAV, 1)
                if href != "index.html"
            ],
            caption="The six parts after this overview",
        )
    )
    page(
        "index.html",
        "index.html",
        SITE_NAME,
        body,
        lead=overview_lead,
        numbered=True,
    )

    # ------------------------------------------------------------ help and change history
    issues = "https://github.com/RuralScan/method/issues"
    body = (
        "<p>This methodology documents the Rural NbS Scan in full. It is a scoping method: it shows "
        "where to look and how strong the evidence is. It holds no maps and no country results, and local "
        "feasibility work is still needed before any investment decision.</p>"
        '<h2 id="start">Finding your way</h2><dl class="glossary">'
        "<div><dt>Where should I start?</dt><dd>On the "
        f"{link('index.html', 'overview')}. It says what the method is for and who it is for, then shows "
        f"{link('index.html#how', 'how it works in one figure')}. Each step links to its technical chapter.</dd></div>"
        "<div><dt>How do I see the evidence for one practice?</dt><dd>Open "
        f"{link('practices.html', 'Practices')} and choose one. Every compiled row has its own page listing the "
        "findings behind it, each with its source and the place in the source it was taken from.</dd></div>"
        "<div><dt>Are the numbers results?</dt><dd>No. Counts of searches, sources, findings and rows describe "
        "coverage and effort. Ratings are the method’s reading of published evidence, each with a stated "
        f"confidence. {link('index.html#status', 'What is settled, and what is not')}.</dd></div>"
        "<div><dt>How does this relate to the visual methodology?</dt><dd>The "
        f"{link(VISUAL_URL + 'index.html', 'visual methodology')} shows what a working tool could look like, "
        "using example data. This methodology is the written method and the evidence behind it. "
        f"{link(chapter_file('scoping-walkthrough'), 'The scoping walkthrough')} connects the two, screen by screen.</dd></div>"
        "<div><dt>Which version am I looking at?</dt><dd>The line at the top of every page gives two numbers: "
        "the version of this methodology and the evidence base it reports. The version menu above it lists this "
        "methodology first, followed by earlier drafts. Select either version number to read its explanation and change history. "
        f"{link('editions.html#numbers', 'What the numbers mean')}.</dd></div>"
        "<div><dt>Can I download the data?</dt><dd>Yes. "
        f"{link('evidence-base.html', 'Get and use the data')} lists every table with its address and checksum, a "
        "field guide and tested queries.</dd></div></dl>"
        '<h2 id="feedback">Giving feedback</h2>'
        "<p>Choose <strong>Comment on this page</strong> in the bar at the top of any page. You can pin a comment to a table, "
        "figure or paragraph, highlight text, or capture part of the screen, and give each note a type and a "
        "severity. The same review tool is used on the visual methodology and on the live evidence dashboard.</p><ul>"
        "<li>Notes stay in your browser. Nothing is sent until you choose to share.</li>"
        "<li>Use Export to save your notes as a file or a readable report, or to open them as a public issue.</li>"
        "<li>Say what you expected and what needs to change. The page and the item are recorded for you.</li></ul>"
        "<p>Reviewing an extracted finding or a compiled rating is a different task, done in the "
        f"{link(live('review-queue'), 'review queue')} of the live dashboard. "
        f"{link('review.html', 'How review records are kept')}.</p>"
        f"<p>You can also {link(issues, 'raise a question or a correction as an issue')} in the method repository.</p>"
        + '<h2 id="citation">Citing this edition</h2>'
        + f'<p>Rural NbS Scan methodology. Version {esc(VERSION)} ({esc(VERSION_STATUS)}), {esc(VERSION_DATE)}. '
        + link("https://ruralscan.github.io/method/reference/", "https://ruralscan.github.io/method/reference/")
        + ".</p><p>This title-based citation identifies the methodology edition; "
        + f"cite evidence-base edition {esc(EVIDENCE_BASE)} as well when reporting its counts or analytical tables. "
        + link("#team", "Project team and counterparts") + " provides the existing team credit. "
        + link("editions.html", "Editions and checks") + " records the evidence and software provenance.</p>"
        + CONTACTS
    )
    page(
        "help.html",
        "index.html",
        "Help, contact and team",
        body,
        lead="How to find your way around this methodology, how to give feedback, and who to contact.",
    )

    versions, earlier = versioning.changelog()

    def entries(items):
        return "<ul>" + "".join(f"<li>{esc(x)}</li>" for x in items) + "</ul>"

    history = (
        '<h2 id="changes">What changed</h2>'
        "<p>Methodology changes, newest first. Each numbered version has "
        f"{link(RELEASES_URL, 'release notes and a fixed source revision on GitHub')}. "
        "The evidence and ratings stay the same unless an entry explicitly records an evidence-base change.</p>"
        + "".join(
            f'<h3 id="v{esc(version)}">v{esc(version)} · {versioning.long_date(day)}</h3>{entries(items)}'
            for version, day, items in versions
        )
        + '<h3 id="earlier">Before version numbers</h3>'
        + "".join(f"<h4>{esc(day)}</h4>{entries(items)}" for day, items in earlier)
    )
    # Keep shared historical URLs, including version anchors, without duplicating the history.
    page("changes.html", "editions.html", "Version history has moved",
         '<p>Version explanations and the full change history are now together on '
         + link('editions.html#changes', 'About versions and changes') + '.</p>'
         + ''.join(f'<span id="v{esc(v)}"></span>' for v, _, _ in versions)
         + '<span id="earlier"></span><span id="feedback"></span>')
    PAGES["changes.html"] = PAGES["changes.html"].replace(
        '</head>', '<link rel="canonical" href="editions.html">'
        '<script>location.replace("editions.html" + (location.hash || "#changes"));</script></head>', 1)

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
        "<p>Every extracted finding receives automated/AI quality checks. Human review is recorded separately: "
        f"{sum(1 for u in kept if u.get('reviewer_ok') is True):,} of {len(kept):,} retained findings have a recorded human approval. "
        "This is not a measure of total QC coverage. Approval covers the recorded review scope; it does not itself approve a compiled mapping or numerical calibration. "
        f"{len(data.EV) - len(kept):,} findings were dropped, by a reviewer or by the automated off-scope quarantine, and are kept for audit. The automated provenance gates and the "
        f"review process are described in {link('ch-review-and-quality.html', 'review and quality')}.</p>"
        '<h2 id="not">What this edition does not establish</h2><ul>'
        "<li>No suitability mapping has an approved numerical calibration, and none is execution-ready.</li>"
        "<li>Country results, maps and pilot outputs are outside this methodology.</li>"
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
        "histories from that repository and lets a signed-in reviewer submit a finding review. This methodology shows the "
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
        "the hazard, suitability and scorecard tables. At the evidence revision this methodology was built against, the "
        "rating log held only the events copied from the producer repository. This methodology does not write decisions.</p>"
        f"<p>{link(EVIDENCE_LIVE + 'workflows/submissions/README.md', 'How to submit a finding vote or an extraction proposal')} · "
        f"{link(EVIDENCE_LIVE + 'workflows/submissions/recipe-rows.md', 'How to review a rating or suggest row wording')}.</p>"
        '<h2 id="pins">Which revision is which</h2>'
        "<p>The live dashboard pins its analytical snapshot to a producer revision later than this methodology’s. Its review "
        "history is not pinned: it is read from the evidence repository’s current main branch when the page loads. Only the "
        "provisional status of hazard ratings is taken from the same revision as this methodology. "
        "A review state shown on a row or finding page here is the state at this methodology’s revision and can be older "
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
            f"Evidence base {EVIDENCE_BASE}: recipe release",
            "Rule tables. Draft: candidate, not released",
            code(RELEASE),
            f"{len(data.ROWS)} rows: "
            + ", ".join(f"{data.TABLE_TOTALS[t]} {t}" for t in ROW_TABLES),
        ],
        [
            "Producer revision",
            "Recipe tables and evidence registers are read from this one revision",
            link(CIAT_URL, code(PRODUCER)),
            "All counts in this methodology",
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
    state = "draft" if VERSION_STATUS == "draft" else "released"
    body = (
        '<h2 id="numbers">About the version numbers</h2>'
        "<p>Two independently numbered versions identify what you are reading: the written methodology "
        "and the fixed evidence base it reports. Updating the text does not by itself change the evidence or ratings.</p>"
        '<h3 id="methodology">Methodology version</h3>'
        f"<p><strong>v{esc(VERSION)}</strong> · {state} · {versioning.long_date(VERSION_DATE)}. "
        "The number follows <strong>major.minor.patch</strong>: major changes alter how the method works and "
        "could change results; minor changes add or rewrite chapters or sections; patch changes correct wording "
        "or layout. Versions before 1.0.0 are drafts; 1.0.0 will be the first released version.</p>"
        f"<p>{link('#changes', 'Read the change history below')} or "
        f"{link(RELEASES_URL, 'open the tagged releases on GitHub')} to recover an earlier version.</p>"
        '<h3 id="evidence-base">Evidence-base version</h3>'
        f"<p><strong>v{esc(EVIDENCE_BASE)}</strong> · {versioning.long_date(EVIDENCE_BASE_DATE)}. "
        "The number follows <strong>year.month.release</strong>: the year and month, then the release number "
        "within that month. It changes when a new fixed set of analytical tables and evidence registers is adopted. "
        "The exact inputs are recorded below. Current review decisions can be newer than this fixed evidence base.</p>"
        f"<p>{link('evidence-base.html', 'Browse and download this evidence base')}. "
        f"{link('#inputs', 'See its exact source revisions')}.</p>"
        + history
        + '<h2 id="inputs">What this version was built from</h2>'
        "<p>An edition is one fixed set of inputs. Everything in this methodology is read from the identifiers "
        "below, so a number here can be reproduced exactly. Counts from different editions are never added, "
        "subtracted or turned into a rate.</p>"
        + table(
            ["Input", "Role", "Identifier", "Used for"],
            rows,
            caption="Inputs to this methodology",
        )
    )
    body += (
        '<h2 id="live">The live dashboard pins its analytical revisions and reads current review records</h2>'
        "<p>The live evidence dashboard is a separate product from this methodology. It pins the revision of its analytical "
        "snapshot, which is later than the revision this methodology is built on. Its review history is read from the evidence "
        "repository’s current records when the page loads. "
        "Its hazard-rating review status is taken from an assessment made at this methodology’s revision, after checking that "
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
        "<p><strong>Version</strong> is the number of this methodology or of an evidence base. <strong>Edition</strong> is used for a fixed set of inputs. <strong>Release</strong> is the content-addressed build of the "
        "recipe tables. <strong>Candidate</strong> means built and checked but not yet released. <strong>Draft</strong> is the plain word "
        "used on the first screen for the same state. Schema and ruleset versions are separate and are named as versions. "
        f"See the {link('glossary.html', 'glossary')}.</p>"
    )
    body += (
        '<h2 id="feedback">Feedback and review history</h2>'
        "<p>Choose <strong>Comment on this page</strong> in the top bar to leave notes on this methodology. "
        f"{link('help.html#feedback', 'How to share feedback')}. Changes made in response appear in the history above.</p>"
        f"<p>{link(live('dashboard-history'), 'Dashboard build history and feedback')} records changes to the review workspace. "
        f"{link('review.html', 'Evidence review records')} describe finding-level decisions; these are distinct from methodology edits.</p>"
    )
    page(
        "editions.html",
        "editions.html",
        "About versions and changes",
        body,
        lead="Version meanings, full change history, exact inputs and feedback in one place.",
        toc=[("methodology", "Methodology version"), ("evidence-base", "Evidence-base version"),
             ("changes", "What changed"), ("inputs", "Exact inputs"),
             ("live", "Current review records"), ("words", "Terms"), ("feedback", "Feedback")],
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
            "One fixed set of inputs from which numbers are computed. Counts from different editions are never combined. An evidence base number stands for one edition of the rule tables and registers.",
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
        (
            "Version number",
            "The number of this methodology, written major.minor.patch, or of an evidence base, written year.month.release. Versions of the methodology before 1.0.0 are drafts.",
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
        lead="Terms as this methodology uses them.",
    )
