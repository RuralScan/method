# Forest Restoration

[Choose another practice](README.md)

Distinguish recovery toward an ecological baseline from production forestry. Check whether seed sources and residual trees can support recovery, whether planting is needed, or whether existing forest needs protection.

## Choose a family

| Family | What determines the choice? | Registered variants | Intended spatial product |
|---|---|---|---|
| Active planting | Check land history, existing canopy and whether the intended trees can establish. | Reforestation, Afforestation, Enrichment planting | Area suitability |
| Assisted regeneration | Identify surviving regeneration potential and the intervention needed for recovery. | Assisted natural regeneration (ANR) | Area suitability |
| Passive regeneration | Look for seed sources and residual cover, and assess whether the pressure preventing recovery can be removed. | Passive natural regeneration, Secondary succession | Area suitability |
| Plantation forestry | Confirm that production forestry is the objective and assess establishment of the target species. | Plantation forestry (tree farming) | Area suitability |
| Protection and community forest management | Locate existing forest and the pressures that threaten it. | Forest protection / avoided degradation, Community-based forest management | Applicability zone |
| Cross-family context | Read shared observations here. Choose a specific intervention family when defining a map. | Cross-cutting envelope (family-agnostic) | Qualitative guidance |

[Practice definition (T0)](https://github.com/RuralScan/method/blob/92f86f035792cacb066eecdc12f439a87ef6d0c0/data-model/configuration/recipes/forest_restoration/T0_nbs_registry.csv) · [Variant definitions and grouping rationale (FAM)](https://github.com/RuralScan/method/blob/92f86f035792cacb066eecdc12f439a87ef6d0c0/data-model/configuration/FAM_family_registry.csv)

## Interpret the spatial output

- **Applicability zone.** A zone in which to inspect individual locations. Field layouts and structure footprints need local delineation.
- **Area suitability.** A potential area surface at a resolution supported by the inputs.
- **Qualitative guidance.** A qualitative assessment or contextual evidence. No pixel-area footprint is assigned.

Confirm prior land cover and the intended ecological baseline before proposing tree planting. On non-forest ecosystems, assess the risk of harm from afforestation.

## Inspect compiled evidence

Each count is an analytical row in the pinned candidate. The family named on the row determines where it is counted. Rows with no family ID appear once under **Practice-wide**, including rows limited to a particular geography or farming system.

| Scope | T3 hazard responses | T4 suitability mappings | T6 scorecard effects | T6E economic profiles |
|---|---:|---:|---:|---:|
| Active planting | 7 | 0 | 10 | 3 |
| Assisted regeneration | 5 | 0 | 4 | 2 |
| Passive regeneration | 8 | 0 | 9 | 2 |
| Plantation forestry | 6 | 0 | 5 | 1 |
| Protection and community forest management | 10 | 0 | 11 | 3 |
| Cross-family context | 2 | 0 | 8 | 1 |
| **Practice-wide** | 18 | 0 | 24 | 4 |
| **All scopes** | 56 | 0 | 71 | 16 |

[Inspect individual rows, context and evidence references](https://github.com/RuralScan/evidence/blob/950f91ea29cea43a5a1a7928bddaef7758965cc7/publication/recipes/forest_restoration.md)

## Check suitability before mapping

This candidate contains zero compiled T4 mappings for this practice. The family definitions describe the intended product. A local suitability score would require supported mappings and spatial validation.

[Open the candidate’s T4 section](https://github.com/RuralScan/evidence/blob/950f91ea29cea43a5a1a7928bddaef7758965cc7/publication/recipes/forest_restoration.md#t4-suitability-mappings) · [Prepare a scoping brief](../handbook/implement-a-scan.md)

<details>
<summary>Family IDs for configuration and evidence lookup</summary>

Use `forest_restoration` for the practice ID.

- Active planting · `forest_restoration__active_planting`
- Assisted regeneration · `forest_restoration__assisted_regeneration`
- Passive regeneration · `forest_restoration__passive_regeneration`
- Plantation forestry · `forest_restoration__plantation`
- Protection and community forest management · `forest_restoration__protection_cbfm`
- Cross-family context · `forest_restoration__cross_family`

</details>
