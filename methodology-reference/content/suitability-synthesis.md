---
title: Suitability synthesis: from reviewed evidence to suitability mappings
slug: suitability-synthesis
summary: Re-derive, audit or challenge any T4 suitability mapping, from the evidence units it rests on through weighting, harmonisation and calibration holds to the function a runtime may execute.
sources:
  - methodology/T4_generation_method.md
  - methodology/T4_developer_contract.md
  - methodology/T4_variable_importance.md
  - methodology/weight_normalisation.md
  - .agents/skills/source-command-t4-synthesise/SKILL.md
  - .agents/skills/extraction_contracts/T4_review_contract.md
  - schema/spec.md
  - schema/structure/columns.json
  - schema/lookups/t4_numeric_compilation_policy.csv
  - schema/lookups/crop_scope_policy.csv
  - schema/recipes/agroforestry/T4_run_policy.csv
  - schema/recipes/water_harvesting_conservation/T4_suitability_mappings.json
  - src/nbs_ruralscan/recipe/synthesis.py
  - src/nbs_ruralscan/recipe/support.py
  - src/nbs_ruralscan/recipe/family.py
  - src/nbs_ruralscan/recipe/developer_contract.py
  - src/nbs_ruralscan/recipe/readiness.py
  - src/nbs_ruralscan/recipe/calibration_requirements.py
  - AGENTS.md
  - method:handbook/read-a-suitability-recipe.md
  - evidence:examples/terrace-rainfall/README.md
  - evidence:workflows/recipe_release/README.md
  - evidence:workflows/recipe_release/counts.md
---

## What this chapter covers

A suitability mapping is one row of [[table:T4]]: for one suitability family and one canonical variable, it states how values of a spatial input translate into suitability for that family. This chapter describes how the method turns reviewed evidence units (see [[ch:extraction]] and [[ch:review-and-quality]]) into such rows, and what a mapping does and does not license a runtime to do. [src: schema/spec.md §T4]

The governing rule is that a document is never turned into a threshold in one step. Extraction records what a source says; synthesis combines sources into a mapping; a reviewer signs off; a separate decision selects a function for execution. Every value in a finished row traces the chain row → evidence units → source (tier, page, quote). [src: methodology/T4_generation_method.md §0]

Three things are kept apart throughout, because confusing them is the commonest way to over-claim:

- **A reviewed record**: the evidence unit is a faithful, approved transcription of what the source says.
- **An executable function**: the mapping carries parameters a computer can evaluate.
- **An applicable function**: the function is valid for the target country, system and dataset.

The developer contract states these as three different states and never infers one from another. [src: methodology/T4_developer_contract.md §Purpose and status]

## The paper-first process

The evidence base for suitability is assembled paper by paper, not variable by variable. Each source is read once, and at that single visit every suitability variable it uses and every quantified threshold or class table it reports is captured as page-stamped evidence units. The source's variable list is recorded on its row in [[table:SRC]] (`vars_extracted`). [src: methodology/T4_generation_method.md §3]

The process then runs in four steps. [src: methodology/T4_generation_method.md §3]

1. **Per-paper scan and relationship capture.** One trip through each document, all variables and relationships at once.
2. **Harmonisation.** Each surface name ("gradient", "% slope") is mapped to a canonical [[table:VONT]] variable, keeping the surface name for audit. A variable missing from the ontology is queued for ontology review before it can enter T4.
3. **Prevalence and a separate quality diagnostic.** Literature prevalence is computed per variable (see "Variable selection signals" below).
4. **Synthesis.** Only then does each surviving family × variable pair receive its T4 row.

The paper-first order exists because the earlier variable-first passes extracted one variable at a time against an unaudited draft variable list, which both missed variables a paper used and invited extraction of thresholds out of context. Reading a paper once also lets the same visit serve the effect tables (see [[ch:effect-synthesis]]). [src: methodology/T4_generation_method.md §3]

Synthesis is reasoned **per suitability family**: sub-practices grouped by their shared dominant limiting factor, each with a spatial product type (`area_suitability`, `applicability_zone`, `zonal_linear`, `qualitative_only`). Linear, zonal and qualitative products are never reported as pixel area, because the over-estimate of footprint grows with pixel size. The family schemes are in the practice chapters, for example [[ch:practice-agroforestry]]. [src: methodology/T4_generation_method.md §2.1] [src: methodology/T4_generation_method.md §2.4] [src: AGENTS.md §What is locked]

## Which evidence may enter a row

The synthesiser filters before it weighs. For one family × variable, a unit is set aside, with a recorded reason, when any of the following holds. [src: src/nbs_ruralscan/recipe/synthesis.py §synthesise_t4_row] [src: src/nbs_ruralscan/recipe/family.py §synthesise_family]

