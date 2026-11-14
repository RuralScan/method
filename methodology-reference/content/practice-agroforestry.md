---
title: Agroforestry
slug: practice-agroforestry
summary: Understand how the method divides agroforestry into suitability families, what each family can report spatially, which host systems gate it, and what the effect evidence covers and cannot claim.
sources:
  - methodology/families/agroforestry.md
  - schema/registers/FAM_family_registry.csv
  - schema/recipes/agroforestry/T0_nbs_registry.csv
  - schema/recipes/agroforestry/README.md
  - schema/recipes/agroforestry/T4_suitability_mappings.csv
  - schema/recipes/agroforestry/T4_run_policy.csv
  - methodology/recipes/agroforestry.md
  - methodology/T4_generation_method.md
  - schema/lookups/effect_locus.csv
  - schema/lookups/comparator_policy.csv
  - schema/lookups/crop_scope_policy.csv
  - methodology/effect_evidence_followups.md
  - AGENTS.md
  - method:cookbook/agroforestry.md
---
## Definition and boundary

Agroforestry, in this method, is the deliberate integration of woody perennials (trees, shrubs, palms, bamboos) with crops and/or livestock on the same land unit, managed so that the components interact [src: schema/recipes/agroforestry/T0_nbs_registry.csv §description_technical]. The defining feature is that the trees sit on **farmland** and the farm household manages them. That places the effect of the practice on the adopting farm (see "Effects and hazards").

Three neighbours must not be confused with it:

- **Forest restoration.** Regeneration or planting on degraded forest or non-farm land belongs to [[practice:forest_restoration]]. The boundary is the land system: regeneration on farmland is agroforestry, regeneration on forest land is forest restoration [src: methodology/families/forest_restoration.md §4. Edge cases the scheme deliberately resolves].
- **Riparian buffers.** Streamside planting is gated by the watercourse network, a different spatial logic, so it is its own practice, [[practice:riparian_buffer]], with a `zonal_linear` product [src: methodology/families/agroforestry.md §Parked / out of scope]. Agroforestry linear plantings (windbreaks, contour buffers) are gated by wind exposure and slope-flow on fields, not by streams [src: methodology/families/riparian_buffer.md §4. Edge cases the scheme resolves].
- **Water harvesting.** Contour structures whose purpose is to hold water belong to [[practice:water_harvesting_conservation]]; a vegetated contour line whose dominant limiter is the placement geometry of a tree or shrub line belongs here.

The practice definition record (T0) lists aliases inherited from an earlier catalogue, including "Riparian buffers" and "Forest farming", and its technical description groups parkland under silvopastoral systems [src: schema/recipes/agroforestry/T0_nbs_registry.csv §aliases]. The family registry is authoritative and differs on both points: riparian buffers are a separate practice and parkland retention is a regeneration practice. Read T0 aliases as search vocabulary, not as a classification.

## Suitability families

A suitability family is a set of sub-practices that share the dominant limiting factor deciding where they can go, because that factor fixes the leading variable and the whole variable set [src: methodology/T4_generation_method.md §2.1 Practice definition → subpractices → suitability families]. Agroforestry is grouped by limiting factor, not by appearance or tree species. The canonical case is scattered trees on cropland: when planted they are limited by the arable envelope and management; when retained through regeneration they are limited by rootstock, seedbank, seed-source proximity and tenure. Same picture, different family [src: methodology/families/agroforestry.md §1. The grouping principle].

The registry rows for this practice:

{{csv:schema/registers/FAM_family_registry.csv|where=nbs_id=agroforestry|cols=subpractice_id,name,suitability_family_id,spatial_product_type,dominant_limiting_factor}}

{{attribution:primitives}}

### Planted silvoarable (`agroforestry__planted_silvoarable`)

