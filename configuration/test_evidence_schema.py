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
