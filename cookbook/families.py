"""Group verified practice definitions and candidate rows by their explicit family scope."""

import csv
import io
import json

TABLES = ("T3", "T4", "T6", "T6E")
PRODUCTS = {
    "area_suitability",
    "applicability_zone",
    "zonal_linear",
    "qualitative_only",
}


def text(row, field):
    value = row.get(field)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Missing {field}")
    return value


def counts():
    return dict.fromkeys(TABLES, 0)


def definitions(model, release):
    config = model / "configuration"
    files = sorted((config / "recipes").glob("*/T0_nbs_registry.csv"))
    practices = list(release.practices)
    if not practices or sorted(practices) != [p.parent.name for p in files]:
        raise ValueError("T0 practice inventory differs from the candidate")
    profiles = {}
    for path in files:
        practice = path.parent.name
        data = path.read_bytes()
        if data != release.setting(practice, path.name):
            raise ValueError(f"{practice}: candidate and method T0 bytes differ")
        rows = list(csv.DictReader(io.StringIO(data.decode("utf-8"), newline="")))
        if len(rows) != 1 or rows[0].get("nbs_id") != practice:
            raise ValueError(f"{practice}: expected one matching T0 identity")
        profiles[practice] = {
            "name": text(rows[0], "nbs_name"),
            "families": {},
            "practice_counts": counts(),
            "totals": counts(),
        }

    subpractices = set()
    owners = {}
    with (config / "FAM_family_registry.csv").open(
        encoding="utf-8", newline=""
    ) as stream:
        for row in csv.DictReader(stream):
            practice = text(row, "nbs_id")
            family = text(row, "suitability_family_id")
            variant = text(row, "subpractice_id")
            product = text(row, "spatial_product_type")
            if (
                practice not in profiles
                or owners.setdefault(family, practice) != practice
            ):
                raise ValueError(f"{family}: unknown or conflicting practice")
            if variant in subpractices:
                raise ValueError(f"Repeated subpractice ID: {variant}")
            subpractices.add(variant)
            families = profiles[practice]["families"]
            if family not in families:
                families[family] = {
                    "product_type": product,
                    "variants": [],
                    "counts": counts(),
                    "with_options": 0,
                    "selected": 0,
                    "spatially_validated": 0,
                    "mapping_variables": [],
                }
            entry = families[family]
            if product not in PRODUCTS or product != entry["product_type"]:
                raise ValueError(f"{family}: unknown or conflicting spatial product")
            entry["variants"].append(
                {
                    "id": variant,
                    "name": text(row, "name"),
                    "definition": text(row, "definition"),
                    "factor": text(row, "dominant_limiting_factor"),
                    "rationale": text(row, "grouping_rationale"),
                }
            )
    if any(not p["families"] for p in profiles.values()):
        raise ValueError("Missing FAM definitions for a practice")
    return profiles


def readiness_rows(release, practice):
    report = json.loads(release.read_bytes(f"tables/{practice}/T4_readiness.json"))
    if report["nbs_id"] != practice:
        raise ValueError(f"{practice}: readiness report has wrong practice")
    by_id = {}
    for row in report["rows"]:
        key = text(row, "rule_id")
        if key in by_id:
            raise ValueError(f"Repeated readiness ID: {key}")
        by_id[key] = row
    return by_id


def family_profiles(model, release):
    """Read T0/FAM and count each compiled row once under its declared scope."""
    profiles = definitions(model, release)
    for practice, profile in profiles.items():
        families = profile["families"]
        readiness = readiness_rows(release, practice)
        for table in TABLES:
            rows = release.table(practice, table)
            profile["totals"][table] = len(rows)
            ids = set()
            for row in rows:
                key = text(row, "mapping_id" if table == "T4" else "record_id")
                if key in ids or row.get("nbs_id") != practice:
                    raise ValueError(
                        f"{practice}/{table}: duplicate or misplaced row {key}"
                    )
                ids.add(key)
                family = row.get("suitability_family_id")
                if family is None or family == "":
                    if table == "T4":
                        raise ValueError(f"{key}: missing T4 family")
                    profile["practice_counts"][table] += 1
                    continue
                if family not in families:
                    raise ValueError(
                        f"{key}: family {family} is absent from {practice}"
                    )
                group = families[family]
                group["counts"][table] += 1
                if table == "T4":
                    if key not in readiness:
                        raise ValueError(f"{key}: missing T4 readiness")
                    report = readiness.pop(key)
                    state = report["readiness"]
                    group["with_options"] += bool(report["functions"])
                    group["selected"] += bool(state["effective_function_id"])
                    group["spatially_validated"] += state["execution_ready"] is True
                    variable = text(row, "variable")
                    if variable not in group["mapping_variables"]:
                        group["mapping_variables"].append(variable)
            allocated = profile["practice_counts"][table] + sum(
                g["counts"][table] for g in families.values()
            )
            if allocated != len(rows):
                raise ValueError(f"{practice}/{table}: row counts do not reconcile")
        # The pinned compiler can publish additional reference-only rows alongside the mappings.
        if any(r["role"] != "reference_only" for r in readiness.values()):
            raise ValueError(f"{practice}: readiness has an extra non-reference row")
        for group in families.values():
            group["mapping_variables"].sort()
    return profiles