Sub-practices: alley cropping, tree intercropping and planted boundaries or live fences on cropland. The shared limiting factor is the arable biophysical envelope (slope, rainfall, temperature, soil reaction, depth and organic carbon) plus management and machinery access on cultivable land [src: schema/registers/FAM_family_registry.csv §alley_cropping]. The product is `area_suitability`: a suitable pixel approximates plantable land [src: methodology/families/agroforestry.md §F1 — Planted silvoarable]. A planted boundary is kept here, not with linear plantings, because establishment by planting on cropland places it in the arable envelope; the linear family is limited by placement geometry instead [src: schema/registers/FAM_family_registry.csv §planted_boundary_cropland].

Host gate: cultivated land from a land-cover product; grassland qualifies only where ungrazed forage is confirmed [src: schema/recipes/agroforestry/README.md §Reviewed T4 — 20 October 2026]. Apart from the cross-family tag's rows, this family carries the practice's only numeric biophysical mappings, and it carries the only run policy (see "What governs where it fits").

### Regeneration-based on farmland (`agroforestry__regeneration_farmland`)

Sub-practices: farmer-managed natural regeneration (FMNR), parkland tree retention and assisted natural regeneration on farmland. The limiting factor is regeneration potential: living stumps and roots, seedbank, seed-source proximity, and tenure security that lets a farmer protect regrowth [src: schema/registers/FAM_family_registry.csv §fmnr]. It cannot be an override of the planted family because it needs a different variable set (woody-cover baseline and change, distance to seed source, tenure proxies), and overrides only re-parameterise existing variables [src: methodology/families/agroforestry.md §F2 — Regeneration-based on farmland]. Product: `area_suitability`, meaning where regeneration can be induced.

The parkland edge case is resolved by establishment driver: a planted Faidherbia parkland is planted silvoarable; a retained or FMNR parkland is regeneration-based [src: methodology/families/agroforestry.md §4. Edge cases the scheme deliberately resolves]. Host gate: cropland, with grass, shrub or bare classes admitted only where agricultural, fallow or former-farmland identity is established, not mere depletion [src: schema/recipes/agroforestry/README.md §Reviewed T4 — 20 October 2026].

Tenure enters this family's limiting factor in the registry, but tenure security is a soft enabling-environment variable. Under the locked routing it is an operational-risk input, not a structural suitability layer (see below) [src: AGENTS.md §What is locked].

### Silvopastoral (`agroforestry__silvopastoral`)

Sub-practices: planted silvopasture and agrosilvopasture. The limiting factor is the biophysical envelope plus grazing context and forage or livestock variables, which the planted family does not carry; hence a separate family [src: schema/registers/FAM_family_registry.csv §planted_silvopasture]. Product: `area_suitability`. Host gate: cultivated or natural and semi-natural grassland from a grassland product, plus local confirmation of grazing [src: schema/recipes/agroforestry/README.md §Reviewed T4 — 20 October 2026]. No global substitute for local grazing confirmation has been approved [src: schema/recipes/agroforestry/README.md §Dataset bindings and execution limits].

### Linear and boundary plantings (`agroforestry__linear_boundary`)

Sub-practices: windbreaks and shelterbelts, contour and vegetative buffers. The limiting factor is linear-feature geometry: wind exposure for windbreaks, slope and flow lines for contour buffers, together with where field boundaries exist [src: schema/registers/FAM_family_registry.csv §windbreaks_shelterbelts]. Product: `applicability_zone`. The intervention is a line within a candidate area, so the family reports candidate length or density (for example erodible field-boundary km per km²), never suitable pixel area. The over-estimate from reporting area grows with pixel size: a 5 km cell flagged for windbreaks implies 25 km² where the real extent is a few line-km [src: methodology/T4_generation_method.md §2.4 Spatial product type & the resolution trap]. Host gate: cropland or grassland plus a field-boundary zone, with a regional width and no universal buffer [src: schema/recipes/agroforestry/README.md §Reviewed T4 — 20 October 2026].

### Shaded perennial-crop systems (`agroforestry__shaded_perennial`)

