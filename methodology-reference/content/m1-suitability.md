---
title: "M1: Suitability to opportunity space"
slug: m1-suitability
summary: Lets the reader configure, compute and correctly interpret a family-level suitability surface and opportunity space, including membership functions, gates, weighting, resolution rules and what a held calibration prevents.
sources:
  - methodology/modules/M1_suitability.md
  - methodology/framework.md
  - methodology/T4_generation_method.md
  - methodology/T4_developer_contract.md
  - methodology/families/agroforestry.md
  - methodology/recipes/water_harvesting.md
  - schema/spec.md
  - schema/structure/columns.json
  - schema/registers/FAM_family_registry.csv
  - schema/registers/VONT_variable_ontology.csv
  - schema/recipes/agroforestry/T4_run_policy.csv
  - reference/R/spatMCDA.R
  - src/nbs_ruralscan/runtime/mcda.py
  - src/nbs_ruralscan/runtime/numeric.py
  - src/nbs_ruralscan/runtime/categorical.py
  - src/nbs_ruralscan/recipe/calibration_requirements.py
  - src/nbs_ruralscan/recipe/developer_contract.py
  - docs/redesign/00-config.html
  - .agents/skills/extraction_contracts/T4_review_contract.md
  - AGENTS.md
  - method:handbook/read-a-suitability-recipe.md
  - method:handbook/implement-a-scan.md
---

## Question this module answers

M1 asks: within this geography, where could this NbS be considered, given terrain, climate, soils, the existing land-use system and hard legal or physical exclusions, and how is that suitability distributed across the landscape? [src: methodology/modules/M1_suitability.md §2. Question answered]

The answer is a **continuous suitability surface** (0 to 1, not a binary map), an ordinal classification of it, and an **opportunity-space mask**: the cells in which the practice merits further consideration. The surface is NbS-specific (variables and responses come from the recipe), family-specific (see step 1) and AOI-specific (correlation reduction and objective weights are computed per AOI). [src: methodology/modules/M1_suitability.md §1. Purpose]

M1 deliberately does not answer where the NbS is strategically desirable (M4), where development outcomes concentrate (M3 and M4), what benefits it delivers (M5) or what comes next (M6). Keeping those questions downstream keeps M1 interpretable. [src: methodology/modules/M1_suitability.md §2. Question answered]

The module specification is a draft (v0.1). Several of its example thresholds and its infrastructure-scenario wording have been superseded by later evidence and routing decisions and must not supply hidden thresholds. Where this chapter reports a conflict, the later rule is stated and both sources are cited. [src: methodology/modules/README.md §Index] [src: methodology/T4_developer_contract.md §Aggregation baseline and design history]

## Inputs

| Input | Source | Schema | Notes |
|---|---|---|---|
| Selected NbS and family | M0 | `T0.nbs_id`, `FAM.suitability_family_id` | T4 rows are keyed to the family. |
| AOI | M0 | [[table:T7]] rows | Country, administrative unit or hydrobasin. |
| Analysis resolution | M0 | run configuration | Bounded by the binding variable and product type (step 4). |
| Climate scenario | M0 | run configuration | `baseline` and optionally future scenarios. |
| Suitability mappings | recipe | [[table:T4]] rows for the family | Variable, dataset, response type and parameters, dimension, weight, flags, evidence IDs. |
| Dataset access | [[table:T1]] via [[table:BIND]] | | Asset, band, native resolution, hosting status. |
| Context overrides | `T4.context_overrides` | keyed to T7 | Re-parameterise a response for an agro-ecological zone or farming system. |
| Approved run policy | [[table:T4_RUN]] | per recipe | Criterion set, weights, aggregation, missing-value and gate policy. |
| Variable Cards | recipe | six slots | Display metadata, not analytical input. |

[src: methodology/modules/M1_suitability.md §3. Inputs] [src: schema/spec.md §T4_RUN]

## Method

### 1. Work per suitability family

An NbS is not a monolith. The method uses three levels: the NbS (the T0 anchor), its **sub-practices** (the variants, for example alley cropping, farmer-managed natural regeneration, windbreaks), and **suitability families**, the unit T4 is authored against. [src: methodology/T4_generation_method.md §2.1 Practice definition → subpractices → suitability families]

**Grouping criterion: shared dominant limiting factor.** A family is a set of sub-practices that share the factor that decides where they are suitable. That factor determines the leading variable and the whole variable set. Grouping by visual structure mis-merges: scattered trees on cropland can arise by planting (limited by the climate, soil and slope envelope plus management) or by retention and natural regeneration (limited by remnant rootstock, seedbank, seed-source proximity and tenure). The picture on the ground is the same; the limiting factor, variables and suitable area differ, so these are different families. [src: methodology/T4_generation_method.md §2.1 Practice definition → subpractices → suitability families] [src: methodology/families/agroforestry.md §1. The grouping principle]

Four limiting-factor archetypes recur: biophysical envelope with planting; regeneration potential; placement or geometry (linear features following wind exposure or slope and flow lines); and proximity or intensive use at sub-pixel scale (for example homegardens). [src: methodology/T4_generation_method.md §2.1 Practice definition → subpractices → suitability families]

A family that needs *additional* variables is its own family, not a context override of another. Context overrides only re-parameterise existing variables. Silvopasture therefore cannot be a "grazing context" of planted silvoarable: it needs forage, grazing and livestock variables. [src: methodology/T4_generation_method.md §2.1 Practice definition → subpractices → suitability families] Where a family is gated by a host crop (shade trees over coffee, cocoa or tea), the crop is a **parameter, not a sub-family**: run per crop, take the maximum, and retain the driving crop. [src: AGENTS.md §What is locked] [src: src/nbs_ruralscan/runtime/categorical.py]

