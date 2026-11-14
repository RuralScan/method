---
title: Indicative cost profiles
slug: cost-profiles
summary: Read, audit and correctly present a T6E economic-profile row: which cost indicators exist, how a cost class is set, when a value range may be published, and why the profile is not a cost-benefit analysis.
sources:
  - methodology/T3_T6_generation_method.md
  - methodology/T3_T6_developer_handover.md
  - methodology/RULESET_VERSIONS.md
  - schema/spec.md
  - schema/structure/columns.json
  - schema/registers/BANDS_magnitude_bands.csv
  - schema/recipes/agroforestry/T6E_economic_profile.json
  - src/nbs_ruralscan/recipe/cell_synthesis.py
  - AGENTS.md
---

## What a cost profile is for

A task team scoping a nature-based solution needs to know whether a practice is cheap or expensive to establish and maintain where it would be invested, and whether it tends to raise income or cut production costs. The cost profile answers that at scoping grade: it gives an **ordinal cost class** ("small, moderate or large given the context") with a confidence expressed in IPCC calibrated language (not a statistically calibrated probability) and, only when strict gates are met, an indicative value range with its sources. [src: methodology/T3_T6_developer_handover.md §1] [src: schema/spec.md §T6]

It does not estimate net present value, rates of return or benefit-cost ratios, and it does not discount or inflate. Costs are indicative and ordinal; this is not cost-benefit analysis, which belongs to the feasibility stage (see [[ch:m6-handoff]]). [src: schema/spec.md §T6] [src: AGENTS.md §What is locked]

## Where cost rows live

Cost and economic-indicator rows (`variable_type = economic_indicator`) are written to [[table:T6E]], the economic profile, not to the scorecard table [[table:T6]]. They share T6's columns and its generator, because they are produced by the same cell synthesis (see [[ch:effect-synthesis]]), but they feed the economic-profile panel, not the scorecard chips. [src: schema/spec.md §T6] [src: schema/structure/columns.json]

A cost has no direction of benefit, so `effect_direction` is left blank on economic rows; the manifest makes it conditional, required only for non-economic rows. `economic_indicator_type` and, when gated in, `economic_value_range` carry the economic content. [src: schema/spec.md §T6] [src: src/nbs_ruralscan/recipe/cell_synthesis.py §synthesise_cell]

## Which indicators exist

The indicator vocabulary is: `establishment_cost`, `recurrent_cost`, `income_potential`, `cost_reduction`, `market_access`, `carbon_revenue`, `subsidy_dependency`, `cost_per_beneficiary`, `cost_per_hectare_restored`, `cost_per_tco2e_avoided` and `cost_per_farmer_reached`. [src: schema/spec.md §T6]

Economic cells are **denominator-specific**. An evidence unit reaches a cost cell only if its unit fits what that cell measures; without this rule a cost per tonne of CO2-equivalent once became the magnitude of a per-hectare establishment cost. [src: src/nbs_ruralscan/recipe/cell_synthesis.py §_ECON_UNITS]

| Indicator | Units it admits |
|---|---|
| `establishment_cost` | per structure, per system, per m³ stored (the generic up-front cell takes the denominators no specific cell owns) |
| `recurrent_cost` | per hectare per year, per household per year, per farmer per year, per structure per year, percent of establishment cost per year |
| `cost_per_hectare_restored` | USD per hectare |
| `cost_per_beneficiary` | USD per beneficiary, per household, per household per year |
| `cost_per_farmer_reached` | USD per farmer, per farmer per year |
| `income_potential` | USD per hectare (per year), per household per year, per farmer per year |
| `carbon_revenue` | USD per hectare per year, USD per tonne CO2e |
| `cost_reduction`, `market_access`, `subsidy_dependency` | not unit-constrained (see below) |

[src: src/nbs_ruralscan/recipe/cell_synthesis.py §_ECON_UNITS, _unit_fits_econ_cell]

Three further routing rules apply. [src: src/nbs_ruralscan/recipe/cell_synthesis.py §_unit_fits_econ_cell]

1. **A cost level is an amount.** The cost-level cells (establishment, recurrent and the cost-per cells) accept only an absolute amount that is not a decrease. A relative measure (a percent change or log response ratio against a control) and an absolute saving go to `cost_reduction` instead. Routing one relative ratio into several level cells had inflated their evidence levels while adding no amount.
2. **Route by what the money buys, not by its denominator.** `context.cost_nature` (`establishment` or `recurrent`) overrides the denominator heuristic in both directions. An annualised capital cost stated "per hectare per year" stays an establishment cost; a recurrent-natured unit never enters the establishment or per-hectare-restored cells. Untagged units keep the denominator routing.
3. **A spread is not a sign.** A cost range across implementers is dispersion, recorded with `direction = none`; the range goes to the value range or `outcome_raw`. [src: methodology/RULESET_VERSIONS.md]

