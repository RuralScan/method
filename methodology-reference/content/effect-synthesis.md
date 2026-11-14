---
title: Effect synthesis: hazard responses and scorecard effects
slug: effect-synthesis
summary: Re-derive any T3 hazard-response row or T6 scorecard row from its pooled evidence, including its weights, class, two-axis confidence, applicability envelope and every cap, discount and hold that shaped it.
sources:
  - methodology/T3_T6_generation_method.md
  - methodology/T3_T6_developer_handover.md
  - methodology/RULESET_VERSIONS.md
  - .agents/skills/source-command-t3t6-synthesise/SKILL.md
  - schema/spec.md
  - schema/structure/columns.json
  - schema/lookups/design_weights.csv
  - schema/lookups/ipcc_confidence_matrix.csv
  - schema/lookups/effect_locus.csv
  - schema/lookups/comparator_policy.csv
  - schema/lookups/family_rollup_policy.csv
  - schema/lookups/xw_route_policy.csv
  - schema/lookups/crop_scope_policy.csv
  - schema/registers/XW_target_crosswalk.csv
  - schema/registers/BANDS_magnitude_bands.csv
  - schema/recipes/water_harvesting_conservation/T3_nbs_hazard_farming.json
  - src/nbs_ruralscan/recipe/cell_synthesis.py
  - src/nbs_ruralscan/recipe/synthesis.py
  - src/nbs_ruralscan/recipe/t3t6_build.py
  - AGENTS.md
---

## Why effects are synthesised by cell

[[table:T3]] records how a practice responds to each climate hazard: whether it reduces the losses a hazard causes to rural livelihoods (`risk_role = livelihood_mitigation`, read by M2) and how badly the hazard damages the practice itself (`risk_role = asset_threat`, read by M2b). [[table:T6]] records how strongly a practice improves each priority of the opportunity space (rural poverty, food insecurity, biodiversity, carbon, erosion, water, gender, hazards). Cost rows sit in [[table:T6E]] and are covered in [[ch:cost-profiles]]. [src: methodology/T3_T6_developer_handover.md §1] [src: schema/spec.md §T3] [src: schema/spec.md §T6]

