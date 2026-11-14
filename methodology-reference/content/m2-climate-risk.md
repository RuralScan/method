---
title: Module 2, rural climate risk to livelihoods
slug: m2-climate-risk
summary: After this chapter you can configure, compute and audit the livelihood climate-risk need layer (Mode A or Mode B, baseline and future) from T2 and T3, and know where the specification stops and a country application must decide.
sources:
  - methodology/modules/M2_climate_risk.md
  - methodology/modules/M2b_project_risk.md
  - methodology/framework.md
  - schema/T2_climate_risk.csv
  - schema/T5_opportunity_space.csv
  - schema/spec.md
  - schema/structure/columns.json
  - schema/registers/BIND_dataset_binding.csv
  - schema/recipes/agroforestry/T3_nbs_hazard_farming.csv
  - schema/recipes/water_harvesting_conservation/T3_nbs_hazard_farming.csv
  - methodology/T3_T6_generation_method.md
  - methodology/effect_evidence_followups.md
  - .agents/skills/_versions/v1.6.6/contracts/SEVERITY_ADDENDUM.md
  - src/nbs_ruralscan/recipe/cell_synthesis.py
  - src/nbs_ruralscan/runtime/mcda.py
  - AGENTS.md
  - method:handbook/implement-a-scan.md
---
## Question this module answers

Module 2 (M2) asks: within the area of interest (AOI), where are rural populations and production systems exposed to the climate hazards that the selected nature-based solution (NbS) could plausibly mitigate, today and under mid-century climate change? [src: methodology/modules/M2_climate_risk.md §2]

The output is a **need layer**. It says where climate risk to livelihoods is concentrated, so that the hotspot analysis in [[ch:m4-hotspots]] can weight "climate risk to rural livelihoods" alongside poverty, biodiversity and the other priorities. [src: methodology/modules/M2_climate_risk.md §5]

M2 deliberately does not answer four neighbouring questions [src: methodology/modules/M2_climate_risk.md §2]:

- **Risk to the investment itself.** Whether hazards could damage or destroy the NbS asset is Module 2b, the project disaster risk screen ([[ch:m2b-project-risk]]).
- **Biophysical feasibility.** Where the NbS can establish is M1 ([[ch:m1-suitability]]).
- **Development priorities.** Where poverty, equity or other priorities concentrate is M3 and M4.
- **Whether the NbS actually reduces the risk.** The practice-level response to each hazard is read from T3 and shown qualitatively in the scorecard ([[ch:m5-scorecard]]). Quantitative impact modelling is downstream of scoping.

### Two risk lenses, never summed

The method keeps two risk lenses apart. Risk to rural livelihoods (M2) is a need layer that feeds hotspots. Risk to the investment (M2b, the development-bank disaster-screening lens) is a feasibility filter or flag. M2b is applied as a filter and is never summed with M2 or with suitability. [src: AGENTS.md §What is locked] [src: methodology/modules/M2b_project_risk.md §2]

The reason is that the same hazard can play opposite roles. A created wetland mitigates downstream flooding for farmers, so flood is a need driver in M2. Storm surge could destroy the same wetland, so surge is an asset threat in M2b. One model cannot hold both roles without confusing "where the NbS helps" with "where the NbS is fragile". [src: methodology/modules/M2b_project_risk.md §2]

## Inputs

| Input | Where it comes from | Role |
|---|---|---|
| Selected practice | [[table:T0]] `nbs_id`, chosen in [[ch:m0-setup]] | Resolves which T3 rows apply |
| AOI and contexts | [[table:T7]] rows (country, admin unit or hydrobasin; AEZ and farming-system masks) | Spatial extent; context overrides |
| Analysis resolution | Run configuration (default 1 km, same as M1) | Common grid |
| Risk mode | Run configuration: `mode_a` (default) or `mode_b` | Selects which T2 components enter |
| Scenarios | Run configuration: always `baseline`, plus one or more `future_*` | Baseline and future surfaces |
| Practice-relevant hazards | [[table:T3]] rows with `risk_role ∈ {livelihood_mitigation, both}` | Which hazards enter the surface |
| Hazard, exposure, sensitivity, adaptive-capacity variables | [[table:T2]] rows by `risk_component`, bound to datasets through [[table:T1]] and [[table:BIND]] | The layers composed |
| Double-count flags | [[table:T2]] `double_count_risk` | Whether a variable feeds M2, M3/M4, or both |

