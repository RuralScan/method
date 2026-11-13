"""Publish the bench-terrace trace as a versioned Frictionless Tabular Data Package."""

from packages import RIGHTS, SITE, catalog_entry, field, save, table

TITLE = "Bench-terrace rainfall evidence and calibration"
SCOPE = (
    "One T4 mapping, its one direct finding and its source. WOCAT reports where "
    "forward-sloping bench terraces are used. This example describes no surveyed "
    "geographic extent. The two contextual findings are documented in the walkthrough."
)


def generate(out, pin, mapping, claim, source, review, evidence_revision):
    decision = mapping["relationship_params"]["reviewed_adaptation"][
        "numerical_calibration"
    ]
    if mapping["evidence_ids"] != [claim["id"]] or decision["status"] != "held":
        raise ValueError(
            "Reassess the worked example after a change of direct evidence or calibration"
        )
    (profile,) = (
        p
        for p in decision["retained_source_profiles"]
        if p["evidence_id"] == claim["id"]
    )
    if {profile["source_id"], claim["source_id"], review["source_id"]} != {
        source["id"]
    }:
        raise ValueError("Bench-terrace source IDs differ")
    directory = out / "bench-terrace"
    directory.mkdir(exist_ok=True)
    edition_url = SITE + "editions/" + out.name + "/"
    ciat_blob = (
        "https://github.com/CIAT/nbs_ruralscan/blob/" + pin["source_revision"] + "/"
    )
    minimum, maximum = profile["reported_annual_rainfall_mm"]
    source_table = table(
        directory,
        "sources",
        "Cited source",
        [
            field("source_id", "CIAT source register identifier."),
            field("citation", "Citation from the pinned workbook."),
            field("publication_url", "Publisher copy of the cited source."),
            field("publication_sha256", "SHA-256 of the PDF used for this finding."),
        ],
        [
            {
                "source_id": source["id"],
                "citation": source["citation"],
                "publication_url": source["publisher_url"],
                "publication_sha256": profile["source_artifact_sha256"],
            }
        ],
    )
    finding_table = table(
        directory,
        "findings",
        "Direct evidence and public finding review",
        [
            field("evidence_id", "CIAT evidence register identifier."),
            field("source_id", "Source containing the finding."),
            field("design", "Terrace design described by the source."),
            field(
                "reported_minimum",
                "Lower end of reported rainfall where this design is used.",
                "number",
                unit=profile["unit"],
            ),
            field(
                "reported_maximum",
                "Upper end of reported rainfall where this design is used.",
                "number",
                unit=profile["unit"],
            ),
            field("source_locator", "PDF and printed page and passage."),
            field(
                "finding_review_status",
                "Applied human finding status. Held counts pending resolution. Rejected is excluded.",
                choices=["unreviewed", "held", "signed_off", "rejected"],
            ),
        ],
        [
            {
                "evidence_id": claim["id"],
                "source_id": source["id"],
                "design": profile["structure"],
                "reported_minimum": minimum,
                "reported_maximum": maximum,
                "source_locator": profile["locator"],
                "finding_review_status": review["status"],
            }
        ],
        joins=[("source_id", "sources")],
    )
    mapping_table = table(
        directory,
        "mappings",
        "T4 calibration and worked site",
        [
            field("mapping_id", "CIAT T4 suitability mapping identifier."),
            field("evidence_id", "Direct support used by this mapping."),
            field(
                "calibration_status",
                "Status of numerical calibration for this worked mapping.",
                choices=["held"],
            ),
            field("decision_date", "Date of calibration review.", "date"),
            field("decision_url", "Calibration decision at the pinned CIAT revision."),
            field(
                "example_rainfall",
                "Annual rainfall at the illustrative site.",
                "number",
                unit=profile["unit"],
            ),
            field(
                "example_score",
                "Blank means unassigned because numerical calibration is held.",
                "number",
                required=False,
            ),
        ],
        [
            {
                "mapping_id": mapping["mapping_id"],
                "evidence_id": claim["id"],
                "calibration_status": decision["status"],
                "decision_date": decision["reviewed_date"],
                "decision_url": ciat_blob + decision["decision_ref"],
                "example_rainfall": 350,
                "example_score": None,
            }
        ],
        joins=[("evidence_id", "findings")],
    )
    metadata_url = edition_url + "bench-terrace/datapackage.json"
    package = {
        "profile": "tabular-data-package",
        "name": "ruralscan-bench-terrace-rainfall",
        "id": metadata_url,
        "title": TITLE,
        "description": SCOPE,
        "version": out.name,
        "schemaVersion": "1.0.0",
        "homepage": edition_url + "terrace.html#downloads",
        "keywords": [
            "nature-based solutions",
            "water harvesting",
            "bench terraces",
            "rainfall",
            "evidence review",
        ],
        "citation": f"RuralScan. {TITLE}. Dashboard edition {out.name}. {metadata_url}",
        "accessRights": RIGHTS,
        "contact": "https://github.com/RuralScan/evidence/issues",
        "sources": [
            {"title": "Pinned CIAT evidence register", "path": claim["url"]},
            {"title": "Pinned CIAT source register", "path": source["url"]},
            {
                "title": "Public review status",
                "path": edition_url + "review-status.json",
            },
            {
                "title": "Public review status manifest",
                "path": edition_url + "review-status-manifest.json",
            },
        ],
        "producerRevision": pin["source_revision"],
        "cookbookRelease": pin["release_id"],
        "evidenceRevision": evidence_revision,
        "resources": [source_table, finding_table, mapping_table],
    }
    save(directory / "datapackage.json", package)
    return catalog_entry(directory, package)
