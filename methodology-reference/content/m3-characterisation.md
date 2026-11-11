---
title: Module 3 - Characterising the opportunity space
slug: m3-characterisation
summary: Assemble, screen, reduce and standardise the opportunity-space variables (T5) inside the suitability mask, and read the descriptive panels and priority layers that Module 4 consumes.
sources:
  - methodology/modules/M3_characterisation.md
  - methodology/opportunity_space_T5.md
  - methodology/framework.md
  - methodology/modules/M1_suitability.md
  - methodology/modules/M2_climate_risk.md
  - methodology/modules/M4_hotspots.md
  - methodology/T4_generation_method.md
  - schema/T5_opportunity_space.csv
  - schema/spec.md
  - schema/registers/BIND_dataset_binding.csv
  - schema/registers/VONT_variable_ontology.csv
  - AGENTS.md
  - method:handbook/implement-a-scan.md
---

## Question this module answers

Module 1 (M1) establishes where a practice could establish: the opportunity space. Module 3 (M3) describes what lies inside that space. Its question is: within the area where this nature-based solution (NbS) could work, who lives there, what is produced, and which development problems (poverty, biodiversity loss, climate exposure, inequity) are most present? [src: methodology/modules/M3_characterisation.md §2]

M3 describes; it does not prioritise. It does not decide feasibility (M1), apply the user's priority weights (Module 4, [[ch:m4-hotspots]]), score the practice's response to the problems it finds (Module 5, [[ch:m5-scorecard]]) or assess risk to the investment (M2b, [[ch:m2b-project-risk]]). [src: methodology/modules/M3_characterisation.md §2]

The opportunity-space variables live in [[table:T5]]. The framework draws a three-way distinction that this module depends on: [[table:T4]] says where a practice *can* establish, T5 says where it *should* be invested given development priorities, and [[table:T6]] says what the practice *does* once placed. [src: methodology/opportunity_space_T5.md §What T5 is]

## Inputs

| Input | From | Role |
|---|---|---|
| Opportunity-space mask | M1 | M3 characterises only inside this mask (high and very-high suitability cells). |
| Opportunity-space variables | [[table:T5]] | Variable identity, theme, `mcda_role`, direction of concern, normalisation method, default weight. |
| Dataset access | [[table:T1]] via [[table:BIND]] | Hosting, native resolution, grain type and administrative level of each bound dataset. |
| Double-count flags | [[table:T2]] | Prevents a variable being active both here and in the M2 vulnerability composite. |
| Geographic context | [[table:T7]] | Administrative units, agro-ecological zones and the six farming-system classes for per-unit summaries. |

[src: methodology/modules/M3_characterisation.md §3] [src: methodology/modules/M1_suitability.md §4]

Datasets are resolved through the dataset binding resolver under "most specific context wins", not read raw from `T5.dataset_id`, so country or farming-system overrides are honoured. [src: methodology/modules/M3_characterisation.md §12] The farming-system breakdown keys to the six EO-derived T7 classes (`cropping_rainfed`, `cropping_irrigated`, `mixed_crop_livestock`, `agro_pastoral`, `pastoral_rangeland`, `tree_perennial`); the Dixon farming-systems vocabulary is a translation crosswalk only. [src: methodology/modules/M3_characterisation.md §12] [src: AGENTS.md §What is locked] See [[ch:farming-systems-and-data]].

## The T5 scheme

### Five themes

T5 rows are grouped into five themes, ordered by the question each answers. [src: methodology/opportunity_space_T5.md §The five-lens scheme (v0.3.0)]

| Theme | Question | Role |
|---|---|---|
| `climate_hazard` | Where is climate exposure highest? | Priority |
| `nbs_response` | Where would the practice do the most? | Priority |
| `people_production` | Where are the people and the productive systems under stress? | Priority |
| `equity_inclusion` | Whose disadvantage is being addressed? | Priority |
| `context` | What is the descriptive backdrop? | Descriptor only, never in the MCDA |

The equity theme was broadened from a gender-only theme to cover Indigenous Peoples and local communities (IPLC), marginalisation and gender, equality and social inclusion. Infrastructure was dropped as a top-level theme because it is either descriptive context (market access) or an operational lever handled by the M2b Stream B filter, not a pillar of the opportunity space. [src: methodology/opportunity_space_T5.md §The five-lens scheme (v0.3.0)]

### Priority versus descriptor

Every T5 row carries `mcda_role`. [src: methodology/opportunity_space_T5.md §mcda_role - priority vs descriptor]

