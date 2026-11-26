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


if __name__ == '__main__':unittest.main()
