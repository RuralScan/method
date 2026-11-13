"""Read-only finding, rating and mapping review views for a pinned cookbook."""

from collections import defaultdict
from urllib.parse import urlencode

import recipes

ROOSE = "ev_flood_hazard_roose17_2"
IEG = "ev_drought_hazard_ieg20_4"
TABLES = {
    "T3": "Hazard ratings",
    "T4": "Suitability mappings",
    "T6": "Scorecard ratings",
}
EXAMPLES = {
    "T3": (
        "water_harvesting_conservation__flood__all",
        "Water harvesting and flood mitigation",
    ),
    "T4": (recipes.TERRACE, "Bench terraces and annual rainfall"),
    "T6": (
        "water_harvesting_conservation__flood_hazard",
        "Water harvesting and the flood scorecard",
    ),
}
STATUS = {
    "unreviewed": "Unreviewed",
    "signed_off": "Signed off",
    "held": "Held (counts, unresolved)",
    "rejected": "Rejected (excluded)",
}
CIAT = "https://github.com/CIAT/nbs_ruralscan"
LIVE = "https://ciat.github.io/nbs_ruralscan/"
FINDING_LOG = "pipeline/metrics/review_log.csv"
RATING_LOG = "pipeline/metrics/row_review_log.csv"
METHOD_LOG = "methodology/decisions/open_decisions.csv"


def _table_url(table, practice=None):
    suffix = f"-{practice}" if practice else ""
    return f"review-{table.lower()}{suffix}.html"


def _finding_link(identifier, label=None):
    return recipes.link(
        recipes.claim_file({"id": identifier}) + "#review-details", label or identifier
    )


def _row_link(row, label=None):
    return recipes.link(
        recipes.row_file(row) + "#review-details", label or recipes.record_name(row)
    )


def _log(revision, path, line=None):
    anchor = f"#L{line}" if line else ""
    return f"{CIAT}/blob/{revision}/{path}{anchor}"


def _historical_id(eid, entry, sidecar):
    parts = [
        f"<code>{recipes.esc(eid)}</code>",
        _link_event(entry["latest_event"], sidecar, FINDING_LOG),
    ]
    if entry["disposition"] == "renamed":
        parts.extend(
            [
                _finding_link(entry["current_evidence_id"], "Open renamed finding"),
                recipes.link(f"{CIAT}/commit/{entry['rename_commit']}", "ID change"),
            ]
        )
    elif entry.get("deferred_register"):
        parts.append(
            recipes.link(
                _log(sidecar["producer_revision"], entry["deferred_register"]),
                "Open deferred register",
            )
        )
    else:
        parts.append("Current finding ID unverified")
    return " · ".join(parts)


def _link_event(event, sidecar, path):
    parts = [
        recipes.esc(str(event.get("date") or "Date unrecorded")),
        recipes.esc(recipes.words(event["decision"])),
    ]
    if event.get("reason"):
        parts.append(recipes.esc(recipes.words(event["reason"])))
    if event.get("historical_evidence_id"):
        parts.append("Logged under " + recipes.esc(event["historical_evidence_id"]))
    parts.append(
        {
            "automated": "Automated update",
            "human": "Human review",
            "unverified": "Reviewer unverified",
        }[event["actor_kind"]]
    )
    parts.append(
        recipes.link(
            _log(sidecar["producer_revision"], path, event.get("line")),
            "Applied log record",
        )
    )
    if event.get("commit"):
        parts.append(
            recipes.link(f"{CIAT}/commit/{event['commit']}", "Application commit")
        )
    return " · ".join(parts)


def _live(identifier, finding):
    if finding.get("live_batch"):
        query = urlencode({"batch": finding["live_batch"], "unit": identifier})
        return recipes.link(
            LIVE + "review.html?" + query,
            "Open this finding in the live CIAT review batch",
        )
    if finding["live_queue_available"]:
        return recipes.link(
            LIVE + "dashboard.html#review-evidence=" + identifier,
            "Open this finding in the live CIAT evidence queue",
        )
    return "No matching live CIAT review card verified for this finding."


