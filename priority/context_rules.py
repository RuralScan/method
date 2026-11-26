"""Generate and inspect contextual classification tables; no runtime release or approval."""
import argparse
from bisect import bisect_left
import csv
from hashlib import sha256
import json
import math
from pathlib import Path
import re

from catalogue import ROOT, digest, finite, require

FOLDER = 'priority/classifications'


def read_table(root, manifest, name):
    spec = manifest['tables'][name]
    with (root / FOLDER / spec['file']).open(newline='') as stream:
        reader = csv.DictReader(stream)
        require(reader.fieldnames == spec['columns'], f'{name}: columns differ from manifest')
        rows = list(reader)
    require(all(None not in r and all(v is not None for v in r.values()) for r in rows), 'Malformed CSV')
    for row in rows:
        for key in spec.get('json_columns', []):
            row[key] = json.loads(row[key])
        for key in spec.get('number_columns', []):
            row[key] = float(row[key]) if row[key] else None
    return rows


def quantiles(values):
    ordered = sorted(values)
    def at(q):
        pos = (len(ordered) - 1) * q
        left = math.floor(pos)
        right = math.ceil(pos)
        return ordered[left] + (ordered[right] - ordered[left]) * (pos - left)
    return [at(1 / 3), at(2 / 3)]


def bundle(root=ROOT):
    folder = root / FOLDER
    manifest = json.loads((folder / 'columns.json').read_text())
    require(manifest['format'] == 'ruralscan.context-classification-tables.v1' and
            manifest['schema_issue'].startswith('https://github.com/RuralScan/method/issues/'), 'Untracked table structure')
    rules = read_table(root, manifest, 'rules')
    samples = read_table(root, manifest, 'samples')
    countries = read_table(root, manifest, 'countries')
    sources = read_table(root, manifest, 'sources')
    source_map = {s['source_id']: s for s in sources}
    require(len(source_map) == len(sources), 'Duplicate source ID')
    for source in sources:
        require(source['url'].startswith('https://') and source['locator'] and
                re.fullmatch('[0-9a-f]{64}', source['sha256']), 'Missing source provenance')
    membership = {(c['country_code'], c['vintage']): c for c in countries}
    require(len(membership) == len(countries), 'Duplicate country/vintage')
    for row in countries:
        require(re.fullmatch('[A-Z]{3}', row['country_code']) and row['income_group'] in {'LIC','LMC','UMC','HIC'}, 'Invalid country membership')
        require(row['source_id'] in source_map, 'Unresolved membership provenance')
    sample_keys = [(s['reference_sample_id'], s['area_id']) for s in samples]
    require(len(sample_keys) == len(set(sample_keys)), 'Duplicate reference observation')
    used_samples = set()
    selectors = set()
    identities = set()
    routes = {}
    with (root / 'priority/T5_classification_refs.csv').open() as stream:
        t5 = {r['variable_id']: r for r in csv.DictReader(stream)}
    for row in rules:
        require(re.fullmatch('[a-z][a-z0-9_]*', row['classification_id']) and
                re.fullmatch(r'\d+\.\d+\.\d+', row['version']), 'Invalid rule identity')
        identity = (row['classification_id'], row['version'])
        require(identity not in identities, 'Duplicate rule version')
        identities.add(identity)
        require(row['status'] == 'proposed', 'Context table cannot assert scientific acceptance')
        route = t5.get(row['variable_id'])
        require(route and route['mcda_role'] == 'priority' and route['concern_id'] == row['concern_id'], 'Context rule conflicts with T5 routing')
        require(route['classification_set_ref'] == f'{FOLDER}/rules.csv#{row["rule_set_id"]}', 'T5 does not link to rule set')
        previous = routes.setdefault(row['rule_set_id'], (row['variable_id'], row['concern_id']))
        require(previous == (row['variable_id'], row['concern_id']), 'Rule set crosses variable/concern identities')
        require(row['context_type'] in {'global', 'wb_income_group', 'region', 'country'}, 'Unsupported context type')
        selector = (row['rule_set_id'], row['context_type'], row['context_value'], row['context_vintage'])
        require(selector not in selectors, 'Ambiguous context selector')
        selectors.add(selector)
        require(row['reference_scope'] and row['rationale'] and row['reference_year'], 'Missing interpretation/context')
        require(row['context_value'] == 'global' if row['context_type'] == 'global' else bool(row['context_value']), 'Invalid context value')
        if row['context_type'] != 'global':
            dimension = {'wb_income_group':'income_group', 'region':'region', 'country':'country_code'}[row['context_type']]
            require(any(c['vintage'] == row['context_vintage'] and c[dimension] == row['context_value'] for c in countries), 'Unresolved context membership')
        require(row['unit'] and row['direction'] in {'higher_is_more_concern','lower_is_more_concern'}, 'Invalid units/direction')
        require(set(row['class_meanings']) == {'none','low','medium','high'} and
                all(isinstance(v,str) and v for v in row['class_meanings'].values()), 'Missing class meanings')
        require(row['source_ids'] and set(row['source_ids']) <= set(source_map), 'Unresolved rule sources')
        binding = row['binding']
        require(set(binding) == {'dataset_id','asset','field','source_unit','scale','offset','spatial_support','validation'}, 'Incomplete binding')
        require(all(binding[k] for k in ('dataset_id','asset','field','source_unit','spatial_support')), 'Missing binding identity')
        require(binding['validation'] in {'table_inspected','documentation_only'} and finite(binding['scale']) and binding['scale'] > 0 and finite(binding['offset']), 'Invalid binding conversion/status')
        lo, hi = row['domain_min'], row['domain_max']
        require(finite(lo) and (hi is None or finite(hi) and lo < hi), 'Invalid classification domain')
        require(row['method'] in {'terciles','thresholds'}, 'Invalid classification method')
        cuts = [row['low_upper'], row['medium_upper']]
        if row['method'] == 'thresholds':
            cuts.insert(0, row['none_upper'])
            require(not row['reference_sample_id'], 'Threshold rule cannot fit reference sample')
            row['reference_sample'] = None
        else:
            require(row['none_upper'] is None, 'Terciles cannot invent a none/very-little band')
            selected = [s for s in samples if s['reference_sample_id'] == row['reference_sample_id']]
            require(len(selected) >= 3, 'Missing reference sample')
            used_samples.add(row['reference_sample_id'])
            for s in selected:
                require(finite(s['value']) and s['value'] >= lo and (hi is None or s['value'] <= hi), 'Sample outside domain')
                country = membership.get((s['country_code'], row['context_vintage']))
                require(country is not None, 'Sample country missing from pinned membership')
                require(row['context_type'] != 'wb_income_group' or country['income_group'] == row['context_value'], 'Reference sample mixes income groups')
                require(s['reference_year'] == row['reference_year'], 'Reference sample mixes periods')
            values = [s['value'] for s in selected]
            require(cuts == quantiles(values), 'Cutoffs differ from reference terciles')
            row['reference_sample'] = {'n':len(selected), 'countries':len({s['country_code'] for s in selected}),
                'sha256':digest(selected), 'algorithm':'linear_n_minus_1', 'weighting':'equal_source_area', 'none_condition':None}
        require(all(finite(v) for v in cuts) and all(a < b for a, b in zip(cuts, cuts[1:])), 'Invalid class boundaries')
        require(cuts[0] >= lo and (hi is None or cuts[-1] <= hi), 'Cutoff outside domain')
        row['cuts'] = cuts
        row['missing'] = 'unknown'
        row['endpoint'] = 'upper_inclusive'
        row['runtime_ready'] = False
    require(used_samples == {s['reference_sample_id'] for s in samples}, 'Unreferenced sample observations')
    for route in t5.values():
        reference = route['classification_set_ref']
        if reference:
            require(reference.startswith(f'{FOLDER}/rules.csv#') and reference.split('#',1)[1] in routes, 'Unresolved classification set')
            require(not route['proposed_rule_ref'] and not route['accepted_rule_ref'], 'Single rule and contextual set conflict')
    return {'format':'ruralscan.context-classification-review.v1', 'runtime_ready':False,
        'input_sha256':{f'{FOLDER}/{name}':sha256((folder/name).read_bytes()).hexdigest()
                        for name in ['columns.json'] + [s['file'] for s in manifest['tables'].values()]},
        'rules':rules, 'countries':countries, 'sources':sources}


