---
title: Water harvesting and conservation
slug: practice-water_harvesting_conservation
summary: Understand how the method divides water harvesting by where the water comes from and how it is held, what each family can report spatially, why every suitability mapping is on hold, and how drought evidence is read.
sources:
  - methodology/families/water_harvesting.md
  - methodology/audits/wh_scope_review_20261104/README.md
  - schema/registers/FAM_family_registry.csv
  - schema/recipes/water_harvesting_conservation/T0_nbs_registry.csv
  - schema/recipes/water_harvesting_conservation/README.md
  - schema/recipes/water_harvesting_conservation/T4_suitability_mappings.csv
  - schema/recipes/water_harvesting_conservation/T3_nbs_hazard_farming.csv
  - schema/recipes/water_harvesting_conservation/T6_nbs_scorecard.csv
  - methodology/recipes/water_harvesting.md
  - methodology/T4_generation_method.md
  - methodology/effect_evidence_followups.md
  - schema/lookups/effect_locus.csv
  - schema/lookups/crop_scope_policy.csv
  - AGENTS.md
  - method:cookbook/water_harvesting_conservation.md
---
## Definition and boundary

Water harvesting and conservation, in this method, covers interventions that intercept, retain and store precipitation and surface runoff for productive use or groundwater recharge [src: schema/recipes/water_harvesting_conservation/T0_nbs_registry.csv §description_technical]. It spans land-based measures (contour bunds, pits, terraces, micro-catchments) and structures (ponds, check dams, tanks, sand and subsurface dams). The practice identifier is `water_harvesting_conservation`; it is planned at watershed scale and has a `quick_returns` economic archetype [src: schema/recipes/water_harvesting_conservation/T0_nbs_registry.csv].

The originating recipe frames three convergent suitability questions: where is enough runoff generated to make harvesting hydrologically meaningful; where can it be captured, stored or infiltrated given terrain, soil and land cover; and where is it strategically desirable given demand, access, climate risk and socio-economic context [src: methodology/recipes/water_harvesting.md §1. Context and Scope]. Only the first two are suitability questions in the current method; the third is need, priority or operational risk (see below).

Boundaries:

- **Not irrigation.** Water harvesting stores and redistributes local rainfall; it fails under late-onset or extreme drought, and is not a drought defence merely because it raised yields in a dry year [src: AGENTS.md §What is locked].
- **Not wetland creation.** The method separates water harvesting from wetland creation because the biophysical logic differs; this is the canonical example of the rule not to cluster practices by appearance [src: AGENTS.md §Don't]. See [[practice:wetland_management]].
- **Not every engineered structure is a nature-based solution.** The registry establishes water-harvesting functions; it does not certify that every engineered implementation restores or manages an ecosystem. Conditional practices need their soil, vegetation or ecosystem management specified [src: methodology/audits/wh_scope_review_20261104/README.md §Decision requested].

## Suitability families

Families are grouped by which water-balance question their dominant limiting factor answers, the same logic the recipe uses to switch membership functions between sub-practices (for example, runoff membership increases for structures that store runoff and decreases for in-field conservation) [src: methodology/families/water_harvesting.md §1. The grouping principle].

{{attribution:primitives}}

The registry rows for this practice:

{{csv:schema/registers/FAM_family_registry.csv|where=nbs_id=water_harvesting_conservation|cols=subpractice_id,name,suitability_family_id,spatial_product_type,dominant_limiting_factor}}

### In-situ moisture conservation (`water_harvesting__in_situ`)

Sub-practices in the registry: contour bunds and ridges, planting pits and zaï, conservation tillage and mulching. Rain is captured where it falls, with no external catchment or storage [src: schema/registers/FAM_family_registry.csv §contour_bunds_ridges]. The limiting factor is the on-field water balance: rainfall deficit, soil infiltration and water-holding capacity, soil depth and gentle slope, placed on inter-stream slopes [src: methodology/families/water_harvesting.md §F1 — In-situ moisture conservation]. Product: `area_suitability`. The family note lists further variants (tied ridging, Negarim micro-basins) that have no separate registry row.

### Micro-catchment harvesting (`water_harvesting__micro_catchment`)

Sub-practices: semi-circular bunds, eyebrow terraces and runoff strips. A small bare catchment feeds an adjacent cropped basin; the limiting factor is the short-slope runoff-to-cropped-area ratio plus slope and soil [src: schema/registers/FAM_family_registry.csv §semicircular_bunds]. Product: `area_suitability`. The split from in-situ conservation turns on whether a distinct runoff-donor area exists. An eyebrow terrace belongs here, not with bench terraces, because it is runoff-ratio driven rather than slope-reshaping [src: methodology/families/water_harvesting.md §4. Edge cases the scheme resolves].

### Runoff catchment and storage (`water_harvesting__runoff_catchment`)

Sub-practices: macro-catchment harvesting (an umbrella record), farm ponds, check dams, percolation tanks, sand dams, subsurface dams and small communal tanks [src: schema/registers/FAM_family_registry.csv §farm_ponds]. Runoff is collected from a catchment larger than the storage or benefiting area. The limiting factor is runoff generation plus drainage-line geomorphology: stream order, drainage density, proximity to channels, and soil clay for storage [src: methodology/families/water_harvesting.md §F3 — Ex-situ / macro-catchment storage]. Sand and subsurface dams add specific channel settings (seasonal sandy riverbeds with a bedrock sill; alluvial valley bottoms) [src: schema/registers/FAM_family_registry.csv §sand_dams].

Product: `applicability_zone`. Structures are sited on or near drainage lines, so the family reports candidate siting density, never suitable pixel area [src: methodology/families/water_harvesting.md §F3 — Ex-situ / macro-catchment storage]. An applicability zone is not a measured count of constructible sites; site density requires separate site-selection evidence [src: methodology/audits/wh_scope_review_20261104/README.md §Implementation handoff after sign-off].

A reviewed scope proposal argues that this family conflates opposite requirements. Surface storage (ponds, check dams) wants fine, low-permeability soils; intentional recharge (percolation tanks) wants permeable substrate; alluvial storage (sand and subsurface dams) is a third mechanism; and check dams must be classified by purpose before routing. A single family-wide soil response is therefore not justified [src: methodology/audits/wh_scope_review_20261104/README.md §Why these boundaries matter]. These are proposed analytical distinctions approved for domain review, not ratified family identifiers [src: methodology/audits/wh_scope_review_20261104/README.md §Decision requested].

### Terracing and slope conservation (`water_harvesting__terracing`)

Sub-practices: bench terraces, and stone bunds or fanya juu. The slope is reshaped to intercept and hold runoff; slope is the defining variable, plus soil depth for construction and, for stone structures, stone availability [src: schema/registers/FAM_family_registry.csv §bench_terraces]. Product: `area_suitability`. The scope review proposes splitting the combined stone-bund and fanya-juu label for domain review [src: methodology/audits/wh_scope_review_20261104/README.md §Why these boundaries matter].

### Spate and floodwater harvesting (`water_harvesting__spate`): linear, parked

Diversion and spreading of ephemeral flood flows (spate irrigation, jessour, water spreading), gated by ephemeral channel or wadi presence and sediment load [src: schema/registers/FAM_family_registry.csv §spate_floodwater]. Product: `zonal_linear`, reported as length or reach coverage along the channel. The registry records it as parked: the evidence is thin and whether it stays a family or folds into runoff storage is a scope question. The scope review keeps it distinct pending domain review rather than silently merging it [src: methodology/audits/wh_scope_review_20261104/README.md §Why these boundaries matter].

### Rooftop harvesting (`water_harvesting__rooftop`): qualitative only, out of scope

Cisterns and reservoirs capturing roof runoff, gated by settlement and building presence at sub-pixel scale. Product: `qualitative_only` [src: schema/registers/FAM_family_registry.csv §rooftop_harvesting]. Rooftop and household cisterns are not a landscape NbS, so the family is parked out of the generated effect tables while its evidence stays in the register [src: AGENTS.md §What is locked]. The scope review records rooftop harvesting as already out of project scope and needing consistent exclusion wording, not another vote [src: methodology/audits/wh_scope_review_20261104/README.md §Decision requested].

### Cross-family tag (`water_harvesting__cross_family`)

A tagging value for pooled soil-and-water-conservation results from syntheses and programme evaluations that do not isolate one practice; `qualitative_only`, and pooled with family rows in the practice roll-up [src: schema/registers/FAM_family_registry.csv §cross_cutting_envelope_wh].

## What governs where it fits

**Biophysical.** The inherited recipe names six variable groups: topographic and morphometric (slope, elevation, curvature, topographic wetness index), hydrological (runoff, drainage density, stream order, flow accumulation, distance to streams), soil and lithology (texture, hydrologic soil group, depth, permeability, lineaments), climatic (rainfall, intensity, PET, aridity), land cover, and socio-economic and risk [src: methodology/recipes/water_harvesting.md §2.1 Variable categories]. It recommends one surface per family, combined by maximum or kept as parallel layers [src: methodology/recipes/water_harvesting.md §7.2 Subpractice-specific suitability surfaces].

```formula
TWI = ln(a / tan β)
```

where `a` is the upslope contributing area per unit contour length and `β` is the slope angle in radians; high values mark water-accumulation zones [src: methodology/recipes/water_harvesting.md §2.1 Variable categories].

**Every T4 mapping at the pin is held.** Each row is either on numerical calibration hold or waiting for a spatial input that measures the same quantity as the source [src: schema/recipes/water_harvesting_conservation/T4_suitability_mappings.csv]. The README states that the rows supply zero executable suitability functions [src: schema/recipes/water_harvesting_conservation/README.md §Suitability]. The holds are substantive:

- Rainfall: one in-field source requires annual rainfall at 80% probability of exceedance, which a mean-annual layer does not measure; a pooled runoff-catchment maximum conflicted with a stated optimum, so four source profiles are retained rather than one score [src: schema/recipes/water_harvesting_conservation/T4_suitability_mappings.csv].
- [[var:slope]]: profiles differ by structure and purpose and are reported in different units (percent versus degrees), so no shared cutoff is approved [src: methodology/audits/wh_scope_review_20261104/README.md §Human QA order].
- [[var:drainage_density]]: increases suitability in some sources and decreases it in another; measurement and purpose are preserved, with no pooled vote [src: methodology/audits/wh_scope_review_20261104/README.md §Human QA order].
- [[var:runoff_potential_index]]: runoff depth, runoff coefficient and curve number share a broad ontology identifier but are different measurements, and decreasing curve-number scores cannot be pooled with increasing runoff-depth scores [src: methodology/audits/wh_scope_review_20261104/README.md §Human QA order].
- [[var:stream_order]] and [[var:soil_depth_to_bedrock]]: the available global layers use a different ordering convention or a proxy with no demonstrated equivalence to the source measures [src: schema/recipes/water_harvesting_conservation/T4_suitability_mappings.csv].

The illustrative bands in the inherited recipe (for example a decreasing slope sigmoid with inflection at 8%, ponds favouring 1–8% slope and terraces 5–25%, and a structural mask list) are historical worked values from the design phase. The family note's status notice says they must not be used as current approved global rules [src: methodology/families/water_harvesting.md].

**System.** Runoff-catchment structures need downstream or on-farm demand to be useful, but population, ecological priority and irrigation demand cannot become general establishment limits; they belong to priority and hand-off, not T4 [src: methodology/audits/wh_scope_review_20261104/README.md §Why these boundaries matter].

**Operational.** Road and town proximity and groundwater demand are preserved as deferred pointers for the project-risk, hotspot and hand-off modules [src: methodology/audits/wh_scope_review_20261104/README.md §Outstanding work, with a stop rule]. Land tenure, customary rights and governance are not core suitability variables [src: methodology/recipes/water_harvesting.md §7.5 Key assumptions].

## Effects and hazards

Effect rows are generated by cell synthesis with an applicability envelope, a transfer class and a two-axis confidence [src: AGENTS.md §What is locked]. Hazard rows at the pin cover drought, flood, heat stress, waterlogging, wind and cyclone, fire, and the asset-threat-only hazards extreme rainfall, sedimentation and landslide [src: schema/recipes/water_harvesting_conservation/T3_nbs_hazard_farming.csv]. Scorecard rows address production gap, rural poverty, food insecurity, water stress, catchment water yield, water quality, soil erosion, biodiversity, carbon and the hazard priorities [src: schema/recipes/water_harvesting_conservation/T6_nbs_scorecard.csv].

**Effect locus** varies by family: in-field, micro-catchment and terracing practices act on the adopter's own plots; runoff-catchment structures are `mixed`, because their water reaches users on and beyond the owning farm [src: schema/lookups/effect_locus.csv]. The lookup has no practice-level default and no row for the spate family.

{{csv:schema/lookups/effect_locus.csv|where=nbs_id=water_harvesting_conservation|cols=nbs_id,suitability_family_id,effect_locus}}

**Crop-specific evidence.** Water harvesting does not define a crop system, so the host crop's yield response (zaï sorghum, stone-bund millet) is the practice effect; crop-specific units re-enter all water-harvesting families' effect cells, while species-specific units never do [src: schema/lookups/crop_scope_policy.csv].

**Drought and the intensity discount.** The method reads drought cells conservatively. Component and proxy routes admit only units that state the hazard, so soil-moisture gains measured in normal years do not count as drought evidence [src: methodology/effect_evidence_followups.md §1f. Forest restoration — effect round 1 (2026-10-06)]. A graded hazard-intensity discount then scales a livelihood class by the weighted share of measured same-hazard evidence that found no benefit or a reversal, floored at `low`; failures tagged by the author as mild are exempt [src: AGENTS.md §What is locked]. The recorded water-harvesting drought evidence includes crop failures and reversals in severe years and penalties in wet years, which lower agreement [src: methodology/effect_evidence_followups.md §1g. Drought-year round 2 (2026-10-06, all three NbS)].

**Bundles and counterfactuals.** Conservation packages are often evaluated as bundles; a bundled intervention is credited by its stated component share, and a hazard-year claim with no normal-year reference is down-weighted [src: AGENTS.md §What is locked]. Recorded cases include a fertilised package compared against unfertilised conventional practice, and a pond whose benefit came through supplementary irrigation [src: methodology/effect_evidence_followups.md §1g. Drought-year round 2 (2026-10-06, all three NbS)]. Wet-year yield penalties are a recorded trade-off of moisture-retaining practices.

## Scheme status and open questions

The August family note is retained as historical rationale. Its statements that there are no T4 rows, that rooftop is a scope question, and its illustrative numeric bands are superseded as status and approval guidance; no structural regrouping has been applied [src: methodology/families/water_harvesting.md]. Settled: the in-situ, micro-catchment and terracing distinctions (retained where the actual water source and slope modification justify them); rooftop out of scope.

Pending domain review: grouping farm ponds and communal tanks as surface storage; percolation tanks as a separate recharge branch; sand and subsurface dams as alluvial storage; check dams classified by purpose; spate kept distinct [src: methodology/audits/wh_scope_review_20261104/README.md §Decision requested]. Gully plugs have no registry record and await a family and purpose decision [src: methodology/audits/wh_scope_review_20261104/README.md §Outstanding work, with a stop rule]. The practice has no dedicated hydrology domain reviewer, which the scheme records as an open gap [src: methodology/families/water_harvesting.md].

No family has an executable mapping. Rooftop has none **by decision**; spate is **parked**; in-situ, micro-catchment, runoff-catchment and terracing are **evidenced but held** for calibration or matching inputs.

## Assumptions and limits

- Scoping uses global layers at roughly 100 m to 1 km; sub-100 m siting is feasibility work [src: methodology/recipes/water_harvesting.md §7.5 Key assumptions].
- Curve-number runoff estimation is weak in tropical and karstic settings; climatology hides intra-annual and event-scale dynamics [src: methodology/recipes/water_harvesting.md §7.5 Key assumptions].
- Coarse elevation models under-represent first-order tributaries and bias drainage density downward [src: methodology/recipes/water_harvesting.md §7.6 Constraints and limitations].
- Area suitability for field systems is not proof that pits or bunds occupy every pixel [src: methodology/audits/wh_scope_review_20261104/README.md §Implementation handoff after sign-off].
- The method does not replace site hydrological modelling, geotechnical assessment or community consultation [src: methodology/recipes/water_harvesting.md §7.6 Constraints and limitations].

## Where this is configured

- Families: [[table:FAM]]; practice definition: [[table:T0]].
- Suitability mappings and their holds: [[table:T4]], [[table:T4_NUMERIC_POLICY]]; dataset bindings: [[table:BIND]], [[table:T1]].
- Hazard responses: [[table:T3]]; scorecard: [[table:T6]]; economic profiles: [[table:T6E]].
- Evidence: [[table:EV]], [[table:SRC]]; variables: [[table:VONT]].
- Lookups: `schema/lookups/effect_locus.csv`, `crop_scope_policy.csv`.
