"""Exercise the same branch writer and pinned reader used by publishers and consumers."""

import csv
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

import register as reg


def commit(root, message):
    reg.git(root, "add", "-A")
    reg.git(
        root,
        "-c",
        "user.name=Fixture",
        "-c",
        "user.email=fixture@example.invalid",
        "commit",
        "-qm",
        message,
    )
    return reg.git(root, "rev-parse", "HEAD").decode().strip()


def event(action, sequence, code="rule_new", **fields):
    return dict(
        {
            "decision_id": code,
            "action": action,
            "sequence": sequence,
            "recorded_on": "2026-11-16",
            "scope": "T3 hazard ratings",
            "statement": "Fixture scientific rationale.",
            "source_ref": "https://github.com/RuralScan/method/issues/17",
        },
        **fields,
    )


class PinnedRegister(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.method, self.evidence = [
            Path(tmp.name) / p for p in ("method", "evidence")
        ]
        for repo in (self.method, self.evidence):
            repo.mkdir()
            reg.git(repo, "init", "-q")
        self.seed_path = "registers/methodology/decisions/method_decisions.csv"
        historical = []
        for code, status in (
            ("old_rule", "decided"),
            ("old_question", "open"),
            ("on_hold", "parked"),
        ):
            row = dict.fromkeys(reg.LEGACY_FIELDS, "")
            row.update(
                decision_id=code,
                status=status,
                raised="2026-09-01",
                question="Original question,\nwith context",
                options="one | two",
                record="archive/science.md",
                decided="one" if status == "decided" else "",
            )
            historical.append(row)
        baseline = reg.csv_bytes(reg.LEGACY_FIELDS, historical)
        archive = self.evidence / self.seed_path
        archive.parent.mkdir(parents=True)
        archive.write_bytes(baseline)
        pin = commit(self.evidence, "Archive scientific projection")
        (self.method / "decisions").mkdir()
        (self.method / reg.BASELINE).write_text(
            json.dumps(
                {
                    "repository": "RuralScan/evidence",
                    "revision": pin,
                    "path": self.seed_path,
                    "rows": 3,
                    "sha256": reg.hashlib.sha256(baseline).hexdigest(),
                }
            )
        )
        (self.method / reg.EVENTS).write_bytes(reg.csv_bytes(reg.EVENT_FIELDS, []))
        shutil.copyfile(
            reg.ROOT / "decisions/register.py", self.method / "decisions/register.py"
        )
        self.cli("build")
        self.old = commit(self.method, "First edition")

    def cli(self, *args):
        return subprocess.check_output(
            [
                sys.executable,
                str(self.method / "decisions/register.py"),
                "--evidence-repo",
                str(self.evidence),
                *args,
            ],
            text=True,
        )

    def record(self, e):
        return reg.record(self.method, self.evidence, e)

    def test_pinned_consumer_pending_implementation_and_supersession(self):
        request = event("propose", 1)
        request_file = self.method.parent / "request.json"
        request_file.write_text(json.dumps(request))
        self.assertIn("Recorded", self.cli("record", str(request_file)))
        self.record(event("decide", 2, supersedes="old_rule"))
        pending = commit(self.method, "Ratify replacement rule")
        result = json.loads(self.cli("show", "rule_new", "--revision", pending))
        self.assertEqual(result["decision"]["implementation_status"], "pending")
        self.assertEqual(result["decision"]["implementation_ref"], "")
        self.assertEqual(result["decision"]["decision_ref"], request["source_ref"])
        implementation = "https://github.com/RuralScan/evidence/commit/" + "a" * 40
        self.record(event("implement", 3, implementation_ref=implementation))
        latest = commit(self.method, "Record separate implementation")
        # Evidence can consume the edition directly as CSV without importing the writer.
        published = reg.git(
            self.method, "show", f"{latest}:decisions/current.csv"
        ).decode()
        rows = {r["decision_id"]: r for r in csv.DictReader(io.StringIO(published))}
        self.assertEqual(rows["rule_new"]["decision_ref"], request["source_ref"])
        self.assertEqual(rows["rule_new"]["implementation_ref"], implementation)
        self.assertEqual(rows["rule_new"]["implementation_status"], "implemented")
        self.assertEqual(
            (rows["old_rule"]["status"], rows["old_rule"]["superseded_by"]),
            ("superseded", "rule_new"),
        )
        # Both the earlier projection and the historical Git object survive later working-tree edits.
        (self.evidence / self.seed_path).write_text("local modifications")
        self.assertEqual(
            json.loads(self.cli("show", "rule_new", "--revision", pending)), result
        )
        original = json.loads(self.cli("show", "old_rule", "--revision", self.old))
        self.assertEqual(
            original["historical_record"]["question"],
            "Original question,\nwith context",
        )
        self.assertEqual(original["decision"]["status"], "decided")
        self.assertEqual(original["decision"]["implementation_status"], "unverified")
        self.assertEqual(original["decision"]["legacy_ref"].split("#")[-1], "L2")

    def test_retry_stale_event_and_historical_names(self):
        self.record(event("propose", 1))
        before = (self.method / reg.EVENTS).read_bytes()
        (self.method / reg.CURRENT).write_text("interrupted projection")
        self.assertFalse(self.record(event("propose", 1)))
        self.assertEqual(before, (self.method / reg.EVENTS).read_bytes())
        self.assertEqual(reg.check(self.method, self.evidence, self.old), 4)
        bad_events = [
            event("propose", 1, statement="Different request at the same sequence"),
            event("propose", 1, code="old_rule"),
            event("decide", 5),
            event("decide", 2, supersedes="missing"),
            event("decide", 2, supersedes="old_question"),
            event("decide", 2, supersedes="rule_new"),
            event("decide", 2, recorded_on="2026-01-01"),
            event("approve", 2),
            event("decide", 2, owner="assignment"),
            event(
                "implement",
                2,
                implementation_ref="https://github.com/RuralScan/evidence/commit/"
                + "b" * 40,
            ),
        ]
        for bad in bad_events:
            with self.subTest(bad=bad), self.assertRaises(ValueError):
                self.record(bad)
        self.assertEqual(before, (self.method / reg.EVENTS).read_bytes())

    def test_existing_open_and_parked_scientific_decisions_continue(self):
        self.record(event("park", 1, code="old_question"))
        self.record(event("reopen", 2, code="old_question"))
        self.record(event("decide", 3, code="old_question"))
        self.record(event("decide", 1, code="on_hold"))
        rows, legacy, _ = reg.replay(
            self.method, self.evidence, (self.method / reg.EVENTS).read_bytes()
        )
        for code in ("on_hold", "old_question"):
            self.assertEqual(rows[code]["status"], "decided")
            self.assertEqual(rows[code]["implementation_status"], "pending")
        self.assertEqual(legacy["on_hold"]["status"], "parked")
        self.assertEqual(legacy["old_question"]["status"], "open")
        with self.assertRaisesRegex(ValueError, "full SHA"):
            self.record(
                event(
                    "implement",
                    4,
                    code="old_question",
                    implementation_ref="https://github.com/RuralScan/evidence/blob/main/build.py",
                )
            )
        with self.assertRaisesRegex(ValueError, "decided scope"):
            self.record(
                event(
                    "implement",
                    4,
                    code="old_question",
                    scope="T6",
                    implementation_ref="https://github.com/RuralScan/evidence/commit/"
                    + "a" * 40,
                )
            )

    def test_rewritten_history_tampered_projection_and_seed(self):
        self.record(event("propose", 1))
        pinned = commit(self.method, "Publish proposal")
        journal = self.method / reg.EVENTS
        journal.write_bytes(
            journal.read_bytes().replace(
                b"Fixture scientific rationale.", b"Rewritten rationale."
            )
        )
        self.cli("build")
        with self.assertRaisesRegex(ValueError, "Previously published"):
            reg.check(self.method, self.evidence, pinned)
        journal.write_bytes(reg.read_file(self.method, reg.EVENTS, pinned))
        with self.assertRaisesRegex(ValueError, "projection differs"):
            reg.check(self.method, self.evidence, pinned)
        baseline = self.method / reg.BASELINE
        baseline.write_text(baseline.read_text().replace('"rows": 3', '"rows": 2'))
        with self.assertRaisesRegex(ValueError, "baseline changed"):
            reg.check(self.method, self.evidence, pinned)

    def test_implementation_link_must_resolve(self):
        ref = (
            "https://github.com/RuralScan/evidence/blob/"
            + "b" * 40
            + "/workflows/procedure.py#L20"
        )
        with (
            patch.object(
                reg,
                "urlopen",
                return_value=io.BytesIO(
                    b'{"type":"dir","path":"workflows/procedure.py"}'
                ),
            ),
            self.assertRaisesRegex(ValueError, "did not resolve"),
        ):
            reg.verify_implementation(ref)
        for url, obj in [
            (ref, {"type": "file", "path": "workflows/procedure.py"}),
            (
                "https://github.com/RuralScan/evidence/commit/" + "b" * 40,
                {"sha": "b" * 40},
            ),
        ]:
            with patch.object(
                reg, "urlopen", return_value=io.BytesIO(json.dumps(obj).encode())
            ):
                reg.verify_implementation(url)

    def test_concurrent_writer_does_not_replace_first_operation(self):
        with (
            reg.writer_lock(self.method),
            self.assertRaisesRegex(ValueError, "Another writer"),
        ):
            self.record(event("propose", 1))
        self.assertTrue(self.record(event("propose", 1)))


if __name__ == "__main__":
    unittest.main()