One sub-practice: shade trees over an existing perennial cash crop. The understorey crop (coffee, cocoa, tea, cardamom, pepper and others) is a **parameter** of the family, not a sub-family [src: schema/registers/FAM_family_registry.csv §shaded_perennial_crop]. The family is run per candidate crop and combined by maximum across crops while retaining which crop drives each pixel; crops are never blended into one envelope, because coffee highlands and cocoa lowlands are nearly disjoint and an average is suitable for neither [src: methodology/families/agroforestry.md §F5 — Shaded perennial-crop systems].

This is the family where the rule "constrain by observed distribution, not a modelled niche" is clearest. Because the intervention shades a crop that already exists, the applicability mask is the crop's observed distribution or production (MapSPAM, GAEZ harvested area, EO commodity maps, national statistics), graded by fractional area where possible. Observed distribution already integrates the climate, soil, market and tenure reasons the crop sits where it does. Bioclimatic envelope modelling is the fallback only where distribution data are absent, and is flagged as potential rather than realised extent [src: methodology/T4_generation_method.md §2.5 Constrain by observed distribution, not a modelled niche, where data exist]. The adaptation benefit of shade is reframed as prioritising the climate-stressed edge within the distribution, not extending beyond it [src: methodology/families/agroforestry.md §F5 — Shaded perennial-crop systems].

In the reviewed T4 the host gate is an OR across coffee, cocoa and tea host fractions, retaining crop identity and fractions; MapSPAM 2020 physical crop area is the global default and better observed commodity maps may override it. Model probabilities are not area fractions. Including tea is recorded as a design decision: coffee and cocoa evidence does not establish a tea-specific response [src: schema/recipes/agroforestry/README.md §Reviewed T4 — 20 October 2026]. Product: `area_suitability`, bounded by the resolution of the crop layer.

### Homegardens (`agroforestry__homegardens_proximity`): qualitative only

Multistrata homegardens are sub-pixel and driven by settlement and water proximity, so a raster surface would mislead. The family is `qualitative_only` and is handled through the scorecard and the hand-off note rather than mapped [src: schema/registers/FAM_family_registry.csv §homegardens]. A `qualitative_only` family is parked out of the generated effect tables; its evidence stays in the register for implementation guidance [src: AGENTS.md §What is locked].

### Cross-family envelope (`agroforestry__cross_family`)

This is a tagging value, not a sub-practice. It lets general envelope evidence that applies across all agroforestry families be registered without being forced onto the planted family. The registry records it as `qualitative_only` and marks the meta-tag as pending ratification [src: schema/registers/FAM_family_registry.csv §cross_cutting_envelope]. Shared evidence does not automatically apply across families [src: schema/recipes/agroforestry/README.md §Reviewed T4 — 20 October 2026].

## What governs where it fits

The three suitability dimensions apply in order of what does the limiting: `biophysical_constraint` (can a tree establish at all: climate, terrain, soil), `system_constraint` (the existing land use or farming system the trees must integrate with) and `operational_constraint` (implementation feasibility) [src: AGENTS.md §What is locked].

**Biophysical.** Only planted silvoarable and the cross-family tag carry numeric biophysical rows at the pin [src: schema/recipes/agroforestry/T4_suitability_mappings.csv]. They retain reviewed source bands for slope, soil reaction, soil organic carbon, rainfall and temperature, plus a favourable-rainfall row for the shaded family; ranks become explicit design scores on the full source scale, unknown gaps and tails are preserved, and each evaluation requires an explicit profile identifier [src: schema/recipes/agroforestry/README.md §Reviewed T4 — 20 October 2026]. The retained hard slope rule excludes planted-silvoarable slopes above 19.3 degrees (a source value of 35% slope); the README states this is one regional source's model rule, not a globally validated optimum [src: schema/recipes/agroforestry/README.md §Reviewed T4 — 20 October 2026]. The older recipe skeleton proposes a different exclusion of slopes above 35° and a soil-depth floor; it is an unauthored skeleton and is not the compiled rule [src: methodology/recipes/agroforestry.md §7.3 Structural exclusion masks].

