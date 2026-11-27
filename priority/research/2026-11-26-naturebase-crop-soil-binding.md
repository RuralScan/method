# Cropland soil-carbon management: Haiti binding inspection

26 November 2026, America/Bogota. Research inspection; no accepted BIND, T4/T6 effect or runtime activation.

**Haiti coverage is confirmed. Retain Naturebase's combined scenario as a candidate for coarse descriptive context, but hold practice-specific benefit transfer.** It combines soil-input management, tillage change and biochar; its total is not the effect of mulching, conservation tillage, or water harvesting alone.

## Dataset and Haiti results

[Increased Soil Carbon in Croplands](https://app.naturebase.org/data/nb/14), Naturebase v2, cited release 6 June 2024. Current public ZIP was last modified 19 November 2026; that packaging date is not an observation date or evidence of a new scientific version. Current metadata and package README retain the v2 citation.

| Check | Verified result |
|---|---|
| Raster | `crp_scc_tco2eha.tif`, single combined band; EPSG:4326, Float32, 40,075 × 14,140 cells |
| Native resolution | 0.00898315284°; nominal 1 km, not a uniform 100 ha cell area |
| Units | Raster: tCO2e/ha/year; administrative totals: tCO2e/year. Generic catalogue `MtCO2e/yr` does not describe raster values. |
| Haiti native cell centres | 28,815 valid: **6,073 positive**, 22,742 zero; no negative or nodata values |
| Stratified sample | All 1,440 points readable; 1,292 distinct native pixels |
| WorldCover cropland samples | **144/160 positive**; median over all 160 points 0.3123, maximum 1.3058 tCO2e/ha/year |
| Maximum checked Haiti raster value | 1.9462 tCO2e/ha/year |
| Published national mitigation | **97,016.440991107 tCO2e/year**, combined scenario |
| Published pathway footprint | **572,200 ha**, coarse raster footprint; not verified hectares available for implementation |
| Administrative records | 1 national, 10 admin1, 42 admin2; one admin2 has `NA` mitigation and area |
| Advertised cloud raster | HTTP 404; public ZIP scientific members readable |

The missing admin2 record is **Arrondissement Saint-Louis du Nord**. Preserve `NA`; do not convert it to zero opportunity. Admin1 mitigation sums to 97,015.191677479 and valid admin2 records to 97,015.387137718 tCO2e/year, respectively about 1.25 and 1.05 below the national total. Their footprint sums are 572,100 and 572,300 ha. Retain these small discrepancies rather than silently forcing reconciliation.

Checks use `USDOS/LSIB_SIMPLE/2017`, filtered to Haiti, with native cell centres. Counts are not area estimates. Sample design is 160 points per class across nine ESA WorldCover classes, not an area-weighted country sample. Positive values also occur at non-cropland sample points; mixed kilometre-scale pixels, map dates and differing classifications prevent treating a positive pixel as evidence that every location inside it is eligible cropland. No field validation or Haiti accuracy statistic is available from this inspection.

## What the scenario contains

The producer describes three mechanisms:

| Mechanism | Published assumptions | Transfer limitation |
|---|---|---|
| Increased inputs / cover cropping | IPCC Tier 1 factors for higher residue inputs, green manures, cover crops and related input-enhancing management; this input category excludes manure | No separate mulching or cover-crop benefit supplied in the inspected scientific members |
| Reduced tillage | No-till relative to an assumed conventional-tillage baseline | Cannot assign the full gain where farmers already use reduced/no tillage; conservation tillage is not automatically equivalent to no-till |
| Biochar | Crop residues estimated from MapSPAM production; pyrolysis and mineralisation determine carbon remaining after 100 years | Residue supply, competing uses, processing and adoption are not established for Haiti; no automatic attribution to water harvesting |

For the first two mechanisms, Naturebase describes a 2018 baseline, an original 20-year transition, and extension to 2050 that reduces the annualised rate. These are **scenario accounting assumptions**, not annual observations. Biochar's 100-year persistence calculation is a different time concept. Current structured `accounting_horizon` is null, while narrative caveats mention 2035 and 2050; preserve that distinction and do not infer an arbitrary accumulation period. Source: [saved Naturebase metadata](naturebase-crop-soil-audit-20261126/catalogue_records.json), Description and Data Caveats.

The named upstream **Soils Revealed soil carbon futures** record describes 20-year SOC stock changes in Mg C/ha to 30 cm, with distinct management-only (`crop_MG`), inputs-only (`crop_I`) and combined (`crop_MGI`) scenarios. Author-deposited DataCite metadata confirms the title and v3.0 identity; [metadata snapshot](naturebase-crop-soil-audit-20261126/soils_revealed_datacite.json). Naturebase names `scenario_crop_MG_dSOC_Y20.tif`, but that one reference does not explain the full cover-crop/tillage/biochar combination. The initial direct-access attempt returned HTTP 403. The subsequent [component inspection](2026-11-26-crop-soil-components.md) acquired and checked native Haiti support for all three original scenarios; this supersedes the acquisition hold, without establishing equivalence to Naturebase processing. Do not apply a blanket unit/time conversion to the combined Naturebase layer or assume it has one uniform soil-depth interpretation including biochar.

The original ZIP inventory contains **one TIFF and three administrative CSVs**, all combined-pathway products. No separate practice raster or component CSV was found. Embedded geodatabase contents were inventoried only, not inspected; component separation is therefore unresolved beyond those scientific members.

## Appropriate use and limitations

- **Practice fit:** partial match to conservation tillage/mulching within `water_harvesting__in_situ`; no transfer of the combined total to that whole family. Terraces, bunds, Zai, micro-catchments, ponds and floodwater diversion receive no inferred benefit from this layer. No scope expansion to biochar is implied.
- **Global/national context:** retain the global product as a provisional scenario comparator. A Haiti refinement needs current cropland boundaries, actual tillage and residue-management baselines, locally appropriate interventions and better SOC evidence. No national replacement was acquired in this inspection.
- **Denominator:** current Naturebase metadata says mitigation is weighted by cropland fraction. A raster value is not automatically a per-treated-hectare rate. Do not weight by that fraction again or multiply it by an arbitrary project footprint. Published pathway hectares carry an explicit coarse-footprint overestimation warning.
- **Scientific uncertainty:** no per-pixel confidence interval or Haiti validation accompanies the inspected outputs. Baseline adoption, carbon saturation and persistence, residue availability and overlapping carbon pools need explicit treatment before investment-level estimates. SOC is not live belowground biomass; do not add overlapping soil benefits from agroforestry or another management scenario without reconciliation.
- **External caution:** Conservation International's related [insetting methods](https://www.conservation.org/projects/mapping-the-climate-potential-of-insetting) recommend geographic comparison with local refinement and explicitly flag aggregated practices. Their separate soil-carbon discount draws on US evidence; **no US-derived discount is adopted for Haiti**.
- **Classification:** mitigation potential remains separate from current carbon-loss concern. No high/medium/low/none cutoffs are introduced. Zero raster values and missing administrative records do not prove no local soil-carbon opportunity.
- **Infrastructure:** roads, power lines, buildings, schools and health facilities remain in scope under the [infrastructure record](../infrastructure/README.md). Global fallback coverage limitations and national replacement needs remain explicit; this inspection does not compute exposure or alter hazard assumptions.

Follow-up: [component separation and Haiti applicability](2026-11-26-crop-soil-components.md) identifies separate no-till, input and joint scenarios and verifies standalone biochar coverage. Soil-scenario terms and downloads were approved on 26 November 2026; native Haiti windows now verify all three scenarios and show the joint scenario exceeds the sum of individual gains by 6.08–10.65%. Sparse support and unverified local baseline conditions still hold practice-specific quantitative transfer. The initial five-part Naturebase inspection queue is now covered; unresolved component and local-data holds remain.

## Reproducibility and access

[Audit and probes](naturebase-crop-soil-audit-20261126/README.md) retain 53 Haiti administrative rows, sample values, native-grid results, original member inventory and hashes. The [public ZIP](https://naturebase-shared-docs.s3.amazonaws.com/Data-download/crp_scc_total.zip) was accessed by HTTP ranges for its five top-level CSV/TXT/TIF members. Selected-member CRCs and SHA256 were checked. Original full ZIP was not downloaded or SHA256-hashed; `crp_scc_selected.zip` is a locally assembled subset. No claim of full-archive verification or GDB inspection is made.

Naturebase catalogue reuse conditions remain CC BY-NC-SA 4.0 with linked source terms. Upstream DataCite metadata lists custom terms, not an unrestricted default licence; the follow-up verified these as CC BY 4.0 for Soils Revealed and CC0 1.0 for the separate biochar dataset. No formal SRC/EV intake, scientific acceptance, schema modification or runtime activation occurred.
