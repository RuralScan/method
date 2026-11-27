"""Reproduce IPC/ENSSAN acquisition diagnostics; no runtime binding is produced.

Usage: uv run --with shapely==2.1.2 --with pyproj==3.7.2 --with openpyxl==3.1.5 python analyze.py SOURCE_DIR OUTPUT.json
"""
from collections import Counter, defaultdict
import csv
import hashlib
import json
from pathlib import Path
import sys

import openpyxl
import pyproj
from pyproj import Transformer
import shapely
from shapely.geometry import shape
from shapely.ops import transform, unary_union
from shapely.validation import explain_validity

HERE = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(source_dir, output):
    source_dir = Path(source_dir)
    acquisition = json.loads((HERE / "acquisition.json").read_text())
    source_names = ("ipc_haiti_202610.geojson", "ipc_haiti_population.xlsx",
                    "enssan-pdf-page-122-tables.json", "enssan-pdf-page-117-tables.json")
    for name in source_names:
        assert digest(source_dir / name) == acquisition["members"][name], name
    boundary_path = HERE.parent / "haiti-diagnostic-inputs-20261126/boundary.json"
    assert digest(boundary_path) == acquisition["boundary_sha256"]
    data = json.loads((source_dir / source_names[0]).read_text())
    features = data["features"]
    groups = defaultdict(list)
    for feature in features:
        p = feature["properties"]
        assert p["country"] == "HT" and p["condition"] == "A"
        groups[p["area_id"]].append(feature)
    with (HERE / "four_class_proposal.csv").open() as stream:
        proposal = {int(r["native_ipc_acute_area_phase"]): r for r in csv.DictReader(stream)}
    assert set(proposal) == set(range(1, 6))
    assert all(r["decision_status"] == "proposed" for r in proposal.values())

    workbook = openpyxl.load_workbook(source_dir / source_names[1], read_only=True, data_only=True)
    table = list(workbook["Population Table"].values)
    headers = table[0]
    excel = [dict(zip(headers, row)) for row in table[1:]]
    totals = next(row for row in excel if row["Area Name"] == "ANALYSIS TOTALS")
    leaves = {r["Area Name"].strip(): r for r in excel if r["Current - Phase"] is not None}
    assert len(leaves) == len(groups)
    compared_fields = ["population", "phase", "from_date", "thru_date", "phase3_plus_population",
                       "confidence_level", "hfa_value", "risk_of_famine"]
    compared_fields += [f"phase{i}_population" for i in range(1, 6)]
    areas, duplicates, invalid, valid_polygons = [], [], [], []
    for area_id, group in sorted(groups.items()):
        p = group[0]["properties"]
        assert all(all(f["properties"][k] == p[k] for k in compared_fields) for f in group)
        row = leaves[p["area_name"]]
        assert int(row["Current - Est Pop"]) == p["population"]
        assert row["Current - Phase"] == p["overall_phase_label"] == f"P{p['phase']}"
        assert row["Current - From Date"] == p["from_date"]
        assert row["Current - Thru Date"] == p["thru_date"]
        assert row["Current - Phase 3+"] == p["phase3_plus_population"]
        for phase in range(1, 6):
            assert row[f"Current - Phase {phase}"] == p[f"phase{phase}_population"]
        kinds = [f["geometry"]["type"] for f in group]
        polygon_support = any(k in ("Polygon", "MultiPolygon") for k in kinds)
        if len(group) > 1:
            duplicates.append({"area_id": area_id, "name": p["area_name"], "geometry_types": kinds})
        for feature in group:
            geometry = shape(feature["geometry"])
            if geometry.geom_type not in ("Polygon", "MultiPolygon"):
                continue
            if geometry.is_valid:
                valid_polygons.append(geometry)
            else:
                invalid.append({"area_id": area_id, "name": p["area_name"],
                                "reason": explain_validity(geometry)})
        areas.append({"area_id": area_id, "name": p["area_name"], "native_phase": p["phase"],
                      "population": p["population"], "phase3_plus_population": p["phase3_plus_population"],
                      "geometry_types": kinds, "has_polygon": polygon_support,
                      "confidence_level": p["confidence_level"], "hfa_value": p["hfa_value"],
                      "risk_of_famine": p["risk_of_famine"],
                      "proposed_display_class": proposal[p["phase"]]["proposed_display_class"],
                      "proposal_status": "proposed"})
    assert sum(a["population"] for a in areas) == totals["Current - Est Pop"]
    assert sum(a["phase3_plus_population"] for a in areas) == totals["Current - Phase 3+"]
    boundary = json.loads(boundary_path.read_text())
    aoi = unary_union([shape(f["geometry"]) for f in boundary["features"]])
    project = Transformer.from_crs(4326, 6933, always_xy=True).transform

    def area(geometry):
        return transform(project, geometry).area / 1e6

    clips = [g.intersection(aoi) for g in valid_polygons]
    union = unary_union(clips)
    # This is deliberately incomplete: invalid polygons and points are not repaired/buffered.
    valid_subset_coverage = 100 * area(union) / area(aoi)
    overlap = sum(area(g) for g in clips) - area(union)

    with (HERE / "enssan_geographic_prevalence.csv").open() as stream:
        geographic_rows = list(csv.DictReader(stream))
    raw_table = json.loads((source_dir / source_names[2]).read_text())[0]
    extracted = {}
    for row in raw_table[1:]:
        cells = ["".join(v for v in row[i:i + 3] if v) for i in range(0, 15, 3)]
        for year, value in zip((2022, 2023, 2024, 2025), cells[1:]):
            extracted[(cells[0], str(year))] = value.removesuffix("%")
    assert len(extracted) == len(geographic_rows) == 48
    for row in geographic_rows:
        value = row["severe_fies_household_percent"]
        assert extracted[(row["source_geography"], row["year"])] == value
        assert row["value_status"] == ("reported" if value else "not_reported")
        assert not value or 0 <= float(value) <= 100
    latest = [r for r in geographic_rows if r["year"] == "2025"]
    with (HERE / "enssan_national_prevalence.csv").open() as stream:
        national = list(csv.DictReader(stream))
    national_raw = json.loads((source_dir / source_names[3]).read_text())[0]
    assert len(national) == len(national_raw) - 1 == 4
    for saved, raw in zip(national, national_raw[1:]):
        cells = ["".join(v for v in raw[i:i + 3] if v).replace(",", ".") for i in range(0, 15, 3)]
        assert list(saved.values()) == cells
    national_2025 = next(r for r in national if r["year"] == "2025")
    result = {
        "checked_date": "2026-11-27", "runtime_ready": False, "four_class_decision": "proposed",
        "input_sha256": {name: digest(source_dir / name) for name in source_names},
        "boundary_sha256": digest(boundary_path), "source_metadata": data["properties"],
        "feature_count": len(features), "unique_assessment_areas": len(groups),
        "geometry_types": dict(Counter(f["geometry"]["type"] for f in features)),
        "feature_validity_periods": sorted({(f["properties"]["from_date"], f["properties"]["thru_date"]) for f in features}),
        "duplicate_area_representations": duplicates, "invalid_polygons": invalid,
        "population_naive_feature_sum": sum(f["properties"]["population"] for f in features),
        "population_deduplicated": sum(a["population"] for a in areas),
        "phase3_plus_population_deduplicated": sum(a["phase3_plus_population"] for a in areas),
        "unique_area_phase_counts": dict(Counter(a["native_phase"] for a in areas)),
        "point_only_area_count": sum(not a["has_polygon"] for a in areas),
        "point_only_population": sum(a["population"] for a in areas if not a["has_polygon"]),
        "valid_polygons_only_coverage_percent": valid_subset_coverage,
        "valid_polygons_only_overlap_km2": overlap,
        "coverage_warning": "Incomplete diagnostic; invalid polygons excluded, points unbuffered; not full source coverage.",
        "geometry_repaired": False, "area_classes_aggregated": False,
        "excel_totals": totals, "areas": areas,
        "enssan": {"geographic_rows": len(geographic_rows), "missing_cells": sum(not r["severe_fies_household_percent"] for r in geographic_rows),
                   "geographies_2025": len(latest), "geographic_support_counts_2025": dict(Counter(r["geographic_support"] for r in latest)),
                   "national_2025_severe_percent": float(national_2025["severe_percent"]), "weighted_national_reconstruction_possible": False,
                   "source_table1_sample_total": 6500, "source_narrative_sample_total": 6550,
                   "geographic_join_performed": False},
        "versions": {"shapely": shapely.__version__, "pyproj": pyproj.__version__, "openpyxl": openpyxl.__version__},
    }
    Path(output).write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n")
    print(f"Verified {len(groups)} IPC areas against Excel; {len(invalid)} invalid polygons; "
          f"{len(latest)} ENSSAN geographic groups; class proposal remains unapproved.")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
