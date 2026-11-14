---
title: Module 4 - Priority hotspots by multi-criteria decision analysis
slug: m4-hotspots
summary: Standardise priority layers, derive and reconcile weights, combine them into a hotspot surface inside the opportunity space, test its sensitivity, and read what a hotspot does and does not mean.
sources:
  - methodology/modules/M4_hotspots.md
  - methodology/modules/M3_characterisation.md
  - methodology/modules/M1_suitability.md
  - methodology/modules/M2_climate_risk.md
  - methodology/modules/M2b_project_risk.md
  - methodology/framework.md
  - methodology/recipes/water_harvesting.md
  - methodology/weight_normalisation.md
  - methodology/T4_variable_importance.md
  - methodology/opportunity_space_T5.md
  - reference/R/spatMCDA.R
  - src/nbs_ruralscan/runtime/mcda.py
  - src/nbs_ruralscan/runtime/scorecard.py
  - schema/T5_opportunity_space.csv
  - schema/spec.md
  - AGENTS.md
  - method:handbook/implement-a-scan.md
---

## Question this module answers

Module 4 (M4) answers: within the opportunity space, where do the user's weighted development priorities (climate need, livelihoods, biodiversity, equity) concentrate most strongly, so that investment can be targeted? [src: methodology/modules/M4_hotspots.md §2]

M1 gives the descriptive answer to "where could it work?"; M4 adds the prescriptive layer "where should investment be targeted?". The product is a continuous 0 to 1 priority surface inside M1's opportunity-space mask, a classified version of it, a bivariate suitability-by-priority view, a ranked list of administrative units with their main drivers, and a sensitivity map. [src: methodology/modules/M4_hotspots.md §1]

M4 does not define feasibility (M1), characterise variables (M3, [[ch:m3-characterisation]]), judge whether the investment is durable (M2b, applied here only as a filter) or quantify benefits (M5, [[ch:m5-scorecard]]). [src: methodology/modules/M4_hotspots.md §2]

## Inputs

| Input | From | Notes |
|---|---|---|
| Opportunity-space mask | M1 | M4 runs only inside it. |
| Standardised priority layers | M3 | One 0 to 1 layer per cluster representative; clustering done in M3. |
| Priority rules | [[table:T5]] | Normalisation method, direction, theme, default weight. Filter to `mcda_role = priority`. |
| User weights | Run configuration | Per priority: none, low, medium or high. |
| Project-risk rating (optional) | M2b | A scope filter only, never an MCDA term. |
| Geographic context | [[table:T7]] | Administrative and agro-ecological units for ranking. |

[src: methodology/modules/M4_hotspots.md §3] [src: methodology/modules/M4_hotspots.md §13]

Descriptor rows never enter the stack. [src: methodology/modules/M4_hotspots.md §13] A priority whose data resolve only to national level for the AOI carries a qualified flag and does not drive differentiation within the country (the spatial-grain rule in [[ch:m3-characterisation]]). [src: methodology/opportunity_space_T5.md §Spatial-grain rule]

## Method

The steps follow the module specification. [src: methodology/modules/M4_hotspots.md §6]

### Step 1. Take in and check the priority layers

Load M3's standardised layers clipped to the mask and confirm each was standardised under its declared rule (method, direction, reference frame). M3 performs the standardisation; M4 validates it and records it verbatim in the run metadata. [src: methodology/modules/M4_hotspots.md §6] [src: methodology/modules/M3_characterisation.md §13]

### Step 2. Standardisation and the reference frame

Priority variables have no universal optimum, so how each is rescaled to 0 to 1 **defines what a hotspot means**. The rule is declared per variable in T5, never hard-coded. [src: methodology/modules/M4_hotspots.md §9]

Two families of method are allowed:

- **Fixed (absolute)** maps raw values against externally justified breakpoints, for example Integrated Food Security Phase Classification (IPC) phases, SPEI drought classes or a poverty line. It is comparable across AOIs and over time, but needs a referenced standard.
- **Statistical (relative)** ranks a value within a distribution. Percentile (quantile) ranking is preferred to min-max scaling because it is less sensitive to outliers. It requires a declared reference frame. [src: methodology/modules/M4_hotspots.md §9]

