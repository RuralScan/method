from pathlib import Path
import subprocess
import tempfile
import unittest
import shutil

from release import ROOT, TRACE, read_table, release


class DefinitionRelease(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for name in ("configuration", "data-model", "decisions"):
            shutil.copytree(ROOT / name, self.root / name)
        subprocess.run(["git", "init", "-q", self.root], check=True)
        self.git("add", ".")
        self.git(
            "-c",
            "user.name=Test",
            "-c",
            "user.email=test@example.org",
            "commit",
            "-qm",
            "Published release",
        )

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.root)

    def test_pinned_release_and_reviewed_change(self):
        old = self.git("show", "HEAD:configuration/release.json")
        path = self.root / "configuration/lookups/family_rollup_policy.csv"
        path.write_bytes(
            path.read_bytes().replace(b"inspection.", b"inspection in this edition.")
        )
        with self.assertRaisesRegex(ValueError, "decided method code"):
            release(self.root, "HEAD", {})
        for code in (
            "missing",
            next(
                r["decision_id"]
                for r in read_table(self.root / "decisions/current.csv")[1]
                if r["status"] == "open"
            ),
        ):
            with self.assertRaisesRegex(ValueError, "decided method code"):
                release(self.root, "HEAD", {TRACE: code})
        changed = release(self.root, "HEAD", {TRACE: "plantation_rollup"})
        import json

        initial = json.loads(old)
        self.assertEqual(
            {k for k in changed["files"] if initial["files"][k] != changed["files"][k]},
            {TRACE},
        )
        self.assertEqual(
            initial["files"][TRACE]["sha256"],
            changed["files"][TRACE]["previous_sha256"],
        )
        self.assertEqual(old, self.git("show", "HEAD:configuration/release.json"))
        self.assertEqual(
            set(
                r["review_status"]
                for r in read_table(
                    self.root / "data-model/configuration/VONT_variable_ontology.csv"
                )[1]
            ),
            {"", "canonical", "pending", "pending_review", "rejected"},
        )

    def test_unknown_family_and_duplicate_key(self):
        path = self.root / "configuration/lookups/family_rollup_policy.csv"
        data = path.read_bytes()
        path.write_bytes(
            data.replace(b"forest_restoration__plantation", b"unknown_family")
        )
        with self.assertRaisesRegex(ValueError, "Unknown family"):
            release(self.root, "HEAD", {TRACE: "plantation_rollup"})
        path.write_bytes(data + data.splitlines(keepends=True)[1])
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            release(self.root, "HEAD", {TRACE: "plantation_rollup"})