- **`priority`** rows drive the Module 4 hotspot analysis, are reweightable by the user, and are the only rows to which T6 effect rows may attach.
- **`descriptor`** rows are carried for narrative, intersection and hand-off, but never enter the MCDA and are never standardised for it.

The distinction resolves a design tension: showing every relevant layer to the user without inflating the dimensionality of the weighted overlay. Descriptors answer "how many people live in this hotspot" or "how far is it from a market"; they do not make a pixel more or less of a priority. [src: methodology/opportunity_space_T5.md §mcda_role - priority vs descriptor] M3 assembles both and splits them at assembly time: priorities go to the standardised stack for Module 4, descriptors go only to the fingerprint. [src: methodology/modules/M3_characterisation.md §12]

### The rows at the pin

The pinned table is the authority for which rows exist:

{{csv:schema/T5_opportunity_space.csv|cols=variable_id,mcda_role,theme,dataset_id,directionality_of_concern,normalisation_method,weight_default,has_future_projection}}

It holds 19 rows: 15 priorities and 4 descriptors. [src: schema/T5_opportunity_space.csv] [src: AGENTS.md §What is locked] The prose companion lists fewer (it predates the later additions of `food_insecurity` and `catchment_water_yield`), and some module notes count 11 or 12 priorities; read those counts as stale. [src: methodology/opportunity_space_T5.md §The 17 ratified rows] [src: methodology/modules/M4_hotspots.md §13]

Three additions carry reasoning a reader needs:

- **`water_quality_risk`** (`nbs_response`) was added because effect evidence on nutrient removal and stream temperature had no T5 target; water quality is the core riparian and wetland service. No scoping-grade global layer exists, so it binds to an upload or a nutrient and sediment export proxy. [src: methodology/opportunity_space_T5.md §Priorities (13)]
- **`food_insecurity`** (`people_production`) was split from `rural_poverty` because rural income and food security are separate benefit streams, not proxies for each other. Its layer choice (IPC phase or FIES) is deferred and it requires upload. [src: methodology/opportunity_space_T5.md §Priorities (13)] [src: schema/T5_opportunity_space.csv]
- **`catchment_water_yield`** (`nbs_response`) was split from `water_stress`. Local infiltration, soil moisture and dry-season on-farm supply stay under water stress; what leaves the catchment for downstream users is scored here. Trees can improve the first while reducing the second, so the two must never be averaged into one class. [src: schema/T5_opportunity_space.csv]

Several rows are held. `biodiversity_priority` layer choice (Key Biodiversity Areas, IBAT, Biodiversity Intactness Index, refugia, distance to protected areas) is a deferred review; `flood_hazard` layer choice (FATHOM, JRC, WRI Aqueduct, basin routing) is open; subnational `gender_inequity` requires upload; broader marginalisation beyond IPLC has no global subnational layer at scoping grade. [src: methodology/opportunity_space_T5.md §Held out / requires_upload / deferred] [src: methodology/opportunity_space_T5.md §Seed issues for follow-up]

### Rows deliberately left out

The ratification records what did not make it and why, which is part of the method. A draft `tree_cover_gap` priority was superseded by more proximate signals (`carbon_sequestration_potential`, `biodiversity_priority`) and kept only as a candidate descriptor for tropical forest restoration. A draft `food_security_risk` was judged too distal at the time. `runoff_potential_index` is an internal calculation, not a T5 row. `groundwater_recharge_potential` is specific to water harvesting and lives in that practice's effect rows. [src: methodology/opportunity_space_T5.md §What did NOT make it (and why)]

## Method

### Step 1. Assemble priority and descriptor variables

For each active T5 row, resolve the dataset through [[table:BIND]] for the area of interest (AOI) context, load it, harmonise it to the analysis resolution, and clip it to the M1 opportunity-space mask. Write resolution-audit rows recording which inputs were upsampled or downsampled. [src: methodology/modules/M3_characterisation.md §6] The framework requires that upsampling by more than one resolution tier raises a visible warning, because synthetic fine-scale variability is misleading. [src: methodology/framework.md §Spatial standardisation]

### Step 2. Apply the spatial-grain rule

A priority can only discriminate hotspots inside a country if its data vary inside the country. The rule: **differentiation requires administrative level 1 (state or province) or finer, or a grid.** A priority whose bound dataset resolves to `admin0` for the AOI carries a qualified flag. It appears in the hand-off and the scorecard but is not used to discriminate hotspots within the country. [src: methodology/opportunity_space_T5.md §Spatial-grain rule]