```formula
min-max, higher is more concern:   p = (x − x_min) / (x_max − x_min)
min-max, lower is more concern:    p = 1 − (x − x_min) / (x_max − x_min)
percentile:                        p = F_R(x) = (number of cells in R with value ≤ x) / N_R
clip (optional):                   x ← min(max(x, q_lo), q_hi) before scaling
```

`x` is the raw value in a cell; `x_min` and `x_max` are the minimum and maximum over the reference frame; `p` is the standardised priority in [0, 1]; `F_R` is the empirical cumulative distribution over reference frame `R`, which contains `N_R` valid cells; `q_lo` and `q_hi` are clip bounds such as low and high percentiles. The min-max form, including the inversion for "lower is more concern", is the pattern of the reference implementation. [src: reference/R/spatMCDA.R §4 STANDARDIZATION] The percentile and clip forms are not specified by the method; they are the standard forms and need confirmation before use.

The reference frame is the population a value is ranked against: the AOI (the default, meaning "highest need within this country"), a sub-national region, the global distribution of the dataset, or a fixed historical baseline. A narrow frame gives full 0 to 1 contrast but is purely relative; a global frame is comparable across AOIs but may give little internal contrast. [src: methodology/modules/M4_hotspots.md §9]

**Ratified default:** percentile within the AOI, labelled as relative, shown beside the raw value and a fixed reference band so relative contrast is not misread as absolute severity. Fixed thresholds are used wherever a credible standard exists. [src: methodology/modules/M4_hotspots.md §9] [src: methodology/modules/M4_hotspots.md §14]

The pinned T5 table does not yet reflect this default: every row carries `normalisation_method = minmax`, and the table has no reference-frame or clip column. [src: schema/T5_opportunity_space.csv] The field-level spec lists `percentile_clip`, `log_transform` and `none` as further allowed methods. [src: schema/spec.md §T5 - Opportunity Space Variables] An implementation must therefore declare the method and frame per variable in its run configuration and record them.

Priority scoring uses monotonic rescales, not the five fuzzy membership functions of M1. Priority is a need score, not a fitness score, so it should rise steadily with need rather than peak at an optimum. [src: methodology/modules/M4_hotspots.md §9]

### Step 3. Turn user priorities into weights

The user sets each priority to none, low, medium or high. These are conceptual ordinal settings, not arithmetic precision. The default mapping is 0, 1, 2, 3, normalised to sum to 1, and in the default configuration these weights are used directly. [src: methodology/modules/M4_hotspots.md §6] [src: methodology/modules/M4_hotspots.md §14]

```formula
w_j = c_j / Σ_k c_k ,   c_j ∈ {0, 1, 2, 3}
```

`c_j` is the numeric code for the user's setting on priority `j` (none 0, low 1, medium 2, high 3); the sum runs over all priorities in the stack; priorities set to none drop out.

T5 also carries default weights organised by theme. `weight_default` is the weight of a variable **within its theme**, the weights within a theme normalise to 1, and a separate set of theme weights says how much each theme drives the index. The product of the two gives a variable's default contribution before the user reweights. [src: schema/spec.md §Theme weights and NbS-response layers]

```formula
w_j = θ_t(j) × d_j / Σ_{k ∈ t(j)} d_k
```

`d_j` is the T5 `weight_default` of variable `j`; `t(j)` is its theme; the inner sum runs over the active variables in that theme, which renormalises them to 1 (needed because, for example, the five `nbs_response` rows at the pin carry 0.25 each); `θ_t` is the theme weight, with Σ θ_t = 1 over the priority themes. [src: schema/T5_opportunity_space.csv] The specification says only that the two weights are multiplied; the written form, including the within-theme renormalisation, is not specified by the method; it is the standard form and needs confirmation before use.

The theme weights are not settled. The spec states a default of 0.20 for each of five themes, but names the pre-ratification themes (including `infrastructure`, since dropped, and `equity_gender`, since renamed), and the lookup it refers to does not exist at the pin. [src: schema/spec.md §Theme weights and NbS-response layers] Because one theme (`context`) is descriptor-only, four priority themes remain; equal theme weights of 0.25 would be the consistent reading, but no pinned file states it. Treat the theme weights as a run-configuration choice and record them.

### Step 4. Derive and reconcile weights: hybrid AHP + CRITIC + Entropy

