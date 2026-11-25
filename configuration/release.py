"""Build and verify the definition inventory that the evidence compiler can adopt."""

import argparse
import csv
from hashlib import sha256
import json
from math import isfinite
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]
CATALOG = "configuration/release.json"
CONTRACT = "configuration/contract.json"
TRACE = "schema/lookups/family_rollup_policy.csv"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_table(path):
    with path.open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream, strict=True)
        rows = list(reader)
        require(
            all(None not in row and None not in row.values() for row in rows),
            f"Malformed CSV row in {path}",
        )
        return reader.fieldnames, rows


def bytes_json(value):
    return (json.dumps(value, sort_keys=True, indent=2) + "\n").encode()


def previous(root, base):
    result = subprocess.check_output(["git", "ls-tree", base, "--", CATALOG], cwd=root)
    if not result:
        return {}
    return json.loads(
        subprocess.check_output(["git", "show", f"{base}:{CATALOG}"], cwd=root)
    )["files"]


def release(root, base, approvals):
    contract = json.loads((root / CONTRACT).read_bytes())
    prior = previous(root, base)
    if prior:
        require(set(contract) == set(prior), "Compiler contract inventory changed")
    decisions = {
        r["decision_id"]: r for r in read_table(root / "decisions/current.csv")[1]
    }
    active = {code for code, row in decisions.items() if row["status"] == "decided"}
    files, tables = {}, {}
    for target, spec in contract.items():
        path = root / spec["file"]
        columns, rows = read_table(path)
        require(columns == spec["columns"], f"Changed header in {target}")
        keys = [tuple(row[k] for k in spec["key"]) for row in rows]
        require(
            all(key[0] for key in keys) and len(keys) == len(set(keys)),
            f"Duplicate or empty key in {target}",
        )
        digest = sha256(path.read_bytes()).hexdigest()
        entry = dict(file=spec["file"], sha256=digest)
        if target in prior and digest == prior[target]["sha256"]:
            require(
                target not in approvals, f"Approval references unchanged file {target}"
            )
            entry = prior[target]
        elif target not in prior and digest == spec["seed_sha256"] and target != TRACE:
            entry["origin"] = "archived compiler baseline"
        else:
            code = approvals.pop(target, None)
            require(code in active, f"{target} needs an active decided method code")
            entry.update(
                decision_id=code,
                previous_sha256=prior[target]["sha256"]
                if target in prior
                else spec["seed_sha256"],
            )
        files[target] = entry
        tables[path.stem] = rows
    require(not approvals, f"Unknown or unused target(s): {sorted(approvals)}")
    check_compatibility(root, tables)
    from family_transition import TRANSITION, validate as validate_family_transition

    transition = validate_family_transition(root)
    require(transition["decision_id"] in active, "Family transition needs a decided method code")
    return dict(
        format="ruralscan.compiler-definitions.v1",
        files=files,
        family_transition={
            "file": TRANSITION,
            "sha256": sha256((root / TRANSITION).read_bytes()).hexdigest(),
            "decision_id": transition["decision_id"],
            "adoption": "separate_evidence_compatibility_and_scope_review_required",
        },
        archive=json.loads((root / "configuration/archive.json").read_bytes()),
    )


