"""Read source workbooks and reproduce exploratory poverty terciles; no source edits."""
import argparse
import hashlib
import json
import math
import statistics
from pathlib import Path

import openpyxl


def rows(path, sheet):
    book = openpyxl.load_workbook(path, read_only=True, data_only=True)
    values = iter(book[sheet].values)
    headers = next(values)
    result = [dict(zip(headers, row)) for row in values]
    book.close()
    return result


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def quantile(values, q):
    values = sorted(values)
    position = (len(values) - 1) * q
    left = math.floor(position)
    right = math.ceil(position)
    return values[left] + (values[right] - values[left]) * (position - left)


parser = argparse.ArgumentParser()
parser.add_argument('--source', type=Path, required=True)
parser.add_argument('--groups', type=Path, required=True)
parser.add_argument('--sheet', required=True)
parser.add_argument('--field', action='append', required=True)
parser.add_argument('--cohort', action='append', required=True, help='name=group|group')
parser.add_argument('--output', type=Path, required=True)
args = parser.parse_args()
classification = rows(args.groups, 'List of economies')
group_map = {r['Code']: r['Income group'] for r in classification if r['Income group']}
assert len(group_map) == sum(bool(r['Income group']) for r in classification)
source = rows(args.source, args.sheet)
assert len({r['geo_code'] for r in source}) == len(source)
assert len({r['lineupyear'] for r in source}) == 1
assert len({r['vintage'] for r in source}) == 1
dictionary = {r['Indicator_code']: r for r in rows(args.source, 'Dictionary')}
for field in args.field:
    assert dictionary[field]['scale_data'] == '0 - 1'
    assert dictionary[field]['scale_factor'] == 100
report = {
    'status': 'exploratory_contextual_calibration_not_accepted_runtime_rule',
    'source_sha256': digest(args.source),
    'groups_sha256': digest(args.groups),
    'group_notes': rows(args.groups, 'notes'),
    'sheet': args.sheet,
    'lineup_year': source[0]['lineupyear'],
    'source_vintage': source[0]['vintage'],
    'source_rows': len(source),
    'source_countries': len({r['code'] for r in source}),
    'weighting': 'one equally weighted source subnational area; not population-weighted',
    'quantile_method': 'linear interpolation at (n-1)*q, q=1/3 and 2/3',
    'none_condition': None,
    'zero_handling': 'retained in low; rounded zero does not establish absence of poverty',
    'results': [],
}
for cohort in args.cohort:
    name, membership = cohort.split('=', 1)
    members = set(membership.split('|'))
    assert members <= set(group_map.values()), members
    selected = [r for r in source if group_map.get(r['code']) in members]
    national = [r for r in selected if r['sample'].strip().lower() == 'national' or '_WB0' in r['geo_code']]
    areas = [r for r in selected if r not in national]
    for field in args.field:
        valid = [r for r in areas if isinstance(r[field], (int, float)) and math.isfinite(r[field]) and 0 <= r[field] <= 1]
        values = [r[field] * 100 for r in valid]
        cuts = [quantile(values, q) for q in (1/3, 2/3)]
        independent = statistics.quantiles(values, n=3, method='inclusive')
        assert all(math.isclose(a, b, abs_tol=1e-10) for a, b in zip(cuts, independent))
        assert cuts[0] < cuts[1]
        counts = [sum(x <= cuts[0] for x in values), sum(cuts[0] < x <= cuts[1] for x in values), sum(x > cuts[1] for x in values)]
        assert sum(counts) == len(values)
        sample = sorted([{'country':r['code'], 'area_id':r['geo_code'], 'area':r['sample'], 'income_group':group_map[r['code']], 'baseyear':r['baseyear'], 'welfaretype':r['welfaretype'], 'rate_percent':r[field]*100, 'vintage_gap':r['vintage_gap']} for r in valid], key=lambda r:r['area_id'])
        canonical = json.dumps(sample, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()
        sample_path = args.output.with_name(args.output.stem + '_' + name + '_' + field + '_sample.json')
        sample_path.write_bytes(canonical + b'\n')
        report['results'].append({
            'cohort': name, 'income_groups': sorted(members), 'field':field,
            'definition':dictionary[field]['indicator_description_long'],
            'countries':len({r['code'] for r in valid}), 'areas':len(valid),
            'excluded_national_countries': sorted({r['code'] for r in national}),
            'countries_with_no_source_rows': sorted({code for code, group in group_map.items() if group in members} - {r['code'] for r in selected}),
            'excluded_invalid_rows': len(areas) - len(valid),
            'zero_estimates':values.count(0),
            'survey_year_range':[min(r['baseyear'] for r in valid), max(r['baseyear'] for r in valid)],
            'missing_new_geometry_ids':sum(not r['geo_code2_new'] for r in valid),
            'max_vintage_gap':max(r['vintage_gap'] for r in valid),
            'cuts_percent':cuts, 'class_counts_low_medium_high':counts,
            'reference_sample_sha256':hashlib.sha256(canonical).hexdigest(),
            'sample_file':sample_path.name,
        })
args.output.write_text(json.dumps(report, indent=2, ensure_ascii=False) + '\n')
for r in report['results']:
    print(r['cohort'], r['field'], r['countries'], r['areas'], r['cuts_percent'], 'zeros',r['zero_estimates'])
