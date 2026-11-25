"""Shared review-coverage display for sections 5 and 6, plus finding drill-down."""

import csv
import io
import json
from pathlib import Path
from urllib.parse import urlencode

import review_coverage as coverage
from core import FILES, PRACTICE_IDS, esc, link, page, practice_name, table


def finding_link(label, node="", lane="all", state="retained", relation="included"):
    query = urlencode(
        {"node": node, "lane": lane, "state": state, "relation": relation}
    )
    return link("evidence-findings.html?" + query, label)


def pin_note():
    pin = coverage.PIN
    return (
        '<p class="basis">Review snapshot: '
        + pin["date"]
        + " · "
        + link(
            f"https://github.com/{pin['repository']}/blob/{pin['revision']}/{pin['path']}",
            pin["revision"][:8],
        )
        + ". Counts use official finding decisions, not your personal queue filters. "
        "Live finding cards may include later changes. "
        + link("evidence-counts.html#definitions", "Count definitions")
        + ".</p>"
    )


def progress(node="", lane="all"):
    c = coverage.load().counts(node, lane)
    return finding_link(
        f"<strong>{c['reviewed_kept']:,} / {c['retained_total']:,}</strong>", node, lane
    )


def headline(practice=""):
    node = "practice:" + practice if practice else ""
    c = coverage.load().counts(node)
    return (
        '<section class="review-coverage"><h2 id="review-coverage">Evidence collected and reviewed</h2>'
        '<div class="stats">'
        f"<div><b>{progress(node)}</b><span>reviewed and kept / total retained</span></div>"
        f"<div><b>{finding_link(format(c['awaiting'], ','), node, state='awaiting')}</b><span>awaiting review or resolution</span></div>"
        f"<div><b>{finding_link(format(c['held'], ','), node, state='held')}</b><span>held · included in awaiting</span></div>"
        f"<div><b>{finding_link(format(c['rejected'], ','), node, state='rejected')}</b><span>rejected · excluded, history kept</span></div></div>"
        "<p>Total retained = reviewed and kept + pending + held. A hold remains unresolved. "
        "Counts measure coverage, not evidence strength or approval of a synthesis.</p>"
        + pin_note()
        + "</section>"
    )


def lane_table(practice=""):
    node = "practice:" + practice if practice else ""
    model = coverage.load()
    rows = []
    for lane in ("T4", "effects", "M2b", "other", "T3", "T6"):
        c = model.counts(node, lane)
        if not c["registered_total"] and lane == "other":
            continue
        rows.append(
            [
                esc(coverage.LANES[lane]),
                progress(node, lane),
                finding_link(str(c["awaiting"]), node, lane, "awaiting"),
                finding_link(str(c["held"]), node, lane, "held"),
                finding_link(str(c["rejected"]), node, lane, "rejected"),
            ]
        )
    return (
        table(
            [
                "Evidence",
                "Reviewed and kept / total retained",
                "Awaiting",
                "Of which held",
                "Rejected",
            ],
            rows,
            caption="Finding coverage by review lane",
            numeric=(1, 2, 3, 4),
        )
        + '<p class="basis">All collected effects includes uncited findings awaiting synthesis. '
        "T3 and T6 cited subsets match the review queue’s membership lists; they can overlap. "
        "Do not add these subsets to the totals. M2b here covers operational feasibility findings; "
        "asset-hazard findings are in collected effects.</p>"
    )


def practice_table():
    rows = []
    for p in PRACTICE_IDS:
        node = "practice:" + p
        c = coverage.load().counts(node)
        rows.append(
            [
                link(f"evidence-practice-{p}.html", esc(practice_name(p))),
                progress(node),
                finding_link(str(c["awaiting"]), node, state="awaiting"),
                finding_link(str(c["held"]), node, state="held"),
                finding_link(str(c["rejected"]), node, state="rejected"),
            ]
        )
    return table(
        [
            "Practice",
            "Reviewed and kept / total retained",
            "Awaiting",
            "Of which held",
            "Rejected",
        ],
        rows,
        caption="Evidence review coverage across the six practices",
        numeric=(1, 2, 3, 4),
    )