def finding_details(claim, sidecar):
    identifier = claim["id"]
    record = sidecar["findings"][identifier]
    status = STATUS[record["status"]]
    event = record.get("latest_event")
    applied = "No applied finding decision recorded."
    if event:
        applied = "Latest log entry · " + _link_event(event, sidecar, FINDING_LOG)
    disposition = record["status_event"]
    if disposition and disposition != event:
        applied += "</p><p>Decision behind this status · " + _link_event(
            disposition, sidecar, FINDING_LOG
        )
    pin = sidecar["producer_revision"]
    source = claim.get("url") or _log(pin, "schema/registers/EV_evidence_register.csv")
    body = (
        '<section id="review-details"><h2>Finding review</h2>'
        f"<p><strong>{status}</strong> · Evidence edition <code>{recipes.esc(pin[:8])}</code></p>"
        f"<p>{applied}</p><p>{_live(identifier, record)}</p><p>"
        + recipes.link(source, "Evidence register at this edition")
        + "</p>"
    )
    if (
        record["status"] == "unreviewed"
        and event
        and event["actor_kind"] == "automated"
    ):
        body += "<p>This automated entry supplies no human sign-off.</p>"
    if record.get("reconciliation_required"):
        body += "<p>The register and review history need reconciliation in CIAT.</p>"
    if record["excluded"]:
        body += "<p>This finding is retained in the evidence register and excluded from active synthesis.</p>"
    if identifier in sidecar["history"]:
        body += (
            "<p>"
            + recipes.link(
                "review-applied.html",
                "Compare the applied decision and subsequent editions",
            )
            + "</p>"
        )
    return (
        body
        + "<p>"
        + recipes.link("#main", "Return to the finding")
        + " · "
        + recipes.link("review.html", "Review overview")
        + "</p></section>"
    )


def _coverage(record, sidecar):
    coverage = record["coverage"]
    if coverage == "unavailable":
        return "<p><strong>Rating-setter coverage unavailable</strong> for this row in this edition.</p>"
    ids = record["setter_ids"]
    findings = sidecar["findings"]
    unresolved = [
        eid for eid in ids if findings[eid]["status"] in {"held", "unreviewed"}
    ]
    if record["provisional"]:
        unit = "finding" if len(unresolved) == 1 else "findings"
        message = f"<strong>Provisional</strong> · {len(unresolved)} rating-setting {unit} awaiting review."
    elif coverage == "partial":
        message = "Only part of this row’s evidence has been tested for its influence on the rating."
    else:
        message = "The rating-setter assessment is complete for this row."
    coverage_label = "Partial" if coverage == "partial" else "Assessed"
    tested_count = record.get("tested_count", len(record.get("tested_ids", [])))
    body = f"<p>{message}</p><p>{coverage_label} coverage · {tested_count:,} findings tested for their influence on this row · {len(ids)} confirmed rating-setting findings.</p>"
    if ids:
        counts = record["status_counts"]
        body += (
            "<p>Confirmed setters by finding status · "
            + " · ".join(f"{label}: {counts[state]}" for state, label in STATUS.items())
            + ".</p>"
        )
        body += recipes.listing(
            _finding_link(eid)
            + " · "
            + STATUS[findings[eid]["status"]]
            + (
                " · Indirect influence through synthesis"
                if eid not in record["evidence_ids"]
                else " · Direct citation"
            )
            for eid in ids
        )
    return body