| Condition | Disposition |
|---|---|
| `review_state = dropped` | Excluded (`qa_dropped`); the record stays restorable |
| Fixed-form practice-database record (`relationship.type = observed_presence`, for example a WOCAT climate block) | Excluded from support and threshold synthesis (`observed_presence`) |
| `use_role` not `structural_suitability` or `operational_risk` | Excluded (`other_role`) |
| `claim_scope = species_specific` | Routed to the species lane, never a practice row |
| `claim_scope = crop_specific` where the crop-scope policy does not admit it | Routed to the crop lane |
| `evidence_type` not `literature_relationship` or `expert` | Retained for selection only (`selection_only`); may not carry shape-bearing parameters |
| Relationship cannot be decoded | Held as unresolved, with the decoder's reason |

Crop-specific evidence is re-admitted only where [[table:T4]] synthesis is told to by the crop-scope policy, never by code. [src: .agents/skills/source-command-t4-synthesise/SKILL.md §Counts and decisions]

{{csv:schema/lookups/crop_scope_policy.csv|cols=nbs_id,suitability_family_id,allow_crop_scope}}

A blank `suitability_family_id` admits crop-specific evidence for every family of that practice. The agroforestry row admits it only for shaded perennial-crop systems, where the understorey crop's envelope is the practice by design. Species-specific evidence is never re-admitted. [src: schema/lookups/crop_scope_policy.csv] [src: methodology/T4_generation_method.md §5.2]

## Evidence weighting

Each unit carries a weight that combines the quality of its source with how strongly the claim is supported within that source:

```formula
w_u = TIER_W(tier_s) × BASIS_W(basis_u) × G(role_u)^[grey_s]
```

- `w_u`: weight of evidence unit u.
- `tier_s`: `benchmark_tier` of the unit's source s, joined from [[table:SRC]] (never stored on the unit). `TIER_W`: high 1.0, medium 0.6, low 0.35; an unknown tier takes 0.5.
- `basis_u`: the unit's `claim_basis`. `BASIS_W`: `primary_measured` 1.0, `table` 0.9, `modelled` 0.7, `figure_read` 0.6, `expert_assertion` 0.5, `cited_secondary` 0.4; unknown 0.5.
- `G(role_u)`: the grey-literature discount, applied only when the source's category is grey (`[grey_s]` is 1 for a grey source, 0 otherwise).

[src: src/nbs_ruralscan/recipe/synthesis.py §TIER_W, BASIS_W, _weight]

The claim basis does work the tier cannot: a low-tier paper can report a measured threshold while a high-tier paper offers only a second-hand ranking, and the measured threshold should outweigh the echo. [src: methodology/T4_generation_method.md §5.2] [src: methodology/T4_generation_method.md §6]

### The grey-literature discount

Grey literature (WOCAT, CGIAR, FAO, NGO and project reports) is not peer reviewed and tends to state benefits optimistically. Its weight is discounted by claim kind: structural suitability ×0.9, effect claims ×0.4, hazard claims ×0.6, any other role ×0.6. The discount is lightest on suitability because a slope or soil limit is rarely an advocacy claim. Grey sources still count in `n_sources`; the discount only stops them dominating the median. [src: src/nbs_ruralscan/recipe/synthesis.py §GREY_DISCOUNT]

### Lineage de-duplication

Ten papers echoing one original "slope below 15°" are one claim, not ten. Before reconciliation the synthesiser resolves each unit's root origin by following `EV.lineage_of` from evidence ID to evidence ID (or to a source ID) until it reaches a unit with no lineage, or an identifier outside the current pool, which is then treated as the root. A lineage cycle, or a source-level pointer to a source whose own units descend from different origins, stops synthesis with an error rather than letting input order choose a parent. [src: src/nbs_ruralscan/recipe/synthesis.py §_resolve_root_origin] [src: methodology/T4_generation_method.md §6.1]

Exact echoes (same origin, same relationship, same context, same taxon) collapse to one unit, keeping the primary unit and then the highest weight. Distinct bounds or contexts reported by one origin are kept, but they cast a single vote (see below). The collapsed echoes are listed in the synthesis report. [src: src/nbs_ruralscan/recipe/synthesis.py §_t4_claims]

## Harmonising relationship types and parameters

### Relationship types

Every mapping uses one canonical response vocabulary. [src: schema/spec.md §Relationship-type reference]

{{attribution:primitives}}

| `relationship_type` | Parameters | Meaning |
|---|---|---|
| `trapezoidal` | `abs_min, opt_low, opt_high, abs_max` | 1 on the optimal plateau, falling to 0 at the absolute limits |
| `gaussian` | `mean, sigma` | Bell-shaped response around an optimum |
| `linear_increasing` / `linear_decreasing` | `unsuitable_min, suitable_max` | Monotonic linear response |
| `sigmoid` / `inverted_sigmoid` | `midpoint, slope` | Smooth monotonic S-curve |
| `threshold` | `threshold, above_is_suitable` | Pass or fail |
| `ranked_classes` | `class_map` | Categorical input to a 0 to 1 score |
| `piecewise` | `points`, or source-band `profiles` | User-defined curve, or ordinal numeric source profiles |