def scope_table(practice):
    model = coverage.load()
    rows = []
    for key, node in sorted(model.nodes.items()):
        if node["nbs_id"] != practice or node["level"] not in {
            "family",
            "group",
            "legacy_family",
        }:
            continue
        name = node["label"].split("__")[-1].replace("_", " ").capitalize()
        level = {
            "group": "Broader group",
            "family": "Family",
            "legacy_family": "Earlier scope · reassignment pending",
        }[node["level"]]
        broader = model.counts(key, relation="broader")
        legacy = model.counts(key, relation="legacy")
        rows.append(
            [
                finding_link(esc(name), key) + f"<br><small>{level}</small>",
                progress(key),
                finding_link(str(broader["retained_total"]), key, relation="broader"),
                finding_link(str(legacy["retained_total"]), key, relation="legacy"),
            ]
        )
    return (
        "<details><summary>Evidence by family and broader group</summary>"
        "<p>Specific findings roll up to broader groups once per evidence ID. Broad findings remain visible "
        "as context; they are not assigned down to a particular child. Earlier family scopes remain "
        "accessible pending source-scope review. Zero specific findings does not mean zero broader evidence.</p>"
        + table(
            [
                "Scope",
                "Reviewed and kept / total retained",
                "Broader retained context",
                "Earlier-scope retained pointers",
            ],
            rows,
            caption="Current evidence scopes, with broader context kept separate",
            numeric=(1, 2, 3),
        )
        + "</details>"
    )


def family_suitability(family):
    """Historical mapping scopes must not be relabelled as new child families."""
    model = coverage.load()
    key = "legacy_family:" + family
    if key not in model.nodes:
        key = "family:" + family
    if key not in model.nodes:
        return ""
    c = model.counts(key, "T4")
    broader = model.counts(key, "T4", "broader")
    return (
        '<p class="basis">Collected T4 evidence at this recorded scope: '
        + progress(key, "T4")
        + " reviewed and kept / total retained; "
        + finding_link(
            str(c["awaiting"]) + " awaiting review or resolution", key, "T4", "awaiting"
        )
        + ". "
        + finding_link(
            str(broader["retained_total"]) + " broader context findings",
            key,
            "T4",
            relation="broader",
        )
        + " are separate from this total."
        + (
            " Earlier scope is preserved pending source-scope review."
            if key.startswith("legacy_family:")
            else ""
        )
        + "</p>"
    )


