import copy
import json
import unittest
from t5_review import ROOT, check, validate_review
class T5Review(unittest.TestCase):
    def setUp(self):
        self.review=json.loads((ROOT/'priority/interpretations/t5-first-batch-0.1.0.json').read_text());self.lock=json.loads((ROOT/'priority/t5-evidence.lock.json').read_text())
    def test_all_four_t5_variables_remain_held(self):self.assertEqual(check()['accepted_rules'],0)
    def test_provider_bands_cannot_be_silently_scored(self):
        water=next(r for r in self.review['records'] if r['variable_id']=='water_stress');water['class_mapping'][0].update(proposed_class='none',score=0)
        with self.assertRaises(ValueError):validate_review(self.review,self.lock)
    def test_unmapped_not_none(self):
        r=next(r for r in self.review['records'] if r['variable_id']=='iplc_lands');r['examples'][0]['T5_class']='none'
        with self.assertRaises(ValueError):validate_review(self.review,self.lock)
    def test_source_finding_identity_required(self):
        with self.assertRaises(ValueError):validate_review(self.review,self.lock,{})
    def test_classification_acceptance_not_source_acceptance(self):
        self.review['records'][0]['human_decision']='keep'
        with self.assertRaises(ValueError):validate_review(self.review,self.lock)
    def test_event_score_contract_fixed(self):
        self.review['records'][0]['class_mapping'][1]['score']=.67
        with self.assertRaises(ValueError):validate_review(self.review,self.lock)
if __name__=='__main__':unittest.main()
