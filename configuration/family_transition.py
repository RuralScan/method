"""Validate the agroforestry crosswalk; never rewrite evidence or review records."""

import csv
from hashlib import sha256
import json
from pathlib import Path
import re

TRANSITION = "configuration/family-transitions/agroforestry-2026-11-24.json"
FAM = "data-model/configuration/FAM_family_registry.csv"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(root):
    return json.loads((Path(root) / TRANSITION).read_bytes())


def current_rows(root):
    with (Path(root) / FAM).open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def family_definition(root, nbs_id, family_id, *, historical=False):
    """Read an explicit edition's definitions; a retired family is not an alias."""
    rows = load(root)["historical_definitions"] if historical else current_rows(root)
    found = [r for r in rows if (r["nbs_id"], r["suitability_family_id"]) == (nbs_id, family_id)]
    require(found, "Family absent from requested definition edition")
    return found


def validate(root):
    root = Path(root)
    data = load(root)
    require(data["format"] == "ruralscan.family-transition.v1", "Unknown family transition format")
    require(data["nbs_id"] == "agroforestry", "Unexpected transition practice")
    baseline = data["baseline"]
    require(baseline["repository"] == "RuralScan/method" and baseline["file"] == FAM,
            "Wrong historical definition source")
    require(re.fullmatch(r"[0-9a-f]{40}", baseline["revision"]), "Unpinned historical revision")
    require(re.fullmatch(r"[0-9a-f]{64}", baseline["sha256"]), "Missing historical digest")
    snapshot = json.loads((root / "data-model/definition-snapshot.json").read_bytes())
    for relative in (FAM, TRANSITION):
        require(snapshot["sha256"].get(relative) == sha256((root / relative).read_bytes()).hexdigest(),
                f"Stale definition snapshot: {relative}")
    old_rows = data["historical_definitions"]
    old = {r["subpractice_id"]: r for r in old_rows}
    new_rows = [r for r in current_rows(root) if r["nbs_id"] == data["nbs_id"]]
    new = {r["subpractice_id"]: r for r in new_rows}
    require(len(old) == len(old_rows) and len(new) == len(new_rows), "Duplicate subpractice ID")
    require(set(old) == set(new), "Subpractice identity lost or added outside transition")
    require(all(r["nbs_id"] == data["nbs_id"] for r in old_rows), "Misplaced historical definition")
    changes = data["subpractice_reassignments"]
    require(len({r["subpractice_id"] for r in changes}) == len(changes), "Duplicate reassignment")
    expected = {uid for uid in old if old[uid]["suitability_family_id"] != new[uid]["suitability_family_id"]}
    require({r["subpractice_id"] for r in changes} == expected, "Incomplete family crosswalk")
    for entry in changes:
        uid = entry["subpractice_id"]
        for prefix, row in (("previous", old[uid]), ("new", new[uid])):
            require(entry[prefix + "_family"] == row["suitability_family_id"] and
                    entry[prefix + "_spatial_product"] == row["spatial_product_type"],
                    "Crosswalk disagrees with definition")
        require(entry["new_spatial_product"] == "applicability_zone", "Linear feature became pixel area")
        require(entry["existing_evidence_action"] == "source_review_required", "Automatic scope transfer")
    old_families = {r["suitability_family_id"] for r in old_rows}
    new_families = {r["suitability_family_id"] for r in new_rows}
    require(set(data["legacy_families"]) == old_families - new_families, "Lost retired family definition")
    for family, spec in data["legacy_families"].items():
        require(spec["status"] == "historical_only" and spec["automatic_alias"] is False,
                "Retired family cannot be an automatic alias")
        successors = {r["new_family"] for r in changes if r["previous_family"] == family}
        require(set(spec["successors"]) == successors, "Invalid successor families")
    for families in data["display_groups"].values():
        require(len(families) == len(set(families)) and set(families) <= new_families,
                "Invalid display-group family")
    require(len(data["legacy_value_aliases"]) == 1, "Legacy spelling alias lost or duplicated")
    for alias in data["legacy_value_aliases"]:
        require(alias == dict(nbs_id="agroforestry", value="cross_family",
                             canonical_id="agroforestry__cross_family", kind="spelling_only",
                             rewritten_by_this_release=False), "Unsafe family alias")
    policy = data["evidence_migration"]
    for key in ("requires_separate_adoption_pr", "requires_source_scope_review", "preserve_evidence_ids",
                "preserve_source_ids_and_locators", "preserve_review_and_receipt_history"):
        require(policy[key] is True, f"Missing evidence protection: {key}")
    for key in ("automatic_reassignment", "reuse_approval_for_changed_scope", "duplicate_multifunction_findings",
                "copy_search_protocols_to_successors", "current_evidence_pin_changed"):
        require(policy[key] is False, f"Unsafe evidence migration: {key}")
    require(policy["unresolved_action"] == "retain_original_attribution_pending_review", "Unresolved scope lost")
    outputs = data["scientific_outputs"]
    require(outputs["definition_change_recomputes_outputs"] is False and
            outputs["affected_proposals_need_new_input_hashes_and_acceptance"] is True and
            outputs["historical_gate_reuse"] == "not_authorized_by_definition_change",
            "Definition edit cannot accept scientific outputs")
    return data