The existence of a generic evaluator does not justify fitting it to a source: a paper that reports only classes is not given a sigmoid. [src: methodology/T4_developer_contract.md §Relationship functions and cross-paper harmonisation]

Different shapes are not interchangeable. When the decoded units for one family × variable carry more than one relationship type, all of them are held as `mixed_relationship_types` for a human decision and no row parameters are computed. For non-trapezoidal typed relationships (thresholds, class maps, custom curves), the units must agree exactly; any disagreement is held as `conflicting_typed_relationships`. The engine deliberately does not invent a consensus scoring or a consensus hard exclusion. [src: src/nbs_ruralscan/recipe/synthesis.py §synthesise_t4_row]

### Units

A unit's parameters are converted to the variable's canonical unit before reconciliation. Slope percent and degrees convert by the trigonometric identity:

```formula
θ_deg = atan(s_pct / 100) × 180 / π        s_pct = tan(θ_deg × π / 180) × 100
```

- `θ_deg`: slope in degrees. `s_pct`: slope in percent.

Any other mismatch is converted only when [[table:VONT]] declares an explicit conversion rule (multiply or divide by a constant); otherwise the unit is refused and logged. Passing a raw number under the wrong unit label is never allowed, because that is how a buffer width in metres was once synthesised as kilometres, a thousand-fold error. Where the canonical unit is a wildcard and source units differ, all contributions are held. [src: src/nbs_ruralscan/recipe/synthesis.py §_harmonise]

### The weighted median

Trapezoidal parameters are reconciled with a source-balanced weighted median, one parameter at a time:

```formula
v_o = WM({ (x_u, w_u) : u ∈ origin o })        W_o = max_{u ∈ o} w_u
v*  = WM({ (v_o, W_o) : o ∈ origins })
WM(P) = smallest x_(k) in ascending order such that Σ_{i ≤ k} w_(i) ≥ ½ Σ_i w_i
```

- `x_u`: unit u's value for the parameter (for example `abs_max`) after unit harmonisation.
- `v_o`, `W_o`: the vote of independent origin o and its weight (the strongest of its units).
- `v*`: the reconciled parameter.

Each origin thus supplies at most one vote per parameter, so extracting the same paper repeatedly adds no authority. Values of magnitude 1 or more are rounded to one decimal place; smaller values to three significant figures, so that 0.03 km is not rounded to zero. If the reconciled parameters are out of order (for example `opt_low > opt_high`), all contributions are held as `inconsistent_bound_order`. [src: src/nbs_ruralscan/recipe/synthesis.py §_weighted_median, _t4_reconcile, _round]

### Uncertainty from spread

`uncertainty_pct` is derived from disagreement, never asserted:

```formula
U = min(60, max(10, max_k 100 × (max x_k − min x_k) / |v*_k|) + 10·[n_ind < 3] + 10·[all basis ∈ {cited_secondary, expert_assertion}])
```

- `x_k`: contributing values of parameter k; `v*_k`: its reconciled value (parameters with fewer than two values or a zero reconciled value are skipped).
- `n_ind`: number of independent origins contributing.

[src: src/nbs_ruralscan/recipe/synthesis.py §synthesise_t4_row]

The two humility bumps encode the method's publication-bias stance: the literature maps where a practice works, rarely where it fails, so a tight citation-driven cluster must widen uncertainty, not narrow it, and conservative reconciliation is preferred where bias is directional. Funnel plots and trim-and-fill are not used, because thresholds carry no effect sizes or standard errors. For ordinal class scores the resulting floor is a humility flag, not an estimated confidence interval. [src: methodology/T4_generation_method.md §6.1] [src: methodology/T4_generation_method.md §6]

## Context overrides

Where evidence from one context disagrees materially with the global picture, it becomes a context override rather than being averaged away. For trapezoidal rows the engine groups contributions by the unit's context identifier (AEZ by default), reconciles each group with the same weighted median, and emits an override when the group's `abs_max` or `opt_high` differs from the global value by more than 25 % in relative terms. Each override records `context_type`, `context_id`, the group's parameters and the evidence IDs behind it. [src: src/nbs_ruralscan/recipe/synthesis.py §synthesise_t4_row] [src: methodology/T4_generation_method.md §6]

At runtime the pipeline checks `context_overrides` for a matching [[table:T7]] context and falls back to the global parameters when none matches. Dataset choice is refined in parallel through [[table:BIND]], with the most specific context winning; overrides change parameters, bindings change which dataset supplies the variable. [src: schema/spec.md §Implementation notes] [src: methodology/T4_generation_method.md §2.5]

