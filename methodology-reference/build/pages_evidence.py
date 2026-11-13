"""Evidence base: counts with definitions, sources, findings per source, search records."""

from collections import Counter

import data
from core import (
    BLOCKED_KEYS,
    PRACTICE_IDS,
    ROW_TABLES,
    SIDE,
    TABLE_NAMES,
    code,
    dl,
    esc,
    link,
    page,
    practice_name,
    render_value,
    source_file,
    table,
    text,
    words,
)


def tier(source):
    return (source.get("benchmark_tier") or "not recorded").lower()


def practices_of(source):
    raw = source.get("nbs_ids") or ""
    return [p for p in raw.replace(",", "|").split("|") if p]


def count_table(counter, label, caption, total_label="Total"):
    rows = [
        [esc(words(k)), f"{v:,}"]
        for k, v in sorted(counter.items(), key=lambda kv: -kv[1])
    ]
    rows.append(
        [
            f"<strong>{total_label}</strong>",
            f"<strong>{sum(counter.values()):,}</strong>",
        ]
    )
    return table([label, "Count"], rows, caption=caption, numeric=(1,), cls="narrow")


def locator(unit):
    if unit.get("locator"):
        return text(f"{words(unit.get('locator_type'))}: {unit['locator']}")
    if unit.get("page") not in (None, ""):
        return f"Page {esc(unit['page'])}"
    return '<span class="none">Not recorded</span>'


def source_page(source):
    sid = source["source_id"]
    units = data.EV_BY_SOURCE.get(sid, [])
    kept = [u for u in units if data.retained(u)]
    rows = data.ROWS_BY_SOURCE.get(sid, [])
    url = source.get("url") or (
        f"https://doi.org/{source['doi']}" if source.get("doi") else ""
    )
    if not str(url).startswith("http"):
        url = ""
    facts = dl(
        [
            ("Citation", esc(source.get("citation") or "")),
            ("Link", link(url, esc(url)) if url else None),
            ("Discovery process", esc(words(source.get("source_category")))),
            ("Source kind", esc(words(source.get("source_kind")))),
            ("Credibility tier", esc(tier(source))),
            (
                "Venue",
                esc(words(source.get("venue_type")))
                if source.get("venue_type")
                else None,
            ),
            (
                "Study design",
                esc(words(source.get("method_type")))
                if source.get("method_type")
                else None,
            ),
            (
                "Country and region",
                esc(
                    ", ".join(
                        x
                        for x in [source.get("study_country"), source.get("region")]
                        if x
                    )
                )
                or None,
            ),
            (
                "Income group of the study setting",
                esc(words(source.get("study_income_group")))
                if source.get("study_income_group")
                else None,
            ),
            (
                "Farming system",
                esc(words(source.get("farming_system")))
                if source.get("farming_system")
                else None,
            ),
            (
                "Spatial scale",
                esc(words(source.get("spatial_scale")))
                if source.get("spatial_scale")
                else None,
            ),
            (
                "Access",
                esc(words(source.get("access_status")))
                if source.get("access_status")
                else None,
            ),
            ("Licence", esc(source.get("license")) if source.get("license") else None),
            (
                "Practices",
                ", ".join(
                    link(f"practice-{p}.html", esc(practice_name(p)))
                    for p in practices_of(source)
                    if p in PRACTICE_IDS
                )
                or None,
            ),
            (
                "Findings",
                f"{len(kept)} retained, {len(units) - len(kept)} dropped and kept for audit",
            ),
        ]
    )
    body = facts
    if rows:
        items = "".join(
            f"<li>{link(r['file'], code(r['id']))} <small>{esc(TABLE_NAMES[r['table']])}</small></li>"
            for r in sorted(rows, key=lambda r: (r["table"], r["id"]))
        )
        body += f'<h2 id="rows">Recipe rows that cite this source ({len(rows)})</h2><ul class="cols">{items}</ul>'
    else:
        body += '<h2 id="rows">Recipe rows that cite this source</h2><p class="empty">No row in this edition cites a finding from this source.</p>'
    unit_rows = []
    for u in sorted(units, key=lambda u: (not data.retained(u), u["evidence_id"])):
        cited = data.ROWS_BY_EV.get(u["evidence_id"], [])
        unit_rows.append(
            [
                f'<span id="{esc(u["evidence_id"])}"></span>{code(u["evidence_id"])}',
                esc(words(u.get("nbs_id")))
                + (
                    f"<br><small>{esc(words((u.get('suitability_family_id') or '').split('__', 1)[-1]))}</small>"
                    if u.get("suitability_family_id")
                    else ""
                ),
                esc(words(u.get("variable")))
                + (
                    f"<br><small>source term: {text(u['raw_name'])}</small>"
                    if u.get("raw_name")
                    else ""
                ),
                esc(words(u.get("use_role"))),
                render_value(u.get("relationship")),
                locator(u),
                f"{esc(words(u.get('claim_basis')))} · {esc(words(u.get('claim_scope')))}",
                ("Retained" if data.retained(u) else "Dropped, kept for audit")
                + f"<br><small>ruleset {esc(u.get('ruleset_version') or 'not recorded')}</small>",
                ", ".join(link(r["file"], esc(r["table"])) for r in cited) or "None",
            ]
        )
    body += '<h2 id="findings">Findings extracted from this source</h2>'
    body += (
        "<p>Each finding is one evidence unit: a variable, an encoded relationship, a locator and a "
        "verbatim quote. The full quote is held in the evidence register, where it is checked against the cached "
        "source text; it is not reproduced here. Short cue phrases recorded with a relationship are shown.</p>"
        + (
            table(
                [
                    "Finding",
                    "Practice and family",
                    "Variable",
                    "Use",
                    "Encoded relationship",
                    "Locator",
                    "Basis and scope",
                    "State",
                    "Cited by rows",
                ],
                unit_rows,
                caption=f"{len(units)} findings from this source",
                cls="evidence",
            )
            if units
            else '<p class="empty">No finding is registered from this source in this edition.</p>'
        )
    )
    page(
        source_file(sid),
        "evidence-base.html",
        sid,
        body,
        crumbs=[
            ("evidence-base.html", "Evidence base"),
            ("sources.html", "Sources"),
            ("", sid),
        ],
        lead=esc(source.get("citation") or ""),
    )


