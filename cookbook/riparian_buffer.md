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

Check how accurately the stream network, adjacent land use and buffer width can be resolved. Confirm the width on the ground before estimating a planted footprint.

## Inspect compiled evidence

Each count is an analytical row in the pinned candidate. The family named on the row determines where it is counted. Rows with no family ID appear once under **Practice-wide**, including rows limited to a particular geography or farming system.

| Scope | T3 hazard responses | T4 suitability mappings | T6 scorecard effects | T6E economic profiles |
|---|---:|---:|---:|---:|
| Natural or restored riparian vegetation | 3 | 0 | 6 | 0 |
| Planted riparian buffers | 2 | 0 | 5 | 0 |
| **Practice-wide** | 2 | 0 | 11 | 2 |
| **All scopes** | 7 | 0 | 22 | 2 |

[Inspect individual rows, context and evidence references](https://github.com/RuralScan/evidence/blob/8ef5b58f5245481548ff04834c8601745d9a49f6/publication/recipes/riparian_buffer.md)

## Check suitability before mapping

This candidate contains zero compiled T4 mappings for this practice. The family definitions describe the intended product. A local suitability score would require supported mappings and spatial validation.

[Open the candidate’s T4 section](https://github.com/RuralScan/evidence/blob/8ef5b58f5245481548ff04834c8601745d9a49f6/publication/recipes/riparian_buffer.md#t4-suitability-mappings) · [Prepare a scoping brief](../handbook/implement-a-scan.md)

<details>
<summary>Family IDs for configuration and evidence lookup</summary>

Use `riparian_buffer` for the practice ID.

- Natural or restored riparian vegetation · `riparian_buffer__natural_restored`
- Planted riparian buffers · `riparian_buffer__planted`

</details>
