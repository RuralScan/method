# Water stress: approved four-class interpretation

25 November 2026. Four-class interpretation approved by Pete in this chat. This concerns baseline water stress, not the overall Aqueduct risk composite or drought frequency.

Approval: “ok approved, capture those four water stress classes and the rationale, then proceed to the next variable”. This follows the displayed crosswalk and its special arid/low-use treatment. Approval covers the class interpretation; runtime release remains separate.

Measure: water demand relative to available renewable water supply. Use the existing inspected Aqueduct 4.0 annual binding, retaining `bws_raw`, `bws_cat` and `bws_label`. The annual statistic is demand-weighted across monthly stress values. The baseline targets 2019 using smoothed historical inputs; it is not a live annual time series. Basin support is retained.

The [WRI technical note, page 11, Baseline water stress](https://files.wri.org/d8/s3fs-public/2023-08/aqueduct-40-technical-note.pdf#page=11) supplies five bands: low (<10%), low-medium (10–20%), medium-high (20–40%), high (40–80%), and extremely high (>80%). It traces the thresholds to Aqueduct 2.1. Approved RuralScan crosswalk:

| WRI published category | `bws_cat` | RuralScan display class |
|---|---:|---|
| Low (<10%) | 0 | Very little |
| Low-medium (10–20%) | 1 | Low |
| Medium-high (20–40%) | 2 | Medium |
| High (40–80%) | 3 | High |
| Extremely high (>80%) | 4 | High |
| Arid and low water use | -1 | High, retaining the arid/low-use flag |

Rationale: keep the published category boundaries, combine the two highest ordinary bands, and use the requested four-label display. Renaming WRI's low class to Very little is a RuralScan interpretation, not WRI terminology or a claim of no scarcity. Retain the original category and label alongside the simplified class. This avoids manufacturing a none category from zero demand.

Map the supplied categories rather than recomputing their membership from rounded raw ratios. The printed ranges do not settle every equality; the published category remains authoritative for exact-boundary observations. This is a categorical crosswalk, not a silent change to the method's upper-inclusive numeric threshold convention. The `categories` row in [rules.csv](../classifications/rules.csv) now captures the mapping; the review preview checks raw data and category together, retaining scarcity flags. Numeric threshold rows remain unchanged. No runtime interface is activated.

The [WRI FAQ, Water Risk Interpretation](https://github.com/wri/Aqueduct40/blob/master/data_FAQ.md#water-risk-interpretation) advises prioritising arid/low-use areas alongside high and extremely high stress. Thus arid/low-use does not become Very little merely because demand is low. The [same FAQ, Water Stress](https://github.com/wri/Aqueduct40/blob/master/data_FAQ.md#water-stress) distinguishes raw `9999` (physical scarcity) from `-9999` (missing). After the existing binding's missing/validity checks, physical scarcity maps to High with its flag retained; missing or invalid records remain unknown. Ordinary valid ratios above 1 are retained, not clipped. Conflicting raw/category states require checking rather than silently assigning Very little.

Source and binding provenance already exist in the pinned WRI technical-note packet and `aqueduct_production_semantics`/`aqueduct_live` observations referenced by [binding candidates](../bindings/README.md). The [official Earth Engine catalogue](https://developers.google.com/earth-engine/datasets/catalog/WRI_Aqueduct_Water_Risk_V4_baseline_annual) identifies the asset `WRI/Aqueduct_Water_Risk/V4/baseline_annual` and its three relevant fields. No new source registration or live acquisition is claimed here.

T5 now links to this contextual rule set. The immutable historical `aqueduct_bws-0.1.0.json` remains preserved. The chat approval is recorded here and in the CSV rationale; no protected runtime-release receipt is asserted. No seasonal-fit analysis is required to review the classes. Next proposal: [chronic food insecurity](2026-11-25-food-insecurity-classes.md).

Pinned WRI FAQ snapshot retained in the team-library mirror under `0_Methodology_&_Frameworks/priority_classification/water_stress_2026_11_25/reviewed_web_sources.zip`; archive SHA-256 `71792ac6b7ca96691a2b17e5419ad7ef3c6a9224f22a242b1489aa2b04d52f4f`. The member was read back and verified byte-for-byte. Remote team access was not checked.
