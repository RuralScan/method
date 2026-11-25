import copy
import csv
from hashlib import sha256
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch
import catalogue
import package


class Release(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        self.git("config", "user.name", "Fixture")
        self.git("config", "user.email", "fixture@example.org")
        self.code = "fixture_decision"
        self.records = {self.code: {"decision_id": self.code, "status": "open", "ruling": "", "decision_ref": ""}}
        self.commit_decisions("Propose")
        self.before = self.head()
        self.records[self.code].update(status="decided", ruling="Exact test ruling", decision_ref="https://github.com/RuralScan/method/pull/1")
        self.commit_decisions("Accept fixture ruling")
        self.accepted = self.head()
        self.pr = {"merged": True, "base": {"ref": "main", "repo": {"full_name": "RuralScan/method"}},
                   "merged_by": {"type": "User"}, "merge_commit_sha": self.accepted}

    def git(self, *args): return subprocess.check_output(["git", *args], cwd=self.root).decode().strip()
    def head(self): return self.git("rev-parse", "HEAD")

    def commit_decisions(self, message):
        path = self.root / "decisions/current.csv"; path.parent.mkdir(exist_ok=True)
        with path.open("w") as f:
            writer = csv.DictWriter(f, fieldnames=["decision_id", "status", "ruling", "decision_ref"])
            writer.writeheader(); writer.writerows(self.records.values())
        self.git("add", "."); self.git("commit", "-qm", message)

    def test_reads_real_ruling_column_and_exact_merge(self):
        row = package.decisions(self.root, self.accepted)[self.code]
        self.assertEqual(package.authorize(self.root, row, self.accepted, self.accepted, lambda n: self.pr)["ruling"], "Exact test ruling")

    def test_unrelated_merge_cannot_approve_older_ruling(self):
        self.git("commit", "--allow-empty", "-qm", "Unrelated")
        pr = {**self.pr, "merge_commit_sha": self.head()}
        with self.assertRaises(ValueError):
            package.authorize(self.root, self.records[self.code], self.head(), self.head(), lambda n: pr)

    def test_unmerged_bot_or_wrong_repository_cannot_accept(self):
        for update in [{"merged": False}, {"merged_by": {"type": "Bot"}}, {"base": {"ref": "main", "repo": {"full_name": "Other/method"}}}]:
            with self.assertRaises(ValueError):
                package.authorize(self.root, self.records[self.code], self.accepted, self.accepted, lambda n: {**self.pr, **update})

    def test_first_batch_real_storage_decision_blocks_export(self):
        # Immutable first-batch state: future legitimate acceptance must not break this regression.
        revision = "e663fc85b4b09169fc5804181d1544c259736f5f"
        with self.assertRaisesRegex(ValueError, "Storage/release contract remains unaccepted"):
            package.build(catalogue.ROOT, revision, revision, self.root, self.accepted, ["priority/proposals/spei12_event-0.1.0.json"])

    def test_binding_verification_needs_exact_content_and_context(self):
        rule = json.loads((catalogue.ROOT / "priority/proposals/spei12_event-0.1.0.json").read_text())
        record = {"format": "ruralscan.priority-binding-verification.v1", "binding_sha256": catalogue.digest(rule["binding"]),
                  "context_sha256": catalogue.digest(rule["context"]), "variables": rule["variables"], "binding_ids": ["fixture"],
                  "checks": {k: "Synthetic observation" for k in package.BINDING_CHECKS},
                  "evidence": [{"url": "https://example.org", "locator": "Synthetic fixture"}], "decision_id": "binding_fixture"}
        decisions = {"binding_fixture": {"status": "decided", "ruling": f"Accept priority binding verification sha256:{catalogue.digest(record)}."}}
        package.binding_receipt(rule, record, decisions)
        rule["binding"]["field"] = "changed"
        with self.assertRaises(ValueError): package.binding_receipt(rule, record, decisions)

    def complete_fixture(self):
        from test_catalogue import Catalogue
        seed = Catalogue(); seed.setUp()
        rule, _ = seed.ready_fixture()
        variables = rule["variables"]
        definitions = {
            "T1_data_registry": "dataset_id\nfixture\n",
            "T2_climate_risk": "variable_id\n",
            "T5_opportunity_space": "variable_id,mcda_role\n" + "".join(f"{v},priority\n" for v in variables),
            "VONT_variable_ontology": "canonical_variable_id\n" + "".join(f"{v}\n" for v in variables),
            "BIND_dataset_binding": "binding_id,variable,dataset_id,status,band\n" + "".join(f"b{i},{v},fixture,available,fixture\n" for i, v in enumerate(variables))}
        for name, body in definitions.items():
            target = self.root / f"data-model/configuration/{name}.csv"
            target.parent.mkdir(parents=True, exist_ok=True); target.write_text(body)
        rule["input_sha256"] = {name: sha256((self.root / name).read_bytes()).hexdigest() for name in package.DEFINITIONS}
        record = {"format": "ruralscan.priority-binding-verification.v1", "binding_sha256": catalogue.digest(rule["binding"]),
                  "context_sha256": catalogue.digest(rule["context"]), "variables": variables,
                  "binding_ids": [f"b{i}" for i in range(len(variables))],
                  "checks": {k: "Synthetic observation" for k in package.BINDING_CHECKS},
                  "evidence": [{"url": "https://example.org", "locator": "Synthetic fixture"}], "decision_id": "binding_fixture"}
        target = self.root / f"priority/binding-verifications/{catalogue.digest(rule['binding'])}-{catalogue.digest(rule['context'])}.json"
        target.parent.mkdir(parents=True); target.write_bytes(catalogue.encoded(record))
        path = "priority/proposals/spei12_event-0.1.0.json"
        target = self.root / path; target.parent.mkdir(); target.write_bytes(catalogue.encoded(rule))
        (self.root / "data-model/priority-contract.json").write_text("{}\n")
        for code, ruling in {"priority_catalogue_release": package.STORAGE_ACCEPTANCE, rule["decision_id"]: catalogue.acceptance_text(rule),
                             "binding_fixture": f"Accept priority binding verification sha256:{catalogue.digest(record)}."}.items():
            self.records[code] = {"decision_id": code, "status": "decided", "ruling": ruling,
                                  "decision_ref": "https://github.com/RuralScan/method/pull/2"}
        self.commit_decisions("Accept synthetic package inputs")
        revision = self.head(); pr = {**self.pr, "merge_commit_sha": revision}
        return revision, path, lambda n: pr

    def test_complete_package_replays_and_detects_tampering_or_stale_bindings(self):
        from types import SimpleNamespace
        revision, path, fetch = self.complete_fixture()
        resolver = SimpleNamespace(resolve=lambda *args: [{"finding_id": "synthetic-kept"}])
        with patch.object(package, "source_tool", return_value=resolver):
            result = package.build(self.root, revision, revision, self.root, revision, [path], fetch)
            self.assertEqual(package.verify(self.root, result, revision, self.root, revision, fetch), catalogue.digest(result))
            changed = copy.deepcopy(result); changed["rules"][0]["proposal_text"] += " "
            with self.assertRaisesRegex(ValueError, "Package differs"):
                package.verify(self.root, changed, revision, self.root, revision, fetch)
            target = self.root / "data-model/configuration/BIND_dataset_binding.csv"
            target.write_text(target.read_text().replace("available", "requires_upload"))
            self.git("add", "."); self.git("commit", "-qm", "Change binding")
            with self.assertRaisesRegex(ValueError, "dependency is stale"):
                package.verify(self.root, result, self.head(), self.root, revision, fetch)

    def test_source_review_failure_blocks_complete_package(self):
        from types import SimpleNamespace
        revision, path, fetch = self.complete_fixture()
        def held(*args): raise ValueError("Finding is held")
        with patch.object(package, "source_tool", return_value=SimpleNamespace(resolve=held)):
            with self.assertRaisesRegex(ValueError, "Finding is held"):
                package.build(self.root, revision, revision, self.root, revision, [path], fetch)

    def test_review_manifest_is_never_an_accepted_package(self):
        manifest = json.loads((catalogue.ROOT / "priority/release.json").read_text())
        with self.assertRaisesRegex(ValueError, "Not an accepted priority package"):
            package.verify(self.root, manifest, self.accepted, self.root, self.accepted)


if __name__ == "__main__": unittest.main()