The weighting engine is shared with M1 and is the inherited framework scheme.

{{attribution:primitives}}

M4 may reconcile the user's weights with an Analytic Hierarchy Process (AHP), CRITIC and Entropy prior, reusing the M1 engine. In the default configuration this step is off and the user's weights are used directly. [src: methodology/modules/M4_hotspots.md §6] The method is a hybrid: subjective (AHP) weights structure the problem and record the rationale; objective weights (CRITIC and Entropy) adjust them to the information content and contrast of the actual layers in the AOI. [src: methodology/recipes/water_harvesting.md §6]

**AHP.** Pairwise judgements on the Saaty 1 to 9 scale form a reciprocal matrix `A`. Weights come from the row geometric means; consistency is checked by the consistency ratio. [src: methodology/recipes/water_harvesting.md §6.1] [src: src/nbs_ruralscan/runtime/mcda.py §ahp_weights]

```formula
g_i = ( Π_{j=1..n} a_ij )^(1/n)
w_AHP,i = g_i / Σ_k g_k
CI = (λ_max − n) / (n − 1)
CR = CI / RI_n ,   accept if CR < 0.10
```

`a_ij` is the judged importance of criterion `i` relative to `j` (with `a_ji = 1/a_ij`, `a_ii = 1`); `n` is the number of criteria; `λ_max` is the largest eigenvalue of `A`; `RI_n` is Saaty's random index for order `n` (0.58, 0.90, 1.12, 1.24, 1.32, 1.41, 1.45, 1.49 for n = 3 to 10; the implementation uses 1.49 above 10). If CR ≥ 0.10 the elicitation is repeated. [src: src/nbs_ruralscan/runtime/mcda.py §ahp_consistency_ratio] [src: methodology/recipes/water_harvesting.md §6.1]

Where no expert matrix is supplied, a perfectly consistent matrix can be generated from the CRITIC weights, `a_ij = w_CRITIC,i / w_CRITIC,j`. [src: reference/R/spatMCDA.R §8] [src: methodology/modules/M1_suitability.md §6.4] Such a matrix has CR = 0 by construction and simply returns the CRITIC weights, so it adds no subjective information.

**CRITIC** (Criteria Importance Through Intercriteria Correlation; Diakoulaki, Mavrotas and Papayannakis 1995) rewards criteria with high contrast and low redundancy. [src: reference/R/spatMCDA.R §6] [src: methodology/recipes/water_harvesting.md §6.2.1]

```formula
C_j = σ_j × Σ_k (1 − r_jk)
w_CRITIC,j = C_j / Σ_k C_k
```

`σ_j` is the standard deviation of standardised criterion `j` over valid cells; `r_jk` is the Pearson correlation between criteria `j` and `k` (the `k = j` term contributes zero). Cells with any missing criterion are dropped first. [src: src/nbs_ruralscan/runtime/mcda.py §critic_weights]

**Entropy** (Shannon) gives more weight to criteria whose values vary more across the study area. [src: methodology/recipes/water_harvesting.md §6.2.2]

```formula
p_ij = x_ij / Σ_i x_ij
E_j = −(1 / ln m) × Σ_i p_ij × ln(p_ij)
w_Entropy,j = (1 − E_j) / Σ_k (1 − E_k)
```

`x_ij` is the standardised value of criterion `j` in cell `i`; `m` is the number of valid cells; `p_ij` is the share of criterion `j`'s total held by cell `i`; `E_j` is its normalised entropy (1 for a perfectly even spread, which carries no discriminating information). [src: methodology/recipes/water_harvesting.md §6.2.2] [src: src/nbs_ruralscan/runtime/mcda.py §entropy_weights]

**Reconciliation.** The final weight is a convex combination of subjective and objective weights. [src: methodology/recipes/water_harvesting.md §6.3] [src: src/nbs_ruralscan/runtime/mcda.py §reconcile_weights]

```formula
w_obj = (w_CRITIC + w_Entropy) / 2
w_final = α × w_AHP + (1 − α) × w_obj ,   α ∈ [0, 1],  α = 0.4 by default
w_final ← w_final / Σ w_final
```

