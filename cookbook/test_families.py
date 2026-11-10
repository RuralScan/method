import csv
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from families import TABLES, family_profiles


class ExampleRelease:
    practices = ["practice"]

    def __init__(self):
        self.identity = b"nbs_id,nbs_name\npractice,Practice\n"
        self.rows = {table: [] for table in TABLES}
        self.report = {"nbs_id": "practice", "rows": []}

    def table(self, practice, table):
        return self.rows[table]

    def setting(self, practice, filename):
        return self.identity

    def read_bytes(self, name):
        return json.dumps(self.report).encode()


class FamilyGuideTests(unittest.TestCase):
    def setUp(self):
        temporary = TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.model = Path(temporary.name)
        self.release = ExampleRelease()
        config = self.model / "configuration"
        recipe = config / "recipes/practice"
        recipe.mkdir(parents=True)
        (recipe / "T0_nbs_registry.csv").write_bytes(self.release.identity)
        self.fam = config / "FAM_family_registry.csv"
        self.variant = dict(
            nbs_id="practice",
            suitability_family_id="different_prefix__a",
            subpractice_id="first",
            name="First",
            definition="First definition",
            dominant_limiting_factor="First factor",
            grouping_rationale="First rationale",
            spatial_product_type="area_suitability",
        )
        self.write_variants([self.variant])

    def write_variants(self, rows):
        with self.fam.open("w", newline="", encoding="utf-8") as stream:
            writer = csv.DictWriter(stream, fieldnames=self.variant)
            writer.writeheader()
            writer.writerows(rows)

    def result(self):
        return family_profiles(self.model, self.release)["practice"]

    def test_scoped_counts_and_readiness_are_distinct(self):
        family = self.variant["suitability_family_id"]
        self.write_variants(
            [
                self.variant,
                self.variant
                | dict(
                    subpractice_id="other", dominant_limiting_factor="Second factor"
                ),
            ]
        )
        assigned = {"nbs_id": "practice", "suitability_family_id": family}
        self.release.rows["T3"] = [
            assigned | {"record_id": "family"},
            dict(
                nbs_id="practice",
                record_id="unassigned",
                scope_type="income_group",
                scope_id="lic",
            ),
        ]
        for uid, selected in (("m1", True), ("m2", False)):
            self.release.rows["T4"].append(
                assigned | dict(mapping_id=uid, variable="slope")
            )
            self.release.report["rows"].append(
                dict(
                    rule_id=uid,
                    functions={"a": "sha"},
                    readiness=dict(
                        effective_function_id="a" if selected else None,
                        execution_ready=False,
                    ),
                )
            )
        self.release.report["rows"].append(
            dict(rule_id="reference", role="reference_only")
        )
        result = self.result()
        group = result["families"][family]
        self.assertEqual(result["totals"], {"T3": 2, "T4": 2, "T6": 0, "T6E": 0})
        self.assertEqual(result["practice_counts"]["T3"], 1)
        self.assertEqual(group["counts"]["T3"], 1)
        self.assertEqual(
            [v["factor"] for v in group["variants"]], ["First factor", "Second factor"]
        )
        self.assertEqual(
            (group["with_options"], group["selected"], group["spatially_validated"]),
            (2, 1, 0),
        )
        self.assertEqual(group["mapping_variables"], ["slope"])

    def test_refuse_wrong_settings_scope_and_readiness(self):
        self.release.identity += b"\n"
        with self.assertRaisesRegex(ValueError, "T0 bytes differ"):
            self.result()
        self.release.identity = self.release.identity[:-1]
        self.release.rows["T4"] = [dict(nbs_id="practice", mapping_id="m")]
        with self.assertRaisesRegex(ValueError, "missing T4 family"):
            self.result()
        self.release.rows["T4"][0]["suitability_family_id"] = "unknown"
        with self.assertRaisesRegex(ValueError, "absent from practice"):
            self.result()
        self.release.rows["T4"][0]["suitability_family_id"] = self.variant[
            "suitability_family_id"
        ]
        with self.assertRaisesRegex(ValueError, "missing T4 readiness"):
            self.result()
        self.release.rows["T4"] = []
        self.release.report["rows"] = [dict(rule_id="extra", role="eligibility_gate")]
        with self.assertRaisesRegex(ValueError, "extra non-reference"):
            self.result()

    def test_reject_duplicate_rows_and_inconsistent_family_definition(self):
        record = dict(nbs_id="practice", record_id="repeat")
        self.release.rows["T6"] = [record, record]
        with self.assertRaisesRegex(ValueError, "duplicate or misplaced"):
            self.result()
        self.release.rows["T6"] = []
        self.write_variants([self.variant, self.variant])
        with self.assertRaisesRegex(ValueError, "Repeated subpractice"):
            self.result()
        self.write_variants(
            [
                self.variant,
                self.variant
                | dict(subpractice_id="next", spatial_product_type="zonal_linear"),
            ]
        )
        with self.assertRaisesRegex(ValueError, "conflicting spatial product"):
            self.result()
