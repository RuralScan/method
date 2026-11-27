# Naturebase coastal restoration — mangrove/Haiti inspection

26 November 2026. Technical inspection authorised by Pete. **Sample checked; scientifically accepted = false; runtime ready = false.** No classification rules or accepted bindings changed.

## Finding

The release contains positive coastal-restoration mitigation values for Haiti, but **does not separate mangrove and tidal-marsh contributions**. Keep it as combined coastal context; do not assign its entire benefit to `mangrove_restoration__tidal_coastal` or also count it under wetland management.

The CSVs omit pathway hectares. An embedded geodatabase contains a `wet_cwr_ha` field, but its Haiti value exceeds the country's area and cannot serve as an implementation denominator. A separate mangrove-only source provides a promising area estimate, not a means of splitting this combined carbon total.

## Binding and component checks

| Field | Verified result |
|---|---|
| Producer | [Naturebase Coastal Wetland Restoration](https://app.naturebase.org/data/nb/16), v3, citation dated 15 April 2025 |
| Acquired package | [wet_cwr_total.zip](https://naturebase-shared-docs.s3.amazonaws.com/Data-download/wet_cwr_total.zip), 173,730,863 bytes; server last-modified 19 November 2026; full archive CRC passed |
| Raster | `wet_cwr_tco2eha.tif`, one Float32 band; EPSG:4326; 40,078 × 20,041; 0.00898315284119522° grid, nominally 1 km |
| Decode | Scale 1; offset 0; nodata −3.4028234663852886e38. Stored zero is distinct from nodata. Unit tag absent; producer raster-specific text states tCO₂e/ha/year |
| Components | One combined raster and combined administrative totals only. Embedded geodatabase schemas contain no separate mangrove/tidal-marsh fields. Public `Data-download/wet_` listing has five combined wetland-pathway archives, no separate component package under that prefix |
| Pools | Mangrove method explicitly includes AGB, BGB and SOC sequestration plus avoided further soil emissions. Tidal-marsh method includes soil sequestration and avoided soil emissions. No separate pool or avoided-emission/removal bands |
| Time | Mangrove opportunity based on losses during 1996–2020, with loss-driver exclusions from 2000–2016; annualised/modelled potential with accounting horizon 2035. Not an observed carbon-loss series |
| Cloud route | Catalogue COG URL returns HTTP 404; ZIP fallback works |
| Metadata defects | README raster filename differs from actual member and contains `WHA83` in CRS text. Catalogue generic units are MtCO₂e/year; raster-specific units govern. Pool list omits BGB although mangrove calculation includes it |

ZIP SHA-256: `8890b37377f819963f041b6aae1707cfe0a003a6f8c0a38a29d8635b8b2ebb3c`.
Raster SHA-256: `d614568e6421092cbb22ee39d896f82fe9fff8cd7cc353604d7d34a7956bbc28`.

## Haiti results

| Check | Result | Interpretation |
|---|---|---|
| Haiti native cell centres | 28,815 valid; 516 positive; 28,299 zero; no nodata or negative values | Positive coarse cells, not hectares of restoration |
| Boundary sensitivity | Including every pixel touched by the country polygon gives 642 positive cells | Coastal results depend on shoreline/boundary and inclusion convention. Neither count establishes a precise restoration footprint |
| Checked maximum | 31.41945 tCO₂e/ha/year | Combined weighted potential, not a mangrove planting coefficient |
| Existing stratified sample | All 1,440 points readable, occupying 1,292 native cells; 146/160 WorldCover mangrove points positive | Current mangrove points are not a validation sample of historical lost/restorable mangroves. Coarse cells can mix intact and lost habitat |
| Producer national total | 40,383.25028 tCO₂e/year | Mangrove plus tidal marsh; split unavailable |
| Departments | Eight positive, two zero; sum 40,383.2502709 tCO₂e/year | Reconciles to national total within 0.00001 tCO₂e/year rounding |
| Level-2 units | 26 positive, 16 zero; sum 40,383.25028174 tCO₂e/year | Also reconciles within rounding |
| CSV area fields | Administrative hectares only; no `wet_cwr_ha` | Cannot apply generic producer pathway-density formula using these CSVs |
| Embedded geodatabase | Haiti `wet_cwr_ha = 15,563,700`; mitigation 40,383.250278 | Area field exceeds published Haiti administrative area of 2,726,111 ha. Definition/unit or calculation requires clarification; **do not use or silently rescale** |

The all-touched test is a sensitivity check using the same USDOS/LSIB_SIMPLE/2017 Haiti polygon; it does not add an offshore jurisdiction or validate tidal habitat boundaries. Point samples are stratified diagnostics, not area-weighted estimates. Subnational CSVs also contain a trailing unnamed blank column; preserve raw provenance and discard only an explicitly identified empty column if a future adapter is built.

## Separate mangrove source actually checked

Acquired the small `Data Exports.zip` from [Worthington et al.'s mangrove restoration dataset](https://zenodo.org/records/11283186), record published in 2024, CC BY 4.0. Its `Country_Statistics.csv`, Haiti row, gives **8.42084982897028 km² (842.08498 ha)** of potentially restorable mangrove area: historical gross loss minus erosion and urban conversion. This is a modelled biophysical opportunity, not verified feasible hectares. Archive description still refers to the associated paper as in review; this inspection does not establish a later publication status.

The archive also provides unit-level restoration/area tables and a separately downloadable spatial typology, linked by unit ID. Its carbon exports describe secured/restored stocks over **40 years**, with AGB and SOC outputs. They are not interchangeable with Naturebase's annual combined coastal product; do not divide the Naturebase total by 842 ha or subtract these stock values to infer the tidal-marsh component. Spatial typology and large scripts archive were not acquired in this check. National row, source hashes and README interpretation are preserved in the audit.

## Conditions for use

- **Mangrove scope:** current 2020 extent is excluded from the lost-area opportunity. Pre-1996 losses and losses attributed to erosion/settlement are excluded. Thus this is not a comprehensive map of locally restorable mangroves, and restoration of degraded but still mapped stands may be missed.
- **Additionality and rates:** producer uses geographically uniform sequestration rates and soil-emission assumptions and does not deduct background mangrove recovery. Keep avoided future emissions separate conceptually from new sequestration; the combined band cannot quantify each separately.
- **Tidal-marsh scope:** opportunity is modelled relative to existing extent; producer acknowledges missing exclusions for permanent settlement and sea-level-rise vulnerability. The cited Buelow study concerns [mangroves and seagrass](https://research.aber.ac.uk/en/publications/ambitious-global-targets-for-mangrove-and-seagrass-recovery/); transfer supporting the stated tidal-marsh percentage remains unverified. No tidal-marsh cutoff or extent assumption is adopted here.
- **Area accounting:** producer applies non-cropland fractional weighting under its [accounting rules](https://naturebase-shared-docs.s3.amazonaws.com/NCS_Accounting_rules_narrative.pdf), section I(c), PDF page 6. Do not apply weighting again or multiply the resulting coarse-cell value directly by locally planted hectares. Missing/unusable pathway denominator is a separate hold.
- **No synthetic split:** masking this combined raster with current mangrove extent would neither remove all tidal-marsh contributions nor recover historical mangrove losses. Obtain the component rasters and their eligible fractions, or construct and verify a separate mangrove-specific source binding.
- **Framework scope:** no seagrass product is present in this package. Existing coastal wetland family holds remain unchanged. Carbon benefit does not quantify flood protection, storm attenuation, infrastructure damage avoided or site hydrological feasibility.

## Disposition and next step

Resolved: ZIP acquisition/integrity, native decoding, positive Haiti coverage, administrative reconciliation, combined component structure, documented mangrove roots/SOC, and a separate mangrove-only national-area lead. Still held: mangrove/tidal split, unusable geodatabase area field, local restoration geometry, uncertainty, annual-versus-stock comparability and working cloud raster.

Keep combined coastal output as descriptive context only. Mangrove-specific quantitative use requires component data or a separately verified mangrove source. The subsequent [peat restoration/management inspection](2026-11-26-naturebase-peat-bindings.md) is complete; Haiti drainage and eligible-area evidence remain unresolved. The mangrove-specific source remains a concrete follow-up rather than a claimed completed binding.

**Infrastructure remains active:** [national-data needs and provisional Haiti fallbacks](../infrastructure/README.md) retain roads, schools, health facilities, power lines and buildings. This inspection changes neither their selected sources nor their exposure-only scoping role.

[Audit](naturebase-coastal-audit-20261126/README.md) contains raw observations, inspected schemas, Haiti rows, provenance and the reusable raster probe.