`α` is the weight given to the expert (AHP) vector; the default 0.4 means 60% objective and 40% expert. [src: methodology/modules/M1_suitability.md §6.4] If only one objective vector is supplied, `w_obj` is that vector; if no AHP vector is supplied, `w_final = w_obj`. Each input vector must already sum to 1. [src: src/nbs_ruralscan/runtime/mcda.py §reconcile_weights] The inherited plan recommends testing α over {0.0, 0.2, 0.4, 0.6, 0.8, 1.0} and lists alternatives: reporting CRITIC and Entropy surfaces in parallel, using AHP only to structure the problem, or using AHP weights as priors in a constrained optimisation. [src: methodology/recipes/water_harvesting.md §6.3] Every derivation is written to a weight log: pairwise matrices, consistency ratios, correlation matrices and the final weights. [src: methodology/recipes/water_harvesting.md §6.4] [src: methodology/modules/M4_hotspots.md §4]

**Sources differ on the Entropy step.** The inherited plan and the Python port normalise each criterion over cells (`p_ij = x_ij / Σ_i x_ij`, a column share). The reference R script normalises each cell over criteria (`vals / rowSums(vals)`, a row share), which measures something different. The R script also uses the sample standard deviation in CRITIC where the port uses the population form, a negligible difference at raster sample sizes. This chapter follows the plan and the port. [src: reference/R/spatMCDA.R §7] [src: methodology/recipes/water_harvesting.md §6.2.2] [src: src/nbs_ruralscan/runtime/mcda.py §entropy_weights]

### Step 5. Combine: weighted linear overlay

Inside the opportunity space, the hotspot score is the weighted sum of standardised priorities, then rescaled to 0 to 1. [src: methodology/modules/M4_hotspots.md §6]

```formula
H(c) = Σ_j w_j × p_j(c) ,   for every cell c inside the opportunity-space mask
H(c) = undefined outside the mask
```

`p_j(c)` is the standardised value of priority `j` in cell `c`; `w_j` are the final weights with Σ w_j = 1. Because each `p_j` lies in [0, 1] and the weights sum to 1, `H` already lies in [0, 1]; the specification adds a renormalisation without stating its form, so any renormalisation of H written into a run is not specified by the method and needs confirmation before use. If it is a min-max stretch within the mask, the result becomes purely relative to the AOI and should be labelled so. [src: methodology/modules/M4_hotspots.md §6] [src: src/nbs_ruralscan/runtime/mcda.py §weighted_overlay]

Weighted linear combination is compensatory: a high value on one priority can offset a low value on another. That is the intended behaviour for a concentration-of-need index, but it means a hotspot can be driven by one dominant priority. The ranked-unit table (Step 8) exposes this.

### Step 6. Apply the project-risk scope (optional)

If M2b is active, high and very-high project-risk cells are flagged by default, or excluded if the user chooses. The rating is applied as a mask and **never summed into H**. [src: methodology/modules/M4_hotspots.md §6] [src: methodology/modules/M4_hotspots.md §14] Because it is never an MCDA term, M2b may share hazard variables with M1 or M4 without double counting: it is a check, not an addend. [src: methodology/modules/M4_hotspots.md §7] [src: methodology/modules/M2b_project_risk.md §7] See [[ch:m2b-project-risk]].

Climate risk to livelihoods (M2) may enter M4 as a priority layer. Its constituent vulnerability variables must not also be standalone priorities; the double-count guard enforces this. [src: methodology/modules/M4_hotspots.md §7] [src: methodology/modules/M2_climate_risk.md §5] The sources differ on form: the module's resolved decision says M2 enters as one composite hazard-exposure layer, while the pinned T5 table carries drought, flood and heat stress as three separate `climate_hazard` priorities. [src: methodology/modules/M4_hotspots.md §14] [src: schema/T5_opportunity_space.csv] A run should use one form, not both.

The user-facing scopes (which suitability classes count as opportunity space, which hotspot classes to display, project-risk scope) subset the view and never reweight the MCDA. [src: methodology/modules/M4_hotspots.md §8]

### Step 7. Bivariate view

Bin suitability (M1) and priority (H) into classes and combine them into a 5 by 5 palette, so a user sees high-suitability, high-priority cells distinctly from high-suitability, low-priority ones. [src: methodology/modules/M4_hotspots.md §6]