Family schemes are first-pass hypotheses, revisable once evidence is in, and each grouping records its rationale and references so that a revision is auditable. Per-practice schemes and their review status are in the practice chapters (for example [[ch:practice-agroforestry]]). [src: methodology/T4_generation_method.md §2.1 Practice definition → subpractices → suitability families] [src: schema/spec.md §FAM]

The registered families and their product types at the pin:

{{csv:schema/registers/FAM_family_registry.csv|cols=subpractice_id,nbs_id,suitability_family_id,spatial_product_type}}

Rows whose family identifier ends in `__cross_family` are tagging values for evidence that applies across all families of one NbS. They are not real sub-practices and do not define a surface, although in effect synthesis the tag still forms its own row and votes like a family (see [[ch:effect-synthesis]]). [src: schema/registers/FAM_family_registry.csv] [src: src/nbs_ruralscan/recipe/cell_synthesis.py §synthesise_cell_with_families]

### 2. Read the family's spatial product type

The MCDA machinery (variables, responses, weighted composite, 0 to 1) is shared by every family. What the output *means*, and how footprint is accounted, differ by family. Each family carries a `spatial_product_type`: [src: methodology/T4_generation_method.md §2.4 Spatial product type & the resolution trap]

| `spatial_product_type` | Meaning | What may be reported as footprint |
|---|---|---|
| `area_suitability` | A pixel can host the practice. | Area (km²). |
| `applicability_zone` | The area would benefit or is a candidate; the intervention is a line within it. | Candidate length or density, **not** pixel area. |
| `zonal_linear` | Suitability is defined along a feature such as a stream. | Zone length or riparian area. |
| `qualitative_only` | Sub-pixel; a raster would mislead. | None. A scorecard entry and a hand-off note. |

[src: methodology/T4_generation_method.md §2.4 Spatial product type & the resolution trap] [src: schema/spec.md §FAM]

**The resolution trap.** A linear or point practice occupies a small fraction of a pixel. Reporting a suitable pixel as suitable area over-estimates footprint, and the over-estimate grows with pixel size: a 5 km cell flagged for windbreaks implies 25 km² of plantable extent where the real quantity is a few line-kilometres. The method therefore: [src: methodology/T4_generation_method.md §2.4 Spatial product type & the resolution trap]

- never reports pixel area as footprint for `applicability_zone`, `zonal_linear` or `qualitative_only` families;
- estimates footprint as candidate zone × a realisable density factor (boundary length, settlement density), not as zone area;
- requires the resolution audit to flag every non-area product, and widens stated uncertainty, not just map blur, when the grid is coarsened;
- compares practices only within a product type, or caveats explicitly; an `area_suitability` km² is never ranked against an `applicability_zone` surface.

A `qualitative_only` family is also parked out of the generated effect tables; its evidence stays in the register for the hand-off. [src: AGENTS.md §What is locked]

### 3. Classify each mapping by suitability dimension

Every T4 row carries a `suitability_dimension`, defined by what does the limiting and ordered from least to most changeable: [src: schema/spec.md §`suitability_dimension`]

1. **`biophysical_constraint`**: the natural envelope of climate, terrain and soils. Can the NbS establish and persist at all? Slow to change, hard to engineer.
2. **`system_constraint`**: the existing land-use, farming or land-cover system the NbS must integrate with (current land cover, existing tree cover, farming system, host-crop presence, livestock density). Changes over years to decades.
3. **`operational_constraint`**: implementation feasibility and the enabling environment (access, tenure, extension, legal and protected-area exclusions).

#### Hard versus soft operational constraints

The operational dimension is split by a practical test: if switching the variable off in a what-if scenario is a reasonable policy question, the variable is soft; if not (no one can legislate away a water body), it is hard. [src: methodology/T4_generation_method.md §2.7]

- **Hard exclusions** (legal protected areas, water bodies, urban or built-up footprints, formally designated reserves) stay inside the opportunity-space logic as T4 masks with `is_scenario_candidate = false`.
- **Soft, investment-addressable factors** (road access, market access, extension, tenure security, finance and credit, labour, value chains, governance) are **not** structural suitability. Their evidence is extracted with `use_role = operational_risk`, routed to the M2b operational-risk stream and to hand-off guidance, and kept out of the T4 suitability surface. Extracting them as structural suitability is a recorded quality defect.

[src: AGENTS.md §What is locked] [src: schema/spec.md §EV]

**The sources are not fully aligned on this point.** The T4 method text and the schema specification still describe soft factors as T4 rows that act as scenario levers (`is_scenario_candidate = true`) as well as inputs to the M2b filter. The locked routing rule supersedes that wording: soft factors may appear in a recipe as flagged operational rows for completeness and traceability, but they do not enter the core M1 weighted score. [src: methodology/T4_generation_method.md §2.7] [src: schema/spec.md §Hard vs soft operational decision] [src: AGENTS.md §What is locked] [src: methodology/T4_developer_contract.md §Module boundaries and output meaning] The consequence for an analyst is simple: biophysical, system and hard-operational dimensions define the opportunity space; soft operational factors become scenario levers and M2b flags ([[ch:m2b-project-risk]]).

### 4. Constrain by observed distribution where data exist

When a family is gated by an existing host system (a land use, a crop, a grazing system), the method prefers the host's **observed distribution or production** over a model of its potential niche. [src: methodology/T4_generation_method.md §2.5 Constrain by observed distribution, not a modelled niche, where data exist]

