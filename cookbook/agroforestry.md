# Agroforestry

[Choose another practice](README.md)

Start with how trees become established. A planted system, regrowth from existing rootstock, a field boundary and a shade crop each need different site information.

## Choose a family

| Family | What determines the choice? | Registered variants | Intended spatial product |
|---|---|---|---|
| Homegardens | Check household access to water and proximity to settlements at the local site. | Multistrata homegardens | Qualitative guidance |
| Linear plantings and boundaries | Locate the field boundary, prevailing wind or contour line that sets the planting position. | Windbreaks & shelterbelts, Contour & vegetative buffers | Applicability zone |
| Regeneration on farmland | Look for remnant trees, rootstock or seed supply that can support regrowth. | Farmer-managed natural regeneration (FMNR), Parkland tree retention, Assisted natural regeneration on farmland | Area suitability |
| Shaded perennial crops | Locate the host crop and consider the conditions under which shade would help it. | Shaded perennial-crop system | Area suitability |
| Trees planted on cropland | Check whether planting can fit cultivable land and field operations. | Alley cropping, Tree intercropping, Planted boundary / live fence on cropland | Area suitability |
| Trees with livestock | Check the grazing system and forage conditions alongside tree establishment. | Planted silvopasture, Agrosilvopasture | Area suitability |
| Cross-family context | Read shared observations here. Choose a specific intervention family when defining a map. | Cross-cutting envelope (family-agnostic) | Qualitative guidance |

[Practice definition (T0)](https://github.com/RuralScan/method/blob/92f86f035792cacb066eecdc12f439a87ef6d0c0/data-model/configuration/recipes/agroforestry/T0_nbs_registry.csv) · [Variant definitions and grouping rationale (FAM)](https://github.com/RuralScan/method/blob/92f86f035792cacb066eecdc12f439a87ef6d0c0/data-model/configuration/FAM_family_registry.csv)

## Interpret the spatial output

- **Applicability zone.** A zone in which to inspect individual locations. Field layouts and structure footprints need local delineation.
- **Area suitability.** A potential area surface at a resolution supported by the inputs.
- **Qualitative guidance.** A qualitative assessment or contextual evidence. No pixel-area footprint is assigned.

For shaded perennial crops, check where the host crop is grown. For regeneration, check local evidence of viable woody regrowth. Record tenure, finance and access separately when assessing implementation.

## Inspect compiled evidence

Each count is an analytical row in the pinned candidate. The family named on the row determines where it is counted. Rows with no family ID appear once under **Practice-wide**, including rows limited to a particular geography or farming system.

| Scope | T3 hazard responses | T4 suitability mappings | T6 scorecard effects | T6E economic profiles |
|---|---:|---:|---:|---:|
| Homegardens | 0 | 0 | 0 | 0 |
| Linear plantings and boundaries | 8 | 1 | 9 | 0 |
| Regeneration on farmland | 10 | 1 | 12 | 2 |
| Shaded perennial crops | 11 | 3 | 9 | 2 |
| Trees planted on cropland | 7 | 15 | 11 | 4 |
| Trees with livestock | 11 | 1 | 11 | 2 |
| Cross-family context | 10 | 5 | 12 | 1 |
| **Practice-wide** | 38 | 0 | 49 | 5 |
| **All scopes** | 95 | 26 | 113 | 16 |

[Inspect individual rows, context and evidence references](https://github.com/RuralScan/evidence/blob/8285769cb6df6cffc6bfbbbddead3ceadd07c635/publication/recipes/agroforestry.md)

## Check suitability before mapping

Read each mapping’s evidence and limitations. A row can offer several functions. Selection identifies the effective function. The spatial validation count uses the producer’s execution-readiness flag.

| Family | Variables in T4 | Mappings with options | With selected function | Spatially validated |
|---|---|---:|---:|---:|
| Linear plantings and boundaries | `land_cover` | 1 | 1 | 0 |
| Regeneration on farmland | `land_cover` | 1 | 1 | 0 |
| Shaded perennial crops | `land_cover` | 3 | 3 | 0 |
| Trees planted on cropland | `accessibility_travel_time`, `annual_precipitation`, `conflict_fragility_index`, `electrification_index`, `extension_governance`, `finance_credit_access`, `labour_availability`, `land_cover`, `market_value_chain`, `mean_annual_temperature`, `protected_area_status`, `slope`, `soil_organic_carbon`, `soil_ph`, `tenure_security` | 6 | 4 | 0 |
| Trees with livestock | `land_cover` | 1 | 1 | 0 |
| Cross-family context | `annual_precipitation`, `elevation`, `ndvi`, `slope`, `soil_organic_carbon` | 4 | 0 | 0 |

Access, finance and tenure can appear in compiled records. Evaluate these implementation factors through the investment-risk screen and local follow-up. The core suitability assessment uses its structural constraints and hard exclusions.

[Open the candidate’s T4 section](https://github.com/RuralScan/evidence/blob/8285769cb6df6cffc6bfbbbddead3ceadd07c635/publication/recipes/agroforestry.md#t4-suitability-mappings) · [Prepare a scoping brief](../handbook/implement-a-scan.md)

<details>
<summary>Family IDs for configuration and evidence lookup</summary>

Use `agroforestry` for the practice ID.

- Homegardens · `agroforestry__homegardens_proximity`
- Linear plantings and boundaries · `agroforestry__linear_boundary`
- Regeneration on farmland · `agroforestry__regeneration_farmland`
- Shaded perennial crops · `agroforestry__shaded_perennial`
- Trees planted on cropland · `agroforestry__planted_silvoarable`
- Trees with livestock · `agroforestry__silvopastoral`
- Cross-family context · `agroforestry__cross_family`

</details>