The rule is computed at run time from `T1.grain_type` (`grid`, `admin`, `vector`) and `T1.admin_level` (`admin0`, `admin1`, `admin2`) of the bound dataset; no T5 field is needed. [src: methodology/opportunity_space_T5.md §Spatial-grain rule] Examples from the source: `gender_inequity` bound to the national Gender Inequality Index is `admin0` and becomes a national qualifier; `rural_poverty` bound to subnational World Bank Poverty and Inequality Platform data at admin1 or admin2 is eligible; `drought_hazard` bound to a gridded SPEI product is eligible. [src: methodology/opportunity_space_T5.md §Spatial-grain rule]

The rule is the human-system counterpart of the resolution trap for suitability (a coarse layer cannot carry fine-scale meaning). [src: methodology/T4_generation_method.md §2.4] It also has an arithmetic consequence: a national value is constant across a single-country AOI, so it has zero variance, cannot be min-max scaled, and contributes nothing to a relative ranking.

### Step 3. Prefer proximate over distal indicators

Where two candidate variables capture the same concern at different distances from the outcome, the method prefers the proximate one, because distal indicators compound uncertainty along the causal chain. The source gives three chains: tree cover before ecosystem health before biodiversity outcome; yield gap before literacy rate before adaptive capacity before resilience; heat-stress days before temperature anomaly before a climate change index. Distal indicators that survive selection are documented as descriptors, not priorities. [src: methodology/opportunity_space_T5.md §Proximate-over-distal principle]

This principle operates when the T5 set is authored or a country adds a variable. It is a selection rule for people writing T5 rows, not a computation the runtime performs.

### Step 4. Reduce correlated variables (two-stage selection)

Variable selection has two stages, and both apply to M3. [src: methodology/framework.md §Variable selection (two stages)] [src: AGENTS.md §What is locked]