The reasons are scientific, not convenience. For "improve the existing system" interventions such as shading existing coffee or cocoa, the intervention happens where the system already is; a potential-niche surface over-claims into land the system never occupies. Observed distribution also integrates the climate, soil, market and tenure reasons the system sits where it does, which a bioclimatic envelope misses. [src: methodology/T4_generation_method.md §2.5 Constrain by observed distribution, not a modelled niche, where data exist]

Rules: use a graded constraint (fractional area or production intensity from crop-allocation maps, harvested-area layers, Earth-observation commodity maps or national statistics) rather than binary presence where data support it; carry the coarseness of the distribution layer into the uncertainty; use niche or envelope modelling only as a fallback, flagged as potential rather than realised extent; and where the family is about adaptation (shade), prioritise the climate-stressed edge *within* the observed distribution rather than extending beyond it. The choice between distribution-constrained and niche-modelled gating is recorded per family. [src: methodology/T4_generation_method.md §2.5 Constrain by observed distribution, not a modelled niche, where data exist]

Two cautions apply when the host is a set of crops. Combining permitted crops by OR establishes where a host exists; it does not establish the biophysical response of each crop. And unknown land-cover classes remain unknown rather than implying a conversion opportunity. [src: methodology/T4_developer_contract.md §Module boundaries and output meaning] [src: methodology/T4_developer_contract.md §Planted host and exclusion contracts]

### 5. Assemble variables at a valid resolution

For each T4 row, resolve its dataset through [[table:BIND]] (most-specific context wins; see [[ch:farming-systems-and-data]]), fetch it, and harmonise all variables to the analysis grid as one band each. Apply context overrides and write the resolution audit. [src: methodology/modules/M1_suitability.md §6.1 Variable assembly]

Coarseness is bounded by two independent limits at once. The first is footprint honesty (step 2). The second is **variable validity**: some variables stop being meaningful above a certain grid size. [src: methodology/T4_generation_method.md §2.4 Per-variable resolution validity]

Slope is the standard case. It is a derivative of elevation, and computed slope flattens as grid size grows, which biases suitability optimistic (under-reads steepness, over-reads suitable area). Derivatives such as slope, topographic wetness index, drainage density and roughness lose signal faster than smooth primary fields such as rainfall or poverty. [src: methodology/T4_generation_method.md §2.4 Per-variable resolution validity]

Rules:

- Each canonical variable carries `min_meaningful_resolution_m` (the coarsest grid at which it stays valid), `resolution_sensitivity` (low, medium, high) and a `derive_then_aggregate` flag. [src: schema/spec.md §VONT]
- **The run's maximum coarseness is set by the most resolution-sensitive selected variable** (the binding variable). A variable run coarser than its limit is flagged and must be excluded, down-weighted with widened uncertainty, or supplied from finer data. [src: methodology/T4_generation_method.md §2.4 Per-variable resolution validity]
- **Derive then aggregate; never resample then derive.** Compute scale-dependent derivatives at native fine resolution, then aggregate the derived metric to the analysis grid, carrying a within-pixel distribution (for example mean slope and the fraction of the cell below the slope threshold). The response can then use the sub-grid fraction, which also gives an honest realisable fraction for slope-limited families. [src: methodology/T4_generation_method.md §2.4 Per-variable resolution validity]
- Upsampling an input by more than one tier of the resolution ladder triggers a visible warning. [src: methodology/framework.md §Spatial standardisation]

Variables flagged for derive-then-aggregate, with their limits:

{{csv:schema/registers/VONT_variable_ontology.csv|where=derive_then_aggregate=true|cols=canonical_variable_id,canonical_unit,min_meaningful_resolution_m,resolution_sensitivity}}

Input preparation for multi-depth soil layers follows the same logic of transforming before evaluating. A proposed scoping summary for 0 to 30 cm scales native units first, takes a thickness-weighted mean of the depth layers second, and evaluates the response last; a missing layer propagates unknown. Such preparation proposals are recorded as proposed and not activated until a run adopts them. [src: methodology/T4_developer_contract.md §Dataset preparation proposals and source compatibility]

### 6. Assign each mapping its execution role

A T4 row can play one of four roles in execution, plus a non-executable fifth. The developer compiler derives the role from the row and records it, so that compensatory scores, gates and scenarios are never mixed silently. [src: methodology/T4_developer_contract.md §Developer table and related files] [src: src/nbs_ruralscan/recipe/developer_contract.py]

| Role | What it does | How it is identified |
|---|---|---|
| Suitability score | A numeric 0–1 response entering the weighted combination. | Numeric profiles or pools, or a held numeric calibration. |
| Eligibility gate | A non-compensatory host-system requirement (for example land cover that can host the practice). Binary class scores only. | A categorical `class_map`; `mapping_role = eligibility_gate`. |
| Hard exclusion | A legal or physical mask (protected area, water body, built-up land). | Remaining non-scenario rows; requires an assessed exclusion mask. |
| Operational scenario | A soft lever shown as a what-if, outside the core score. | `is_scenario_candidate = true`. |
| Reference only | Retained evidence with no executable response. | Assigned in readiness reporting. |

[src: src/nbs_ruralscan/recipe/developer_contract.py] [src: src/nbs_ruralscan/runtime/categorical.py] [src: methodology/T4_developer_contract.md §Reconciled implementation readiness]

