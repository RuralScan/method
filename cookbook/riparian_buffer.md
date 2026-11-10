# Riparian Buffers

[Choose another practice](README.md)

Identify the watercourse and the condition of its banks. Choose between restoring existing riparian vegetation and establishing a planted strip.

## Choose a family

| Family | What determines the choice? | Registered variants | Intended spatial product |
|---|---|---|---|
| Natural or restored riparian vegetation | Identify bank degradation, existing vegetation, regeneration potential and connection to the watercourse. | Riparian natural regeneration, Riparian reforestation | Linear corridor |
| Planted riparian buffers | Inspect slope and available width beside the watercourse and the runoff entering from adjoining fields. | Planted grass/herbaceous filter strip, Planted woody/forested riparian buffer | Linear corridor |

[Practice definition (T0)](https://github.com/RuralScan/method/blob/92f86f035792cacb066eecdc12f439a87ef6d0c0/data-model/configuration/recipes/riparian_buffer/T0_nbs_registry.csv) · [Variant definitions and grouping rationale (FAM)](https://github.com/RuralScan/method/blob/92f86f035792cacb066eecdc12f439a87ef6d0c0/data-model/configuration/FAM_family_registry.csv)

## Interpret the spatial output

- **Linear corridor.** A reach or corridor along a network. Report its length or reach-level coverage and document any width assumption.

The two distance-to-waterbody mappings retain reported widths. For natural or restored vegetation, those widths describe study areas or guidance for particular banks. For planted strips, they describe planting zones or designs for particular services. Both mappings leave the distance score unassigned. Confirm stream position and local width before estimating a footprint.

## Inspect compiled evidence

Each count is an analytical row in the pinned candidate. The family named on the row determines where it is counted. Rows with no family ID appear once under **Practice-wide**, including rows limited to a particular geography or farming system.

| Scope | T3 hazard responses | T4 suitability mappings | T6 scorecard effects | T6E economic profiles |
|---|---:|---:|---:|---:|
| Natural or restored riparian vegetation | 3 | 1 | 6 | 0 |
| Planted riparian buffers | 2 | 1 | 5 | 0 |
| **Practice-wide** | 2 | 0 | 11 | 2 |
| **All scopes** | 7 | 2 | 22 | 2 |

[Inspect individual rows, context and evidence references](https://github.com/RuralScan/evidence/blob/1532768de6c688e2c8eb26097eb7618848390b1d/publication/recipes/riparian_buffer.md)

## Check suitability before mapping

Read each mapping’s evidence and limitations. A row can offer several functions. Selection identifies the effective function. The spatial validation count uses the producer’s execution-readiness flag.

| Family | Variables in T4 | Mappings with options | With selected function | Spatially validated |
|---|---|---:|---:|---:|
| Natural or restored riparian vegetation | `distance_to_waterbody` | 0 | 0 | 0 |
| Planted riparian buffers | `distance_to_waterbody` | 0 | 0 | 0 |

[Open the candidate’s T4 section](https://github.com/RuralScan/evidence/blob/1532768de6c688e2c8eb26097eb7618848390b1d/publication/recipes/riparian_buffer.md#t4-suitability-mappings) · [Prepare a scoping brief](../handbook/implement-a-scan.md)

<details>
<summary>Family IDs for configuration and evidence lookup</summary>

Use `riparian_buffer` for the practice ID.

- Natural or restored riparian vegetation · `riparian_buffer__natural_restored`
- Planted riparian buffers · `riparian_buffer__planted`

</details>
