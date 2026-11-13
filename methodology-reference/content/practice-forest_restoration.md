---
title: Forest restoration
slug: practice-forest_restoration
summary: Understand how the method splits forest restoration along the restoration continuum, why plantations and mangroves sit outside the restoration roll-up, and what the suitability and effect evidence can and cannot support.
sources:
  - methodology/families/forest_restoration.md
  - methodology/families/mangrove.md
  - schema/registers/FAM_family_registry.csv
  - schema/recipes/forest_restoration/T0_nbs_registry.csv
  - schema/recipes/forest_restoration/README.md
  - schema/recipes/forest_restoration/T4_suitability_mappings.csv
  - schema/recipes/forest_restoration/T3_nbs_hazard_farming.csv
  - schema/recipes/forest_restoration/T6_nbs_scorecard.csv
  - methodology/audits/t4_followup_20261106/anr_proximity_decision.md
  - methodology/T4_generation_method.md
  - schema/lookups/effect_locus.csv
  - schema/lookups/comparator_policy.csv
  - schema/lookups/family_rollup_policy.csv
  - methodology/effect_evidence_followups.md
  - AGENTS.md
  - method:cookbook/forest_restoration.md
---
## Definition and boundary

Forest restoration, in this method, is the re-establishment or protection of forest structure, composition and function on degraded, deforested or non-forest land [src: schema/recipes/forest_restoration/T0_nbs_registry.csv §description_short]. Suitability is reasoned along the **restoration continuum**: passive natural regeneration once a pressure is removed, assisted natural regeneration where regeneration potential is partial, and active planting where natural regeneration will not deliver [src: schema/recipes/forest_restoration/T0_nbs_registry.csv §description_technical]. The practice is planned at landscape scale and is applicable alongside any farming system [src: schema/recipes/forest_restoration/T0_nbs_registry.csv §implementation_scale].

Neighbours it must not be confused with:

- **Agroforestry.** Regeneration or planting on farmland (FMNR, parkland retention, on-farm assisted regeneration) is [[practice:agroforestry]]. The boundary is the land system, farmland versus forest or non-farm land [src: methodology/families/forest_restoration.md §4. Edge cases the scheme deliberately resolves]. Agroforestry-based restoration also belongs to agroforestry.
- **Mangrove restoration.** Mangroves are a separate practice, [[practice:mangrove_restoration]], with their own coastal-hydrology family; terrestrial and tidal envelopes are never pooled [src: methodology/families/forest_restoration.md §F4 — Historical mangrove proposal (superseded 2026-10-19)].
- **Riparian buffers.** Streamside restoration is [[practice:riparian_buffer]], with a `zonal_linear` product [src: methodology/families/forest_restoration.md §4. Edge cases the scheme deliberately resolves].
- **Plantation forestry.** Production tree farming is registered under this practice as its own family but is excluded from the restoration roll-up (below).

## Suitability families

The grouping rule is the shared dominant limiting factor. The trap specific to restoration is that passive regeneration, assisted regeneration and planting all end with "forest returns" but are decided by different limiting factors: regeneration potential, intervention feasibility and the planting envelope respectively. They are therefore separate families [src: methodology/families/forest_restoration.md §1. The grouping principle].

The registry rows for this practice:

{{csv:schema/registers/FAM_family_registry.csv|where=nbs_id=forest_restoration|cols=subpractice_id,name,suitability_family_id,spatial_product_type,dominant_limiting_factor}}

The registry contains no mangrove family under this practice. The family note retains a historical "F4 mangrove/coastal" entry and states that its identifier and discovery hold are superseded; follow the registry [src: methodology/families/forest_restoration.md §Current routing (reconciled 2026-10-28)].

### Passive natural regeneration (`forest_restoration__passive_regeneration`)

