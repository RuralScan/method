# Implement a rural scan

Use the Haiti planted-silvoarable agroforestry example to work through one decision: **which locations merit a closer look at terrain and soils, and what information is still needed there?** The published notebook computes a partial first-pass index. The remaining modules below describe how to turn a suitability result into an investment-scoping brief. [Haiti first-pass notebook](https://github.com/RuralScan/runtime/blob/e690d4e413d925c28c273945a5268ddbfb2d67cc/notebooks/01_agroforestry.ipynb)

In the cookbook, choose **Agroforestry → Trees planted on cropland**. In the evidence workbook, inspect its slope mapping (`agroforestry__planted_silvoarable__slope`) and follow a claim to its source and locator. Then use the notebook to see how a particular scoring package combines slope and soil inputs. Record the workbook release and runtime package separately. [Agroforestry recipe](../cookbook/agroforestry.md)

## 1. Check the inputs before making a map

Start with a pinned runtime checkout. This check reads the supplied run configuration and scoring package locally; it needs Git and Python 3.11 or newer. Run these commands in a terminal on macOS or Linux.

```sh
git clone https://github.com/RuralScan/runtime.git rural-runtime
cd rural-runtime
git checkout --detach e690d4e413d925c28c273945a5268ddbfb2d67cc
PYTHONPATH=src python3 - <<'PY'
from pathlib import Path
from nbs_runtime.plan import plan

run = plan(Path("config/runs/agroforestry_planted_first_pass.toml"))
print("Scoring package", run.package_version)
print(*run.holds, sep="\n")
PY
```

Expect scoring package **0.1.5**. The base configuration reports outstanding choices about the AOI boundary and its source, transfer of evidence to Haiti, soil inputs and legal exclusions. Record the actual boundary, dataset choices and decision references for an operational run. A country code can resolve a data binding; it cannot establish that a locally observed response transfers to Haiti. [Run configuration](https://github.com/RuralScan/runtime/blob/e690d4e413d925c28c273945a5268ddbfb2d67cc/config/runs/agroforestry_planted_first_pass.toml)

## 2. Run and interpret the first pass

From the same runtime checkout, install the notebook dependencies in a Python environment and open the notebook.

```sh
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -e '.[geo,gee,viz]' jupyterlab
python -m jupyterlab notebooks/01_agroforestry.ipynb
```

Select the kernel from this environment. In the parameters cell choose `DATA_SOURCE = "synthetic"` for an offline software exercise. To process geographic data, use `"gee"`, authenticate Earth Engine and set your enabled project. Inspect input maps, units, coverage and each reported hold before interpreting the index. [Notebook instructions](https://github.com/RuralScan/runtime/blob/e690d4e413d925c28c273945a5268ddbfb2d67cc/README.md)

With Earth Engine inputs, the quick overview uses an approximate Haiti bounding box, a **5 km grid** and exploratory mode. Its default `HOST_GATE = "skip"` treats every cell as host and leaves legal exclusions unapplied. The offline synthetic run generates artificial host fractions and records `host_gate_applied = true` even when the parameter says `"skip"`. Use the output manifest to identify which inputs and gate produced a map. Its score combines slope (50%), soil organic carbon (25%) and pH (25%). Use the overview to inspect relative terrain-and-soil patterns and sensitivity to class scores. A national estimate of plantable hectares requires a suitable boundary, host-system data, exclusion masks, supported resolution and resolved applicability. The detailed setting applies the host gate at 250 m; check the remaining holds independently. Preserve scored, excluded and unknown pixel states. [Notebook parameters and pixel states](https://github.com/RuralScan/runtime/blob/e690d4e413d925c28c273945a5268ddbfb2d67cc/notebooks/01_agroforestry.ipynb)

## 3. Build the scoping brief

Use one suitability family and one area of interest at a time. When citing a mapping, include its family, geographic context and any conditions on applying it. [Method definitions for the six-practice workbook](https://github.com/RuralScan/method/blob/247d5cf98d3dd6daf010aa5bfe51fad21ea35849/data-model/definition-snapshot.json) · [Field definitions](../data-model/spec.md)

| Module | Analyst action | Output to retain |
|---|---|---|
| M0 · Scope | Select the practice in T0, family in FAM, spatial context in T7 and inputs in T1. Resolve dataset bindings for the AOI. | Decision question, boundary source, grid, dates, product type and input versions. |
| M1 · Opportunity | Use T4 mappings supported for that family and target context. Apply host requirements and hard exclusions. | Suitability layer with coverage, exclusions and unresolved inputs. For linear products use the recipe's reporting unit. |
| M2 · Livelihood risk | Use T2 to characterise hazard and livelihood exposure. State the period and scenario. | A map of climate-related need in the rural landscape. |
| M2b · Investment risk | Use T2 hazards and T3 asset threats; inspect implementation constraints such as access and tenure. | A separate project-risk flag or filter. Keep its score out of the livelihood-need sum. |
| M3 · Characterise | Summarise T5 people, production, equity and other descriptors within the opportunity space; retain geography and denominators. | Counts, shares or distributions with units, spatial support and missing-data coverage. |
| M4 · Prioritise | Use eligible T5 priorities. Choose representatives for correlated indicators and state weights. Repeat with plausible alternate weights. | Ranked areas and a record of which priorities or assumptions change their rank. |
| M5 · Compare responses | Read hazard responses in T3, scorecard effects in T6 and indicative costs in T6E where available. Check evidence IDs, confidence and context. | A comparison of expected benefits, trade-offs and evidence gaps for each practice. |
| M6 · Hand off | For each promising area, identify local checks on land use, tenure, safeguards and design. | Shortlist, maps and explicit questions for field or feasibility work. |

Keep the run configuration, input and package identifiers, output manifest and map legends together. For each number in the brief, identify its unit, denominator and coverage. For each analytical rule, follow its evidence IDs to the original claim and locator. The bench-terrace example shows why a reported rainfall range can inform a local question while calibration stays on hold. [Read the recipe row](read-a-suitability-recipe.md) · [Replay its evidence extraction](https://github.com/RuralScan/evidence/blob/f83b0c017878b7d0edc5c4e0959930b257be401d/workflows/extraction/README.md)
