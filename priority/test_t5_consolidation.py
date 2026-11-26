import copy
import csv
import json
import io
from pathlib import Path
import shutil
import tempfile
import unittest
import catalogue
import package
import t5_refs
import t5_review


class Consolidation(unittest.TestCase):
    def test_current_profiles_preserve_nineteen_ids_and_unscored_iplc(self):
        self.assertEqual(t5_refs.check(), {'rows':19,'priorities':14,'descriptors':5,'accepted_rules':0})
        self.assertEqual(t5_review.check()['candidate_findings'], 8)

    def test_release_route_blocks_iplc_and_unresolved_carbon_alias(self):
        root = catalogue.ROOT
        rows = list(csv.DictReader(io.StringIO((root / 'priority/T5_classification_refs.csv').read_text())))
        legacy = {r['variable_id']:r for r in csv.DictReader(io.StringIO((root / 'data-model/configuration/T5_opportunity_space.csv').read_text()))}
        directions = json.loads((root / 'priority/routing-directions.json').read_text())
        for variable, message in [('iplc_lands','Unscored descriptor'),('carbon_sequestration_potential','blocked pending')]:
            row = next(r for r in rows if r['variable_id'] == variable)
            rule = {'variables':[variable], 'concern_id':row['concern_id']}
            with self.assertRaisesRegex(ValueError,message): package.scoring_route(rule,legacy,rows,directions)
        with self.assertRaisesRegex(ValueError,'accepted release adapter'):
            package.scoring_route({'variables':['water_stress'],'concern_id':'water_stress'},legacy,rows,directions)
        package.scoring_route({'variables':['drought_hazard'],'concern_id':'drought'},legacy,rows,directions)
        with self.assertRaisesRegex(ValueError,'current concern'):
            package.scoring_route({'variables':['drought_hazard'],'concern_id':'different_quantity'},legacy,rows,directions)

    def test_routing_change_invalidates_previously_prepared_package(self):
        from test_package import Release
        from types import SimpleNamespace
        from unittest.mock import patch
        fixture = Release(); fixture.setUp(); self.addCleanup(fixture.doCleanups)
        revision, path, fetch = fixture.complete_fixture()
        with patch.object(package,'source_tool',return_value=SimpleNamespace(resolve=lambda *args: [])):
            payload = package.build(fixture.root,revision,revision,fixture.root,revision,[path],fetch)
            target = fixture.root / 'priority/T5_classification_refs.csv'
            target.write_text(target.read_text().replace(',priority,',',descriptor,'))
            fixture.git('add','.'); fixture.git('commit','-qm','Synthetic routing change')
            with self.assertRaisesRegex(ValueError,'dependency is stale'):
                package.verify(fixture.root,payload,fixture.head(),fixture.root,revision,fetch)

    def test_historical_findings_and_profiles_cannot_be_rewritten(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for directory in ['priority','data-model']:
                shutil.copytree(catalogue.ROOT / directory,root / directory)
            path = root / 'priority/history/t5-proposal/profiles/t5-0.1.0.json'
            path.write_bytes(path.read_bytes()+b'\n')
            with self.assertRaisesRegex(ValueError,'Preserved T5 proposal changed'): t5_refs.check(root)

    def test_catalogue_can_admit_future_proposal_with_current_routing_pins(self):
        from hashlib import sha256
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            for directory in ['priority','data-model']:
                shutil.copytree(catalogue.ROOT / directory,root / directory)
            original = root / 'priority/proposals/spei12_event-0.1.0.json'
            rule = json.loads(original.read_bytes()); rule['version'] = '0.2.0'
            rule['input_sha256'] = {name:sha256((root/name).read_bytes()).hexdigest() for name in package.DEFINITIONS}
            successor = root / 'priority/proposals/spei12_event-0.2.0.json'
            lock = {'repository':'RuralScan/evidence','revision':'f'*40,'status':'synthetic_unreviewed',
                    'files':{'workflows/priority_classification/batches/fixture/candidate.json':'e'*64}}
            source = rule['sources'][0]; source.update(revision=lock['revision'],path=next(iter(lock['files'])),sha256='e'*64)
            folder = root/'priority/source-locks';folder.mkdir();(folder/'fixture.json').write_text(json.dumps(lock))
            successor.write_text(json.dumps(rule))
            manifest = catalogue.check(root)
            self.assertEqual(len(manifest['proposals']),6)
            self.assertEqual(manifest['accepted_rules'],[])
            rule['input_sha256']['priority/routing-directions.json'] = '0'*64
            successor.write_text(json.dumps(rule))
            with self.assertRaisesRegex(ValueError,'Stale current rule dependencies'): catalogue.check(root)

    def test_candidate_reference_path_is_narrow_and_does_not_approve_it(self):
        rule = json.loads((catalogue.ROOT/'priority/proposals/spei12_event-0.1.0.json').read_text())
        rule['sources'][0]['path']='workflows/priority_classification/batches/t5-2026-11-25/candidate.json'
        catalogue.validate(rule)
        with self.assertRaises(ValueError): catalogue.eligible(rule,{})
        for path in ['workflows/priority_classification/batches/../candidate.json','arbitrary/candidate.json']:
            rule['sources'][0]['path']=path
            with self.assertRaisesRegex(ValueError,'Invalid packet path'): catalogue.validate(rule)


if __name__ == '__main__': unittest.main()
