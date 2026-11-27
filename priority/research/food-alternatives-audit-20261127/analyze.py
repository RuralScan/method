"""Inspect acquired food-source files without defining or activating classes.

Usage: uv run --with shapely==2.1.2 --with pyproj==3.7.2 python analyze.py SOURCE_DIR OUTPUT.json
SOURCE_DIR contains the three pinned original JSON/GeoJSON files in acquisition.json.
"""
from collections import defaultdict
import hashlib
import json
from pathlib import Path
import sys

import pyproj
from pyproj import Transformer
import shapely
from shapely.geometry import shape
from shapely.ops import transform, unary_union

HERE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(source_dir, output):
    source_dir = Path(source_dir)
    manifest = json.loads((HERE / "acquisition.json").read_text())
    names = ("fews_haiti_202610.geojson", "wdi_fies_haiti.json", "wdi_fies_metadata.json")
    for name in names:
        assert digest(source_dir / name) == manifest["members"][name], name
    boundary_path = HERE.parent / "haiti-diagnostic-inputs-20261126/boundary.json"
    assert digest(boundary_path) == manifest["boundary_sha256"]
    boundary = json.loads(boundary_path.read_text())
    aoi = unary_union([shape(f["geometry"]) for f in boundary["features"]])
    assert aoi.is_valid
    project = Transformer.from_crs(4326, 6933, always_xy=True).transform

    def area(geometry):
        return transform(project, geometry).area / 1e6

    data = json.loads((source_dir / names[0]).read_text())
    groups = defaultdict(list)
    for feature in data["features"]:
        p = feature["properties"]
        assert shape(feature["geometry"]).is_valid
        assert p["country_code"] == "HT" and p["classification_scale"] == "IPC 3.1"
        assert p["reporting_date"] == "2026-10-01"
        groups[p["scenario"]].append(feature)
    assert set(groups) == {"CS", "ML1", "ML2"}, "Unexpected scenario inventory"
    total = area(aoi)
    scenarios = []
    for scenario, features in sorted(groups.items()):
        clipped = [shape(f["geometry"]).intersection(aoi) for f in features]
        covered = unary_union(clipped)
        covered_area = area(covered)
        missing_area = area(aoi.difference(covered))
        assert abs(total - covered_area - missing_area) < 1e-3
        overlap = sum(area(g) for g in clipped) - covered_area
        assert overlap >= -1e-3
        properties = [f["properties"] for f in features]
        scenarios.append({
            "scenario": scenario, "features": len(features),
            "reporting_dates": sorted({p["reporting_date"] for p in properties}),
            "start": sorted({p["projection_start"] for p in properties}),
            "end": sorted({p["projection_end"] for p in properties}),
            "native_phases": sorted({p["value"] for p in properties}),
            "haiti_coverage_percent": covered_area / total * 100,
            "unknown_area_km2": missing_area, "overlap_km2": overlap,
            "overlap_reconciled": False,
            "assistance_flags": sorted({p["is_allowing_for_assistance"] for p in properties}),
            "native_properties": properties,
        })
    wdi = json.loads((source_dir / names[1]).read_text())
    assert wdi[0]["pages"] == 1
    observations = [r for r in wdi[1] if r["value"] is not None]
    assert all(r["countryiso3code"] == "HTI" and r["indicator"]["id"] == "SN.ITK.MSFI.ZS"
               for r in observations)
    latest = max(observations, key=lambda r: int(r["date"]))
    result = {
        "checked_date": "2026-11-27", "runtime_ready": False,
        "approved_chronic_mapping_applicable": False,
        "area_crs": "EPSG:6933", "boundary_area_km2": total,
        "boundary_sha256": digest(boundary_path),
        "input_sha256": {name: digest(source_dir / name) for name in names},
        "fews": {"feature_count": len(data["features"]), "all_geometries_valid": True,
                 "scenarios": scenarios, "area_classes_aggregated": False},
        "wdi": {"latest_nonnull_observation": latest,
                "metadata": json.loads((source_dir / names[2]).read_text()),
                "grain": "national", "averaging_interval_verified": False},
        "versions": {"shapely": shapely.__version__, "pyproj": pyproj.__version__},
    }
    Path(output).write_text(json.dumps(result, indent=2) + "\n")
    print(f"Checked {len(data['features'])} FEWS features in {len(scenarios)} separate scenarios; "
          f"overlaps retained as holds; latest non-null WDI year {latest['date']}.")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