These rows are **generated**, never extracted as rows from a paper. An earlier attempt asked each paper to yield a finished row. The quotes were real, but the numbers had incompatible denominators (Hedges' *g*, net present value per acre, benefit-cost ratios, project budget lines with no unit), context was recorded under many spellings, outcomes had no mapping to what the consumers key on, and one Swedish boreal cost figure sat as an equal beside a Sahelian yield claim. The method therefore keeps the verbatim evidence unit and changes the unit of output: pool every evidence unit that hits a table **cell**, reconcile deterministically, and emit one row per cell per applicability scope with its evidence IDs and a confidence expressed in IPCC calibrated language (not a statistically calibrated probability). [src: methodology/T3_T6_generation_method.md §0] [src: AGENTS.md §What is locked]

Five tenets follow. [src: methodology/T3_T6_generation_method.md §0]

1. **Ordinal first.** The value is a direction, a strength class and a confidence expressed in IPCC calibrated language (not a statistically calibrated probability). Numbers appear only under explicit gates.
2. **Context bounds applicability.** Every row carries the envelope of contexts its evidence came from and a transfer class against the investment target. A row built from high-income temperate evidence never silently sets a value for a low-income dryland.
3. **Role is the kind of claim; the crosswalk decides the table.** One unit can feed both T3 and T6.
4. **Reuse the suitability engine.** Tier and claim-basis weights, lineage de-duplication, the weighted median and the grey discount are imported from the suitability synthesiser (see [[ch:suitability-synthesis]]).
5. **Confidence is derived, never asserted.** No person and no model writes a confidence level.

The engine is deterministic: the same register produces byte-identical rows. [src: src/nbs_ruralscan/recipe/cell_synthesis.py]

## What a cell is

| Table | Cell key | Notes |
|---|---|---|
| T3 | `nbs_id` × `hazard_type` × `farming_system` | `farming_system = all` is the universal row; a named system refines it. Hazards: `drought`, `flood`, `heat_stress`, `fire`, `wind_cyclone`, `waterlogging`. |
| T3 asset threat | `nbs_id` × hazard (asset-threat cell) | Distinct from the mitigation cell of the same hazard. |
| T6 effect | `nbs_id` × `variable_id` (a [[table:T5]] row with `mcda_role = priority`) | `variable_type = climate_hazard_mitigation` for hazard priorities, otherwise `opportunity_space_variable`. Descriptor rows get no T6 row. |
| T6E economic | `nbs_id` × `economic_indicator_type` | See [[ch:cost-profiles]]. |

[src: methodology/T3_T6_generation_method.md §2.1] [src: schema/spec.md §T3] [src: schema/spec.md §T6]

Frost is excluded from T3 for every practice; frost-tagged units stay in the register and still feed T6. Erosion is not a T3 hazard; erosion reduction is the T6 priority `soil_erosion_risk`. [src: src/nbs_ruralscan/recipe/cell_synthesis.py §EXCLUDED_T3_HAZARDS] [src: schema/spec.md §T3]

A cell holds several layered rows: the **roll-up row** for the whole practice (`suitability_family_id` blank), **family rows** for sub-practice families, the **global row** (`scope_type` blank, reconciled for the investment target) and **scope rows** for particular contexts. Record IDs follow `<nbs>[__<family>]__<cell>[__<scope_type>-<scope_id>]`. [src: methodology/T3_T6_developer_handover.md §1] [src: methodology/T3_T6_generation_method.md §2.3]

## The evidence atom

### Roles

| `use_role` | Meaning | Routed to |
|---|---|---|
| `nbs_effect` | The practice changes an outcome (yield, erosion, carbon, income, a hazard's impact). | T3 livelihood rows and/or T6, through the crosswalk |
| `asset_vulnerability` | The hazard damages the practice asset (seedling mortality in drought, plantation fire, windthrow, flood scour). | T3 asset-threat rows only |
| `climate_risk` | Reserved for hazard-index definitions in [[table:T2]]; not emitted. | none |

[src: methodology/T3_T6_generation_method.md §3.1]

### The effect claim

An effect unit's `relationship` carries `direction` (`positive`, `negative`, `none`), `strength_class` (`slight`, `moderate`, `strong`, `unspecified`), `metric` (`smd_hedges_g`, `pct_change`, `ln_response_ratio`, `absolute`, `ordinal_rating`, `narrative`, and the contrast metrics), `magnitude` with optional bounds, `unit`, `significance` (`sig`, `ns`, `not_reported`), `n`, `design` and `outcome_raw` (the paper's own outcome wording). Every number must appear in the quote. [src: methodology/T3_T6_generation_method.md §3.2] [src: methodology/RULESET_VERSIONS.md]

`direction` is stated on the **outcome as named**, not on "good for people": `erosion_hazard` with `direction = negative` means erosion went down. Each direction carries a verbatim `direction_cue`, and every effect variable has a row in the direction-sense lookup that says what positive and negative mean for it. The benefit frame is applied later by the engine, never by the extractor. [src: methodology/T3_T6_generation_method.md §3.2] [src: AGENTS.md §Don't]

Context is recorded under fixed keys only: `country` (ISO3 list), `region` (informational), `aez`, `farming_system`, `income_group` (back-filled from country through the World Bank income classification) and a coarse `climate_zone`. Per-unit values override the source's defaults for multi-site studies. [src: methodology/T3_T6_generation_method.md §3.3] [src: src/nbs_ruralscan/recipe/cell_synthesis.py §unit_context]

Further context keys shape weighting and eligibility: `hazard_type`, `hazard_severity` and its verbatim `severity_cue`, `attribution`, `bundle_components`, `component_share_pct`, `normal_year_reference`, `beneficiary`, `comparator`, `counterfactual`, `envelope_misfit`, `gas`, `cost_nature` and `practice_as_described`. Their use is described below. [src: methodology/RULESET_VERSIONS.md] [src: src/nbs_ruralscan/recipe/cell_synthesis.py]

## Step 1: gather and route

### The target crosswalk

An outcome variable becomes a consumer key only through the [[table:XW]] register: one row per outcome variable × target table × target key, with `polarity`, `proximity` and `weight_factor`. It is many-to-many: `drought_hazard` routes to T3 `drought` and to T6 `drought_hazard`. A variable with no crosswalk row is catalogued as `unmapped`, feeds no cell, and is listed in the run report; unmapped is a state, not an error. [src: methodology/T3_T6_generation_method.md §4] [src: schema/spec.md §XW]

- **Polarity** converts the unit's sign into the **benefit frame** of the row (positive means the practice helps): `inverted` for outcomes where high is bad (erosion, hazards, costs as outcomes), `same` for outcomes where low is bad (yield, income, carbon, biodiversity). [src: schema/spec.md §XW]
- **Proximity** records whether the outcome is the target itself (`direct`), a stand-in for it (`proxy`, for example household income for rural poverty) or one part of a composite target (`component`, for example soil organic carbon for carbon sequestration potential). Proxies and components carry a weight factor of 0.7 by default, and are named as such in the row's account, so a proxy is never silently relabelled as the target. [src: methodology/T3_T6_generation_method.md §4] [src: src/nbs_ruralscan/recipe/cell_synthesis.py §PROXIMITY_W]

A route can be switched off for one practice where its causal claim fails for that practice, through the route policy. For example, wetland surface cooling does not route to the heat-stress cells because the cooled place has no demonstrated rural receptor. [src: src/nbs_ruralscan/recipe/cell_synthesis.py §load_xw_route_policy]

{{csv:schema/lookups/xw_route_policy.csv|cols=nbs_id,ev_variable,target_table,target_key,included}}

### Routing rules inside a cell

Before weighting, the engine applies the following rules. Each exclusion is logged with its reason. [src: src/nbs_ruralscan/recipe/cell_synthesis.py §synthesise_cell]

- Dropped units, units of another role, another practice or another family are excluded.
- `species_specific` units never enter; `crop_specific` units enter only where the crop-scope policy admits them for the practice or family (see [[ch:suitability-synthesis]]).
- In T3, a unit that **states** its hazard speaks only to that hazard's cell. A unit with no stated hazard is dropped when its variable routes to several hazards, and when it reaches the cell only through a proxy or component route: an infiltration gain in a normal year is water-stress evidence, not drought mitigation.
- In T3, a named farming-system row is emitted only when at least one unit states that system; otherwise the all-systems row applies.
- In T6 hazard priorities, a unit stating a different hazard is excluded.
- Asset-vulnerability units bypass the crosswalk; the unit's stated hazard selects the asset cell.

### Parked families

A family whose spatial product type is `qualitative_only` is parked out of the generated T3 and T6 tables. Its evidence stays in the register for implementation hand-off material but never sets a class. The water-harvesting rooftop and household cistern family is the case in point: a built domestic supply technology, not a landscape practice. [src: src/nbs_ruralscan/recipe/t3t6_build.py] [src: AGENTS.md §What is locked]

## Step 2: lineage de-duplication for cells

Echoes of one original collapse to it, as in suitability synthesis. A cell differs in one respect: a source may legitimately report several arms (two countries, or a meta-analysis' subgroup estimates). All units whose own source is the origin are therefore kept, and that source's weight is split equally across them:

```formula
share_u = 1 / k_s
```

- `k_s`: number of units of source s that reach the cell as its own (non-echo) findings.

One source thus still carries one source weight, while its arms inform the median and the range. [src: src/nbs_ruralscan/recipe/cell_synthesis.py §dedupe_for_cells]

## Step 3: rank each unit

Each unit is placed on a shared ordinal scale from −3 to +3 in the benefit frame. [src: methodology/T3_T6_generation_method.md §7.2] [src: src/nbs_ruralscan/recipe/cell_synthesis.py §unit_rank]

```formula
sign_u = d_u × f_u × p_u          rank_u = sign_u × m_u
```

- `d_u`: +1 for `positive`, −1 for `negative`, 0 for `none`.
- `f_u`: −1 when the source measured the effect of **losing** the vegetation (`framing = loss`), else +1.
- `p_u`: −1 for an `inverted` crosswalk route, else +1.
- `m_u`: magnitude rank, `slight` 1, `moderate` 2, `strong` 3; undefined for `unspecified` (the unit then votes on sign only).

The strength class comes from the [[table:BANDS]] register, which maps a magnitude and metric to a class. Bands are inclusive at the lower edge and exclusive at the upper edge on the absolute distance from a centre: 0 for differences and percent changes, 1 for ratios (a response ratio of 0.9 is a 10 % reduction). Unit-specific and income-band-specific rows are tried before generic rows. [src: src/nbs_ruralscan/recipe/cell_synthesis.py §match_band] [src: schema/spec.md §BANDS]

{{csv:schema/registers/BANDS_magnitude_bands.csv|cols=band_id,metric,strength_class,abs_min,abs_max,unit,centre,source_scale_value|limit=24}}

The first rows of the register are shown above. Further rows band stated multipliers (`fold_change`, centred on 1), WOCAT impact and cost-benefit ratings, labour days, and absolute costs relative to an income band (see [[ch:cost-profiles]]). An absolute value or narrative with no band stays `unspecified`. [src: schema/registers/BANDS_magnitude_bands.csv]

The register labels its Hedges' *g* bands as Cohen conventions, but its cuts (slight below 0.2, moderate 0.2 to 0.5, strong 0.5 and above) sit one step above Cohen's (0.2 small, 0.5 medium, 0.8 large), so an effect Cohen would call medium (0.5 to 0.8) reads as strong here. [src: schema/registers/BANDS_magnitude_bands.csv] The percent-change and log-response-ratio cuts are scoping conventions recorded as pending ratification. [src: methodology/T3_T6_generation_method.md §16] [src: schema/registers/BANDS_magnitude_bands.csv]

Further rules fix awkward encodings:

- **Ranges.** A unit reporting only a range is classed by its weakest end, not its midpoint; a range spanning zero has no assured effect and floors at 0. [src: src/nbs_ruralscan/recipe/cell_synthesis.py §range_floor]
- **Contrasts.** A with-and-without pair is classed by its ratio against the response-ratio bands, and an all-or-nothing statement ("only fields with pits produced a harvest") is `strong` by definition. [src: methodology/RULESET_VERSIONS.md]
- **Unreplicated designs.** A single plot per farm or an unreplicated before-and-after comparison without statistics is capped at `moderate`, whatever its ratio. [src: src/nbs_ruralscan/recipe/cell_synthesis.py §unit_rank]
- **Direction only.** A unit with a direction but no number contributes to direction, never to strength. A unit with no direction (a cost figure, say) is not a null finding and is excluded from the direction vote, though it stays in the envelope and the counts. [src: methodology/T3_T6_generation_method.md §3.2] [src: src/nbs_ruralscan/recipe/cell_synthesis.py §_reconcile_rank]

## Step 4: weight each unit

```formula
w_u = TIER_W × BASIS_W × D × G × T(d) × X × N × B_sc × B × Y × C × share_u
```

| Factor | Value | Source |
|---|---|---|
| `TIER_W` | source tier: high 1.0, medium 0.6, low 0.35 (unknown 0.5) | suitability engine |
| `BASIS_W` | `primary_measured` 1.0, `table` 0.9, `modelled` 0.7, `figure_read` 0.6, `expert_assertion` 0.5, `cited_secondary` 0.4; `practitioner_rating` and any unlisted basis 0.5, so a practitioner rating carries basis 0.5 × design 0.5 | suitability engine |
| `D` | study-design weight (lookup below; unlisted designs 1.0) | design weights |
| `G` | grey-literature discount when the source is grey: `nbs_effect` 0.4, `asset_vulnerability` 0.6 | suitability engine |
| `T(d)` | transferability by context distance d: 1.0, 0.7, 0.3 | Step 4a |
| `X` | crosswalk factor: direct 1.0, proxy or component 0.7 | XW |
| `N` | 0.5 when `significance = ns` | effect contract |
| `B_sc` | 0.5 for a loosely attributed programme result (`evidence_type = scoping_candidate`) | engine |
| `B` | bundled intervention share (Step 4b) | effect contract |
| `Y` | 0.7 for a hazard-year claim with `normal_year_reference = absent` | effect contract |
| `C` | 0.7 for an implied, unmeasured counterfactual | engine |
| `share_u` | own-arm split from Step 2 | engine |

[src: src/nbs_ruralscan/recipe/cell_synthesis.py §unit_weight] [src: src/nbs_ruralscan/recipe/synthesis.py §TIER_W, BASIS_W, GREY_DISCOUNT] [src: methodology/T3_T6_generation_method.md §7.8]

{{csv:schema/lookups/design_weights.csv|cols=design,weight_factor}}

Design weights put syntheses above single studies and above practitioner ratings, which are expected to be biased toward the technology the rater documents. Some values are recorded as pending ratification in the lookup. [src: schema/lookups/design_weights.csv] [src: AGENTS.md §What is locked]

Grey sources still count in `n_sources` and in the envelope; the discount stops them dominating, it does not remove them. [src: methodology/T3_T6_generation_method.md §7.8]

### 4a. Context distance and transferability

The distance between a unit's context and the row's target is scored 0 (same), 1 (adjacent) or 2 (far) per dimension, and the unit's distance is the maximum over dimensions populated on both sides. [src: methodology/T3_T6_generation_method.md §5.2] [src: src/nbs_ruralscan/recipe/cell_synthesis.py §context_distance]

| Dimension | 0 | 1 | 2 |
|---|---|---|---|
| Income group | same band (low and lower-middle are one band) | low or lower-middle vs upper-middle | anything vs high |
| AEZ or climate zone | same AEZ | different AEZ, same climate zone (tropical, dryland, temperate, boreal) | different climate zone |
| Farming system | same | rainfed cropping vs mixed crop-livestock; agro-pastoral vs pastoral rangeland; tree-perennial vs mixed crop-livestock | otherwise |

Unknown is not "same": when the target states an income band and the unit states none, the income dimension scores 1. Otherwise a context-less unit would read as fully in context. [src: methodology/T3_T6_generation_method.md §5.2]

Global rows are reconciled against the investment target `income_group = lic_lmic` with AEZ and farming system unset, so at generation transferability reduces to income: low and lower-middle income 1.0, upper-middle 0.7, high income 0.3. [src: methodology/T3_T6_generation_method.md §5.3]

### 4b. Bundles, counterfactuals and beneficiaries

An effect measured on a bundle of practices is never credited in full to one of them. A unit tagged `attribution = bundled` is weighted by the stated share of the sample using the practice component, floored at 0.25, or by a flat 0.6 when no share is stated or when the component is mandatory in every comparison and cannot be separated:

```formula
B = max(0.25, min(1, component_share_pct / 100))   if an adoption share is stated
B = 0.6                                            otherwise
```

A marginal component is a reason to exclude the unit altogether. [src: src/nbs_ruralscan/recipe/cell_synthesis.py §bundle_factor] [src: methodology/RULESET_VERSIONS.md]

A hazard-year gain with no normal-year comparison cannot be separated from an ordinary production gain, so it counts at ×0.7 and the account says so. A resilience claim needs both years to be a resilience claim. [src: src/nbs_ruralscan/recipe/cell_synthesis.py §unit_weight] [src: AGENTS.md §What is locked]

## Step 5: class eligibility

Some units are evidence for a row but may not set its class. They stay in the row's `evidence_ids`, sources and account, under `held_out_of_class` with a reason, and do not vote. [src: src/nbs_ruralscan/recipe/cell_synthesis.py §partition_voters]

| Reason | Applies to | Rule |
|---|---|---|
| `reference_shortfall` | all cells | A restored site falling short of an intact reference (`comparator = reference_wetland` or `reference_forest`) is a recovery note, not an effect of restoring. |
| `not_a_net_balance` | T6 carbon | Once methane or nitrous oxide evidence is in the pool, only net CO2-equivalent units may set the class. |
| `existing_use_opportunity_cost` | T6 rural poverty, production gap | Income already drawn from an existing wetland or forest is the opportunity cost of restoring it, not a benefit. |
| `unmanaged_state_comparator` | T3 | A unit's sign must be read against the farming-system comparator, not the unmanaged state. |
| `envelope_misfit` | T6 production gap | A loss the author attributes to the practice being outside its suitable envelope is a siting caveat; it still votes in T3, where failure under the hazard is the signal. |
| `not_a_household_benefit` | T6 rural poverty | Value landing on society (avoided damage, benefit-cost ratios) does not set a poverty class; only `farm_household` or `community` beneficiaries do. |

### Evidence floor and data-deficient rows

A cell states a class only when its voters clear a floor: at least two independent sources, or at least one measured finding (`primary_measured` or `table`). Below it, the row is still published, with its evidence and applicability, as **data deficient**: class blank, `evidence_level = limited`, `confidence = very_low`, and a `data_deficient_reason` naming what is missing. A blank reads as "does not work"; the truth is "not enough has been looked at". Consumers show "?" rather than zero. A data-deficient asset row states no sensitivity, so M2b treats it as not assessed rather than undamaged. [src: src/nbs_ruralscan/recipe/cell_synthesis.py §meets_evidence_floor, data_deficient_record] [src: methodology/T3_T6_developer_handover.md §2]

## Step 6: reconcile direction, agreement and strength

Over the voting units with a direction, let W+, W− and W0 be the summed weights of positive, negative and null units, and W = W+ + W− + W0. [src: src/nbs_ruralscan/recipe/cell_synthesis.py §_reconcile_rank]

```formula
modal = +1 if W+ ≥ W−, else −1
A = (W_modal + W0 / 2) / W
conflicting = [ W+ > 0 and W− > 0 and min(W+, W−) / (W+ + W−) ≥ 1/3 ]
rank = round( WM({ (sign_u × m_u, w_u) : sign_u = modal, m_u defined }) )
```

- `A`: weighted sign agreement. Nulls count half toward the modal side.
- `WM`: the weighted median of the suitability engine.
- If no modal-sign unit states a strength, `rank = modal × 1` (the weakest class of that sign) and the row's `strength_basis` is `direction_only`.
- If every direction-bearing unit is non-significant, the cell is `no_relationship` with `A = 1`: they agree there is no clear effect.
- If no unit has a non-zero sign, the cell is `no_relationship`.

This is the **modal-sign ordinal median**. Opposite-sign and null units are not averaged into the strength: they lower agreement, and through it confidence. Averaging them in would collapse two opposite findings into a false "no relationship" and would penalise twice, once in agreement and again in strength. `no_relationship` is emitted only when the evidence actually reports no effect. When the minority sign holds at least a third of the signed weight, the row states `conflicting_evidence` instead of a near-tie class. [src: methodology/T3_T6_generation_method.md §7.2] [src: src/nbs_ruralscan/recipe/cell_synthesis.py §CONFLICT_MIN_SHARE] [src: AGENTS.md §What is locked]

Ranks map to classes: [src: src/nbs_ruralscan/recipe/cell_synthesis.py §t6_effect_direction, t3_mitigation_potential, asset_sensitivity]

| Rank | T6 `effect_direction` | T3 `mitigation_potential` | T3 `asset_sensitivity` |
|---|---|---|---|
| +3 | `strong_positive` | `very_high` if confidence ≥ high, else `high` | `very_high` if confidence ≥ high, else `high` |
| +2 | `moderate_positive` | `moderate` | `moderate` |
| +1 | `slight_positive` | `low` | `low` |
| 0 | `no_relationship` | `none` | `none` |
| −1, −2 | `slight_negative`, `moderate_negative` | `negative` | (damage scale is 0 to 3) |
| −3 | `strong_negative` | `very_negative` | |

The top T3 class is earned by evidence, not by one enthusiastic paper. [src: methodology/T3_T6_generation_method.md §7.2]

## Step 7: caps and discounts on the class

Four adjustments act on the rank after reconciliation, in this order: proxy cap, modelled-only cap, size-sparse cap, then (T3 livelihood cells only) the hazard-intensity discount. Each sets a flag that the row's account reports. [src: src/nbs_ruralscan/recipe/cell_synthesis.py §synthesise_cell]

**Proxy cap and direct-first strength.** When any direct unit of the modal sign states a strength, the direct units alone set the strength (`strength_from = direct`); agreement and confidence still come from the whole pool. When no unit is direct, |rank| is capped at 2 (`proxy_capped`): a cell resting entirely on soil-moisture or infiltration proxies cannot read `very_high` for drought. [src: src/nbs_ruralscan/recipe/cell_synthesis.py §apply_proxy_cap]

**Modelled-only cap.** When a model is among the units that set the strength and no measured unit (`primary_measured` or `cited_secondary`) of the majority sign backs it, |rank| is capped at 2 (`modelled_capped`). The model still votes on direction. [src: src/nbs_ruralscan/recipe/cell_synthesis.py §apply_modelled_cap] [src: AGENTS.md §What is locked]

**Size-sparse cap.** In a pool of at least three same-direction units, when fewer than a third of them state a size, |rank| is capped at 2 (`size_sparse`, with counts). The evidence may all point one way, but only one sentence says how much. One- and two-unit cells are not capped here; their thinness already shows in the evidence level. [src: src/nbs_ruralscan/recipe/cell_synthesis.py §apply_size_sparse_cap]

**Hazard-intensity discount (graded, not a cap).** A strong gain in a dry year does not make a practice a drought defence: water harvesting is not irrigation and can fail under late-onset or extreme drought. In a positive T3 livelihood cell, the class is scaled down by the share, by weight, of same-hazard evidence whose claim basis is `primary_measured`, `cited_secondary` or `modelled` that found no benefit or a reversal. The engine uses three different sets under the word "measured": the evidence floor counts `primary_measured` and `table` units; the modelled-only cap counts `primary_measured` and `cited_secondary` as measured backers; the intensity discount and the maladaptation signal count `primary_measured`, `cited_secondary` and `modelled`.

```formula
L = { u : basis_u ∈ {primary_measured, cited_secondary, modelled}, hazard_u = h, sign_u ≤ 0, severity_u ≠ mild }
M = { u : basis_u ∈ {primary_measured, cited_secondary, modelled}, hazard_u = h, (severity_u ≠ mild or sign_u > 0) }
share = Σ_{u ∈ L} w_u / Σ_{u ∈ M} w_u
rank' = max(modal, round(rank × (1 − share)))
```

- `h`: the cell's hazard. Only units that state this hazard count; practitioner ratings and other-hazard nulls act through agreement alone.
- A failure the source itself places at a `mild` event (a dry spell, erratic rain) is not an intensity limit. Failures of `unspecified` severity still count.
- The floor is the weakest class of the modal sign.

One crop failure among ten measured gains barely moves the class; failures weighing a third of the measured drought-year evidence take `very_high` to `moderate`. The row is flagged `intensity_limited` with `intensity_limit_share` and the limiting evidence IDs. A hard "any failure caps the class" rule was considered and rejected as too extreme. [src: src/nbs_ruralscan/recipe/cell_synthesis.py §apply_intensity_cap] [src: AGENTS.md §What is locked]

### Hazard severity

`context.hazard_severity` records the **author's** characterisation of the event (`mild`, `moderate`, `severe`, `extreme`, default `unspecified`), with the verbatim `severity_cue`; it is never inferred. Most evidence stays `unspecified`. Every T3 livelihood row reports `severity_coverage`: gains and failures per severity, and a verdict on the severe end (`tested_gain`, `mostly_no_gain`, `tested_no_gain` or `untested`), so the statement can say when no measured gain exists under severe or extreme events. [src: src/nbs_ruralscan/recipe/cell_synthesis.py §severity_coverage] [src: methodology/RULESET_VERSIONS.md]

### The maladaptation signal

When a cell's majority says benefit, every measured unit showing **harm** (a reversal, not a null) is listed in `justification.maladaptation` with its unit and source counts, and the statement names it. A minority of harm findings is never hidden inside an agreement score; a majority of harm already yields a negative class. Consumers outline the chip as a caution where any study measured harm. [src: src/nbs_ruralscan/recipe/cell_synthesis.py §maladaptation_signal] [src: methodology/T3_T6_developer_handover.md §3]

## Step 8: two-axis confidence

Confidence follows the IPCC calibrated-language approach: an **evidence** axis and an **agreement** axis combine through a fixed matrix. [src: methodology/T3_T6_generation_method.md §7.4]

**Evidence level** counts independent sources after de-duplication, with a meta-analysis counting as its stated number of pooled studies (n ≥ 2): [src: src/nbs_ruralscan/recipe/cell_synthesis.py §evidence_level, independent_sources]

| `evidence_level` | Rule |
|---|---|
| `limited` | ≤ 2 independent sources, or every unit `cited_secondary`, `expert_assertion` or `practitioner_rating` |
| `robust` | ≥ 5 independent sources AND (≥ 2 `primary_measured` or `table` units OR a high-tier meta-analysis among the units); a meta-analysis counts as its pooled n toward the 5 |
| `medium` | otherwise |

**Agreement level** is `high` when A ≥ 0.8, `medium` when 0.6 ≤ A < 0.8, and `low` below 0.6. With only one independent source, agreement is undefined and set to 0, so it reads `low`. [src: src/nbs_ruralscan/recipe/cell_synthesis.py §agreement_level, _reconcile_group]

{{csv:schema/lookups/ipcc_confidence_matrix.csv}}

The matrix follows the IPCC uncertainty guidance (Mastrandrea et al. 2010), unchanged in AR6. Expert-only evidence is an evidence property (`limited`, with `source_mix = expert_only`), not a confidence level; the former `expert_opinion` level was removed so that no cell can bypass the matrix. [src: methodology/T3_T6_generation_method.md §7.4]

Strength and confidence are separate and both are shown. "Slight benefit, very high confidence" is a well-established small effect; "strong benefit, low confidence" is a promising but thin finding. Transferability is deliberately not folded into confidence: confidence answers "how sure is the literature", the transfer class answers "does it apply here". [src: methodology/T3_T6_developer_handover.md §2] [src: methodology/T3_T6_generation_method.md §7.4]

## Step 9: the applicability envelope and transfer class

Every row, including global rows, carries an `applicability` object: counts of independent sources by income group, AEZ and farming system (with `unknown` counted), the list of countries, `n_sources_in_scope`, `weight_share_in_context`, the target and the `transfer_class`. [src: methodology/T3_T6_generation_method.md §5.4] [src: src/nbs_ruralscan/recipe/cell_synthesis.py §build_applicability]

The transfer class is computed from **pre-transfer** weights, that is each unit's weight divided by its transferability factor:

```formula
s0 = Σ_{d_u = 0} ŵ_u / Σ ŵ_u     s≤1 = Σ_{d_u ≤ 1} ŵ_u / Σ ŵ_u     s2 = Σ_{d_u = 2} ŵ_u / Σ ŵ_u     ŵ_u = w_u / T(d_u)
```

| `transfer_class` | Rule (strict majorities) |
|---|---|
| `in_context` | s0 > 0.5 |
| `out_of_context` | s2 > 0.5 |
| `adjacent` | s≤1 > 0.5 and not in context |
| `mixed` | none of the above, including an exact 50/50 split |

Measuring the share on transfer-weighted weights would be circular: the far unit would first be cut to 0.3 and then found to be a small share, so one low-income and one high-income unit would read as almost entirely in context. [src: methodology/T3_T6_generation_method.md §5.4] [src: src/nbs_ruralscan/recipe/cell_synthesis.py §transfer_class_from_shares]

### Why high-income evidence never silently sets a target value

Three mechanisms act together. High-income evidence enters a global row at ×0.3; the envelope records it as high income; and at run time, a global row whose recomputed transfer class for the study area is `out_of_context` yields the status **`no_applicable_evidence`**, with the row shown greyed and a statement such as "evidence from high-income temperate contexts only (n = 2)". The class is never shown as if it applied. M2b falls back to its equal-weight default and records the substitution. Economic figures face a harder rule: an exclusion, not a weight (see [[ch:cost-profiles]]). The worked test is a Swedish riparian cost figure, which must never set or nudge a Sahelian value; it ships as an acceptance fixture. [src: methodology/T3_T6_generation_method.md §5.5] [src: methodology/T3_T6_generation_method.md §5.6]

## Step 10: rows per scope

Overrides are rows, not nested objects, because each carries its own class, confidence, evidence IDs, envelope and prose and must be reviewable as a row. `scope_type` takes `aez`, `farming_system` (T6 only, since it is a T3 cell key), `admin_country`, `admin_region`, `hydrobasin` or `income_group` (`low`, `lower_middle`, `upper_middle`, `high`, or the pooled `lic_lmic`). [src: methodology/T3_T6_generation_method.md §2.3] [src: schema/spec.md §T3]

For each populated context dimension, units are grouped by value; a group with at least two independent sources is re-reconciled (eligibility, floor, caps, discount and confidence all re-applied) against its own target. An income-group scope uses that income band as its target; an AEZ or farming-system scope keeps the global income target, so a scope built only from high-income evidence is `out_of_context` even within its own AEZ. [src: methodology/T3_T6_generation_method.md §5.3] [src: src/nbs_ruralscan/recipe/cell_synthesis.py §synthesise_cell]

The method document emits a scope row when the group's rank differs from the global row by at least one, or when the global row is `out_of_context` for that scope. The engine also emits it when the global row's agreement is low. [src: methodology/T3_T6_generation_method.md §2.3] [src: src/nbs_ruralscan/recipe/cell_synthesis.py §synthesise_cell]

`context_dependent = true` on the global row means: global agreement is low or medium and at least two emitted scope rows differ in sign or rank. It is a machine-readable "read the scope rows". [src: src/nbs_ruralscan/recipe/cell_synthesis.py §synthesise_cell] [src: methodology/T3_T6_generation_method.md §7.4]

At run time the most specific matching scope wins: administrative region, country, hydrobasin, farming system, AEZ, income group, then global. Income groups match by band. [src: methodology/T3_T6_developer_handover.md §4] [src: src/nbs_ruralscan/recipe/cell_synthesis.py §resolve_for_aoi]

## Step 11: family rows and the family vote

Effects differ by family: farmer-managed natural regeneration and planted silvoarable systems differ several-fold on establishment cost and by years on carbon accrual. Each family with at least two distinct source identifiers in the cell (the pooled n of a meta-analysis is not applied at this step) receives its own row (without scope rows). A family row identical in evidence to the roll-up is not emitted. The **roll-up row is always emitted**, as a pooled synthesis over all of the practice's eligible units, not a mean of family medians, so tier, grey and transfer weighting stay intact. [src: methodology/T3_T6_generation_method.md §2.2] [src: src/nbs_ruralscan/recipe/cell_synthesis.py §synthesise_cell_with_families]

The roll-up's **class** then defers to its families through a vote:

```formula
v_f = √(n_sources_f)
dissent = ( Σ_{f ∈ C} v_f + min(Σ_{f ∈ P} v_f, Σ_{f ∈ Q} v_f) ) / ( Σ_{f ∈ C} v_f + Σ_{f ∈ P} v_f + Σ_{f ∈ Q} v_f )
```

- `f`: each classed family row (a family whose roll-up policy excludes it casts no vote).
- `C`: families classed `conflicting_evidence`; `P`, `Q`: families with a positive or a negative signed class. Families classed `no_relationship` add to neither the numerator nor the denominator.
- If dissent ≥ 1/3, the roll-up states `conflicting_evidence`, its agreement is set to `low` and its confidence is re-derived from the matrix.
- Otherwise the class is the weighted median of the modal-sign family ranks.
- Guards: at least two classed family rows, covering at least half of the roll-up's sources. Otherwise the pooled class stands, with the reason recorded.

Findings tagged to a practice's cross-family context form their own row and vote like a family; for example, the water-harvesting drought vote includes the cross-family tag. This sits uneasily with the description elsewhere of cross-family tags as shared context rather than sub-practices (see [[ch:m1-suitability]]). [src: src/nbs_ruralscan/recipe/cell_synthesis.py §synthesise_cell_with_families] [src: schema/registers/FAM_family_registry.csv]

The square root damps the advantage of a heavily studied family without letting a thin one outvote it. The same one-third conflict rule applies at the unit and the family level. The vote, its weights, dissent share and coverage are recorded in `justification.family_vote`. Separately, `family_spread = true` flags a roll-up whose family ranks differ by two or more, so a consumer can show "varies by sub-practice". [src: src/nbs_ruralscan/recipe/cell_synthesis.py §_family_vote] [src: AGENTS.md §What is locked]

{{csv:schema/lookups/family_rollup_policy.csv|cols=nbs_id,suitability_family_id,rollup_included}}

A family excluded from the roll-up keeps its own rows but never sets the practice-level class: plantation forestry is tree farming, not restoration toward a natural baseline. [src: schema/lookups/family_rollup_policy.csv]

### Comparator policy

Studies of what an **existing** forest or wetland does, or what its loss costs, are evidence for keeping it, not for planting or creating one within a project horizon. Such units leave the roll-up and every family except their home family, which the policy names for cross-family units. [src: src/nbs_ruralscan/recipe/cell_synthesis.py §synthesise_cell_with_families] [src: methodology/RULESET_VERSIONS.md]

{{csv:schema/lookups/comparator_policy.csv|cols=nbs_id,comparator,rollup_included,home_family}}

## Step 12: effect locus

Where the farmer feels an effect differs by practice: trees on the farm affect the adopting household; forest restoration acts off-site, downstream or at landscape scale. Every T3 livelihood row is stamped with its locus in `justification.effect_locus`, the statement says when the effect is off-site or partly off-site, and an `off_site` practice sets `landscape_scale_only = true`. A family's own entry wins over the practice default. Where a practice has no default, its roll-up takes the locus its families share, or `mixed` when they differ. [src: src/nbs_ruralscan/recipe/cell_synthesis.py §effect_locus_for, apply_effect_locus] [src: AGENTS.md §What is locked]

{{csv:schema/lookups/effect_locus.csv|cols=nbs_id,suitability_family_id,effect_locus}}

## Asset vulnerability and asset-threat rows

Asset-threat rows answer a different question from livelihood rows: how badly does the hazard damage the investment? They are built from `asset_vulnerability` units and feed M2b Stream A, which is a filter on the investment and is never summed with M2's livelihood risk (see [[ch:m2b-project-risk]]). [src: methodology/T3_T6_generation_method.md §7.5] [src: AGENTS.md §What is locked]

Sourcing is layered. The seed is the WOCAT technology questionnaire's tolerance-to-extremes ratings, read from the structured questionnaire, cached as a deterministic transcript and converted rule by rule (no model) into units with a practitioner-rating design and the grey discount. Literature from the single-pass sweep (establishment mortality, windthrow, plantation fire, flood scour) adds to it; WOCAT-versus-literature concordance is what the agreement axis then measures. An internal rating pass by domain colleagues is optional; there is no external expert-elicitation programme, so many asset cells are honestly `limited`. [src: methodology/T3_T6_generation_method.md §9]

The WOCAT tolerance scale maps to strength through ordinal BANDS rows: "not well" → strong damage, "moderately" → moderate, "well" → slight, "very well" → none. [src: schema/registers/BANDS_magnitude_bands.csv]

The reconciled rank (0 to 3, damage direction) maps to `asset_sensitivity` with the same `very_high` gate as T3 livelihood rows. `timescale_of_effect` on these rows means the **vulnerability window** (for example the establishment period), read with [[table:T0]] `establishment_period_years`. [src: methodology/T3_T6_generation_method.md §7.5]

### Asset-threat-only hazards

Sedimentation, extreme rainfall and landslides are valid only in asset-vulnerability units and asset-threat rows: siltation of dams and tanks, or storm damage to structures, threatens the investment, not livelihoods directly. They open no livelihood cell, have no crosswalk route, and are outside the hazard-weight completeness rule. [src: src/nbs_ruralscan/recipe/cell_synthesis.py §ASSET_ONLY_HAZARDS] [src: AGENTS.md §What is locked]

### When the asset risk weight is emitted

`asset_risk_weight` is a derived normalisation, never extracted:

```formula
a_h = r_h / Σ_{k ∈ H} r_k
```

- `H`: the practice's core hazard set; `r_h`: the asset-sensitivity rank of hazard h on the global roll-up asset row (none 0, low 1, moderate 2, high and very high 3).
- If every rank is zero, weights are equal.

Weights are emitted only when every core hazard has an assessed (non-blank) asset row; a data-deficient row counts as missing. Otherwise the weights stay blank, the practice is reported as `weights_incomplete`, and M2b uses equal weights and says so. The method and schema text state the rule as "all seven hazards"; since frost left T3, the engine applies it to the six core hazards. [src: src/nbs_ruralscan/recipe/cell_synthesis.py §asset_risk_weights] [src: schema/spec.md §T3] [src: methodology/T3_T6_generation_method.md §7.5]

## Step 13: numbers under the class, and the traceable account

`magnitude_summary` on a T6 effect row is emitted only when at least two independent sources in scope share a metric and a convertible unit: `{metric, unit, median, low, high, n, income_groups}`, with the weighted median and the observed extremes (never a confidence interval that was not measured). The pool is direction-aware: units opposing the row's direction are counted as excluded, never pooled. Cross-metric pooling is forbidden, and the number sits under the class; it is not an MCDA value. [src: methodology/T3_T6_generation_method.md §7.6] [src: src/nbs_ruralscan/recipe/cell_synthesis.py §magnitude_summary]

`justification` is a traceable account in the style of an IPCC evidence table: `statement`, `evidence_summary`, `agreement_note`, `mechanism`, `conditionality` or `caveats`, `key_evidence_ids` (up to five top-weight units) and `source_mix`, together with the flags from the steps above. Levels and classes are inserted by the engine. The only AI step is a gated prose writer, which may quote or paraphrase only the used units' quotes, may not introduce a number, source or direction absent from them, and cites evidence IDs per sentence; a deterministic check verifies every number. Until the writer runs, prose fields carry the engine statement marked as pending. [src: methodology/T3_T6_generation_method.md §8] [src: .agents/skills/source-command-t3t6-synthesise/SKILL.md]

## Assumptions and limits

- **Scoping, not feasibility.** A class says what the pooled literature supports about direction and size in comparable contexts. It does not estimate an effect at a site, and it is not ecosystem-service modelling.
- **Conventions, not calibration.** The band cuts for percent change and log response ratio, the design weights, the 0.7 proxy haircut, the transferability factors and the one-third conflict threshold are declared defaults, several pending ratification. They should be varied in sensitivity analysis. The two scales also disagree: the percent-change cut for strong is 30 %, but the log-response-ratio cut is 0.35 (about 42 %), so a 30 % gain is strong as a percent change and moderate as a log response ratio. [src: schema/registers/BANDS_magnitude_bands.csv]
- **Coarse context.** Climate zone has four classes, and AEZ and farming system are often unknown in the evidence, so most scope rows are by income group; country and region scope rows do not yet exist.
- **Fragility.** Thin cells can change class when one unit is added, dropped or re-reviewed. Classes move between builds as evidence is added; consumers read the tables at run time.
- **Publication bias.** Benefits are over-reported. The grey discount, the maladaptation signal and the intensity discount partly offset this; no statistical correction is applied.
- **Transfer.** An `in_context` label means income-band match, not ecological equivalence. A feasibility study must still test the effect for the site, the farming system and the hazard regime.
- **Cross-family tags vote.** In the family vote the cross-family tag counts as a family, although elsewhere it is described as shared context, not a sub-practice. A roll-up class can therefore be swayed by evidence that names no sub-practice.
- **Do not combine across editions.** Row counts and classes belong to one build.

## Where this is configured

- [[table:T3]], [[table:T6]], [[table:T6E]]: generated rows (CSV is the source of truth; JSON is generated).
- [[table:EV]], [[table:SRC]]: evidence units, tiers, categories and study context.
- [[table:XW]]: outcome-to-target routes, polarity, proximity and weight factors.
- [[table:BANDS]]: magnitude-to-strength bands.
- [[table:T5]]: the priority rows T6 links to.
- `schema/lookups/ipcc_confidence_matrix.csv`, `design_weights.csv`, `effect_locus.csv`, `comparator_policy.csv`, `family_rollup_policy.csv`, `xw_route_policy.csv`, `crop_scope_policy.csv`: the policy tables above.
- [[table:FAM]]: families and spatial product types (which decide parking).
