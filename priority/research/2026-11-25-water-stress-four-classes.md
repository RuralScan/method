# Water stress: four-class mapping for review

25 November 2026. Next classification proposal after soil erosion; not yet approved. This concerns baseline water stress, not the overall Aqueduct risk composite or drought frequency.

Measure: water demand relative to available renewable water supply. Use the existing inspected Aqueduct 4.0 annual binding, retaining `bws_raw`, `bws_cat` and `bws_label`. The annual statistic is demand-weighted across monthly stress values. The baseline targets 2019 using smoothed historical inputs; it is not a live annual time series. Basin support is retained.

The [WRI technical note, page 11, Baseline water stress](https://files.wri.org/d8/s3fs-public/2023-08/aqueduct-40-technical-note.pdf#page=11) supplies five bands: low (<10%), low-medium (10–20%), medium-high (20–40%), high (40–80%), and extremely high (>80%). It traces the thresholds to Aqueduct 2.1. Proposed RuralScan crosswalk:

| WRI published category | `bws_cat` | RuralScan display class |
|---|---:|---|
| Low (<10%) | 0 | Very little |
| Low-medium (10–20%) | 1 | Low |
| Medium-high (20–40%) | 2 | Medium |
| High (40–80%) | 3 | High |
| Extremely high (>80%) | 4 | High |
| Arid and low water use | -1 | High, retaining the arid/low-use flag |

Rationale: keep the published category boundaries, combine the two highest ordinary bands, and use the requested four-label display. Renaming WRI's low class to Very little is a RuralScan interpretation, not WRI terminology or a claim of no scarcity. Retain the original category and label alongside the simplified class. This avoids manufacturing a none category from zero demand.

Map the supplied categories rather than recomputing their membership from rounded raw ratios. The printed ranges do not settle every equality; the published category remains authoritative for exact-boundary observations. This is a categorical crosswalk, not a silent change to the method's upper-inclusive numeric threshold convention. No numeric `rules.csv` row or new categorical runtime interface is activated in this draft.

The [WRI FAQ, Water Risk Interpretation](https://github.com/wri/Aqueduct40/blob/master/data_FAQ.md#water-risk-interpretation) advises prioritising arid/low-use areas alongside high and extremely high stress. Thus arid/low-use does not become Very little merely because demand is low. The [same FAQ, Water Stress](https://github.com/wri/Aqueduct40/blob/master/data_FAQ.md#water-stress) distinguishes raw `9999` (physical scarcity) from `-9999` (missing). After the existing binding's missing/validity checks, physical scarcity maps to High with its flag retained; missing or invalid records remain unknown. Ordinary valid ratios above 1 are retained, not clipped. Conflicting raw/category states require checking rather than silently assigning Very little.

Source and binding provenance already exist in the pinned WRI technical-note packet and `aqueduct_production_semantics`/`aqueduct_live` observations referenced by [binding candidates](../bindings/README.md). The [official Earth Engine catalogue](https://developers.google.com/earth-engine/datasets/catalog/WRI_Aqueduct_Water_Risk_V4_baseline_annual) identifies the asset `WRI/Aqueduct_Water_Risk/V4/baseline_annual` and its three relevant fields. No new source registration or live acquisition is claimed here.

This advances the earlier held mapping into a concrete proposal without rewriting the immutable historical `aqueduct_bws-0.1.0.json` or treating this draft as user approval. No seasonal-fit analysis is required to review the classes.
