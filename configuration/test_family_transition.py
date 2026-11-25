"""Check historical attribution and fail-closed future adoption rules."""

import csv
from hashlib import sha256
import io
import json
from pathlib import Path
import shutil
import subprocess
from tempfile import TemporaryDirectory
import unittest

from family_transition import FAM, TRANSITION, family_definition, load, validate

ROOT = Path(__file__).resolve().parents[1]


class AgroforestryTransition(unittest.TestCase):
    def test_old_definitions_match_source_and_other_practices_unchanged(self):
        data = validate(ROOT)
        pin = data["baseline"]
        original = subprocess.check_output(["git", "show", pin["revision"] + ":" + pin["file"]], cwd=ROOT)
        self.assertEqual(sha256(original).hexdigest(), pin["sha256"])
        old = list(csv.DictReader(io.StringIO(original.decode())))
        with (ROOT / FAM).open(newline="") as stream:
            current = list(csv.DictReader(stream))
        self.assertEqual([r for r in old if r["nbs_id"] == "agroforestry"], data["historical_definitions"])
        self.assertEqual([r for r in old if r["nbs_id"] != "agroforestry"],
                         [r for r in current if r["nbs_id"] != "agroforestry"])
        self.assertEqual({r["subpractice_id"] for r in old}, {r["subpractice_id"] for r in current})

    def test_old_family_requires_explicit_historical_edition(self):
        rows = family_definition(ROOT, "agroforestry", "agroforestry__linear_boundary", historical=True)
        self.assertEqual({r["subpractice_id"] for r in rows}, {"windbreaks_shelterbelts", "contour_vegetative_buffers"})
        with self.assertRaisesRegex(ValueError, "requested definition edition"):
            family_definition(ROOT, "agroforestry", "agroforestry__linear_boundary")
        with self.assertRaises(ValueError):
            family_definition(ROOT, "riparian_buffer", "agroforestry__linear_boundary", historical=True)

    def test_distinct_linear_families_and_preserved_livestock_identity(self):
        expected = {"boundary_planting": "planted_boundary_cropland", "wind_shelter": "windbreaks_shelterbelts",
                    "contour_buffers": "contour_vegetative_buffers"}
        for suffix, uid in expected.items():
            rows = family_definition(ROOT, "agroforestry", "agroforestry__" + suffix)
            self.assertEqual([r["subpractice_id"] for r in rows], [uid])
            self.assertEqual(rows[0]["spatial_product_type"], "applicability_zone")
        rows = family_definition(ROOT, "agroforestry", "agroforestry__silvopastoral")
        self.assertEqual({r["subpractice_id"] for r in rows}, {"planted_silvopasture", "agrosilvopasture"})

    def test_reject_invalid_crosswalk_and_weakened_history_protection(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            for name in ("configuration", "data-model"):
                shutil.copytree(ROOT / name, root / name)
            initial = load(root)
            mutations = [
                (lambda d: d["subpractice_reassignments"].pop(), "Incomplete family crosswalk"),
                (lambda d: d["subpractice_reassignments"][0].update(new_family="wrong"), "Crosswalk disagrees"),
                (lambda d: d["legacy_families"].clear(), "Lost retired family"),
                (lambda d: d["legacy_families"]["agroforestry__linear_boundary"].update(automatic_alias=True), "automatic alias"),
                (lambda d: d["evidence_migration"].update(preserve_review_and_receipt_history=False), "Missing evidence protection"),
                (lambda d: d["evidence_migration"].update(automatic_reassignment=True), "Unsafe evidence migration"),
                (lambda d: d["evidence_migration"].update(reuse_approval_for_changed_scope=True), "Unsafe evidence migration"),
                (lambda d: d["scientific_outputs"].update(definition_change_recomputes_outputs=True), "cannot accept"),
                (lambda d: d["evidence_aggregation"]["groups"]["agroforestry__linear_plantings"]["families"].pop(), "Incomplete evidence group"),
                (lambda d: d["evidence_aggregation"].update(specific_to_broad=False), "Missing aggregation safeguard"),
                (lambda d: d["evidence_aggregation"].update(parent_count="sum_of_child_counts"), "Invalid evidence aggregation"),
                (lambda d: d["evidence_aggregation"].update(automatic_downward_inheritance=True), "Unsafe evidence aggregation"),
                (lambda d: d["evidence_aggregation"].update(missing_child_support_is_zero=True), "Unsafe evidence aggregation"),
                (lambda d: d["evidence_aggregation"].update(pool_placement_rules=True), "Unsafe evidence aggregation"),
            ]
            for mutate, message in mutations:
                with self.subTest(message=message):
                    data = json.loads(json.dumps(initial))
                    mutate(data)
                    target = root / TRANSITION
                    target.write_text(json.dumps(data))
                    snapshot_path = root / "data-model/definition-snapshot.json"
                    snapshot = json.loads(snapshot_path.read_bytes())
                    snapshot["sha256"][TRANSITION] = sha256(target.read_bytes()).hexdigest()
                    snapshot_path.write_text(json.dumps(snapshot))
                    with self.assertRaisesRegex(ValueError, message):
                        validate(root)

    def test_reject_stale_definition_snapshot(self):
        with TemporaryDirectory() as folder:
            root = Path(folder)
            for name in ("configuration", "data-model"):
                shutil.copytree(ROOT / name, root / name)
            with (root / FAM).open("a") as stream:
                stream.write("\n")
            with self.assertRaisesRegex(ValueError, "Stale definition snapshot"):
                validate(root)