`cost_reduction` counts as a benefit only where it is a farm-level production-cost saving, that is, a route to household profit and so to poverty reduction. [src: schema/spec.md §T6]

### What is not generated

`cost_per_tco2e_avoided` belongs to feasibility, not scoping, and its cells are not published; the evidence units stay in the register. Total project costs without a per-unit denominator are not evidence for any cost cell: a budget line with no denominator is not a unit. [src: schema/spec.md §T6] [src: src/nbs_ruralscan/recipe/cell_synthesis.py §FEASIBILITY_ONLY_ECON] [src: methodology/T3_T6_generation_method.md §6]

Families whose spatial product type is `qualitative_only` are parked out of the generated tables, including T6E. [src: AGENTS.md §What is locked]

## Where cost evidence comes from

Economic evidence is admitted only with a per-unit denominator. The preferred sources are World Bank project appraisal documents and implementation completion reports where they give denominators, structured project archetypes, and meta-analyses of adoption economics. Evidence must come from searches targeted at effects and costs; papers found for suitability are not a substitute. [src: methodology/T3_T6_generation_method.md §6]

Each cost unit records the currency year when the source states it (`currency_year`), the country and so the income group, and the denominator in `unit`. [src: src/nbs_ruralscan/recipe/cell_synthesis.py §economic_value_range] [src: methodology/T3_T6_generation_method.md §3.3]

## The ordinal-first rule: the cost class

The value a consumer reads first is a **cost class**, not a number. For an economic row the engine computes a magnitude summary over the cost figures in the row's scope that share a metric and unit, takes their weighted median and classes it with the [[table:BANDS]] rows for that unit **and that income band**. The class is reported in the row statement as small, moderate or large, with its unit and context. [src: src/nbs_ruralscan/recipe/cell_synthesis.py §magnitude_summary, synthesise_cell]

```formula
m = WM({ (x_u, w_u) : u ∈ row scope, metric_u = M, unit_u = U, band(u) = band(target) })
class = BANDS(metric = absolute, unit = U, income_band = band(target))(m)
```

- `x_u`: the unit's stated amount; `w_u`: its synthesis weight (tier, claim basis, design, grey discount and the other factors in [[ch:effect-synthesis]]).
- `band(·)`: the income band, with low and lower-middle income pooled as `lic_lmic`; global rows target `lic_lmic`.
- `WM`: the weighted median; the pool is the metric-and-unit group with the most independent sources.

The bands for low and lower-middle income contexts are: [src: schema/registers/BANDS_magnitude_bands.csv]

{{csv:schema/registers/BANDS_magnitude_bands.csv|where=income_band=lic_lmic|cols=band_id,strength_class,abs_min,abs_max,unit}}

The thresholds are scoping-grade, set against a typical smallholder gross margin in low and lower-middle income countries of roughly USD 200 to 800 per hectare per year. Upper-middle income thresholds are twice and high-income thresholds five times those values, so the same amount can be "large" in one context and "small" in another. The rule is to adjust the thresholds, not the mechanism. In the class vocabulary `slight` reads as small and `strong` as large. [src: schema/registers/BANDS_magnitude_bands.csv]

Two choices make the class honest about where it comes from. First, the income-band gate that governs value ranges also governs the class, so a class can never rest on a figure from another income band. Second, because economics are read ordinally, a single source may set the class, unlike effect magnitude summaries, which need two; the row's confidence (limited evidence, undefined agreement, so very low) carries the caveat. [src: src/nbs_ruralscan/recipe/cell_synthesis.py §synthesise_cell, magnitude_summary]

When a row states no class, the statement says why, so a blank is never read as "cheap": the evidence states no cost figure; no size band exists for the unit; every figure comes from another income group; or no two sources give a figure in the same unit. [src: src/nbs_ruralscan/recipe/cell_synthesis.py §_no_cost_class_reason]

Confidence on economic rows follows the same IPCC two-axis matrix as every generated row. [src: schema/spec.md §T6]

## Gates on publishing a value range

`economic_value_range` is `{low, high, unit, source_note}`. It is emitted only when **all** of the following hold. [src: methodology/T3_T6_generation_method.md §7.7] [src: src/nbs_ruralscan/recipe/cell_synthesis.py §economic_value_range]

