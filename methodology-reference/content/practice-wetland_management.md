---
title: Wetland management and restoration
slug: practice-wetland_management
summary: Understand how the method splits wetland work into restoration, creation and peatland families, which families are parked and why, how the held step profiles work, and how off-site effects and opportunity costs are treated.
sources:
  - methodology/families/wetland_management.md
  - schema/registers/FAM_family_registry.csv
  - schema/recipes/wetland_management/T0_nbs_registry.csv
  - schema/recipes/wetland_management/T4_suitability_mappings.csv
  - schema/recipes/wetland_management/T3_nbs_hazard_farming.csv
  - schema/recipes/wetland_management/T6_nbs_scorecard.csv
  - methodology/families/riparian_buffer.md
  - methodology/T4_generation_method.md
  - methodology/feasibility_notes.md
  - schema/lookups/effect_locus.csv
  - schema/lookups/comparator_policy.csv
  - schema/lookups/crop_scope_policy.csv
  - AGENTS.md
  - method:cookbook/wetland_management.md
---
## Definition and boundary

Wetland management and restoration, in this method, means restoring, rewetting or creating inland wetlands, including peatlands and paludiculture, to recover hydrology, storage, water quality, habitat and carbon in rural landscapes [src: schema/recipes/wetland_management/T0_nbs_registry.csv §description_short]. Every wetland intervention is gated by hydrology: water table, inundation regime, drainage history and water availability [src: methodology/families/wetland_management.md §1. The grouping principle]. It is planned at watershed scale and applicable alongside any farming system [src: schema/recipes/wetland_management/T0_nbs_registry.csv].

Neighbours:

- **Water harvesting.** Ponds and tanks that store runoff are [[practice:water_harvesting_conservation]]; the method treats "water harvesting ≠ wetland creation" as a standing check against clustering by appearance [src: methodology/T4_generation_method.md §2.1 Practice definition → subpractices → suitability families].
- **Riparian buffers.** Floodplain reconnection targeting the wetland body is here; the streamside strip is [[practice:riparian_buffer]] [src: methodology/families/wetland_management.md §4. Edge cases the scheme resolves]. Floodplain reconnection was removed from riparian buffers and lives in this practice [src: AGENTS.md §What is locked].
- **Mangrove restoration.** Mangroves are [[practice:mangrove_restoration]]. Tidal marsh is a parked family here.

## Suitability families

Families split on the intervention driver (restore an existing or degraded wetland, create a new one, or rewet peat), because that sets the variable set and the suitable extent [src: methodology/families/wetland_management.md §1. The grouping principle].

The registry rows for this practice:

{{csv:schema/registers/FAM_family_registry.csv|where=nbs_id=wetland_management|cols=subpractice_id,name,suitability_family_id,spatial_product_type,dominant_limiting_factor}}

### Restoration and rewetting (`wetland_management__restoration_rewetting`)

Sub-practices: wetland restoration or rewetting, drainage blocking and re-flooding, and floodplain wetland reconnection. The limiting factor is former or degraded wetland extent plus hydrology (water table, drainage history, connectivity to the water source): restore what was [src: schema/registers/FAM_family_registry.csv §wetland_restoration]. Product: `area_suitability`. The observed-distribution principle applies directly: the gating layer is where a wetland was or is degrading, not a modelled niche [src: methodology/T4_generation_method.md §2.5 Constrain by observed distribution, not a modelled niche, where data exist].

### Creation (`wetland_management__creation`)

Sub-practices: wetland creation and wetland reconstruction. The limiting factor is water availability, low-lying or depression terrain, soil permeability and the fact that the land is currently not wetland: a siting problem, not a restore-what-was problem, hence a different variable set [src: methodology/families/wetland_management.md §F2 — Wetland creation]. Product: `area_suitability`. A documented implementation (freshwater lagoons excavated alongside drains on a sugarcane floodplain) describes how a scheme was built; it yields no siting cutoff [src: methodology/families/wetland_management.md §F2 — Wetland creation].

### Peatland rewetting and paludiculture (`wetland_management__peatland`)

