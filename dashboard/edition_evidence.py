"""Publish public analytical tables, evidence joins and review coverage at one edition."""

import json
from collections import Counter, defaultdict
from html import escape

import recipes
import review
from packages import RIGHTS, SITE, catalog_entry, field, save, table

# Only fields already shared in the edition's evidence cards may enter the projection.
STUDY_CONTEXT = ("study_country", "study_area", "farming_system", "aez")
TABLES = ("T3", "T4", "T6")
RECORD = field(
    "record_id", "CIAT analytical row ID. For T4 this is the native mapping_id."
)
EVIDENCE = field("evidence_id", "CIAT evidence register ID.")
SOURCE = field("source_id", "CIAT source register ID.")
PRACTICE = field("practice", "Practice ID in the pinned recipe.")
STATUSES = ("unreviewed", "held", "signed_off", "rejected")
RECORD_JOIN = [("record_id", "records")]


def optional(name, description, kind="string"):
    return field(
        name,
        description + " Blank means unreported or inapplicable.",
        kind,
        required=False,
    )


def projection(data, keys):
    subset = {k: data[k] for k in keys if data.get(k) is not None and data[k] != ""}
    return (
        json.dumps(subset, ensure_ascii=False, separators=(",", ":"))
        if subset
        else None
    )


def public_parameters(parameters):
    values = {k: parameters[k] for k in recipes.PARAMETER_FIELDS if k in parameters}
    profiles = []
    for profile in parameters.get("profiles", []):
        item = {
            k: profile[k]
            for k in ("profile_id", "applicability_note", "unit", "score_policy")
            if k in profile
        }
        item["intervals"] = [
            {
                k: band[k]
                for k in (
                    "label",
                    "lower",
                    "upper",
                    "lower_inclusive",
                    "upper_inclusive",
                    "score",
                    "score_basis",
                )
                if k in band
            }
            for band in profile.get("intervals", [])
        ]
        profiles.append(item)
    if profiles:
        values["profiles"] = profiles
    return (
        json.dumps(values, ensure_ascii=False, separators=(",", ":"))
        if values
        else None
    )