1. **Thematic grouping** (expert, per recipe, done once). For the opportunity space the groups are the T5 themes. (For suitability in M1 the framework's six standard themes are topographic, hydrological, soil, climatic, land use and land cover, and socio-economic plus hazard.) [src: methodology/framework.md §Variable selection (two stages)] [src: methodology/modules/M3_characterisation.md §12]
2. **Correlation clustering** (empirical, per AOI). Compute pairwise Pearson correlation between the variables, cluster those with |r| > 0.7, and pass one representative per cluster to Module 4. In M3 the clustering runs **within each theme, never across themes**. [src: methodology/modules/M3_characterisation.md §6] [src: methodology/modules/M3_characterisation.md §12]

```formula
r_jk = cov(x_j, x_k) / (σ_j × σ_k)
cluster j and k together if |r_jk| > τ, with τ = 0.7 by default
```

Here `x_j` and `x_k` are two variables sampled over the valid cells of the opportunity space, `cov` is their covariance, `σ` their standard deviations, and `τ` the configurable clustering threshold. [src: methodology/modules/M1_suitability.md §6.3]

The representative is the member with the highest variance unless an expert-chosen primary is flagged. [src: methodology/modules/M1_suitability.md §6.3] T5 has no counterpart to the T4 field that flags an expert primary, so for priorities the variance rule applies by default, and the user can promote any clustered variable to primary in technical mode. [src: methodology/framework.md §Variable selection (two stages)] A caution: if variance is measured after fuzzy standardisation, the highest-variance member reflects the shape and parameters of its membership function as much as its information content, so the choice can change with a curve's steepness rather than with the data.

Cluster membership is preserved, not discarded. The cluster log maps every variable to its representative and is shown to the user, so a reader can see that, for example, a poverty layer stood in for a correlated food-insecurity layer in this AOI. [src: methodology/modules/M3_characterisation.md §4] [src: methodology/framework.md §Variable selection (two stages)]

The sources fix the threshold and the representative rule but not the clustering algorithm: the linkage method is not specified (for example, whether "|r| > τ ⇒ same cluster" is applied by single linkage, so chains of pairwise links merge, or by complete linkage, so every pair in a cluster must exceed τ). An implementation must declare it in the run metadata.

### Step 5. Standardise priorities

Each priority is rescaled to 0 to 1 according to its T5 rule. M3 applies the rule; Module 4 validates it and records it. The full normalisation and reference-frame method is specified in Module 4 and described in [[ch:m4-hotspots]]. [src: methodology/modules/M3_characterisation.md §6] [src: methodology/modules/M3_characterisation.md §13] Priority scoring uses monotonic rescales with a direction and a clip, not the fuzzy membership curves used for suitability, because priority is a need score rather than a fitness score. [src: methodology/modules/M4_hotspots.md §9] `iplc_lands` is standardised as binary presence (0 or 1). [src: methodology/modules/M3_characterisation.md §12]

### Step 6. Extract the opportunity fingerprint

Within the mask, summarise total area, area by suitability class, rural population, smallholder farm count, production value, average farm size and dominant farming-system class, and the share of each that lies in the opportunity space. [src: methodology/modules/M3_characterisation.md §6] [src: methodology/modules/M3_characterisation.md §12] These are descriptor quantities. They are reported with units, denominators and missing-data coverage. [src: method:handbook/implement-a-scan.md §3. Build the scoping brief]

### Step 7. Compute the problem-variable distribution

For each priority or hazard, compute the share of opportunity-space land at each severity level from None to Very High, for the baseline and, where projections exist, the future horizon. [src: methodology/modules/M3_characterisation.md §6] [src: methodology/modules/M3_characterisation.md §13] These distributions feed the "risk to rural livelihoods" and "what this practice can address" panels and are reused by Module 5 to place each problem's spatial presence beside the practice's response. [src: methodology/modules/M3_characterisation.md §5] The breakpoints that define the severity levels are not fixed in the pinned sources.

### Step 8. Summarise per administrative unit and set flags

Aggregate the above to administrative units for downstream ranking. [src: methodology/modules/M3_characterisation.md §6] Compute a boolean for whether IPLC land overlaps the opportunity-space mask; Module 6 uses it to raise a Free, Prior and Informed Consent (FPIC) and World Bank Environmental and Social Standard 7 (ESS7) flag. Coverage of IPLC data is patchy, so absence of a polygon does not mean absence of IPLC presence. [src: methodology/modules/M3_characterisation.md §12] [src: schema/T5_opportunity_space.csv]

### The double-count guard

A variable active in T5 must not also be active in the M2 vulnerability composite for the same practice. Poverty, gender and social inclusion proxies and adaptive-capacity proxies belong to M3 and M4 as user priorities, not to the M2 Mode B vulnerability term. The guard raises a validation error if a variable is active in both. [src: methodology/modules/M3_characterisation.md §9] [src: methodology/modules/M2_climate_risk.md §10] Descriptors are exempt because they carry no weight. [src: methodology/modules/M4_hotspots.md §13] This is one expression of the locked rule that livelihood risk (M2) and investment risk (M2b) are distinct and never summed; see [[ch:m2-climate-risk]].

## The production gap

[[var:production_gap]] is the shortfall between actual and attainable productivity of the dominant farming system. It is a `people_production` priority. [src: AGENTS.md §What is locked] [src: schema/T5_opportunity_space.csv]

The metric is not one dataset. It is resolved per farming system through BIND: a crop yield gap for cropping systems, a net primary productivity (NPP) gap for rangelands, and a composite for mixed and agro-pastoral systems. [src: methodology/opportunity_space_T5.md §Priorities (13)] Every binding at the pin is `requires_upload`, and the livestock side is noted as often thinner:

{{csv:schema/registers/BIND_dataset_binding.csv|where=variable=production_gap|cols=binding_id,scope_id,status,fitness_note}}

Two consequences follow. First, no production-gap layer can enter a run until a country supplies or selects one; a run without it is a run without that priority, and should say so. Second, because the metric changes with the farming system, production-gap values from different farming-system cells are not on one scale; standardisation within the AOI turns them into relative ranks, which hides that difference. Extending the per-system bindings is listed as follow-up work. [src: methodology/opportunity_space_T5.md §Seed issues for follow-up]

On the response side, the production gap is treated as an intermediate step towards rural poverty and food insecurity and has no scorecard row of its own (see [[ch:m5-scorecard]]). [src: schema/lookups/scorecard_rows.csv]

## Context-sensitivity flags

Variables differ in how freely a global dataset transfers and how politically charged the numbers are. [[table:VONT]] carries `context_sensitivity`: `low` for generalisable physical variables, `medium` for context-dependent but apolitical ones, and `high` for nationally derived, sovereignty-sensitive ones such as population, poverty and production statistics. For `high` variables a global model can diverge from or appear to contradict the country's own figures, so the scoping output recommends a country-endorsed source and treats the global default as provisional. [src: methodology/T4_generation_method.md §2.6] [src: schema/spec.md §VONT - Variable Ontology]

This is a flag, not a resolution. The scan marks the variable; feasibility confirms or replaces the source. The flag does not change the analysis. [src: methodology/T4_generation_method.md §2.6] [src: AGENTS.md §What is locked] The flags at the pin do not fully match the prose: `rural_poverty`, `gender_inequity`, `iplc_lands` and `agricultural_dependency` are `high`, but the T5 descriptors `rural_population` and `agricultural_production_value` are `medium`, although population and production are the guidance's examples of `high`. [src: schema/registers/VONT_variable_ontology.csv] A run should apply the guidance (treat population and production as sensitive) until the register is reconciled.

## Outputs

| Output | Grain | How to read it |
|---|---|---|
| Standardised priority layers (0 to 1) | Analysis grid, inside the mask | Relative need per priority under its declared rule; input to M4. |
| Raw priority layers | Analysis grid | Values in native units, for the raw-versus-transformed comparison on each variable card. |
| Opportunity fingerprint | AOI and administrative unit | Area, people, farms, production and farm size, and their share in the opportunity space. |
| Problem-variable distribution | Per priority, per scenario | Share of opportunity-space land at each severity level. |
| Cluster log | Per AOI | Every variable mapped to its representative. |
| Run metadata | Per run | Double-count decisions, AOI, scenario, normalisation applied, grain flags. |

[src: methodology/modules/M3_characterisation.md §4]

## Assumptions and limits

- **Not implemented at the pin.** The module specification is ratified, and the dataset binding resolver exists, but the characterisation runtime it describes is a set of suggested function signatures, not code at the pinned commit. Nothing here has been run, validated or calibrated for a country. [src: methodology/modules/M3_characterisation.md §12] [src: methodology/modules/M3_characterisation.md §11]
- **Fields named in the module notes are not all in T5.** The module notes refer to per-row `norm_method`, `direction`, `reference_frame` and `clip` fields; the pinned T5 table carries `normalisation_method` and `directionality_of_concern` but no reference-frame or clip column. Until those exist, the reference frame and clip must be declared in run configuration. [src: methodology/modules/M3_characterisation.md §12] [src: schema/T5_opportunity_space.csv]
- **Enumerations differ between spec and table.** The field-level spec still lists the pre-ratification theme values (`infrastructure`, `equity_gender`) and different direction and normalisation spellings (`high_is_bad`, `min_max`) from those in the table (`higher_is_more_concern`, `minmax`). The table and the ratification document reflect the current scheme. [src: schema/spec.md §T5 - Opportunity Space Variables] [src: schema/T5_opportunity_space.csv]
- **Some sources disagree on bindings.** The ratification document says `biodiversity_priority` ships as `requires_upload`; the pinned table and BIND bind it to the global Biodiversity Intactness Index (using 1 minus BII as concern). [src: methodology/opportunity_space_T5.md §Held out / requires_upload / deferred] [src: schema/registers/BIND_dataset_binding.csv]
- **Three priorities have no ontology entry.** `water_quality_risk`, `food_insecurity` and `catchment_water_yield` have no [[table:VONT]] row at the pin, although T5 requires one, so their units, valid resolution and sensitivity are undeclared. [src: schema/spec.md §T5 - Opportunity Space Variables] [src: schema/registers/VONT_variable_ontology.csv]
- **Several priorities need country data.** `production_gap`, `food_insecurity`, `water_quality_risk`, `catchment_water_yield` and `soil_erosion_risk` have no global default dataset in T5 at the pin. [src: schema/T5_opportunity_space.csv]
- **Correlation is not redundancy of meaning.** Clustering at |r| > 0.7 removes statistical duplication in this AOI; two correlated variables can still represent different concerns, and the representative chosen by variance is not necessarily the most policy-relevant one. Cluster membership is shown so the user can override.
- **Relative, not absolute.** Standardised layers rank cells within the chosen reference frame. They do not say whether a problem is severe in absolute terms.
- **What feasibility must still do:** confirm the country-endorsed sources for sensitive variables, check the grain of every layer used, and verify on the ground that the characterisation (population, production, IPLC presence) is right.

## Where this is configured

- [[table:T5]]: variables, themes, `mcda_role`, direction, normalisation method, default weights, projection availability.
- [[table:BIND]]: dataset per variable per context, including the per-farming-system production-gap bindings.
- [[table:T1]]: grain type and administrative level that drive the spatial-grain rule.
- [[table:VONT]]: units, valid resolution and `context_sensitivity`.
- [[table:T2]]: `double_count_risk`, which enforces the guard against the M2 vulnerability term.
- [[table:T7]]: administrative units, agro-ecological zones and farming-system classes for summaries.