Sub-practices: peatland rewetting and paludiculture (productive use of wet or rewetted peat: wet meadow, pasture, reed). The limiting factor is peat soil presence plus drainage state and water table; peat depth and extent, subsidence and carbon make this a distinct variable set rather than a context of restoration [src: methodology/families/wetland_management.md §F3 — Peatland restoration / paludiculture]. Paludiculture additionally needs a suitable wet crop [src: schema/registers/FAM_family_registry.csv §paludiculture]. Product: `area_suitability`. Tropical peat (South-East Asia, Congo Basin) is a major rural carbon and land-use case in LMICs [src: methodology/families/wetland_management.md §F3 — Peatland restoration / paludiculture].

### Constructed or treatment wetlands (`wetland_management__constructed`): qualitative only, parked

Engineered wetlands for point-source or agricultural-drainage treatment are a siting and engineering problem, often peri-urban, rather than a landscape suitability surface. The registry records the family as `qualitative_only` and parked [src: schema/registers/FAM_family_registry.csv §constructed_treatment_wetland]. Qualitative-only families are parked out of the generated effect tables, with their evidence retained for implementation guidance [src: AGENTS.md §What is locked].

### Coastal wetlands (`wetland_management__coastal`): parked

Tidal marsh and salt-marsh restoration, gated by coastal hydrology (tidal inundation, salinity, elevation). Product: `area_suitability`. The registry records it as parked under the same coastal scope question once raised for mangroves [src: schema/registers/FAM_family_registry.csv §tidal_marsh_restoration]. The family nonetheless holds effect rows, because evidence measured on existing coastal marsh is routed to it [src: schema/lookups/comparator_policy.csv].

## What governs where it fits

**Biophysical and hydrological.** The leading variables are [[var:water_table_depth]], inundation regime, drainage history, [[var:distance_to_waterbody]] or connectivity, terrain position, soil permeability and, for peatland, peat presence [src: methodology/families/wetland_management.md §2. Proposed families].

**Reviewed step profiles, not a global rule.** The T4 table at the pin holds mappings for restoration (distance to waterbody), creation (distance to waterbody) and peatland ([[var:water_table_depth]] and [[var:groundwater_seepage]]) [src: schema/recipes/wetland_management/T4_suitability_mappings.csv]. Each is a piecewise function reconciled from reviewed ordinal source bands, with versioned semantic class scores. Each requires an explicit choice of source-context profile; there is no global consensus profile and no automatic inheritance between families [src: schema/recipes/wetland_management/T4_suitability_mappings.csv]. A run must therefore select the profile whose source context matches the target landscape; a profile chosen without that match is a transfer the user must justify.

**System.** Restoration is gated by observed former or degraded extent; creation by currently non-wetland land; peatland by observed peat soils and drainage state. Existing use of the wetland (cultivation, harvesting, fishing) is not a suitability factor but defines the opportunity cost (see below).

**Operational.** Water bodies, urban areas and legal protected areas are hard exclusions. Tenure, governance and community use rights are soft and route to the operational-risk filter and implementation guidance [src: AGENTS.md §What is locked].

## Effects and hazards

Effect rows are generated by cell synthesis with an applicability envelope, a transfer class and a two-axis confidence [src: AGENTS.md §What is locked]. Hazard rows at the pin cover flood, drought, waterlogging, wind and cyclone, fire, and extreme rainfall as an asset threat [src: schema/recipes/wetland_management/T3_nbs_hazard_farming.csv]. Scorecard rows address water stress, catchment water yield, water quality, flood and drought hazard, soil erosion, biodiversity, carbon, production gap, rural poverty and food insecurity [src: schema/recipes/wetland_management/T6_nbs_scorecard.csv].

**Effect locus.** Wetland management is `off_site`: wetland works sit outside cropped land, so farmer effects are hydrological and downstream [src: schema/lookups/effect_locus.csv].

{{csv:schema/lookups/effect_locus.csv|where=nbs_id=wetland_management|cols=nbs_id,suitability_family_id,effect_locus}}

**Crop-specific evidence.** In paludiculture the crop (reed, cattail, Sphagnum, sago) is the practice, so crop-specific units re-enter the peatland family's effect cells; species-specific units never do [src: schema/lookups/crop_scope_policy.csv].

