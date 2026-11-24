"""Keep the additive classification contract and schema vocabulary in agreement."""
import hashlib
import json
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]


class EvidenceClassificationSchema(unittest.TestCase):
    def test_manifest_and_snapshot_match_contract(self):
        contract = json.loads((ROOT / 'data-model/evidence-classification.json').read_text())
        manifest = json.loads((ROOT / 'data-model/structure/columns.json').read_text())['tables']['EV']
        snapshot = json.loads((ROOT / 'data-model/definition-snapshot.json').read_text())
        for field, spec in contract['fields'].items():
            self.assertIn(field, manifest['optional'])
            self.assertEqual(manifest['enum_values'][field], spec['values'])
        for name in ('spec.md', 'structure/columns.json', 'evidence-classification.json'):
            relative = 'data-model/' + name
            self.assertEqual(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(), snapshot['sha256'][relative])

    def test_legacy_format_never_implies_scientific_basis(self):
        contract = json.loads((ROOT / 'data-model/evidence-classification.json').read_text())
        for old, fmt in [('table', 'table'), ('figure_read', 'figure')]:
            self.assertEqual(contract['legacy_mapping'][old], {'knowledge_basis': 'unknown', 'extraction_format': fmt})
        self.assertNotIn('table', contract['fields']['knowledge_basis']['values'])
        self.assertNotIn('expert_assertion', contract['fields']['extraction_format']['values'])


class AgentEffectsSchema(unittest.TestCase):
    def test_contract_vocabulary_and_snapshot_match(self):
        contract = json.loads((ROOT / 'data-model/agent-effects-contract.json').read_text())
        manifest = json.loads((ROOT / 'data-model/structure/columns.json').read_text())
        snapshot = json.loads((ROOT / 'data-model/definition-snapshot.json').read_text())
        for table, spec in contract['tables'].items():
            self.assertEqual(spec['enum_values'], manifest['tables'][table]['enum_values'])
            self.assertEqual(spec['required'], manifest['tables'][table]['required'])
            self.assertIn('conflicting_evidence', spec['enum_values']['mitigation_potential' if table == 'T3' else 'effect_direction'])
        path = 'data-model/agent-effects-contract.json'
        self.assertEqual(hashlib.sha256((ROOT / path).read_bytes()).hexdigest(), snapshot['sha256'][path])


class PrioritySchema(unittest.TestCase):
    def test_contract_is_in_definition_snapshot(self):
        relative = 'data-model/priority-contract.json'
        snapshot = json.loads((ROOT / 'data-model/definition-snapshot.json').read_text())
        self.assertEqual(hashlib.sha256((ROOT / relative).read_bytes()).hexdigest(),
                         snapshot['sha256'][relative])
        contract = json.loads((ROOT / relative).read_text())
        spec = (ROOT / 'data-model/spec.md').read_text()
        for table in ('T2', 'T5'):
            section = spec.split('## ' + table + ' —', 1)[1].split('\n## ', 1)[0]
            for field in contract['table_fields'][table]['fields']:
                self.assertIn('`' + field + '`', section)