def row_details(row, sidecar):
    table = row["table"]
    if table not in TABLES:
        return ""
    pin = sidecar["producer_revision"]
    body = f'<section id="review-details"><h2>Review details</h2><p>Evidence edition <code>{recipes.esc(pin[:8])}</code></p>'
    if table == "T4":
        fields = row["fields"]
        body += "<h3>Mapping calibration and function</h3>" + recipes.entries(
            [
                (key, fields[key])
                for key in (
                    "Reviewed numerical calibration",
                    "Function options",
                    "Function selected",
                    "Spatially validated",
                )
            ]
        )
        if row["id"] == recipes.TERRACE:
            body += "<p>The rainfall observation documents use of forward-sloping benches. The calibration hold leaves the numerical score unassigned.</p>"
    else:
        record = sidecar["rows"][row["id"]]
        body += "<h3>Compiled rating</h3>" + recipes.entries(
            [("Rating", record["rating"]), ("Confidence", record["confidence"])]
        )
        body += _coverage(record, sidecar)
        replay = sidecar["setter_assessment"]
        result = replay["results"].get(row["id"])
        if result:
            value = result["without"]
            outcome = " / ".join(value) if value else "No compiled row"
            body += (
                "<p>Replaying this edition without "
                + _finding_link(replay["finding_id"])
                + " produced <strong>"
                + recipes.esc(outcome)
                + "</strong>.</p>"
            )
        body += "<h3>Reviews of the compiled rating</h3>"
        reviews = record["rating_reviews"]
        if reviews:
            items = []
            for event in reviews:
                text = _link_event(event, sidecar, RATING_LOG)
                reviewed = [event.get("rating"), event.get("confidence")]
                if all(reviewed):
                    text += " · Reviewed value " + recipes.esc(" / ".join(reviewed))
                revision = event.get("row_revision")
                if revision:
                    text += " · " + recipes.link(
                        f"{CIAT}/tree/{revision}", f"Reviewed version {revision[:8]}"
                    )
                else:
                    text += " · Exact row version reviewed was unrecorded."
                items.append(text)
            body += recipes.listing(items)
        else:
            body += "<p>No applied rating review recorded for this row.</p>"
    ids = row["evidence_ids"]
    body += f"<details><summary>Direct findings and their review status ({len(ids)})</summary>"
    body += (
        recipes.listing(
            _finding_link(eid) + " · " + STATUS[sidecar["findings"][eid]["status"]]
            for eid in ids
        )
        if ids
        else "<p>No direct findings cited in this edition.</p>"
    )
    body += "</details>"
    if any(h["headline_id"] == row["id"] for h in sidecar["history"].values()):
        body += (
            "<p>"
            + recipes.link(
                "review-applied.html",
                "Compare the drought rating before and after the finding decision",
            )
            + "</p>"
        )
    return (
        body
        + "<p>"
        + recipes.link("#main", "Return to the compiled record")
        + " · "
        + recipes.link(
            _table_url(table, row["practice"]),
            "Review this practice’s " + TABLES[table].lower(),
        )
        + " · "
        + recipes.link("method-decisions.html", "Synthesis method decisions")
        + "</p></section>"
    )


def _history(history, rows, sidecar):
    name = history["headline_id"]
    lines = []
    for data_key, revision_key, citations_key, label in [
        (
            "before",
            "before_revision",
            "citations_before",
            "Before the applied decision",
        ),
        ("after", "applied_revision", "citations_after", "After the applied decision"),
        ("edition", "edition_revision", "citations_in_edition", "Dashboard edition"),
    ]:
        result, revision = history[data_key], history[revision_key]
        lines.append(
            '<tr><th scope="row">'
            + label
            + "</th><td>"
            + recipes.link(f"{CIAT}/tree/{revision}", revision[:8])
            + "</td><td>"
            + str(len(history[citations_key]))
            + "</td><td>"
            + recipes.esc(result["rating"])
            + "</td><td>"
            + recipes.esc(result["confidence"])
            + "</td><td>"
            + str(len(result["evidence_ids"]))
            + "</td></tr>"
        )
    earlier = history["citations_before"]
    return (
        "<p>The IEG Ethiopia programme finding was excluded for wrong practice. Several findings were removed in the same compilation.</p>"
        + "<p>"
        + _finding_link(IEG, "Open the excluded finding and its applied decision")
        + "</p>"
        + '<div class="table-wrap"><table><caption>Agroforestry drought rating and direct evidence</caption>'
        "<thead><tr><th>Comparison</th><th>Revision</th><th>Rows citing the IEG finding</th>"
        "<th>Headline rating</th><th>Confidence</th><th>Findings in the headline row</th></tr></thead><tbody>"
        + "".join(lines)
        + "</tbody></table></div><p>At the applied revision: <strong>"
        + recipes.esc(history["result"])
        + "</strong>. Attribution for the subsequent rating change is unverified.</p>"
        + "<h2>Applied finding decisions</h2>"
        + recipes.listing(
            _link_event(event, sidecar, FINDING_LOG)
            for event in history["finding_events"]
        )
        + "<details><summary>Rows that previously cited the excluded finding</summary>"
        + recipes.listing(
            _row_link(rows[rid], rid) if rid in rows else recipes.esc(rid)
            for rid in earlier
        )
        + "</details><p>"
        + _row_link(
            rows[name], "Open the edition’s drought rating and row review history"
        )
        + "</p>"
    )


