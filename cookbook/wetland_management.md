# Wetland Management & Restoration

[Choose another practice](README.md)

Check present and former wetland extent, soil and water source. Creation, restoration of a former wetland, peatland rewetting and engineered treatment answer different siting questions.

## Choose a family

| Family | What determines the choice? | Registered variants | Intended spatial product |
|---|---|---|---|
| Coastal wetlands | Check tidal inundation, salinity and elevation. | Tidal marsh / coastal wetland restoration | Area suitability |
| Constructed treatment wetlands | Identify the inflow or drainage source and assess the engineered site. | Constructed / treatment wetland | Qualitative guidance |
| Peatland rewetting and paludiculture | Confirm peat soils, drainage state and water table. Paludiculture also requires a suitable wet crop. | Peatland rewetting, Paludiculture | Area suitability |
| Restoration and rewetting | Check former wetland extent, altered drainage and hydraulic connectivity. | Wetland restoration / rewetting, Drainage blocking / re-flooding, Floodplain wetland reconnection | Area suitability |
| Wetland creation or reconstruction | Check water supply, terrain and soils where a wetland could be established. | Wetland creation, Wetland reconstruction | Area suitability |

[Practice definition (T0)](https://github.com/RuralScan/method/blob/92f86f035792cacb066eecdc12f439a87ef6d0c0/data-model/configuration/recipes/wetland_management/T0_nbs_registry.csv) · [Variant definitions and grouping rationale (FAM)](https://github.com/RuralScan/method/blob/92f86f035792cacb066eecdc12f439a87ef6d0c0/data-model/configuration/FAM_family_registry.csv)

## Interpret the spatial output

- **Area suitability.** A potential area surface at a resolution supported by the inputs.
- **Qualitative guidance.** A qualitative assessment or contextual evidence. No pixel-area footprint is assigned.

For reconnection, verify former wetland extent and hydraulic connectivity. For peatland work, establish peat presence, drainage history and water-table conditions.

## Inspect compiled evidence

Each count is an analytical row in the pinned candidate. The family named on the row determines where it is counted. Rows with no family ID appear once under **Practice-wide**, including rows limited to a particular geography or farming system.

| Scope | T3 hazard responses | T4 suitability mappings | T6 scorecard effects | T6E economic profiles |
|---|---:|---:|---:|---:|
| Coastal wetlands | 3 | 0 | 8 | 3 |
| Constructed treatment wetlands | 0 | 0 | 0 | 0 |
| Peatland rewetting and paludiculture | 3 | 2 | 9 | 3 |
| Restoration and rewetting | 5 | 1 | 11 | 3 |
| Wetland creation or reconstruction | 1 | 1 | 5 | 1 |
| **Practice-wide** | 14 | 0 | 31 | 5 |
| **All scopes** | 26 | 4 | 64 | 15 |

[Inspect individual rows, context and evidence references](https://github.com/RuralScan/evidence/blob/1532768de6c688e2c8eb26097eb7618848390b1d/publication/recipes/wetland_management.md)

## Check suitability before mapping

Read each mapping’s evidence and limitations. A row can offer several functions. Selection identifies the effective function. The spatial validation count uses the producer’s execution-readiness flag.

| Family | Variables in T4 | Mappings with options | With selected function | Spatially validated |
|---|---|---:|---:|---:|
| Peatland rewetting and paludiculture | `groundwater_seepage`, `water_table_depth` | 2 | 0 | 0 |
| Restoration and rewetting | `distance_to_waterbody` | 1 | 0 | 0 |
| Wetland creation or reconstruction | `distance_to_waterbody` | 1 | 0 | 0 |

[Open the candidate’s T4 section](https://github.com/RuralScan/evidence/blob/1532768de6c688e2c8eb26097eb7618848390b1d/publication/recipes/wetland_management.md#t4-suitability-mappings) · [Prepare a scoping brief](../handbook/implement-a-scan.md)

<details>
<summary>Family IDs for configuration and evidence lookup</summary>

Use `wetland_management` for the practice ID.

- Coastal wetlands · `wetland_management__coastal`
- Constructed treatment wetlands · `wetland_management__constructed`
- Peatland rewetting and paludiculture · `wetland_management__peatland`
- Restoration and rewetting · `wetland_management__restoration_rewetting`
- Wetland creation or reconstruction · `wetland_management__creation`

</details>