def build():
    SIDE["evidence-base.html"] = [
        ("evidence-base.html", "Evidence base at this edition"),
        ("sources.html", "Sources"),
        ("searches.html", "Search records"),
        ("review.html", "Review queues and records"),
    ]
    kept = [u for u in data.EV if data.retained(u)]
    dropped = len(data.EV) - len(kept)
    cited = set(data.ROWS_BY_EV)
    cited_sources = {s for s in data.ROWS_BY_SOURCE if s}
    approved = sum(1 for u in kept if u.get("reviewer_ok") is True)

    per_practice = []
    for p in PRACTICE_IDS:
        srcs = [s for s in data.SRC if p in practices_of(s)]
        units = [u for u in kept if u.get("nbs_id") == p]
        searches = [s for s in data.SRCH if s.get("nbs_id") == p]
        behind = {
            data.EV_BY_ID[i]["source_id"]
            for r in data.ROWS
            if r["practice"] == p
            for i in r["raw"].get("evidence_ids") or []
            if i in data.EV_BY_ID
        }
        per_practice.append(
            [
                link(f"practice-{p}.html", esc(practice_name(p))),
                f"{len(searches):,}",
                f"{len(srcs):,}",
                f"{len(units):,}",
                f"{len(behind):,}",
            ]
            + [str(data.ROW_COUNTS[(p, t)]) for t in ROW_TABLES]
        )
    reported = Counter()
    sums = Counter()
    for s in data.SRCH:
        for key in ("n_retrieved", "n_screened", "n_included"):
            value = s.get(key)
            if isinstance(value, (int, float)) and not isinstance(value, bool):
                reported[key] += 1
                sums[key] += value
    body = (
        "<p>This page counts what the evidence registers hold at one pinned revision, the same revision "
        "the recipe rows were compiled from. Every number has a definition. None is a measure of evidence "
        "strength: a row resting on many findings can still carry low confidence, and the confidence of "
        "each row is stated on the row.</p>"
        '<div class="stats">'
        f"<div><b>{len(data.SRCH):,}</b><span>search records</span></div>"
        f"<div><b>{len(data.SRC):,}</b><span>sources registered</span></div>"
        f"<div><b>{len(kept):,}</b><span>findings retained</span></div>"
        f"<div><b>{len(cited):,}</b><span>findings cited by recipe rows</span></div>"
        f"<div><b>{len(data.ROWS):,}</b><span>recipe rows</span></div></div>"
        '<p class="basis">Do not read these as a funnel. Searches, sources, findings and rows are different units, '
        "and one source contributes to several rows.</p>"
        '<h2 id="definitions">Definitions</h2>'
        + table(
            ["Count", "Value", "Definition"],
            [
                [
                    "Search records",
                    f"{len(data.SRCH):,}",
                    "Rows in the search register: one per practice or sub-practice, table and discovery process, each with its search terms, screening steps, inclusion criteria and ruleset version.",
                ],
                [
                    "Sources registered",
                    f"{len(data.SRC):,}",
                    "Rows in the source register: documents and tool code that passed screening. Dataset intake is paused. "
                    + f"{sum(1 for x in data.SRC if not x.get('artifact_sha1')):,} sources record no artefact hash.",
                ],
                [
                    "Findings registered",
                    f"{len(data.EV):,}",
                    "Rows in the evidence register. One finding is one variable and relationship at one locator in one source, with a verbatim quote.",
                ],
                [
                    "Findings retained",
                    f"{len(kept):,}",
                    "Findings whose review state is not “dropped”. These are available to synthesis.",
                ],
                [
                    "Findings dropped, kept for audit",
                    f"{dropped:,}",
                    "Findings dropped by a reviewer or by the automated off-scope quarantine. They are never deleted, are excluded from synthesis, and can be re-opened.",
                ],
                [
                    "Findings kept by a reviewer after a flag",
                    f"{approved:,}",
                    "Retained findings whose <code>reviewer_ok</code> field is true: a reviewer kept or reclassified the finding after it was flagged. This confirms the finding against its quote, not its numbers or any calibration. Findings that were never flagged may not have been seen by a reviewer.",
                ],
                [
                    "Findings cited by recipe rows",
                    f"{len(cited):,}",
                    "Distinct findings named in the <code>evidence_ids</code> of at least one of the recipe rows in this edition.",
                ],
                [
                    "Sources behind recipe rows",
                    f"{len(cited_sources):,}",
                    "Distinct sources of those cited findings.",
                ],
                [
                    "Recipe rows",
                    f"{len(data.ROWS):,}",
                    "Rows of the four recipe tables in the draft edition: "
                    + ", ".join(
                        f"{data.TABLE_TOTALS[t]} {TABLE_NAMES[t].lower()}"
                        for t in ROW_TABLES
                    )
                    + ".",
                ],
            ],
            caption="What each count means",
            numeric=(1,),
        )
        + '<h2 id="practice">By practice</h2>'
        + table(
            [
                "Practice",
                "Search records",
                "Sources",
                "Findings retained",
                "Sources behind rows",
            ]
            + [TABLE_NAMES[t] for t in ROW_TABLES],
            per_practice,
            caption="Evidence base by practice. A source that serves two practices is counted under both.",
            numeric=(1, 2, 3, 4, 5, 6, 7, 8),
        )
        + '<h2 id="sources">Sources</h2><div class="grid2">'
        + count_table(
            Counter(s.get("source_category") or "not recorded" for s in data.SRC),
            "Discovery process",
            "Sources by discovery process",
        )
        + count_table(
            Counter(tier(s) for s in data.SRC),
            "Credibility tier",
            "Sources by credibility tier",
        )
        + count_table(
            Counter(s.get("venue_type") or "not recorded" for s in data.SRC),
            "Venue",
            "Sources by venue",
        )
        + count_table(
            Counter(s.get("study_income_group") or "not recorded" for s in data.SRC),
            "Income group",
            "Sources by income group of the study setting",
        )
        + count_table(
            Counter(s.get("method_type") or "not recorded" for s in data.SRC),
            "Study design",
            "Sources by study design",
        )
        + count_table(
            Counter(s.get("access_status") or "not recorded" for s in data.SRC),
            "Access",
            "Sources by access status",
        )
        + '</div><h2 id="findings">Findings retained</h2><div class="grid2">'
        + count_table(
            Counter(u.get("use_role") or "not recorded" for u in kept),
            "Use",
            "Retained findings by use in the method",
        )
        + count_table(
            Counter(u.get("claim_scope") or "not recorded" for u in kept),
            "Claim scope",
            "Retained findings by claim scope",
        )
        + count_table(
            Counter(u.get("claim_basis") or "not recorded" for u in kept),
            "Claim basis",
            "Retained findings by claim basis",
        )
        + count_table(
            Counter(u.get("evidence_type") or "not recorded" for u in kept),
            "Evidence type",
            "Retained findings by evidence type",
        )
        + "</div>"
        "<p>Species-specific and crop-specific findings are kept but routed away from practice-level rows; crop-specific findings re-enter only where the crop-scope policy allows it. "
        "Findings read from tool code are design choices, recorded as expert assertion and weighted down. "
        f"See {link('ch-extraction.html', 'extraction')} and {link('ch-review-and-quality.html', 'review and quality')}.</p>"
        '<h2 id="searches">Searches</h2><div class="grid2">'
        + count_table(
            Counter(s.get("table") or "not recorded" for s in data.SRCH),
            "Table",
            "Search records by target table",
        )
        + count_table(
            Counter(s.get("category") or "not recorded" for s in data.SRCH),
            "Discovery process",
            "Search records by discovery process",
        )
        + "</div>"
        + table(
            [
                "Reported field",
                "Search records reporting it",
                "All search records",
                "Sum of reported values",
            ],
            [
                [code(k), f"{reported[k]:,}", f"{len(data.SRCH):,}", f"{sums[k]:,.0f}"]
                for k in ("n_retrieved", "n_screened", "n_included")
                if reported[k]
            ],
            caption="Screening counts as reported. Searches overlap, so a sum is not a count of unique records. Where a field is missing it was not reported.",
            numeric=(1, 2, 3),
        )
        + f"<p>Every search record is listed in {link('searches.html', 'Search records')} with its terms, criteria and ruleset version. "
        f"The method is described in {link('ch-discovery.html', 'discovery')}.</p>"
    )
    page(
        "evidence-base.html",
        "evidence-base.html",
        "Evidence base at this edition",
        body,
        lead="What the registers hold, with a definition for every count.",
        toc=[
            ("definitions", "Definitions"),
            ("practice", "By practice"),
            ("sources", "Sources"),
            ("findings", "Findings retained"),
            ("searches", "Searches"),
        ],
    )

    # Sources index
    rows = []
    for s in sorted(
        data.SRC, key=lambda s: (s.get("citation") or s["source_id"]).lower()
    ):
        units = data.EV_BY_SOURCE.get(s["source_id"], [])
        rows.append(
            [
                link(
                    source_file(s["source_id"]),
                    esc(s.get("citation") or s["source_id"]),
                ),
                esc(words(s.get("source_category"))),
                esc(tier(s)),
                esc(words(s.get("venue_type"))) if s.get("venue_type") else "",
                esc(words(s.get("study_income_group")))
                if s.get("study_income_group")
                else "",
                esc(", ".join(words(p) for p in practices_of(s))),
                str(sum(1 for u in units if data.retained(u))),
                str(len(data.ROWS_BY_SOURCE.get(s["source_id"], []))),
            ]
        )
    body = (
        "<p>Every source in the register, with its discovery process, credibility tier and how much of the "
        "method rests on it. Open a source for its findings and the rows that cite them.</p>"
        '<p><label for="sf">Filter sources</label> <input id="sf" type="search" data-filter="src" placeholder="author, year, practice, tier"></p>'
        + table(
            [
                "Source",
                "Discovery process",
                "Tier",
                "Venue",
                "Income group",
                "Practices",
                "Findings retained",
                "Rows citing",
            ],
            rows,
            caption=f"Source register · {len(rows)} sources",
            ident="src",
            numeric=(6, 7),
        )
    )
    page(
        "sources.html",
        "evidence-base.html",
        "Sources",
        body,
        crumbs=[("evidence-base.html", "Evidence base"), ("", "Sources")],
        lead=f"{len(rows)} registered sources.",
    )
    for s in data.SRC:
        source_page(s)

    # Search records
    shown = [
        "nbs_id",
        "table",
        "category",
        "search_date",
        "ruleset_version",
        "n_retrieved",
        "n_screened",
        "n_included",
    ]
    rows = []
    for s in sorted(
        data.SRCH,
        key=lambda s: (s.get("nbs_id") or "", s.get("table") or "", s.get("search_id")),
    ):
        rest = {
            k: v
            for k, v in s.items()
            if k not in shown
            and k != "search_id"
            and not BLOCKED_KEYS.search(k)
            and k != "run_id"
        }
        detail = f"<details><summary>Terms, criteria and limits</summary>{render_value(rest)}</details>"
        fam = s.get("family") or s.get("suitability_family_id") or ""
        rows.append(
            [
                f'<span id="{esc(s["search_id"])}"></span>{code(s["search_id"])}{detail}',
                esc(words(s.get("nbs_id")))
                + (
                    f"<br><small>{esc(words(fam.split('__', 1)[-1]))}</small>"
                    if fam
                    else ""
                ),
                esc(s.get("table") or ""),
                esc(words(s.get("category"))),
                esc(s.get("search_date") or ""),
                esc(s.get("ruleset_version") or ""),
            ]
            + [
                esc(s.get(k))
                if s.get(k) not in (None, "")
                else '<span class="none">not reported</span>'
                for k in ("n_retrieved", "n_screened", "n_included")
            ]
        )
    body = (
        "<p>One record per search actually run: practice or sub-practice, target table and discovery "
        "process. Each records the search terms, the screening steps, the inclusion criteria, the limits "
        "and the version of the search instructions in force, so the search can be repeated. "
        "A missing count means the count was not reported for that search.</p>"
        '<p><label for="qf">Filter search records</label> <input id="qf" type="search" data-filter="srch" placeholder="practice, table, process"></p>'
        + table(
            [
                "Search record",
                "Practice",
                "Table",
                "Process",
                "Date",
                "Ruleset",
                "Retrieved",
                "Screened",
                "Included",
            ],
            rows,
            caption=f"Search register · {len(rows)} records",
            ident="srch",
            numeric=(6, 7, 8),
        )
    )
    page(
        "searches.html",
        "evidence-base.html",
        "Search records",
        body,
        crumbs=[("evidence-base.html", "Evidence base"), ("", "Search records")],
        lead=f"{len(rows)} recorded searches with their protocols.",
    )
