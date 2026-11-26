# Production gap: published crop-yield bands for review

25 November 2026. Proposed crop component of `production_gap`; not yet approved or bound to a spatial dataset.

FAO's *The State of the World's Land and Water Resources for Food and Agriculture 2025*, Figure 19 (printed page 38; PDF page 64), reports five yield-gap bands: limited 0–20%, moderate 20–40%, significant 40–60%, severe 60–80% and very severe 80–100%. The figure compares maize, rice and wheat at country level, using 2001–2020 averages. [Official report and PDF](https://openknowledge.fao.org/bitstreams/934f7fed-ceb0-4245-adbd-04c108ba4d42/download#page=64).

Proposed four-class collapse:

| RuralScan class | Yield gap (% of attainable yield) | Published basis |
|---|---:|---|
| Very little | 0–20 | Limited |
| Low | >20–40 | Moderate |
| Medium | >40–60 | Significant |
| High | >60–100 | Severe and very severe combined |

The label changes, merging of the highest bands and upper-inclusive endpoints are RuralScan conventions. Very little does not mean zero gap. This preserves a published classification rather than inventing new split points; it does not establish universal agronomic response thresholds.

Define the relative gap as `100 × (1 − actual_yield / attainable_yield)`. FAO's Annex §1.2 (printed page 103; PDF page 129) uses adjusted attainable yield and matching fresh-matter units. Its analysis combines high-input GAEZ v5 attainable yields with FAOSTAT country yields; the report explicitly distinguishes this calculation from GAEZ's pixel-level yield-achievement product. [Annex method](https://openknowledge.fao.org/bitstreams/934f7fed-ceb0-4245-adbd-04c108ba4d42/download#page=129).

A spatial application therefore needs a separately specified crop dataset, attainable benchmark, input/management level, water regime, units and period. Country statistics cannot create within-country variation by rasterization. The [GAEZ crop-product catalogue](https://gaez.fao.org/) offers candidate yield/production-gap products; no file or field has been selected in this pass.

Keep the initial interpretation crop-specific. The published demonstration covers maize, rice and wheat; applying it to other crops or finer spatial support is an explicit transfer requiring contextual review. Livestock, pasture NPP and mixed-system production need their own appropriate metrics and classification. Do not average unrelated crops or combine yield and livestock/NPP gaps without a declared aggregation method.

Missing observations, nonpositive attainable yield and unresolved coverage remain unknown. Negative computed gaps (actual above the chosen attainable benchmark) require checking; retain the raw result and flag the mismatch rather than silently clipping it to Very little. Non-cropped land is outside the crop measure, not a 100% gap. A large gap is baseline production need, not the share an NbS can close or proof that degradation caused it.

Source verification: downloaded the official PDF from FAO, verified its title/author and PDF format, visually checked Figure 19 and read the Annex calculation. This is a classification research note, not formal source registration or an accepted data binding.

Source artefacts archived in the team-library mirror under `0_Methodology_&_Frameworks/priority_classification/production_gap_2026_11_25/classification_sources.zip`; SHA-256 `08ce920f6510be115f96a21f7da060f1e25c864e66dd72e10269bb81a864c419`. All members were read back byte-for-byte. Remote team access was not checked.

Official PDF SHA-256: `70c077173fcbb84ee4e7fee6d143c98dccb009c2d39d4ccddae062fed2a6b73e`. The publisher landing page supplied an EPUB in its PDF metadata slot; the separate PDF asset was identified and verified. Figure/page locators above refer only to the actual PDF.
