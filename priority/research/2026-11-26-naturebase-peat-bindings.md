# Naturebase peat restoration and management: Haiti binding inspection

Inspection: 26 November 2026, America/Bogota. Research candidates only; no accepted BIND, T4/T6 rule or runtime activation.

**Decision: retain the conceptual matches, but hold quantitative Haiti use for both pathways.** Naturebase rasters contain zero throughout the checked Haiti footprint and their administrative tables contain `NA`. However, PEATMAP polygons and the newer Global Peatland Map both indicate peat in Haiti. Neither the Naturebase zeros nor the masked drainage input establishes absence of peat, degradation or restoration opportunity.

## Pathway meaning and family fit

| Candidate | What it estimates | RuralScan fit | Material restrictions |
|---|---|---|---|
| [Peatland Restoration, v3](https://app.naturebase.org/data/nb/17), `wet_per` | Annual avoided greenhouse-gas emissions from rewetting degraded peat, with cropland proportion excluded; includes an avoided-fire calculation | `wetland_management__peatland`; `restoration_rewetting` only where peat substrate and action are established | Not a general freshwater/mineral-wetland or floodplain-restoration model. The 50% emissions-reduction assumption is a producer scenario, not a Haiti-calibrated effect or our classification rule. |
| [Improved Peatland Management, v3](https://app.naturebase.org/data/nb/30), `wet_ipm` | Agricultural partial rewetting: a **10 cm increase in annual water-table level**, with cropland fraction weighting | Agricultural peat management within `wetland_management__peatland` | Not a target water-table depth of 10 cm, full restoration, or a dedicated paludiculture model. Production preservation is an assumed scenario objective, not verified Haiti performance. |

Both methods intersect FAO's 2018 drained organic-soil estimate with Xu/PEATMAP peat extent. Listed regional peat replacements do not include Haiti. The 2020 cropland agreement map separates agricultural management from non-cropland restoration. Do not sum both full benefits on the same hectare or apply the cropland fraction twice. Source methods and caveats are retained in [catalogue records](naturebase-peat-audit-20261126/catalogue_records.json).

Restoration's fire term uses average burned extent from 2013–2022, taking precedence over drainage emissions where they overlap. The drainage check below does not independently reproduce or validate that fire branch. Management caveats exclude pasture and burned area, although its methods discuss grassland emission factors; clarify that scope inconsistency before transferring coefficients.

These are annual mitigation scenarios with a stated 2035 accounting horizon, not observations of current carbon loss or carbon stocks. Raster documentation specifies **tCO2e/ha/year**; the generic catalogue's aggregate unit must not replace this. Methods include CO2, CH4 and N2O. Catalogue carbon-pool labels do not establish independently downloadable aboveground or belowground biomass outputs. Peat soil carbon must not be relabelled as root biomass.

## Verified Haiti coverage

| Check | Peatland Restoration | Improved Peatland Management |
|---|---:|---:|
| Native cells with centres inside Haiti boundary | 28,815 | 28,815 |
| Valid stored zeros | 28,815 | 28,815 |
| Positive / negative / nodata cells | 0 / 0 / 0 | 0 / 0 / 0 |
| Stratified sample points with zero value | 1,440 / 1,440 | 1,440 / 1,440 |
| National / admin1 / admin2 records | 1 / 10 / 42 | 1 / 10 / 42 |
| Mitigation and pathway-area fields in every Haiti record | `NA` | `NA` |
| Advertised hosted raster | HTTP 404 | No `cog_url` supplied |
| Public ZIP scientific members | Readable | Readable |

The sample uses 160 points in each of nine ESA WorldCover classes, representing 1,292 distinct native raster pixels. The exhaustive country check uses `USDOS/LSIB_SIMPLE/2017`, `country_na=Haiti`, with a cell-centre convention. Counts depend on that boundary; they are not hectares. Positive controls outside Haiti confirm both rasters contain positive values elsewhere, rather than being entirely empty files.

Both TIFFs are one-band Float32 in EPSG:4326, 40,076 × 14,140 cells, approximately 0.00898315° pixels (nominal 1 km), scale 1, offset 0, nodata approximately −3.4028235e38. Stored zero is distinct from nodata. File headers govern CRS and geometry where README wording is inconsistent. Inspection details and sample coordinates are in the [audit](naturebase-peat-audit-20261126/README.md).

## Underlying peat and drainage checks

| Source and actual check | Haiti result | Interpretation |
|---|---|---|
| [PEATMAP North America](https://archive.researchdata.leeds.ac.uk/251/), original vector ZIP; Haiti boundary transformed to source ESRI:54034 | **171 polygons** in `Other_North_American_Peatlands.shp` intersect Haiti with positive area; 258 bounding-box candidates screened | The peat-extent source itself maps peat in Haiti. Polygon counts are not sites, hectares, drainage observations or eligible restoration area. |
| [FAO Drained Organic Soils Area](https://developers.google.com/earth-engine/datasets/catalog/FAO_GHG_1_DROSA_A), exact GEE image `FAO/GHG/1/DROSA_A/DROSA_A_2018` | **0 unmasked cells** in either cropland or grassland band; 33,487 native grid centres inside boundary | No valid Haiti observations in this input. Returned sums of zero must not be interpreted as measured zero drained hectares. It models agricultural organic soils using histosols and land-cover proxies, not a comprehensive drainage inventory. |
| [Global Peatland Map 2.0](https://greifswaldmoor.de/global-peatland-database-en.html), community GEE asset `projects/sat-io/open-datasets/GLOBAL-PEATLAND-DATABASE` | **266 unmasked cells, all class 1 (peat dominated)**; 23,056 masked cells on the checked native grid | Supports coarse peat-presence context. This single-band extent asset does not supply drainage condition, restoration need or intervention eligibility. Do not reclassify masked background as verified absence. |

PEATMAP combines source inventories of different dates and quality; the publication year is not a uniform observation epoch. Global Peatland Map 2.0 was updated for the 2022 UNEP assessment and uses an inclusive organic-soil definition. Its downloadable raster is nominally 1 km; the community-hosted version was updated in July 2024. These dates do not constitute annual monitoring. Neither product validates Haiti peat depth or local water-table condition. See the [primary map description](https://greifswaldmoor.de/global-peatland-database-en.html) and [community asset documentation](https://gee-community-catalog.org/projects/peatland/).

**Inference:** the absence of valid FAO drainage cells is consistent with the empty agricultural-drainage support behind Naturebase's Haiti result. It is not proof of the precise producer mask/fill operation, nor a complete diagnosis of the restoration fire calculation. No local peat/drainage dataset has been acquired or validated in this inspection.

## Binding decision and follow-up

- **Global default candidates:** retain both Naturebase pathways as practice-specific mitigation comparators, subject to footprint/denominator and scenario validation. Do not substitute them for the carbon-loss concern variable.
- **Haiti:** hold quantitative mitigation and eligible-area use. Coarse peat-presence context is defensible if labelled as mapped indication; **do not assign `none/very little`** from these outputs. This inspection proposes that treatment, without activating a new binding.
- **National/local replacement needed:** peat or organic-soil extent and depth, drainage/ditch and water-table condition, current land use, degradation/fire history and hydrological restoration feasibility. Use national or locally validated evidence where available; a more detailed extent map alone cannot resolve drainage status.
- **Pools and overlap:** keep soil emissions, non-CO2 gases and vegetation biomass explicit. Do not add peat-management benefits to restoration on the same footprint, or duplicate peatland/coastal family attribution.
- **Licensing:** Naturebase catalogue uses CC BY-NC-SA 4.0; PEATMAP repository lists CC BY 4.0; the community GPD entry lists non-commercial share-alike terms. Retain source-specific conditions and verify intended reuse before distribution or runtime promotion. Access does not imply unrestricted use.
- **Infrastructure remains in scope:** roads, power lines, buildings, schools and health facilities continue under the [infrastructure record](../infrastructure/README.md), with global fallback coverage limitations and preference for national replacements. This carbon inspection adds no infrastructure exposure calculation or new hazard assumptions.

Subsequent inspection completed: [Increased Soil Carbon in Croplands](2026-11-26-naturebase-crop-soil-binding.md), restricted to matching soil-management subpractices such as conservation tillage/mulching. Do not transfer its bundled scenario to the whole water-harvesting group. Mangrove component separation and Haiti peat/drainage validation remain explicit follow-ups.

## Acquisition and reproducibility

Public scientific members were acquired from [restoration ZIP](https://naturebase-shared-docs.s3.amazonaws.com/Data-download/wet_per_total.zip) and [management ZIP](https://naturebase-shared-docs.s3.amazonaws.com/Data-download/wet_ipm_total.zip) using HTTP ranges. Only top-level CSV/TXT/TIF members were extracted and CRC-checked; **the original whole ZIPs were not downloaded or SHA256-hashed**, and embedded geodatabases were not inspected. Hashes named `*_selected.zip` describe locally assembled subsets. Original HTTP headers, archive inventory and each acquired member's SHA256 are retained separately.

Original PEATMAP North America ZIP was acquired in full and hashed. The [compact audit](naturebase-peat-audit-20261126/README.md) retains probes, provenance, selected-member hashes, Haiti administrative records, native-grid checks and sample values; global binaries remain in the private working cache. No source/evidence-register promotion, accepted schema change or class threshold is implied.