def generate(pub, sidecar, write):
    if (pub["source_revision"], pub["release_id"]) != (
        sidecar["producer_revision"],
        sidecar["release_id"],
    ):
        raise ValueError("Review data and workbook must share one producer and release")
    grouped = defaultdict(list)
    rows = {row["id"]: row for row in pub["rows"]}
    for row in rows.values():
        if row["table"] in TABLES:
            grouped[row["table"], row["practice"]].append(row)
    practices = sorted({r["practice"] for r in rows.values()})
    paths = []
    for table, label in TABLES.items():
        subsets = []
        for practice in practices:
            subset = grouped[table, practice]
            name = recipes.practice_name(practice)
            path = _table_url(table, practice)
            subsets.append(recipes.link(path, f"{name} ({len(subset)})"))
            links = []
            for row in subset:
                item = _row_link(row)
                if table == "T4":
                    item += " · Calibration: " + recipes.esc(
                        row["fields"]["Reviewed numerical calibration"]
                    )
                else:
                    record = sidecar["rows"][row["id"]]
                    item += (
                        " · "
                        + recipes.esc(record["rating"])
                        + " / "
                        + recipes.esc(record["confidence"])
                    )
                    if record["provisional"]:
                        item += " · <strong>Provisional</strong>"
                    elif record["coverage"] == "unavailable":
                        item += " · Rating-setter coverage unavailable"
                links.append(item)
            listing = (
                recipes.listing(links)
                if links
                else "<p>No compiled rows in this scope and edition.</p>"
            )
            write(
                path,
                "Review",
                f"{name} · {label}",
                listing
                + "<p>"
                + recipes.link(_table_url(table), "All practices")
                + " · "
                + recipes.link(recipes.recipe_file(practice), "Open practice recipe")
                + "</p>",
            )
        example_id, example_title = EXAMPLES[table]
        example = _row_link(rows[example_id], example_title)
        eid = recipes.WOCAT if table == "T4" else ROOSE
        if eid not in rows[example_id]["evidence_ids"]:
            raise ValueError(f"Review example {example_id} no longer cites {eid}")
        example_finding = _finding_link(
            eid,
            "Inspect the WOCAT finding"
            if table == "T4"
            else "Inspect the Roose finding",
        )
        write(
            _table_url(table),
            "Review",
            label,
            "<p>Worked example · "
            + example
            + " · "
            + example_finding
            + "</p><h2>Choose a practice</h2>"
            + recipes.listing(subsets),
        )
        paths.append(recipes.link(_table_url(table), table + " · " + label))
    excluded = sorted(eid for eid, f in sidecar["findings"].items() if f["excluded"])
    active_ids = {claim["id"] for claim in pub["claims"]}
    sources = {source["id"] for source in pub["sources"]}
    for eid in excluded:
        if eid in active_ids:
            raise ValueError(f"Excluded finding still active in workbook: {eid}")
        record = sidecar["findings"][eid]
        body = (
            "<p><code>"
            + recipes.esc(eid)
            + "</code></p>"
            + recipes.entries([("Source ID", record["source_id"])])
        )
        if record["source_id"] in sources:
            body += (
                "<p>"
                + recipes.link(
                    recipes.source_file({"id": record["source_id"]}),
                    "Open the source record",
                )
                + "</p>"
            )
        body += finding_details({"id": eid}, sidecar)
        body += (
            "<p>"
            + recipes.link("review-history.html", "Return to excluded findings")
            + "</p>"
        )
        write(recipes.claim_file({"id": eid}), "Review", "Excluded finding", body)
    exclusions_by_reason = defaultdict(list)
    for eid in excluded:
        event = sidecar["findings"][eid]["status_event"] or {}
        reason = (
            recipes.words(event.get("reason"))
            if event.get("decision") == "drop"
            else ""
        )
        exclusions_by_reason[reason or "Reason unavailable"].append(eid)
    groups = "".join(
        "<details><summary>"
        + recipes.esc(reason.capitalize())
        + f" ({len(members):,})</summary>"
        + recipes.listing(_finding_link(eid) for eid in members)
        + "</details>"
        for reason, members in sorted(exclusions_by_reason.items())
    )
    write(
        "review-history.html",
        "Review",
        "Excluded findings",
        f"<p>{len(excluded):,} findings retained for audit in this edition. "
        + recipes.link(
            "review-applied.html", "Trace the applied agroforestry drought decision"
        )
        + ".</p><p>"
        + recipes.link(
            "evidence.html#find",
            "Search findings by evidence ID, source or exclusion reason",
        )
        + "</p><h2>Browse by recorded exclusion reason</h2>"
        + groups
        + "<h2>Historical finding IDs outside this edition’s register</h2>"
        + "<p>Follow each log entry to its renamed finding or deferred register where available.</p>"
        + recipes.listing(
            _historical_id(eid, entry, sidecar)
            for eid, entry in sidecar["unmatched_finding_reviews"].items()
        ),
    )
    write(
        "review-applied.html",
        "Review",
        "An applied agroforestry drought decision",
        _history(sidecar["history"][IEG], rows, sidecar),
    )
    method_notes = []
    for decision in sidecar["method_decisions"]:
        title = decision["decision_id"]
        info = [
            recipes.link(
                _log(sidecar["producer_revision"], METHOD_LOG, decision.get("line")),
                title,
            )
        ]
        for key in ("date", "decided"):
            if decision.get(key):
                info.append(recipes.esc(decision[key]))
        if decision.get("implementation_commit"):
            info.append(
                recipes.link(
                    f"{CIAT}/commit/{decision['implementation_commit']}",
                    "Implementation commit",
                )
            )
        method_notes.append(" · ".join(info))
    write(
        "method-decisions.html",
        "Review",
        "Synthesis method decisions",
        "<p>These project decisions include rules for combining evidence across rows. Each entry opens the decision register at the edition’s producer revision.</p>"
        + "<p>The register supplies the date and decision code. When an implementing revision is unverified, the entry links to its recorded decision.</p>"
        + recipes.listing(method_notes),
    )
    write(
        "review.html",
        "Review",
        "Review evidence and recipe decisions",
        f"<p>Cookbook edition <code>{recipes.esc(pub['release_id'][:8])}</code> · evidence revision "
        f"<code>{recipes.esc(pub['source_revision'][:8])}</code>. Inspect the applied decision for a finding, "
        "the review history of a rating, or the calibration of a suitability mapping. Available CIAT cards open the live review workspace.</p>"
        + '<h2>Choose a table</h2><nav class="tiles" aria-label="Review tables">'
        + "".join(paths)
        + "</nav>"
        + f"<p>Live batch and queue links use CIAT <code>{recipes.esc(sidecar['live_navigation_revision'][:8])}</code>. Human reviewers record decisions in CIAT. An automated check alone cannot sign off a finding.</p>"
        + "<p>"
        + recipes.link("review-status.json", "Download edition review records (JSON)")
        + " · "
        + recipes.link("review-status-manifest.json", "Verify edition and file digests")
        + "</p>"
        + "<h2>History and method</h2>"
        + recipes.listing(
            [
                recipes.link(
                    "review-applied.html",
                    "Trace a finding exclusion through three versions of an agroforestry rating",
                ),
                recipes.link("review-history.html", "Browse excluded findings"),
                recipes.link(
                    "method-decisions.html", "Read synthesis method decisions"
                ),
                recipes.link("ai.html", "How findings enter review"),
            ]
        ),
    )