[src: methodology/modules/M2_climate_risk.md §3] [src: methodology/T3_T6_generation_method.md §1]

### The T2 table

[[table:T2]] holds one row per risk variable. Its fields fix the component (`hazard`, `exposure`, `sensitivity`, `adaptive_capacity`), the hazard type, the scenario (`baseline`, `future_ssp126`, `future_ssp245`, `future_ssp585`), whether the variable enters each mode, the double-count flag, the normalisation method and parameters, a default weight, whether the analyst may change that weight, and the direction of the variable (`positive_risk` or `negative_risk`, with adaptive capacity as the example of `negative_risk`). [src: schema/spec.md §T2]

T2 is a single shared table, not a per-practice recipe file. It has no `nbs_id` column; practice specificity comes from T3, which lists the hazards each practice responds to. [src: schema/structure/columns.json §tables.T2] The M2 module sheet instead describes T2 rows living under each practice's recipe folder; the column manifest is the enforced structure and places T2 at the schema root. [src: methodology/modules/M2_climate_risk.md §7]

The pinned T2 rows are:

{{csv:schema/T2_climate_risk.csv|cols=variable_id,dataset_id,risk_component,hazard_type,scenario_type,use_in_simplified_mode,use_in_advanced_mode,double_count_risk,normalisation_method,normalisation_params,weight_default,directionality}}

Three things about this content matter for an auditor:

- **No row carries evidence.** Every `evidence_ids` value is empty. The `justification` prose cites published studies, but none is linked to an evidence unit, so the T2 weights are draft defaults, not evidence-derived calibration. [src: schema/T2_climate_risk.csv]
- **The rows mix practices.** Some justifications are written for agroforestry (SPEI-12 drought, heat stress, cropland exposure), others for water harvesting (runoff depth, rainfall variability, soil permeability). [src: schema/T2_climate_risk.csv]
- **Proxies are in use.** The baseline flood row uses CHELSA BIO13 (wettest-month precipitation) as a proxy for flood-generating rainfall, while the binding registry binds the global flood-hazard variable to the JRC Global Flood Hazard 100-year layer. The future drought row uses a CHELSA SSP2-4.5 dataset rather than SPEI, so the baseline and future drought metrics are not the same quantity. [src: schema/T2_climate_risk.csv] [src: schema/registers/BIND_dataset_binding.csv]

The hazard layers that the M2 sheet records as bound in [[table:BIND]] are drought (SPEI v2.6), flood (JRC Global Flood Hazard, 100-year return period), heat stress (CHELSA BIO5, maximum temperature of the warmest month) and water stress (WRI Aqueduct 4.0). [src: methodology/modules/M2_climate_risk.md §14]

### Hazard vocabulary

T2 allows seven hazard types: `drought`, `flood`, `heat_stress`, `fire`, `wind_cyclone`, `waterlogging`, `frost`. [src: schema/structure/columns.json §tables.T2] T3 drops frost for every practice: frost-tagged evidence stays in the register and can feed T6, but opens no T3 livelihood or asset cell. [src: src/nbs_ruralscan/recipe/cell_synthesis.py §EXCLUDED_T3_HAZARDS] [src: schema/spec.md §T3] Because M2 selects hazards through T3, a frost row in T2 can never be selected for any practice. Erosion is not a hazard in T3; it is the T6 priority `soil_erosion_risk`. [src: schema/spec.md §T3]

## Method

The module sheet defines eight steps. Each is specified as an input-output contract; the composition functions inside steps 4 and 5 are marked as open methodology choices. [src: methodology/modules/M2_climate_risk.md §6]

### Step 1. Scope the hazards from T3

Take the T3 rows for the selected practice whose `risk_role` is `livelihood_mitigation` or `both`. The distinct `hazard_type` values form the hazard set. A hazard with no T3 row for the practice is not included, so recipe authors must populate T3 explicitly. [src: methodology/modules/M2_climate_risk.md §6.1] [src: methodology/T3_T6_generation_method.md §1]

