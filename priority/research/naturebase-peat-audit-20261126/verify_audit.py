"""Check recorded evidence consistency; no analytical thresholds or rules."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent


def read(name):
    return json.loads((root / name).read_text())


for prefix in ["wet_per", "wet_ipm"]:
    inspection = read(f"{prefix}/inspection.json")
    raster = inspection["rasters"][0]
    summary = raster["haiti_cell_centre_summary"]
    assert summary["valid"] == summary["zero"] == raster["haiti_cell_centres"] == 28815
    assert summary["positive"] == summary["negative"] == raster["haiti_missing_cells"] == 0
    points = [p for p in read(f"{prefix}/{prefix}_tco2eha_samples.json") if "landcover" in p]
    assert len(points) == len({p["id"] for p in points}) == 1440
    assert all(p["value"] == 0 for p in points)
    assert len({(p["row"], p["col"]) for p in points}) == raster["unique_sample_pixels"] == 1292
    assert len({p["landcover"] for p in points}) == 9
    for count in raster["stratified_summary"].values():
        assert count["valid"] == count["zero"] == 160
    tables = read(f"{prefix}/haiti_tables.json")
    assert [len(tables[f"adm{i}"]) for i in range(3)] == [1, 10, 42]
    assert all(row[prefix + "_tco2e"] == row[prefix + "_ha"] == "NA"
               for rows in tables.values() for row in rows)
    selected = read(f"{prefix}/acquisition.json")["selected"]
    source_raster = next(m for m in selected if m["name"] == raster["member"])
    assert source_raster["sha256"] == raster["sha256"]
    assert all(m["crc32_checked"] for m in selected)
    assert read("positive_controls.json")[prefix]["value"] > 0

drainage, peat = read("drainage_checks.json")["results"]
assert drainage["unmasked_counts"] == {"cropland": 0, "grassland": 0}
assert peat["unmasked_counts"] == {"b1": 266}
assert peat["value_histogram"]["b1"] == {"1": 266, "null": 23056}
layers = read("peatmap_checks.json")["layers"]
assert sum(layer["positive_area_intersection_count"] for layer in layers) == 171
assert all(layer["total_features_before_filter"] >= layer["bbox_candidates"]
           >= layer["haiti_intersection_count"] for layer in layers)
assert read("provenance.json")["runtime_ready"] is False
manifest = read("manifest.json")
for name, expected in manifest.items():
    assert hashlib.sha256((root / name).read_bytes()).hexdigest() == expected, name
print(f"PASS: two pathway audits, 106 Haiti table rows, peat/drainage checks; {len(manifest)} file hashes")