Sub-practices: passive natural regeneration and secondary succession. The limiting factor is regeneration potential: proximity to remnant forest and seed sources, residual woody cover and rootstock, low prior land-use intensity, and whether the degrading pressure can be removed [src: methodology/families/forest_restoration.md §F1 — Passive natural regeneration]. Leading variables named in the scheme are distance to remnant forest, residual tree cover ([[var:tree_canopy_cover]]), degradation intensity, prior land use, slope and erosion, with climate as a coarse gate. Product: `area_suitability`, a pixel approximating land that will regenerate if released [src: methodology/families/forest_restoration.md §F1 — Passive natural regeneration].

### Assisted natural regeneration (`forest_restoration__assisted_regeneration`)

Sub-practice: assisted natural regeneration (weeding, fire and grazing protection, liberation thinning, releasing wildlings), still relying on natural propagules. It differs from passive regeneration because regeneration potential is only partial and because it needs **intervention feasibility** (access, labour, management) [src: schema/registers/FAM_family_registry.csv §assisted_natural_regeneration]. Product: `area_suitability`.

A reviewed interpretation fixes how remnant-forest proximity enters this family. A source statement that nearby remnant forest supports seed supply is retained as qualitative siting evidence. The final recipe must combine observed degraded or former-forest context, distance to contemporary remnant patches and a separate regeneration-potential check; recent forest loss alone does not establish suitability or land availability. No distance cutoff, loss-age window or score is approved, and the output before calibration is an annotated candidate footprint, not a 0–1 surface [src: methodology/audits/t4_followup_20261106/anr_proximity_decision.md §Proposed spatial interpretation for the final recipe]. Candidate datasets (a tropical moist forest disturbance product, a global forest-change product, national layers) are pointers only, not approved bindings [src: methodology/audits/t4_followup_20261106/anr_proximity_decision.md §Dataset candidates, not approved bindings].

### Active tree planting (`forest_restoration__active_planting`)

Sub-practices: reforestation, afforestation and enrichment planting. The limiting factor is the planting envelope for the target species or community plus degradation too severe for natural regeneration (no seed source, no rootstock) [src: methodology/families/forest_restoration.md §F3 — Active tree planting]. Product: `area_suitability`.

Two rules shape this family. First, **species or community is a parameter, not a sub-family**: the family runs per target and combines by maximum while retaining which target drives each pixel; single-species niche models inform the envelope but must not define the family [src: methodology/families/forest_restoration.md §F3 — Active tree planting]. Species envelopes never define a practice row [src: AGENTS.md §What is locked]. Second, **reforestation versus afforestation is a prior-land-cover context flag**, not a separate family. Afforestation of native grassland or peatland carries a do-no-harm flag; it is a caveat, not a suitability rule [src: schema/registers/FAM_family_registry.csv §afforestation].

### Plantation forestry (`forest_restoration__plantation`)

Sub-practice: plantation forestry, meaning establishment or management of production tree plantations, including afforestation of grassland or shrubland with plantation species. The criterion is plantation **structure** (commercial or cyclical-harvest planting, monocultures, plantation genera), not species origin [src: methodology/families/forest_restoration.md §Family added 2026-10-19 — `forest_restoration__plantation` (tree farming)]. The limiting factor is the planting envelope of the production species plus rotation economics, distinct from restoration toward a natural baseline [src: schema/registers/FAM_family_registry.csv §plantation_forestry]. Product: `area_suitability`.

The method treats plantations as tree farming, not restoration, because a plantation is not representative of the natural baseline that restoration aims to recover. The family keeps its own effect rows but never sets a practice-level forest-restoration class [src: schema/lookups/family_rollup_policy.csv].

{{csv:schema/lookups/family_rollup_policy.csv|where=nbs_id=forest_restoration|cols=nbs_id,suitability_family_id,rollup_included}}

The split moved catchment water-yield reductions and most hard cost evidence into the plantation family, and dissolved an apparent biodiversity conflict in active planting whose two sides were plantation versus natural-regeneration evidence [src: methodology/families/forest_restoration.md §Family added 2026-10-19 — `forest_restoration__plantation` (tree farming)]. Re-inclusion would need the condition "indigenous and diverse plantings" made operational in the evidence [src: schema/lookups/family_rollup_policy.csv]. Some units remain in active planting as `mixed_or_unclear` pending resolution [src: methodology/families/forest_restoration.md §Family added 2026-10-19 — `forest_restoration__plantation` (tree farming)].