### Step 2. Assemble hazard layers

For each hazard in the set and each scenario, build one band from the T2 hazard rows and their T1 datasets, harmonised to the AOI and resolution. Bands are intensity or frequency metrics (SPEI-12, return-period flood depth, days above a heat threshold). Context overrides from T7 apply where defined, for example AEZ-specific drought thresholds, and every input gets a resolution-audit row. [src: methodology/modules/M2_climate_risk.md §6.2]

### Step 3. Assemble exposure layers

Build the exposure stack from T2 exposure rows: rural population, smallholder farm density, production value, livestock density. Exposure is **baseline only**: it is not projected forward, so a future surface is baseline exposure combined with future hazard. [src: methodology/modules/M2_climate_risk.md §6.3] Where they align, exposure layers should reuse the T5 descriptor variables `rural_population` (WorldPop), `agricultural_production_value` (MapSPAM v2) and `farm_size` (Lesiv et al. 2019). [src: methodology/modules/M2_climate_risk.md §14] [src: schema/T5_opportunity_space.csv]

### Step 4. Normalise each layer

Each T2 variable carries a `normalisation_method` from the enum `min_max`, `percentile_clip`, `log_transform`, `none`, with optional parameters such as `{p_low: 2, p_high: 98}`. [src: schema/spec.md §T2] The specification names the methods and their parameters but does not write out the transforms, and no M2 runtime module exists at the pinned commit (the runtime package holds the MCDA, binding and scorecard code, not `climate_risk.py`). The transforms below, and the `negative_risk` inversion, are not specified by the method; they are the standard forms and need confirmation before use. An implementation must confirm them and log them.

```formula
min_max:          x'(p) = (x(p) − min_AOI x) / (max_AOI x − min_AOI x)
percentile_clip:  x'(p) = clip( (x(p) − P_low) / (P_high − P_low), 0, 1 )
log_transform:    x'(p) = min_max( ln(1 + x(p)) )
negative_risk:    x''(p) = 1 − x'(p)
```

- `x(p)`: raw value of the variable at pixel `p`.
- `min_AOI x`, `max_AOI x`: minimum and maximum of the variable over the AOI.
- `P_low`, `P_high`: the `p_low`-th and `p_high`-th percentiles of the variable over the AOI, from `normalisation_params`.
- `clip(·, 0, 1)`: truncation to the unit interval.
- `negative_risk`: applied when `directionality = negative_risk`, so that a higher value always means more risk.

One pinned T2 row uses `normalisation_method = linear_decay` with parameters `{suitable_max: 0, unsuitable_min: 10000}`; that value is not in the T2 enum. [src: schema/T2_climate_risk.csv] [src: schema/spec.md §T2]

### Step 5. (Mode B only) Compose vulnerability

In Mode B, vulnerability is a function of sensitivity and adaptive capacity, following IPCC AR6, and returns a 0–1 raster where higher means more vulnerable. Variables flagged `opportunity_space_only` are excluded. The composition function is **not yet chosen**: the options recorded are a weighted geometric mean, an additive index or a principal-component index. Mode A skips this step entirely. [src: methodology/modules/M2_climate_risk.md §6.4] The suggested first implementation defers Mode B behind a not-implemented error. [src: methodology/modules/M2_climate_risk.md §14]

### Step 6. Compose risk

The framework follows the IPCC AR6 decomposition: risk is a function of hazard, exposure and vulnerability, with vulnerability a function of sensitivity and adaptive capacity. [src: methodology/framework.md §Climate risk formulation] The module sheet's suggested default is per-hazard multiplication, then a weighted sum across hazards, then normalisation to 0–1. [src: methodology/modules/M2_climate_risk.md §6.5]

```formula
Mode A:  R_s(p) = N( Σ_h w_h · H_{h,s}(p) · E(p) )
Mode B:  R_s(p) = N( Σ_h w_h · H_{h,s}(p) · E(p) · V(p) )
Δ_s(p)  = R_s(p) − R_baseline(p)
```

