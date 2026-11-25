import copy
import json
import unittest
from unittest.mock import patch
import binding_candidates as bindings


class BindingCandidateTests(unittest.TestCase):
    def setUp(self):
        self.rows = bindings.read_rows()

    def row(self, key):
        return next(r for r in self.rows if r['binding_id'] == key)

    def test_generated_projection_and_observed_encoding_vectors(self):
        bindings.validate(self.rows)
        self.assertEqual((bindings.ROOT / 'candidates.json').read_bytes(), bindings.generated(self.rows))
        self.assertEqual(len(self.rows), 14)

    def test_di_wrong_percent_scale_rejected_by_real_sample(self):
        self.row('fao_di_annual_candidate')['decode']['scale'] = 1
        with self.assertRaisesRegex(ValueError, 'Encoding regression'):
            bindings.validate(self.rows)

    def test_spei_display_limits_are_not_domain_limits(self):
        self.row('spei03_211_candidate')['decode']['valid_range'] = [-2.33, 2.33]
        with self.assertRaisesRegex(ValueError, 'Encoding regression'):
            bindings.validate(self.rows)

    def test_missing_and_specials_cannot_become_numeric_zero(self):
        self.row('fao_di_annual_candidate')['decode']['special_values'].pop('254')
        with self.assertRaisesRegex(ValueError, 'Encoding regression'):
            bindings.validate(self.rows)

    def test_hansen_valid_land_mask_required(self):
        self.row('hansen_forest_loss_candidate')['decode']['guards'] = []
        with self.assertRaisesRegex(ValueError, 'Encoding regression'):
            bindings.validate(self.rows)

    def test_cumulative_emissions_not_silently_annualized(self):
        self.row('forest_gross_emissions_candidate')['decode']['scale'] = 1 / 24
        with self.assertRaisesRegex(ValueError, 'Encoding regression'):
            bindings.validate(self.rows)

    def test_cumulative_emissions_cannot_be_relabeled_annual(self):
        self.row('forest_gross_emissions_candidate')['unit'] = 'Mg_CO2e_per_ha_per_year'
        with self.assertRaisesRegex(ValueError, 'Encoding unit regression'):
            bindings.validate(self.rows)

    def test_iplc_cannot_be_scored_or_numerically_decoded(self):
        row = self.row('landmark_community_overlap_candidate')
        with self.assertRaisesRegex(ValueError, 'No inspected numeric contract'):
            bindings.inspect_numeric(row, 0)
        row['mcda_role'] = 'priority'
        with self.assertRaisesRegex(ValueError, 'current routing'):
            bindings.validate(self.rows)

    def test_no_acceptance_and_no_legacy_carbon_alias(self):
        self.row('forest_gross_emissions_candidate')['runtime_ready'] = True
        with self.assertRaisesRegex(ValueError, 'cannot accept or release'):
            bindings.validate(self.rows)
        self.row('forest_gross_emissions_candidate')['runtime_ready'] = False
        self.row('forest_gross_emissions_candidate')['variable_id'] = 'carbon_sequestration_potential'
        with self.assertRaisesRegex(ValueError, 'carbon alias'):
            bindings.validate(self.rows)

    def test_landmark_acquired_schema_and_unscored_presence(self):
        row = self.row('landmark_community_overlap_candidate')
        self.assertEqual(row['route'], 'approved_official_zip')
        self.assertEqual(row['selectors']['id_field'], 'landmark_i')
        self.assertEqual(row['selectors']['layer_filter'], ['Indigenous Lands', 'Community Lands'])
        self.assertEqual(row['selectors']['absence_policy'], 'unknown_without_independent_completeness_evidence')
        self.assertEqual(row['mcda_role'], 'descriptor')
        self.assertIsNone(row['decode'])

    def test_modified_pinned_observation_rejected(self):
        lock = json.loads((bindings.ROOT / 'evidence.lock.json').read_text())
        # Reproduce the pinned manifest shape without requiring a network or evidence checkout.
        entries = {r['observation_id']: r for row in self.rows for r in row['observation_refs']}
        manifest = json.dumps({'status': 'technical_observations_not_binding_acceptance', 'records': list(entries.values())}).encode()
        lock = copy.deepcopy(lock); lock['manifest_sha256'] = bindings.sha256(manifest).hexdigest()
        original_read = bindings.Path.read_text
        def read_text(path, *args, **kwargs):
            if path == bindings.ROOT / 'evidence.lock.json':
                return json.dumps(lock)
            return original_read(path, *args, **kwargs)
        with patch.object(bindings.Path, 'read_text', read_text), patch.object(bindings.subprocess, 'check_output', side_effect=[manifest, b'changed observation']):
            with self.assertRaisesRegex(ValueError, 'Observation hash mismatch'):
                bindings.check_evidence(self.rows, '/unused-fixture')

class RecurrenceTests(unittest.TestCase):
    def setUp(self):
        self.rows = {r['binding_id']: r for r in bindings.read_rows()}
        self.candidate = self.rows['fao_asi_recurrence_candidate']
        self.source = self.rows['fao_asi_annual_candidate']
        self.series = [{'year': y, 'value': 0} for y in range(1984, 2026)]

    def calculate(self, threshold=30):
        return bindings.inspect_recurrence(self.candidate, self.source, self.series, threshold)

    def test_strict_threshold_and_half_percent_preserved(self):
        self.series[0]['value'] = 30
        self.series[1]['value'] = 30.5
        self.assertEqual(self.calculate()['event_count'], 1)
        self.assertAlmostEqual(self.calculate()['value'], 100 / 42)

    def test_missing_year_not_shorter_denominator(self):
        self.series.pop()
        result = self.calculate()
        self.assertEqual(result['valid_seasons'], 41)
        self.assertEqual(result['state'], 'incomplete_series')
        self.assertIsNone(result['value'])

    def test_special_codes_not_drought_events(self):
        self.series[0]['value'] = 254
        self.assertEqual(self.calculate()['event_count'], 0)
        self.assertIsNone(self.calculate()['value'])

    def test_duplicate_year_rejected(self):
        self.series.append(self.series[0])
        with self.assertRaisesRegex(ValueError, 'Duplicate'):
            self.calculate()

    def test_arbitrary_event_cutoff_rejected(self):
        with self.assertRaisesRegex(ValueError, 'Unsupported'):
            self.calculate(25)

    def test_source_quantization_rejected(self):
        self.source['selectors']['pixelType'] = 'U8'
        with self.assertRaisesRegex(ValueError, 'float-preserving'):
            bindings.validate(list(self.rows.values()))

    def test_producer_zero_is_unknown(self):
        self.assertEqual(bindings.inspect_numeric(self.rows['forest_gross_emissions_2025_candidate'], 0),
                         {'state': 'unknown', 'value': None})
