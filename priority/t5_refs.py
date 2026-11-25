"""Validate the proposed T5 extension. No accepted rule or runtime activation."""
import csv
from hashlib import sha256
import json
from pathlib import Path
from catalogue import ROOT, digest, require

COLUMNS = ['variable_id', 'mcda_role', 'concern_id', 'profile_ref',
           'proposed_rule_ref', 'accepted_rule_ref', 'classification_status']
PROFILE_FIELDS = {'quantity', 'unit', 'temporal_statistic', 'spatial_support', 'context',
                  'binding_candidates', 'binding_status', 'uncertainty', 'missing', 'blockers'}

def read_csv(path):
    with path.open(newline='') as stream:
        reader = csv.DictReader(stream)
        return reader.fieldnames, list(reader)


def validate_rows(rows, profiles, legacy, bindings, rules, directions):
    expected = {r['variable_id']: r for r in legacy}
    require(len(rows) == len(expected) and {r['variable_id'] for r in rows} == set(expected),
            'T5 extension must preserve every historical ID exactly once')
    require(set(profiles) == set(expected), 'Profile coverage differs from T5')
    binding_by_id = {b['binding_id']: b for b in bindings}
    for row in rows:
        require(set(row) == set(COLUMNS), 'Unexpected T5 extension columns')
        variable = row['variable_id']; profile = profiles[variable]
        override = directions['role_overrides'].get(variable)
        if override:
            require(override['historical_role'] == expected[variable]['mcda_role'], 'Role override lost historical trace')
        role = override['effective_role'] if override else expected[variable]['mcda_role']
        require(row['mcda_role'] == role, 'Role differs from explicit routing direction')
        require(row['concern_id'] and row['profile_ref'] == f'priority/profiles/t5-0.2.0.json#{variable}', 'Missing concern or invalid profile reference')
        require(row['accepted_rule_ref'] == '', 'This extension has no accepted release adapter')
        descriptor = row['mcda_role'] == 'descriptor'
        require(row['classification_status'] == ('descriptor' if descriptor else 'held'), 'Cannot assert readiness')
        require(not descriptor or row['proposed_rule_ref'] == '', 'Descriptor cannot carry a scoring proposal')
        if row['proposed_rule_ref']:
            require(row['proposed_rule_ref'] in rules, 'Unresolved proposed rule')
            rule = rules[row['proposed_rule_ref']]
            require(variable in rule['variables'] and rule['concern_id'] == row['concern_id'] and rule['role'] == 'priority', 'Rule/variable/concern mismatch')
        require(set(profile) == PROFILE_FIELDS, 'Unexpected profile fields')
        for key in ('quantity', 'unit', 'temporal_statistic', 'spatial_support'):
            require(isinstance(profile[key], str) and profile[key].strip(), f'Missing {key}')
        require(profile['missing'] == 'unknown' and profile['binding_status'] == 'unverified', 'Premature binding validation or changed missing policy')
        require(profile['blockers'] and all(isinstance(b,str) and b for b in profile['blockers']), 'Unresolved profiles need blockers')
        require(profile['context'] == {'geography': None, 'period': None, 'scenario': 'baseline', 'purpose': 'method_review_only_not_pilot'}, 'No context accepted in this version')
        require(set(profile['uncertainty']) == {'source', 'transfer', 'interpretation'} and all(profile['uncertainty'].values()), 'Incomplete uncertainty')
        candidates = profile['binding_candidates']
        require(isinstance(candidates,list), 'Invalid binding candidate list')
        ids = [b['binding_id'] for b in candidates]
        require(len(ids) == len(set(ids)), 'Duplicate binding candidate')
        require(set(ids) == {b['binding_id'] for b in bindings if b['variable'] == variable}, 'Binding audit omits or invents candidates')
        for candidate in candidates:
            require(set(candidate) == {'binding_id','dataset_id','record_sha256'}, 'Invalid binding reference')
            actual = binding_by_id[candidate['binding_id']]
            require(actual['variable'] == variable and actual['dataset_id'] == candidate['dataset_id'] and digest(actual) == candidate['record_sha256'], 'Stale or mismatched binding')


def check(root=ROOT):
    manifest = json.loads((root/'priority/t5-structure.json').read_text())
    require(manifest['format'] == 'ruralscan.t5-extension-manifest.v1' and manifest['status'] == 'proposed_not_accepted', 'Unexpected manifest')
    require(manifest['activation'] == 'disabled' and manifest['accepted_rules'] == [], 'No production activation permitted')
    require(manifest['columns'] == COLUMNS and set(manifest['profile_fields']) == PROFILE_FIELDS, 'Changed frozen structure')
    require(manifest['readiness_states'] == ['held','descriptor'], 'Changed lifecycle')
    require(manifest['table'] == 'priority/T5_classification_refs.csv' and manifest['primary_key'] == 'variable_id' and manifest['profile_file'] == 'priority/profiles/t5-0.2.0.json', 'Unexpected store')
    expected_deps = {'data-model/configuration/'+f for f in ['T5_opportunity_space.csv','T1_data_registry.csv','VONT_variable_ontology.csv','BIND_dataset_binding.csv']} | {'data-model/priority-contract.json', 'priority/routing-directions.json'}
    require(set(manifest['dependencies']) == expected_deps, 'Missing dependency pin')
    for path, expected in manifest['dependencies'].items():
        require(sha256((root/path).read_bytes()).hexdigest() == expected, f'Stale dependency: {path}')
    header, rows = read_csv(root/manifest['table'])
    require(header == COLUMNS, 'CSV structure differs from manifest')
    bundle = json.loads((root/manifest['profile_file']).read_text())
    require(set(bundle) == {'format','version','status','profiles'} and bundle['format'] == 'ruralscan.t5-profiles.v1' and bundle['version'] == '0.2.0' and bundle['status'] == 'proposed_not_accepted', 'Unexpected profile bundle')
    _, legacy = read_csv(root/'data-model/configuration/T5_opportunity_space.csv')
    _, bindings = read_csv(root/'data-model/configuration/BIND_dataset_binding.csv')
    rules = {str(p.relative_to(root)):json.loads(p.read_text()) for p in (root/'priority/proposals').glob('*.json')}
    directions = json.loads((root/'priority/routing-directions.json').read_text())
    require(directions['human_classification_acceptance'] is False, 'Routing instruction cannot accept a classification')
    validate_rows(rows, bundle['profiles'], legacy, bindings, rules, directions)
    preserved = json.loads((root/'priority/consolidation.json').read_text())
    for item in preserved['files']:
        require(sha256((root/item['preserved_path']).read_bytes()).hexdigest() == item['sha256'], 'Preserved T5 proposal changed')
    return {'rows':len(rows), 'priorities':sum(r['mcda_role']=='priority' for r in rows), 'descriptors':sum(r['mcda_role']=='descriptor' for r in rows), 'accepted_rules':0}

if __name__ == '__main__':
    print(json.dumps(check(), sort_keys=True))
