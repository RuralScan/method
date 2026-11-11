---
title: Mangrove restoration
slug: practice-mangrove_restoration
summary: Understand why mangrove restoration is a separate practice with a single tidal-coastal family, what governs its footprint, how its mixed effect locus and comparator rules shape the effect rows, and which inputs remain unset.
sources:
  - methodology/families/mangrove.md
  - methodology/families/forest_restoration.md
  - schema/registers/FAM_family_registry.csv
  - schema/recipes/mangrove_restoration/T0_nbs_registry.csv
  - schema/recipes/mangrove_restoration/T4_suitability_mappings.csv
  - schema/recipes/mangrove_restoration/T3_nbs_hazard_farming.csv
  - schema/recipes/mangrove_restoration/T6_nbs_scorecard.csv
  - schema/lookups/effect_locus.csv
  - schema/lookups/comparator_policy.csv
  - methodology/feasibility_notes.md
  - methodology/T4_generation_method.md
  - AGENTS.md
  - method:cookbook/mangrove_restoration.md
---
## Definition and boundary

Mangrove restoration, in this method, restores mangrove forest along tidal coasts either by re-establishing water exchange so that mangroves regenerate, or by planting where local conditions support establishment [src: schema/recipes/mangrove_restoration/T0_nbs_registry.csv §description_short]. It is planned at landscape scale; the farming-system entry `all` means any adjoining farming system can be considered, while the footprint depends on local coastal conditions [src: methodology/families/mangrove.md §Reading the practice definition (T0)].

The method treats mangroves as their own practice, not a forest-restoration family, because the dominant limiting factors differ in kind, not degree: tidal position and hydroperiod, salinity, coastal geomorphology (accreting versus eroding shoreline) and propagule supply. None of the terrestrial suitability logic (rainfall envelope, slope, soil depth) transfers, and the evidence base (coastal protection, surge and wave attenuation, silvo-aquaculture) is distinct [src: methodology/families/mangrove.md §Why its own NbS, not a forest-restoration family].

Neighbours:

- **Forest restoration.** [[practice:forest_restoration]] covers terrestrial forest. An earlier coastal family identifier under forest restoration is superseded; terrestrial and tidal envelopes are never pooled [src: methodology/families/forest_restoration.md §F4 — Historical mangrove proposal (superseded 2026-10-19)].
- **Coastal wetlands.** Tidal marsh and salt-marsh restoration is a family of [[practice:wetland_management]] (`wetland_management__coastal`), parked under the same coastal scope question [src: schema/registers/FAM_family_registry.csv §tidal_marsh_restoration].

The T0 record places the practice in the stocktake's tree-based catalogue group (`cluster = tree_based`) for cataloguing only; suitability is defined by the tidal-coastal family [src: methodology/families/mangrove.md §Reading the practice definition (T0)].

## Suitability families

The registry records exactly one family for this practice:

{{csv:schema/registers/FAM_family_registry.csv|where=nbs_id=mangrove_restoration|cols=subpractice_id,name,suitability_family_id,spatial_product_type,dominant_limiting_factor}}

### Tidal-coastal (`mangrove_restoration__tidal_coastal`)

Sub-practices: mangrove restoration by planting, and ecological mangrove restoration (EMR), which restores tidal hydrology and lets mangroves regenerate naturally rather than mass-planting [src: schema/registers/FAM_family_registry.csv §ecological_mangrove_restoration]. The shared limiting factor is coastal hydrology: tidal hydroperiod, salinity, intertidal elevation, sediment supply and wave energy; natural recruitment additionally depends on propagules reaching the site [src: schema/recipes/mangrove_restoration/T0_nbs_registry.csv §description_technical]. Product: `area_suitability`, an area within the coastal zone.

The scheme is deliberately one family to start. Both sub-practices establish mangrove on the same tidal envelope; what differs is the **method** (plant, or restore hydrology and let propagules arrive). The evidence says method is the main determinant of success: the Vietnamese record holds measured accretion where siting and establishment worked and a whole province's planting washing out where they did not. Method is therefore carried on each evidence unit (as the source's own description of the practice) rather than as separate families, until evidence shows the two need different suitability surfaces [src: methodology/families/mangrove.md §The scheme, deliberately one family to start].

There is no host-system gate in the agroforestry sense. The observed-distribution principle still applies in spirit: where existing or former mangrove extent and tidal connectivity can be observed, they are better evidence of what can establish than a modelled niche [src: methodology/T4_generation_method.md §2.5 Constrain by observed distribution, not a modelled niche, where data exist].

## What governs where it fits

**Biophysical.** Intertidal elevation relative to tidal datum, hydroperiod (frequency and duration of flooding), salinity, sediment supply and wave exposure govern the footprint [src: schema/recipes/mangrove_restoration/T0_nbs_registry.csv §description_technical]. For EMR the first question is whether tidal exchange can be restored at all; the user-facing guidance is to verify local tidal connectivity before choosing between planting and hydrological restoration [src: method:cookbook/mangrove_restoration.md §Interpret the spatial output].

**System.** Farming systems describe the surrounding landscape rather than gating establishment [src: schema/recipes/mangrove_restoration/T0_nbs_registry.csv §description_technical]. No system gate is compiled.

**Operational.** Hard exclusions follow the general rule; soft factors (tenure, community governance, access, finance) are operational-risk inputs, not suitability [src: AGENTS.md §What is locked]. Project-specific timing and cost inputs are discussed below.