**Comparator caveats.** Studies of what existing wetlands or floodplains do are evidence for keeping or restoring them, not for creating new ones; they stay in the restoration family row, out of the roll-up. Existing coastal marsh evidence goes to the coastal family. A restored wetland falling short of an intact reference wetland is not harm; a more sensible baseline is the condition before restoration or creation, or the gain in landscape connectivity, and such units are kept as recovery notes that never set a class [src: schema/lookups/comparator_policy.csv].

{{csv:schema/lookups/comparator_policy.csv|where=nbs_id=wetland_management|cols=nbs_id,comparator,rollup_included,home_family}}

**Trade-offs and maladaptation themes.**

- **Opportunity cost.** Households already draw income from the wetlands restoration would alter (cultivation, product sales, fish catches). These are treated as the counterfactual, recorded as non-voting notes in the poverty and production cells, not as benefits of restoring [src: methodology/feasibility_notes.md §2026-10-16 · wetland_management · existing-use income is the opportunity cost of rewetting].
- **Service decay.** Created basins can lose sediment and phosphorus retention as they fill while nitrate removal persists; a wetland traps eroded sediment but does not prevent landscape erosion, so the erosion-risk route for this case was removed and the unit votes on water quality only [src: methodology/feasibility_notes.md §2026-10-19 · wetland_management (creation) · sediment trapping decays without maintenance].
- **Coastal maintenance.** Most salt-marsh deterioration comes from frequent moderate storms rather than rare intense ones, so the maintenance burden is continuous [src: methodology/feasibility_notes.md §2026-10-15 · wetland_management (coastal) · budget for steady edge retreat, not storm repair].

## Scheme status and open questions

The family note is a draft for domain sign-off. Its open questions cover the restore, create and peatland split; whether constructed or treatment wetlands are in scope for a rural landscape scan; whether coastal wetlands are in scope; the floodplain boundary with riparian buffers; hydrology datasets at scoping grade; and naming [src: methodology/families/wetland_management.md §6. Open questions for sign-off]. The floodplain boundary is now settled in the registry: reconnection of the wetland body belongs here and no riparian floodplain family exists [src: AGENTS.md §What is locked]. The note still describes a parked riparian floodplain family; follow the registry.

Status by family:

- Restoration and rewetting, creation, peatland: **evidenced**, with reviewed step profiles that require explicit source-context selection; none is a default global function.
- Constructed or treatment wetlands: **parked** pending the scope question (qualitative only, engineering siting); the registry records it as a scope question, not a final exclusion.
- Coastal wetlands: **parked** pending the coastal scope question; no suitability mapping, though effect rows exist.

The note says no wetland T4 rows exist; that is out of date at the pin [src: schema/recipes/wetland_management/T4_suitability_mappings.csv]. Some wetland suitability units were extracted incidentally during effect extraction; they stay in the register, but this is not a completed suitability search [src: methodology/effect_evidence_followups.md §1g. Drought-year round 2 (2026-10-06, all three NbS)].

## Assumptions and limits

- Former wetland extent, water table and drainage history are poorly observed by global products; candidate layers (surface-water history, inundation, hydrography, peat maps) must be resolved through dataset bindings and checked locally [src: methodology/families/wetland_management.md §6. Open questions for sign-off].
- The method cannot judge whether hydrology can actually be restored at a site; that requires survey and hydrological design.
- Effects are off-site and accrue to people other than those bearing the opportunity cost; feasibility must count forgone wetland-use income and plan replacement livelihoods [src: methodology/feasibility_notes.md §2026-10-16 · wetland_management · existing-use income is the opportunity cost of rewetting].
- Restored wetlands rarely match intact ones; the method does not score that shortfall as harm, and does not claim full recovery.

## Where this is configured

- Families: [[table:FAM]]; practice definition: [[table:T0]].
- Suitability step profiles: [[table:T4]], [[table:T4_NUMERIC_POLICY]]; dataset bindings: [[table:BIND]], [[table:T1]].
- Hazard responses: [[table:T3]]; scorecard: [[table:T6]]; economic profiles: [[table:T6E]].
- Evidence: [[table:EV]], [[table:SRC]]; variables: [[table:VONT]].
- Lookups: `schema/lookups/effect_locus.csv`, `comparator_policy.csv`, `crop_scope_policy.csv`.
