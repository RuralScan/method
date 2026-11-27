"""Reproduce Haiti coverage and basin-fragment diagnostics, not a runtime adapter.

Usage: uv run --with shapely --with pyproj python analyze.py OUTPUT.json
Class meanings come from the existing contextual rule bundle; none are set here.
"""
from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path
import sys

import pyproj
from pyproj import Geod, Transformer
import shapely
from shapely.geometry import shape
from shapely.geometry.polygon import orient
from shapely.ops import transform, unary_union

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "priority"))
from context_rules import bundle, preview_category_record


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(output):
    boundary_path = HERE.parent / "haiti-diagnostic-inputs-20261126/boundary.json"
    source_path = HERE / "haiti_intersecting_native.geojson.gz"
    boundary = json.loads(boundary_path.read_text())
    source_bytes = gzip.decompress(source_path.read_bytes())
    features = json.loads(source_bytes)["features"]
    aoi = unary_union([shape(f["geometry"]) for f in boundary["features"]])
    assert aoi.is_valid and not aoi.is_empty
    projection = Transformer.from_crs(4326, 6933, always_xy=True).transform

    def area(geometry):
        return transform(projection, geometry).area / 1e6

    rule = next(r for r in bundle()["rules"] if r["variable_id"] == "water_stress")
    rows, geometries, excluded = [], {}, []
    for feature in features:
        geometry = shape(feature["geometry"])
        # Fail rather than silently repair a source polygon.
        assert geometry.is_valid, feature["id"]
        clipped = geometry.intersection(aoi)
        clipped_area = area(clipped)
        if clipped_area <= 0:
            excluded.append({"feature_id": feature["id"], "reason": "no_positive_area_after_clip",
                             "source_country": feature["properties"].get("gid_0"),
                             "native_bounds": list(geometry.bounds)})
            continue
        properties = feature["properties"]
        decoded = preview_category_record(rule, properties.get("bws_raw"), properties.get("bws_cat"))
        rows.append({**properties, "feature_id": feature["id"], "clipped_area_km2": clipped_area,
                     "review_class": decoded["class"], "decode_state": decoded["state"]})
        geometries[feature["id"]] = clipped

    covered = unary_union(list(geometries.values()))
    valid_rows = [r for r in rows if r["review_class"] is not None]
    valid = unary_union([geometries[r["feature_id"]] for r in valid_rows])
    total, covered_area, valid_area = area(aoi), area(covered), area(valid)
    overlap = sum(r["clipped_area_km2"] for r in rows) - covered_area
    # Tolerance is numerical area bookkeeping, not an analytical exclusion threshold.
    assert abs(overlap) < 1e-3, "Overlapping fragments need explicit reconciliation"
    basin_groups = defaultdict(list)
    for row in valid_rows:
        basin_groups[row["pfaf_id"]].append(row)
    basins = []
    for basin_id, group in sorted(basin_groups.items()):
        states = {(r["bws_raw"], r["bws_cat"], r["bws_label"], r["review_class"]) for r in group}
        assert len(states) == 1, f"Conflicting values within basin {basin_id}"
        raw, category, label, display = next(iter(states))
        footprint = unary_union([geometries[r["feature_id"]] for r in group])
        a = area(footprint)
        basins.append({"pfaf_id": basin_id, "fragment_count": len(group), "bws_raw": raw,
                       "bws_cat": category, "bws_label": label, "review_class": display,
                       "haiti_area_km2": a, "percent_of_boundary": 100 * a / total,
                       "percent_of_valid_coverage": 100 * a / valid_area,
                       "source_feature_ids": [r["feature_id"] for r in group]})
    classes = []
    for label in sorted({r["review_class"] for r in valid_rows}):
        footprint = unary_union([geometries[r["feature_id"]] for r in valid_rows if r["review_class"] == label])
        a = area(footprint)
        classes.append({"class": label, "area_km2": a, "percent_of_boundary": a / total * 100,
                        "percent_of_valid_coverage": a / valid_area * 100})
    unknown_source = area(covered.difference(valid))
    uncovered = area(aoi.difference(covered))
    assert abs(total - valid_area - unknown_source - uncovered) < 1e-3
    assert abs(sum(b["haiti_area_km2"] for b in basins) - valid_area) < 1e-3

    # A separate ellipsoidal-area sensitivity check; reported area convention stays EPSG:6933.
    geod = Geod(ellps="WGS84")
    parts = [aoi] if aoi.geom_type == "Polygon" else list(aoi.geoms)
    geodesic_km2 = sum(abs(geod.geometry_area_perimeter(orient(g, sign=1))[0]) for g in parts) / 1e6
    normal = all(r["decode_state"] == "numeric" for r in valid_rows)
    diagnostic_means = None
    if normal:
        diagnostic_means = {
            "unweighted_fragment_mean": sum(r["bws_raw"] for r in valid_rows) / len(valid_rows),
            "unweighted_distinct_basin_mean": sum(b["bws_raw"] for b in basins) / len(basins),
            "covered_land_area_weighted_mean": sum(b["bws_raw"] * b["haiti_area_km2"] for b in basins) / valid_area,
            "interpretation": "Diagnostic only; not a national demand/supply ratio or accepted classifier."
        }
    result = {
        "scope": "Haiti boundary coverage inspection; not opportunity-space or infrastructure exposure",
        "runtime_ready": False, "area_crs": "EPSG:6933", "boundary_area_km2": total,
        "source_selected_features": len(features), "positive_area_features": len(rows),
        "valid_fragments": len(valid_rows), "distinct_valid_basins": len(basins),
        "covered_area_km2": covered_area, "valid_area_km2": valid_area,
        "valid_percent_of_boundary": valid_area / total * 100,
        "source_nodata_area_km2": unknown_source, "uncovered_area_km2": uncovered,
        "unknown_percent_of_boundary": (unknown_source + uncovered) / total * 100,
        "fragment_overlap_km2": overlap, "excluded_after_clip": excluded,
        "basins": basins, "classes": classes, "mean_diagnostics": diagnostic_means,
        "source_country_counts_positive_area": dict(Counter(r["gid_0"] for r in rows)),
        "source_country_areas_km2": {k: sum(r["clipped_area_km2"] for r in rows if r["gid_0"] == k)
                                     for k in sorted({r["gid_0"] for r in rows})},
        "boundary_geodesic_area_km2": geodesic_km2,
        "boundary_area_method_difference_percent": (total - geodesic_km2) / geodesic_km2 * 100,
        "versions": {"shapely": shapely.__version__, "pyproj": pyproj.__version__},
        "input_sha256": {"boundary": digest(boundary_path), "aqueduct_subset": hashlib.sha256(source_bytes).hexdigest(),
                         "class_rules_csv": digest(ROOT / "priority/classifications/rules.csv"),
                         "binding_candidates_csv": digest(ROOT / "priority/bindings/candidates.csv")},
        "fragments": rows
    }
    Path(output).write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({k: v for k, v in result.items() if k not in {"fragments", "basins"}}, indent=2))


if __name__ == "__main__":
    main(sys.argv[1])
