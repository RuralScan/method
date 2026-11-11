"""Render public search records and Progress from one immutable CIAT snapshot."""

import json
import re
import subprocess
from collections import defaultdict
from functools import lru_cache
from html import escape

REVISION = "bec50bc0f9dc74b3d5ffafcf881571a8a8ec5c06"
SOURCE = f"https://github.com/CIAT/nbs_ruralscan/blob/{REVISION}"
TABLE_NAMES = {
    "T2a": "Climate risk (T2, displayed as T2a)",
    "T3": "Hazard responses (T3)",
    "T4": "Structural suitability (T4)",
    "T6": "Scorecard effects (T6)",
}


@lru_cache(maxsize=1)
def _snapshot(ciat):
    raw = subprocess.check_output(
        ["git", "-C", str(ciat), "show", f"{REVISION}:docs/dashboard_data.json"]
    )
    data = json.loads(raw)
    return (
        data["progress_overview"],
        data["registers"]["SRCH_search_register"],
        data["progress_ledger"],
        data["build"]["count_definition_version"],
    )


def _label(value):
    return escape(str(value).replace("_", " "))


def _number(value):
    return f"{value:,}" if isinstance(value, int) else "Not recorded"


def _path(record):
    identifier = record["search_id"]
    if not re.fullmatch(r"[a-zA-Z0-9_.-]+", identifier):
        raise ValueError(f"Unsafe search record ID: {identifier}")
    return f"search-{identifier}.html"


def _link(url, label):
    return f'<a href="{escape(url, quote=True)}">{escape(label)}</a>'


def _table(caption, headings, rows):
    columns = "".join(f'<th scope="col">{escape(title)}</th>' for title in headings)
    body = "".join(
        '<tr><th scope="row">'
        + row[0]
        + "</th>"
        + "".join(f"<td>{value}</td>" for value in row[1:])
        + "</tr>"
        for row in rows
    )
    return f'<div class="table-wrap"><table><caption>{escape(caption)}</caption><thead><tr>{columns}</tr></thead><tbody>{body}</tbody></table></div>'


def summary(ciat):
    model, records, _, _ = _snapshot(ciat)
    totals = model["totals"]
    counts = totals["search_metrics"]
    return (
        '<figure class="effort"><div><h3>Search and screening</h3>'
        f"<p><strong>{counts['events']:,} distinct search events</strong> across "
        f"{len(records):,} table-specific search records. The "
        f"{counts['complete_counts']:,} events with complete comparable counts recorded "
        f"{counts['paired_retrieved']:,} retrieval observations, "
        f"{counts['paired_screened']:,} screening assessments and "
        f"{counts['paired_included']:,} selections.</p></div>"
        "<div><h3>Evidence catalogued</h3>"
        f"<p><strong>{totals['known_sources']:,} catalogued sources</strong> and "
        f"<strong>{totals['all_excerpts']:,} saved claims</strong> across the project. "
        "Claims include retained and excluded extracts.</p></div><figcaption>"
        f"{_link('progress.html#definitions', 'Progress definitions')} · "
        f"{_link(SOURCE + '/docs/dashboard_data.json', 'Progress snapshot ' + REVISION[:8])}.</figcaption></figure>"
    )


def _metrics_row(name, metrics):
    searches = metrics["search_metrics"]
    return [
        name,
        _number(metrics["known_sources"]),
        _number(metrics["all_excerpts"]),
        _number(metrics["reviewed_excerpts"]),
        _number(metrics["compiled_outputs"]),
        f"{_number(searches['complete_counts'])} of {_number(searches['events'])}",
    ]