### Forest protection and community forest management (`forest_restoration__protection_cbfm`)

Sub-practices: forest protection or avoided degradation, and community-based forest management. This is not new establishment. The structural part of the limiting factor is existing standing forest × degradation or deforestation pressure (a `system_constraint`); the governance and tenure part is soft enabling environment and routes to the project-risk filter and implementation guidance, not to T4 [src: methodology/families/forest_restoration.md §F5 — Forest protection & CBFM]. Product: `applicability_zone`, within the existing-forest mask, never reported as new-establishment area. The registry records this family as parked from discovery pending a scope decision on whether protection is a restoration family or a separate avoided-deforestation stream [src: schema/registers/FAM_family_registry.csv §forest_protection].

### Cross-family tag (`forest_restoration__cross_family`)

A tagging value for pooled restoration results that do not isolate planting, regeneration or protection; `qualitative_only` in the registry but exempt from the rule that parks qualitative-only families out of the effect tables [src: schema/registers/FAM_family_registry.csv §cross_cutting_envelope_fr].

## What governs where it fits

**Biophysical.** For regeneration families the leading factors are propagule supply and residual cover; for planting families the climate, soil and slope envelope of the chosen target. Climate is a coarse gate rather than the defining variable for regeneration [src: methodology/families/forest_restoration.md §F1 — Passive natural regeneration].

**System.** Observed land cover gates each family: degraded or former forest for regeneration, prior land cover for the reforestation versus afforestation flag, existing standing forest for protection. Recent loss may now be productive agriculture, settlement or plantation, so loss is never silently treated as land available for restoration [src: methodology/audits/t4_followup_20261106/anr_proximity_decision.md §Proposed spatial interpretation for the final recipe].

**Operational.** Only hard exclusions (legal protected areas, water bodies, urban footprints) act as masks. Governance, tenure, access, labour and finance are soft, investment-addressable factors and enter the operational-risk filter as scenario levers [src: AGENTS.md §What is locked]. Implementation technique matters to outcomes: technique-to-survival evidence ([[var:establishment_survival]]) is captured as operational-risk evidence that feeds implementation guidance, not as a suitability or scorecard cell [src: methodology/effect_evidence_followups.md §1f. Forest restoration — effect round 1 (2026-10-06)]. See [[ch:m2b-project-risk]] and [[ch:m6-handoff]].

## Effects and hazards

Effect rows are generated by cell synthesis with an applicability envelope, a transfer class and a two-axis confidence (evidence, agreement) [src: AGENTS.md §What is locked]. At the pin the hazard rows cover drought, flood, extreme rainfall, heat stress, waterlogging, wind and cyclone, fire and landslide, with rows for every family and the cross-family tag [src: schema/recipes/forest_restoration/T3_nbs_hazard_farming.csv]. Landslide, like extreme rainfall and sedimentation, is an asset-threat-only hazard: it describes risk to the investment and has no livelihood cell [src: AGENTS.md §What is locked]. Scorecard rows address water stress, catchment water yield, water quality, soil erosion, biodiversity, carbon, production gap, rural poverty, food insecurity and the hazard priorities [src: schema/recipes/forest_restoration/T6_nbs_scorecard.csv].

**Effect locus.** Forest restoration is `off_site`: it does not occur on farmland, so farmers feel it downstream and at landscape scale (water, flood, microclimate, access to forest products) or as a wider societal benefit, never as an on-plot effect. T3 rows are stamped landscape-scale only. Plantation forestry is the exception, recorded as `mixed`, because timber or payment income accrues to the grower on the plot while hydrological and erosion effects land off-site [src: schema/lookups/effect_locus.csv].

{{csv:schema/lookups/effect_locus.csv|where=nbs_id=forest_restoration|cols=nbs_id,suitability_family_id,effect_locus}}

