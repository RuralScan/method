"""Validate priority proposals and build content-addressed review manifests.

No raster execution, source voting, scientific acceptance or publication occurs here.
"""
import argparse
from bisect import bisect_left
import csv
import io
from hashlib import sha256
import json
import math
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
SCORES = {"none": 0, "low": .33, "medium": .66, "high": 1}
FIELDS = {"format", "classification_id", "version", "author_assessment", "variables",
          "concern_id", "role", "quantity", "unit", "temporal_statistic", "context",
          "spatial_support", "binding", "method", "direction", "cuts", "endpoint",
          "missing", "class_scores", "class_meanings", "reference_sample", "sources",
          "input_sha256", "rationale", "alternatives", "blockers", "supersedes", "decision_id"}


def require(ok, message):
    if not ok:
        raise ValueError(message)


def encoded(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), allow_nan=False) + "\n").encode()


def digest(value):
    return sha256(encoded(value)).hexdigest()


def finite(value):
    return type(value) in (int, float) and math.isfinite(value)


def validate(rule):
    require(set(rule) == FIELDS, "Unknown or missing proposal fields")
    require(rule["format"] == "ruralscan.priority-proposal.v1", "Wrong proposal format")
    require(re.fullmatch(r"[a-z][a-z0-9_]*", rule["classification_id"]), "Invalid classification ID")
    require(re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", rule["version"]), "Invalid version")
    require(rule["author_assessment"] in {"proposed", "held"}, "Author cannot assert acceptance")
    require(rule["role"] in {"priority", "descriptor", "investment_risk"}, "Invalid role")
    require(rule["variables"] and len(rule["variables"]) == len(set(rule["variables"])), "Invalid variable set")
    for field in ("quantity", "unit", "temporal_statistic", "spatial_support", "rationale", "concern_id", "decision_id"):
        require(isinstance(rule[field], str) and rule[field].strip(), f"Missing {field}")
    require(rule["missing"] == "unknown" and rule["endpoint"] == "upper_inclusive", "Changed missing or endpoint policy")
    require(rule["class_scores"] == SCORES, "Changed method scores")
    require(set(rule["context"]) == {"geography", "period", "scenario", "purpose"}, "Incomplete context")
    require(rule["context"]["scenario"] and rule["context"]["purpose"], "Missing scenario/purpose")
    require(isinstance(rule["blockers"], list) and all(isinstance(b, str) and b for b in rule["blockers"]), "Invalid blockers")
    binding = rule["binding"]
    require(set(binding) == {"dataset_id", "asset", "field", "source_unit", "scale", "offset", "domain", "nodata", "validation"}, "Invalid binding fields")
    require(finite(binding["scale"]) and binding["scale"] > 0 and finite(binding["offset"]), "Invalid conversion")
    domain = binding["domain"]
    require(set(domain) == {"min", "max"} and all(x is None or finite(x) for x in domain.values()), "Invalid domain")
    require(domain["min"] is None or domain["max"] is None or domain["min"] < domain["max"], "Reversed domain")
    require(binding["source_unit"] and binding["nodata"] and binding["validation"] in {"not_verified", "documentation_only", "verified"}, "Missing binding provenance")
    method = rule["method"]
    require(method in {None, "thresholds", "terciles"}, "Unsupported classification method")
    if method is None:
        require(rule["cuts"] is None and rule["class_meanings"] is None and rule["blockers"] and rule["author_assessment"] == "held", "Unsupported rules must remain held without cuts")
    else:
        require(rule["direction"] in {"higher_is_more_concern", "lower_is_more_concern"}, "Invalid direction")
        cuts = rule["cuts"]
        require(isinstance(cuts, list) and len(cuts) == (3 if method == "thresholds" else 2), "Wrong cut count")
        require(all(finite(x) for x in cuts) and all(a < b for a, b in zip(cuts, cuts[1:])), "Cutoffs must be finite and strictly increasing")
        require(isinstance(rule["class_meanings"], dict) and set(rule["class_meanings"]) == set(SCORES), "Missing class meanings")
        if method == "thresholds":
            require(rule["reference_sample"] is None, "Thresholds must not fit a sample")
        else:
            sample = rule["reference_sample"]
            require(isinstance(sample, dict) and set(sample) == {"values", "sha256", "population", "period", "exclusions", "n", "algorithm", "none_condition"}, "Incomplete relative reference")
            require(sample["none_condition"] is None, "Non-null none predicates require a separately tested adapter")
            require(sample["algorithm"] == "linear_n_minus_1", "Unsupported quantile algorithm")
            require(sample["population"] and sample["period"] and sample["exclusions"], "Unidentified reference population")
            values = sample["values"]
            require(isinstance(values, list) and all(finite(x) for x in values) and len(values) >= 3, "Invalid reference sample")
            require(sample["n"] == len(values) and sample["sha256"] == digest(values), "Stale reference sample")
            ordered = sorted(values)
            def quantile(q):
                pos = (len(ordered) - 1) * q
                lo = int(pos); hi = min(lo + 1, len(ordered) - 1)
                return ordered[lo] + (ordered[hi] - ordered[lo]) * (pos - lo)
            require(cuts == [quantile(1 / 3), quantile(2 / 3)], "Stale realized tercile cuts")
    require(rule["sources"], "No source packet")
    for source in rule["sources"]:
        require(set(source) == {"repository", "revision", "path", "sha256", "source_id", "finding_ids", "review_state"}, "Invalid source reference")
        require(source["repository"] == "RuralScan/evidence" and re.fullmatch(r"[0-9a-f]{40}", source["revision"]), "Unpinned source repository")
        require(re.fullmatch(r"workflows/priority_classification/packets/[a-z0-9_]+\.json", source["path"]), "Invalid packet path")
        require(re.fullmatch(r"[0-9a-f]{64}", source["sha256"]), "Invalid source packet digest")
    require(rule["input_sha256"] and all(re.fullmatch(r"[0-9a-f]{64}", h) for h in rule["input_sha256"].values()), "Missing definition dependency hashes")
    return digest(rule)


def example_class(rule, value, unit):
    """Review-only scalar conformance oracle; not a spatial runtime adapter."""
    validate(rule)
    require(rule["method"] is not None, "Held rule has no classifier")
    require(unit == rule["unit"], "Input units differ; convert explicitly before classification")
    if value is None:
        return None
    require(finite(value), "Input must be finite or null")
    lo = rule["binding"]["domain"]["min"]
    hi = rule["binding"]["domain"]["max"]
    if (lo is not None and value < lo) or (hi is not None and value > hi):
        return None
    labels = ["none", "low", "medium", "high"] if rule["method"] == "thresholds" else ["low", "medium", "high"]
    if rule["direction"] == "lower_is_more_concern":
        labels.reverse()
    return labels[bisect_left(rule["cuts"], value)]


def acceptance_text(rule):
    return f"Accept priority proposal sha256:{validate(rule)} for context sha256:{digest(rule['context'])}."


def eligible(rule, decisions):
    """Structural acceptance check. Protected human PR review authenticates decisions."""
    validate(rule)
    require(rule["role"] == "priority" and rule["method"] is not None, "Not a scoring rule")
    require(not rule["blockers"], "Unresolved blockers")
    require(all(rule["context"].values()) and rule["context"]["purpose"] != "method_review_only_not_pilot", "Unresolved target context")
    b = rule["binding"]
    require(b["validation"] == "verified" and b["dataset_id"] and b["asset"] and b["field"], "Unverified binding")
    require(all(s["review_state"] == "kept" and s["source_id"] and s["finding_ids"] for s in rule["sources"]), "Unreviewed/unregistered sources")
    route = decisions.get("priority_catalogue_release", {})
    require(route.get("status") == "decided", "Storage/release contract not accepted")
    decision = decisions.get(rule["decision_id"], {})
    require(decision.get("status") == "decided" and decision.get("outcome") == acceptance_text(rule), "No exact-content classification acceptance")
    require(re.fullmatch(r"https://github.com/RuralScan/method/pull/[0-9]+", decision.get("decision_ref", "")), "Acceptance needs protected review PR")


def git_blob(root, revision, path):
    return subprocess.check_output(["git", "show", f"{revision}:{path}"], cwd=root)


def check(root=ROOT, evidence_repo=None, base=None):
    audit = json.loads((root / "priority/audit.json").read_text())
    keys = {(e["table"], e["variable_id"]) for e in audit["entries"]}
    actual = set()
    originals = {}
    for table, file in [("T2", "T2_climate_risk.csv"), ("T5", "T5_opportunity_space.csv")]:
        rows = list(csv.DictReader(io.StringIO((root / "data-model/configuration" / file).read_text())))
        actual.update((table, row["variable_id"]) for row in rows)
        originals.update({(table, row["variable_id"]): row for row in rows})
    require(keys == actual and len(keys) == len(audit["entries"]) == 30, "Audit omits or duplicates legacy entries")
    require(sum(e["table"] == "T5" and e["legacy_record"]["mcda_role"] == "priority" for e in audit["entries"]) == 15, "Wrong T5 role count")
    require(all(e["inventory_status"] == "audited_proposal_not_approved" and e["audit"]["interpretation_and_blocker"] for e in audit["entries"]), "Incomplete audit")
    directory = root / "data-model/configuration"
    def table(name):
        return list(csv.DictReader(io.StringIO((directory / name).read_text())))
    ontology = table("VONT_variable_ontology.csv")
    bindings = table("BIND_dataset_binding.csv")
    datasets = table("T1_data_registry.csv")
    for entry in audit["entries"]:
        variable = entry["variable_id"]
        require(entry["legacy_record"] == originals[entry["table"], variable], "Altered historical row in audit")
        expected_bindings = [r for r in bindings if r["variable"] == variable]
        ids = {entry["legacy_record"]["dataset_id"]} | {b["dataset_id"] for b in expected_bindings}
        require(entry["audit"]["ontology_records"] == [r for r in ontology if r["canonical_variable_id"] == variable], "Incorrect ontology join")
        require(entry["audit"]["binding_records"] == expected_bindings, "Incorrect binding join")
        require(entry["audit"]["dataset_records"] == [r for r in datasets if r["dataset_id"] in ids], "Incorrect dataset join")
    for path, expected in audit["input_sha256"].items():
        require(sha256((root / path).read_bytes()).hexdigest() == expected, f"Stale audit dependency: {path}")
    lock = json.loads((root / "priority/evidence.lock.json").read_text())
    files, identities = {}, set()
    for path in sorted((root / "priority/proposals").glob("*.json")):
        rule = json.loads(path.read_text()); value = validate(rule)
        identity = (rule["classification_id"], rule["version"])
        require(identity not in identities, "Duplicate rule version")
        identities.add(identity)
        require(set(rule["variables"]) <= {v for _, v in keys}, "Unknown variable")
        require(rule["input_sha256"] == audit["input_sha256"], "Stale rule dependencies")
        for source in rule["sources"]:
            require(source["revision"] == lock["revision"] and source["sha256"] == lock["files"].get(source["path"]), "Stale evidence lock")
        files[str(path.relative_to(root))] = {"file_sha256": sha256(path.read_bytes()).hexdigest(), "proposal_sha256": value, "decision_id": rule["decision_id"]}
    if evidence_repo:
        for path, expected in lock["files"].items():
            require(sha256(git_blob(evidence_repo, lock["revision"], path)).hexdigest() == expected, f"Source packet mismatch: {path}")
    if base:
        old = subprocess.check_output(["git", "ls-tree", "-r", "--name-only", base, "--", "priority/proposals"], cwd=root, text=True).splitlines()
        for path in old:
            require((root / path).exists() and (root / path).read_bytes() == git_blob(root, base, path), "Published proposal versions are immutable; add a successor")
    return {"format": "ruralscan.priority-review-manifest.v1", "status": "proposals_only_not_runtime_release", "contract_sha256": sha256((root / "data-model/priority-contract.json").read_bytes()).hexdigest(), "proposal_schema_sha256": sha256((root / "priority/proposal-schema.json").read_bytes()).hexdigest(), "audit_sha256": sha256((root / "priority/audit.json").read_bytes()).hexdigest(), "evidence_lock_sha256": sha256((root / "priority/evidence.lock.json").read_bytes()).hexdigest(), "proposals": files, "accepted_rules": []}


def write_immutable(directory, payload):
    directory.mkdir(parents=True, exist_ok=True)
    content = encoded(payload); path = directory / (sha256(content).hexdigest() + ".json")
    if path.exists():
        require(path.read_bytes() == content, "Immutable artefact was altered")
    else:
        with path.open("xb") as stream: stream.write(content)
    return path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["check", "manifest"])
    parser.add_argument("--evidence-repo", type=Path)
    parser.add_argument("--base")
    args = parser.parse_args()
    manifest = check(evidence_repo=args.evidence_repo, base=args.base)
    target = ROOT / "priority/release.json"
    if args.command == "manifest":
        target.write_text(json.dumps(manifest, indent=2) + "\n")
    else:
        require(json.loads(target.read_text()) == manifest, "Stale review manifest")
    print(f"{len(manifest['proposals'])} proposals; 0 accepted runtime rules")


if __name__ == "__main__": main()
