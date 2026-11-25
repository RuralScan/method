"""Prepare immutable priority packages from merged, explicitly accepted inputs."""
import argparse
import csv
from hashlib import sha256
import importlib.util
import io
import json
from pathlib import Path
import re
import subprocess
import sys

from catalogue import ROOT, digest, eligible, encoded, require, validate, write_immutable

REV = re.compile(r"[0-9a-f]{40}")
PROPOSAL = re.compile(r"priority/proposals/[a-z0-9_]+-[0-9]+\.[0-9]+\.[0-9]+\.json")
BINDING_CHECKS = {"asset_identity", "units_and_conversion", "nodata_and_domain", "spatial_support", "temporal_statistic", "scenario", "context_resolution"}
STORAGE_ACCEPTANCE = "Accept priority catalogue sidecar storage and release contract v1."
ROUTING = {"priority/T5_classification_refs.csv", "priority/routing-directions.json"}
DEFINITIONS = {f"data-model/configuration/{name}.csv" for name in
               ("T1_data_registry", "T2_climate_risk", "T5_opportunity_space", "VONT_variable_ontology", "BIND_dataset_binding")} | ROUTING


def git(root, *args):
    return subprocess.check_output(["git", *args], cwd=root)


def blob(root, revision, path):
    require(REV.fullmatch(revision), "Full method revision required")
    return git(root, "show", f"{revision}:{path}")