def _scope_tables(model):
    headings = [
        "Scope",
        "Sources",
        "Saved claims",
        "Claims with a review decision",
        "Compiled or configured records",
        "Search events with complete counts",
    ]
    blocks = []
    for code in ("T4", "T2a", "T3", "T6"):
        view = model["table_views"][code]
        rows = [_metrics_row("Whole table", view["totals"])]
        if view.get("project_level"):
            note = "<p>These indicators are shared across practices. Source work is not allocated to individual practices in this snapshot.</p>"
            details = ""
        else:
            note = "<p>Sources and claims can occur in several families. Whole-table and practice totals count each within their own scope.</p>"
            details = []
            for practice in view["practices"]:
                pid = practice["nbs_id"]
                name = (
                    "General reference sources" if pid == "cross" else practice["name"]
                )
                rows.append(_metrics_row(escape(name), practice["metrics"]))
                families = [
                    _metrics_row(escape(f["name"]), f["metrics"])
                    for f in practice.get("families", [])
                ]
                if families:
                    details.append(
                        f"<details><summary>{escape(name)} · family scopes</summary>"
                        + _table(f"{name} · {code}", headings, families)
                        + "</details>"
                    )
            details = "".join(details)
        blocks.append(
            f'<details id="table-{code}"><summary>{TABLE_NAMES[code]}</summary>'
            + note
            + _table(TABLE_NAMES[code], headings, rows)
            + details
            + "</details>"
        )
    return "".join(blocks)


def _scope(record):
    return (
        record["nbs_id"],
        record.get("suitability_family_id") or record.get("family") or "",
        record["table"],
        record["category"],
    )


def _record_title(record):
    return " · ".join(
        [
            record["category"].replace("_", " "),
            record["table"],
            record.get("suitability_family_id") or "whole practice",
            record.get("search_date") or "date unavailable",
        ]
    )


def _record_links(records):
    items = []
    titles = [_record_title(r) for r in records]
    for record, title in zip(records, titles):
        if titles.count(title) > 1:
            title += " · " + record["search_id"]
        items.append(f"<li>{_link(_path(record), title)}</li>")
    return "<ul>" + "".join(items) + "</ul>"


def _ledger(ledger, by_scope):
    groups = defaultdict(list)
    for row in ledger:
        groups[row["nbs_id"]].append(row)
    blocks = []
    for practice, rows in sorted(groups.items()):
        display = []
        for row in rows:
            _, family, table, category = _scope(row)
            matches = by_scope.get(_scope(row), [])
            links = (
                _record_links(matches) if matches else "No search record in this scope"
            )
            display.append(
                [
                    _label(family or "Whole practice"),
                    escape(table),
                    _label(category),
                    *[
                        _label(row.get(stage) or "Not recorded")
                        for stage in ("searched", "screened", "verified")
                    ],
                    links,
                ]
            )
        blocks.append(
            f"<details><summary>{_label(practice)} · {len(rows)} ledger records</summary>"
            + _table(
                "Recorded stages and search records in the same scope",
                [
                    "Family",
                    "Table",
                    "Channel",
                    "Search",
                    "Screening",
                    "Verification",
                    "Search records",
                ],
                display,
            )
            + "</details>"
        )
    return "".join(blocks)