- `R_s(p)`: composite rural climate risk at pixel `p` under scenario `s`.
- `h`: a hazard in the set from Step 1.
- `w_h`: weight of hazard `h`, from T2 `weight_default` or the analyst's adjusted value where `weight_adjustable = true`.
- `H_{h,s}(p)`: normalised hazard layer for hazard `h` under scenario `s`.
- `E(p)`: normalised baseline exposure. How several exposure layers combine into `E` is not specified by the method (see below).
- `V(p)`: Mode B vulnerability from Step 5.
- `N(·)`: rescaling of the composite to 0–1.
- `Δ_s(p)`: change in risk from baseline to future scenario `s`.

The composite as written here, a normalised weighted sum of per-hazard products, is not specified by the method; it is the standard form and needs confirmation before use. The choice between this multiplicative form and an additive one is open; whichever is used must be documented and logged in the run metadata. [src: methodology/modules/M2_climate_risk.md §6.5] Equal hazard weights are the recommended starting point, with recipe-specific hazard weights an open question. [src: methodology/modules/M2_climate_risk.md §Open questions]

Two parts of this formula are not specified and must be fixed by an application:

- **How several exposure layers combine into `E`.** T2 gives each exposure variable its own weight, but the sheet does not say whether `E` is a weighted mean of the exposure layers or whether each enters the product separately. A weighted mean is the standard form, but it is not specified by the method and needs confirmation before use.
- **How T2 weights partition.** T2 weights sum to 1.0 within each `scenario_type` group across all components (hazard, exposure, sensitivity, adaptive capacity together). [src: schema/spec.md §T2] The pinned baseline rows do sum to 1.0, and the single future row has weight 1.0. [src: schema/T2_climate_risk.csv] Using them as hazard weights `w_h` therefore needs a renormalisation within the hazard component, and dropping sensitivity and adaptive-capacity rows in Mode A needs one too. Neither renormalisation is written down.

### Step 7. Run future scenarios

Repeat Step 2 with future hazard datasets (through T1 or T2 `scenario_type`), keep Step 3 exposure fixed, and recompose with Step 6. Produce one risk raster and one change raster per scenario. [src: methodology/modules/M2_climate_risk.md §6.6]

### Step 8. Sensitivity and summary

Perturb the weights and map the variance, using the same routine as M1: each of `n = 50` runs multiplies each weight by `(1 + u)`, with `u` drawn uniformly from `[−0.10, 0.10]`, renormalises the weights to sum to 1, recomputes the weighted overlay, and returns per-pixel mean and variance plus the range each weight took. [src: methodology/modules/M2_climate_risk.md §6.7] [src: src/nbs_ruralscan/runtime/mcda.py §sensitivity_perturb]

```formula
w'_k = w_k (1 + u_k) / Σ_j w_j (1 + u_j),   u_k ~ U(−0.10, 0.10)
Var(p) = variance over runs of Σ_k w'_k · x_k(p)
```

- `w_k`: default weight of layer `k`; `w'_k`: perturbed, renormalised weight.
- `x_k(p)`: normalised layer `k` at pixel `p`.
- `Var(p)`: the sensitivity raster.

Then summarise per hazard, per scenario and per admin unit: mean risk, share of area in the high-risk class, exposed rural population, exposed production value, and change against baseline. [src: methodology/modules/M2_climate_risk.md §6.8] The cut-off for the "high-risk class" is not specified.

## Mode A and Mode B

| | Mode A, hazard × exposure | Mode B, full IPCC AR6 |
|---|---|---|
| Formula | `R = H × E` | `R = H × E × V`, `V = f(sensitivity, adaptive capacity)` |
| Variables needed | Hazard and exposure | Hazard, exposure, sensitivity, adaptive capacity |
| Status | Pilot default | Selectable, not default |

[src: methodology/modules/M2_climate_risk.md §9] [src: AGENTS.md §What is locked]

**Why Mode A is the default.** Vulnerability indicators (poverty, education, adaptive capacity, gender and social-inclusion proxies) also appear as stand-alone priorities in M3 and M4. If they enter M2 through `V` and then enter M4 again as priorities, the same signal is counted twice in the hotspot index, once inside the climate-risk layer and once on its own. Mode A keeps "risk to livelihoods" separate from "development priorities" and needs about half the data. Mode B is more complete conceptually and suits AOIs with good vulnerability data where the analysis explicitly compares the two modes. [src: methodology/modules/M2_climate_risk.md §9] [src: methodology/framework.md §Climate risk formulation]

