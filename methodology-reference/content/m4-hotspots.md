---
title: "M4: Priority hotspots"
slug: m4-hotspots
summary: Rank candidate areas by declared development priorities and explain the weights, drivers and sensitivity of the shortlist.
sources:
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
| T5 priority settings | Identify eligible indicators, direction and scaling rules. |
| Recorded user weights | State the relative emphasis on each selected priority. |
| Geographic units | Define the areas to be compared and shortlisted. |
| M2b risk flags, if used | Provide a separate investment-risk screen. |

[src: methodology/modules/M4_hotspots.md §3]

Only T5 rows marked `priority` enter the score. Descriptors such as population counts provide context. Country-level values cannot distinguish locations within a country; they are reported as context or qualified flags rather than as spatially differentiating priorities. [[ch:m3-characterisation]] describes this screening and the treatment of related indicators. [src: methodology/opportunity_space_T5.md §Spatial-grain rule]

## Method

### 1. State what a high priority value means

Each indicator needs a declared direction, scaling rule and reference frame. A high value must consistently mean more of the concern being prioritised. Priority scaling is therefore different from suitability, where an intermediate optimum may be appropriate. [src: methodology/modules/M4_hotspots.md §9]

A **fixed reference** uses externally justified thresholds and supports comparisons across places or time. A **relative reference** ranks conditions within a stated area or distribution. Relative ranking helps reveal local contrasts, but even a low-need area will have a highest-ranked location. Show raw values and their units beside transformed scores so relative rank is not mistaken for absolute severity. [src: methodology/modules/M4_hotspots.md §9]

Record the actual transform, bounds or reference distribution used in the application. The data table and the application configuration must identify the same rule; a display label alone is insufficient to reproduce a ranking. [src: methodology/modules/M3_characterisation.md §13] [src: methodology/modules/M4_hotspots.md §9]

### 2. Record the team's priorities and weights

The module specification offers the settings none, low, medium and high, coded 0, 1, 2 and 3 and normalised across the selected priorities:

```formula
w_j = c_j / Σ_k c_k
```

`c_j` is the recorded code for priority `j`; `w_j` is its resulting weight. At least one priority must be selected for the denominator to be non-zero. The coding is a decision convention: it does not measure how much more valuable one outcome is than another. [src: methodology/modules/M4_hotspots.md §6]

An application records the final criterion set and weights, including any theme-level choices and treatment of related indicators. Its rationale should be understandable in terms of the investment question. Re-run with plausible alternative priorities and weights to show which assumptions drive the shortlist. [src: schema/spec.md §Theme weights and NbS-response layers] [src: method:handbook/implement-a-scan.md §3. Build the scoping brief]

Weights extracted from published models describe those models' emphasis. Study counts and evidence-quality weights serve different purposes. None automatically becomes the team's priority weight. Detailed treatment of literature weights belongs in [[ch:suitability-synthesis]]. [src: methodology/weight_normalisation.md §Scope - evidence, not an MCDA input]

### 3. Combine priorities within the candidate area

The module's weighted-overlay formulation is:

```formula
H(x) = Σ_j w_j p_j(x),       Σ_j w_j = 1
```

`H(x)` is the priority index at location `x` within the opportunity space, `p_j(x)` is the standardised value of selected priority `j`, and `w_j` is its recorded weight. Outside that space no hotspot score is assigned. [src: methodology/modules/M4_hotspots.md §6]

A weighted sum is compensatory: a strong contribution from one priority can offset a weak contribution from another. Show the main drivers of each shortlisted area's rank so a high combined score is not interpreted as high need on every indicator. [src: methodology/modules/M4_hotspots.md §13]

Keep the two risk lenses separate. Livelihood climate risk may contribute to need, but its component variables must not be counted again as independent priorities. Investment risk from M2b is a flag or chosen filter, never an additional term in `H`. State whether climate need was represented through separate hazards or a composite; do not include both. [src: methodology/modules/M4_hotspots.md §7] [src: methodology/modules/M2_climate_risk.md §10]

### 4. Rank areas and show suitability alongside priority

Use the application's declared geographic units and aggregation measure to rank candidate areas. Record whether the ranking reflects mean priority, the share above a chosen threshold, or another documented summary. Show the strongest contributing priorities, data coverage and relevant population or production totals with their denominators. [src: methodology/modules/M4_hotspots.md §6] [src: method:handbook/implement-a-scan.md §3. Build the scoping brief]

Display suitability and priority as separate dimensions. A high-suitability, high-need area answers a different planning question from a high-suitability, low-need area. Class boundaries and the number of display classes belong in the map legend and run record. Quantile classes are relative positions in the stated distribution, not universal severity thresholds. [src: methodology/modules/M4_hotspots.md §8] [src: methodology/modules/M4_hotspots.md §9]

### 5. Test whether the shortlist changes

Repeat the ranking with plausible alternative priority settings and document which areas remain prominent and which move substantially. Record the settings tested and the resulting rank changes. Where data coverage or scaling choices could change the result, assess those alongside weights rather than treating weight sensitivity as total uncertainty. [src: method:handbook/implement-a-scan.md §3. Build the scoping brief]

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
