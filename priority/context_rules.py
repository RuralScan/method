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
    require(manifest['format'] == 'ruralscan.context-classification-tables.v3' and
            manifest['schema_issue'].startswith('https://github.com/RuralScan/method/issues/'), 'Untracked table structure')
    core_rules = read_table(root, manifest, 'rules')
    supplementary_rules = read_table(root, manifest, 'supplementary_rules')
    visual_variables = read_table(root, manifest, 'visual_variables')
    visual_ids = {r['variable_id'] for r in visual_variables}
    require(len(visual_variables) == len(visual_ids) == 9 and
            len({r['visual_key'] for r in visual_variables}) == 9, 'Visual scope must contain nine unique problems')
    require(all(r['variable_id'] in visual_ids for r in core_rules), 'Core rule outside visual scope')
    require(all(r['variable_id'] not in visual_ids for r in supplementary_rules), 'Visual rule filed as supplementary')
    rules = core_rules + supplementary_rules
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
    require(visual_ids <= set(t5), 'Visual scope has unknown T5 variables')
    for row in rules:
        require(re.fullmatch('[a-z][a-z0-9_]*', row['classification_id']) and
                re.fullmatch(r'\d+\.\d+\.\d+', row['version']), 'Invalid rule identity')
        identity = (row['classification_id'], row['version'])
        require(identity not in identities, 'Duplicate rule version')
        identities.add(identity)
        require(row['status'] == 'proposed', 'Context table cannot assert scientific acceptance')
        route = t5.get(row['variable_id'])
        require(route and route['mcda_role'] == 'priority' and route['concern_id'] == row['concern_id'], 'Context rule conflicts with T5 routing')
        rule_file = 'rules.csv' if row['variable_id'] in visual_ids else 'supplementary_rules.csv'
        require(route['classification_set_ref'] == f'{FOLDER}/{rule_file}#{row["rule_set_id"]}', 'T5 does not link to rule set')
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
        require(binding['validation'] in {'table_inspected','documentation_only','requires_local_assessment','requires_local_data','requires_reference_calibration'} and finite(binding['scale']) and binding['scale'] > 0 and finite(binding['offset']), 'Invalid binding conversion/status')
        require(binding['validation'] != 'requires_local_assessment' or row['method'] == 'categories', 'Local assessment rule must preserve published categories')
        lo, hi = row['domain_min'], row['domain_max']
        require(finite(lo) and (hi is None or finite(hi) and lo < hi), 'Invalid classification domain')
        require(row['method'] in {'terciles','thresholds','categories'}, 'Invalid classification method')
        require(isinstance(row['category_map'], dict), 'Invalid category map')
        if binding['validation'] in {'requires_local_data', 'requires_reference_calibration'}:
            require(row['method'] == 'terciles', 'Pending calibration only supports the tercile approach')
            require(all(row[k] is None for k in ('none_upper','low_upper','medium_upper')) and
                    not row['reference_sample_id'] and not row['category_map'],
                    'Pending calibration cannot carry cutoffs, a sample or category classes')
            row.update(binding_candidate=None, reference_sample=None, cuts=None, missing='unknown',
                       endpoint='not_calibrated', runtime_ready=False)
            continue
        if row['method'] == 'categories':
            require(binding['scale'] == 1 and binding['offset'] == 0 and row['unit'] == binding['source_unit'],
                    'Category codes cannot be numerically transformed')
            require(row['category_map'] and all(isinstance(k,str) and k and v in {'none','low','medium','high'}
                    for k,v in row['category_map'].items()), 'Invalid category mapping')
            require(not {'unknown','outside_domain'} & set(row['category_map']), 'Unknown cannot become a class')
            require(all(row[k] is None for k in ('none_upper','low_upper','medium_upper')) and
                    not row['reference_sample_id'], 'Category rule cannot carry numeric thresholds or a sample')
            from binding_candidates import read_rows
            candidates = [c for c in read_rows(root / 'priority/bindings')
                          if c['variable_id'] == row['variable_id'] and c['asset'] == binding['asset']
                          and c['dataset_id'] == binding['dataset_id'] and binding['field'] in c['auxiliary_fields']]
            if binding['validation'] == 'requires_local_assessment':
                require(not candidates, 'Local assessment placeholder conflicts with inspected binding')
                require(hi is not None and lo.is_integer() and hi.is_integer() and hi - lo < 100,
                        'Invalid published category domain')
                require(set(row['category_map']) == {str(i) for i in range(int(lo),int(hi)+1)},
                        'Published categories must cover the declared domain exactly')
                row.update(binding_candidate=None, reference_sample=None, cuts=None, missing='unknown',
                           endpoint='provider_category', runtime_ready=False)
                continue
            require(len(candidates) == 1 and candidates[0]['decode'] is not None, 'Unresolved category input binding')
            candidate = candidates[0]
            declared = candidate['selectors']['native_categories']
            expected = {k for k,v in declared.items() if v != 'unknown'}
            states = set(candidate['decode']['special_values'].values()) | {
                v for g in candidate['decode']['guards'] for v in g['equals'].values()}
            states -= {'unknown','outside_domain'}
            require(set(row['category_map']) == expected | states, 'Category map must cover declared codes and special states')
            require(all(row['category_map'][k] == row['category_map'][v]
                        for k,v in declared.items() if v in states), 'Category and decoded flag disagree')
            row['binding_candidate'] = candidate
            row['reference_sample'] = None
            row['cuts'] = None
            row['missing'] = 'unknown'
            row['endpoint'] = 'provider_category'
            row['runtime_ready'] = False
            continue
        require(not row['category_map'], 'Numeric rule cannot carry a category map')
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
            require(reference.startswith((f'{FOLDER}/rules.csv#', f'{FOLDER}/supplementary_rules.csv#')) and reference.split('#',1)[1] in routes, 'Unresolved classification set')
            require(not route['proposed_rule_ref'] and not route['accepted_rule_ref'], 'Single rule and contextual set conflict')
    return {'format':'ruralscan.context-classification-review.v3', 'runtime_ready':False,
        'input_sha256':{f'{FOLDER}/{name}':sha256((folder/name).read_bytes()).hexdigest()
                        for name in ['columns.json'] + [s['file'] for s in manifest['tables'].values()]},
        'rules':core_rules, 'supplementary_rules':supplementary_rules, 'visual_variables':visual_variables, 'countries':countries, 'sources':sources}