```formula
B(c) = 5 × (s(c) − 1) + h(c) ,   s, h ∈ {1, ..., 5}
```

`s(c)` and `h(c)` are the suitability and priority classes of cell `c`; `B` is a single code from 1 to 25. This encoding is not specified by the method (the specification asks only for a "single 1 to 25 code" and does not fix the ordering); it is the standard form and needs confirmation before use. [src: methodology/modules/M4_hotspots.md §13]

### Step 8. Classify, rank and fingerprint

Classify H into five classes (Low to Very High). [src: methodology/modules/M4_hotspots.md §1] [src: methodology/modules/M4_hotspots.md §4] Aggregate to administrative units by mean score or share of hotspot area, and for each unit report its top three drivers by weighted contribution. [src: methodology/modules/M4_hotspots.md §6] [src: methodology/modules/M4_hotspots.md §13]

```formula
H_u = mean of H(c) over cells c in unit u
D_uj = w_j × mean of p_j(c) over cells c in unit u
```

`H_u` is the unit's hotspot score; `D_uj` is the contribution of priority `j` to it (Σ_j D_uj = H_u before any renormalisation). The specification says only "mean/share" and "weighted contribution to the unit mean"; these two forms are not specified by the method; they are the standard forms and need confirmation before use. The three largest `D_uj` are the unit's drivers. Build the intersection fingerprint (people, production and poverty in suitability ∩ hotspot cells) for the same units. [src: methodology/modules/M4_hotspots.md §4]

The classification breaks are not fully fixed. The reference implementation and its port classify by quartiles into four classes; the M4 specification asks for five classes and a 5 by 5 bivariate grid. [src: src/nbs_ruralscan/runtime/mcda.py §quartile_classify] [src: methodology/modules/M4_hotspots.md §4] Quantile classes are themselves relative: by construction each holds the same share of cells, so "Very High" means "top fifth in this AOI", not a severity threshold.

### Step 9. Sensitivity

Perturb the weights and recompute the overlay to show where the result depends on the exact weights. [src: methodology/modules/M4_hotspots.md §6]

```formula
w_j^(r) = w_j × (1 + u_j^(r)) ,   u_j^(r) ~ Uniform(−s, s)
w^(r) ← w^(r) / Σ_j w_j^(r)
H^(r)(c) = Σ_j w_j^(r) × p_j(c) ,   r = 1, ..., R
sensitivity(c) = variance over r of H^(r)(c)
```

`s` is the perturbation scale (0.10 by default, so ±10%); `R` is the number of runs (50 by default); the output is a per-cell mean and variance, plus the minimum and maximum weight each criterion took. [src: src/nbs_ruralscan/runtime/mcda.py §sensitivity_perturb] [src: methodology/modules/M1_suitability.md §6.7] The reference R script performs a single perturbed run with a fixed seed; the port generalises it to many. [src: reference/R/spatMCDA.R §11]

A ±10% weight perturbation is a narrow test. It does not explore the different conceptual settings a user might reasonably choose. The scoping brief should therefore also be repeated with plausible alternative weight settings and record which priorities or assumptions change the ranking. [src: method:handbook/implement-a-scan.md §3. Build the scoping brief]

## What a hotspot is, and is not

A hotspot **is** a place, inside the area where a practice could establish, where the priorities the user chose concentrate most strongly relative to the rest of the AOI, under declared standardisation rules and weights.

A hotspot **is not**:

- **a feasibility finding.** It is downstream of a scoping-grade suitability mask; land availability, tenure, safeguards and design are checked later (see [[ch:m6-handoff]]);
- **a statement of absolute severity.** Under the default AOI percentile frame, a "Very High" cell in a low-need country may be less severe than a "Low" cell elsewhere. The raw value and a fixed reference band are shown alongside for that reason [src: methodology/modules/M4_hotspots.md §9];
- **a place where the practice will deliver most.** The hotspot weights describe need. T6 effect evidence never changes them. The user may switch on an optional filter that keeps only the priorities the practice is evidenced to improve: those with a positive effect class at medium confidence or better. [src: src/nbs_ruralscan/runtime/scorecard.py §build_nbs];
- **a risk-adjusted score.** Project risk is a separate filter, never part of H.

## Literature weights are benchmarks, not inputs