def check_compatibility(root, tables):
    ontology = {
        row["canonical_variable_id"] for row in tables["VONT_variable_ontology"]
    }
    family_rows = tables["FAM_family_registry"]
    scopes = {(row["nbs_id"], row["suitability_family_id"]) for row in family_rows}
    directory = root / "data-model/configuration"
    practices = {
        row["nbs_id"]
        for path in (directory / "recipes").glob("*/T0_nbs_registry.csv")
        for row in read_table(path)[1]
    }
    contexts = {
        (row["context_type"], row["context_id"])
        for row in read_table(directory / "T7_geographic_context.csv")[1]
    }
    contexts.add(("global", ""))
    dataset_ids = {
        row["dataset_id"]
        for row in read_table(root / "data-model/configuration/T1_data_registry.csv")[1]
    }
    rules = json.loads((root / "data-model/structure/columns.json").read_bytes())[
        "tables"
    ]
    targets = {
        "T3": {
            r["code"]
            for r in tables["configuration_vocabulary"]
            if (r["table"], r["field"]) == ("T3", "hazard_type")
        },
        "T6": {
            r["variable_id"]
            for r in read_table(
                root / "data-model/configuration/T5_opportunity_space.csv"
            )[1]
        }
        | set(rules["T6"]["enum_values"]["economic_indicator_type"]),
    }
    score_rows = {r["row_id"] for r in tables["scorecard_rows"]}
    for name, rows in tables.items():
        enums = rules.get(name.split("_", 1)[0], {}).get("enum_values", {})
        for row in rows:
            for field, allowed in enums.items():
                if row.get(field):
                    require(
                        row[field] in allowed
                        or (
                            name == "VONT_variable_ontology"
                            and field == "review_status"
                            and row[field] == "pending"
                        ),
                        f"Invalid {name}.{field}: {row[field]}",
                    )
            for field in ("variable", "ev_variable"):
                if row.get(field):
                    require(
                        row[field] in ontology,
                        f"Unknown {field} in {name}: {row[field]}",
                    )
            if row.get("nbs_id") and row["nbs_id"] != "*":
                require(row["nbs_id"] in practices, f"Unknown practice in {name}")
                for field in ("home_family", "suitability_family_id"):
                    if row.get(field):
                        require(
                            (row["nbs_id"], row[field]) in scopes,
                            f"Unknown family in {name}",
                        )
            if name in {"XW_target_crosswalk", "xw_route_policy"}:
                table, key = row["target_table"], row["target_key"]
                wildcard = (
                    name == "xw_route_policy"
                    and key == "*"
                    and table in {"*", "T3", "T6"}
                )
                require(
                    wildcard or key in targets.get(table, ()),
                    f"Unknown target {table}.{key} in {name}",
                )
            if name == "BIND_dataset_binding":
                require(
                    (row["scope_type"], row["scope_id"]) in contexts,
                    "Unknown BIND context",
                )
            if name == "BIND_dataset_binding" and row["dataset_id"]:
                require(
                    row["dataset_id"] in dataset_ids,
                    f"Unknown BIND dataset: {row['dataset_id']}",
                )
            if name.startswith("scorecard_") and "row_id" in row:
                require(row["row_id"] in score_rows, f"Unknown scorecard row in {name}")
            for field in ("included", "rollup_included", "allow_crop_scope"):
                if field in row:
                    require(
                        row[field] in {"true", "false"}, f"Invalid {field} in {name}"
                    )
            if "weight_factor" in row:
                require(
                    isfinite(float(row["weight_factor"]))
                    and float(row["weight_factor"]) >= 0,
                    f"Invalid weight in {name}",
                )
            if name == "BANDS_magnitude_bands":
                ends = [float(row[k]) for k in ("abs_min", "abs_max") if row[k]]
                require(
                    all(isfinite(x) for x in ends) and ends == sorted(ends),
                    "Invalid magnitude range",
                )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["build", "check"])
    parser.add_argument("--base", required=True, help="Base method revision")
    parser.add_argument(
        "--approve", action="append", default=[], metavar="SCHEMA_PATH=DECISION_ID"
    )
    args = parser.parse_args()
    target = ROOT / CATALOG
    prior = previous(ROOT, args.base)
    if args.command == "check":
        current = json.loads(target.read_bytes())["files"]
        approvals = {
            p: x["decision_id"]
            for p, x in current.items()
            if "decision_id" in x and x != prior.get(p)
        }
    else:
        approvals = dict(pair.split("=", 1) for pair in args.approve)
    data = bytes_json(release(ROOT, args.base, approvals))
    if args.command == "build":
        target.write_bytes(data)
    else:
        require(data == target.read_bytes(), "Stale or altered definition release")
    print(f"Verified {len(json.loads(data)['files'])} compiler definitions.")


if __name__ == "__main__":
    main()
