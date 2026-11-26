import copy
import csv
import json
import math
from pathlib import Path
import shutil
import tempfile
import unittest

import context_rules as rules
import package
import t5_refs


class ContextRules(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name in ['priority', 'data-model']:
            shutil.copytree(rules.ROOT / name, self.root / name)

    def read(self, filename):
        with (self.root / rules.FOLDER / filename).open() as f:
            return list(csv.DictReader(f))

    def write(self, filename, rows):
        with (self.root / rules.FOLDER / filename).open('w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader(); writer.writerows(rows)

    def generate(self):
        data = rules.bundle(self.root)
        (self.root / rules.FOLDER / 'rules.json').write_text(json.dumps(data))
        return data

    def resolve(self, country, **kwargs):
        return rules.resolve('rural_poverty',country,vintage='FY2027',root=self.root,**kwargs)

    def test_three_tiers_and_reference_replay(self):
        expected = {'UGA':('LIC',339,19), 'KEN':('LMC',525,43), 'COL':('UMC',745,43)}
        for country, (group, n, countries) in expected.items():
            rule = self.resolve(country)
            self.assertEqual(rule['context_value'],group)
            self.assertEqual(rule['reference_sample']['n'],n)
            self.assertEqual(rule['reference_sample']['countries'],countries)
            self.assertEqual(rule['reference_scope'],'global_within_income_group')
            self.assertFalse(rule['runtime_ready'])
        self.assertEqual(t5_refs.check(self.root)['rows'],19)

    def test_no_cross_group_fallback_or_unpinned_vintage(self):
        for country in ['USA','XXX',None]:
            with self.assertRaises(ValueError):self.resolve(country)
        with self.assertRaisesRegex(ValueError,'vintage'):
            rules.resolve('rural_poverty','KEN',vintage='FY2026',root=self.root)
        with self.assertRaisesRegex(ValueError,'Region conflicts'):
            self.resolve('KEN',region='Europe & Central Asia')
        with self.assertRaisesRegex(ValueError,'not an accepted runtime release'):
            self.resolve('KEN',for_runtime=True)

    def test_boundaries_units_zero_missing_and_domain(self):
        rule = self.resolve('KEN')
        first, second = rule['cuts']
        for value, expected in [(0,'low'),(first,'low'),(math.nextafter(first,math.inf),'medium'),
                                (second,'medium'),(math.nextafter(second,math.inf),'high'),(100,'high'),
                                (-1,None),(101,None),(None,None),(float('nan'),None)]:
            self.assertEqual(rules.preview(rule,value,unit='percent'),expected)
        with self.assertRaisesRegex(ValueError,'units differ'):rules.preview(rule,.5,unit='fraction')

    def test_duplicate_context_and_mixed_reference_are_rejected(self):
        rows = self.read('rules.csv'); duplicate = copy.deepcopy(rows[0]);duplicate['classification_id']='other'
        self.write('rules.csv',rows+[duplicate])
        with self.assertRaisesRegex(ValueError,'Ambiguous context'):rules.bundle(self.root)
        self.write('rules.csv',rows)
        samples = self.read('reference_samples.csv');samples[0]['country_code']='COL'
        self.write('reference_samples.csv',samples)
        with self.assertRaisesRegex(ValueError,'mixes income groups'):rules.bundle(self.root)

    def test_stale_cuts_and_generated_content_are_rejected(self):
        rows=self.read('rules.csv');rows[0]['medium_upper']='99'
        self.write('rules.csv',rows)
        with self.assertRaisesRegex(ValueError,'differ from reference'):rules.bundle(self.root)
        path=self.root/rules.FOLDER/'rules.json'
        data=json.loads(path.read_text());data['runtime_ready']=True;path.write_text(json.dumps(data))
        shutil.copy2(rules.ROOT/rules.FOLDER/'rules.csv',self.root/rules.FOLDER/'rules.csv')
        with self.assertRaisesRegex(ValueError,'Stale generated'):rules.check(self.root)

    def test_explicit_country_override_wins_without_changing_other_countries(self):
        rows=self.read('rules.csv'); override=copy.deepcopy(rows[0])
        override.update(classification_id='poverty_country_example',context_type='country',context_value='KEN',
            method='thresholds',none_upper='0',low_upper='10',medium_upper='30',reference_sample_id='',
            rationale='Synthetic test only: explicit contextual justification')
        self.write('rules.csv',rows+[override]);self.generate()
        self.assertEqual(self.resolve('KEN')['classification_id'],'poverty_country_example')
        self.assertEqual(self.resolve('BGD')['context_value'],'LMC')

    def test_contextual_rules_cannot_bypass_existing_release_route(self):
        root=self.root
        with (root/'priority/T5_classification_refs.csv').open() as f:routing=list(csv.DictReader(f))
        with (root/'data-model/configuration/T5_opportunity_space.csv').open() as f:legacy={r['variable_id']:r for r in csv.DictReader(f)}
        directions=json.loads((root/'priority/routing-directions.json').read_text())
        with self.assertRaisesRegex(ValueError,'accepted release adapter'):
            package.scoring_route({'variables':['rural_poverty'],'concern_id':'rural_poverty'},legacy,routing,directions)

    def test_soil_global_thresholds_preserve_published_bands_and_domain(self):
        rule=rules.resolve('soil_erosion_risk',vintage='FY2027',root=self.root)
        self.assertEqual(rule['cuts'],[1,3,5])
        self.assertEqual(rule['binding']['validation'],'documentation_only')
        self.assertIn('Very little',rule['class_meanings']['none'])
        for value,expected in [(0,'none'),(1,'none'),(1.001,'low'),(3,'low'),(3.001,'medium'),
                               (5,'medium'),(5.001,'high'),(-1,None),(None,None)]:
            self.assertEqual(rules.preview(rule,value,unit='tonnes_per_ha_per_year'),expected)

    def test_water_stress_uses_native_categories_and_retains_flags(self):
        rule=rules.resolve('water_stress',vintage='FY2027',root=self.root)
        for raw,category,expected,state in [(.05,0,'none','numeric'),(.15,1,'low','numeric'),
                (.3,2,'medium','numeric'),(.6,3,'high','numeric'),(2,4,'high','numeric'),
                (1,-1,'high','arid_low_use'),(9999,4,'high','physical_scarcity')]:
            result=rules.preview_category_record(rule,raw,category)
            self.assertEqual((result['class'],result['state']),(expected,state))
            self.assertEqual((result['raw'],result['category']),(raw,category))
        # Provider category settles equality; no reclassification of rounded ratios.
        self.assertEqual(rules.preview_category_record(rule,.1,0)['class'],'none')
        self.assertEqual(rules.preview_category_record(rule,.1,1)['class'],'low')
        with self.assertRaisesRegex(ValueError,'raw value and category together'):
            rules.preview(rule,0,unit='provider_category')

    def test_water_missing_and_invalid_inputs_never_become_low_stress(self):
        rule=rules.resolve('water_stress',vintage='FY2027',root=self.root)
        for raw,category in [(None,0),(None,-1),(-9999,-1),(-9999,0),(-2,-1),
                (float('nan'),1),(float('inf'),4),(.2,None),(.2,-9999),(.2,9),(.2,1.5),(.2,False)]:
            self.assertIsNone(rules.preview_category_record(rule,raw,category)['class'])

    def test_category_structure_and_binding_changes_are_checked(self):
        rows=self.read('rules.csv');water=next(r for r in rows if r['method']=='categories')
        water['none_upper']='.1';self.write('rules.csv',rows)
        with self.assertRaisesRegex(ValueError,'cannot carry numeric'):rules.bundle(self.root)
        water['none_upper']='';mapping=json.loads(water['category_map']);del mapping['-1']
        water['category_map']=json.dumps(mapping);self.write('rules.csv',rows)
        with self.assertRaisesRegex(ValueError,'must cover declared'):rules.bundle(self.root)
        shutil.copy2(rules.ROOT/rules.FOLDER/'rules.csv',self.root/rules.FOLDER/'rules.csv')
        path=self.root/'priority/bindings/candidates.csv'
        with path.open() as f:
            reader=csv.DictReader(f);fields=reader.fieldnames;candidates=list(reader)
        selected=next(c for c in candidates if c['binding_id']=='aqueduct_bws_annual_candidate')
        selected['documentation']=json.dumps(['Changed source context'])
        with path.open('w',newline='') as f:
            writer=csv.DictWriter(f,fieldnames=fields);writer.writeheader();writer.writerows(candidates)
        with self.assertRaisesRegex(ValueError,'Stale generated'):rules.check(self.root)

    def test_food_levels_require_available_applicable_assessment(self):
        rule=rules.resolve('food_insecurity',vintage='FY2027',root=self.root)
        self.assertIsNone(rule['binding_candidate'])
        self.assertFalse(rule['runtime_ready'])
        for level,label in [(1,'none'),(2,'low'),(3,'medium'),(4,'high')]:
            self.assertIsNone(rules.preview_documented_category(rule,level,unit='ipc_chronic_area_level'))
            self.assertIsNone(rules.preview_documented_category(rule,level,unit='ipc_chronic_area_level',assessment_available=True))
            self.assertIsNone(rules.preview_documented_category(rule,level,unit='ipc_chronic_area_level',assessment_applicable=True))
            self.assertEqual(rules.preview_documented_category(rule,level,unit='ipc_chronic_area_level',
                assessment_available=True,assessment_applicable=True),label)
        for value in [None,0,5,-9999,2.5,True,float('nan')]:
            self.assertIsNone(rules.preview_documented_category(rule,value,unit='ipc_chronic_area_level',
                assessment_available=True,assessment_applicable=True))
        with self.assertRaisesRegex(ValueError,'do not substitute'):
            rules.preview_documented_category(rule,2,unit='ipc_acute_phase',assessment_available=True,assessment_applicable=True)
        with self.assertRaisesRegex(ValueError,'local assessment'):
            rules.preview_category_record(rule,2,2)

    def test_food_placeholder_cannot_claim_inspected_binding(self):
        rows=self.read('rules.csv');food=next(r for r in rows if r['variable_id']=='food_insecurity')
        binding=json.loads(food['binding']);binding['validation']='table_inspected';food['binding']=json.dumps(binding)
        self.write('rules.csv',rows)
        with self.assertRaisesRegex(ValueError,'Unresolved category input'):rules.bundle(self.root)
        binding['validation']='requires_local_assessment';food['binding']=json.dumps(binding)
        mapping=json.loads(food['category_map']);mapping['5']='high';food['category_map']=json.dumps(mapping)
        self.write('rules.csv',rows)
        with self.assertRaisesRegex(ValueError,'declared domain exactly'):rules.bundle(self.root)


if __name__ == '__main__':unittest.main()