The single run policy at the pin builds a partial terrain-and-soil index for planted silvoarable:

{{csv:schema/recipes/agroforestry/T4_run_policy.csv|cols=system,output_label,variable_group,rule_id,group_weight,criterion_weight,aggregation,sensitivity_aggregation,missing_values,gate_policy,applicability}}

It combines criteria by weighted linear combination, reports a minimum aggregation as sensitivity, propagates unknown values rather than filling them, applies host and legal masks separately, and requires a transfer check before use outside the source context [src: schema/recipes/agroforestry/T4_run_policy.csv]. Current default weights are equal and are not claimed to be evidence-derived importance [src: schema/recipes/agroforestry/README.md §Source-review resolution and variable importance (20 October)].

**System.** Each mapped family is gated by its observed host system: cultivated land, farmland identity, grazing land, field boundaries or a specific perennial crop (see the family sections). This is the observed-distribution rule applied to the human system [src: methodology/T4_generation_method.md §2.5 Constrain by observed distribution, not a modelled niche, where data exist].

**Operational.** Only hard exclusions (legal protected areas, water bodies, urban footprints) are suitability masks. Soft, investment-addressable factors such as [[var:distance_to_road]], market access, [[var:tenure_security]], extension, finance and labour are routed to the project-risk operational filter and implementation guidance, not to structural suitability [src: AGENTS.md §What is locked]. The agroforestry table still holds soft operational rows flagged `operational_constraint`; they are catalogued for traceability but kept out of the structural suitability surface [src: schema/recipes/agroforestry/README.md §Dataset bindings and execution limits]. The retained protected-area row is scoped to planted silvoarable and needs explicit legal-category mask handling before any opportunity-space output can be called complete [src: schema/recipes/agroforestry/README.md §Dataset bindings and execution limits]. See [[ch:m1-suitability]] and [[ch:m2b-project-risk]].

**Resolution.** Slope is a derivative of elevation and flattens as the grid coarsens, biasing suitability optimistic; derivatives are computed at native resolution and then aggregated, never resampled and then derived [src: methodology/T4_generation_method.md §Per-variable resolution validity (a *second*, independent coarseness limit)].

## Effects and hazards

Effect rows for agroforestry are generated by cell synthesis over pooled evidence, not extracted row by row: T3 cells are practice × hazard × farming system, T6 cells are practice × scorecard priority, and each row carries an applicability envelope, a transfer class and a two-axis confidence [src: AGENTS.md §What is locked]. At the pin the hazard rows cover drought, flood, extreme rainfall, heat stress, waterlogging, wind and cyclone, and fire, with family-scope rows for every mapped family and the cross-family tag [src: schema/recipes/agroforestry/T3_nbs_hazard_farming.csv]. The scorecard rows address production gap, rural poverty, food insecurity, gender inequity, water stress, catchment water yield, water quality, soil erosion, biodiversity, carbon and the hazard priorities [src: schema/recipes/agroforestry/T6_nbs_scorecard.csv]. See [[ch:effect-synthesis]] and [[ch:m5-scorecard]].

**Effect locus.** Agroforestry is `on_farm` at practice level: the measured livelihood effect lands on the household that adopts [src: schema/lookups/effect_locus.csv].

{{csv:schema/lookups/effect_locus.csv|where=nbs_id=agroforestry|cols=nbs_id,suitability_family_id,effect_locus}}

**Crop-specific evidence.** Crop-level yield evidence counts as practice evidence only in the shaded perennial family, because that family is defined by its understorey crop; elsewhere crop- and species-specific claims are retained but routed out of the practice-level surface [src: schema/lookups/crop_scope_policy.csv].

**Comparator caveat.** Silvopasture measured against ungrazed native forest is a conservation benchmark, not an intervention counterfactual, and never sets a class [src: schema/lookups/comparator_policy.csv].