def generate(out, pub, native_rows, evidence, status, evidence_revision, write):

    directory = out / "evidence-tables"
    directory.mkdir(exist_ok=True)
    base = SITE + "editions/" + out.name + "/"
    rows = [r for r in pub["rows"] if r["table"] in TABLES]
    findings = status["findings"]
    if evidence.keys() != findings.keys():
        raise ValueError("Pinned EV register and review status IDs differ")
    resources = []

    def publish(name, title, fields, records, **kwargs):
        resources.append(table(directory, name, title, fields, records, **kwargs))

    publish(
        "sources",
        "Sources",
        [
            SOURCE,
            field("citation", "Bibliographic citation in this edition."),
            field("kind", "Document type."),
            optional("publication_url", "Publication or publisher URL."),
            field("register_url", "Pinned source register entry."),
        ],
        (
            {
                "source_id": s["id"],
                "citation": s["citation"],
                "kind": s["kind"],
                "publication_url": s["publication_url"] or s["publisher_url"],
                "register_url": s["url"],
            }
            for s in pub["sources"]
        ),
    )

    finding_rows = []
    for eid, f in sorted(findings.items()):
        ev = evidence[eid]
        if f["source_id"] != ev["source_id"]:
            raise ValueError(f"Finding and status source differ for {eid}")
        finding_rows.append(
            {
                "evidence_id": eid,
                "source_id": ev["source_id"],
                "practice": ev["nbs_id"],
                "family": ev["suitability_family_id"],
                "variable": ev["variable"],
                "use_role": ev["use_role"],
                "claim_scope": ev["claim_scope"],
                "basis": ev["claim_basis"],
                "extraction_confidence": ev["extraction_confidence"],
                "page": ev.get("page"),
                "locator_type": ev["locator_type"],
                "locator": ev.get("locator"),
                "reported": projection(
                    ev.get("relationship") or {}, recipes.REPORTED_FIELDS
                )
                if not f["excluded"]
                else None,
                "study_context": projection(ev.get("context") or {}, STUDY_CONTEXT)
                if not f["excluded"]
                else None,
                "status": f["status"],
                "excluded": f["excluded"],
                "reconciliation_required": f["reconciliation_required"],
                "live_review_url": review.live_url(eid, f),
            }
        )
    publish(
        "findings",
        "Findings and applied human review status",
        [
            EVIDENCE,
            SOURCE,
            PRACTICE,
            field("family", "Suitability family ID."),
            field("variable", "Registered variable or outcome."),
            field("use_role", "Analytical use of this finding."),
            field("claim_scope", "Scope of the extracted claim."),
            field("basis", "Registered basis of the claim."),
            field("extraction_confidence", "Confidence assigned at extraction."),
            optional("page", "One-based page in source document.", "integer"),
            field("locator_type", "Type of source locator."),
            optional(
                "locator",
                "Source section, anchor, line or other locator. Use page when present.",
            ),
            field(
                "reported",
                "Public extracted values, with source-specific units in unit when recorded. Blank for excluded or unreported findings. Keys: "
                + ", ".join(recipes.REPORTED_FIELDS),
                "object",
                required=False,
            ),
            field(
                "study_context",
                "Reported study context. Blank for excluded or unreported findings. Keys: "
                + ", ".join(STUDY_CONTEXT),
                "object",
                required=False,
            ),
            field(
                "status",
                "Applied human status at edition pin. Held counts unresolved. Rejected is excluded.",
                choices=list(STATUSES),
            ),
            field("excluded", "Excluded from synthesis at the edition pin.", "boolean"),
            field(
                "reconciliation_required",
                "Effective review state and historical events need reconciliation.",
                "boolean",
            ),
            optional(
                "live_review_url",
                "Verified CIAT navigation route at the separate navigation revision.",
            ),
        ],
        finding_rows,
        joins=[("source_id", "sources")],
    )

    publish(
        "records",
        "Index of T3, T4 and T6 rows",
        [
            RECORD,
            field("table", "Analytical table.", choices=list(TABLES)),
            PRACTICE,
            optional(
                "family",
                "Family ID. Practice-wide applicability is given in the row's scope.",
            ),
            field("subject", "Hazard, suitability variable or scorecard indicator."),
            field("record_url", "Pinned native analytical row."),
        ],
        (
            {
                "record_id": r["id"],
                "table": r["table"],
                "practice": r["practice"],
                "family": r["family"],
                "subject": r["subject"],
                "record_url": r["url"],
            }
            for r in rows
        ),
    )

    links, source_links = [], []
    detail_rows = defaultdict(list)
    setter_rows = defaultdict(list)
    held_mappings = []
    for r in rows:
        rid, lane, fields = r["id"], r["table"], r["fields"]
        support = {"direct": r["evidence_ids"], "context": r["context_ids"]}
        source_links.extend(
            {"record_id": rid, "source_id": sid} for sid in r["context_source_ids"]
        )
        if lane == "T4":
            native = native_rows[rid]
            detail = {
                "function_role": fields["Function role"],
                "function_options": int(fields["Function options"]),
                "function_selected": fields["Function selected"] == "Yes",
                "spatially_validated": fields["Spatially validated"] == "Yes",
                "calibration": fields["Reviewed numerical calibration"],
                "relationship_type": native.get("relationship_type"),
                "dataset_id": native.get("dataset_id"),
                "dimension": native.get("suitability_dimension"),
            }
            params = native.get("relationship_params") or {}
            calibration = params.get("reviewed_adaptation", {}).get(
                "numerical_calibration", {}
            )
            detail["parameters"] = public_parameters(params)
            detail["calibration_reason"] = calibration.get("reason")
            if detail["calibration"] == "Held":
                held_mappings.append(r)
        else:
            state = status["rows"][rid]
            support["setter"] = state["setter_ids"]
            detail = {
                "rating": state["rating"],
                "confidence": state["confidence"],
                "scope": fields["Scope"],
                "setter_coverage": state["coverage"],
                "provisional": state["provisional"],
            }
            if lane == "T3":
                detail.update(
                    risk_role=fields["Risk role"],
                    farming_system=fields["Farming system"],
                )
            for eid in state["unresolved_setter_ids"]:
                setter_rows[eid].append(r)
        detail_rows[lane].append({"record_id": rid, **detail})
        for kind, ids in support.items():
            for eid in ids:
                if eid not in findings or (
                    kind in ("direct", "setter") and findings[eid]["excluded"]
                ):
                    raise ValueError(f"Invalid {kind} finding {eid} on {rid}")
                links.append({"record_id": rid, "evidence_id": eid, "kind": kind})

    ratings = [
        RECORD,
        field(
            "rating",
            "Compiled value. Blank means the producer did not assign a rating.",
            required=False,
        ),
        field("confidence", "Compiled confidence."),
        field("scope", "Practice or family scope of the row."),
        field(
            "setter_coverage",
            "Extent of historical assessment of findings that can change the rating.",
            choices=["assessed", "partial", "unavailable"],
        ),
        field(
            "provisional",
            "True when a confirmed setter is unresolved. False when fully assessed with no unresolved setter. Blank means undetermined.",
            "boolean",
            required=False,
        ),
    ]
    publish(
        "t3",
        "T3 hazard ratings",
        ratings
        + [
            field("risk_role", "Livelihood mitigation or threat to investment."),
            field("farming_system", "Farming system scope."),
        ],
        detail_rows["T3"],
        joins=RECORD_JOIN,
    )
    publish(
        "t4",
        "T4 suitability mappings",
        [
            RECORD,
            field(
                "function_role",
                "Suitability score, gate, hard exclusion or operational scenario.",
            ),
            field("function_options", "Number of candidate functions.", "integer"),
            field(
                "function_selected", "Producer recorded a selected function.", "boolean"
            ),
            field(
                "spatially_validated",
                "Producer recorded spatial validation.",
                "boolean",
            ),
            field("calibration", "Reviewed numerical calibration disposition."),
            optional("relationship_type", "Native relationship type."),
            optional("dataset_id", "Input dataset ID."),
            optional("dimension", "Suitability dimension."),
            optional(
                "parameters",
                "Public relationship parameters and source profiles. Profile intervals carry their own units and boundaries.",
                "object",
            ),
            optional(
                "calibration_reason", "Recorded rationale for the calibration decision."
            ),
        ],
        detail_rows["T4"],
        joins=RECORD_JOIN,
    )
    publish("t6", "T6 scorecard ratings", ratings, detail_rows["T6"], joins=RECORD_JOIN)
    publish(
        "record-findings",
        "Row-to-finding joins",
        [
            RECORD,
            EVIDENCE,
            field(
                "kind",
                "Direct citation, contextual evidence, or confirmed rating setter. A setter may act indirectly.",
                choices=["direct", "context", "setter"],
            ),
        ],
        links,
        primary=["record_id", "evidence_id", "kind"],
        joins=[*RECORD_JOIN, ("evidence_id", "findings")],
    )
    publish(
        "context-sources",
        "Contextual source references",
        [RECORD, SOURCE],
        source_links,
        primary=["record_id", "source_id"],
        joins=[*RECORD_JOIN, ("source_id", "sources")],
    )

    publish(
        "queue",
        "Unresolved finding and T4 calibration review tasks",
        [
            field(
                "target_id",
                "Finding ID for an unresolved setter or mapping ID for a held calibration.",
            ),
            field(
                "task",
                "Published reason for review.",
                choices=["unresolved_setter", "held_calibration"],
            ),
            field(
                "status",
                "Finding disposition or T4 calibration status at the edition pin.",
            ),
            optional("evidence_id", "Finding target for an unresolved setter."),
            optional("record_id", "Mapping target for a held calibration."),
            field("read_url", "Edition page with finding history or mapping decision."),
            optional(
                "live_review_url",
                "Verified CIAT finding card. A calibration hold opens its mapping decision.",
            ),
        ],
        [
            {
                "target_id": eid,
                "task": "unresolved_setter",
                "status": findings[eid]["status"],
                "evidence_id": eid,
                "record_id": None,
                "read_url": base + recipes.claim_file({"id": eid}) + "#review-details",
                "live_review_url": review.live_url(eid, findings[eid]),
            }
            for eid in sorted(setter_rows)
        ]
        + [
            {
                "target_id": r["id"],
                "task": "held_calibration",
                "status": "held",
                "evidence_id": None,
                "record_id": r["id"],
                "read_url": base + recipes.row_file(r) + "#review-details",
                "live_review_url": None,
            }
            for r in held_mappings
        ],
        primary=["task", "target_id"],
        joins=[*RECORD_JOIN, ("evidence_id", "findings")],
    )
    coverage = []

    def count(group, unit, population, members, statuses):
        counts = Counter(members)
        for label in statuses:
            coverage.append(
                {
                    "group": group,
                    "unit": unit,
                    "population": population,
                    "status": label,
                    "count": counts[label],
                    "denominator": sum(counts.values()),
                }
            )

    count(
        "EV",
        "findings",
        "All registered findings",
        (f["status"] for f in findings.values()),
        STATUSES,
    )
    for lane in ("T3", "T6"):
        detail = detail_rows[lane]
        count(
            lane,
            "rows",
            "Setter assessment",
            (r["setter_coverage"] for r in detail),
            ["assessed", "partial", "unavailable"],
        )
        count(
            lane,
            "rows",
            "Rating status",
            (
                "undetermined"
                if r["provisional"] is None
                else "provisional"
                if r["provisional"]
                else "assessed_clear"
                for r in detail
            ),
            ["provisional", "assessed_clear", "undetermined"],
        )
    count(
        "T4",
        "mappings",
        "Numerical calibration",
        (r["calibration"] for r in detail_rows["T4"]),
        sorted({r["calibration"] for r in detail_rows["T4"]}),
    )
    publish(
        "coverage",
        "Review coverage by edition",
        [
            field("group", "Register or analytical table."),
            field("unit", "Counting unit."),
            field("population", "Partition within the group."),
            field(
                "status",
                "Bucket in this partition. assessed_clear means no confirmed unresolved setter after full assessment.",
            ),
            field("count", "Members in this bucket.", "integer"),
            field(
                "denominator", "Total distinct members of this population.", "integer"
            ),
        ],
        coverage,
        primary=["group", "population", "status"],
    )

    title = "RuralScan evidence tables and edition review coverage"
    package = {
        "name": "ruralscan-edition-evidence",
        "profile": "tabular-data-package",
        "id": base + "evidence-tables/datapackage.json",
        "version": out.name,
        "schemaVersion": "1.0.0",
        "title": title,
        "description": "All candidate T3, T4 and T6 records in this edition, their findings, sources, review status and coverage. Geography on a finding describes the study. T6E economic profiles have a separate analytical purpose.",
        "homepage": base + "review-coverage.html",
        "keywords": [
            "nature-based solutions",
            "evidence synthesis",
            "review",
            "hazard",
            "suitability",
            "scorecard",
        ],
        "citation": f"RuralScan. {title}. Edition {out.name}. {base}evidence-tables/datapackage.json",
        "accessRights": RIGHTS,
        "contact": "https://github.com/RuralScan/evidence/issues",
        "producerRevision": pub["source_revision"],
        "evidenceRevision": evidence_revision,
        "cookbookRelease": pub["release_id"],
        "liveNavigationRevision": status["live_navigation_revision"],
        "sources": [
            {"title": "Public candidate workbook", "path": base + "workbook.html"},
            {
                "title": "Applied finding, rating and method decisions",
                "path": base + "review-status.json",
            },
            {
                "title": "Checksums and pins",
                "path": base + "review-status-manifest.json",
            },
        ],
        "resources": resources,
    }
    save(directory / "datapackage.json", package)
    publish_views(
        write,
        coverage,
        setter_rows,
        held_mappings,
        findings,
        resources,
        pub["source_revision"],
        {c["id"]: c for c in pub["claims"]},
    )
    return catalog_entry(directory, package)


