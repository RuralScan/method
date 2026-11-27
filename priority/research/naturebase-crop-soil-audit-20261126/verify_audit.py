"""Check inspection consistency, preserving missingness and published totals."""
import hashlib
import json
import math
from pathlib import Path

root = Path(__file__).resolve().parent


def read(name):
    return json.loads((root / name).read_text())


raster = read("crp_scc/inspection.json")["rasters"][0]
summary = raster["haiti_cell_centre_summary"]
assert raster["haiti_cell_centres"] == summary["valid"] == 28815
assert summary["positive"] == 6073 and summary["zero"] == 22742
assert summary["negative"] == raster["haiti_missing_cells"] == 0
points = [p for p in read("crp_scc/crp_scc_tco2eha_samples.json") if "landcover" in p]
assert len(points) == len({p["id"] for p in points}) == 1440
assert len({(p["row"], p["col"]) for p in points}) == raster["unique_sample_pixels"] == 1292
crop = [p for p in points if p["landcover"] == 40]
assert len(crop) == 160 and sum(p["value"] > 0 for p in crop) == 144
assert all(p["value"] is not None for p in points)
tables = read("crp_scc/haiti_tables.json")
assert [len(tables[f"adm{i}"]) for i in range(3)] == [1, 10, 42]
missing = [r for r in tables["adm2"] if r["crp_scc_tco2e"] == "NA"]
assert len(missing) == 1 and missing[0]["crp_scc_ha"] == "NA"
assert missing[0]["adm2_id"] == "57096268B27125670128287"
assert float(tables["adm0"][0]["crp_scc_tco2e"]) == 97016.440991107
recorded = read("summary.json")
for level, rows in tables.items():
    for field in ["crp_scc_tco2e", "crp_scc_ha"]:
        values = [float(r[field]) for r in rows if r[field] != "NA"]
        saved = recorded["administrative_sums"][level][field]
        assert len(values) == saved["valid_records"]
        assert math.isclose(sum(values), saved["sum"], rel_tol=1e-12)
acquisition = read("crp_scc/acquisition.json")
assert len(acquisition["members"]) == 73 and len(acquisition["selected"]) == 5
assert all(m["crc32_checked"] for m in acquisition["selected"])
member = next(m for m in acquisition["selected"] if m["name"] == raster["member"])
assert member["sha256"] == raster["sha256"]
assert read("provenance.json")["runtime_ready"] is False
manifest = read("manifest.json")
for name, expected in manifest.items():
    assert hashlib.sha256((root / name).read_bytes()).hexdigest() == expected, name
print(f"PASS: Haiti raster/sample support, 53 table rows, one missing admin2, arithmetic; {len(manifest)} file hashes")
