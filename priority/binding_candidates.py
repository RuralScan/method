"""Offline proposal generation and inspection checks. No runtime adapter or acceptance."""
import argparse
import csv
from hashlib import sha256
import json
import math
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parent / 'bindings'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def read_rows(root=ROOT):
    structure = json.loads((root / 'columns.json').read_text())
    with (root / 'candidates.csv').open(newline='') as stream:
        reader = csv.DictReader(stream)
        require(reader.fieldnames == structure['columns'], 'Binding proposal columns changed')
        rows = list(reader)
    for row in rows:
        require(None not in row and all(v is not None for v in row.values()), 'Malformed CSV row')
        for key in structure['json_columns']:
            row[key] = json.loads(row[key])
    return rows


def inspect_numeric(row, raw, auxiliary=None):
    """Review oracle for source encoding only; no spatial coverage or classification."""
    spec = row['decode']
    require(spec is not None, 'No inspected numeric contract')
    auxiliary = auxiliary or {}
    for guard in spec['guards']:
        value = auxiliary.get(guard['field'])
        if value is None:
            return {'state': guard['missing'], 'value': None}
        for code, state in guard['equals'].items():
            if float(value) == float(code):
                return {'state': state, 'value': None}
        if 'valid_values' in guard and value not in guard['valid_values']:
            return {'state': 'unknown', 'value': None}
    if raw is None or not math.isfinite(float(raw)):
        return {'state': spec['missing_state'], 'value': None}
    raw = float(raw)
    for code, state in spec['special_values'].items():
        if raw == float(code):
            return {'state': state, 'value': None}
    bounds = spec['valid_range']
    if bounds is not None and ((bounds[0] is not None and raw < bounds[0])
                               or (bounds[1] is not None and raw > bounds[1])):
        return {'state': 'outside_domain', 'value': None}
    return {'state': 'numeric', 'value': raw * spec['scale'] + spec['offset']}


def inspect_recurrence(candidate, source, series, threshold):
    """Review arithmetic for a declared annual series; not a spatial runtime adapter."""
    spec = candidate['selectors']['derivation']
    require(source['binding_id'] == spec['source_binding_id'], 'Wrong recurrence source')
    require(threshold in spec['allowed_affected_area_thresholds'], 'Unsupported affected-area event threshold')
    require(spec['event_operator'] == '>' and spec['require_complete_period'] is True,
            'Recurrence requires explicit strict event and complete-period semantics')
    years = set(range(spec['start_year'], spec['end_year'] + 1))
    seen, valid, events = set(), 0, 0
    for item in series:
        year = item['year']
        require(year in years and year not in seen, 'Duplicate or out-of-period growing season')
        seen.add(year)
        decoded = inspect_numeric(source, item['value'])
        if decoded['state'] == 'numeric':
            valid += 1
            events += decoded['value'] > threshold
    complete = valid == len(years)
    return {'state': 'numeric' if complete else 'incomplete_series',
            'value': 100 * events / valid if complete else None,
            'valid_seasons': valid, 'expected_seasons': len(years), 'event_count': events}


