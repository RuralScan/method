import copy
import json
from pathlib import Path
import tempfile
import unittest
from catalogue import ROOT, acceptance_text, check, digest, eligible, example_class, validate, write_immutable


class Catalogue(unittest.TestCase):
    def setUp(self):
        self.rule = json.loads((ROOT / "priority/proposals/spei12_event-0.1.0.json").read_text())

    def test_all_thirty_rows_and_five_proposals(self):
        manifest = check()
        self.assertEqual(len(manifest["proposals"]), 5)
        self.assertEqual(manifest["accepted_rules"], [])

    def test_reverse_endpoints_missing_and_true_zero(self):
        cases = [(-2.1, "high"), (-2, "high"), (-1.999, "medium"), (-1.5, "medium"),
                 (-1.499, "low"), (-1, "low"), (-.999, "none"), (0, "none"), (None, None)]
        for raw, expected in cases:
            self.assertEqual(example_class(self.rule, raw, "unitless"), expected)

    def test_units_domain_and_nonfinite_inputs(self):
        with self.assertRaises(ValueError): example_class(self.rule, 1, "percent")
        with self.assertRaises(ValueError): example_class(self.rule, float("nan"), "unitless")
        self.rule["binding"]["domain"] = {"max": 4, "min": -4}
        self.assertIsNone(example_class(self.rule, -5, "unitless"))

    def test_invalid_cuts_scores_and_unsupported_methods(self):
        for field, value in [("cuts", [-1, -2, -3]), ("cuts", [-2, -2, -1]),
                             ("cuts", [False, 1, 2]), ("cuts", [-2, -1, float("inf")]),
                             ("method", "quintiles"), ("class_scores", {"none": 0})]:
            rule = copy.deepcopy(self.rule); rule[field] = value
            with self.assertRaises(ValueError): validate(rule)

    def test_held_binary_cannot_be_forced_through_classifier(self):
        rule = json.loads((ROOT / "priority/proposals/iplc_presence-0.1.0.json").read_text())
        with self.assertRaises(ValueError): example_class(rule, 1, "binary")
        rule["cuts"] = [0, .3, .6]
        with self.assertRaises(ValueError): validate(rule)

    def test_any_semantic_edit_changes_proposal_identity(self):
        before = validate(self.rule)
        for section, field, value in [("context", "period", "1991–2020"), ("binding", "field", "other")]:
            rule = copy.deepcopy(self.rule); rule[section][field] = value
            self.assertNotEqual(before, validate(rule))
        rule = copy.deepcopy(self.rule); rule["sources"][0]["sha256"] = "0" * 64
        self.assertNotEqual(before, validate(rule))

    def test_current_candidates_cannot_be_released(self):
        for path in (ROOT / "priority/proposals").glob("*.json"):
            with self.assertRaises(ValueError): eligible(json.loads(path.read_text()), {})

    def ready_fixture(self):
        # Synthetic only: never writes votes, method events, receipts or releases.
        rule = copy.deepcopy(self.rule)
        rule["blockers"] = []
        rule["context"].update(geography="synthetic_fixture", period="2000", purpose="test_only")
        rule["binding"].update(validation="verified", dataset_id="fixture", asset="fixture", field="fixture")
        rule["sources"][0].update(review_state="kept", source_id="fixture", finding_ids=["fixture"])
        decisions = {"priority_catalogue_release": {"status": "decided"}, rule["decision_id"]: {
            "status": "decided", "outcome": acceptance_text(rule), "decision_ref": "https://github.com/RuralScan/method/pull/1"}}
        return rule, decisions

    def test_acceptance_is_exact_and_rejects_stale_content(self):
        rule, decisions = self.ready_fixture()
        eligible(rule, decisions)
        rule["cuts"][0] = -2.01
        with self.assertRaises(ValueError): eligible(rule, decisions)

    def test_descriptor_m2b_and_open_storage_decision_block(self):
        for role in ["descriptor", "investment_risk"]:
            rule, decisions = self.ready_fixture(); rule["role"] = role
            with self.assertRaises(ValueError): eligible(rule, decisions)
        rule, decisions = self.ready_fixture(); decisions["priority_catalogue_release"]["status"] = "open"
        with self.assertRaises(ValueError): eligible(rule, decisions)

    def test_immutable_retry_and_rollback_keep_old_bytes(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            first = write_immutable(directory, {"edition": 1})
            self.assertEqual(first, write_immutable(directory, {"edition": 1}))
            second = write_immutable(directory, {"edition": 2})
            self.assertNotEqual(first, second)
            self.assertEqual(first, write_immutable(directory, {"edition": 1}))
            first.write_text("tampered")
            with self.assertRaises(ValueError): write_immutable(directory, {"edition": 1})

    def test_terciles_require_pinned_sample_and_never_invent_none(self):
        values = [0, 1, 2, 3, 4, 5, 6]
        self.rule.update(method="terciles", cuts=[2, 4], direction="higher_is_more_concern",
                         reference_sample={"values": values, "sha256": digest(values), "population": "synthetic",
                                           "period": "test", "exclusions": "no missing or none observations",
                                           "n": 7, "algorithm": "linear_n_minus_1", "none_condition": None})
        self.assertEqual(example_class(self.rule, 0, "unitless"), "low")
        self.assertEqual(example_class(self.rule, 2, "unitless"), "low")
        self.assertEqual(example_class(self.rule, 4, "unitless"), "medium")
        self.rule["reference_sample"]["values"][0] = -.1
        with self.assertRaises(ValueError): validate(self.rule)

    def test_collapsed_relative_cuts_fail(self):
        self.rule.update(method="terciles", cuts=[1, 1])
        with self.assertRaises(ValueError): validate(self.rule)

    def test_handoff_vectors_are_internally_consistent(self):
        vectors = json.loads((ROOT / "priority/test-vectors.json").read_text())
        for case in vectors["classification"]["cases"]:
            self.assertEqual(example_class(self.rule, case["raw"], "unitless"), case["class"])
        forward = vectors["forward_synthetic"]
        self.rule.update(cuts=forward["cuts"], unit=forward["unit"], direction=forward["direction"])
        self.rule["binding"]["domain"] = dict(zip(["min", "max"], forward["domain"]))
        for value, label in forward["cases"]:
            self.assertEqual(example_class(self.rule, value, "percent"), label)
        conversion = vectors["conversion_synthetic"]
        self.assertEqual(conversion["input"] * conversion["scale"] + conversion["offset"], conversion["expected"])
        for case in vectors["aggregation"]:
            if case["mask"] is False:
                self.assertEqual(case["expected"], "excluded")
            elif case["mask"] is None or any(w > 0 and s is None for w, s in zip(case["weights"], case["scores"])):
                self.assertIsNone(case["expected"])
            else:
                contributions = [w * s / sum(case["weights"]) for w, s in zip(case["weights"], case["scores"]) if w > 0]
                self.assertAlmostEqual(sum(contributions), case["expected"])

    def test_schema_covers_all_authored_fields(self):
        schema = json.loads((ROOT / "priority/proposal-schema.json").read_text())
        self.assertEqual(set(schema["required"]), set(self.rule))
        self.assertEqual(set(schema["properties"]), set(self.rule))
        self.assertFalse(schema["additionalProperties"])


if __name__ == "__main__": unittest.main()