The module sheet recommends a per-practice-run mode toggle, so an analyst could run Mode A for one practice and Mode B for another in the same AOI, with the mode recorded in the run metadata so that outputs from different modes are not compared by accident. This is listed as an open question; it is not ratified. [src: methodology/modules/M2_climate_risk.md §9] [src: methodology/modules/M2_climate_risk.md §Open questions]

**Mode flags in T2 are ambiguous.** The framework maps the two modes onto the T2 flags `use_in_simplified_mode` and `use_in_advanced_mode`. [src: methodology/framework.md §Climate risk formulation] The field reference instead defines the simplified mode as "climate-index-only" and the advanced mode as "hazard × exposure". [src: schema/spec.md §T2] The pinned data fit neither reading cleanly: a sensitivity variable is flagged for the simplified mode, and the baseline heat-stress hazard is not. [src: schema/T2_climate_risk.csv] An application must state which flag selects which mode before running.

## The double-count guard

### How the guard works

Each T2 variable carries `double_count_risk`:

- `risk_only`: used in M2 only.
- `opportunity_space_only`: used in M3/M4 only; excluded from the Mode B vulnerability composite.
- `shared`: the pipeline uses it in M2 only by default; the recipe author can override.

[src: methodology/modules/M2_climate_risk.md §10] [src: schema/spec.md §T2]

The guard is a start-of-pipeline check: if a variable is active in both T2 and [[table:T5]] for the same practice without an explicit override, validation fails. [src: methodology/modules/M2_climate_risk.md §10] Since T5 now separates `priority` from `descriptor` rows, the concern is a T2 variable doubling into a T5 **priority** row; overlap with a descriptor, which never enters the hotspot sum, is not double counting. [src: methodology/modules/M2_climate_risk.md §14] T5 marks rows that also act as climate-risk components with `is_climate_risk_component`. [src: schema/spec.md §T5] At the pin, the three T5 `climate_hazard` priorities (`drought_hazard`, `flood_hazard`, `heat_stress_hazard`) carry that flag. [src: schema/T5_opportunity_space.csv]

### Recommended placements

The module sheet recommends: poverty headcount and education stay in M3/M4 only, never in Mode B vulnerability; smallholder share and crop production value go to M2 exposure, with M3 free to show production value descriptively. [src: methodology/modules/M2_climate_risk.md §10]

### Where the sources disagree on road access

The sheet says distance to road belongs to neither M2 nor M4 because it is an M1 suitability variable. [src: methodology/modules/M2_climate_risk.md §10] T2 contains `adaptive_capacity_road_access` as a `shared` Mode B adaptive-capacity variable. [src: schema/T2_climate_risk.csv] The locked routing for enabling-environment variables says road and market access are soft, investment-addressable factors that belong to the M2b operational-risk stream and implementation guidance, not to structural suitability. [src: AGENTS.md §What is locked] The locked routing is the current rule for how evidence is extracted; the T2 row and the module-sheet placement predate it and are inconsistent with it. See [[ch:m2b-project-risk]].

### Shared hazards with M2b are not double counting

A hazard variable may feed both M2 and M2b. Double counting only arises when correlated variables are summed into the same additive composite. M2b is a filter, so it never adds a term to the hotspot sum. [src: methodology/modules/M2b_project_risk.md §7]

## How T3 hazard responses connect to this layer

[[table:T3]] is the practice × hazard × farming-system table. It is generated by cell synthesis over pooled evidence, not authored row by row (see [[ch:effect-synthesis]]). Each row's `risk_role` says whether the practice mitigates the hazard for livelihoods (`livelihood_mitigation`, read by M2), whether the hazard threatens the asset (`asset_threat`, read by M2b), or both. [src: schema/spec.md §T3]

M2 reads, from livelihood rows: `nbs_id`, `hazard_type`, `farming_system`, `mitigation_potential`, `confidence`, `landscape_scale_only` and `applicability`. [src: methodology/T3_T6_generation_method.md §1] What the specification uses them for is narrower than what they could support:

- **Specified:** the hazard set (Step 1).
- **Specified elsewhere:** the practice's qualitative response to each hazard is shown in the scorecard, which reads T3, not the M2 rasters. [src: methodology/modules/M2_climate_risk.md §5]
- **Not specified:** any modulation of the M2 surface by `mitigation_potential` or `confidence`. M2 maps hazard exposure; it does not multiply it by how well the practice responds.

### What the T3 fields mean for a reader of M2

- `mitigation_potential` is an ordinal class (`very_negative`, `negative`, `none`, `low`, `moderate`, `high`, `very_high`), plus `conflicting_evidence` when material weight sits on both signs, and blank for a data-deficient cell. `very_high` requires the top rank and `confidence ≥ high`. [src: schema/spec.md §T3]
- `confidence` is derived from two axes, evidence level and agreement level, through the IPCC matrix; it is never authored. [src: schema/spec.md §T3] [src: methodology/T3_T6_generation_method.md §7.4]
- `applicability.transfer_class` (`in_context`, `adjacent`, `out_of_context`, `mixed`) says whether the evidence comes from contexts like the target. Transferability is kept separate from confidence. At runtime, a global row whose recomputed class is `out_of_context` for the AOI is returned as `no_applicable_evidence`, not as a class. [src: methodology/T3_T6_generation_method.md §5.5] [src: methodology/T3_T6_generation_method.md §7.4]
- `landscape_scale_only = true` means the effect appears only at landscape or catchment scale, not on the farm. [src: schema/spec.md §T3]
- `farming_system` is a cell key (`all` for the universal row), and scope rows by AEZ, country, region, hydrobasin or income group refine the global row where at least two independent sources in that context diverge. [src: schema/spec.md §T3]

### Hazard severity and the intensity discount

T3 originally answered "does the practice reduce drought impact?" with one class whatever the drought. Every hazard-tagged evidence unit now carries `context.hazard_severity` (`mild`, `moderate`, `severe`, `extreme`, or `unspecified` by default), which records the source author's own description of the event, backed by a verbatim `severity_cue`. It is never inferred from rainfall numbers or country, and "when in doubt, `unspecified`". [src: .agents/skills/_versions/v1.6.6/contracts/SEVERITY_ADDENDUM.md §context.hazard_severity]

The synthesis uses severity in two ways. First, a graded **hazard-intensity discount**: in a livelihood cell, the class is scaled by the weighted share of measured same-hazard evidence that found no benefit or a reversal, as `rank × (1 − share)`, floored at `low`, and flagged `intensity_limited`. Failures tagged `mild` are exempt. Second, every livelihood row carries `severity_coverage`, which records gains and failures per severity value and says when the severe end is untested. [src: methodology/effect_evidence_followups.md §Hazard-intensity discount] [src: .agents/skills/_versions/v1.6.6/contracts/SEVERITY_ADDENDUM.md §Synthesis]

For M2 users this matters because a need layer that shows severe future drought next to a practice whose drought evidence comes only from moderate dry years invites a wrong reading. The T3 row says which end of the hazard range the evidence covers; the M2 surface does not.

## Outputs

| Output | Form | Use |
|---|---|---|
| Composite rural climate risk, baseline | Cloud-optimised GeoTIFF, 0–1 | Opportunity-space view next to M1; M4 hotspot layer |
| Composite risk, each future scenario | GeoTIFF, 0–1 | Future-state view |
| Change raster per scenario | GeoTIFF | Climate trajectory |
| Per-hazard surfaces | GeoTIFF per hazard × scenario | Drill-down |
| Hazard summary table | CSV per hazard × scenario × admin unit | Panel readout |
| Weight log | CSV | Audit of hazard and exposure weights and mode |
| Resolution audit | CSV, merged with M1 | Native versus analysis resolution per input |
| Run metadata | JSON | Mode, scenarios, double-count decisions |

[src: methodology/modules/M2_climate_risk.md §4]

