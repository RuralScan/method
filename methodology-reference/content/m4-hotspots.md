---
title: "M4: Priority hotspots"
slug: m4-hotspots
summary: Rank candidate areas by declared development priorities and explain the weights, drivers and sensitivity of the shortlist.
sources:
  - method:priority/README.md
  - method:data-model/priority-contract.json
  - method:methodology-reference/reviews/critic-assessment-2026-11-24.md
  - methodology/modules/M4_hotspots.md
  - method:handbook/implement-a-scan.md
  - methodology/opportunity_space_T5.md
  - methodology/modules/M3_characterisation.md
  - schema/spec.md
  - methodology/weight_normalisation.md
  - methodology/modules/M2_climate_risk.md
  - methodology/framework.md
---

## Question this module answers

Module 4 (M4) asks where the project team's development priorities concentrate within the opportunity space. M1 identifies candidate areas; M3 describes their conditions; M4 combines selected priorities into a ranking for closer investigation. The result reflects the chosen priorities and weights, not a prediction of investment returns. [src: methodology/modules/M4_hotspots.md §2] [src: method:handbook/implement-a-scan.md §3. Build the scoping brief]

## Inputs

Table: Inputs to priority ranking.

| Input | Role |
|---|---|
| M1 opportunity-space mask | Limits the comparison to candidate areas. |
| M3 priority layers | Describe climate-related need, production, poverty, biodiversity and equity. |
| T2/T5 priority settings | Identify eligible indicators, direction and scaling rules. |
| Recorded user weights | State the relative emphasis on each selected priority. |
| Geographic units | Define the areas to be compared and shortlisted. |
| M2b risk flags, if used | Provide a separate investment-risk screen. |

[src: methodology/modules/M4_hotspots.md §3]

Only selected T2 or T5 rows marked `priority` enter the score. Descriptors such as population counts provide context. Country-level values cannot distinguish locations within a country; they are reported as context or qualified flags rather than as spatially differentiating priorities. [[ch:m3-characterisation]] describes this screening and the treatment of related indicators. [src: methodology/opportunity_space_T5.md §Spatial-grain rule]

## Method

### 1. Use the declared problem classes

M3 produces none, low, medium and high concern scores of 0, 0.33, 0.66 and 1. Each selected variable retains its raw value, unit and classification rule. Threshold classes express the declared fixed reference; terciles express position within a stated reference population. A relative high class does not establish absolute severity. See [[ch:m3-characterisation]] for classification and duplicate-concern checks. [src: method:data-model/priority-contract.json]

### 2. Record user priorities

Give each selected concern an explicit nonnegative weight. Zero leaves it out. At least one weight must be positive. These weights express the user's priorities; they are different from the four problem-class scores and from a source's influence on scientific synthesis. If an interface offers low/medium/high weights, it must show the numeric convention it uses. The evaluator does not infer default or equal weights from missing settings. [src: method:priority/README.md §Correlation and weighting]

Record the representative chosen for each concern and the reason. Themes organise the explanation; they do not secretly multiply the weights. If theme controls are added later, their translation into final per-concern weights must be explicit and approved. [src: method:priority/README.md]

### 3. Sum and normalise once

```formula
w_j = u_j / Σ_k u_k
H(x) = Σ_j w_j p_j(x)
```

`u_j` is the recorded user weight; `w_j` is its normalised contribution. `p_j(x)` is the problem-class score at location `x`. `H(x)` is the combined priority within the opportunity space. The denominator and selected concern set are the same for every scored pixel. [src: method:priority/README.md §Correlation and weighting]

Any missing positive-weight indicator makes the pixel unknown. A missing zero-weight indicator does not block it. Outside the opportunity space the pixel is excluded; an unknown mask stays unknown. The final score is already between 0 and 1, so there is no second pixel-based rescaling and no quintile re-binning. Show each concern's contribution alongside the total. [src: method:data-model/priority-contract.json]

Keep M2b investment-risk screening separate. T2 now supplies individual climate-risk variables, not a second composite Climate Risk Index to add alongside its components. A high priority score indicates combined need or concern, not confirmed suitability or intervention effectiveness. [src: method:priority/README.md]