{{csv:schema/lookups/comparator_policy.csv|where=nbs_id=agroforestry|cols=nbs_id,comparator,rollup_included,home_family}}

**Trade-offs and hazard limits.** The drought evidence is the main caution. Once component routes admitted only units that state the hazard, the practice-level drought reading fell sharply, because much of the earlier strength rested on infiltration gains measured outside drought years [src: methodology/effect_evidence_followups.md §1f]. Drought-year evidence includes findings that full-sun cocoa was more resilient than shaded cocoa in a West African drought and that diverse shade gave no benefit, alongside positive alley-cropping results [src: methodology/effect_evidence_followups.md §1g]. Shade, competition for water and the graded hazard-intensity discount therefore matter: a gain in an ordinary year does not make a practice a drought defence [src: AGENTS.md §What is locked]. Every livelihood and priority row lists measured harm units so that a minority of harm findings is visible [src: AGENTS.md §What is locked].

## Scheme status and open questions

The family scheme document is a draft for domain sign-off; its open questions (the planted versus regeneration split, crops and distribution datasets for the shaded family, whether silvopasture is in scope for applications, homegardens as qualitative only, family naming) are recorded as unanswered in the source [src: methodology/families/agroforestry.md §6. Open questions for sign-off]. The registry has implemented the scheme as written. The cross-family tag is pending ratification [src: schema/registers/FAM_family_registry.csv §cross_cutting_envelope].

The scheme note says only the planted family has T4 rows. That is out of date at the pin: every mapped family now has a categorical host gate, and only the planted family (with the cross-family tag) has numeric biophysical rows [src: schema/recipes/agroforestry/T4_suitability_mappings.csv]. Homegardens has no T4 mapping **by decision** (qualitative only), not for lack of evidence [src: schema/recipes/agroforestry/README.md §Reviewed T4 — 20 October 2026]. Several candidate mappings are parked pending source or class clarification, and the support denominator (screened-source membership) is unknown, so no prevalence percentage is reported [src: schema/recipes/agroforestry/README.md §Reviewed T4 — 20 October 2026]. The methodology recipe for agroforestry remains a skeleton [src: methodology/recipes/agroforestry.md §1. Context and Scope].

## Assumptions and limits

- The scheme is a scoping-grade grouping, a first-pass hypothesis revisable once evidence is in; it is not a feasibility taxonomy [src: methodology/families/agroforestry.md §5. How this maps to the schema].
- Numeric bands come from regional sources and require a target-transfer check; they are not global optima. Held or parked calibration is not a score.
- Host gates depend on land-cover and crop-area products whose resolution bounds what can be claimed; a coarse crop layer constrains coarsely. Missing codes and masks remain unknown; whole pixels are never counted as crop footprint or linear planting area [src: schema/recipes/agroforestry/README.md §Dataset bindings and execution limits].
- Boundary geometry, regional placement width, grazing confirmation and farmland identity are explicit inputs an application must supply.
- The categorical and host evaluators operate on caller-supplied aligned arrays; they are not a complete raster acquisition or suitability runner [src: schema/recipes/agroforestry/README.md §Dataset bindings and execution limits].
- Effect classes for drought rest on thin drought-year evidence. Feasibility must still test species, management, tenure, market and labour on site.

## Where this is configured

- Families and grouping rationale: [[table:FAM]].
- Practice definition, economic archetype and indicative costs: [[table:T0]].
- Suitability mappings: [[table:T4]]; run policy: [[table:T4_RUN]]; numeric policy: [[table:T4_NUMERIC_POLICY]].
- Dataset resolution by context (for example MapSPAM default, national commodity override): [[table:BIND]] and [[table:T1]].
- Hazard responses: [[table:T3]]; scorecard: [[table:T6]]; economic profiles: [[table:T6E]].
- Evidence and sources: [[table:EV]], [[table:SRC]]; variables: [[table:VONT]].
- Lookups: `schema/lookups/effect_locus.csv`, `comparator_policy.csv`, `crop_scope_policy.csv`.