def check(root=ROOT):
    actual = bundle(root)
    require(json.loads((root / FOLDER / 'rules.json').read_text()) == actual, 'Stale generated contextual rules')
    return actual


def resolve(variable, country_code=None, *, vintage, region=None, for_runtime=False, include_supplementary=False, root=ROOT):
    """Resolve a core review rule; supplementary work requires explicit opt-in."""
    require(not for_runtime, 'Context rules are not an accepted runtime release')
    data = check(root)
    available = data['rules'] + (data['supplementary_rules'] if include_supplementary else [])
    rules = [r for r in available if r['variable_id'] == variable]
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
    require(rule['method'] != 'categories', 'Category rules require raw value and category together')
    if rule['binding']['validation'] in {'requires_local_data', 'requires_reference_calibration'}:
        return None
    if value is None or not finite(value):
        return None
    if value < rule['domain_min'] or (rule['domain_max'] is not None and value > rule['domain_max']):
        return None
    labels = ['low','medium','high'] if rule['method'] == 'terciles' else ['none','low','medium','high']
    if rule['direction'] == 'lower_is_more_concern':
        labels.reverse()
    return labels[bisect_left(rule['cuts'], value)]


def preview_category_record(rule, raw, category):
    """Review one bound record; retain its source category and decoded scarcity flag."""
    from binding_candidates import inspect_numeric
    require(rule['method'] == 'categories', 'Not a category rule')
    candidate = rule['binding_candidate']
    require(candidate is not None, 'Select an applicable local assessment before previewing source records')
    result = {'class':None, 'state':'unknown', 'raw':raw, 'category':category}
    if not finite(raw) or not finite(category) or not float(category).is_integer():
        return result
    # Missing raw data takes precedence over an auxiliary category flag.
    missing = {float(k) for k,v in candidate['decode']['special_values'].items() if v == 'unknown'}
    if raw in missing:
        return result
    bounds = candidate['decode']['valid_range']
    if bounds and ((bounds[0] is not None and raw < bounds[0]) or (bounds[1] is not None and raw > bounds[1])):
        result['state'] = 'outside_domain'
        return result
    decoded = inspect_numeric(candidate, raw, {'category':category})
    state = decoded['state']
    key = str(int(category)) if state == 'numeric' else state
    result.update(state=state, **{'class':rule['category_map'].get(key)})
    return result


def preview_documented_category(rule, value, *, unit, assessment_available=False, assessment_applicable=False):
    """Review published category meanings only within explicitly available, applicable coverage."""
    require(rule['method'] == 'categories' and rule['binding']['validation'] == 'requires_local_assessment',
            'Not a local assessment category rule')
    require(unit == rule['unit'], 'Input units differ; do not substitute another classification')
    if assessment_available is not True or assessment_applicable is not True:
        return None
    if not finite(value) or not float(value).is_integer():
        return None
    return rule['category_map'].get(str(int(value)))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['generate','check'])
    args = parser.parse_args()
    if args.command == 'generate':
        (ROOT / FOLDER / 'rules.json').write_text(json.dumps(bundle(), indent=2, ensure_ascii=False) + '\n')
    data = check()
    print(f'{len(data["rules"])} core contextual rules; {len(data["supplementary_rules"])} supplementary rules; 0 accepted runtime rules')
