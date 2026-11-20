---
title: Combining evidence into analytical tables
slug: compiling-evidence
summary: Decide which reviewed claims can be combined, account for dependence and uncertainty, and select the synthesis method appropriate to each table.
sources:
  - methodology/T4_generation_method.md
  - methodology/T3_T6_generation_method.md
  - methodology/T4_developer_contract.md
  - methodology/T4_variable_importance.md
  - method:data-model/evidence-classification.json
  - src/nbs_ruralscan/recipe/synthesis.py
  - src/nbs_ruralscan/recipe/cell_synthesis.py
---

## From reviewed claims to a specified output

Review establishes what a claim can support within its recorded scope. Synthesis decides how eligible claims contribute to a particular analytical output. It may produce a numeric rule, an ordinal class, conditional alternatives, a qualitative statement or an unresolved hold. A faithfully extracted number is not automatically eligible for every output. [src: methodology/T4_generation_method.md §0] [src: methodology/T3_T6_generation_method.md §7]

This chapter gives the shared reasoning and its limits. The next chapter describes agent-led T4 synthesis; the following chapters describe effect and economic methods. Historical editions remain immutable; their retired algorithms are not supported production routes. T3/T6 scientific judgments now follow the AI-led proposal/acceptance workflow. Shared guidance does not prescribe one automatic algorithm or introduce new numerical weights.

| Output | Unit of synthesis | What is combined | Detailed method |
|---|---|---|---|
| T4 suitability | Family × variable × declared context | Compatible implementation constraints, thresholds or response profiles | [[ch:suitability-synthesis]] |
| T3 hazard response or asset threat | Practice/family × hazard × scope, with the relevant role kept separate | Claims about hazard mitigation, or claims about damage to the investment | [[ch:effect-synthesis]] |
| T6 scorecard effect | Practice/family × priority outcome × scope | Outcome claims routed through the target crosswalk, with comparator, beneficiary and proximity retained | [[ch:effect-synthesis]] |
| T6E economic profile | Practice/family × economic indicator × scope | Cost or economic observations with the required unit, denominator and context | [[ch:cost-profiles]] |

[src: schema/spec.md §T3] [src: schema/spec.md §T4] [src: schema/spec.md §T6] [src: methodology/T3_T6_generation_method.md §7]

T0, T1, T2, T5 and T7 need justified configuration decisions rather than this same pooling operation. For example, choosing a spatial dataset requires fitness for purpose; setting hotspot priorities requires explicit decision preferences. Neither can be settled by counting papers. Their roles and links to the relevant module methods are set out in [[ch:evidence-principles]].

## A sequence for synthesis

Use the following sequence to make the reasoning inspectable. It brings together the shared questions in the suitability and effect methods. Dependence and sensitivity are explicit AI reasoning and scientific review requirements. [src: methodology/T4_generation_method.md §6] [src: methodology/T3_T6_generation_method.md §7]

1. **Specify the decision.** Identify table, practice/family, target quantity, intended context and output. Retrieve the previously accepted rule and its approval scope.
2. **Assemble the candidate record.** Include contrary findings and identify dropped, held, out-of-scope and eligible units. Preserve reasons rather than silently removing inconvenient claims.
3. **Check comparability before weighting.** Match claim meaning, intervention, comparator, measurement, scale, context and units. A unit conversion does not resolve a conceptual mismatch.
4. **Account for dependence.** Identify the underlying studies, datasets, projects, response profiles and judgements represented by the publications and rows. Record unresolved overlap.
5. **Choose the supported representation.** Apply the relevant table's method. Preserve source profiles and conditional alternatives when one pooled value would be misleading.
6. **Assess uncertainty and consequential choices.** Distinguish transcription, validity, disagreement, dependence, transfer and design uncertainty. Test material choices where feasible and state what remains untested.
7. **Record and review the proposal.** Show contributing and excluded evidence, transformations, policy versions, comparison with the previous result, rationale and remaining holds. Compile and release only through the authorised workflow.

## Compatibility precedes weighting

| Dimension | Question to resolve | Consequence if unresolved |
|---|---|---|
| Claim meaning | Occurrence, an establishment limit, an effect, a risk or a cost? | Keep separate; observed presence is not a threshold and an effect is not an eligibility rule |
| Practice and management | Same establishment pathway, host system and intervention components? | Split families or contexts, or document a justified transfer |
| Measured quantity | Same metric, statistic, depth, period and measurement method? | Retain distinct profiles; annual and growing-season rainfall are not equivalent because both use millimetres |
| Comparator and beneficiary | Same baseline and affected population or asset? | Keep effect scopes separate; do not attribute a programme bundle to one practice without support |
| Spatial support | Same point, plot, landscape or grid meaning? | Assess compatibility with the runtime dataset rather than equating unlike spatial summaries |
| Scale and denominator | Cardinal measurement, ordinal category, relative change, per-hectare amount or annual flow? | Use the table's declared conversion or hold; never average unmatched scales |
| Transfer context | Relevant climate, farming system, income context and implementation conditions? | Apply the table-specific scope and transfer policy; unknown context is not evidence of a match |

