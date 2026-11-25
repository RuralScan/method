"""Resolve the first T5 interpretation batch to pinned, unreviewed evidence candidates."""
import argparse
from hashlib import sha256
import json
from pathlib import Path
import re
from catalogue import ROOT, SCORES, digest, git_blob, require

VARIABLES = {'drought_hazard','water_stress','iplc_lands','carbon_sequestration_potential'}

def validate_review(review, lock, findings=None):
    require(set(review)=={'format','status','evidence_batch','records','accepted_rules'},'Invalid interpretation envelope')
    require(review['format']=='ruralscan.t5-interpretation-review.v1' and review['status']=='proposed_not_accepted' and review['accepted_rules']==[], 'No classification acceptance in this batch')
    ref=review['evidence_batch']
    require(set(ref)=={'repository','revision','path','sha256'} and ref['repository']==lock['repository'] and ref['revision']==lock['revision'] and ref['sha256']==lock['files'].get(ref['path']), 'Unpinned evidence batch')
    require(len(review['records'])==4 and {r['variable_id'] for r in review['records']}==VARIABLES,'First-batch coverage differs')
    for record in review['records']:
        require(set(record)=={'variable_id','proposal_ref','related_event_proposal','findings','status','interpretation','class_mapping','uncertainty','examples','next_decision','human_decision'},'Invalid interpretation fields')
        require(record['status']=='held' and record['human_decision'] is None,'Agent cannot record human acceptance')
        require(record['findings'] and record['interpretation'] and record['next_decision'],'Missing trace or interpretation')
        require(set(record['uncertainty'])=={'source','transfer','interpretation'} and all(record['uncertainty'].values()), 'Incomplete uncertainty')
        for finding in record['findings']:
            require(set(finding)=={'candidate_finding_id','version','sha256'} and finding['version']=='0.1.0' and re.fullmatch('[0-9a-f]{64}',finding['sha256']), 'Invalid candidate finding reference')
            if findings is not None:
                actual=findings.get(finding['candidate_finding_id'])
                require(actual is not None and digest(actual)==finding['sha256'] and record['variable_id'] in actual['variables'], 'Changed or incompatible finding')
        for mapping in record['class_mapping']:
            require(set(mapping)=={'source_class','proposed_class','score','scope'} and mapping['source_class'] and mapping['scope'], 'Invalid semantic mapping')
            target=mapping['proposed_class']
            if record['variable_id']=='drought_hazard':
                require(target in SCORES and type(mapping['score']) in (int,float) and mapping['score']==SCORES[target] and mapping['scope']=='event-only candidate; not T5 climatology','Wrong event mapping or score')
            else:require(target is None and mapping['score'] is None, 'Unresolved T5 interpretation cannot invent classes')
        require(record['examples'] and all(e['T5_class'] is None for e in record['examples']), 'Held T5 examples cannot score')


def check(evidence_repo=None, root=ROOT):
    lock=json.loads((root/'priority/t5-evidence.lock.json').read_text())
    require(set(lock)=={'repository','revision','status','files'} and lock['repository']=='RuralScan/evidence' and re.fullmatch('[0-9a-f]{40}',lock['revision']) and lock['status']=='unreviewed_candidates_not_canonical', 'Invalid evidence lock')
    require(lock['files'] and all(re.fullmatch('[0-9a-f]{64}',h) for h in lock['files'].values()),'Invalid dependency digests')
    review=json.loads((root/'priority/interpretations/t5-first-batch-0.1.0.json').read_text())
    findings=None
    if evidence_repo:
        for path,expected in lock['files'].items():
            require(not Path(path).is_absolute() and '..' not in Path(path).parts,'Unsafe evidence path')
            require(sha256(git_blob(evidence_repo,lock['revision'],path)).hexdigest()==expected,f'Stale evidence dependency: {path}')
        bundle=json.loads(git_blob(evidence_repo,lock['revision'],review['evidence_batch']['path']))
        require(bundle['status']=='unreviewed_candidate' and bundle['review_events']==[], 'Unexpected evidence disposition')
        findings={f['candidate_finding_id']:f for f in bundle['findings']}
    validate_review(review,lock,findings)
    for record in review['records']:
        for field in ['proposal_ref','related_event_proposal']:
            path=record[field]
            if path:
                require(re.fullmatch(r'priority/proposals/[a-z0-9_]+-[0-9.]+\.json',path),'Invalid rule path')
                rule=json.loads((root/path).read_text())
                require(record['variable_id'] in rule['variables'],'Rule does not describe this variable')
    return {'T5_variables':4,'candidate_findings':8,'accepted_rules':0,'pinned_evidence_checked':bool(evidence_repo)}

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--evidence-repo',type=Path);args=p.parse_args();print(json.dumps(check(args.evidence_repo),sort_keys=True))