## Ordinal numeric class tables

Most quantitative suitability evidence arrives as ordinal bands ("slope 0–8 % high, 8–15 % moderate, above 30 % unsuitable") rather than smooth curves. These are compiled into `piecewise.profiles`, one profile per source and context, with explicit interval bounds, inclusivity flags, labels, ranks and scores. Null bounds are open-ended and never replaced by invented finite limits. [src: methodology/T4_generation_method.md §6] [src: schema/spec.md §Relationship-type reference]

### Score convention

Class labels map to a declared common scale: very low 0.10, low 0.25, moderate 0.50, high 0.75, very high 0.90; an explicitly unsuitable class is 0 and an explicit optimum is 1. In the current agroforestry policies, marginal, good and very good map to low, high and very high. These are design scores, not empirical calibration and not probabilities. A label without an ordinal meaning ("favourable" with no class) stays unknown. Original ranks, earlier compiler scores (source rank divided by the full scale maximum) and any scores the source reports are retained beside the harmonised score. [src: methodology/T4_generation_method.md §6] [src: methodology/T4_developer_contract.md §Relationship functions and cross-paper harmonisation] [src: schema/spec.md §Relationship-type reference]

The following rules prevent a profile from saying more than its source:

- Never normalise only the observed subset of a scale; a three-class source ending at "high" is complete at 0.75 and is not stretched to 1.
- Equivalent cardinal scales are rescaled only with verified score meaning and declared endpoints, never observed extremes.
- No interpolation between classes and no extrapolation outside reported bounds.
- A boundary shared by two classes with different scores is unknown.
- A favourable-only threshold yields a positive band with an unknown complement, not a hard exclusion.
- A source's low suitability is not a legal exclusion.

[src: methodology/T4_generation_method.md §6] [src: methodology/T4_developer_contract.md §Obvious source completions]

### Pools

Distinct source profiles are preserved within one family × variable row; no source is chosen automatically, and cross-family evidence remains a reference row rather than a rule every family inherits. Profiles may be combined into a **compatible pool** only with an explicit compatibility approval (`pool_id`, `system_id`, `context_id`, `compatibility_approved = true`). Within a pool, step responses are partitioned at every breakpoint and exact endpoint, and a source-quality-weighted median set is computed per cell, with one independent origin receiving one vote. Pools retain source range, eligible and contributing source counts, and weight coverage. A tied median, or a conflict between a zero and a positive score, yields no executable scalar; a combined zero is not a legal or universal exclusion. A runtime must select a pool explicitly. [src: methodology/T4_generation_method.md §6] [src: methodology/T4_generation_method.md §Harmonization policy contract]

Source quality inside a pool uses the same tier × claim-basis × grey weighting described above. Context is an explicit pool-eligibility check, not a numerical context or recency weight. Conflicting values within one origin are unresolved, never counted as several votes. [src: methodology/T4_generation_method.md §Harmonization policy contract]

## The numeric compilation policy

Whether a reviewed numeric record is compiled, and how, is configuration keyed by evidence ID in the numeric compilation policy ([[table:T4_NUMERIC_POLICY]]). Each row names the action (`compile` or `hold`), the source encoding (for example `labelled_ranges`, `reviewed_intervals`, `named_bounds`, `favourable_above`), the declared source unit, the full ordinal scale, an optional permission for a descending range, an applicability note, the reason for any hold and an optional `harmonization` object carrying the score crosswalk and pool assignment. The policy does not override evidence approval, role or species and crop routing. [src: schema/spec.md §Relationship-type reference] [src: methodology/T4_generation_method.md §Harmonization policy contract]

{{csv:schema/lookups/t4_numeric_compilation_policy.csv|cols=evidence_id,nbs_id,action,encoding,input_unit,reason}}

Every reviewed numeric payload must be either compiled or assigned a meaningful reason: source ambiguity, variable mismatch, parameter-choice grid, importance weight, observed site descriptor, unsupported applicability or scope exclusion. Evidence approval alone does not turn a site description or an analytic-hierarchy weight into a response curve. [src: methodology/T4_generation_method.md §6]

A verified continuation of a reviewed source table (a class table split across pages) may be restored as a compiler correction, recorded in the policy with the source checksum and content fingerprints of both extracts. It does not change reviewer approvals or study counts, and it fails closed if content, units or the parent's state change. A function with a known uncompiled continuation is marked partial and cannot be selected. [src: methodology/T4_developer_contract.md §Obvious source completions] [src: methodology/T4_developer_contract.md §One dashboard for inspection]

## Three assessments and the plausibility gate

Each claim is assessed on three independent questions. [src: .agents/skills/extraction_contracts/T4_review_contract.md §Three independent assessments]