[src: methodology/T4_developer_contract.md §Cross-paper harmonisation] [src: methodology/T3_T6_generation_method.md §3] [src: methodology/T3_T6_generation_method.md §5]

Eligibility and weighting are different decisions. T3/T6 uses explicit context-distance factors for eligible effects, whereas a new T4 proposal must justify which profiles are compatible and how they contribute. T6E applies outright income-band and unit gates to monetary ranges. A discount cannot rescue a claim that fails the relevant eligibility gate. [src: methodology/T4_generation_method.md §Reviewed numeric class tables] [src: methodology/T3_T6_generation_method.md §5] [src: methodology/T3_T6_generation_method.md §7.7]

## Repeated observations, publications and author groups

Keep three units distinct: extracted records, reporting publications and underlying study/data or judgement origins. A paper may contain several studies; several papers may describe one study. Similar values can be independent replications, while different values can be repeated measurements from one experiment. The classification contract requires dependence to be considered rather than inferred from row counts or authorship. [src: method:data-model/evidence-classification.json]

| Situation | Treatment in the synthesis audit |
|---|---|
| A value repeated in text, table, figure, translation or repository copy | Reconcile identity and retain useful locators; do not treat the presentations as independent evidence |
| Several bands or endpoints of one suitability response | Preserve the full profile; its number of extracted rows is not its credibility weight |
| Repeated years, depths, treatments or sites within a study | Keep informative variation and sampling structure; do not automatically call each observation independent |
| Companion papers or project reports sharing data | Link origins and record complete or partial sample overlap |
| A meta-analysis and its included primary studies | Identify overlap before allowing both to contribute; publication-level de-duplication alone cannot resolve it |
| The same expert judgement repeated in several works | Retain the cited origin and count the judgement once within the relevant pool |
| Shared authors reporting new studies | Retain new evidence; authorship is a dependency flag, not proof of duplication |
| Different authors reusing one dataset, model or panel | Apply the same dependency checks; different names do not prove independence |
| Uncertain reuse | Record independence as unresolved; examine plausible dependency scenarios rather than claim certainty |

Historical records remain recoverable. Resolving duplication changes eligibility or influence, not the existence of the evidence trail. Use `lineage_of` where its semantics fit and record fuller overlap and study structure in the synthesis audit. Do not imply that author-group or sampling-covariance fields already exist in the registry. [src: schema/spec.md §EV] [src: method:data-model/evidence-classification.json]

### Worked illustration: nine records are not nine replications

This hypothetical example concerns one outcome and target context. All four publications are relevant, but their data overlap.

Table: Hypothetical publications representing two underlying experiments.

| Publication | Extracted records | Underlying origin | Decision to document |
|---|---:|---|---|
| A: trial report | 3 annual observations | Experiment 1 | Retain time variation; years are repeated observations, not three independent experiments |
| B: companion paper | The same 3 annual observations | Experiment 1 | Link to A; resolve duplicate reporting rather than give the result another vote |
| C: new trial by the same author group | 2 treatment comparisons | Experiment 2 | Keep the new experiment; assess dependence between its treatment arms |
| D: review summarising A and C | 1 pooled estimate | Experiments 1 and 2 | Choose the review or primary level for the target question, or justify explicit overlap treatment |

There are nine extracted records, four publications and two identified primary data origins. Keeping all nine records for provenance does not require weighting all nine as independent contributions. Excluding C merely because its authors recur would discard new evidence; counting D as an extra independent experiment would repeat existing evidence. If D also included untraced studies, the origin count would be unresolved rather than assumed to remain two. [src: method:data-model/evidence-classification.json]

The decision record should state which estimates answer the target question, how repeated observations are handled and what changes when each independent origin is left out. This is an illustration of the audit, not a new numerical weighting rule.

### Current scientific responsibility

AI proposals must report records, publications and identified origins separately,
including unresolved overlap. Explain how repeated observations and review/primary
relationships affect the judgment. Historical source-share factors do not calculate
new judgments. Scientific review assesses the account; code checks complete candidate
dispositions and preserves the accepted output. See [[ch:effect-synthesis]] and
[[ch:suitability-synthesis]].

## Different meanings of weight

| Quantity | Meaning | Must not be read as |
|---|---|---|
| Literature support | Frequency within a defined searched or screened cohort | Agreement on a threshold, independent replication or probability of success |
| Evidence credibility weight | A claim's relative influence under a declared synthesis policy | Statistical precision or probability that the claim is true |
| Statistical precision weight | Influence derived from an estimate's uncertainty in an appropriate statistical analysis | A label that can be attached to heuristic credibility multipliers |
| Within-study variable importance | Emphasis within the source's own model and denominator | A transferable response curve or approved Rural Scan criterion weight |
| Runtime criterion weight | Contribution of a selected variable to a spatial calculation | A copy of source credibility or publication frequency |
| Priority preference | Importance assigned to decision outcomes | Evidence that physical suitability or an effect has changed |