**How to read it.** Values are relative within the AOI, not absolute risk. A pixel at 0.8 is among the more exposed places in this AOI under this mode and these weights; it is not comparable with 0.8 in another AOI or another mode. M4 consumes the baseline composite (and optionally the future one) as one priority layer. [src: methodology/modules/M2_climate_risk.md §1] [src: methodology/modules/M2_climate_risk.md §5] The product handbook asks the analyst to state the period and scenario with every M2 map. [src: method:handbook/implement-a-scan.md §3. Build the scoping brief]

## Worked illustration

This illustration uses the pinned T3 table for water harvesting and conservation; it shows how Step 1 behaves on real generated rows. No M2 surface has been computed from it.

The global, all-farming-system livelihood rows for [[practice:water_harvesting_conservation]] are drought, fire, flood, heat stress, waterlogging and wind/cyclone. [src: schema/recipes/water_harvesting_conservation/T3_nbs_hazard_farming.csv] Under the Step 1 rule ("a hazard with a T3 row is included") all six would enter the hazard set. Read with their classes, they tell a different story:

- **Drought**: `mitigation_potential = moderate`, confidence very high, transfer class in context, landscape scale only. The class was moderated by the intensity discount, because a substantial share of measured drought-year evidence found no gain. [src: schema/recipes/water_harvesting_conservation/T3_nbs_hazard_farming.csv] [src: methodology/effect_evidence_followups.md §Hazard-intensity discount]
- **Flood**: moderate, confidence high, adjacent context, landscape scale only.
- **Waterlogging**: `negative` at very high confidence: the practice worsens waterlogging.
- **Fire, heat stress, wind/cyclone**: blank class at very low confidence, that is, data-deficient.

[src: schema/recipes/water_harvesting_conservation/T3_nbs_hazard_farming.csv]

So, taken literally, Step 1 would map livelihood exposure to three hazards for which the practice has no evidenced effect and one it makes worse. The specification does not say whether rows with a blank, `none` or negative class enter the hazard set. A defensible application restricts the set to rows with a positive class and labels the rest, but that is an application choice, not a specified rule.

## Assumptions and limits

- **Not implemented.** At the pinned commit there is no M2 runtime module; the module sheet is a draft scaffold with its composition functions open. The acceptance tests listed in the sheet (an end-to-end Mode A run, a finite Mode B vulnerability raster, a guard that catches a mis-flagged variable) are unchecked. [src: methodology/modules/M2_climate_risk.md §12] Nothing here has been run, validated or calibrated.
- **T2 is unevidenced draft content.** Weights and normalisation parameters are defaults with no linked evidence units; treat them as placeholders, not calibration.
- **Relative, AOI-bounded scores.** Normalisation over the AOI makes the surface relative. If baseline and future layers are normalised separately, their difference mixes climate change with rescaling; the specification does not fix shared bounds, so an application must.
- **Exposure is held at baseline.** Future risk shows hazard change only, not population or land-use change.
- **Metric mismatches.** Baseline and future drought use different datasets; baseline flood uses a rainfall proxy rather than the bound flood-hazard layer.
- **The response is not in the surface.** M2 says where hazards meet livelihoods, not where the practice reduces them. That reading comes from T3 classes, their confidence, transfer class and severity coverage, and it should be read alongside the map.
- **Hazard-set rule is permissive.** Step 1 admits data-deficient and negative rows unless the application filters them.
- **Unresolved mode flags.** The T2 mode flags do not map cleanly to Mode A and Mode B.
- **Feasibility must still do:** local hazard data at design resolution, event-specific hydrology, a vulnerability assessment with country-endorsed socio-economic data, and validation of any exposure layer flagged as context-sensitive.

## Where this is configured

- [[table:T2]]: risk variables, components, scenarios, mode flags, double-count flags, normalisation, default weights, directionality.
- [[table:T3]]: the practice × hazard rows; `risk_role` decides which rows M2 reads.
- [[table:T1]] and [[table:BIND]]: datasets and their context-resolved bindings.
- [[table:T5]]: `is_climate_risk_component` and `mcda_role`, which the double-count guard checks against.
- [[table:T7]]: AOI, AEZ and farming-system contexts and overrides.
- [[table:EV]]: the evidence units behind T3, including `hazard_severity`.
- Run configuration (from [[ch:m0-setup]]): mode, scenarios, resolution.