Gate inputs are not MCDA criteria; their weights are zero. A source's low suitability class is not a legal exclusion, and a favourable-only statement ("suitable above X") does not establish an unsuitable complement. Membership in a global protected-area layer is a screening input; applicable restrictions must be established for the target jurisdiction and intervention, and absence from a global layer is not a completed legal assessment. [src: methodology/T4_developer_contract.md §Planted host and exclusion contracts] [src: methodology/T4_developer_contract.md §Relationship functions and cross-paper harmonisation]

### 7. Standardise each criterion with a membership function

{{attribution:primitives}}

Each criterion is transformed to a 0–1 membership value before combination. The function chosen must reflect the relationship between the variable and suitability. [src: methodology/recipes/water_harvesting.md §5. Normalisation Using Fuzzy Membership Functions]

#### The five inherited function families

The framework inherited five families: increasing sigmoid, linear, Gaussian, generalised bell and inverted (decreasing) sigmoid. The recipe template describes them, and categorical reclassification, as follows. [src: methodology/framework.md §Inherited framework primitives] [src: methodology/recipes/water_harvesting.md §5.1 Recommended membership functions]

**Increasing sigmoid.** For variables where suitability rises with value and saturates.

```formula
S(x) = 1 / (1 + exp(−a × (x − c)))
```

- `x`: raw variable value in its canonical unit.
- `c`: inflection point, the value at which S = 0.5.
- `a`: steepness; larger |a| gives a sharper transition.

[src: methodology/recipes/water_harvesting.md §5.3 Sigmoid parameterisation example] The schema names the two parameters `midpoint` and `slope`. [src: schema/spec.md §Relationship-type reference (`relationship_type` + `relationship_params`)]

**Decreasing (inverted) sigmoid.** For variables where suitability falls with value, implemented as the complement of the increasing sigmoid.

```formula
S_dec(x) = 1 − S(x)
```

- `S(x)`: the increasing sigmoid above, with the same `c` and `a`.

[src: methodology/recipes/water_harvesting.md §5.1 Recommended membership functions] The recipe template's illustrative starting values (runoff depth c = 50 mm, a = 0.05; slope as a decreasing sigmoid with c = 8 %) are explicitly to be calibrated to the study area and are not evidence-derived thresholds. [src: methodology/recipes/water_harvesting.md §5.3 Sigmoid parameterisation example] The template also gives a = −0.4 for slope while defining the decreasing sigmoid as 1 − S, which inverts the curve twice and yields an increasing response; that parameter should not be copied. [src: methodology/recipes/water_harvesting.md §5.1 Recommended membership functions] [src: methodology/recipes/water_harvesting.md §5.3 Sigmoid parameterisation example]

**Linear (min–max).** Used where no non-linear threshold is defensible. The reference script rescales over the observed raster range.

```formula
x′ = (x − min(x)) / (max(x) − min(x))          (increasing)
x′ = 1 − (x − min(x)) / (max(x) − min(x))      (decreasing)
```

- `min(x)`, `max(x)`: minimum and maximum of the variable over the analysed raster.

[src: reference/R/spatMCDA.R] The canonical schema form instead fixes the bounds from evidence: `linear_increasing {unsuitable_min, suitable_max}` rises linearly between the bounds, and `linear_decreasing {suitable_max, unsuitable_min}` falls between them. [src: schema/spec.md §Relationship-type reference (`relationship_type` + `relationship_params`)] The difference matters: min–max scaling is relative to the AOI, so the same raw value receives a different score in a different AOI. Evidence-fixed bounds do not have this property.

**Gaussian and generalised bell.** For variables with an intermediate optimum. The schema parameterises the Gaussian as `{mean, sigma}` and states that it subsumes the older "bell". [src: schema/spec.md §Relationship-type reference (`relationship_type` + `relationship_params`)] The pinned specifications do not state either formula. The only pinned implementations are in the interactive design prototype, which uses:

```formula
G(x) = exp(−(x − m)² / (2 × s²))
B(x) = 1 / (1 + |(x − m) / s|⁴)
```

- `m`: centre (optimum); `s`: width (standard deviation for G, half-width scale for B).
- The bell exponent is fixed at 4 in the prototype.

[src: docs/redesign/00-config.html] Treat these as demonstrator renderings, not the analytical engine (see "Implementation status" below).

**Reclassified categorical.** For categorical inputs (land cover, hydrologic soil group, texture, lithology), each class receives a membership value from expert consensus or evidence priors. [src: methodology/recipes/water_harvesting.md §5.1 Recommended membership functions]

#### The canonical response list

The schema holds one canonical list of response types, which supersedes the earlier "five-function" wording and older names (`binary`, `linear_decay`, `*_fuzzy`). [src: schema/spec.md §Relationship-type reference (`relationship_type` + `relationship_params`)] [src: schema/structure/columns.json]

| `relationship_type` | Parameters | Stated behaviour |
|---|---|---|
| `trapezoidal` | `abs_min, opt_low, opt_high, abs_max` | 1.0 within [opt_low, opt_high], falling to 0 at abs_min and abs_max. `uncertainty_pct` applies a symmetric ± buffer to the limits. |
| `gaussian` | `mean, sigma` | Bell-shaped around an optimum. |
| `linear_increasing` | `unsuitable_min, suitable_max` | Rises linearly between the bounds. |
| `linear_decreasing` | `suitable_max, unsuitable_min` | Falls linearly between the bounds. |
| `sigmoid` | `midpoint, slope` | Smooth monotonic increase. |
| `inverted_sigmoid` | `midpoint, slope` | Smooth monotonic decrease. |
| `threshold` | `threshold, above_is_suitable` | Hard pass or fail. |
| `ranked_classes` | `class_map {value: score}` | Categorical input to 0–1 scores. |
| `piecewise` | `points [[x, y], …]` or numeric `profiles` | User-defined curve, or source band profiles. |