def merged(root, revision, base):
    require(REV.fullmatch(revision) and REV.fullmatch(base), "Full revision and trusted main base required")
    require(subprocess.run(["git", "merge-base", "--is-ancestor", revision, base], cwd=root,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0,
            "Method input is not merged into inspected main")


def rows(data):
    return list(csv.DictReader(io.StringIO(data.decode())))


def decisions(root, revision):
    records = rows(blob(root, revision, "decisions/current.csv"))
    result = {r["decision_id"]: r for r in records}
    require(len(result) == len(records), "Duplicate decision identity")
    return result


def github_pr(number):
    return json.loads(subprocess.check_output(["gh", "api", "--hostname", "github.com", f"repos/RuralScan/method/pulls/{number}"]))


def authorize(root, decision, revision, base, fetch=github_pr):
    """Require the named merged PR to have introduced this exact ruling."""
    require(decision["status"] == "decided", "Decision remains open, parked or superseded")
    match = re.fullmatch(r"https://github.com/RuralScan/method/pull/([0-9]+)", decision["decision_ref"])
    require(match, "Decision needs its human-reviewed method PR")
    pr = fetch(int(match[1]))
    require(pr["merged"] is True and pr["base"]["ref"] == "main" and
            pr["base"]["repo"]["full_name"] == "RuralScan/method" and
            pr.get("merged_by", {}).get("type") == "User", "Decision PR is not human-merged method main")
    commit = pr["merge_commit_sha"]
    merged(root, commit, revision); merged(root, revision, base)
    code = decision["decision_id"]
    accepted = decisions(root, commit).get(code, {})
    require(accepted.get("status") == "decided" and accepted.get("ruling") == decision["ruling"], "PR does not contain the exact accepted ruling")
    parent = git(root, "rev-parse", commit + "^1").decode().strip()
    before = decisions(root, parent).get(code, {})
    require(before.get("status") != "decided" or before.get("ruling") != decision["ruling"], "Unrelated PR cannot authenticate an older ruling")
    return {"decision_id": code, "ruling": decision["ruling"], "pull_request": decision["decision_ref"], "merge_revision": commit}


def source_tool(evidence):
    folder = evidence / "workflows/priority_classification"
    sys.path.insert(0, str(folder))
    spec = importlib.util.spec_from_file_location("priority_source_store", folder / "priority_store.py")
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module


def binding_receipt(rule, record, current):
    require(set(record) == {"format", "binding_sha256", "context_sha256", "variables", "binding_ids", "checks", "evidence", "decision_id"}, "Invalid binding verification record")
    require(record["format"] == "ruralscan.priority-binding-verification.v1" and
            record["binding_sha256"] == digest(rule["binding"]) and
            record["context_sha256"] == digest(rule["context"]) and
            set(record["variables"]) == set(rule["variables"]), "Binding verification has different content/context")
    require(set(record["checks"]) == BINDING_CHECKS and all(isinstance(v, str) and v.strip() for v in record["checks"].values()), "Incomplete binding verification")
    require(isinstance(record["binding_ids"], list) and record["binding_ids"] and len(set(record["binding_ids"])) == len(record["binding_ids"]), "Binding IDs required")
    require(isinstance(record["evidence"], list) and record["evidence"] and all(
        set(e) == {"url", "locator"} and e["url"].startswith("https://") and e["locator"] for e in record["evidence"]), "Binding verification lacks evidence locators")
    decision = current.get(record["decision_id"], {})
    expected = f"Accept priority binding verification sha256:{digest(record)}."
    require(decision.get("status") == "decided" and decision.get("ruling") == expected, "Binding verification lacks exact acceptance")
    return decision


def scoring_route(rule, t5, routing_rows, directions):
    routing = {r['variable_id']: r for r in routing_rows}
    require(len(routing) == len(routing_rows) and set(routing) == set(t5), 'Incomplete or duplicated T5 routing')
    blocked = set(directions['blocked_scoring_variables'])
    require(not blocked.intersection(rule['variables']), 'Variable is blocked pending a separately defined successor')
    for variable in rule['variables']:
        if variable not in t5: continue
        row = routing[variable]
        require(row['mcda_role'] == 'priority', 'Unscored descriptor cannot be released as a priority')
        require(row['concern_id'] == rule['concern_id'], 'Rule does not match the current concern')


def build(method, revision, method_base, evidence, evidence_base, paths, fetch=github_pr):
    merged(method, revision, method_base)
    require(paths and len(paths) == len(set(paths)), "Select at least one unique proposal")
    current = decisions(method, revision); latest = decisions(method, method_base)
    storage = current.get("priority_catalogue_release", {})
    require(storage.get("status") == "decided" and storage.get("ruling") == STORAGE_ACCEPTANCE, "Storage/release contract remains unaccepted")
    require(latest.get("priority_catalogue_release") == storage, "Storage ruling changed after selected revision")
    approvals = [authorize(method, storage, revision, method_base, fetch)]
    contract = blob(method, revision, "data-model/priority-contract.json")
    require(contract == blob(method, method_base, "data-model/priority-contract.json"), "Priority contract changed after selected revision")
    source = source_tool(evidence)
    require(REV.fullmatch(evidence_base), "Full evidence main base required")
    packaged = []; identities = set(); dependencies = {}
    for path in sorted(paths):
        require(PROPOSAL.fullmatch(path), "Invalid proposal path")
        data = blob(method, revision, path); rule = json.loads(data)
        eligible(rule, current)
        identity = (rule["classification_id"], rule["version"])
        require(identity not in identities, "Duplicate rule version")
        identities.add(identity)
        decision = current[rule["decision_id"]]
        require(latest.get(rule["decision_id"]) == decision, "Classification ruling changed or was superseded")
        approvals.append(authorize(method, decision, revision, method_base, fetch))
        require(set(rule["input_sha256"]) == DEFINITIONS, "Incomplete definition/binding dependency set")
        for name, expected in rule["input_sha256"].items():
            require(name in DEFINITIONS, "Invalid definition dependency")
            body = blob(method, revision, name)
            require(sha256(body).hexdigest() == expected and body == blob(method, method_base, name), "Definition or binding dependency is stale")
            dependencies[name] = expected
        ontology = {r["canonical_variable_id"] for r in rows(blob(method, revision, "data-model/configuration/VONT_variable_ontology.csv"))}
        require(set(rule["variables"]) <= ontology, "Missing canonical variable")
        t5 = {r["variable_id"]: r for r in rows(blob(method, revision, "data-model/configuration/T5_opportunity_space.csv"))}
        require(all(t5[v]["mcda_role"] == "priority" for v in rule["variables"] if v in t5), "Descriptor cannot be scored through an alias")
        routing = rows(blob(method, revision, "priority/T5_classification_refs.csv"))
        directions = json.loads(blob(method, revision, "priority/routing-directions.json"))
        scoring_route(rule, t5, routing, directions)
        binding_path = f"priority/binding-verifications/{digest(rule['binding'])}-{digest(rule['context'])}.json"
        binding = json.loads(blob(method, revision, binding_path))
        binding_decision = binding_receipt(rule, binding, current)
        bind_rows = {r["binding_id"]: r for r in rows(blob(method, revision, "data-model/configuration/BIND_dataset_binding.csv"))}
        require(set(binding["binding_ids"]) <= bind_rows.keys(), "Missing BIND row")
        resolved = [bind_rows[key] for key in binding["binding_ids"]]
        require({r["variable"] for r in resolved} == set(rule["variables"]) and all(
            r["dataset_id"] == rule["binding"]["dataset_id"] and r["status"] != "requires_upload" and
            r["band"] in {"", rule["binding"]["field"]} for r in resolved), "Binding IDs do not resolve the accepted variable/dataset/field")
        datasets = {r["dataset_id"] for r in rows(blob(method, revision, "data-model/configuration/T1_data_registry.csv"))}
        require(rule["binding"]["dataset_id"] in datasets, "Missing T1 dataset")
        require(latest.get(binding_decision["decision_id"]) == binding_decision, "Binding approval changed")
        approvals.append(authorize(method, binding_decision, revision, method_base, fetch))
        findings = [source.resolve(evidence, ref, evidence_base) for ref in rule["sources"]]
        packaged.append({"path": path, "file_sha256": sha256(data).hexdigest(), "proposal_sha256": validate(rule),
                         "proposal_text": data.decode(), "binding_verification": binding, "source_findings": findings})
    return {"format": "ruralscan.priority-release.v1", "method_revision": revision,
            "method_main_checked": method_base, "evidence_main_checked": evidence_base,
            "contract_sha256": sha256(contract).hexdigest(), "definition_sha256": dependencies,
            "decisions": approvals, "rules": packaged}


def verify(method, package, method_base, evidence, evidence_base, fetch=github_pr):
    require(package.get("format") == "ruralscan.priority-release.v1", "Not an accepted priority package")
    rebuilt = build(method, package["method_revision"], package["method_main_checked"], evidence,
                    package["evidence_main_checked"], [r["path"] for r in package["rules"]], fetch)
    require(package == rebuilt, "Package differs from accepted inputs")
    # Historical replay stays exact; new adoption additionally checks current bases.
    build(method, package["method_revision"], method_base, evidence, evidence_base,
          [r["path"] for r in package["rules"]], fetch)
    return digest(package)


def check_releases(method, base, evidence, evidence_base):
    old = git(method, "ls-tree", "-r", "--name-only", base, "--", "priority/releases", "priority/binding-verifications").decode().splitlines()
    for name in old:
        require((method / name).is_file() and (method / name).read_bytes() == blob(method, base, name), "Published release/binding verification changed")
    count = 0
    for path in sorted((method / "priority/releases").glob("*.json")):
        value = json.loads(path.read_bytes())
        require(path.stem == digest(value) and path.read_bytes() == encoded(value), "Release filename or canonical bytes differ")
        if str(path.relative_to(method)) not in old:
            verify(method, value, base, evidence, evidence_base)
        count += 1
    return count


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=["prepare", "verify", "check-history"])
    parser.add_argument("--method-revision")
    parser.add_argument("--method-base", required=True)
    parser.add_argument("--evidence-repo", type=Path, required=True)
    parser.add_argument("--evidence-base", required=True)
    parser.add_argument("--proposal", action="append", default=[])
    parser.add_argument("--out", type=Path)
    parser.add_argument("--package", type=Path)
    args = parser.parse_args()
    if args.command == "check-history":
        print(f"{check_releases(ROOT, args.method_base, args.evidence_repo, args.evidence_base)} immutable accepted release files")
    elif args.command == "prepare":
        require(args.method_revision and args.out, "Revision and private output directory required")
        payload = build(ROOT, args.method_revision, args.method_base, args.evidence_repo, args.evidence_base, args.proposal)
        print(write_immutable(args.out, payload))
    else:
        require(args.package is not None, "Package file required")
        print(verify(ROOT, json.loads(args.package.read_bytes()), args.method_base, args.evidence_repo, args.evidence_base))


if __name__ == "__main__": main()
