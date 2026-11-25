import copy
import json
import unittest
from t5_refs import ROOT, check, read_csv, validate_rows

class T5References(unittest.TestCase):
    def setUp(self):
        self.rows=read_csv(ROOT/'priority/T5_classification_refs.csv')[1]
        self.profiles=json.loads((ROOT/'priority/profiles/t5-0.1.0.json').read_text())['profiles']
        self.legacy=read_csv(ROOT/'data-model/configuration/T5_opportunity_space.csv')[1]
        self.bindings=read_csv(ROOT/'data-model/configuration/BIND_dataset_binding.csv')[1]
        self.rules={str(p.relative_to(ROOT)):json.loads(p.read_text()) for p in (ROOT/'priority/proposals').glob('*.json')}
    def validate(self): validate_rows(self.rows,self.profiles,self.legacy,self.bindings,self.rules)
    def test_coverage_and_no_activation(self):
        self.assertEqual(check(), {'rows':19,'priorities':15,'descriptors':4,'accepted_rules':0})
    def test_duplicate_or_missing_id(self):
        self.rows[-1]=copy.deepcopy(self.rows[0])
        with self.assertRaises(ValueError): self.validate()
    def test_descriptor_cannot_score(self):
        row=next(r for r in self.rows if r['mcda_role']=='descriptor')
        row['proposed_rule_ref']='priority/proposals/spei12_event-0.1.0.json'
        with self.assertRaises(ValueError): self.validate()
    def test_no_asserted_acceptance(self):
        self.rows[0]['accepted_rule_ref']='priority/releases/fake.json'
        with self.assertRaises(ValueError): self.validate()
    def test_wrong_quantity_proposal_cannot_activate_drought(self):
        self.rows[0]['classification_status']='accepted'
        with self.assertRaises(ValueError): self.validate()
    def test_stale_binding_needs_review(self):
        self.profiles['water_stress']['binding_candidates'][0]['record_sha256']='0'*64
        with self.assertRaises(ValueError): self.validate()
    def test_missing_is_not_none(self):
        self.profiles['water_stress']['missing']='none'
        with self.assertRaises(ValueError): self.validate()
    def test_old_weights_are_not_current_fields(self):
        self.rows[0]['weight_default']='0.33'
        with self.assertRaises(ValueError): self.validate()
    def test_no_fabricated_binding(self):
        self.profiles['food_insecurity']['binding_candidates']=[{'binding_id':'invented','dataset_id':'imaginary','record_sha256':'0'*64}]
        with self.assertRaises(ValueError): self.validate()

if __name__ == '__main__': unittest.main()