[src: schema/spec.md §Relationship-type reference (`relationship_type` + `relationship_params`)]

A crop-envelope composite (minimum, optimal-low, optimal-high and maximum limits per dimension) is not a base type; it is built from trapezoidal and threshold limits and documented as a composite where used. [src: schema/spec.md §Relationship-type reference (`relationship_type` + `relationship_params`)]

The threshold and piecewise behaviours that the evaluator implements are:

```formula
threshold:  f(x) = 1 if x ≥ t else 0        (above_is_suitable = true)
            f(x) = 1 if x ≤ t else 0        (above_is_suitable = false)
piecewise:  f(x) = linear interpolation through (x_k, y_k); unknown outside [x_1, x_K]
profiles:   f(x) = score of the single interval containing x; unknown if none or more than one
```

- `t`: the threshold; `(x_k, y_k)`: user points ordered by x; an interval has lower and upper bounds, each inclusive or exclusive, and a null bound is open-ended.

[src: src/nbs_ruralscan/runtime/numeric.py] [src: schema/spec.md §Relationship-type reference (`relationship_type` + `relationship_params`)]

#### Ordinal source bands

Many sources report a numeric variable as ordinal classes rather than a curve. These are compiled into `piecewise` profiles that keep the source's full ordinal scale. The approved common scale is very low 0.10, low 0.25, moderate 0.50, high 0.75 and very high 0.90; explicit unsuitable maps to 0 and explicit optimum to 1. These are documented design scores, not calibrated probabilities. [src: methodology/T4_developer_contract.md §Relationship functions and cross-paper harmonisation]

The conventions that protect those scores: never stretch a source's observed subset to fill 0–1; never interpolate across classes or extrapolate beyond reported bounds; leave tails, gaps and conflicting shared boundaries unknown; never fit a smooth curve to a source that reports only classes; and do not manufacture a score-1 band because a curve stops below 1. Distinct source profiles stay separate unless an explicitly approved compatible pool combines them, and a pool or profile requires explicit selection at run time. [src: methodology/T4_generation_method.md §Reviewed numeric class tables] [src: methodology/T4_developer_contract.md §Obvious source completions] [[ch:suitability-synthesis]] gives the pooling rules.

#### Implementation status

The specification is broader than the pinned evaluator. The numeric evaluator executes `threshold` (numeric thresholds only) and `piecewise` (points, profiles and approved pools), and rejects any other numeric type as unsupported. Categorical class maps and eligibility gates are executed by a separate categorical evaluator. `trapezoidal`, `gaussian`, `linear_*`, `sigmoid` and `inverted_sigmoid` are specified and synthesised as parameters, but are not executed by the pinned runtime evaluator. [src: src/nbs_ruralscan/runtime/numeric.py] [src: src/nbs_ruralscan/runtime/categorical.py]

### 8. Reduce correlated criteria

After standardisation, compute pairwise Pearson correlation across all standardised bands, cluster variables with |r| > 0.7 (default, configurable), and keep one representative per cluster: the highest-variance member unless an expert has flagged a primary. Write the cluster log mapping every variable to its representative. [src: methodology/modules/M1_suitability.md §6.3]

The specification names a T4 flag for the expert primary (`is_cluster_default`), but that column is not in the frozen T4 manifest at the pin; a run must record any expert primary in its own configuration. [src: methodology/modules/M1_suitability.md §6.3] [src: schema/structure/columns.json]

The criterion set J and its weights are fixed before evaluation. Do not change J per pixel or renormalise weights over whichever inputs happen to be available. A change in criterion set or group membership requires a newly documented policy. [src: methodology/T4_developer_contract.md §Aggregation baseline and design history] [src: methodology/T4_developer_contract.md §Approved first-pass policy]

### 9. Derive weights

The framework's weighting primitive reconciles an expert prior with objective weights computed from the AOI's data. [src: methodology/framework.md §Inherited framework primitives]

**Expert prior (AHP).** Pairwise comparisons on the Saaty 1–9 scale; the consistency ratio must be below 0.10, otherwise the elicitation is repeated. [src: methodology/recipes/water_harvesting.md §6.1] The Python port derives weights by the row geometric mean and computes consistency as follows.

```formula
w_AHP,i = g_i / Σ_k g_k,      g_i = (Π_j a_ij)^(1/n)
CI = (λ_max − n) / (n − 1)
CR = CI / RI(n)
```

- `a_ij`: pairwise judgement of criterion i over j; `n`: number of criteria.
- `λ_max`: largest eigenvalue of the comparison matrix; `RI(n)`: Saaty's random index for order n.

[src: src/nbs_ruralscan/runtime/mcda.py]

**CRITIC.** Rewards contrast and penalises redundancy, which matters where several layers derive from one elevation model.

```formula
C_j = σ_j × Σ_k (1 − r_jk)
w_CRITIC,j = C_j / Σ_j C_j
```

- `σ_j`: standard deviation of standardised criterion j over pixels.
- `r_jk`: Pearson correlation between criteria j and k.

[src: methodology/recipes/water_harvesting.md §6.2.1 CRITIC (Criteria Importance Through Intercriteria Correlation)] [src: src/nbs_ruralscan/runtime/mcda.py]

**Entropy.** Rewards criteria that vary more across the AOI.

```formula
p_ij = x_ij / Σ_i x_ij
E_j = −(1 / ln n) × Σ_i p_ij × ln(p_ij)
w_Entropy,j = (1 − E_j) / Σ_j (1 − E_j)
```

