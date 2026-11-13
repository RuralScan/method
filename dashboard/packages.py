"""Shared CSV, metadata and catalogue publishing for dashboard editions."""

import csv
import json
from hashlib import sha256

SITE = "https://ruralscan.github.io/method/"
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


def table(directory, name, title, fields, records, *, primary=None, joins=()):
    columns = [f["name"] for f in fields]
    expected = set(columns)
    path = directory / (name + ".csv")
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        for record in records:
            if record.keys() != expected:
                raise ValueError(f"Export fields differ from schema for {name}")
            writer.writerow(record)
    schema = {
        "fields": fields,
        "primaryKey": primary or columns[0],
        "missingValues": [""],
    }
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


def catalog_entry(directory, package):
    metadata_url = package["id"]
    return {
        "@type": "Dataset",
        "@id": metadata_url,
        "name": package["title"],
        "description": package["description"],
        "identifier": package["name"],
        "version": package["version"],
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
                "contentUrl": metadata_url.rsplit("/", 1)[0] + "/" + r["path"],
                "sha256": r["hash"].split(":", 1)[1],
            }
            for r in package["resources"]
        ],
    }