def _detail(record, event):
    fields = [
        ("Practice", "nbs_id"),
        ("Family", "suitability_family_id"),
        ("Table", "table"),
        ("Discovery channel", "category"),
        ("Run ID", "run_id"),
        ("Search date", "search_date"),
        ("Ruleset version", "ruleset_version"),
        ("Search terms", "search_terms"),
        ("Screening steps", "screening_steps"),
        ("Inclusion criteria", "inclusion_criteria"),
        ("Limits", "limits"),
        ("Retrieved observations", "n_retrieved"),
        ("Screening assessments", "n_screened"),
        ("Selections", "n_included"),
    ]
    pairs = []
    for label, key in fields:
        value = record.get(key)
        if value is None or value == "":
            value = (
                "Whole practice" if key == "suitability_family_id" else "Not recorded"
            )
        pairs.append(f"<dt>{label}</dt><dd>{escape(str(value))}</dd>")
    version = record.get("ruleset_version")
    archive = ""
    if version:
        archive_url = f"https://github.com/CIAT/nbs_ruralscan/tree/{REVISION}/.agents/skills/_versions/{version}"
        archive = _link(archive_url, f"Archived ruleset {version}") + " · "
    siblings = [r for r in event["search_ids"] if r != record["search_id"]]
    shared = ""
    if siblings:
        links = [_link(_path({"search_id": r}), r) for r in siblings]
        shared = (
            "<p>Other records sharing this retrieval event: "
            + ", ".join(links)
            + ".</p>"
        )
    return (
        f"<p><code>{escape(record['search_id'])}</code> · Progress edition {REVISION[:8]}</p>"
        f"<dl>{''.join(pairs)}</dl>{shared}<p>"
        + _link("ai.html#ai-system", "Evidence workflow and instructions")
        + " · "
        + archive
        + _link(SOURCE + "/methodology/RULESET_VERSIONS.md", "Version history")
        + " · "
        + _link(
            SOURCE + "/schema/registers/SRCH_search_register.csv",
            "Pinned search register",
        )
        + " · "
        + _link("searches.html", "All search records")
        + " · "
        + _link("progress.html", "Progress")
        + "</p>"
    )


def generate(out, evidence, ciat, write):
    model, records, ledger, version = _snapshot(ciat)
    event_by_id = {
        rid: event for event in model["searches"] for rid in event["search_ids"]
    }
    if set(event_by_id) != {r["search_id"] for r in records} or len(event_by_id) != len(
        records
    ):
        raise ValueError(
            "Search register IDs do not reconcile with the progress snapshot"
        )
    by_practice = defaultdict(list)
    by_scope = defaultdict(list)
    for record in records:
        by_practice[record["nbs_id"]].append(record)
        by_scope[_scope(record)].append(record)
        write(
            _path(record),
            "Evidence",
            _record_title(record),
            _detail(record, event_by_id[record["search_id"]]),
        )
    search_index = "".join(
        f"<details><summary>{_label(practice)} · {len(rows)} records</summary>{_record_links(rows)}</details>"
        for practice, rows in sorted(by_practice.items())
    )
    write(
        "searches.html",
        "Evidence",
        "Recorded searches",
        f"<p>{len(records)} table-specific search records · Progress edition {REVISION[:8]}. "
        + _link("progress.html", "See event counts and stage coverage")
        + " · "
        + _link("ai.html", "Read the evidence workflow")
        + "</p>"
        + search_index,
    )

    metrics = model["totals"]["search_metrics"]
    coverage = _table(
        "Recorded search counts by field",
        ["Count field", "Events reporting this field", "All search events"],
        [
            [
                label,
                _number(metrics["coverage"][field]["recorded"]),
                _number(metrics["coverage"][field]["total"]),
            ]
            for field, label in [
                ("retrieved", "Retrieved"),
                ("screened", "Screened"),
                ("included", "Selected"),
            ]
        ],
    )
    definitions = model["definitions"]
    notes = "".join(
        f"<dt>{title}</dt><dd>{escape(definitions[key])}</dd>"
        for title, key in [
            ("Search events", "searches"),
            ("Sources", "known_sources"),
            ("Recorded review", "reviewed_excerpts"),
            ("Compiled records", "compiled_outputs"),
        ]
    )
    write(
        "progress.html",
        "Progress",
        "Research effort and outputs",
        summary(ciat)
        + coverage
        + "<p>"
        + _link("searches.html", "Browse recorded searches")
        + "</p>"
        + "<h2>Evidence and outputs by table</h2>"
        + _scope_tables(model)
        + "<h2>Recorded stages by practice</h2><p>Stages come from the pipeline ledger. "
        "The linked search records share the practice, family, table and discovery channel. "
        "An unrecorded stage has no measured completion percentage.</p>"
        + _ledger(ledger, by_scope)
        + f'<h2 id="definitions">Count definitions</h2><p>Progress snapshot {REVISION[:8]} '
        f"· definition version {escape(str(version))}.</p><dl>{notes}</dl>",
    )
