"""Verify the bounded 27 November Aqueduct/food research snapshots offline."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    names = ("aqueduct-haiti-audit-20261127", "food-alternatives-audit-20261127")
    for name in names:
        folder = ROOT / name
        manifest = json.loads((folder / "manifest.json").read_text())
        for filename, expected in manifest.items():
            assert digest(folder / filename) == expected, f"Changed snapshot: {name}/{filename}"
        for script in folder.glob("*.py"):
            compile(script.read_text(), str(script), "exec")
    water = json.loads((ROOT / names[0] / "inspection.json").read_text())
    assert water["runtime_ready"] is False
    assert water["input_sha256"]["boundary"] == digest(ROOT / "haiti-diagnostic-inputs-20261126/boundary.json")
    assert water["input_sha256"]["class_rules_csv"] == digest(ROOT.parent / "classifications/rules.csv")
    assert water["input_sha256"]["binding_candidates_csv"] == digest(ROOT.parent / "bindings/candidates.csv")
    assert water["distinct_valid_basins"] == len(water["basins"]) == 2
    assert water["valid_fragments"] == sum(b["fragment_count"] for b in water["basins"]) == 42
    total = water["boundary_area_km2"]
    assert abs(total - water["valid_area_km2"] - water["source_nodata_area_km2"] - water["uncovered_area_km2"]) < 1e-3
    food = json.loads((ROOT / names[1] / "inspection.json").read_text())
    acquisition = json.loads((ROOT / names[1] / "acquisition.json").read_text())
    assert food["boundary_sha256"] == water["input_sha256"]["boundary"]
    assert food["runtime_ready"] is False and food["approved_chronic_mapping_applicable"] is False
    for name, value in food["input_sha256"].items():
        assert acquisition["members"][name] == value
    scenarios = food["fews"]["scenarios"]
    assert {s["scenario"] for s in scenarios} == {"CS", "ML1", "ML2"}
    assert sum(s["features"] for s in scenarios) == food["fews"]["feature_count"]
    assert all(s["overlap_reconciled"] is False for s in scenarios)
    assert food["wdi"]["grain"] == "national" and food["wdi"]["averaging_interval_verified"] is False
    print("Verified two frozen Haiti research audits; no runtime or class acceptance asserted.")


if __name__ == "__main__":
    main()