def validate(rows, root=ROOT):
    require(bool(rows), 'Empty binding proposal')
    ids = set()
    method = root.parents[1]
    with (method / 'priority/T5_classification_refs.csv').open() as f:
        t5 = {r['variable_id']: r for r in csv.DictReader(f)}
    with (method / 'priority/t2/variables.csv').open() as f:
        t2 = {r['variable_id']: r for r in csv.DictReader(f)}
    for row in rows:
        key = row['binding_id']
        require(re.fullmatch('[a-z][a-z0-9_]+', key) and key not in ids, 'Invalid/duplicate binding ID')
        ids.add(key)
        require(row['scientifically_accepted'] is False and row['runtime_ready'] is False,
                'Candidate table cannot accept or release bindings')
        require(row['blocking'] and row['documentation'] and row['observation_refs'], 'Missing blockers or provenance')
        require(row['inspection_status'] in {'sample_checked', 'metadata_checked', 'access_unavailable'}, 'Invalid inspection status')
        require(row['registry'] in {'T2', 'T5', 'proposed_successor', 'proposed_descriptor'}, 'Unknown registry')
        if row['registry'] in {'T2', 'T5'}:
            registry = t5 if row['registry'] == 'T5' else t2
            require(row['variable_id'] in registry, 'Unknown current variable')
            current = registry[row['variable_id']]
            require(row['mcda_role'] == current['mcda_role'] and row['concern_id'] == current['concern_id'],
                    'Candidate conflicts with current routing')
        elif row['registry'] == 'proposed_descriptor':
            require(row['mcda_role'] == 'descriptor', 'Proposed descriptor cannot be scored')
        require(row['variable_id'] != 'carbon_sequestration_potential', 'Legacy carbon alias is blocked')
        require(row['selectors'].get('required'), 'Explicit context/selection requirements missing')
        spec = row['decode']
        if row['inspection_status'] == 'sample_checked':
            require(spec is not None, 'Sample-checked candidate needs its inspected encoding')
        if spec is not None:
            require(set(spec) == {'scale', 'offset', 'valid_range', 'special_values', 'guards', 'missing_state', 'clip'}, 'Unknown decoding contract fields')
            require(spec['clip'] is False and spec['missing_state'] == 'unknown', 'Clipping or false-zero missingness forbidden')
            require(all(isinstance(spec[k], (int, float)) and math.isfinite(spec[k]) for k in ('scale', 'offset')), 'Invalid scale/offset')
            require(spec['scale'] > 0, 'Positive unit scale required')
            bounds = spec['valid_range']
            require(bounds is None or (len(bounds) == 2 and (None in bounds or bounds[0] < bounds[1])), 'Invalid domain')
    vectors = json.loads((root / 'inspection-vectors.json').read_text())
    by_id = {r['binding_id']: r for r in rows}
    for vector in vectors:
        require(by_id[vector['binding_id']]['unit'] == vector['expected_unit'], 'Encoding unit regression: ' + vector['name'])
        actual = inspect_numeric(by_id[vector['binding_id']], vector['raw'], vector.get('auxiliary'))
        require(actual == vector['expected'], 'Encoding regression: ' + vector['name'])
    recurrence = by_id['fao_asi_recurrence_candidate']
    source = by_id[recurrence['selectors']['derivation']['source_binding_id']]
    require(source['selectors']['pixelType'] == 'F32', 'ASI recurrence requires float-preserving input')
    for vector in json.loads((root / 'recurrence-vectors.json').read_text()):
        actual = inspect_recurrence(recurrence, source, vector['series'], vector['threshold'])
        require(actual == vector['expected'], 'Recurrence regression: ' + vector['name'])
    # The producer-native source is a distinct version/encoding from the old convenience mirror.
    producer = by_id['forest_gross_emissions_2025_candidate']
    require(producer['selectors']['matched_loss_binding_id'] == 'hansen_forest_loss_candidate'
            and producer['selectors']['model_version'] == '1.4.3'
            and producer['selectors']['gfw_dataset_version'] == 'v20260327'
            and producer['unit'] == 'Mg_CO2e_per_ha_over_2001_2025', 'Forest model/loss edition mismatch')
    require(inspect_numeric(producer, 0) == {'state': 'unknown', 'value': None},
            'Producer-native nodata zero cannot become zero emissions')
    holds = json.loads((root / 'holds.json').read_text())
    require(holds['runtime_release_ready'] is False, 'Hold resolution cannot release a pilot')
    seen_holds = set()
    observations = {ref['observation_id'] for row in rows for ref in row['observation_refs']}
    for hold in holds['holds']:
        require(hold['id'] not in seen_holds, 'Duplicate hold ID')
        seen_holds.add(hold['id'])
        require(hold['status'] in {'resolved', 'resolved_by_replacement', 'context_required', 'scientific_review'}, 'Invalid hold status')
        require(set(hold['bindings']) <= by_id.keys() and bool(hold['bindings']), 'Unknown hold binding')
        require(set(hold['observations']) <= observations and bool(hold['observations']), 'Missing hold provenance')
        require(bool(hold['resolution']), 'Missing hold disposition')
        if hold['status'] == 'resolved_by_replacement':
            require(hold['replacement_binding_id'] in hold['bindings'], 'Replacement binding missing')
    return rows


def generated(rows):
    return (json.dumps({'format': 'ruralscan.binding-candidates.v1',
                        'status': 'technical_proposals_not_accepted_bindings', 'candidates': rows},
                       indent=2, ensure_ascii=False, allow_nan=False) + '\n').encode()


def check_evidence(rows, evidence_repo, root=ROOT):
    lock = json.loads((root / 'evidence.lock.json').read_text())
    require(lock['repository'] == 'https://github.com/RuralScan/evidence.git'
            and re.fullmatch('[0-9a-f]{40}', lock['revision']), 'Invalid evidence revision')
    def blob(path):
        return subprocess.check_output(['git', '-C', str(evidence_repo), 'show', f"{lock['revision']}:{path}"])
    body = blob(lock['manifest_path'])
    require(sha256(body).hexdigest() == lock['manifest_sha256'], 'Inspection manifest hash mismatch')
    manifest = json.loads(body)
    require(manifest['status'] == 'technical_observations_not_binding_acceptance', 'Unexpected evidence packet status')
    entries = {r['observation_id']: r for r in manifest['records']}
    for row in rows:
        for ref in row['observation_refs']:
            require(entries.get(ref['observation_id']) == ref, 'Observation reference does not match pinned manifest')
            require(ref['path'] == f"observations/{ref['observation_id']}.json", 'Invalid observation path')
            data = blob(str(Path(lock['manifest_path']).parent / ref['path']))
            require(sha256(data).hexdigest() == ref['sha256'], 'Observation hash mismatch')
            require(json.loads(data)['human_review'] is None, 'Technical observation cannot supply acceptance')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['generate', 'check'])
    parser.add_argument('--evidence-repo', type=Path)
    args = parser.parse_args()
    rows = validate(read_rows())
    output = ROOT / 'candidates.json'
    if args.command == 'generate':
        output.write_bytes(generated(rows))
    else:
        require(output.read_bytes() == generated(rows), 'Generated binding JSON is stale')
    if args.evidence_repo:
        check_evidence(rows, args.evidence_repo)
    print(f'{len(rows)} binding candidates checked; no acceptance or runtime release')