**Comparator caveats.** Studies of what existing forest does, or what its loss costs, are evidence for keeping forest standing, not for what planting or regeneration achieves within a project horizon. They are tagged `existing_forest` (extraction ruleset v1.6.4) and kept in the protection family row, out of the roll-up and every other family. A restored stand falling short of an intact reference forest is a recovery note, not harm, and never sets a class [src: schema/lookups/comparator_policy.csv].

{{csv:schema/lookups/comparator_policy.csv|where=nbs_id=forest_restoration|cols=nbs_id,comparator,rollup_included,home_family}}

**Trade-offs.** The principal recorded trade-off is water: measured catchment evidence on planting points to reduced water yield, which is why the water-stress reading for planting families is not taken from a single scenario model [src: methodology/effect_evidence_followups.md §1f. Forest restoration — effect round 1 (2026-10-06)]. Drought threatens establishment itself: seedling mortality evidence makes drought a high asset threat, and fire is named in the literature as a main cause of failure [src: methodology/effect_evidence_followups.md §1f. Forest restoration — effect round 1 (2026-10-06)]. Afforestation of non-forest ecosystems carries the do-no-harm flag above. Flood effects at large-basin scale are weaker than early evidence suggested once measured nulls entered the pool [src: methodology/effect_evidence_followups.md §1f. Forest restoration — effect round 1 (2026-10-06)].

## Scheme status and open questions

The family scheme, including the plantation split, is recorded as signed off, with further domain review welcome but non-blocking [src: methodology/families/forest_restoration.md §Current routing (reconciled 2026-10-28)]. Settled: the continuum split; species as a parameter of active planting; mangroves as their own practice; plantations out of the roll-up.

Open or pending:

- **Protection and community forest management.** Parked from discovery pending the scope call on restoration family versus avoided-deforestation stream [src: schema/registers/FAM_family_registry.csv §forest_protection]. The family nonetheless holds effect rows, because existing-forest comparator studies are routed to it [src: schema/lookups/comparator_policy.csv].
- **Farmland versus forest-land boundary** for degraded fallow is recorded as a design question [src: methodology/families/forest_restoration.md §6. Original questions retained for design history].
- **Plantation units** with mixed or unclear planting type remain in active planting pending resolution.

**No family has a compiled suitability mapping at the pin** [src: schema/recipes/forest_restoration/T4_suitability_mappings.csv]. This is "not yet evidenced and calibrated", not "parked by decision": the remnant-proximity evidence for assisted regeneration is held qualitative by review, with no score approved [src: methodology/audits/t4_followup_20261106/anr_proximity_decision.md §Application and verification]. The recipe README still lists a `mangrove_coastal` family and the existing-forest comparator rationale still mentions it; both predate the mangrove promotion, and the registry, which has no such family here, is authoritative [src: schema/recipes/forest_restoration/README.md].

## Assumptions and limits

- Families are a scoping-grade, first-pass grouping; revisions are recorded in the scheme [src: methodology/families/forest_restoration.md §5. How this maps to the schema].
- Without compiled T4 mappings the method cannot yet produce a forest-restoration suitability surface; the families describe the intended product only.
- Forest-loss and disturbance products do not establish seedling abundance, species composition or land availability; unknown regeneration stays an explicit verification need.
- Off-site effects are not attributable to individual farms; the scorecard reports landscape-scale effects.
- Effect evidence for some cells is dominated by practitioner ratings or by temperate harvest-renewal studies, which carry transfer labels.
- Feasibility must still confirm the ecological baseline, land claims, species choice, protection from fire and grazing, and maintenance.

## Where this is configured

- Families: [[table:FAM]]; practice definition: [[table:T0]].
- Suitability mappings (none compiled at the pin): [[table:T4]]; dataset bindings: [[table:BIND]], [[table:T1]].
- Hazard responses: [[table:T3]]; scorecard: [[table:T6]]; economic profiles: [[table:T6E]].
- Evidence: [[table:EV]], [[table:SRC]]; variables: [[table:VONT]].
- Lookups: `schema/lookups/effect_locus.csv`, `comparator_policy.csv`, `family_rollup_policy.csv`.