1. **Variable use.** Did the source actually use this variable in its suitability calculation? Mention is not use.
2. **Suitability direction.** Does suitability increase, decrease, peak in a range, or respond non-monotonically as the variable increases? This is the direction of suitability, not of an effect.
3. **Numeric calibration.** Are units, class boundaries, endpoint meanings and scores sufficient for an executable function?

A claim can pass the first two while the third remains unresolved. It is then retained, with the calibration gap reported. Direction-only evidence can never create numeric scores, interpolation, exclusion cutoffs or default weights, and a model weight is never substituted for a suitability score. [src: .agents/skills/extraction_contracts/T4_review_contract.md §Three independent assessments]

Before any numeric calibration is proposed, extractors, reviewers and synthesis must also pass a **numeric plausibility gate**. A correctly transcribed class can still be unfit for an executable recipe. The gate records:

- **Measurement and precision**: units, statistic, averaging period, spatial support, class widths and endpoint inclusion, compared with measurement or interpolation uncertainty and temporal variability. If these are unavailable the record says so; no error estimate is invented.
- **Scientific meaning**: what mechanism justifies each transition, distinguishing validated response boundaries from local ranking, quantiles, map-class breaks, expert choice and proxies. Unusually narrow bands, false precision, abrupt jumps, exclusions and missing tails are flagged.
- **Transfer**: the practice, family, climate, region and measurement context in which the rule was derived and tested. Local ordering is not a global monotonic response.
- **Disposition**: source values, concern, justification available, validation missing, and the exact scope of any approval.

[src: .agents/skills/extraction_contracts/T4_review_contract.md §Numeric plausibility gate]

The worked warning in the contract is a regional rainfall table that places moderate suitability between 1,150 and 1,170 mm per year, a band 20 mm wide, built on an interpolated ten-year average. Its regional qualitative direction was retained and its numeric use held. This is not a universal minimum band width: a narrow band can be defensible when mechanism, measurement and validation support it. [src: .agents/skills/extraction_contracts/T4_review_contract.md §Numeric plausibility gate]

The gate cuts both ways. Regional origin alone is not a plausibility defect, and a published numeric table is not reduced to direction-only evidence merely because transfer needs synthesis. Complete quantitative source profiles are retained for comparison with compatible independent studies; source retention and executable calibration are separate decisions. [src: .agents/skills/extraction_contracts/T4_review_contract.md §Retain complete quantitative source recommendations]

## "Numerical calibration held" and "not recorded"

A mapping-level calibration decision is carried in `relationship_params.reviewed_adaptation.numerical_calibration`. When its `status` is `held`, the record must carry a non-empty `reason`; the compiler fails closed on a malformed hold. A held mapping keeps the reviewed source profiles, their dispositions, locators and quotes, but carries **no approved breakpoints and no score**. Its implementation state is `blocked`, with the stated reason "Numerical calibration held", and resolving the hold is a method decision, not a data task. [src: src/nbs_ruralscan/recipe/calibration_requirements.py §calibration_requirement] [src: src/nbs_ruralscan/recipe/readiness.py §assess]

"Not recorded" is what the published recipe index shows when a mapping has no mapping-level numerical-calibration decision at all. It is not an approval: it means no reviewer has recorded whether the numbers may be used, and the reader must check selection and readiness separately. [src: evidence:workflows/recipe_release/recipe_index.py §table_cells] [src: evidence:workflows/recipe_release/README.md §Browse and reproduce the recipe index]

Neither state is ever a score, a range or "reviewed". The method's invariant is that held or unrecorded calibration stays out of executable recipes, because a runtime that read the retained source classes as a response would silently transfer a regional, possibly implausible, rule into a target country. [src: AGENTS.md §What is locked] [src: .agents/skills/extraction_contracts/T4_review_contract.md §Numeric plausibility gate]

The terrace rainfall example shows the consequence. The mapping `water_harvesting__terracing__annual_precipitation` considers three source profiles: a regional watershed model scoring October to April rainfall, a stone-line manual describing a different structure, and one manual page documenting forward-sloping bench terraces in places receiving 200 to 600 mm per year. Only the last supports the annual terrace observation, so `n_sources = 1` and calibration is `held`. At a site with 350 mm per year an analyst may report that the site lies within a documented use range, and must leave the rainfall suitability score unassigned. [src: schema/recipes/water_harvesting_conservation/T4_suitability_mappings.json] [src: method:handbook/read-a-suitability-recipe.md §Check the decision before scoring] [src: evidence:examples/terrace-rainfall/README.md §Follow the inputs]

## Function options, the selected function and function role