- `x_ij`: standardised value of criterion j at pixel i; `n`: number of complete pixels.

[src: methodology/recipes/water_harvesting.md §6.2.2 Entropy weighting] [src: src/nbs_ruralscan/runtime/mcda.py]

**Reconciliation.**

```formula
w_obj = mean(w_CRITIC, w_Entropy)
w_final = α × w_AHP + (1 − α) × w_obj
```

- `α ∈ [0, 1]`: share given to the expert prior; default 0.4 (60 % objective, 40 % expert).
- Sensitivity is tested over α ∈ {0.0, 0.2, 0.4, 0.6, 0.8, 1.0}.

[src: methodology/recipes/water_harvesting.md §6.3 Step 3] [src: src/nbs_ruralscan/runtime/mcda.py] [src: methodology/modules/M1_suitability.md §6.4 Weight derivation]

All derivations are written to a weight log (pairwise matrices, consistency ratios, correlation matrices, CRITIC, entropy and final weights) with a sum-to-one check. [src: methodology/modules/M1_suitability.md §4. Outputs] [src: methodology/recipes/water_harvesting.md §6.4 Documentation and reproducibility]

Three cautions follow from the sources:

- If expert weights are absent, the specification allows an AHP matrix to be generated from CRITIC weights (a_ij = w_i / w_j). Such a matrix is perfectly consistent and returns the CRITIC weights, so the "hybrid" then reduces to an objective weighting. [src: methodology/modules/M1_suitability.md §6.4 Weight derivation] [src: src/nbs_ruralscan/runtime/mcda.py]
- Objective weights depend on the spatial extent and shift if the AOI changes; this must be reported. [src: methodology/recipes/water_harvesting.md §7.6 Constraints and limitations]
- Evidence quantities are not runtime weights. Counts of studies using a variable, source-quality weights and within-study relative importance each serve other purposes and must not be promoted to MCDA weights. A runtime weight combines selected criteria in a declared run. [src: methodology/T4_developer_contract.md §Counts, importance and runtime weights]

### 10. Combine into a suitability surface

The current implementation baseline is a **weighted linear combination (WLC) with separate gates and exclusion masks**. [src: methodology/T4_developer_contract.md §Aggregation baseline and design history]

```formula
S(x) = Σ_{j∈J} w_j × f_j(x),      w_j ≥ 0,  Σ_{j∈J} w_j = 1
```

- `J`: the declared eligible criterion set (one representative per cluster), fixed before evaluation.
- `f_j(x)`: membership value of criterion j at location x (step 7).
- `w_j`: final weight of criterion j (step 9 or an approved run policy).

[src: methodology/T4_developer_contract.md §Aggregation baseline and design history] [src: methodology/modules/M1_suitability.md §6.6 Weighted overlay]

Gates and exclusions are evaluated separately from S, with explicit precedence rather than arithmetic multiplication by a mask: [src: methodology/T4_developer_contract.md §Aggregation baseline and design history] [src: methodology/T4_developer_contract.md §Approved first-pass policy] [src: methodology/T4_developer_contract.md §Planted host and exclusion contracts]

1. A known hard exclusion, or a known failure of host eligibility, gives the state **excluded**. Known exclusion dominates unknown inputs.
2. Otherwise, an unknown required gate or an unknown criterion gives the state **unknown**. Unknown is not zero and is not suitable by default; the overlay propagates missing values.
3. Otherwise the cell is **scored** with S(x).
4. A partial host fraction (for example 30 % of the cell is cropland) is retained as a separate layer and never multiplied into S.

Input and score coverage are reported alongside the surface. [src: methodology/T4_developer_contract.md §Aggregation baseline and design history]

**WLC is compensatory; this is a known design tension.** Earlier design text described a non-compensatory limiting-factor minimum for structural suitability, and the recipe template applies a rule-of-minimum Boolean filter for strong limiting factors before WLC. Under WLC a low score on one criterion can be offset by high scores elsewhere. The baseline is recorded as the implementation baseline, not a ratified resolution of every earlier statement, and approved run policies compute a minimum-factor surface as a sensitivity alternative. [src: methodology/T4_developer_contract.md §Aggregation baseline and design history] [src: methodology/recipes/water_harvesting.md §7.1 Aggregation rule] [src: schema/spec.md §T4_RUN]

Exclusion thresholds stated as examples in older text conflict and must not be used as rules: the module specification lists "slope > 35°", citing a recipe section that lists "slopes > 30%" (a different unit), with both described as subpractice-dependent examples. Exclusions come from the current T4 rows and their evidence. [src: methodology/modules/M1_suitability.md §6.5 Structural exclusion masking] [src: methodology/recipes/water_harvesting.md §7.3 Structural exclusion masks] [src: methodology/T4_developer_contract.md §Aggregation baseline and design history]

**Context overrides.** For each location, identify its agro-ecological zone and farming system through T7; for each T4 row, use the `context_overrides` parameters matching that context, else the global parameters. The most-specific-context-wins precedence used for dataset binding also governs overrides. [src: schema/spec.md §Implementation notes] [src: schema/spec.md §BIND]

**Operational scenarios.** Soft levers are shown as what-ifs outside the core score. The sources describe two different mechanisms: the schema notes say toggling a lever off sets its suitability to 1.0 and recomputes; the module specification says the lever's weight is redistributed. The developer contract records that configured 0–1 scenario endpoints are placeholders whose raw-variable scale, direction and combination still need confirmation. A run that reports a what-if must state which mechanism it used. [src: schema/spec.md §Implementation notes] [src: methodology/modules/M1_suitability.md §10. What-if scenarios] [src: src/nbs_ruralscan/recipe/developer_contract.py]