def publish_views(
    write, coverage, setters, held, findings, resources, revision, claims
):
    by_practice = defaultdict(dict)
    for eid, rows in setters.items():
        for row in rows:
            by_practice[row["practice"]].setdefault(eid, []).append(row)

    queue = [
        review.reviewer_actions(),
        f"<p>Evidence revision <code>{escape(revision[:8])}</code>. Start with a finding that can change a published hazard or scorecard rating, or inspect a held suitability mapping.</p>",
        (
            f'<p><a href="#setters">Unresolved rating-setting findings ({len(setters)})</a> · '
            f'<a href="#calibrations">Held T4 calibrations ({len(held)})</a> · '
            '<a href="evidence-tables/queue.csv">Download queue (CSV)</a> · <a href="review-coverage.html">Edition coverage and downloads</a></p>'
        ),
        '<h2 id="setters">Findings that set provisional T3 or T6 ratings</h2>',
        (
            "<p>Each finding appears once per affected practice. Open an affected rating to check its evidence, then use the CIAT card to record a vote. Held findings continue to count. "
            "A rating with incomplete or unavailable setter assessment can have additional unresolved findings.</p>"
        ),
    ]
    for practice, entries in sorted(by_practice.items()):
        items = []
        for eid, affected in sorted(
            entries.items(), key=lambda item: (-len(item[1]), item[0])
        ):
            links = [
                review._row_link(r, f"{r['table']} · {recipes.record_name(r)}")
                for r in affected
            ]
            items.append(
                "<li>"
                + review._finding_link(
                    eid,
                    recipes.claim_name(claims[eid])
                    + " · "
                    + recipes.locator(claims[eid]),
                )
                + " · <code>"
                + escape(eid)
                + "</code>"
                + " · "
                + review.STATUS[findings[eid]["status"]]
                + " · "
                + review._live(eid, findings[eid])
                + f"<details><summary>Affected ratings ({len(links)})</summary>"
                + recipes.listing(links)
                + "</details></li>"
            )
        queue.append(
            f"<details><summary>{escape(recipes.practice_name(practice))} ({len(entries)})</summary><ul>{''.join(items)}</ul></details>"
        )
    queue += [
        '<h2 id="calibrations">T4 mappings with numerical calibration held</h2>',
        "<p>Open the mapping to read the calibration decision and inspect its cited findings. A finding review alone cannot authorise a numerical suitability score.</p>",
        recipes.listing(
            review._row_link(
                r, recipes.practice_name(r["practice"]) + " · " + recipes.record_name(r)
            )
            for r in held
        ),
        '<p><a href="review.html">Browse all reviewed and unreviewed records</a></p>',
    ]
    write("review-queue.html", "Review", "Unresolved evidence in this edition", "".join(queue))
    metric_rows = "".join(
        "<tr>"
        + "".join(
            f"<td>{escape(str(r[k]).replace('_', ' '))}</td>"
            for k in ("group", "population", "status", "count", "denominator")
        )
        + "</tr>"
        for r in coverage
    )
    downloads = recipes.listing(
        recipes.link("evidence-tables/" + r["path"], r["title"] + " (CSV)")
        for r in resources
    )
    write(
        "review-coverage.html",
        "Review",
        "Evidence downloads and review coverage",
        f"<p>CIAT evidence revision <code>{escape(revision[:8])}</code>. The total column gives the denominator for each count. A finding can support several rows. T3 and T6 rating counts and T4 calibration counts use separate denominators.</p>"
        '<p><a href="review-queue.html">Open outstanding reviews</a> · <a href="evidence-tables/datapackage.json">Download metadata, citation, field definitions and checksums</a></p>'
        '<div class="table-wrap"><table><caption>Applied human review and assessment coverage at the edition revision</caption><thead><tr><th>Table</th><th>Population</th><th>Status</th><th>Count</th><th>Total</th></tr></thead><tbody>'
        + metric_rows
        + "</tbody></table></div>"
        "<p>“Undetermined” means the assessment cannot establish whether the rating is provisional. “Assessed clear” means all setters were assessed and none was held or unreviewed.</p>"
        "<h2>Download tables</h2><p>Join an analytical row to its index and evidence links by <code>record_id</code>, then join each finding by <code>evidence_id</code> and its source by <code>source_id</code>. "
        "Direct, contextual and rating-setting links have distinct labels. Excluded findings remain available for their history.</p>"
        + downloads
        + '<p><a href="review-status.json">Applied review history and method decisions (JSON)</a> · <a href="review-status-manifest.json">Review manifest</a></p>',
    )