The compiler publishes, for each mapping, zero or more **function options**: each a machine-readable function (intervals, profile or pool) with its evidence IDs, units, completeness and a content **fingerprint**. A **selected function** is one option chosen explicitly in a selection document, keyed by `mapping_id`, with the `function_id`, its exact fingerprint, the target system, the applicability country, an applicability note and a decision reference. Unknown fields are rejected, and a changed fingerprint invalidates a stale selection. Numeric responses always require an explicit selection; authored gates are taken as authored. Where nothing is selected, the package publishes the options and a blocking reason rather than choosing a convenient first row. [src: methodology/T4_developer_contract.md §Selections, corrections and rebuilds] [src: methodology/T4_developer_contract.md §Reproducible chain]

Each mapping also has a **function role**, its execution role in the scan. [src: methodology/T4_developer_contract.md §Developer table and related files] [src: src/nbs_ruralscan/recipe/developer_contract.py]

| Role | Meaning | Derived when |
|---|---|---|
| `suitability_score` | A numeric response that enters the M1 weighted score | Parameters carry source profiles, or a calibration hold |
| `eligibility_gate` | Host-system eligibility (for example observed cropland or grassland), a gate, not a score | Parameters carry a class map |
| `hard_exclusion` | A legal or physical exclusion mask (protected areas, water, built-up) | Neither of the above, and not a scenario |
| `operational_scenario` | A soft, investment-addressable factor kept outside M1 scoring | `is_scenario_candidate = true` |
| `reference_only` | Retained operational evidence with no executable response | Operational-risk evidence with no configured mapping |

Gates and exclusions are not criteria: their weights are zero, and they are combined by precedence, not by arithmetic. A known exclusion dominates unknown inputs; otherwise an unknown required gate propagates as unknown. A legal gate takes an assessed boolean mask with provenance and coverage; absence from a global protected-area layer is not a completed legal assessment. [src: methodology/T4_developer_contract.md §Planted host and exclusion contracts]

### Implementation readiness and spatial validation

Readiness is derived after compilation into four mutually exclusive states: `defined` (response or mask interface specified), `provisional` (specified response with unresolved input assumptions, such as soil depth preparation), `blocked` (a response, continuation, calibration or scenario decision is needed) and `reference_only`. Every state keeps `execution_ready = false`; no raster validation is inferred. Each row lists its reasons and next actions. [src: methodology/T4_developer_contract.md §Reconciled implementation readiness] [src: src/nbs_ruralscan/recipe/readiness.py §assess]

**Spatial validation** is a separate status: the producer's execution-readiness flag, set only when a function has been checked against its intended spatial inputs and location. The release report counts function options, selected functions and spatially validated mappings separately, and the three overlap. In the pinned candidate release, 20 of 49 T4 mappings have options, 10 have a selected function and none is spatially validated. [src: evidence:workflows/recipe_release/README.md §Interpret the results] [src: evidence:workflows/recipe_release/counts.md]

## `suitability_dimension` and the hard and soft split

Every row carries one of three dimensions, ordered by what does the limiting. [src: schema/spec.md §suitability_dimension]

- `biophysical_constraint`: the natural envelope (climate, terrain, soils). Can the practice establish and persist at all?
- `system_constraint`: the existing land-use or farming system the practice must integrate with. This is where the rule "constrain by observed distribution, not a modelled niche" lives: where a host system's observed extent is mapped (for example MapSPAM or Earth-observation crop maps), it gates applicability, and niche modelling is the fallback.
- `operational_constraint`: implementation feasibility and enabling environment.

[src: methodology/T4_generation_method.md §2.5]

Only **hard exclusions** (legal protected areas, water bodies, urban footprints) act as suitability masks, with `is_scenario_candidate = false`. **Soft, investment-addressable** factors (road and market access, tenure, extension, finance, labour) are operational-risk inputs. Their evidence is extracted with `use_role = operational_risk`, compiled as rows flagged `operational_constraint`, and kept out of the T4 support and selection surface and out of the core M1 weighted score; they serve the M2b operational filter and implementation guidance (see [[ch:m2b-project-risk]] and [[ch:m6-handoff]]). The practical test: if switching the variable off in a what-if scenario is a reasonable policy question, it is soft. [src: AGENTS.md §What is locked] [src: schema/spec.md §Hard vs soft operational decision] [src: methodology/T4_developer_contract.md §Module boundaries and output meaning]

The engine sets `suitability_dimension = operational_constraint` on a synthesised row only when all its contributing units are `operational_risk`; otherwise it emits `biophysical_constraint`, and `system_constraint` rows are authored. [src: src/nbs_ruralscan/recipe/synthesis.py §synthesise_t4_row]

## Variable selection signals

Which variables enter a family's recipe is decided by three signals, kept separate from the response shape: literature prevalence, machine-learning importance and thematic fit. Machine learning ranks importance and is structurally barred from setting parameters. [src: methodology/T4_generation_method.md §6] [src: methodology/T4_generation_method.md §3.1]

```formula
paper_support_pct(V) = 100 × n_sources(V) / corpus_n
quality_weighted_pct(V) = 100 × Σ_{s ∈ S(V)} TIER_W(tier_s) / Σ_{s ∈ C} TIER_W(tier_s)
```