### 11. Test sensitivity

Perturb the final weights N times and report the per-pixel variance of S as the sensitivity layer.

```formula
w′_j = w_j × (1 + u_j),   u_j ~ Uniform(−0.1, 0.1)
w″_j = w′_j / Σ_k w′_k
Var(x) = variance over N runs of Σ_j w″_j × f_j(x)
```

- `N`: number of perturbed runs, default 50; the ±0.1 range is the default scale.

[src: methodology/modules/M1_suitability.md §6.7 Sensitivity analysis] [src: src/nbs_ruralscan/runtime/mcda.py]

This measures sensitivity to weights only. It does not represent uncertainty in membership parameters, data or evidence transfer. The evidence base skews optimistic, so a sensitivity pass is also meant to be run as conservative-versus-optimistic scenarios with a standing caveat. [src: methodology/T4_generation_method.md §6.1 Publication bias & uncertainty (pragmatic)] An `uncertainty_pct` floor of 20 % on ordinal scores is a humility flag, not an estimated confidence interval. [src: methodology/T4_generation_method.md §Reviewed numeric class tables]

### 12. Classify and define the opportunity space

The specification's classification step divides the surface into four classes by quartile or natural breaks (the reference implementation labels them unsuitable, marginal, moderate, highly suitable) and defines the opportunity space as the top two classes. [src: methodology/modules/M1_suitability.md §6.8 Classification & fingerprint extraction] [src: src/nbs_ruralscan/runtime/mcda.py]

Two consequences must be understood before using that mask:

- **Quartile classes are relative to the AOI.** "Highly suitable" means the top quarter of scored cells in this AOI, not an absolute standard. The same cell can change class when the AOI changes.
- **By construction the top two quartile classes contain about half of the scored cells**, whatever the absolute scores. The mask therefore says where suitability is *relatively* higher, not that half the AOI is suitable.

The specification is internally inconsistent here: its purpose section and output table describe five classes (very high, high, moderate, low, excluded) while its classification step and the implementation use four quartile classes. [src: methodology/modules/M1_suitability.md §1. Purpose] [src: methodology/modules/M1_suitability.md §4. Outputs] Cells in an excluded or unknown state should be kept as their own states rather than folded into the lowest class. [src: method:handbook/implement-a-scan.md §2. Run and interpret the first pass]

### 13. Future scenarios

M1 runs once per scenario. Rows with `has_future_projection = true` use `future_dataset_ids` for the scenario instead of `baseline_dataset_id`; all other variables keep their baseline data. A difference raster (future minus baseline suitability) shows where suitability shifts. [src: methodology/modules/M1_suitability.md §9. Climate scenario handling] [src: schema/spec.md §T4]

## What a held numerical calibration means

Three things about a T4 mapping are assessed separately: whether a source used the variable, the direction of the relationship, and whether a numeric calibration is defensible. A claim can pass the first two while the third remains unresolved. [src: methodology/T4_generation_method.md §Directional evidence is distinct from numeric calibration] [src: .agents/skills/extraction_contracts/T4_review_contract.md]

A published class table can be transcribed exactly and still be unsuitable for a recipe: measurement precision, class widths, proxy meaning and context transfer are checked before any numeric use. Unresolved plausibility stays a calibration or transfer hold; raw values and any supported direction are preserved, but nothing is promoted to an executable curve, scores, pooled cut-offs or a hard exclusion. A general "keep" decision on a claim is not numerical approval. [src: .agents/skills/extraction_contracts/T4_review_contract.md §Numeric plausibility gate]

Mechanically, a hold is declared on the mapping as `relationship_params.reviewed_adaptation.numerical_calibration` with `status = held` and a non-empty reason. A malformed hold fails closed. [src: src/nbs_ruralscan/recipe/calibration_requirements.py] Its effects in execution are:

- the numeric evaluator refuses to evaluate the row and reports the hold reason; [src: src/nbs_ruralscan/runtime/numeric.py]
- the developer package lists the hold as a blocker, and the row's readiness is never execution-ready; [src: src/nbs_ruralscan/recipe/developer_contract.py] [src: methodology/T4_developer_contract.md §Reconciled implementation readiness]
- the row's `relationship_type` label (for example `trapezoidal`) does not imply approved breakpoints. [src: method:handbook/read-a-suitability-recipe.md §Check the decision before scoring]

For reporting, a held calibration is **never** a score, never a range presented as a suitability boundary, and never described as "reviewed" in the sense of approved for scoring. The defensible statement is narrower: whether a site lies within a documented use range, with the score left unassigned. [src: method:handbook/read-a-suitability-recipe.md §Check the decision before scoring] [src: AGENTS.md §What is locked]

Readiness states make this visible: `defined` (response or mask interface specified), `provisional` (specified response with unresolved input assumptions), `blocked` (response, continuation or scenario decision needed) and `reference_only` (retained evidence without an executable response). Every state carries `execution_ready = false` in the developer package; raster validation is never inferred. [src: methodology/T4_developer_contract.md §Reconciled implementation readiness]

## Outputs

| Output | Format | Consumer |
|---|---|---|
| Continuous suitability raster | Cloud-optimised GeoTIFF, 0–1, single band | M3, M4, notebooks |
| Classified suitability raster | GeoTIFF, ordinal classes | maps |
| Opportunity-space mask | Boolean GeoTIFF (top classes) | M3 extraction, M4 constraint |
| Opportunity fingerprint table | CSV | summary panel, M6 |
| Sensitivity raster | GeoTIFF, per-pixel variance under weight perturbation | uncertainty section |
| Cluster log | JSON | variable configuration, audit |
| Weight-derivation log | CSV | audit |
| Resolution audit | CSV | audit |
| Run configuration | JSON | reproducibility |

