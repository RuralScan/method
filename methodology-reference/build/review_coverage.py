"""Read-only, deduplicated coverage of a pinned official review queue.

The queue owns scope and review status. This module does not synthesise rows, infer
child applicability from broader evidence, or convert personal votes into consensus.
It intentionally has no dependency on the historical recipe edition or page renderer.
"""

import hashlib
import json
from collections import Counter
from functools import cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PIN = json.loads((ROOT / "review-coverage-pin.json").read_text())
URL = f"https://raw.githubusercontent.com/{PIN['repository']}/{PIN['revision']}/{PIN['path']}"
CACHE = ROOT / ".cache" / "review-coverage" / (PIN["revision"] + ".json")
LANES = {
    "all": "All findings",
    "T4": "T4 suitability",
    "effects": "T3/T6 effects · all collected",
    "M2b": "M2b operational feasibility",
    "other": "Other registered evidence",
    "T3": "Cited by T3 rows",
    "T6": "Cited by T6 rows",
}
STATES = {
    "retained": "Total retained",
    "reviewed_kept": "Reviewed and kept",
    "awaiting": "Awaiting review or resolution",
    "pending": "Pending review",
    "held": "Held · unresolved",
    "rejected": "Rejected · excluded",
    "all": "All registered, including rejected",
}
RELATIONS = {
    "included": "This scope and its children",
    "broader": "Broader context · not added to this total",
    "legacy": "Earlier scope · needs source-scope review",
}
DEFINITIONS = {
    "reviewed_kept": "Official finding status is reviewed_kept. Personal votes are not consensus approval.",
    "retained_total": "reviewed_kept + pending + held; rejected findings are excluded from this denominator.",
    "awaiting": "pending + held. Holds remain retained but unresolved; they are not counted as reviewed and kept.",
    "registered_total": "retained_total + rejected. Rejected findings remain accessible for audit.",
    "scope": "Unique evidence_id across this node and descendants. Never sum child counts to derive a parent.",
    "broader": "Direct findings at ancestor nodes; contextual support, not evidence assigned to the child.",
    "legacy": "Pointers to earlier family scopes awaiting source-scope review; not silently assigned to new families.",
    "effects": "All nbs_effect and asset_vulnerability findings, including uncited and pending findings.",
    "T3_T6": "Cited subsets use the queue membership lists. They can overlap and do not exhaust collected effects.",
    "meaning": "Coverage and review progress, not strength of evidence, synthesis acceptance or runtime readiness.",
}


def verified(raw):
    if hashlib.sha256(raw).hexdigest() != PIN["sha256"]:
        raise ValueError("Review queue does not match review-coverage-pin.json")
    return json.loads(raw)


@cache
def load():
    if not CACHE.is_file():
        raise ValueError(
            "Review snapshot missing. Run python build/fetch_package.py first."
        )
    return Coverage(verified(CACHE.read_bytes()))


