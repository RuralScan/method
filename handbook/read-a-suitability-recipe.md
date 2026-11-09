# Read a suitability recipe

A site receives **350 mm of rain per year**. Can an analyst use that number to score the site for bench terraces? To assess any proposed suitability rule, identify the family, check what the input measures, then read the evidence and the decision attached to the mapping.

## Find the family and input

| Look up | What the definition says | Why it matters |
|---|---|---|
| Practice and family | The practice is `water_harvesting_conservation`. Its `bench_terraces` subpractice belongs to `water_harvesting__terracing`, whose spatial product type is `area_suitability`. | The family defines which siting question the evidence must address. An area-suitability map, where supported, describes candidate areas for investigation. |
| Variable | `annual_precipitation` means **mean annual precipitation**, in mm/year. | A seasonal total in mm measures a different quantity. |
| Draft definition snapshot | The global binding identifies band `BIO12` of `chelsa_bioclim_v21_baseline` as the annual input. | A dataset can supply a value at the site. The rule still needs evidence for how that value affects suitability. Check the applicable geographic binding when working in another context. |

Look up the identifiers in the definition tables. A dataset binding identifies the input, while T4 holds the relationship for the practice family. [Practice](../data-model/configuration/recipes/water_harvesting_conservation/T0_nbs_registry.csv) · [Families](../data-model/configuration/FAM_family_registry.csv) · [Variables](../data-model/configuration/VONT_variable_ontology.csv) · [Bindings](../data-model/configuration/BIND_dataset_binding.csv) · [Datasets](../data-model/configuration/T1_data_registry.csv)

The reviewed terrace run records a different dataset ID, `worldclim_v2_precip`. Use the run record to identify the input associated with that decision. The catalogued CHELSA binding above illustrates how to look up a global default. Neither input supplies the missing calibration. [Terrace run record](https://github.com/CIAT/nbs_ruralscan/blob/2023cb82c94a93120600a7feb17d8cd1e12ce54f/methodology/audits/t4_water_block_20261109/terrace_rainfall_run.json)

## Read what the sources support

The reviewed T4 mapping is `water_harvesting__terracing__annual_precipitation`. Its decision considers three source profiles. **One** supports the annual terrace observation. [Compiled mapping table](https://github.com/CIAT/nbs_ruralscan/blob/2023cb82c94a93120600a7feb17d8cd1e12ce54f/schema/recipes/water_harvesting_conservation/T4_suitability_mappings.json) · [Source profiles and locators](https://github.com/CIAT/nbs_ruralscan/blob/2023cb82c94a93120600a7feb17d8cd1e12ce54f/methodology/audits/t4_water_block_20261109/terrace_rainfall.md)

| Source profile | What it contributes |
|---|---|
| WOCAT, p. 129 | Documents forward-sloping bench terraces used in places receiving 200–600 mm/year. The observed range supports a statement about where this design has been used. |
| Ronquillo watershed model | Uses mean October–April rainfall in a regional scoring model. Its classes and weight describe that model. |
| FAO contour stone lines | Describes rainfall conditions for a different water-harvesting structure. Its guidance belongs with that design. |

## Check the decision before scoring

The release records `n_sources = 1` and a **held** numerical calibration. The T4 row's relationship type is labelled `trapezoidal`. Its parameters carry the review decision, with no approved breakpoints for scoring. This example uses a fixed producer revision so it can be repeated as evidence review continues. [Release verification](https://github.com/CIAT/nbs_ruralscan/blob/ab89c9dba2223855b09b3cfb7e83a54d9ff09db4/methodology/migration/2026-11-05/m16-runtime-799-handoff.md)

Run this read-only check with Python 3 and an internet connection. It reads the published row and prints the source count, evidence identifier and calibration status.

```python
import json
from urllib.request import urlopen

url = (
    "https://raw.githubusercontent.com/CIAT/nbs_ruralscan/"
    "2023cb82c94a93120600a7feb17d8cd1e12ce54f/schema/recipes/"
    "water_harvesting_conservation/T4_suitability_mappings.json"
)
with urlopen(url, timeout=30) as response:
    rows = json.load(response)
mapping = next(row for row in rows
               if row["mapping_id"] == "water_harvesting__terracing__annual_precipitation")
calibration = mapping["relationship_params"]["reviewed_adaptation"]["numerical_calibration"]
print(mapping["n_sources"], mapping["evidence_ids"], calibration["status"])
```

Expected output is `1 ['ev_wh_precip_wocatgl13_benchterraces'] held`.

**At 350 mm/year**, the analyst can report that the site falls within a documented use range for forward-sloping benches. Leave the rainfall suitability score unassigned. Scoring this family would require a supported response to annual rainfall, calibration for the intended context and a released decision that permits its use.

## Reuse these definitions

The definition snapshot fixes the field specification, table structure, seven shared configuration tables and five practice identity tables to one Git revision. A consumer can verify each file against its SHA-256 before using it. The snapshot describes the draft definitions used in this example. Read its files at the recorded source revision. Scientific decisions, compiler settings and compiled rows carry their own revisions. [Historical definition snapshot](https://github.com/RuralScan/method/blob/aad360c25efd64d6a2754138e79ca558d2b472c7/data-model/definition-snapshot.json) · [Definition coverage at the pinned revision](https://github.com/RuralScan/method/blob/747081661229d2598e6c2439c9774bb84b389c65/data-model/baseline.md)