def check(root=ROOT):
    actual = bundle(root)
    require(json.loads((root / FOLDER / 'rules.json').read_text()) == actual, 'Stale generated contextual rules')
    return actual


def resolve(variable, country_code=None, *, vintage, region=None, for_runtime=False, root=ROOT):
    """Resolve one review rule; explicit country > region > income tier > global."""
    require(not for_runtime, 'Context rules are not an accepted runtime release')
    data = check(root)
    rules = [r for r in data['rules'] if r['variable_id'] == variable]
    require(rules, 'No contextual rule set for variable')
    membership = [c for c in data['countries'] if c['country_code'] == country_code and c['vintage'] == vintage]
    if country_code is not None:
        require(len(membership) == 1, 'Unknown country or income-group vintage')
    country = membership[0] if membership else None
    if region is not None:
        require(country and region == country['region'], 'Region conflicts with pinned country membership')
    dimensions = {'global':'global'}
    if country:
        dimensions.update(country=country_code, region=country['region'], wb_income_group=country['income_group'])
    matches = [r for r in rules if r['context_value'] == dimensions.get(r['context_type']) and
               (r['context_type'] == 'global' or r['context_vintage'] == vintage)]
    require(matches, 'No rule for this context; no automatic fallback to another income group')
    rank = {'global':0,'wb_income_group':1,'region':2,'country':3}
    best = max(rank[r['context_type']] for r in matches)
    matches = [r for r in matches if rank[r['context_type']] == best]
    require(len(matches) == 1, 'Ambiguous contextual rules')
    return matches[0]


def preview(rule, value, *, unit):
    """Inspect already converted scalar values in the table's declared units."""
    require(unit == rule['unit'], 'Input units differ; convert explicitly')
    if value is None or not finite(value):
        return None
    if value < rule['domain_min'] or (rule['domain_max'] is not None and value > rule['domain_max']):
        return None
    labels = ['low','medium','high'] if rule['method'] == 'terciles' else ['none','low','medium','high']
    if rule['direction'] == 'lower_is_more_concern':
        labels.reverse()
    return labels[bisect_left(rule['cuts'], value)]


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['generate','check'])
    args = parser.parse_args()
    if args.command == 'generate':
        (ROOT / FOLDER / 'rules.json').write_text(json.dumps(bundle(), indent=2, ensure_ascii=False) + '\n')
    data = check()
    print(f'{len(data["rules"])} contextual rules; 0 accepted runtime rules')
