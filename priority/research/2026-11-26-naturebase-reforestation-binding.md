# Naturebase reforestation — binding inspection

26 November 2026. Technical inspection authorised by Pete. **Sample checked; scientifically accepted = false; runtime ready = false.** No classification thresholds, suitability rules or binding registry rows changed.

## Finding

Haiti has readable, spatially differentiated reforestation mitigation potential in this release: **9,869 positive native cells** within the checked country boundary. Producer's national table reports **3,827,519.92959 tCO₂e/year**, with positive results in all 10 departments and all 42 level-2 units. Retain as a **coarse natural-regrowth mitigation comparator**. These are model outputs under the producer's assumptions, not validated feasible project benefits or observed carbon loss.

## Binding facts

| Field | Verified result |
|---|---|
| Producer record | [Naturebase Reforestation, pathway 4](https://app.naturebase.org/data/nb/4), citing Fesenmyer et al. (2025), published 11 June 2025 |
| Acquired package | [for_ref_total.zip](https://naturebase-shared-docs.s3.amazonaws.com/Data-download/for_ref_total.zip), 255,776,699 bytes; server last-modified 19 November 2026; full archive CRC passed. Package has no explicit numbered Naturebase release identifier; pin bytes and retrieval date |
| Cloud route | Catalogue COG URL returns HTTP 404. Three author-code GEE asset references were also unavailable to the current account; this does not establish that assets are absent for every user |
| Actual raster | `for_ref_tco2eha.tif`, band 1, Float32, EPSG:4326; 40,076 × 19,329; 0.00898315284119522° cells, nominally 1 km |
| Decode and units | Scale 1, offset 0, nodata −3.4028234663852886e38; stored zero also occurs offshore. Raster unit tag absent; producer raster-specific documentation states tCO₂e/ha/year. Generic catalogue MtCO₂e/year field is not the raster unit |
| Time | Reforestation extent based on 2019–2020 land cover; natural-regrowth rates averaged over first 30 years; background forest loss/gain from 2000–2020; catalogue accounting horizon 2035. These describe different aspects of the model, not an annual monitoring series |
| Pools | Aboveground biomass and belowground biomass supported by documented calculation. Catalogue pool list also includes soil organic carbon, but package methods and archived calculation do not substantiate an SOC term. **SOC contribution unverified; do not count or label it as confirmed** |
| Components | One total mitigation raster, administrative CSVs and administrative geodatabase. No separate pool, uncertainty, eligibility-fraction, albedo or additionality rasters in this package |
| Header defects | README names `for_ref_total.tif` and includes `WHA83` in CRS text; actual member and EPSG:4326 header govern decoding |

ZIP SHA-256: `3d997a2a226f8496c97ed0f4e58e0dc1ffe2c49a02a3307b50f850f170d820cc`.
Raster SHA-256: `018ec40482df3e2f081651d93b8c330d88807f0bce827bc9f11a75a92a7b028c`.

## Haiti coverage and reconciliation

| Check | Result | Interpretation |
|---|---|---|
| Cell centres inside USDOS/LSIB_SIMPLE/2017 Haiti | 28,815 valid; 9,869 positive; 18,946 zero; no nodata or negative values | Country is covered; positive coarse cells are not wholly eligible implementation area |
| Checked maximum | 15.81143 tCO₂e/ha/year | Weighted model output, not measured site-level sequestration |
| WorldCover 2021 diagnostics | 1,440 readable points, 1,292 distinct Naturebase cells | Stratified samples, not area-weighted national estimates or accuracy measurements |
| Positive samples, each stratum n=160 | Trees 85; shrubs 2; grassland 50; cropland 8; built-up 10; bare ground 14; water 6; herbaceous wetland 25; mangrove 8 | Coarse pixels mix land covers and source dates/definitions differ. This does not establish eligibility at those fine-scale locations |
| National producer total | 3,827,519.92959 tCO₂e/year; pathway footprint 933,600 ha | Producer warns footprint hectares can overestimate implementation extent |
| Sum of 10 department rows | 3,828,438.12865481 tCO₂e/year; 933,800 ha | Exceeds national total by 918.19906481 tCO₂e/year and 200 ha |
| Sum of 42 level-2 rows | 3,834,314.75888955 tCO₂e/year; 934,700 ha | Exceeds national total by 6,794.82929955 tCO₂e/year and 1,100 ha |

Administrative totals **do not exactly reconcile**. Preserve native levels and discrepancy; do not sum subunits and label the result the published national total. Boundary/rasterisation and area accounting must be checked before replacing any totals. All three levels contain positive values with no `NA` for Haiti. The inspection window fully contains the supplied boundary; mask uses cell centres, not all-touched inclusion.

## Meaning for RuralScan

The package models recovery of forest on currently non-forest land that can naturally support forest, subject to existing-forest, urban, water, permanent bare/ice, cropland, wetland/peat, albedo and fire-related constraints. Those producer choices are context, not newly adopted RuralScan T4 rules. Positive coarse cells do not override our fine-scale exclusions; zeros do not establish absence of locally feasible restoration.

Best family match is passive natural regeneration, with a conditional analogue for assisted regeneration. It does not isolate the extra effect of assistance. Planting is included in the pathway concept, but the carbon model uses natural-regrowth rates, not plantation- or planting-specific performance. Existing-forest enrichment and protection remain different interventions; naturally open ecosystems must not become planting opportunities simply because a coarse pixel is positive.

The [published Methods](https://www.nature.com/articles/s41467-025-59799-8), “Overlays and additional scenarios” (PDF page 10), use AGB+BGB regrowth rates, albedo and eligible area; additionality is reduced where broad-scale forest gains exceed losses. Archived `Summarize scenarios.js` uses `GROA_agb_bgb_offset` and multiplies it by eligible fraction and pixel area (lines 37–43 and 161–163). Neither establishes a soil-carbon contribution. The pool-list discrepancy remains a producer clarification item; no message sent.

**Denominator:** the final surface already combines eligible reforestation fraction, biomass sequestration, albedo and additionality. Current Naturebase [accounting rules](https://naturebase-shared-docs.s3.amazonaws.com/NCS_Accounting_rules_narrative.pdf), section I(c), additionally describe non-cropland proportional weighting. It is not a carbon coefficient per planted hectare. Do not apply these fractions twice or multiply this weighted value directly by RuralScan planted hectares. The national table ratio, 3,827,519.92959 / 933,600 = **4.09974 tCO₂e/ha/year**, describes its coarse pathway footprint, not an intervention-specific local rate. Geographic pixels are not uniformly 100 ha. No 30-year project total is inferred from the annual value.

## Upstream data and remaining holds

The [author archive](https://doi.org/10.6084/m9.figshare.27335799), inspected version 3, provides `constrained_reforestation.tif` (eligible proportion), `constrained_reforestation_ha.tif`, pixel area, forest potential and scenario maps. These offer a concrete route to denominator reconciliation. Metadata, README and relevant code were inspected; those upstream global rasters were not downloaded or assumed identical to the later Naturebase package. The archive specifies CC BY 4.0, distinct from the Naturebase catalogue conditions recorded in the preceding crosswalk; preserve source-specific licensing.

Resolved: package acquisition/integrity, native raster decoding, Haiti positive coverage, actual administrative outputs and documented biomass basis. Still held: SOC metadata conflict, family-specific benefit transfer, fractions and administrative reconciliation, uncertainty, local eligibility and equivalent hosted delivery. Keep as inspected descriptive comparator, not accepted runtime binding or carbon-loss classifier.

Subsequent [coastal restoration inspection](2026-11-26-naturebase-coastal-binding.md) is complete; separate mangrove quantitative use remains held. **Infrastructure stays active:** [Haiti national-data needs and current fallbacks](../infrastructure/README.md) cover roads, schools, health facilities, power lines and buildings. No infrastructure exposure or protection benefit was computed in this carbon inspection.

[Audit files](naturebase-reforestation-audit-20261126/README.md) preserve hashes, catalogue records, samples, table rows and reproducible inspection code.
