"""Publish the bench-terrace trace as a versioned Frictionless Tabular Data Package."""

import csv
import json
from hashlib import sha256

SITE = "https://ruralscan.github.io/method/"
TITLE = "Bench-terrace rainfall evidence and calibration"
SCOPE = (
    "One T4 mapping, its one direct finding and its source. WOCAT reports where "
    "forward-sloping bench terraces are used. This example describes no surveyed "
    "geographic extent. The two contextual findings are documented in the walkthrough."
)
RIGHTS = (
    "Public read access. A reuse licence for the extracted data awaits confirmation. "
    "The source publication retains its own terms."
)


def field(name, description, kind="string", *, required=True, choices=None, unit=None):
    constraints = {"required": required}
    if choices:
        constraints["enum"] = choices
    result = {
        "name": name,
        "type": kind,
        "description": description,
        "constraints": constraints,
    }
    if unit:
        result["unit"] = unit
    return result


def table(directory, name, title, fields, record, *, joins=()):
    columns = [f["name"] for f in fields]
    if set(columns) != record.keys():
        raise ValueError(f"Export fields differ from schema for {name}")
    path = directory / (name + ".csv")
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        writer.writerow(record)
    schema = {"fields": fields, "primaryKey": columns[0], "missingValues": [""]}
    if joins:
        schema["foreignKeys"] = [
            {"fields": key, "reference": {"resource": target, "fields": key}}
            for key, target in joins
        ]
    data = path.read_bytes()
    return {
        "name": name,
        "title": title,
        "path": path.name,
        "profile": "tabular-data-resource",
        "format": "csv",
        "mediatype": "text/csv",
        "encoding": "utf-8",
        "schema": schema,
        "bytes": len(data),
        "hash": "sha256:" + sha256(data).hexdigest(),
        "accessRights": RIGHTS,
    }


def save(path, data):
    path.write_text(
        json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
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
        {
            "source_id": source["id"],
            "citation": source["citation"],
            "publication_url": source["publisher_url"],
            "publication_sha256": profile["source_artifact_sha256"],
        },
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
        {
            "evidence_id": claim["id"],
            "source_id": source["id"],
            "design": profile["structure"],
            "reported_minimum": minimum,
            "reported_maximum": maximum,
            "source_locator": profile["locator"],
            "finding_review_status": review["status"],
        },
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
        {
            "mapping_id": mapping["mapping_id"],
            "evidence_id": claim["id"],
            "calibration_status": decision["status"],
            "decision_date": decision["reviewed_date"],
            "decision_url": ciat_blob + decision["decision_ref"],
            "example_rainfall": 350,
            "example_score": None,
        },
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
    dataset = {
        "@type": "Dataset",
        "@id": metadata_url,
        "name": TITLE,
        "description": SCOPE,
        "identifier": package["name"],
        "version": out.name,
        "url": package["homepage"],
        "citation": package["citation"],
        "keywords": package["keywords"],
        "conditionsOfAccess": RIGHTS,
        "distribution": [
            {
                "@type": "DataDownload",
                "name": "Tabular Data Package metadata, joins and checksums",
                "encodingFormat": "application/json",
                "contentUrl": metadata_url,
                "sha256": sha256(
                    (directory / "datapackage.json").read_bytes()
                ).hexdigest(),
            }
        ]
        + [
            {
                "@type": "DataDownload",
                "name": r["title"],
                "encodingFormat": r["mediatype"],
                "contentUrl": edition_url + "bench-terrace/" + r["path"],
                "sha256": r["hash"].split(":", 1)[1],
            }
            for r in package["resources"]
        ],
    }
    save(
        out / "catalog.json",
        {
            "@context": "https://schema.org",
            "@type": "DataCatalog",
            "@id": edition_url + "catalog.json",
            "name": "RuralScan published evidence packages",
            "version": out.name,
            "dataset": [dataset],
        },
    )
