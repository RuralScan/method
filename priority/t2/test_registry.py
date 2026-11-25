"""Guard the migration boundary: identity survives; unverified inputs cannot run."""
import csv
import json
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

import registry


class RegistryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for path in ['priority/t2', 'data-model/configuration']:
            shutil.copytree(registry.ROOT / path, self.root / path)
        shutil.copy2(registry.ROOT / 'data-model/priority-contract.json', self.root / 'data-model')

    def mutate(self, callback):
        path = self.root / 'priority/t2/variables.csv'
        with path.open(newline='') as f:
            reader = csv.DictReader(f)
            fields, rows = reader.fieldnames, list(reader)
        callback(rows)
        with path.open('w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=fields, lineterminator='\n')
            writer.writeheader()
            writer.writerows(rows)

    def test_original_revision_and_ids_survive(self):
        rows, schema, migration = registry.read(self.root)
        pinned = subprocess.check_output(['git', 'show', migration['source']['revision'] + ':' + registry.SOURCE], cwd=registry.ROOT)
        self.assertEqual(registry.digest(pinned), migration['source']['sha256'])
        self.assertEqual(len(rows), 11)
        self.assertEqual({r['variable_id'] for r in rows}, {r['variable_id'] for r in migration['original_rows']})
        forbidden = {'weight_default', 'normalisation_method', 'use_in_simplified_mode', 'use_in_advanced_mode'}
        self.assertFalse(forbidden & set(schema['fields']))
        self.assertTrue(forbidden <= set(migration['field_dispositions']))
        self.assertEqual(registry.check(self.root)['runnable_variables'], 0)

    def test_lost_and_duplicate_ids_fail(self):
        for change in [lambda rows: rows.pop(), lambda rows: rows.__setitem__(1, rows[0])]:
            with self.subTest(change=change):
                shutil.copy2(registry.HERE / 'variables.csv', self.root / 'priority/t2')
                self.mutate(change)
                with self.assertRaises(ValueError):
                    registry.read(self.root)

    def test_historical_file_cannot_be_rewritten(self):
        path = self.root / registry.SOURCE
        path.write_text(path.read_text() + '\n')
        with self.assertRaisesRegex(ValueError, 'Historical T2 CSV changed'):
            registry.read(self.root)

    def test_no_silent_promotion_or_bad_roles(self):
        values = {'dataset_id': 'spei_global_v26', 'classification_id': 'unapproved',
                  'classification_version': '1.0.0', 'readiness': 'ready',
                  'binding_status': 'verified', 'classification_status': 'accepted',
                  'mcda_role': 'hazard', 'reference_period': '1991-2020', 'context_id': 'global'}
        for field, value in values.items():
            with self.subTest(field=field):
                shutil.copy2(registry.HERE / 'variables.csv', self.root / 'priority/t2')
                self.mutate(lambda rows: rows[0].__setitem__(field, value))
                with self.assertRaises(ValueError):
                    registry.read(self.root)

    def test_candidate_or_scenario_change_requires_new_migration(self):
        for field, value in [('candidate_dataset_id', 'chelsa_bioclim_v21_baseline'), ('scenario_type', 'future_ssp245')]:
            with self.subTest(field=field):
                shutil.copy2(registry.HERE / 'variables.csv', self.root / 'priority/t2')
                self.mutate(lambda rows: rows[0].__setitem__(field, value))
                with self.assertRaises(ValueError):
                    registry.read(self.root)

    def test_manifest_detects_changed_content(self):
        self.mutate(lambda rows: rows[0].__setitem__('blockers', 'Changed scientific interpretation'))
        with self.assertRaisesRegex(ValueError, 'Stale T2 manifest'):
            registry.check(self.root)

    def test_manifest_detects_changed_policy(self):
        p = self.root / 'data-model/priority-contract.json'
        p.write_text(p.read_text() + '\n')
        with self.assertRaisesRegex(ValueError, 'Stale T2 manifest'):
            registry.check(self.root)

    def test_descriptors_and_operational_inputs_stay_outside_priority(self):
        rows = {r['variable_id']: r for r in registry.read(self.root)[0]}
        for identity in ['agricultural_cropland_exposure', 'population_exposure_rural',
                         'soil_degradation_sensitivity', 'soil_permeability_sensitivity']:
            self.assertEqual(rows[identity]['mcda_role'], 'descriptor')
        self.assertEqual(rows['adaptive_capacity_road_access']['mcda_role'], 'investment_risk')
        self.assertEqual(rows['drought_spei12_baseline']['concern_id'], rows['drought_spei12_ssp245_2050']['concern_id'])


if __name__ == '__main__':
    unittest.main()