def build():
    model = coverage.load()
    summary = model.summary()
    FILES["data/review-coverage.json"] = (
        json.dumps(summary, ensure_ascii=False, indent=1) + "\n"
    )
    FILES["data/review-findings.json"] = (
        json.dumps(model.export(), ensure_ascii=False, separators=(",", ":")) + "\n"
    )
    out = io.StringIO()
    writer = csv.DictWriter(out, fieldnames=list(summary["rows"][0]))
    writer.writeheader()
    writer.writerows(summary["rows"])
    FILES["data/review-coverage.csv"] = out.getvalue()
    FILES["review-coverage.js"] = (
        Path(__file__).with_name("review-coverage.js").read_text()
    )
    body = (
        headline()
        + '<h2 id="practice">Review progress by practice</h2>'
        + practice_table()
    )
    body += '<h2 id="findings">Coverage by review lane</h2>' + lane_table()
    body += (
        '<h2 id="definitions">What these counts mean</h2><dl>'
        + "".join(
            f"<dt>{esc(key.replace('_', ' '))}</dt><dd>{esc(value)}</dd>"
            for key, value in coverage.DEFINITIONS.items()
        )
        + '</dl><h2 id="downloads">Download the coverage data</h2><p>'
        + link("data/review-coverage.csv", "Counts CSV")
        + " · "
        + link("data/review-coverage.json", "Counts and definitions JSON")
        + " · "
        + link("data/review-findings.json", "Finding IDs, scopes and statuses JSON")
        + "</p>"
        '<h2 id="sources">Historical edition and sources</h2><p id="searches">'
        "Recipe rows, search records and source pages below retain their original edition pin. "
        "They are not newly accepted outputs from the review snapshot. "
        + link("edition-counts.html", "Historical edition counts and definitions")
        + " · "
        + link("evidence-base.html#download", "Historical edition downloads")
        + "</p>"
    )
    page(
        "evidence-counts.html",
        "evidence-base.html",
        "Evidence counts and review progress",
        body,
        lead="Reviewed versus total, with pending, held and broader evidence still accessible.",
    )
    for practice in PRACTICE_IDS:
        name = practice_name(practice)
        body = (
            '<p>' + link(f"practice-{practice}.html", "Practice definition and sub-practices") + ' · '
            + finding_link("Browse all retained findings →", "practice:" + practice) + '</p>'
            + headline(practice)
            + '<p>' + finding_link("Browse reviewed and kept findings", "practice:" + practice, state="reviewed_kept") + '</p>'
            + '<h2 id="lanes">Evidence by table and review lane</h2>' + lane_table(practice)
            + '<h2 id="scopes">Family and broader evidence</h2>' + scope_table(practice)
            + '<h2 id="records">Historical recipe records</h2><p>Compiled outputs are separate from collected findings. '
            'A practice can have pending evidence without a compiled mapping. '
            + link(f"practice-{practice}.html#historical-rows", "Inspect the earlier T4, T3, T6 and T6E records") + '.</p>'
        )
        page(f"evidence-practice-{practice}.html", "evidence-base.html", name + ": evidence",
             body, crumbs=[("evidence-base.html", "Evidence base"), ("", name)],
             lead="Review progress and findings, including pending, held and broader evidence.",
             toc=[("review-coverage", "Reviewed versus total"), ("lanes", "Tables and review lanes"),
                  ("scopes", "Family and broader evidence"), ("records", "Historical outputs")])

    options = lambda values: "".join(
        f'<option value="{esc(k)}">{esc(v)}</option>' for k, v in values.items()
    )
    body = (
        pin_note()
        + "<p>Browse the findings behind a count. Open a finding to inspect its source and review history in the live queue.</p>"
        '<div id="coverage-browser"><form id="coverage-filters" class="grid3">'
        '<label>Practice or evidence scope<select name="node"><option value="">All practices</option></select></label>'
        '<label>Evidence lane<select name="lane">'
        + options(coverage.LANES)
        + "</select></label>"
        '<label>Review status<select name="state">'
        + options(coverage.STATES)
        + "</select></label>"
        '<label>Relationship to scope<select name="relation">'
        + options(coverage.RELATIONS)
        + "</select></label>"
        '<label>Find a source, variable or evidence ID<input name="q" type="search" placeholder="Search findings"></label>'
        '<div><button type="reset">Reset filters</button></div></form>'
        '<p id="coverage-status" role="status" aria-live="polite">Loading pinned findings…</p>'
        '<p id="coverage-scope-note"></p><div id="coverage-results"></div>'
        '<div class="coverage-pagination"><button id="coverage-prev" type="button">Previous</button> '
        '<span id="coverage-page"></span> <button id="coverage-next" type="button">Next</button></div></div>'
        "<noscript><p>Use the downloadable finding IDs and statuses without JavaScript.</p></noscript>"
        "<p>"
        + link("data/review-findings.json", "Download all finding IDs and statuses")
        + "</p>"
        '<script src="review-coverage.js" defer></script>'
    )
    page(
        "evidence-findings.html",
        "evidence-base.html",
        "Collected evidence findings",
        body,
        lead="Pending and broader findings remain visible even where no recipe mapping has been accepted.",
    )
