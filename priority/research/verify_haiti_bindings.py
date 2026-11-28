"""Verify the bounded 27 November Aqueduct, food-search and IPC/ENSSAN snapshots offline."""
import hashlib
import json
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    names = ("aqueduct-haiti-audit-20261127", "food-alternatives-audit-20261127",
             "ipc-enssan-audit-20261127")
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
    ipc = json.loads((ROOT / names[2] / "inspection.json").read_text())
    ipc_acquisition = json.loads((ROOT / names[2] / "acquisition.json").read_text())
    assert ipc["runtime_ready"] is False and ipc["four_class_decision"] == "proposed"
    assert ipc["boundary_sha256"] == water["input_sha256"]["boundary"]
    for name, value in ipc["input_sha256"].items():
        assert ipc_acquisition["members"][name] == value
    assert len(ipc["areas"]) == ipc["unique_assessment_areas"] == 30
    assert len({a["area_id"] for a in ipc["areas"]}) == 30
    assert sum(a["population"] for a in ipc["areas"]) == ipc["population_deduplicated"] == ipc["excel_totals"]["Current - Est Pop"]
    assert sum(a["phase3_plus_population"] for a in ipc["areas"]) == ipc["phase3_plus_population_deduplicated"] == ipc["excel_totals"]["Current - Phase 3+"]
    assert sum(not a["has_polygon"] for a in ipc["areas"]) == ipc["point_only_area_count"] == 8
    assert len(ipc["invalid_polygons"]) == 2 and ipc["geometry_repaired"] is False
    assert ipc["enssan"]["geographic_rows"] == 48 and ipc["enssan"]["missing_cells"] == 2
    assert ipc["enssan"]["geographies_2025"] == 12 and ipc["enssan"]["geographic_join_performed"] is False
    for name in ('food-insecurity-approval-20261127', 'bii-haiti-audit-20261127'):
        folder = ROOT / name
        for filename, expected in json.loads((folder / 'manifest.json').read_text()).items():
            assert digest(folder / filename) == expected, f'Changed snapshot: {name}/{filename}'
    approval_folder = ROOT / 'food-insecurity-approval-20261127'
    approval = json.loads((approval_folder / 'decision.json').read_text())
    assert approval['interpretation_status'] == 'approved' and approval['runtime_ready'] is False
    assert approval['source_proposal_sha256'] == digest(ROOT / 'ipc-enssan-audit-20261127/four_class_proposal.csv')
    assert approval['source_inspection_sha256'] == digest(ROOT / 'ipc-enssan-audit-20261127/inspection.json')
    assert approval['approved_crosswalk_sha256'] == digest(approval_folder / 'classes.csv')
    with (approval_folder / 'classes.csv').open() as stream:
        approved = list(csv.DictReader(stream))
    assert [r['native_ipc_acute_area_phase'] for r in approved] == ['1','2','3','4','5']
    assert all(r['interpretation_status'] == 'approved' for r in approved)
    assert [r['ordinal_code'] for r in approved] == ['0','1','2','3','3']
    assert [r['critical_phase_5'] for r in approved] == ['false','false','false','false','true']
    assert approval['phase_5_flag_required'] is True
    bii_folder = ROOT / 'bii-haiti-audit-20261127'
    bii = json.loads((bii_folder / 'inspection.json').read_text())
    contract = json.loads((bii_folder / 'contract.json').read_text())
    assert bii['source_sha256'] == contract['source_sha256']
    assert bii['contract_sha256'] == digest(bii_folder / 'contract.json')
    assert bii['classes_sha256'] == digest(bii_folder / 'classes.csv')
    assert bii['boundary_sha256'] == water['input_sha256']['boundary']
    assert bii['runtime_ready'] is False and bii['combined_biodiversity'].startswith('Not assessed')
    assert len(bii['cells']) == bii['intersecting_native_cells'] == 453
    assert sum(c['class'] is not None for c in bii['cells']) == bii['valid_native_cells'] == 443
    assert abs(sum(c['haiti_area_km2'] for c in bii['cells']) - bii['boundary_area_km2']) < 1e-3
    assert abs(sum(c['area_km2'] for c in bii['classes']) - bii['valid_area_km2']) < 1e-3
    for cell in bii['cells']:
        if cell['class'] is not None:
            assert abs(cell['bii_percent'] + cell['depletion'] - contract['reference']) < 1e-12
    compile((bii_folder / 'probe.py').read_text(), str(bii_folder / 'probe.py'), 'exec')
    print('Verified four frozen Haiti research audits and approved food crosswalk with Phase 5 flag; no runtime release asserted.')


if __name__ == "__main__":
    main()
