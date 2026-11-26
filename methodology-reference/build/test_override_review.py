"""Check publication against the pinned specialist records and evaluator."""
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import unittest

import override_review


class OverrideReview(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.repo = Path(os.environ['RURALSCAN_EVIDENCE'])
        cls.pin = re.search(r'^EVIDENCE_OPERATING = "([0-9a-f]{40})"', Path(__file__).with_name('core.py').read_text(), re.M)[1]
        cls.model = override_review.payload(cls.repo, cls.pin)

    def test_candidates_are_exact_pending_source_records(self):
        self.assertEqual(len(self.model['records']), 4)
        for item in self.model['records']:
            candidate = item['candidate']
            source = override_review.blob(self.repo, self.pin, f"suitability/overrides/candidates/{candidate['id']}.json")
            self.assertEqual(candidate, json.loads(source))
            self.assertEqual(item['sha256'], hashlib.sha256(source).hexdigest())
            self.assertEqual(candidate['status'], 'pending')
            self.assertIs(candidate['activate'], False)
        self.assertIs(self.model['activate'], False)
        self.assertIs(self.model['runtime_implemented'], False)

    def test_curves_preserve_declared_twenty_and_eighty_percent_anchors(self):
        curves = [c for r in self.model['records'] for c in r['curves']]
        self.assertTrue(curves)
        for curve in curves:
            points = dict(curve['points'])
            self.assertAlmostEqual(points[curve['x20']], .2)
            self.assertAlmostEqual(points[curve['x80']], .8)
            self.assertTrue(all(0 <= y <= 1 for x, y in curve['points']))

    def test_reference_examples_do_not_invent_eligible_hectares(self):
        examples = {e['id']: e['result'] for e in self.model['examples']}
        climate = examples['fmnr-dan-saga']
        self.assertEqual(climate['state'], 'climate_pass_host_or_legal_unresolved')
        self.assertGreater(climate['score'], 0)
        self.assertIsNone(climate['area_ha'])
        mangrove = examples['mangrove-partial-unit']
        self.assertEqual(mangrove['score'], .6)
        self.assertIsNone(mangrove['area_ha'])
        self.assertEqual((mangrove['area_lower_ha'], mangrove['area_upper_ha']), (0,100))

    def test_different_revision_cannot_be_published(self):
        with self.assertRaisesRegex(ValueError, 'differs from the operating pin'):
            override_review.payload(self.repo, '0' * 40)

    def test_official_validator_rejects_activation(self):
        from t4_synthesis import profiles
        candidate = copy.deepcopy(self.model['records'][0]['candidate'])
        candidate['activate'] = True
        with self.assertRaises((ValueError, AssertionError)):
            profiles.validate_candidate(candidate)


if __name__ == '__main__':
    unittest.main()