1. **Numeric.** The unit states a magnitude, or both bounds of a range.
2. **Denominated.** The unit is one of `usd_per_ha`, `usd_per_ha_yr`, `usd_per_beneficiary`, `usd_per_tco2e` or `usd_per_farmer`. The method also admits a unit convertible to one of these through the variable ontology; the engine checks the enumeration directly. A total project cost with no denominator fails.
3. **Known context.** The unit's income group is known.
4. **Same income band.** The unit's band equals the row's band. Low and lower-middle income are pooled; upper-middle and high income are never pooled with them or with each other.
5. **No high-income figures in target rows.** High-income cost figures are **excluded outright** from low and lower-middle income rows and from global rows. This is an exclusion, not a down-weighting, because labour, land and discount regimes do not transfer.
6. **Replicated.** At least two independent sources in the same unit; a meta-analysis counts as the number of studies it pools.
7. **Same scope row.**

`low` and `high` are the observed extremes of the qualifying figures (both bounds of a range-only figure enter), never a confidence interval. `source_note` lists each contributing source with its country and currency year, the count and the band. Every unit that fails a gate is listed in the run report with the gate it failed, so exclusions are visible rather than silent. [src: src/nbs_ruralscan/recipe/cell_synthesis.py §economic_value_range] [src: methodology/T3_T6_generation_method.md §7.7]

These gates are strict by design, and at the pinned revision none of the agroforestry economic rows publishes a value range; those rows carry cost classes with their confidence instead. [src: schema/recipes/agroforestry/T6E_economic_profile.json]

The spec's value-range unit enumeration is narrower than the set of units that may set a cost class: per-household, per-structure and per-cubic-metre figures can set an ordinal class through their own bands, but cannot form a published range. [src: schema/spec.md §T6] [src: schema/registers/BANDS_magnitude_bands.csv] [src: src/nbs_ruralscan/recipe/cell_synthesis.py §ECON_UNITS]

## Why currencies and price years are not normalised

No currency conversion, inflation adjustment or price-year harmonisation is applied, and consumers are instructed to show the range as is and never to compute new ratios. [src: methodology/T3_T6_developer_handover.md §3] [src: methodology/T3_T6_generation_method.md §7.7]

The reasons are methodological, not a shortcut:

- **The question is ordinal.** At scoping grade the decision-relevant reading is whether an amount is big or small for the context where it is spent. The income-banded classes answer that directly; a deflated, converted figure would imply a precision the evidence does not have. [src: schema/registers/BANDS_magnitude_bands.csv]
- **Price levels do not transfer.** Costs depend on local labour, land and capital conditions. A conversion to a common currency and year would make figures look comparable while hiding exactly the differences the income-band exclusion is there to respect. [src: methodology/T3_T6_generation_method.md §7.7]
- **Transparency is kept.** Each figure's currency year is recorded in `source_note`, so a feasibility economist can normalise later with project-specific deflators and exchange rates. [src: methodology/T3_T6_generation_method.md §7.7]

Relative measures (percent changes in cost against a control) carry no denominator: they may vote on direction in `cost_reduction` but never set a value. [src: src/nbs_ruralscan/recipe/cell_synthesis.py §_RELATIVE_METRICS]

## Why this is not cost-benefit analysis

- **No valuation of benefits.** Benefits are expressed as ordinal effect classes in T6, not monetised. T6E holds costs and a small set of income and revenue indicators.
- **No discounting or time profile.** Ranges are observed extremes from different studies, years and designs; there is no cash-flow model.
- **No site specificity.** Figures describe documented projects in comparable income contexts, not the costs at a proposed site.
- **No feasibility indicators.** Carbon abatement cost is deliberately not generated.

An economist can use a gated range for an indicative narrative without a full cost-benefit analysis; the analysis itself, with local prices and a project design, is feasibility work. [src: schema/spec.md §T6] [src: AGENTS.md §What is locked]

## Assumptions and limits

- **Thresholds are conventions.** The cost bands are scoping-grade, anchored on an assumed smallholder gross margin, with simple multipliers for richer contexts. Different anchors would move some classes.
- **Sparse, heterogeneous evidence.** Few sources report costs with a usable denominator; many rows are classed from one source and carry very low confidence. Classes can change as evidence is added.
- **Mixed price years.** Pooled figures span different years and currencies. A class near a band edge is sensitive to inflation that is deliberately not corrected.
- **Implementation context.** Costs depend on project design, scale, implementer and labour arrangements that the evidence rarely reports consistently.
- **What feasibility must still do.** Cost the specific design with local prices, discount rates and time horizons; value benefits; test sensitivity; and confirm financing and subsidy assumptions.

## Where this is configured

- [[table:T6E]]: generated economic-profile rows (CSV is the source of truth).
- [[table:BANDS]]: income-banded cost classes and other magnitude bands.
- [[table:EV]], [[table:SRC]]: cost units, denominators, currency years, countries and income groups.
- [[table:XW]]: routes from cost outcome variables to economic indicators.
- [[table:T6]]: the effect rows the profile sits beside.
