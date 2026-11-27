# Carbon loss: Haiti checks of the promising broader-land-use candidates

26 November 2026. Follow-up authorised by Pete. Research and binding preparation only: no scientific acceptance, runtime release, four-class cutoffs or aggregation rule introduced. The earlier forest-only proposal is superseded as a proposal for the whole carbon concern; its forest-domain data inspection remains valid. Infrastructure stays in scope through the existing [infrastructure notes](../infrastructure/README.md).

## Decision supported by these checks

Retain **OpenLandMap-soildb soil-carbon change** and **CTrees woody-biomass change** as the leading complementary candidates. Both have useful numerical coverage beyond forests in Haiti. Neither currently supports an unqualified four-class map of total ecosystem carbon loss. The unresolved issue is interpretation and change uncertainty, not basic access.

Treat these as components of the single carbon concern in the nine-variable visual method. Roots, herbaceous biomass, deep peat, deadwood and litter are not silently filled with zero. Do not sum gross forest emissions with overlapping soil/biomass stock differences.

## Coverage actually checked

Sampled 160 locations per present class in ESA WorldCover 2021, within the simplified LSIB Haiti polygon: **1,440 locations across nine classes**. The sampling grid is 100 m in UTM 18N; each carbon raster was then read at native resolution. Equal allocation supports within-class diagnostic comparisons, not national area estimates. WorldCover describes 2021 cover, not land-use history; “tree cover” is not necessarily nationally defined forest, and “grassland” does not establish grazing use. The boundary is an international fallback, not a country-endorsed pilot boundary. [WorldCover catalogue](https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v200), [boundary catalogue](https://developers.google.com/earth-engine/datasets/catalog/USDOS_LSIB_SIMPLE_2017)

| WorldCover class | Sampled points | Soil: valid both periods | CTrees: valid 2000, 2022 and 2025 |
|---|---:|---:|---:|
| Tree cover | 160 | 160 | 160 |
| Shrubland | 160 | 160 | 160 |
| Grassland | 160 | 159 | 160 |
| Cropland | 160 | 160 | 160 |
| Herbaceous wetland | 160 | 153 | 160 |
| Mangroves | 160 | 140 | 159 |
| Bare/sparse vegetation | 160 | 158 | 160 |
| Built-up | 160 | 160 | 159 |
| Permanent water | 160 | 20 | 154 |

These are finite, unmasked values, not proof that every carbon pool is represented or accurate. The water results demonstrate why provider masks alone are insufficient: resolution, shoreline/mixed-pixel and domain differences require an explicit applicability mask. They do not prove the products measure aquatic carbon. Native pixels are larger than WorldCover cells; neighbouring cover can contribute.

## OpenLandMap soil-carbon lead

Checked 0–30 cm SOC density for 2000–2005 and 2020–2022. GEE raw values require **0.1 scaling** to kg C/m³; native nodata is 32767. For this fixed depth, stock in t C/ha is density × 0.3 × 10. Do not multiply density by bulk density again. Do not label period differences annual emissions.

Retrieved producer-native **120 m mean, 16th and 84th percentile layers for both periods**, using the same grid, units and depth. At 20 deliberately spatially spread locations across tree, shrub, grass, crop, wetland and mangrove classes, every pair of period prediction intervals overlapped. These locations are a diagnostic subset, not independent field validation or a representative uncertainty sample.

For example, a cropland location has a modelled fixed-depth change of −1.5 t C/ha, while the marginal period prediction ranges are much wider. The saved corner-envelope calculation is descriptive only: subtracting marginal quantiles does not construct a calibrated confidence interval for change. Overlap does not prove no real change; cross-time error dependence is unresolved.

The paper explicitly warns about limited repeat soil observations, prediction uncertainty and difficulties validating trends. Its block periods reduce interannual noise but do not eliminate those issues. Consequently this is a useful **modelled soil-change context candidate**, with four-level scoring still pending a defensible change-uncertainty convention. [Paper, §§2.11, 4.4–4.5](https://essd.copernicus.org/articles/18/989/2026/), [producer access tutorial](https://github.com/openlandmap/soildb/blob/main/OpenLandMap_soildb_tutorial.ipynb)

## CTrees biomass lead

Checked annual 100 m AGB and uncertainty for 2000, 2022 and 2025 through community GEE; previous work also verified anonymous AWS native COG reads. Both bands use 0.1 scaling. Retain **dry biomass** units until an explicit carbon-fraction conversion is chosen. The public 100 m collection is woody AGB; numerical values in cropland/grassland do not establish coverage of crop biomass, grass roots or soil. [Producer](https://ctrees.org/data/datasets/global-aboveground-biomass), [GEE band definitions](https://gee-community-catalog.org/projects/ctrees_global/), [AWS](https://registry.opendata.aws/ctrees-agb-100m-global/)

In the tree-cover sample, median absolute 2000–2025 AGB difference was 2.6 Mg/ha, compared with median supplied stock uncertainties of 22.2 and 22.05 Mg/ha. Cropland equivalents were 1.2 versus 14.7 and 15.55 Mg/ha. These descriptive comparisons flag a problem to resolve; they are **not temporal significance tests**, since stock errors can be correlated across years. Do not assign high/medium/low solely because a nonzero difference exists.

The 2022 image enables examination of an endpoint near the soil product's final period; a single 2022 stock is still not identical temporal support to a 2020–2022 soil block. No combined physical total has been calculated.

## Roots and access

CTrees JMRV includes AGB plus BGB inferred from IPCC defaults, with annual 1 km stocks through 2025. Its producer still directs raster requests to the contact form; public jurisdiction summaries are not an inspected gridded download. It excludes soil, peat, deadwood and litter. Its forest/non-forest accounting does not establish complete non-woody root-carbon change. [JMRV methods/access](https://ctrees.org/data/datasets/global-land-carbon-stocks-emissions-removals)

Following the cited scientific lineage found a downloadable 2000–2019 live-biomass dataset accompanying Xu et al. (2021). That study works at 10 km and explicitly concerns woody vegetation, with allometrically inferred roots. This is a possible coarse comparison, not a solution to the herbaceous/root gap or evidence of access to current 1 km JMRV rasters. No file in that older package was substituted for JMRV. [Study](https://pmc.ncbi.nlm.nih.gov/articles/PMC11205271/), [author dataset](https://zenodo.org/records/4161694)

No provider message or form was submitted. Provider questions needed for the next binding decision:

- JMRV: obtain Haiti/global raster access, pool-separated AGB/BGB if available, exact units/masks, version and uncertainty definitions.
- CTrees: clarify cross-year covariance or supplied change uncertainty and validation in non-forest systems; confirm coverage of herbaceous vegetation versus woody plants within those land covers.
- OpenLandMap: establish how to quantify uncertainty of period differences, and whether paired model outputs or a recommended operational change threshold are available.

## Published classification rationale found

UNCCD's 2026 reporting manual, §1.3.6 action 5, uses **relative SOC decline >10%** as a default degradation screen. It allows statistical or relative-change approaches and calls for national verification. This supplies a published starting point for **soil-carbon degradation**, not universal biomass-loss thresholds or four severity bands. Its reporting periods also differ from OpenLandMap's blocks. [UNCCD reporting manual](https://prais4-reporting-manual.unccd.int/en/2026/SO1.html)

The 2025 advanced-unedited addendum uses “10 per cent or more” and says the starting threshold should be refined for country and dataset uncertainty. The equality convention therefore needs explicit source/version selection before implementation. No 10% rule was applied to this sample. [Addendum, printed p.83, PDF page 91](https://www.unccd.int/sites/default/files/2025-07/GPG%20Addendum_%20Advanced%20Unedited%20Version.pdf)

Do not relabel changes within 10% as proven absence of loss. Low/medium/high subdivisions above a screen would still require an explicit project rule and reference population; the cited guidance does not supply them.

## Binding status and next decision

| Component | Resolved | Remaining hold | Proposed current role |
|---|---|---|---|
| OpenLandMap SOC | GEE/native access, scaling, depth, period labels, sampled Haiti coverage, native uncertainty access | Temporal-change uncertainty; representativeness; classification | Unscored modelled soil-change context candidate |
| CTrees 100 m | GEE/AWS access, scaling, annual bands, sampled Haiti coverage | Change uncertainty; non-woody coverage; classification | Woody-carbon-change candidate |
| CTrees 1 km JMRV | Published pools and request route | Raster access and verification; non-woody root scope | Hold as live-biomass alternative |
| Total carbon concern | Complementary components identified | Pool/time alignment, aggregation and four-class rules | One concern; no new priority variables |

Infrastructure remains in scope, including national replacement needs for Haiti. No climate-hazard selection changed.

## Reproducibility

[Audit directory](carbon-loss-audit-20261126/README.md) contains compact observations, image metadata, native soil uncertainty reads, computed summaries, scripts and SHA-256 manifest. This is bounded technical inspection, not formal SRC/EV dataset intake or a production binding. Numbers above can be checked offline against the retained records. Raw per-image responses and full boundary snapshot also remain in the local research workspace.

## Related mitigation-potential comparison

The [Naturebase ↔ RuralScan crosswalk](2026-11-26-naturebase-nbs-crosswalk.md) assesses all six NbS groups and current families. It keeps practice-specific mitigation opportunity separate from carbon-loss need and identifies pathway-specific binding checks.