Weights extracted from published models arrive in incompatible encodings, such as AHP priorities, random-forest importances and tool sliders. The method compares them across sources but never injects them into the MCDA, which computes its own weights at run time. [src: methodology/weight_normalisation.md §Scope - evidence, not an MCDA input] Two bases must not be averaged together: a **share** (a fraction of a source's total importance, summing to 1 across its variables) and an **intensity** (a value on a fixed scale set independently per variable, normalised as value divided by scale maximum). [src: methodology/weight_normalisation.md §The rule - two bases that must NOT be averaged together]

For within-study comparison the method uses relative importance against the model's mean weight:

```formula
R_i = w_i / ( Σ_{k=1..N} w_k / N )
```

`w_i` is the source's weight for variable `i` and `N` the number of variables in that complete model; `R_i = 1` is average emphasis, 2 is twice average. Hierarchical models also get a hierarchy-adjusted ratio against an equal-allocation benchmark down the same tree. [src: methodology/T4_variable_importance.md §Flat-model comparison] [src: methodology/T4_variable_importance.md §Hierarchical comparison] These diagnostics measure emphasis within a model, not predictive accuracy, and no runtime weight changes follow from them. [src: methodology/T4_variable_importance.md §Hierarchical comparison] They are described with the suitability evidence in [[ch:suitability-synthesis]].

## Outputs

| Output | Grain | How to read it |
|---|---|---|
| Hotspot score | Grid, 0 to 1, inside mask | Relative concentration of weighted need. |
| Classified hotspot | Grid, classes | Display classes; relative under quantile breaks. |
| Bivariate raster | Grid, 25 codes | Suitability against priority. |
| Ranked units | Administrative unit | Score, top drivers, poverty, production and population. |
| Intersection fingerprint | Administrative unit | What lies in suitability ∩ hotspot. |
| Weight log | Per run | Conceptual-to-numeric mapping, AHP, CRITIC, Entropy and final weights. |
| Sensitivity map | Grid | Per-cell variance under weight perturbation. |
| Run metadata | Per run | Weights, reference frames, scopes, double-count decisions, grain flags. |

[src: methodology/modules/M4_hotspots.md §4]

## Assumptions and limits

- **Engine implemented, module not.** The weighting, overlay, classification and sensitivity functions exist as a tested port of the reference script. The hotspot module that uses them (conceptual weights, stack assembly, project-risk scope, bivariate view, unit ranking) is specified as function signatures only at the pin. No hotspot surface has been produced, validated or checked against regional knowledge. [src: methodology/modules/M4_hotspots.md §13] [src: methodology/modules/M4_hotspots.md §12]
- **Objective weights reward contrast, not importance.** CRITIC and Entropy give weight to layers that vary and are uncorrelated in this AOI. For priorities this can raise a noisy layer above a policy-central but spatially smooth one. That is why the user's settings lead and objective weighting is an optional reconciliation.
- **Relative by default.** AOI percentiles and quantile classes make every result relative to the country. The same priority map cannot be compared across countries unless a fixed or global frame is used.
- **Ordinal weights treated as ratio.** The 0 to 3 coding turns ordinal settings into ratios (high is three times low). The source treats this as a convention, not a measurement; sensitivity to alternative codings is not specified.
- **Configuration gaps at the pin:** no reference-frame or clip field in T5; theme weights unlisted; classification count and bivariate encoding inconsistent between specification and engine; M2 entry form (composite or three hazards) unresolved. A run must state its choices.
- **Several priorities need country data**, so a first run may use fewer priorities than the scheme lists ([[ch:m3-characterisation]]).
- **What feasibility must still do:** validate the top-ranked units in the field, confirm the source of every sensitive variable, and test whether the ranking holds under the weights stakeholders actually hold.

## Where this is configured

- [[table:T5]]: priorities, themes, direction, normalisation method and default within-theme weights.
- [[table:T1]] and [[table:BIND]]: datasets and their grain, which decides eligibility.
- [[table:T2]]: the double-count guard against the M2 vulnerability term.
- [[table:T7]]: units for ranking.
- [[table:T3]]: asset-threat rows behind the optional M2b project-risk scope.
- Run configuration: user priority settings, α, reference frames, theme weights, and the perturbation scale and run count, all written to the weight log and run metadata.
