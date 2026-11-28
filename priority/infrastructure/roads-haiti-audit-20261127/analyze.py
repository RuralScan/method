"""Inspect complete road geometry and Haiti-clipped line lengths; no exposure model."""
import collections
import hashlib
import io
import json
import sys
import zipfile
from pathlib import Path
import shapefile
from shapely.geometry import shape, box
from shapely.ops import transform, unary_union
from shapely import normalize
from pyproj import CRS, Transformer, Geod


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inspect(reader, source_crs, boundary, class_field, id_field):
    crs = CRS.from_user_input(source_crs)
    to_wgs = Transformer.from_crs(crs, 4326, always_xy=True).transform
    geod = Geod(ellps='WGS84')
    bounds = box(*boundary.bounds)
    totals = collections.Counter({key: 0 for key in (
        'source_records', 'empty_source_geometry', 'nonline_source_geometry',
        'invalid_source_geometry', 'nonsimple_source_geometry',
        'haiti_touch_only_or_zero_length', 'haiti_positive_length_records',
        'haiti_nonsimple_source_geometry', 'exact_duplicate_clipped_geometry_records',
        'exact_duplicate_clipped_geometry_km')})
    groups = {}
    seen_geometry = set()
    ids = collections.Counter()
    blank_fields = collections.Counter()
    duplicate_examples = []
    for row in reader.iterShapeRecords():
        totals['source_records'] += 1
        if not row.shape.points:
            totals['empty_source_geometry'] += 1
            continue
        geom = shape(row.shape.__geo_interface__)
        if geom.geom_type not in ('LineString', 'MultiLineString'):
            totals['nonline_source_geometry'] += 1
            continue
        if not geom.is_valid:
            totals['invalid_source_geometry'] += 1
            continue
        if not geom.is_simple:
            totals['nonsimple_source_geometry'] += 1
        if crs != CRS.from_epsg(4326):
            geom = transform(to_wgs, geom)
        if not geom.intersects(bounds) or not geom.intersects(boundary):
            continue
        clipped = geom.intersection(boundary)
        def lines(g):
            if g.geom_type == 'LineString': return [g]
            if hasattr(g, 'geoms'): return [part for child in g.geoms for part in lines(child)]
            return []
        parts = lines(clipped)
        length = sum(geod.geometry_length(p) for p in parts)/1000
        if length <= 0:
            totals['haiti_touch_only_or_zero_length'] += 1
            continue
        totals['haiti_positive_length_records'] += 1
        if not geom.is_simple:
            totals['haiti_nonsimple_source_geometry'] += 1
        attrs = row.record.as_dict()
        for field, value in attrs.items():
            if value is None or str(value).strip() == '':
                blank_fields[field] += 1
        category = str(attrs[class_field])
        group = groups.setdefault(category, {'records': 0, 'mapped_line_km': 0.0,
            'bridge_values': {}, 'tunnel_values': {}})
        group['records'] += 1
        group['mapped_line_km'] += length
        for field in ('bridge', 'tunnel'):
            if field in attrs:
                key = str(attrs[field])
                values = group[field+'_values']
                values[key] = values.get(key, 0)+1
        identifier = str(attrs[id_field]).strip()
        ids[identifier] += 1
        key = normalize(unary_union(parts)).wkb
        if key in seen_geometry:
            totals['exact_duplicate_clipped_geometry_records'] += 1
            totals['exact_duplicate_clipped_geometry_km'] += length
            if len(duplicate_examples) < 10:
                duplicate_examples.append({'source_id': identifier, 'class': category})
        seen_geometry.add(key)
    for group in groups.values():
        group['mapped_line_km'] = round(group['mapped_line_km'], 6)
    return {
        'source_crs': crs.to_string(), 'class_field': class_field, 'id_field': id_field,
        'haiti_blank_attribute_counts': dict(sorted(blank_fields.items())),
        'counts': dict(sorted(totals.items())),
        'haiti_classes': dict(sorted(groups.items())),
        'all_classes_mapped_line_km': round(sum(g['mapped_line_km'] for g in groups.values()),6),
        'haiti_distinct_nonblank_ids': len([key for key in ids if key]),
        'haiti_blank_id_records': ids[''],
        'haiti_repeated_nonblank_ids': sum(n>1 for key,n in ids.items() if key),
        'haiti_extra_records_sharing_nonblank_id': sum(n-1 for key,n in ids.items() if key and n>1),
        'duplicate_examples': duplicate_examples,
        'geometry_repaired': False, 'deduplication_applied': False,
    }


def main():
    osm_dir, national_zip, boundary_path, output = map(Path, sys.argv[1:])
    boundary_json = json.loads(boundary_path.read_text())
    boundary = unary_union([shape(f['geometry']) for f in boundary_json['features']])
    assert boundary.is_valid
    acquisition = json.loads((osm_dir/'acquisition.json').read_text())
    for name, info in acquisition['members'].items():
        assert sha(osm_dir/name) == info['sha256'], name
    reader = shapefile.Reader(str(osm_dir/'gis_osm_roads_free_1'), encoding='utf-8')
    osm = inspect(reader, (osm_dir/'gis_osm_roads_free_1.prj').read_text(), boundary, 'fclass', 'osm_id')
    with zipfile.ZipFile(national_zip) as z:
        # Select the main network explicitly; ancillary surface/condition lines excluded.
        names = [n for n in z.namelist() if n.endswith('.shp')]
        main_name = next(n for n in names if 'seau_Routier' in n)
        prefix = main_name[:-4]
        reader = shapefile.Reader(shp=io.BytesIO(z.read(main_name)),
            dbf=io.BytesIO(z.read(prefix+'.dbf')), encoding='utf-8')
        national = inspect(reader, z.read(prefix+'.prj').decode(), boundary, 'type_tronc', 'OBJECTID')
        national['member'] = main_name
    result = {'runtime_ready': False, 'hazard_overlay_performed': False,
        'opportunity_space_overlay_performed': False,
        'boundary_sha256': sha(boundary_path),
        'osm_acquisition_sha256': sha(osm_dir/'acquisition.json'),
        'national_zip_sha256': sha(national_zip),
        'length_method': 'WGS84 ellipsoidal geodesic length after exact polygon clipping; no resampling',
        'osm': osm, 'cnigs': national,
        'comparison_limit': 'Different dates, classes and mapping conventions; lengths are not accuracy or completeness estimates. Sources are not concatenated.'}
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n')
    print(json.dumps({k:{'counts':v['counts'],'all_classes_mapped_line_km':v['all_classes_mapped_line_km']} for k,v in [('osm',osm),('cnigs',national)]},indent=2))

if __name__ == '__main__':
    main()
