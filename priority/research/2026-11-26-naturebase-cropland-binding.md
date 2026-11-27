# Naturebase cropland agroforestry — binding inspection

26 November 2026. Technical inspection authorised by Pete. **Sample checked; scientifically accepted = false; runtime ready = false.** No analytical rules, suitability masks or four-class thresholds changed.

## Finding

The downloadable v3 package contains readable global data and positive mitigation values in Haiti. It is a **coarse, practice-related mitigation-potential comparator**, with a very restricted mapped Haitian opportunity footprint. It cannot establish the absence of agroforestry opportunity elsewhere, or supply an effect per hectare planted without further work. Keep it separate from the carbon-loss concern.

## Binding facts

| Field | Inspected result |
|---|---|
| Producer record | [Cropland-based Agroforestry, pathway 12](https://app.naturebase.org/data/nb/12); citation dated 15 April 2025, v3 |
| Working acquisition | [Download ZIP](https://naturebase-shared-docs.s3.amazonaws.com/Data-download/crp_cba_total.zip), 426,689,183 bytes; HTTP last-modified 19 November 2026. Release citation and server modification date are different identifiers. |
| Preferred cloud route | Catalogue COG URL returns HTTP 404. ZIP fallback works; no working server-side raster route verified. |
| Actual raster | `crp_cba_tco2eha.tif`, band 1; Float32; 40,076 × 14,140; EPSG:4326; 0.00898315284119522° grid, nominally 1 km. Geographic cells are not uniformly 100 ha. |
| Decode | Scale 1; offset 0; nodata −3.4028234663852886e38. Zero is a stored value, including at the offshore diagnostic point. |
| Meaning | Annual potential mitigation, tCO₂e/ha/year, from the catalogue and package documentation; raster unit tag itself is empty. |
| Pools | Aboveground biomass, belowground biomass and soil organic carbon combined. One total band; no separate pool or uncertainty raster among top-level members. |
| Time | Modelled opportunity, not an annual observed time series. Inputs include 2015 tree cover and 2019 cropland; current overlap accounting uses a 2020 cropland fraction; accounting horizon 2035. |
| Other contents | Administrative totals at levels 0–2, administrative geodatabase, README and a nested ZIP. Nested archive not used or recursively inspected. |
| Metadata defects | README gives a different raster filename and labels raster dimensions as “crs”; use inspected header. Catalogue generic `units` field says MtCO₂e/year, while raster-specific text states tCO₂e/ha/year. Do not ingest generic field blindly. |
| Licence | Catalogue displays CC BY-NC-SA 4.0; intended-use compatibility remains a deployment consideration. |

ZIP and raster SHA-256 hashes, catalogue snapshot, headers, sample observations and inspection script are preserved in [audit directory](naturebase-cropland-audit-20261126/README.md). Original global files remain in private local storage, not the repository.

## Haiti checks

| Check | Result | Interpretation |
|---|---|---|
| Native raster cell centres inside USDOS/LSIB_SIMPLE/2017 Haiti boundary | 28,815 valid; 102 positive; 28,713 zero; no nodata | Spatial coverage exists; positive modelled opportunity is sparse. Boundary and centre-inclusion choice are explicit, not an implementation-area estimate. |
| Positive range | National checked maximum 2.10919 tCO₂e/ha/year | Model output, not validation against measured sequestration. |
| Existing WorldCover 2021 stratified sample | All 1,440 points readable; 1,292 distinct native cells. Cropland stratum: 6 positive, 154 zero of 160 | Point strata are not area weighted; land-cover dates and spatial support differ. Not a national opportunity percentage or accuracy estimate. |
| Producer Haiti administrative total | 7,226.751334 tCO₂e/year; pathway footprint 9,400 ha | Producer's model scenario and coarse raster footprint, not verified feasible hectares. |
| Producer departments | Positive totals in Sud and Nord-Ouest; eight other department rows contain `NA` | Preserve `NA`; do not turn it into a measured zero. Positive department totals reconcile to national total within rounding. |
| Offshore diagnostic at −73°, 18° | Stored zero | Numeric validity cannot serve as a cropland or applicability mask. |

The 102 positive cell-centre count and producer's 9,400 ha footprint do not directly reconcile. Administrative boundaries, raster accounting and area conventions require reconciliation before reconstructing national totals. No total was derived by treating every geographic pixel as 100 ha.

## Area denominator and family use

[Accounting rules](https://naturebase-shared-docs.s3.amazonaws.com/NCS_Accounting_rules_narrative.pdf), section I(c), PDF page 6, state that cropland pathway values are multiplied by the cropland proportion within the nominal 1 km² accounting pixel. The pathway method also multiplies flux by possible additional tree-cover percentage. Thus the supplied value already contains spatial opportunity weighting; it is not a stand-alone sequestration coefficient per planted hectare. **Do not multiply it by our planted hectares or apply cropland weighting again.** Exact transfer to a RuralScan footprint remains held until the relevant fractions and denominator can be reconciled.

Producer's table formula gives 7,226.751334 / 9,400 = **0.76880 tCO₂e/ha/year over its coarse mapped pathway footprint**. Dividing by the national administrative area instead gives 0.002651. Neither is a family-specific planting rate. Producer warns that pathway footprint hectares can be overestimated, particularly for sub-kilometre practices.

Best conceptual fit remains planted silvoarable and shaded-perennial additions. Rates average relevant practices within climate zones, with broader geographic fallbacks; they do not distinguish alley cropping, coffee, cacao or shade intensity. Regeneration-based additions are only partial matches; retention of existing trees is not the same additional-carbon intervention. Boundary plantings, windbreaks and woody contour buffers remain contextual analogues with explicit linear-footprint limitations. No suitability family is activated or reclassified by this inspection.

## Disposition and next step

Resolved: acquisition via ZIP, raster identity and decode, combined pools, actual Haiti presence, administrative rows and sparse opportunity support. Still held: working hosted raster, independent applicability/fraction layers, footprint and area reconciliation, family-specific effect transfer and uncertainty. Do not treat the restrictive global opportunity extent as a local exclusion.

Subsequent inspections completed: [savanna agroforestry](2026-11-26-naturebase-savanna-binding.md), [reforestation](2026-11-26-naturebase-reforestation-binding.md) and [coastal restoration](2026-11-26-naturebase-coastal-binding.md). Their remaining scientific holds are retained in those reports. Infrastructure remains in scope under [the infrastructure workstream](../infrastructure/README.md), including Haiti national-source replacements and documented global fallback limitations.
