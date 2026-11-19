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

This chapter gives the shared reasoning and its limits. The next chapter describes agent-led T4 synthesis; the following chapters describe effect and economic methods. Historical T4 algorithms are kept separately for reproduction of the pinned evidence edition. Shared guidance does not prescribe one automatic algorithm or introduce new numerical weights.

| Output | Unit of synthesis | What is combined | Detailed method |
|---|---|---|---|
| T4 suitability | Family × variable × declared context | Compatible implementation constraints, thresholds or response profiles | [[ch:suitability-synthesis]] |
| T3 hazard response or asset threat | Practice/family × hazard × scope, with the relevant role kept separate | Claims about hazard mitigation, or claims about damage to the investment | [[ch:effect-synthesis]] |
| T6 scorecard effect | Practice/family × priority outcome × scope | Outcome claims routed through the target crosswalk, with comparator, beneficiary and proximity retained | [[ch:effect-synthesis]] |
| T6E economic profile | Practice/family × economic indicator × scope | Cost or economic observations with the required unit, denominator and context | [[ch:cost-profiles]] |

[src: schema/spec.md §T3] [src: schema/spec.md §T4] [src: schema/spec.md §T6] [src: methodology/T3_T6_generation_method.md §7]

T0, T1, T2, T5 and T7 need justified configuration decisions rather than this same pooling operation. For example, choosing a spatial dataset requires fitness for purpose; setting hotspot priorities requires explicit decision preferences. Neither can be settled by counting papers. Their roles and links to the relevant module methods are set out in [[ch:evidence-principles]].

## A sequence for synthesis

Use the following sequence to make the reasoning inspectable. Its gates consolidate the existing suitability and effect methods. The additional dependence and sensitivity checks below are review guidance where the current compiler does not implement them. [src: methodology/T4_generation_method.md §6] [src: methodology/T3_T6_generation_method.md §7]

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

Eligibility and weighting are different decisions. T3/T6 uses explicit context-distance factors for eligible effects, whereas T4 numeric-profile pooling requires an approved compatible pool. T6E applies outright income-band and unit gates to monetary ranges. A discount cannot rescue a claim that fails the relevant eligibility gate. [src: methodology/T4_generation_method.md §Reviewed numeric class tables] [src: methodology/T3_T6_generation_method.md §5] [src: methodology/T3_T6_generation_method.md §7.7]

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

### What the historical edition implements

The historical controls differ. The earlier T4 compiler resolves citation lineage and applies its declared source/origin balancing; approved ordinal-profile pools permit one independent-origin contribution per interval or endpoint. T3/T6 resolves lineage but retains a source's eligible own arms, with a within-cell share factor of `1/k` across its `k` own units. T6E uses the effect machinery and adds economic eligibility and replication gates. The specialist chapters give the exact rules. [src: src/nbs_ruralscan/recipe/synthesis.py §_resolve_root_origin] [src: methodology/T4_generation_method.md §Reviewed numeric class tables] [src: src/nbs_ruralscan/recipe/cell_synthesis.py §dedupe_for_cells]

These controls do not automatically identify shared datasets across unlinked papers, overlap between reviews and their primaries, or correlated observations. The effect share factor prevents influence increasing simply with the number of own arms; those arms can still have different design and context weights. It is not a covariance model or a guarantee that the resulting publications are independent.

For new synthesis proposals, report record, publication and identified-origin counts separately, including unknown origins. Where overlap matters, prepare a documented inclusion decision or dependency-aware analysis for review. An agent-led T4 proposal must state and justify its synthesis choices; it must not silently rewrite the provenance of historical outputs. The [source-contribution plan](https://github.com/RuralScan/method/issues/44) tracks unresolved implementation work.

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

The current synthesis weights are policy judgements, not inverse-variance meta-analysis weights. Their exact factors belong in [[ch:suitability-synthesis]] and [[ch:effect-synthesis]], where their roles can be interpreted alongside eligibility, design and transfer rules. The historical factors include mixed `claim_basis` labels. Separating knowledge basis and extraction format corrects the classification model; it does not itself approve replacement numerical factors or recalibrate past outputs. [src: method:data-model/evidence-classification.json]

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

## Agent synthesis, validation and historical reproduction

For new T4 mappings, an AI agent will interpret reviewed evidence and derive a traceable proposal. Scientific review assesses that interpretation; deterministic code validates and packages the accepted mapping. Code that checks a schema or evaluates a curve is not the agent's scientific reasoning process. [[ch:suitability-synthesis]] describes the adopted route and its required decision record.

The rows displayed in this pinned evidence edition were produced by earlier compiler code. Their algorithms remain available in [[ch:t4-legacy-compiler]] and in the effect/economic chapters. They are not evidence of a completed production agent run, and the T4 change does not imply that T3/T6/T6E have changed synthesis method. Reproduce accepted agent outputs from their recorded decisions and validated representation; do not promise that a fresh model run will repeat the same judgement.

## Assumptions and limits

A pooled result is conditional on search coverage, source validity, dependence, compatibility and policy choices. Agreement among repeated or selectively reported claims can remain misleading. A narrow spread is not proof of low uncertainty, and absence of reported failures is not proof of safety or feasibility.

The implemented lineage and source-sharing controls are useful but incomplete representations of study dependence. Sensitivity analyses and new statistical pooling require recorded methods and validation before their results can be presented as operational. Local feasibility must still test transfer, engineering requirements, costs and implementation conditions.

## Where this is configured

[[table:EV]] and [[table:SRC]] provide claims, provenance, context and lineage; [[table:FAM]], [[table:VONT]] and [[table:XW]] provide families, quantities and routes. The agent proposal and accepted mapping govern new T4 synthesis; [[table:T4_RUN]] records execution settings. [[table:T4_NUMERIC_POLICY]] documents historical numeric compilation. [[table:BANDS]] and effect lookups govern effect and economic classification. The historical T4 record and specialist effect/economic chapters identify the pinned factors and code used for [[table:T4]], [[table:T3]], [[table:T6]] and [[table:T6E]].
