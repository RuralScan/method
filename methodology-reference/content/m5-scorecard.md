---
title: "M5: NbS scorecard and response"
slug: m5-scorecard
summary: Compare evidence-supported benefits, harms, confidence, context and indicative costs without turning them into site-level predictions.
sources:
  - methodology/modules/M5_scorecard.md
  - schema/spec.md
  - methodology/T3_T6_generation_method.md
  - schema/lookups/scorecard_locus.csv
  - schema/lookups/scorecard_chip_scale.csv
  - AGENTS.md
  - methodology/T4_generation_method.md
  - schema/T5_opportunity_space.csv
---

## Question this module answers

Module 5 (M5) asks what a nature-based solution could plausibly contribute to the problems identified in the opportunity space, with what confidence, under which conditions and at what indicative cost. It supports comparison of practices; it does not calculate project returns or predict site-level effects. [src: methodology/modules/M5_scorecard.md §2]

## Inputs

The comparison draws on effect rows in [[table:T6]], hazard-response evidence in [[table:T3]], indicative economic profiles in [[table:T6E]] and the problem distributions described by M3. Each effect retains its supporting evidence, applicability conditions and confidence. [src: methodology/modules/M5_scorecard.md §3] [src: schema/spec.md §T6 - NbS Scorecard - Effects and Economic Profile]

The detailed synthesis rules belong in [[ch:effect-synthesis]] and [[ch:cost-profiles]]. M5 explains how to read their outputs together. It does not derive new classes or costs from display symbols.

## Method

### 1. Pair the local problem with the evidence of response

For each concern, show its presence in the candidate area beside the evidence-supported response of the practice. Keep these as separate quantities. A strongly supported effect on a problem that is barely present locally may be less relevant than a moderate effect on a widespread concern. [src: methodology/modules/M5_scorecard.md §6]

T6 rows refer to development priorities; T3 hazard rows can additionally distinguish farming systems and whether the evidence concerns livelihood mitigation or threats to the asset. Read that scope before comparing them. [src: methodology/T3_T6_generation_method.md §1]

### 2. Keep effect, confidence and applicability separate

Table: Questions to ask when reading an effect rating.

| Dimension | What it tells the reader |
|---|---|
| Direction and class | Whether the evidence supports benefit, harm or no relationship, and the ordinal size of that effect. |
| Confidence | How the amount and quality of evidence combine with agreement among findings. |
| Applicability | Whether the evidence matches the target geography, farming system and conditions. |
| Effect location | Whether benefits occur on-farm, downstream, across the landscape or as a wider public good. |
| Directness and conditions | Whether outcomes were measured directly or inferred through proxies, and what implementation conditions matter. |

[src: methodology/T3_T6_generation_method.md §7.4] [src: methodology/T3_T6_generation_method.md §5.5] [src: schema/lookups/scorecard_locus.csv]

A small effect can have high confidence; a large reported effect can have low confidence. Confidence is not effect size, and neither establishes transferability. Evidence outside the target context remains qualified; where no applicable evidence supports a rating, show that gap rather than silently applying a global class. [src: methodology/T3_T6_generation_method.md §7.4] [src: methodology/T3_T6_generation_method.md §5.5]

### 3. Preserve disagreement, gaps and harm

Table: Evidence states that must remain distinguishable in a comparison.

| State | Meaning |
|---|---|
| No relationship | Evidence supports a null relationship. |
| Conflicting evidence | Material findings point in opposing directions. |
| Data deficient | Findings exist but cannot support a class. |
| Not assessed | No assessment row is available. |
| No applicable evidence | Available evidence does not support a rating for the target context. |

[src: schema/spec.md §T6 - NbS Scorecard - Effects and Economic Profile] [src: methodology/T3_T6_generation_method.md §5.5] [src: schema/lookups/scorecard_chip_scale.csv]

Opposing benefit and harm findings must not disappear into an apparent zero effect. Retain measured harms and adverse outcomes even when the overall class is favourable. Explain the people, places or conditions to which they apply. [src: methodology/T3_T6_generation_method.md §7.8] [src: AGENTS.md §What is locked]

### 4. Compare costs on compatible terms

Use the separate T6E economic profile. State currency, unit, denominator, establishment or recurrent period and any contextual qualification. Numerical ranges are shown only where the economic synthesis supports them; otherwise retain the indicative class or evidence gap. Do not calculate a new ratio from unrelated benefit and cost rows. [[ch:cost-profiles]] gives the detailed compatibility and reporting rules. [src: methodology/T3_T6_generation_method.md §7.7]

Indicative costs are not a cost-benefit analysis. They cannot establish affordability, financial viability or cost-effectiveness for a particular investment without local design, cost and benefit assessment. [src: methodology/modules/M5_scorecard.md §2]

### 5. Make trade-offs visible

Compare practices against the same concerns while retaining their different contexts, footprint units and effect locations. A line of riparian vegetation, an area of restored woodland and an unmapped practice cannot be compared by treating all candidate pixels as planted hectares. [src: methodology/T4_generation_method.md §2.4 Spatial product type & the resolution trap]

Keep different outcomes visible rather than reducing the comparison to one overall “best practice” score. For example, on-farm water availability and catchment water yield are distinct outcomes: a practice may improve one while reducing the other. A combined display should retain the underlying findings so that this trade-off remains visible. [src: schema/T5_opportunity_space.csv]

## Reading the comparison

High local need and positive response evidence together support further investigation. They do not establish a causal project benefit. Show suitability, local need, response evidence and investment risk alongside one another, with a clear path from each rating to its evidence units, source and locator. [src: methodology/modules/M5_scorecard.md §8]

## Outputs

Provide a concern-by-practice comparison with effect direction and class, confidence, context, conditions and evidence links. Include the separate cost profile and the qualifications needed to interpret it. Record which evidence edition and application context the comparison uses. [src: methodology/modules/M5_scorecard.md §4]

## Assumptions and limits

Ratings summarise the literature as extracted, not validated predictions for the site. A class resting on few independent sources may change when one source is removed. Counts describe coverage, not strength, and published evidence can over-represent successful outcomes. Feasibility work must quantify the effects and costs that matter locally and test the conditions on which the comparison depends. [src: methodology/T3_T6_generation_method.md §7.8] [src: methodology/modules/M5_scorecard.md §2]

## Where this is configured

[[table:T6]] holds effect rows, [[table:T3]] hazard responses and [[table:T6E]] economic profiles. [[table:T5]] defines the concerns being compared. [[table:EV]] and [[table:SRC]] hold the evidence trail. Synthesis, confidence and magnitude rules are explained once in [[ch:effect-synthesis]] and [[ch:cost-profiles]].