[src: methodology/T4_variable_importance.md] [src: methodology/T4_generation_method.md §6] [src: methodology/modules/M4_hotspots.md] [src: methodology/T3_T6_generation_method.md §7]

New T3/T6 and T4 proposals justify scientific influence and pooling choices. Fixed historic design weights, lineage discounts and confidence matrices are not new defaults. Code checks the proposal and exact acceptance; it does not compute these judgments. Historical values keep their historical provenance. See [[ch:effect-synthesis]] and [[ch:suitability-synthesis]].

A source tier may already consider context, independence and authority. Additional discounts need a stated rationale so the same weakness is not penalised repeatedly without consideration. Conversely, a high tier cannot supply missing source context or make a practitioner rating a measured effect. Increasing numerical precision in the output does not remove these limitations.

## Choosing a defensible result

For new T4 mappings, the agent interprets compatible constraints and response profiles, proposes a representation and exposes its judgement for review. Direction without supported boundaries can remain useful while numerical calibration is held. It does not become a fitted curve by borrowing an effect-synthesis formula. [[ch:suitability-synthesis]] explains what the agent must specify about shape, parameters and endpoints.

T3/T6 reconciles eligible claims into ordinal effect classes with evidence and agreement assessments and an applicability envelope. It does not pool every percentage, standardised effect and narrative as one continuous effect size. A formal meta-analysis would require a separately specified estimand, compatible estimates, uncertainty and dependence treatment. [[ch:effect-synthesis]] gives the current reconciliation method.

T6E keeps cost classes and monetary ranges distinct. A published range describes qualifying observations; it is not a confidence interval or a local budget estimate. Matching a unit label does not harmonise price years, cost scope or project design. [[ch:cost-profiles]] gives the current gates and remaining limitations.

One claim can legitimately inform different outputs through the crosswalk. Its appearance in both T3 and T6 does not create a second independent source. Nor does that reuse establish that downstream criteria are independent; correlated priority layers require the separate selection and clustering treatment in [[ch:m4-hotspots]]. [src: schema/spec.md §XW] [src: methodology/modules/M4_hotspots.md]

## Uncertainty, sensitivity and the decision record

Recommended review checks should target choices capable of changing the conclusion. They are not claims that every published row has undergone these analyses.

- Leave out one identified origin at a time. If related studies dominate, also inspect leave-one-author-group-out results; this diagnoses concentration rather than declaring all work by one group a single study.
- Compare the stated credibility policy with an equal-origin diagnostic and, where informative, a measured/validated subset. Keep eligibility and context consistent so the comparison has a clear meaning.
- Test plausible overlap assumptions where independence is unresolved. Keep incompatible contexts separate rather than manufacture agreement by pooling them.
- For T4, examine boundary inclusion, missing tails and alternative approved source profiles. For T3/T6, inspect changes in class, direction, agreement and contributing origins. For T6E, inspect denominator, scope and price-year differences before interpreting a range.
- Where spatial application exists, report changes in affected locations, classes or ranks, and area only for products that permit area reporting. Otherwise state that map sensitivity remains untested.

The review record should identify inputs and revisions, candidate dispositions, compatibility groups, origin accounting, transformations, numerical policies, sensitivity results, unresolved holds and approval scope. An AI-assisted proposal additionally needs its prompt or immutable task reference, skill version and actual model/settings where available. Missing settings are recorded as missing. Replay should use accepted inputs and decisions, rather than ask an AI to reinterpret them afresh. [src: methodology/T4_generation_method.md §Synthesis decision record]

## Reproducing the accepted output

The displayed edition retains its original analytical outputs. Historical T4 records remain in immutable Git editions; the retired T4 synthesis route is no longer offered by current workflows. For a newly accepted agent-led T4 mapping, replay the archived decision and validated representation. The workflow and implementation boundary have one home in [[ch:suitability-synthesis]]; a fresh model run is not a reproducibility guarantee. [[ch:effect-synthesis]] and [[ch:cost-profiles]] document the existing effect and economic implementations.

## Assumptions and limits

A pooled result is conditional on search coverage, source validity, dependence, compatibility and policy choices. Agreement among repeated or selectively reported claims can remain misleading. A narrow spread is not proof of low uncertainty, and absence of reported failures is not proof of safety or feasibility.

AI origin accounting and source review remain necessary to assess study dependence. Sensitivity analyses and new statistical pooling require recorded methods and validation before their results can be presented as operational. Local feasibility must still test transfer, engineering requirements, costs and implementation conditions.

## Where this is configured

[[table:EV]] and [[table:SRC]] provide claims, provenance, context and lineage; [[table:FAM]], [[table:VONT]] and [[table:XW]] provide families, quantities and routes. The agent proposal and accepted mapping govern new T4 synthesis; [[table:T4_RUN]] records execution settings. [[table:BANDS]] and effect lookups govern effect and economic classification. The specialist effect/economic chapters identify the pinned factors and code used for [[table:T3]], [[table:T6]] and [[table:T6E]].