## Effects and hazards

Effect rows are generated by cell synthesis with an applicability envelope, a transfer class and a two-axis confidence [src: AGENTS.md §What is locked]. At the pin the hazard rows cover flood, wind and cyclone, extreme rainfall, sedimentation, waterlogging and drought [src: schema/recipes/mangrove_restoration/T3_nbs_hazard_farming.csv]. Extreme rainfall and sedimentation are asset-threat-only hazards: they describe risk to the planted stand, not a livelihood response [src: AGENTS.md §What is locked]. Scorecard rows address flood hazard, soil erosion, water quality, biodiversity, carbon, production gap and rural poverty [src: schema/recipes/mangrove_restoration/T6_nbs_scorecard.csv].

**Effect locus.** Mangrove restoration is `mixed`. Protection value lands on the coast behind the stand (off-site), while fishery, crab and silvo-aquaculture value can accrue to the household working the stand itself. This differs from terrestrial forest restoration, which is off-site outright [src: schema/lookups/effect_locus.csv].

{{csv:schema/lookups/effect_locus.csv|where=nbs_id=mangrove_restoration|cols=nbs_id,suitability_family_id,effect_locus}}

**Comparator caveats.** Much of the storm-protection literature measures what **existing** mangroves do (wave attenuation, surge protection, avoided storm damage). That is evidence for keeping mangroves, not for what planting achieves within a project horizon; the provincial wash-out above is the standing illustration. Such units are tagged `existing_forest`, kept in the family row and excluded from the practice roll-up. A restored stand short of an intact reference stand is a recovery note, never harm [src: schema/lookups/comparator_policy.csv].

{{csv:schema/lookups/comparator_policy.csv|where=nbs_id=mangrove_restoration|cols=nbs_id,comparator,rollup_included,home_family}}

**Attribution and maladaptation themes.** Household welfare gains reported in one ex-post evaluation of a coastal wetlands project were attributed by its authors to resettlement and technology transfer bundled with the planting, not to the mangroves; the method does not credit those numbers to the practice [src: methodology/feasibility_notes.md §2026-10-19 · mangrove_restoration · welfare outcomes came from the bundle, not the trees]. Bundled interventions are never credited in full to one practice [src: AGENTS.md §What is locked]. Planting on unsuitable tidal positions fails outright, which is why siting carries the method's main risk.

**Costs and timing.** The economic archetype is `long_horizon`, reflecting the time and continuing care needed to restore a functioning stand. Blue-carbon crediting depends on a project meeting its chosen standard [src: methodology/families/mangrove.md §Reading the practice definition (T0)]. Costs are indicative and ordinal, held in the economic profile table by income group, not a cost-benefit analysis. See [[ch:cost-profiles]].

## Scheme status and open questions

The one-family scheme is recorded as signed off, with domain review welcome and able to amend it [src: methodology/families/mangrove.md]. Recorded open question: whether EMR should split into its own family once suitability evidence arrives, since its limiting factor arguably adds hydrological connectivity (can the tide be restored at all), closer to the wetland floodplain-reconnection logic [src: methodology/families/mangrove.md §The scheme, deliberately one family to start].

The registry rationale still carries the earlier note "parked from discovery pending scope decision" alongside the promotion to its own practice; the promotion supersedes the park [src: schema/registers/FAM_family_registry.csv §mangrove_restoration].

**No suitability mapping is compiled at the pin** [src: schema/recipes/mangrove_restoration/T4_suitability_mappings.csv]. This is "not yet evidenced", not a parking decision: the evidence acquired so far is effect evidence re-homed from the earlier forest-restoration coastal family [src: methodology/families/mangrove.md §What moved at the promotion (2026-10-19)].

Three T0 operational inputs are deliberately left unset: the establishment period (needed for the establishment-period adjustment in the project-risk screen), the time to benefit, and the recurrent cost class; the optional upfront cost range is also empty. The source explains that published recovery intervals measure forest recovery, not a project establishment endpoint, and that different benefits (fisheries, hydrological function, soil carbon) mature over different periods, so each must be specified locally against a stated endpoint [src: methodology/families/mangrove.md §Reading the practice definition (T0)].

## Assumptions and limits

- A single family assumes planting and EMR share one suitability surface; this is provisional.
- Without compiled T4 mappings the method cannot yet produce a mangrove suitability surface. Global coastal layers are unlikely to resolve intertidal elevation and hydroperiod at the precision siting needs; feasibility must survey them.
- Existing-stand protection evidence does not transfer to young plantings within a project horizon.
- Welfare outcomes require a budgeted complementary livelihood package; the trees alone did not deliver them in the one ex-post evaluation held [src: methodology/feasibility_notes.md §2026-10-19 · mangrove_restoration · welfare outcomes came from the bundle, not the trees].
- Establishment window, time to benefit and recurrent cost must be set per project, against a stated endpoint, before the M2b establishment-period adjustment is used [src: methodology/families/mangrove.md §Reading the practice definition (T0)].

## Where this is configured

- Family: [[table:FAM]]; practice definition and unset timing fields: [[table:T0]].
- Suitability mappings (none compiled at the pin): [[table:T4]].
- Hazard responses: [[table:T3]]; scorecard: [[table:T6]]; economic profiles by income group: [[table:T6E]].
- Evidence: [[table:EV]], [[table:SRC]].
- Lookups: `schema/lookups/effect_locus.csv`, `comparator_policy.csv`.