- `n_sources(V)`: distinct source IDs yielding at least one unit for variable V. `corpus_n`: number of sources screened for the family; `C`: that screened set; `S(V)`: the subset supporting V.
- Group prevalence uses the set union of member variables' sources, never a sum.
- `quality_weighted_pct` is a diagnostic, computed only when the complete screened membership and every member's tier are known. An integer corpus count never licenses invented tiers.

[src: src/nbs_ruralscan/recipe/support.py] [src: .agents/skills/source-command-t4-synthesise/SKILL.md §Counts and decisions]

A variable below a soft floor (default 20 %) is flagged `review_low_support` for a recorded inclusion decision, not dropped, because prevalence reflects convention and citation echo as much as importance. Machine-learning importance can rescue it (`include_ml_override`); an unknown denominator yields `review_unknown_support`. Statistical pruning is left to per-area correlation clustering at runtime, which keeps one representative per cluster (see [[ch:m1-suitability]]). [src: src/nbs_ruralscan/recipe/support.py §selection_table] [src: methodology/T4_generation_method.md §6]

Counts serve different purposes and are never interchanged: studies using a variable describe inclusion in a stated cohort; source and lineage weights reconcile responses; within-study importance describes emphasis in one model; a runtime MCDA weight combines criteria in a declared run. None of these is a runtime weight by default. [src: methodology/T4_developer_contract.md §Counts, importance and runtime weights]

## Variable importance within studies

Source models report weights on different scales and variable counts, so raw percentages are not comparable. The convention for comparing them is: [src: methodology/T4_variable_importance.md §Flat-model comparison]

```formula
R_i = w_i / ( Σ_{j=1..N} w_j / N )
```

- `w_i`: the non-negative weight of variable i in a complete model of N comparable variables (the mean includes the target variable). `R_i = 1` is average emphasis, 2 twice average.

For hierarchical models three views are kept: the within-group ratio; the flat whole-model ratio (path product divided by the mean contribution of final inputs); and the primary **hierarchy-adjusted ratio**, the observed path contribution divided by an equal-allocation benchmark that splits equally at each node of the same hierarchy. In the worked example with climate 60 % (two variables) and soil 40 % (four variables, pH 50 % within soil), pH contributes 20 %, its flat ratio is 20 / (100/6) = 1.2 and its hierarchy-adjusted ratio is 20 / 12.5 = 1.6. Missing siblings, unclear nesting or contradictory weight sets prevent a settled ratio. [src: methodology/T4_variable_importance.md §Hierarchical comparison] [src: methodology/T4_variable_importance.md §Three accepted theoretical examples]

When extracted weights are compared across sources they are tagged by basis. A **share** (analytic-hierarchy priority, random-forest normalised importance) sums to 1 across a model; an **intensity** (a tool slider on a fixed scale) is divided by its scale maximum. Shares and intensities are never averaged together. This is an evidence-comparison view, never an MCDA input. [src: methodology/weight_normalisation.md §The rule]

Importance results supply sensitivity alternatives, not defaults: for the declared slope and rainfall comparison, equal weights are the baseline and pooled importance-based weights are sensitivity scenarios. [src: methodology/T4_variable_importance.md §Candidate-weight sensitivity follow-up]

## The run policy

An approved analytical policy for a spatial run is authored per recipe in [[table:T4_RUN]], one row per policy and numeric criterion: `policy_id`, `system`, `output_label`, `variable_group`, `rule_id`, `function_id`, `function_fingerprint`, `group_weight`, `criterion_weight`, `aggregation`, `sensitivity_aggregation`, `missing_values`, `gate_policy`, `applicability` and `decision_reference`. Criterion weights are positive shares summing to their group budget, and group budgets sum to one. Only numeric suitability mappings for the named system may carry weights. Function IDs and fingerprints pin the approved responses; a missing or changed function holds the policy rather than silently selecting a replacement. [src: schema/spec.md §T4_RUN]

The aggregation baseline is a weighted linear combination with separate masks:

```formula
S(x) = Σ_{j ∈ J} w_j × f_j(x)        w_j ≥ 0,  Σ_{j ∈ J} w_j = 1
```

- `J`: the declared eligible criterion set, fixed before evaluation; `f_j(x)`: criterion j's selected response at location x; `w_j`: its policy weight.

J is never changed per pixel and weights are never renormalised over whichever inputs happen to be available. Missing values propagate as unknown; unknown is neither zero nor suitable. A minimum-factor aggregation is run as a sensitivity, because the original design described a non-compensatory limiting-factor minimum while the current implementation is compensatory; the package records both rather than resolving that choice silently. [src: methodology/T4_developer_contract.md §Aggregation baseline and design history] [src: schema/recipes/agroforestry/T4_run_policy.csv]