class Coverage:
    def __init__(self, queue):
        hierarchy = queue["evidence_hierarchy"]
        self.nodes = hierarchy["nodes"]
        self.views = hierarchy["coverage"]
        self.findings = {}
        units = queue["registers"]["EV_evidence_register"]
        sources = {s["source_id"]: s for s in queue["registers"]["SRC_source_register"]}
        if len({u["evidence_id"] for u in units}) != len(units):
            raise ValueError("Duplicate evidence_id in review queue")
        if {u["evidence_id"] for u in units} != set(hierarchy["findings"]):
            raise ValueError("Hierarchy does not cover every registered finding")
        cited = {t: set(queue["membership"][t]) for t in ("T3", "T6")}
        for u in units:
            eid = u["evidence_id"]
            h = hierarchy["findings"][eid]
            if h["review_status"] not in {
                "reviewed_kept",
                "pending",
                "held",
                "rejected",
            }:
                raise ValueError(f"Unknown finding review status: {eid}")
            lane = {
                "structural_suitability": "T4",
                "operational_risk": "M2b",
                "nbs_effect": "effects",
                "asset_vulnerability": "effects",
            }.get(u.get("use_role"), "other")
            self.findings[eid] = {
                "evidence_id": eid,
                "practice": u["nbs_id"],
                "node": h["node"],
                "scope_status": h["scope_status"],
                "status": h["review_status"],
                "lanes": ["all", lane] + [t for t in cited if eid in cited[t]],
                "source_id": u["source_id"],
                "citation": sources[u["source_id"]].get("citation", u["source_id"]),
                "variable": u.get("variable", ""),
                "url": "https://ruralscan.github.io/method/dashboard.html#review-evidence="
                + eid,
            }
        # Fail closed if published roll-ups and their underlying IDs disagree.
        for node, expected in self.views.items():
            counts = self.counts(node)
            for field in (
                "reviewed_kept",
                "retained_total",
                "pending",
                "held",
                "rejected",
            ):
                if counts[field] != expected[field]:
                    raise ValueError(f"Queue hierarchy count mismatch: {node} {field}")
            if counts["registered_total"] != expected["total"]:
                raise ValueError(f"Queue hierarchy total mismatch: {node}")
            if self.ids(node) & self.ids(node, relation="broader"):
                raise ValueError(f"Broader context included in child count: {node}")

    def ids(self, node="", lane="all", relation="included"):
        if not node:
            values = set(self.findings) if relation == "included" else set()
        else:
            view = self.views[node]
            if relation == "included":
                values = set(view["direct_evidence_ids"]) | set(
                    view["descendant_evidence_ids"]
                )
            else:
                values = set(
                    view[
                        {
                            "broader": "broader_evidence_ids",
                            "legacy": "legacy_scope_evidence_ids",
                        }[relation]
                    ]
                )
        return {eid for eid in values if lane in self.findings[eid]["lanes"]}

    def counts(self, node="", lane="all", relation="included"):
        ids = self.ids(node, lane, relation)
        c = Counter(self.findings[eid]["status"] for eid in ids)
        return {
            "registered_total": len(ids),
            "retained_total": len(ids) - c["rejected"],
            "reviewed_kept": c["reviewed_kept"],
            "pending": c["pending"],
            "held": c["held"],
            "awaiting": c["pending"] + c["held"],
            "rejected": c["rejected"],
        }

    def metadata(self):
        return {
            "format": "ruralscan.review-coverage.v1",
            "source": {**PIN, "url": URL},
            "definitions": DEFINITIONS,
            "lanes": LANES,
            "states": STATES,
            "relations": RELATIONS,
            "csv_schema": {
                "primary_key": ["node", "relation", "lane"],
                "fields": {
                    "node": {
                        "type": "string",
                        "description": "Hierarchy key; empty means all practices.",
                    },
                    "relation": {"type": "string", "enum": list(RELATIONS)},
                    "lane": {"type": "string", "enum": list(LANES)},
                    **{
                        field: {"type": "integer", "minimum": 0}
                        for field in (
                            "registered_total",
                            "retained_total",
                            "reviewed_kept",
                            "pending",
                            "held",
                            "awaiting",
                            "rejected",
                        )
                    },
                },
            },
            "historical_recipe_edition": "Separate snapshot; not a claim that these findings were synthesised.",
        }

    def summary(self):
        rows = []
        for node in [""] + sorted(self.nodes):
            for relation in RELATIONS if node else ["included"]:
                for lane in LANES:
                    rows.append(
                        {
                            "node": node,
                            "relation": relation,
                            "lane": lane,
                            **self.counts(node, lane, relation),
                        }
                    )
        return {"metadata": self.metadata(), "rows": rows}

    def export(self):
        return {
            "metadata": self.metadata(),
            "nodes": self.nodes,
            "scopes": self.views,
            "findings": list(self.findings.values()),
        }
