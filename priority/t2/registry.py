"""Validate the current T2 registry and generate its descriptive manifest.

This is a registry migration, not an evaluator or accepted calibration exporter.
"""
import argparse
import csv
import hashlib
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
SOURCE = "data-model/configuration/T2_climate_risk.csv"
FORMAT = "ruralscan.t2-registry-manifest.v1"


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def load_json(path):
    return json.loads(path.read_text())


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read(root=ROOT):
    folder = root / "priority/t2"
    schema = load_json(folder / "schema.json")
    migration = load_json(folder / "migration.json")
    with (folder / "variables.csv").open(newline="") as handle:
        reader = csv.DictReader(handle)
        require(reader.fieldnames == list(schema["fields"]), "T2 columns do not match schema")
        rows = list(reader)
    source = (root / SOURCE).read_bytes()
    require(digest(source) == migration["source"]["sha256"], "Historical T2 CSV changed")
    with (root / SOURCE).open(newline="") as handle:
        original = list(csv.DictReader(handle))
    require(original == migration["original_rows"], "Migration does not preserve the original rows")
    require(migration["source"]["path"] == SOURCE, "Unexpected historical source path")
    require(re.fullmatch(r"[0-9a-f]{40}", migration["source"]["revision"]), "Source revision must be immutable")
    require(set(migration["field_dispositions"]) == set(original[0]), "Historical fields not fully accounted for")
    require(len({r["variable_id"] for r in original}) == len(original), "Duplicate historical variable ID")
    old = {r["variable_id"]: r for r in original}
    require(len(rows) == len(old), "T2 migration added or removed entries")
    require(len({r["variable_id"] for r in rows}) == len(rows), "Duplicate current variable ID")
    require({r["variable_id"] for r in rows} == set(old), "T2 identities were not preserved")
    with (root / "data-model/configuration/T1_data_registry.csv").open(newline="") as handle:
        datasets = {r["dataset_id"] for r in csv.DictReader(handle)}
    policy = load_json(root / "data-model/priority-contract.json")
    for row in rows:
        identity = row["variable_id"]
        require(None not in row and all(v is not None for v in row.values()), f"Malformed row: {identity}")
        for field, spec in schema["fields"].items():
            value = row[field]
            require(value == value.strip(), f"Whitespace in {identity}.{field}")
            if spec.get("required"):
                require(bool(value), f"Missing {identity}.{field}")
            if value and "enum" in spec:
                require(value in spec["enum"], f"Invalid {identity}.{field}: {value}")
            if value and spec.get("identifier"):
                require(bool(re.fullmatch(r"[a-z][a-z0-9_]*", value)), f"Invalid identifier: {identity}.{field}")
        for field in ("variable", "hazard_type", "scenario_type"):
            require(row[field] == old[identity][field], f"Migration changed identity/context: {identity}.{field}")
        require(row["candidate_dataset_id"] == old[identity]["dataset_id"], f"Lost candidate dataset: {identity}")
        require(row["candidate_dataset_id"] in datasets, f"Unknown candidate dataset: {identity}")
        require(row["mcda_role"] in policy["roles"], f"Role outside priority contract: {identity}")
        require(row["readiness"] == "blocked" and row["binding_status"] == "unverified"
                and row["classification_status"] == "not_assessed",
                f"Readiness promoted without acceptance route: {identity}")
        # This initial schema cannot represent acceptance or verified binding.
        require(row["dataset_id"] == "", f"Unverified dataset promoted: {identity}")
        require(row["classification_id"] == row["classification_version"] == "", f"Classification promoted without acceptance route: {identity}")
        require(row["reference_period"] == row["context_id"] == "", f"Unreviewed context supplied: {identity}")
    require(set(policy["table_fields"]["T2"]["fields"]) <= set(schema["fields"]), "T2 priority interface field missing")
    return rows, schema, migration


def manifest(root=ROOT):
    rows, schema, migration = read(root)
    paths = ["priority/t2/variables.csv", "priority/t2/schema.json", "priority/t2/migration.json", "data-model/priority-contract.json", "data-model/configuration/T1_data_registry.csv"]
    return {
        "format": FORMAT, "version": schema["version"],
        "status": "registry_only_not_accepted_calibration",
        "table": "T2", "primary_key": "variable_id", "rows": len(rows),
        "runnable_variables": 0, "accepted_classifications": [],
        "source": migration["source"],
        "files": [{"path": path, "sha256": digest((root / path).read_bytes()),
                   "media_type": "text/csv" if path.endswith(".csv") else "application/json"} for path in paths],
    }


def check(root=ROOT):
    expected = manifest(root)
    require(load_json(root / "priority/t2/manifest.json") == expected, "Stale T2 manifest: run registry.py build")
    return expected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["build", "check"])
    args = parser.parse_args()
    if args.command == "build":
        (HERE / "manifest.json").write_text(json.dumps(manifest(), indent=2) + "\n")
    result = check()
    print(f"T2: {result['rows']} IDs preserved; {result['runnable_variables']} runnable variables; manifest verified")


if __name__ == "__main__":
    main()
