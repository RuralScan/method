"""Publish review inputs from the pinned evidence contract; never author rules."""

import hashlib
import importlib
import json
from pathlib import Path
import subprocess
import sys


def blob(repo, revision, path):
    return subprocess.check_output(["git", "-C", str(repo), "show", f"{revision}:{path}"])


def payload(repo, revision):
    """Use the official validator and evaluator from an exact, verified checkout."""
    repo = Path(repo).resolve()
    head = subprocess.check_output(["git", "-C", str(repo), "rev-parse", "HEAD"], text=True).strip()
    if head != revision:
        raise ValueError("Override evidence checkout differs from the operating pin")
    paths = subprocess.check_output([
        "git", "-C", str(repo), "ls-tree", "-r", "--name-only", revision,
        "suitability/overrides", "workflows/t4_synthesis", "workflows/synthesis/core.py",
    ], text=True).splitlines()
    for path in paths:
        if (repo / path).read_bytes() != blob(repo, revision, path):
            raise ValueError(f"Override input differs from pinned bytes: {path}")
    sys.path.insert(0, str(repo / "workflows"))
    try:
        candidates = importlib.import_module("t4_synthesis.override_candidates")
        profiles = importlib.import_module("t4_synthesis.profiles")
        for module in (candidates, profiles):
            if not Path(module.__file__).resolve().is_relative_to(repo):
                raise ValueError("Override evaluator loaded from another checkout")
        folder = repo / "suitability/overrides"
        manifest = candidates.generate(folder, check=True)
        records = candidates.records(folder)
        summaries = []
        for record in records:
            curves = []

            def visit(node):
                if node["kind"] == "minimum":
                    for child in node["children"]:
                        visit(child)
                    return
                # Plot domain is display-only. It neither defines tails nor a screen.
                lo = 0 if node["kind"] == "log_logistic" else node["x20"] - (node["x80"] - node["x20"]) / 2
                hi = node["x80"] * 1.5
                xs = sorted({lo + (hi - lo) * i / 100 for i in range(101)} | {node["x20"], node["x80"]})
                curves.append(dict(node, points=[[x, profiles.smooth(node["kind"], node["x20"], node["x80"], x)] for x in xs]))

            if record["profile"]["type"] == "composite_scoping":
                visit(record["profile"]["score"])
            name = record["id"] + ".json"
            summaries.append({"candidate": record, "curves": curves,
                              "sha256": hashlib.sha256((folder / "candidates" / name).read_bytes()).hexdigest()})
        examples = []
        for name in ("fmnr-dan-saga", "mangrove-partial-unit"):
            sample = json.loads((folder / "examples" / (name + ".json")).read_bytes())
            matching = [r for r in records if any(s["family_id"] == sample["context"]["family_id"] for s in r["profile"]["scope"])]
            if len(matching) != 1:
                raise ValueError("Example does not identify one pending candidate")
            examples.append({"id": name, "candidate_id": matching[0]["id"], "inputs": sample,
                             "result": profiles.evaluate_candidate(matching[0], sample["values"], sample["context"])})
        return {"format": "ruralscan.override-review.v1", "revision": revision,
                "contract_sha256": hashlib.sha256((repo / "workflows/t4_synthesis/contract.json").read_bytes()).hexdigest(),
                "source_csv": f"https://github.com/RuralScan/evidence/blob/{revision}/suitability/overrides/overrides.csv",
                "summary_url": f"https://github.com/RuralScan/evidence/blob/{revision}/suitability/overrides/README.md",
                "manifest": manifest, "records": summaries, "examples": examples,
                "scientific_acceptance": "pending", "runtime_implemented": False, "activate": False}
    finally:
        sys.path.pop(0)


def build():
    import core

    model = payload(core.EVIDENCE, core.EVIDENCE_OPERATING)
    core.FILES["data/t4-overrides.json"] = json.dumps(model, indent=2, ensure_ascii=False, allow_nan=False) + "\n"
    for name in ("override-review.js", "override-review.css"):
        core.FILES[name] = Path(__file__).with_name(name).read_text()
    mount = ('<link rel="stylesheet" href="override-review.css">'
             '<div class="override-review" data-override-review data-source="data/t4-overrides.json">'
             '<p role="status">Loading pinned pending rule proposals…</p></div>'
             '<script src="override-review.js" defer></script>')
    target = "ch-t4-overrides.html"
    placeholder = '<div id="override-catalogue-mount"></div>'
    if core.PAGES[target].count(placeholder) != 1:
        raise ValueError("Pending override chapter must have one catalogue mount")
    core.PAGES[target] = core.PAGES[target].replace(placeholder, mount)
    return model
