# Water Harvesting and Conservation

[Choose another practice](README.md)

Identify where water originates and where it will be used. A field receiving rainfall, a short slope feeding a basin and a channel supplying storage belong to different families.

## Choose a family

| Family | What determines the choice? | Registered variants | Intended spatial product |
|---|---|---|---|
| In-field water conservation | Examine how rainfall infiltrates and is retained in the cultivated soil. | Contour bunds / ridges, Planting pits / Zai, Conservation tillage / mulching | Area suitability |
| Microcatchments | Locate the short runoff-producing slope and the adjacent basin or planting strip it supplies. | Semi-circular bunds, Eyebrow terraces, Runoff strips | Area suitability |
| Rooftop harvesting | Inspect the roof and domestic storage arrangement at building scale. | Rooftop / domestic harvesting | Qualitative guidance |
| Runoff capture and storage | Trace the contributing drainage area, then check storage terrain and the chosen structure’s siting requirements. | Macro-catchment water harvesting, Farm ponds, Check dams, Percolation tanks, Sand dams, Subsurface dams, Small communal tanks / reservoirs | Applicability zone |
| Spate or floodwater harvesting | Locate an ephemeral channel and examine the floodwater and sediment it carries. | Spate / floodwater harvesting | Linear corridor |
| Terracing | Inspect slope and the soil depth needed to reshape it. For stone structures, check material availability. | Bench terraces, Stone bunds / fanya juu | Area suitability |
| Cross-family context | Read shared observations here. Choose a specific intervention family when defining a map. | Cross-cutting envelope (family-agnostic) | Qualitative guidance |

[Practice definition (T0)](https://github.com/RuralScan/method/blob/92f86f035792cacb066eecdc12f439a87ef6d0c0/data-model/configuration/recipes/water_harvesting_conservation/T0_nbs_registry.csv) · [Variant definitions and grouping rationale (FAM)](https://github.com/RuralScan/method/blob/92f86f035792cacb066eecdc12f439a87ef6d0c0/data-model/configuration/FAM_family_registry.csv)

## Interpret the spatial output

- **Applicability zone.** A zone in which to inspect individual locations. Field layouts and structure footprints need local delineation.
- **Area suitability.** A potential area surface at a resolution supported by the inputs.
- **Qualitative guidance.** A qualitative assessment or contextual evidence. No pixel-area footprint is assigned.
- **Linear corridor.** A reach or corridor along a network. Report its length or reach-level coverage and document any width assumption.

For bench terraces, check the slope and soil information for the proposed design. The documented annual rainfall range in the worked example supports a siting observation. Its numerical calibration remains on hold.

[Trace the bench-terrace rainfall decision](../handbook/read-a-suitability-recipe.md)

## Inspect compiled evidence

Each count is an analytical row in the pinned candidate. The family named on the row determines where it is counted. Rows with no family ID appear once under **Practice-wide**, including rows limited to a particular geography or farming system.

| Scope | T3 hazard responses | T4 suitability mappings | T6 scorecard effects | T6E economic profiles |
|---|---:|---:|---:|---:|
| In-field water conservation | 11 | 4 | 11 | 1 |
| Microcatchments | 7 | 3 | 8 | 1 |
| Rooftop harvesting | 0 | 0 | 0 | 0 |
| Runoff capture and storage | 13 | 6 | 11 | 4 |
| Spate or floodwater harvesting | 5 | 0 | 6 | 2 |
| Terracing | 11 | 4 | 11 | 3 |
| Cross-family context | 5 | 0 | 10 | 2 |
| **Practice-wide** | 40 | 0 | 54 | 8 |
| **All scopes** | 92 | 17 | 111 | 21 |

[Inspect individual rows, context and evidence references](https://github.com/RuralScan/evidence/blob/8ef5b58f5245481548ff04834c8601745d9a49f6/publication/recipes/water_harvesting_conservation.md)

## Check suitability before mapping

Read each mapping’s evidence and limitations. A row can offer several functions. Selection identifies the effective function. The spatial validation count uses the producer’s execution-readiness flag.

| Family | Variables in T4 | Mappings with options | With selected function | Spatially validated |
|---|---|---:|---:|---:|
| In-field water conservation | `annual_precipitation`, `aridity_index`, `slope`, `soil_depth_to_bedrock` | 0 | 0 | 0 |
| Microcatchments | `annual_precipitation`, `slope`, `soil_depth_to_bedrock` | 0 | 0 | 0 |
| Runoff capture and storage | `annual_precipitation`, `catchment_area`, `drainage_density`, `runoff_potential_index`, `slope`, `stream_order` | 0 | 0 | 0 |
| Terracing | `annual_precipitation`, `runoff_potential_index`, `slope`, `soil_depth_to_bedrock` | 0 | 0 | 0 |

[Open the candidate’s T4 section](https://github.com/RuralScan/evidence/blob/8ef5b58f5245481548ff04834c8601745d9a49f6/publication/recipes/water_harvesting_conservation.md#t4-suitability-mappings) · [Prepare a scoping brief](../handbook/implement-a-scan.md)

<details>
<summary>Family IDs for configuration and evidence lookup</summary>

Use `water_harvesting_conservation` for the practice ID.

- In-field water conservation · `water_harvesting__in_situ`
- Microcatchments · `water_harvesting__micro_catchment`
- Rooftop harvesting · `water_harvesting__rooftop`
- Runoff capture and storage · `water_harvesting__runoff_catchment`
- Spate or floodwater harvesting · `water_harvesting__spate`
- Terracing · `water_harvesting__terracing`
- Cross-family context · `water_harvesting__cross_family`

</details>
