"""Check frozen Haiti infrastructure provenance and reporting invariants offline."""
import hashlib
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parent
folder = ROOT / 'roads-haiti-audit-20261127'
manifest = json.loads((folder/'manifest.json').read_text())
for name, expected in manifest.items():
    assert hashlib.sha256((folder/name).read_bytes()).hexdigest() == expected, name
for script in folder.glob('*.py'):
    compile(script.read_text(), str(script), 'exec')
result = json.loads((folder/'inspection.json').read_text())
boundary = ROOT.parent/'research/haiti-diagnostic-inputs-20261126/boundary.json'
assert result['boundary_sha256'] == hashlib.sha256(boundary.read_bytes()).hexdigest()
assert result['osm_acquisition_sha256'] == manifest['acquisition.json']
assert result['national_zip_sha256'] == json.loads((folder/'inputs.json').read_text())['national_zip_sha256']
assert result['runtime_ready'] is False
assert result['hazard_overlay_performed'] is False
assert result['opportunity_space_overlay_performed'] is False
for source in ('osm', 'cnigs'):
    data = result[source]
    counts = data['counts']
    groups = data['haiti_classes']
    records = counts['haiti_positive_length_records']
    assert records == sum(group['records'] for group in groups.values())
    assert 0 < records <= counts['source_records']
    assert all(math.isfinite(group['mapped_line_km']) and group['mapped_line_km'] >= 0 for group in groups.values())
    assert abs(sum(group['mapped_line_km'] for group in groups.values()) - data['all_classes_mapped_line_km']) < 1e-5
    assert data['haiti_distinct_nonblank_ids'] + data['haiti_extra_records_sharing_nonblank_id'] + data['haiti_blank_id_records'] == records
    assert all(0 <= count <= records for count in data['haiti_blank_attribute_counts'].values())
    assert counts.get('exact_duplicate_clipped_geometry_records', 0) <= records
    assert data['geometry_repaired'] is False and data['deduplication_applied'] is False
assert result['cnigs']['class_field'] == 'type_tronc'
assert result['cnigs']['id_field'] == 'OBJECTID'
assert result['cnigs']['haiti_blank_attribute_counts']['cod_tronc'] == result['cnigs']['counts']['haiti_positive_length_records']
print(f'PASS: {len(manifest)} road-audit hashes, source/boundary pins, class/length/identity totals; no exposure or runtime activation.')

folder = ROOT / 'facilities-haiti-audit-20261127'
manifest = json.loads((folder/'manifest.json').read_text())
for name, expected in manifest.items():
    assert hashlib.sha256((folder/name).read_bytes()).hexdigest() == expected, name
for script in folder.glob('*.py'):
    compile(script.read_text(), str(script), 'exec')
result = json.loads((folder/'inspection.json').read_text())
review = json.loads((folder/'review_summary.json').read_text())
assert result['input_sha256']['boundary.json'] == hashlib.sha256(boundary.read_bytes()).hexdigest()
assert result['input_sha256']['config.json'] == manifest['config.json']
assert result['input_sha256']['departments.geojson'] == json.loads((folder/'departments-acquisition.json').read_text())['sha256']
assert result['runtime_ready'] is False and result['automatic_merge'] is False and result['exposure_computed'] is False
assert result['department_features'] == 10
for source, data in result['sources'].items():
    inside = data['states'].get('in_haiti', 0)
    assert sum(data['states'].values()) == data['records']
    assert sum(data['classes_in_haiti'].values()) == inside
    assert sum(sum(v.values()) for v in data['department_class_counts'].values()) == inside
    assert sum(data['classes_in_national_boundary'].values()) == data['inside_national_department_union']
    assert sum(data['national_department_counts'].values()) == data['inside_national_department_union']
    assert inside + data['inside_national_but_outside_pinned'] - data['inside_pinned_but_outside_national'] == data['inside_national_department_union']
    groups = data['exact_geometry_groups_in_haiti']
    assert sum(len(g)-1 for g in groups) == data['exact_geometry_excess_in_haiti']
    assert all(len(g) > 1 and len(set(g)) == len(g) for g in groups)
    assert len({key for g in groups for key in g}) == sum(len(g) for g in groups)
assert sum(result['osm_point_polygon_by_theme_name'].values()) == result['osm_point_polygon_pairs']
assert sum(result['osm_polygon_overlap_by_theme_name'].values()) == result['osm_polygon_overlap_pairs']
assert review['decision'] == 'unresolved_candidates_not_deleted'
assert len(review['same_name_point_polygon_pairs']) == sum(v for k,v in result['osm_point_polygon_by_theme_name'].items() if k.endswith('same_normalized_name'))
assert review['point_polygon_pair_counts'] == result['osm_point_polygon_by_theme_name']
assert review['polygon_overlap_pair_counts'] == result['osm_polygon_overlap_by_theme_name']
assert result['paho_department_mismatch_count'] <= result['sources']['paho']['states']['in_haiti']
print(f'PASS: {len(manifest)} facility-audit hashes, both boundary counts, source/class totals and unresolved duplicate flags; no automatic merge or exposure.')
