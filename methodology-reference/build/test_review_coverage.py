"""Reconcile the reference against independent EV/log and review-queue inputs."""

import json
import unittest
from collections import Counter

import review_coverage as coverage


class ReviewCoverage(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.queue = coverage.verified(coverage.CACHE.read_bytes())
        cls.model = coverage.load()

    def test_review_counts_match_ev_and_final_consensus_events(self):
        latest = {r["evidence_id"]: r.get("decision") for r in self.queue["review_log"]}
        expected = {}
        for row in self.queue["registers"]["EV_evidence_register"]:
            eid = row["evidence_id"]
            decision = latest.get(eid)
            if row.get("review_state") == "dropped" or decision in {"drop", "reject"}:
                state = "rejected"
            elif decision in {"flag", "hold", "query"} or row.get("review_state") in {
                "held",
                "flagged",
                "query",
            }:
                state = "held"
            elif decision != "reopen" and str(row.get("reviewer_ok")).lower() == "true":
                state = "reviewed_kept"
            else:
                state = "pending"
            expected[eid] = state
        self.assertEqual(
            expected, {eid: f["status"] for eid, f in self.model.findings.items()}
        )
        counts = Counter(expected.values())
        actual = self.model.counts()
        self.assertEqual(
            actual["retained_total"],
            counts["pending"] + counts["held"] + counts["reviewed_kept"],
        )
        self.assertEqual(actual["registered_total"], len(expected))
        # A held unit with an earlier reviewer_ok flag must still be unresolved.
        held = [eid for eid, state in expected.items() if state == "held"]
        self.assertTrue(held)

    def test_lanes_match_queue_filters_without_losing_uncited_effects(self):
        for lane in ("T3", "T6"):
            self.assertEqual(
                self.model.ids(lane=lane), set(self.queue["membership"][lane])
            )
        for lane, roles in (
            ("T4", {"structural_suitability"}),
            ("M2b", {"operational_risk"}),
            ("effects", {"nbs_effect", "asset_vulnerability"}),
        ):
            expected = {
                u["evidence_id"]
                for u in self.queue["registers"]["EV_evidence_register"]
                if u.get("use_role") in roles
            }
            self.assertEqual(self.model.ids(lane=lane), expected)
        uncited = (
            self.model.ids(lane="effects")
            - self.model.ids(lane="T3")
            - self.model.ids(lane="T6")
        )
        self.assertTrue(
            any(self.model.findings[eid]["status"] == "pending" for eid in uncited)
        )

    def test_practice_totals_match_register_without_scope_assumptions(self):
        units = self.queue["registers"]["EV_evidence_register"]
        for practice in {u["nbs_id"] for u in units}:
            self.assertEqual(
                self.model.ids("practice:" + practice),
                {u["evidence_id"] for u in units if u["nbs_id"] == practice},
            )

    def test_broader_and_old_family_scopes_stay_visible_not_assigned_to_children(self):
        key = "family:agroforestry__wind_shelter"
        specific = self.model.ids(key)
        broader = self.model.ids(key, relation="broader")
        legacy = self.model.ids(key, relation="legacy")
        self.assertTrue(broader)
        self.assertTrue(legacy)
        self.assertFalse(specific & (broader | legacy))
        parent = self.model.ids("practice:agroforestry")
        self.assertTrue((broader | legacy | specific) <= parent)
        pending_scope = {
            eid
            for eid, f in self.model.findings.items()
            if f["scope_status"] == "source_scope_review_required"
        }
        self.assertEqual(len(pending_scope), 567)
        self.assertTrue(pending_scope <= parent)

    def test_no_compiled_mapping_does_not_hide_collected_t4_evidence(self):
        self.assertGreater(
            self.model.counts("practice:forest_restoration", "T4")["retained_total"], 0
        )
        self.assertGreater(
            self.model.counts("practice:mangrove_restoration", "T4")["awaiting"], 0
        )

    def test_duplicate_membership_is_counted_once(self):
        queue = json.loads(json.dumps(self.queue))
        scope = queue["evidence_hierarchy"]["coverage"]["practice:agroforestry"]
        eid = next(iter(scope["descendant_evidence_ids"]))
        scope["direct_evidence_ids"].extend([eid, eid])
        self.assertEqual(
            coverage.Coverage(queue).counts("practice:agroforestry"),
            self.model.counts("practice:agroforestry"),
        )

    def test_corrupt_input_fails_closed(self):
        with self.assertRaisesRegex(ValueError, "does not match"):
            coverage.verified(b"{}")
        queue = json.loads(json.dumps(self.queue))
        queue["evidence_hierarchy"]["coverage"]["practice:agroforestry"]["pending"] += 1
        with self.assertRaisesRegex(ValueError, "count mismatch"):
            coverage.Coverage(queue)

    def test_download_contains_no_personal_votes_or_review_notes(self):
        for finding in self.model.export()["findings"]:
            self.assertEqual(
                set(finding),
                {
                    "evidence_id",
                    "practice",
                    "node",
                    "scope_status",
                    "status",
                    "lanes",
                    "source_id",
                    "citation",
                    "variable",
                    "url",
                },
            )


if __name__ == "__main__":
    unittest.main()
