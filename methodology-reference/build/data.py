"""Load the pinned release and registers once, and index them for the page builders."""

import re
from collections import Counter, defaultdict

from core import (
    EVIDENCE,
    PRACTICE_IDS,
    ROW_TABLES,
    TABLE_FILES,
    pinned_csv,
    pinned_json,
    row_file,
    row_id,
)

ROWS = []
for _p in PRACTICE_IDS:
    for _t in ROW_TABLES:
        for _raw in pinned_json(f"schema/recipes/{_p}/{TABLE_FILES[_t]}"):
            ROWS.append(
                {
                    "table": _t,
                    "practice": _p,
                    "id": row_id(_raw),
                    "family": _raw.get("suitability_family_id") or "",
                    "raw": _raw,
                    "file": row_file(_t, _raw),
                }
            )
ROW_COUNTS = Counter((r["practice"], r["table"]) for r in ROWS)
TABLE_TOTALS = Counter(r["table"] for r in ROWS)

FAM = pinned_json("schema/registers/FAM_family_registry.json")
FAMILIES = defaultdict(list)  # practice -> ordered family ids
FAMILY_ROWS = defaultdict(list)  # family id -> sub-practice records
for _f in FAM:
    if _f["suitability_family_id"] not in FAMILIES[_f["nbs_id"]]:
        FAMILIES[_f["nbs_id"]].append(_f["suitability_family_id"])
    FAMILY_ROWS[_f["suitability_family_id"]].append(_f)
# Families that appear only on rows (for example cross-family context) follow the registered ones.
for _r in ROWS:
    if _r["family"] and _r["family"] not in FAMILIES[_r["practice"]]:
        FAMILIES[_r["practice"]].append(_r["family"])


def family_product(family_id):
    kinds = {f["spatial_product_type"] for f in FAMILY_ROWS.get(family_id, [])}
    return sorted(kinds)


VONT = {
    v["canonical_variable_id"]: v
    for v in pinned_json("schema/registers/VONT_variable_ontology.json")
}
T1 = {d["dataset_id"]: d for d in pinned_csv("schema/T1_data_registry.csv")}
T5 = {v["variable_id"]: v for v in pinned_csv("schema/T5_opportunity_space.csv")}
BIND = pinned_csv("schema/registers/BIND_dataset_binding.csv")
EV = pinned_json("schema/registers/EV_evidence_register.json")
EV_BY_ID = {e["evidence_id"]: e for e in EV}
SRC = pinned_json("schema/registers/SRC_source_register.json")
SRC_BY_ID = {s["source_id"]: s for s in SRC}
SRCH = pinned_json("schema/registers/SRCH_search_register.json")

EV_BY_SOURCE = defaultdict(list)
for _e in EV:
    EV_BY_SOURCE[_e.get("source_id")].append(_e)

ROWS_BY_EV = defaultdict(list)
for _r in ROWS:
    for _i in _r["raw"].get("evidence_ids") or []:
        ROWS_BY_EV[_i].append(_r)
ROWS_BY_SOURCE = defaultdict(list)
for _i, _rows in ROWS_BY_EV.items():
    _s = EV_BY_ID.get(_i, {}).get("source_id")
    for _r in _rows:
        if _r not in ROWS_BY_SOURCE[_s]:
            ROWS_BY_SOURCE[_s].append(_r)


def retained(unit):
    return unit.get("review_state") != "dropped"


def default_binding(variable):
    rows = [
        b for b in BIND if b["variable"] == variable and b["scope_type"] == "global"
    ]
    rows.sort(key=lambda b: int(b["preference_rank"] or 99))
    return rows[0]["dataset_id"] if rows else None


# Function role and readiness are produced with the release and published in the evidence
# repository's recipe tables. Read them from there so this reference never restates them.
_LINE = re.compile(r'^\| \[[^\]]*\]\(\S+ "([^"]+)"\) \|(.*)\|\s*$')
READINESS = {}
for _p in PRACTICE_IDS:
    _in_t4 = False
    for _line in (EVIDENCE / f"publication/recipes/{_p}.md").read_text().splitlines():
        if _line.startswith("## "):
            _in_t4 = "T4" in _line
            continue
        _m = _LINE.match(_line) if _in_t4 else None
        if _m:
            _c = [c.strip() for c in _m.group(2).split("|")]
            if len(_c) == 6:
                READINESS[_m.group(1)] = {
                    "role": _c[1],
                    "calibration": _c[2],
                    "options": _c[3],
                    "selected": _c[4],
                    "validated": _c[5],
                }


def readiness(row):
    return READINESS.get(row["id"])
