"""Inspect BII at native grid support using previously approved class data.

Usage: uv run --with rasterio==1.5.2 --with shapely==2.1.2 --with pyproj==3.7.2 python probe.py SOURCE_TIF OUTPUT.json
This is a bounded research probe, not a released binding or combined biodiversity score.
"""
import csv
import hashlib
import json
import math
from pathlib import Path
import sys

import pyproj
from pyproj import Transformer
import rasterio
from rasterio.windows import Window, from_bounds
import shapely
from shapely.geometry import box, shape
from shapely.ops import transform, unary_union

HERE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def decode(value, contract, classes):
    if value is None or not math.isfinite(value) or not contract['valid_min'] <= value <= contract['valid_max']:
        return None, None
    assert contract['transform'] == 'reference_minus_input'
    depletion = contract['reference'] - value
    label = next(row['class'] for row in classes if depletion <= float(row['depletion_upper_inclusive']))
    return depletion, label


def main(source, output):
    source = Path(source)
    contract = json.loads((HERE / 'contract.json').read_text())
    assert digest(source) == contract['source_sha256']
    with (HERE / contract['class_source']).open() as stream:
        classes = list(csv.DictReader(stream))
    cuts = [float(r['depletion_upper_inclusive']) for r in classes]
    assert cuts == sorted(set(cuts))
    boundary_path = HERE.parent / 'haiti-diagnostic-inputs-20261126/boundary.json'
    boundary = json.loads(boundary_path.read_text())
    aoi = unary_union([shape(f['geometry']) for f in boundary['features']])
    assert aoi.is_valid
    project = Transformer.from_crs(4326, 6933, always_xy=True).transform

    def area(geometry):
        return transform(project, geometry).area / 1e6

    rows = []
    with rasterio.open(source) as ds:
        assert ds.crs.to_epsg() == 4326 and ds.count == 1 and ds.scales == (1.0,) and ds.offsets == (0.0,)
        assert math.isnan(ds.nodata) and ds.transform.b == ds.transform.d == 0
        extent = from_bounds(*aoi.bounds, transform=ds.transform)
        r0, c0 = math.floor(extent.row_off), math.floor(extent.col_off)
        r1, c1 = math.ceil(extent.row_off + extent.height), math.ceil(extent.col_off + extent.width)
        values = ds.read(1, window=Window(c0, r0, c1-c0, r1-r0))
        for r in range(r0, r1):
            for c in range(c0, c1):
                x0, y0 = ds.transform * (c, r)
                x1, y1 = ds.transform * (c+1, r+1)
                clipped = box(x0, y1, x1, y0).intersection(aoi)
                if clipped.is_empty:
                    continue
                clipped_area = area(clipped)
                if clipped_area <= 0:
                    continue
                value = float(values[r-r0, c-c0])
                depletion, label = decode(value, contract, classes)
                rows.append({'native_row': r, 'native_col': c,
                             'bii_percent': value if math.isfinite(value) else None,
                             'depletion': depletion, 'class': label, 'haiti_area_km2': clipped_area})
        metadata = {'crs': str(ds.crs), 'resolution_degrees': list(ds.res), 'shape': list(ds.shape),
                    'transform': list(ds.transform), 'dtype': ds.dtypes[0], 'nodata': 'NaN'}
    total = area(aoi)
    assert abs(sum(r['haiti_area_km2'] for r in rows) - total) < 1e-3
    valid = [r for r in rows if r['class'] is not None]
    valid_area = sum(r['haiti_area_km2'] for r in valid)
    unknown_area = sum(r['haiti_area_km2'] for r in rows if r['class'] is None)
    assert abs(total - valid_area - unknown_area) < 1e-3
    summaries = []
    for category in classes:
        group = [r for r in valid if r['class'] == category['class']]
        a = sum(r['haiti_area_km2'] for r in group)
        summaries.append({'class': category['class'], 'native_intersecting_cells': len(group),
                          'area_km2': a, 'percent_of_boundary': a/total*100,
                          'percent_of_valid_area': a/valid_area*100})
    edge_checks = []
    # Fixed approved equality cases; table remains the analytical source for the decoder.
    for value, expected in [(0, 'High'), (60, 'Medium'), (80, 'Low'), (90, 'Very little'),
                            (100, 'Very little'), (-1, None), (101, None), (None, None), (float('nan'), None)]:
        depletion, label = decode(value, contract, classes)
        assert label == expected
        edge_checks.append({'input': value if value is None or math.isfinite(value) else 'NaN',
                            'depletion': depletion, 'class': label})
    for value in [r['bii_percent'] for r in valid]:
        depletion, _ = decode(value, contract, classes)
        assert abs(value + depletion - contract['reference']) < 1e-12
    result = {'scope': 'Country boundary / native-cell inspection; not an NbS footprint or combined biodiversity score',
              'runtime_ready': False, 'combined_biodiversity': 'Not assessed: KBA input unavailable',
              'source_year': contract['source_year'], 'source_sha256': digest(source),
              'boundary_sha256': digest(boundary_path), 'contract_sha256': digest(HERE/'contract.json'),
              'classes_sha256': digest(HERE/contract['class_source']), 'metadata': metadata,
              'area_crs': 'EPSG:6933', 'boundary_area_km2': total,
              'intersecting_native_cells': len(rows), 'valid_native_cells': len(valid),
              'valid_area_km2': valid_area, 'unknown_area_km2': unknown_area,
              'valid_percent_of_boundary': valid_area/total*100, 'unknown_percent_of_boundary': unknown_area/total*100,
              'bii_min': min(r['bii_percent'] for r in valid), 'bii_max': max(r['bii_percent'] for r in valid),
              'out_of_domain_cells': sum(r['bii_percent'] is not None and r['class'] is None for r in rows),
              'classes': summaries, 'boundary_checks': edge_checks, 'cells': rows,
              'versions': {'rasterio': rasterio.__version__, 'shapely': shapely.__version__, 'pyproj': pyproj.__version__}}
    Path(output).write_text(json.dumps(result, indent=2, allow_nan=False)+'\n')
    print(json.dumps({k:v for k,v in result.items() if k not in ('cells','boundary_checks')}, indent=2))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