### 4. Assess CRITIC without replacing user priorities

CRITIC derives weights from variation and correlations in the supplied indicators. We tested the implementation against its original published example and ran controlled checks for duplicates, constant indicators, opposing signals, changing study areas and classifying values. It is useful for sensitivity analysis, but those weights answer a different question from the user's priorities. [src: method:methodology-reference/reviews/critic-assessment-2026-11-24.md]

The tests show that changing the area, discretisation or scaling can materially change CRITIC weights. Identical indicators leave the method without identifiable weights; it must not invent an equal-weight fallback. Correlation also cannot decide which of two records is the canonical representation of a concern. Keep CRITIC **diagnostic only** in this version; there is no automatic CRITIC, entropy or AHP multiplier. [src: method:methodology-reference/reviews/critic-assessment-2026-11-24.md]

### 5. Test the shortlist

Repeat the ranking with plausible user weights, alternative justified classifications and representative choices. Show which locations change and why. Keep suitability, evidence of intervention response, investment-risk flags and data coverage alongside priority. The resulting shortlist directs local investigation; it does not validate an investment. [src: method:priority/README.md] [src: method:handbook/implement-a-scan.md §3. Build the scoping brief]

## Worked illustration

This is hypothetical, not a country calibration. Give poverty a weight of 3 and flood concern a weight of 1. The normalised weights are 0.75 and 0.25.

Table: Hypothetical problem classes and user-weighted scores.

| Cell | Poverty score | Flood score | Priority calculation | Result |
|---|---:|---:|---|---:|
| A | 1 | 0.33 | 0.75 × 1 + 0.25 × 0.33 | 0.8325 |
| B | 0.66 | 1 | 0.75 × 0.66 + 0.25 × 1 | 0.745 |
| C | Unknown | 1 | Missing a positive-weight criterion | Unknown |

A ranks above B under these priorities. Increasing the user's emphasis on flood concern can reverse that order. Neither ranking proves greater intervention benefit. [src: method:priority/README.md]

## Reading a hotspot

A hotspot is a concentration of the selected needs within the candidate space. It is not a confirmed feasible site or the place where a practice is guaranteed to deliver the largest benefit. Read the ranking alongside the evidence of response in [[ch:m5-scorecard]] and the investment-risk flags in [[ch:m2b-project-risk]]. [src: methodology/modules/M4_hotspots.md §2]

For example, an area may rank highly because of poverty and flood exposure. That supports further investigation of interventions there; it does not establish that the particular practice reduces either problem in that context. The effect evidence and local assessment answer those questions separately. This is an illustrative interpretation, not a reported pilot result.

## Outputs

Retain the priority map, ranked areas, main drivers and sensitivity results, together with raw indicators, scaling rules, final weights, geographic units and data coverage. Report the people or production within shortlisted areas as contextual quantities, not automatically as beneficiaries or attributable benefits. [src: methodology/modules/M4_hotspots.md §4] [src: method:handbook/implement-a-scan.md §3. Build the scoping brief]

## Assumptions and limits

The ranking depends on the priorities, weights and reference frame chosen. Ordinal settings are conventions rather than measured ratios of value. Correlated indicators may represent different policy concerns even when one is selected to avoid statistical duplication. Relative ranks cannot be compared across countries as measures of absolute need without a common reference. [src: methodology/modules/M4_hotspots.md §9] [src: methodology/framework.md §Variable selection (two stages)]

Missing or coarse data can hide local disadvantage. Sensitivity tests reveal dependence on tested choices; they do not validate the inputs or prove a single best allocation. Stakeholder review and field assessment must test whether the shortlist reflects the intended investment priorities. [src: method:handbook/implement-a-scan.md §3. Build the scoping brief]

## Where this is configured

[[table:T5]] defines priorities and descriptors. [[table:T1]] and [[table:BIND]] describe the inputs and their spatial support; [[table:T7]] defines comparison units. The run record supplies the selected priorities, final weights, scaling, class boundaries and sensitivity scenarios. [[table:T2]] supports the check against counting climate-risk components twice.

The shared classification contract defines the active calculation. Historical index modes, theme defaults and T6 effect multipliers are not imported into it. [src: method:priority/README.md]
