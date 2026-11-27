"""Verify inspection records without inferring model validity or zero coverage."""
from pathlib import Path
import hashlib
import json

root = Path(__file__).resolve().parent


def read(name):
    return json.loads((root / name).read_text(), parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))


report = read("biochar_checks.json")
for raster, valid, missing, crop_positive in zip(report["rasters"], [314, 281], [15, 48], [156, 149]):
    assert raster["boundary_cells"] == valid + missing == 329
    assert raster["positive"] == raster["valid"] == valid
    assert raster["missing"] == missing
    assert raster["zero"] == raster["negative"] == 0
    assert raster["nodata"] == "NaN"
    points = read(raster["file"] + "_samples.json")
    assert len(points) == len({p["id"] for p in points}) == 1440
    assert len({(p["row"], p["col"]) for p in points}) == 340
    crop = [p for p in points if p["landcover"] == 40]
    assert len(crop) == 160
    assert sum(p["value"] is not None and p["value"] > 0 for p in crop) == crop_positive
assert report["constrained_exceeds_technical_cells"] == 0
checks = read("component_checks.json")
assert {s["scenario"] for s in checks["scenarios"]} == {"crop_MG", "crop_I", "crop_MGI"}
assert all("not found" in s["error"] for s in checks["scenarios"])
provenance = read("provenance.json")
assert provenance["soil_approval"]["answer"] == "Approve these downloads and licence"
assert provenance["soil_download_status"] in {"haiti_windows_checked_full_input_joint_transferring", "all_originals_acquired_checked"}
soil = read("soil_window_checks.json")
assert len(soil["rasters"]) == 3
sample_sets = {}
for raster in soil["rasters"]:
    stat = raster["haiti_statistics"]
    assert raster["boundary_cells"] == stat["valid"] + raster["missing"] == 448992
    assert stat["valid"] == stat["positive"] == 80187
    assert stat["zero"] == stat["negative"] == 0
    assert raster["missing"] == 368805
    points = read(raster["scenario"] + "_window_samples.json")
    assert len(points) == len({p["id"] for p in points}) == 1440
    assert len({(p["row"], p["col"]) for p in points}) == raster["unique_sample_cells"] == 1429
    crop = [p for p in points if p["landcover"] == 40]
    assert len(crop) == 160
    assert sum(p["value"] is not None for p in crop) == 49
    assert sum(p["value"] is None for p in crop) == 111
    sample_sets[raster["scenario"]] = {p["id"]: p["value"] for p in points}
comparison = soil["joint_vs_sum"]
assert comparison["mask_disagreement_cells"] == 0
assert comparison["common_valid_cells"] == 80187
assert comparison["joint_minus_MG_minus_I"]["positive"] == 80187
assert comparison["within_1e_minus_5_MgC_per_ha"] == 0
for pid, mg in sample_sets["crop_MG"].items():
    inp, joint = (sample_sets[key][pid] for key in ["crop_I", "crop_MGI"])
    assert (mg is None) == (inp is None) == (joint is None)
    if mg is not None:
        assert joint - mg - inp > 1e-5
        assert 1.0608 < joint / (mg + inp) < 1.1066
mg_file = soil["rasters"][0]
assert mg_file["md5"] == provenance["soil_producer_md5"][mg_file["file"]]
if provenance["soil_download_status"] == "all_originals_acquired_checked":
    originals = read("soil_raster_checks.json")
    assert originals["joint_vs_sum"] == soil["joint_vs_sum"]
    for raster, subset in zip(originals["rasters"], soil["rasters"]):
        assert raster["md5"] == provenance["soil_producer_md5"][raster["file"]]
        assert raster["haiti_statistics"] == subset["haiti_statistics"]
        assert raster["sample_statistics"] == subset["sample_statistics"]
assert read("provenance.json")["runtime_ready"] is False
manifest = read("manifest.json")
for name, expected in manifest.items():
    assert hashlib.sha256((root / name).read_bytes()).hexdigest() == expected, name
print(f"PASS: biochar masks, sample counts and comparison; soil masks, non-additivity, approval and acquisition scope verified; {len(manifest)} hashes")
