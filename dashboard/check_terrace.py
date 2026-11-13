"""Trace the bench-terrace example using only the dashboard entry point."""

import csv
import io
import json
import sys
from hashlib import sha256
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin
from urllib.request import urlopen


class Discovery(HTMLParser):
    def __init__(self):
        super().__init__()
        self.base = ""
        self.catalog = ""

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if tag == "base":
            self.base = attrs["href"]
        if (
            tag == "link"
            and "describedby" in attrs.get("rel", "").split()
            and attrs.get("type") == "application/ld+json"
        ):
            self.catalog = attrs["href"]


def check(root):
    local = not root.startswith(("http://", "https://"))
    start = Path(root).resolve().as_uri() + "/" if local else root.rstrip("/") + "/"

    def fetch(url):
        with urlopen(url, timeout=40) as response:
            return response.read()

    home = Discovery()
    home.feed(fetch(urljoin(start, "index.html")).decode())
    if not home.catalog:
        raise ValueError("Homepage lacks a machine-readable catalogue link")
    edition = urljoin(start, home.base)
    catalog_bytes = fetch(urljoin(edition, home.catalog))
    if catalog_bytes != fetch(urljoin(start, "catalog.json")):
        raise ValueError("Latest catalogue differs from selected edition")
    catalog = json.loads(catalog_bytes)
    edition_id = catalog["version"]
    public_edition = catalog["@id"].removesuffix("catalog.json")
    if not public_edition.endswith(
        "/editions/" + edition_id + "/"
    ) or not edition.endswith("/editions/" + edition_id + "/"):
        raise ValueError("Catalogue and homepage editions differ")

    def resolve(url):
        if not url.startswith(public_edition):
            raise ValueError(f"Asset does not belong to selected edition: {url}")
        return urljoin(edition, url.removeprefix(public_edition)) if local else url

    (dataset,) = [
        d
        for d in catalog["dataset"]
        if d["identifier"] == "ruralscan-bench-terrace-rainfall"
    ]
    archived = {}
    for asset in dataset["distribution"]:
        url = asset["contentUrl"]
        contents = fetch(resolve(url))
        if sha256(contents).hexdigest() != asset["sha256"]:
            raise ValueError(f"Catalogue checksum mismatch: {url}")
        archived[url] = contents
    metadata_url = dataset["@id"]
    package = json.loads(archived[metadata_url])
    review_status = json.loads(fetch(urljoin(edition, "review-status.json")))
    if (
        package["version"],
        package["producerRevision"],
        package["cookbookRelease"],
    ) != (
        edition_id,
        review_status["producer_revision"],
        review_status["release_id"],
    ):
        raise ValueError("Package and public review join use different inputs")
    tables = {}
    expected_keys = {
        "sources": ("source_id", None),
        "findings": ("evidence_id", ("source_id", "sources")),
        "mappings": ("mapping_id", ("evidence_id", "findings")),
    }
    for resource in package["resources"]:
        url = urljoin(metadata_url, resource["path"])
        contents = archived[url]
        if (
            len(contents) != resource["bytes"]
            or "sha256:" + sha256(contents).hexdigest() != resource["hash"]
        ):
            raise ValueError(f"Package checksum or size mismatch: {url}")
        schema = resource["schema"]
        primary, foreign = expected_keys[resource["name"]]
        expected_joins = (
            [
                {
                    "fields": foreign[0],
                    "reference": {"resource": foreign[1], "fields": foreign[0]},
                }
            ]
            if foreign
            else []
        )
        if (
            schema["primaryKey"] != primary
            or schema.get("foreignKeys", []) != expected_joins
        ):
            raise ValueError(f"Package lacks the documented keys: {url}")
        reader = csv.DictReader(io.StringIO(contents.decode(resource["encoding"])))
        if reader.fieldnames != [f["name"] for f in schema["fields"]]:
            raise ValueError(f"CSV header differs from schema: {url}")
        (row,) = reader
        tables[resource["name"]] = row
        for field in schema["fields"]:
            value = row[field["name"]]
            constraints = field["constraints"]
            if (
                not value
                and constraints["required"]
                or "enum" in constraints
                and value not in constraints["enum"]
            ):
                raise ValueError(f"Invalid {field['name']} in {url}")
            if value and field["type"] == "number":
                float(value)
            if (
                field["name"]
                in {"reported_minimum", "reported_maximum", "example_rainfall"}
                and field.get("unit") != "mm/year"
            ):
                raise ValueError(f"Annual rainfall unit missing: {url}")
    for resource in package["resources"]:
        row = tables[resource["name"]]
        for join in resource["schema"].get("foreignKeys", []):
            target = join["reference"]
            if row[join["fields"]] != tables[target["resource"]][target["fields"]]:
                raise ValueError(f"Broken {join['fields']} join")
    mapping, finding, source = (tables[k] for k in ("mappings", "findings", "sources"))
    status = review_status["findings"][finding["evidence_id"]]
    if not (
        mapping["mapping_id"] == "water_harvesting__terracing__annual_precipitation"
        and mapping["evidence_id"]
        == finding["evidence_id"]
        == "ev_wh_precip_wocatgl13_benchterraces"
        and finding["source_id"]
        == source["source_id"]
        == status["source_id"]
        == "wocat_wh_guidelines_2013"
        and finding["finding_review_status"] == status["status"] == "unreviewed"
        and not status["excluded"]
        and (
            float(finding["reported_minimum"]),
            float(mapping["example_rainfall"]),
            float(finding["reported_maximum"]),
        )
        == (200, 350, 600)
        and mapping["calibration_status"] == "held"
        and mapping["example_score"] == ""
        and "PDF p. 129, printed p. 116" in finding["source_locator"]
        and package["producerRevision"] in mapping["decision_url"]
    ):
        raise ValueError("Bench-terrace trace differs from acceptance case")
    print(
        f"{edition_id}: catalogue, metadata and three CSVs verified. 350 mm/year: calibration held, score unassigned."
    )


if __name__ == "__main__":
    check(sys.argv[1])