The first approved policy is a **partial terrain-and-soil index** for planted silvoarable agroforestry: terrain 50 %, soil 50 % split equally between soil organic carbon and pH, using conditional pools derived from regional Indian planted-system models. It is not full biophysical suitability and not a universal transfer; target country remains unset, host eligibility and legal exclusions stay separate gates, and a valid partial host fraction is retained separately, never multiplied into the score. [src: methodology/T4_developer_contract.md §Approved first-pass policy]

## What the developer contract promises a runtime

The developer package is a generated, non-authoritative view of the CSV registers and recipe tables. It promises the following. [src: methodology/T4_developer_contract.md §Reproducible chain] [src: methodology/T4_developer_contract.md §Acceptance and limitations]

1. **Traceability.** One row can be followed from evidence through selected response and dataset to an expected score without reading prose; function intervals are machine-readable, with gaps visible.
2. **Explicit choices.** Function selection, profile or pool, transfer decision, dataset binding and weights are recorded in a decision manifest; unresolved choices are published as blocking reasons.
3. **Separated filters.** The target country (`--country`) resolves dataset bindings; the evidence-country filter (`--evidence-country`) is an exact recorded-label filter. Neither approves ecological transfer, and a typed threshold survives an evidence filter only if all its contributors match.
4. **Parity.** The compiler rebuilds the full corpus and checks it against the audited recipe before any filter is applied; a stale recipe fails the build.
5. **Verification.** Input and output hashes can be checked against a checkout; hash consistency is not research authenticity or a new approval.
6. **Conformance examples.** Small synthetic arrays demonstrate scores, interval boundaries, gaps, host gates, exclusions and weighted output. They are contract tests, not pilot validation.

It does not promise that a regional rule transfers to the pilot country, that a dataset adapter exists, that legal masks are complete, or that the spatial run is ready. Native units, scale and temporal reducers remain null until confirmed against actual asset metadata. [src: methodology/T4_developer_contract.md §Purpose and status] [src: methodology/T4_developer_contract.md §Selections, corrections and rebuilds]

## The synthesis decision record and replay

The interpretation of evidence for one family, variable and context is a recorded decision. Its record pins inputs (registers, bindings, policies, prior recipe and compiler by revision or hash, every candidate evidence ID and locator), the agent run (instructions, ruleset and skill versions, model and settings), the interpretation (how each source was used or set aside, compatibility groups, conversions, endpoints, at least one consequential boundary case) and the decision and output. [src: methodology/T4_generation_method.md §Synthesis decision record]

On identical inputs, the accepted decision is replayed and compared, not re-interpreted; a fresh interpretation is a proposal. If it differs materially, the old and proposed results are shown for the same example sites before the accepted rule is replaced. The terrace rainfall example replays this way from pinned revisions and checks a row digest. [src: methodology/T4_generation_method.md §Synthesis decision record] [src: evidence:examples/terrace-rainfall/README.md §Replay the compiled recipe only]

## Assumptions and limits

- **Scoping, not feasibility.** A mapping states where a family is a candidate for investigation; it does not establish site feasibility. Scoping flags; feasibility validates.
- **Optimistic corpus.** The literature over-represents where practices succeed. The method widens uncertainty and prefers conservative reconciliation but applies no statistical bias correction.
- **Regional rules.** Most numeric profiles derive from regional models. Pools are explicit analytical transfers, not globally validated limits, and the target country remains an open decision in every selection.
- **Design scores.** The ordinal score convention and the 25 % override threshold are design conventions, not calibrated quantities.
- **Weights.** Tier, basis and grey weights are defaults; a different reasonable choice can move a weighted median between adjacent source values.
- **Compensation.** The weighted linear baseline lets a high score offset a low one; the minimum-factor sensitivity exists to expose that.
- **No spatial validation yet.** At the pinned release no mapping is spatially validated. Any run must still confirm target applicability, input units and depth, selected representatives, host data and the applicable legal rules.
- **Held calibration.** Many mappings carry a held calibration. They contribute documented ranges and directions, not scores.

## Where this is configured

- [[table:T4]]: mappings, `relationship_params` (profiles, pools, `reviewed_adaptation`), dimensions, overrides.
- [[table:T4_NUMERIC_POLICY]]: per-evidence compile or hold decisions and harmonisation.
- [[table:T4_RUN]]: approved run policies, criterion sets and weights.
- [[table:EV]], [[table:SRC]]: evidence units, tiers, categories and lineage.
- [[table:VONT]]: canonical variables, units and conversion rules.
- [[table:FAM]]: families and spatial product types.
- [[table:BIND]], [[table:T1]]: dataset bindings and access metadata.
- [[table:T7]]: contexts for overrides.
- `schema/lookups/crop_scope_policy.csv`: crop-specific admission.