[src: methodology/modules/M1_suitability.md §4. Outputs]

The fingerprint table summarises the opportunity space: total area and area by class, share of country, rural population, smallholder farm count, production value, dominant farming systems, drought exposure and change under the future scenario. [src: methodology/modules/M1_suitability.md §6.8 Classification & fingerprint extraction] Area columns apply only to `area_suitability` families; other product types report their own unit (step 2).

Read the outputs in three pixel states (scored, excluded, unknown) and with their coverage. Preserve all three in maps and summaries. [src: method:handbook/implement-a-scan.md §2. Run and interpret the first pass]

## Worked illustration

**A held calibration.** A site receives 350 mm of rain a year. Can it be scored for bench terraces? Bench terraces belong to the family `water_harvesting__terracing`, an `area_suitability` family. The variable is mean annual precipitation in mm per year. The reviewed mapping considers three source profiles, of which one supports the annual terrace observation: a documented use range of 200 to 600 mm per year for forward-sloping bench terraces. The other two describe a regional scoring model using seasonal rainfall and a different structure. The release records one supporting source and a held numerical calibration. The analyst can report that the site falls within a documented use range for that design and must leave the rainfall suitability score unassigned. [src: method:handbook/read-a-suitability-recipe.md §Find the family and input] [src: method:handbook/read-a-suitability-recipe.md §Check the decision before scoring]

**An approved partial policy.** For planted silvoarable agroforestry, an approved first-pass policy combines slope, soil organic carbon and pH from conditional, regionally derived compatible pools:

{{csv:schema/recipes/agroforestry/T4_run_policy.csv|cols=rule_id,variable_group,group_weight,criterion_weight,aggregation,sensitivity_aggregation,missing_values,gate_policy,applicability}}

Terrain takes half the weight and soil the other half, split equally between organic carbon and pH, giving criterion weights of 0.5, 0.25 and 0.25. Aggregation is WLC with a minimum-factor sensitivity alternative; unknown values propagate; host and legal masks are separate; and transfer to a target country requires a recorded decision. This is a partial terrain-and-soil index, not full biophysical suitability and not a universal transfer. [src: schema/recipes/agroforestry/T4_run_policy.csv] [src: methodology/T4_developer_contract.md §Approved first-pass policy]

The published first-pass notebook built on it uses a 5 km grid for its quick overview. Its default setting skips the host gate (treating every cell as host) and applies no legal exclusions, so its output shows relative terrain-and-soil patterns, not plantable hectares. A national estimate requires a boundary, host-system data, exclusion masks, a supported resolution and resolved applicability. Slope at 5 km is far coarser than its 90 m limit, which is why derive-then-aggregate matters for any area claim. [src: method:handbook/implement-a-scan.md §2. Run and interpret the first pass] [src: schema/registers/VONT_variable_ontology.csv]

## Assumptions and limits

- **Relative, not absolute.** Quartile classes and min–max scaling make results relative to the AOI. Do not compare class maps across AOIs without re-expressing them on fixed membership scores.
- **Compensation.** WLC lets strengths offset weaknesses. Where a single factor is genuinely limiting, the minimum-factor sensitivity surface should be inspected alongside the WLC result.
- **Design scores are not probabilities.** Ordinal scores (0.10 to 0.90) and membership values express a documented convention, not a calibrated probability of success.
- **Specification exceeds implementation.** Smooth response types are specified but not executed by the pinned evaluator; scenario mechanics and the classification scheme have conflicting descriptions; an expert-primary cluster flag is named but not in the manifest.
- **Evidence transfer.** Regionally derived pools are explicit analytical transfers, not globally validated limits. A country code resolves data; it does not approve a response for that country. [src: methodology/T4_generation_method.md §Reviewed numeric class tables] [src: methodology/T4_developer_contract.md §Target country and evidence country are different filters]
- **Optimistic evidence.** Literature maps where practices work; suitable area is likely over-stated. [src: methodology/T4_generation_method.md §6.1 Publication bias & uncertainty (pragmatic)]
- **Data limits.** Coarse global soil and hydrology layers carry large uncertainty; stream extraction from coarse elevation models under-counts small tributaries; land-cover products differ in mosaic landscapes. [src: methodology/recipes/water_harvesting.md §7.6 Constraints and limitations]
- **What feasibility must still do.** Confirm host systems and field boundaries on the ground, establish legal restrictions for the jurisdiction and intervention, confirm tenure, run site-level hydrological or geotechnical assessment where relevant, and calibrate responses for the context. [src: methodology/T4_developer_contract.md §Module boundaries and output meaning]

## Where this is configured

- Families, sub-practices, dominant limiting factors and product types: [[table:FAM]].
- Suitability mappings (dimension, response type, parameters, flags, weights, evidence): [[table:T4]].
- Approved run policies (criterion set, weights, aggregation, gates, missing values): [[table:T4_RUN]].
- Numeric compilation and harmonisation policy for ordinal bands: [[table:T4_NUMERIC_POLICY]].
- Variable units, resolution limits and derive-then-aggregate flags: [[table:VONT]].
- Datasets and context-specific bindings: [[table:T1]], [[table:BIND]]; contexts for overrides: [[table:T7]].
- Evidence behind every mapping: [[table:EV]], [[table:SRC]]; synthesis rules: [[ch:suitability-synthesis]].
