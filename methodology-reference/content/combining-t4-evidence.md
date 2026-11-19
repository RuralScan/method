---
title: Combining evidence and weighting T4
slug: combining-t4-evidence
summary: Combine compatible evidence with explicit dependency, weighting and uncertainty decisions.
sources:
  - method:data-model/evidence-classification.json
  - methodology/T4_generation_method.md
  - schema/spec.md
---

T4 synthesis authors, scientific reviewers and runtime implementers.  
**Companion:** [Evidence registry and source limitations](ch-evidence-registry.html).

T4 synthesis should combine evidence only when it addresses the same practice, measured quantity and application context. Weighting cannot make incompatible claims comparable. A synthesis may legitimately end with a qualitative relationship, several conditional profiles or an explicit calibration gap instead of one executable curve.

This guide distinguishes **current rules**, **historical implementation** and **proposed improvements**. It describes local revision `9d84fd9900b9c913804a9f94eb6f9779f2734994`. The current [synthesis skill](https://github.com/CIAT/nbs_ruralscan/blob/9d84fd9900b9c913804a9f94eb6f9779f2734994/.agents/skills/source-command-t4-synthesise/SKILL.md), [T4 review contract](https://github.com/CIAT/nbs_ruralscan/blob/9d84fd9900b9c913804a9f94eb6f9779f2734994/.agents/skills/extraction_contracts/T4_review_contract.md), approved recipe inputs and recorded decisions remain authoritative.

## 1. Keep five different numerical questions separate

| Quantity | Meaning | What it must not become |
|---|---|---|
| **Literature support** | How many sources in an explicitly defined cohort use/support this variable? Current headline `paper_support_pct = 100 × n_sources / corpus_n`. | An agreement rate on a threshold, a probability of suitability or a runtime weight. |
| **Evidence credibility weight** | Relative influence of an eligible source/claim in a particular synthesis. | A physical response or statistical precision unless derived from an appropriate statistical model. |
| **Within-study importance** | Emphasis assigned to a criterion in the source's own model, on its own variable set and hierarchy. | A transferable ecological importance or automatically approved recipe weight. |
| **Suitability response score** | How a value of a spatial variable maps to a declared suitability scale. | A calibrated probability of establishment when it is only an ordinal/design score. |
| **Runtime criterion weight** | How much a selected variable contributes to the opportunity-space calculation. | A copy of publication frequency, source credibility or an unreviewed literature weight. |

Stakeholder preferences in hotspot prioritisation are another decision layer. They express priorities across outcomes; they should not rewrite the physical conditions for establishment.

The [October support decision](https://github.com/CIAT/nbs_ruralscan/blob/9d84fd9900b9c913804a9f94eb6f9779f2734994/methodology/decisions/2026-10-28_t4_support_reporting.md) makes the headline fraction unweighted. A separate `quality_weighted_pct` diagnostic requires complete screened membership and known tiers. A model-use cohort has a different denominator from the screened literature corpus; label each explicitly. Neither permits a causal or independent-study interpretation merely from a paper count.

## 2. A sequence for defensible synthesis

1. **Define the decision.** State the NbS family, target variable, intended geography, host system, spatial product and whether the decision concerns variable inclusion, direction, calibration or a hard exclusion. Retrieve the previous accepted rule and its rationale.
2. **Assemble the candidate record.** Include relevant active evidence, contrary findings, source profiles, review status and recorded holds. Log every candidate's disposition. Do not hide unresolved evidence by omitting it from the summary.
3. **Apply the source and claim gates.** Confirm that the source establishes spatially usable implementation conditions. Separate site descriptors, species selection, benefit prioritisation, engineering design and soft operational constraints.
4. **Form compatibility groups.** Compare practice, quantity/statistic, units, soil depth or averaging period, spatial support, host system, management and climate context. Convert only equivalent quantities. Keep incompatible profiles separate.
5. **Resolve dependencies.** Reconcile duplicate identities and claim/model lineages, including multiple data points within a source and related publications from the same author group. Identify shared datasets, sites, panels and borrowed thresholds. Count independent origins for pooled calibration, while preserving data-point and reporting-paper counts separately. Shared authorship alone neither proves duplication nor establishes independence.
6. **Assess three outputs separately.** Record evidence for variable use, suitability direction and numeric calibration. Preserve full quantitative source profiles even when global transfer is unresolved. A numerical plausibility problem can hold calibration without discarding useful direction.
7. **Choose the supported representation.** Use a categorical gate, scoped range, ordinal profile, continuous curve or qualitative statement only where its meaning is supported. Explain missing tails, endpoint conventions, interpolation and exclusions.
8. **Combine eligible profiles under an explicit policy.** Record source weights, score crosswalks, pool membership, disagreement and coverage. Evaluate consequential boundary cases. A compatible unit is not, by itself, permission to pool.
9. **Test the proposed rule and record the decision.** Compare with the accepted rule, show what locations or illustrative sites change, review uncertainty and sensitivity, and retain rationale, holds and reviewer scope.
10. **Compile from accepted inputs.** Pin evidence, policy, dataset binding and authoring decisions. Use the deterministic compiler and release workflow so replay does not depend on a fresh AI interpretation.

These steps consolidate the current skill and method. They do not authorise a new discovery sweep or changes to accepted recipes.

## 3. Compatibility precedes weighting

| Check | Example of a consequential difference | Treatment |
|---|---|---|
| Practice and establishment pathway | Planting trees versus assisted regeneration. | Separate families unless a documented transfer is defensible. |
| Claim meaning | Rainfall at observed sites versus a stated establishment limit. | Retain occurrence as context; do not pool it as a limit. |
| Quantity | Annual mean rainfall versus growing-season rainfall; soil stock versus concentration. | Different quantities remain separate even if unit labels overlap. |
| Spatial support | Plot slope versus mean slope of a large grid cell. | Match the runtime layer and aggregation meaning; derive terrain variables before aggregation. |
| Measurement method | Soil pH measured in different solutions; carbon measured at different depths. | Require an explicit comparable basis or retain separate profiles. |
| Management and host | Irrigated versus rainfed; different crop requirements. | Preserve conditions and crop policy; use contextual rules where appropriate. |
| Score meaning | Local rank classes versus measured survival probability. | Never average as if both were cardinal values on the same scale. |
| Independence | A manual, paper and WOCAT entry repeat one recommendation. | One underlying calibration origin; keep the three documentary links. |

Absent contextual metadata is an unresolved eligibility question, not evidence of a match. Ecological transfer cannot be reduced to country proximity or an income-group label.

## 4. Match the combination method to the evidence

| Evidence available | Defensible synthesis | Hold or limitation |
|---|---|---|
| Several explicit inclusion or exclusion conditions | Compare scope and mechanism; preserve legal/system gates separately from graded responses. | A low class or a source-model zero is not automatically a universal hard mask. |
| Comparable continuous thresholds with equivalent meanings | Reconcile parameter values using a declared robust summary, such as the existing weighted-median route; retain source range and provenance. | Do not average optima with absolute limits. Check parameter ordering and avoid inventing a hybrid curve whose joint shape is unsupported. |
| Compatible ordinal class profiles | Map labels through an approved semantic crosswalk; combine step profiles at their breakpoints. | Scores are declared conventions; no interpolation or extrapolation without separate support. |
| Direction without calibrated boundaries | Retain increasing/decreasing/optimum/non-monotonic direction and identify the missing calibration. | Direction supplies no numerical endpoint, score or default weight. |
| Model importance only | Compare within-study emphasis on a compatible scale and complete model denominator. | No response curve follows from importance. |
| Observed practice ranges or WOCAT site descriptors | Summarise documented presence and context; use to frame transfer questions. | Outside the observed range remains unevaluated. Presence is not a complete niche; missing records are not absence data. |
| Expert ranges reported in literature | Preserve the published rationale, context, uncertainty, reported elicitation method and cited origin. | Do not invent missing participant-level data or treat an undocumented panel average as a statistical confidence interval. No new elicitation is in scope. |
| Incompatible or conflicting sources | Retain alternatives, contextual overrides or an unresolved hold. | More low-quality or dependent records cannot resolve a conceptual incompatibility. |

A formal meta-analysis can be appropriate for genuinely comparable effect estimates with uncertainty and dependency information. That is a different task from averaging heterogeneous suitability classes. T3/T6 has its own [effect-generation method](https://github.com/CIAT/nbs_ruralscan/blob/9d84fd9900b9c913804a9f94eb6f9779f2734994/methodology/T3_T6_generation_method.md); it should not silently supply the T4 algorithm.

### Multiple data points from one source or author group

**Dependency accounting, 19 November 2026:** explicitly address dependence within papers and across related author groups. The following handling extends the documentation; new diagnostics or statistical aggregation require implementation and validation before being advertised as operational.

| Situation | Treatment |
|---|---|
| Same value repeated in text, table, figure, translation or repository copy | Retain useful locators and reconcile identity; count the underlying claim once. Do not hard-delete historical EV rows. |
| Several class bands or endpoints describing one source response | Retain the complete response profile. Its ten extracted rows do not give it ten times the influence of a profile stored in one row. |
| Repeated years, depths, treatments or locations in one study | Retain real variation and sampling structure. These can be informative without being independent calibrations. Do not promote each observation to a separate threshold vote. |
| Several independent studies reported in one publication | Distinguish study origins if the source establishes independence and comparable scope. One publication is not necessarily one study; if current lineage representation cannot express this, retain the detail and flag the pooling limitation. |
| Companion papers or overlapping datasets from one author group | Link shared origins and overlapping samples. Pool once at the relevant origin level or use a separately justified dependency-aware analysis; do not count full samples repeatedly. |
| Different author groups reuse a dataset, model, manual or expert panel | Apply the same dependency controls. Different names do not establish independence. |
| Same author group reports genuinely new data | Retain the new contribution; do not merge solely by authorship. Still test whether conclusions depend on that group's shared modelling or judgement conventions. |
| Reuse cannot be resolved | Mark independence unknown. Compare plausible separate-origin and shared-origin scenarios rather than assert either as established fact. |

For each compatibility pool, document publication IDs, underlying study/data or judgement origins, repeated-observation structure, author-group links, evidence of reuse and unresolved overlap. These are information requirements for the synthesis audit, not claims that dedicated registry columns already exist. Use existing lineage fields where their semantics fit; propose a versioned extension if necessary.

The current ordinal-profile rule remains one contribution per independent origin per interval/endpoint. Keep distinct contexts separate and conflicting within-origin profiles unresolved; do not average them simply to clear a hold. More observations may improve knowledge of a source's response, but should not increase credibility weight automatically through row count. Statistical precision-based weighting would require comparable estimates and an explicit treatment of dependency, not sample-size weighting of suitability classes.

Report at least three counts separately: extracted records/data points, reporting publications and identified independent origins. Include unknown-origin counts. Run leave-one-origin-out sensitivity and, where several related studies dominate, leave-one-author-group-out sensitivity. The latter checks concentration of influence; it is not a rule that all work by one team counts as one study.

### Current ordinal-profile convention

The [T4 harmonisation policy](https://github.com/CIAT/nbs_ruralscan/blob/9d84fd9900b9c913804a9f94eb6f9779f2734994/methodology/T4_generation_method.md#reviewed-numeric-class-tables-october-2026-issue-362) supports explicit, compatible step-profile pools. Its approved semantic scores are very low `0.10`, low `0.25`, moderate `0.50`, high `0.75`, very high `0.90`; explicit unsuitable is `0`, explicit optimum is `1`. These values are design conventions, not measured probabilities. Unmapped meanings remain unknown; a source's reported scores and native labels are retained.

Pooling requires an approved `pool_id`, `system_id`, `context_id` and compatibility decision. At each interval and exact endpoint, one independent origin supplies one vote. The compiler retains the source range, eligible/contributing counts and weight coverage. Median ties and zero-versus-positive conflicts do not yield an executable scalar. Missing coverage remains unknown. Pools require explicit selection; a regional pool does not become the global default.

## 5. Evidence weighting needs an explicit interpretation

**Inspected implementation:** [T4 synthesis code](https://github.com/CIAT/nbs_ruralscan/blob/9d84fd9900b9c913804a9f94eb6f9779f2734994/src/nbs_ruralscan/recipe/synthesis.py) contains the following heuristic multipliers:

| Component | Current values |
|---|---|
| Source tier | High `1.0`; medium `0.6`; low `0.35`. |
| Claim basis | `primary_measured=1.0`; `table=0.9`; `modelled=0.7`; `figure_read=0.6`; `expert_assertion=0.5`; `cited_secondary=0.4`. |
| Grey-source adjustment for structural suitability | `0.9` when `source_category=grey`. |

For eligible T4 claims this is a tier × basis × category multiplier. For example, medium-tier expert assertion with grey category receives `0.6 × 0.5 × 0.9 = 0.27`. The number describes relative synthesis influence; it is not a 27% probability that the expert is correct. Context is an explicit eligibility/pool decision in the current harmonisation contract, not an implemented continuous context/recency multiplier.

**Limitations requiring review before formal endorsement:**

- `table` and `figure_read` describe presentation, not research design. Current multipliers can therefore misrepresent the epistemic strength of an otherwise correctly labelled claim.
- A discovery category is an imperfect proxy for bias. A grey report can contain measurements; a journal model can contain unvalidated assertions. Document claim-specific concerns instead of treating venue as conclusive.
- Source tier already includes context, authority and independence considerations. Further discounts can count the same weakness twice unless their rationale is explicit.
- These are policy judgements rather than estimated inverse-variance weights. A large numerical precision in the combined output is not earned by multiplying them.
- The inspected multipliers live in Python constants, despite the project's intended configuration-driven architecture. Formal integration should document and version the actual policy, then consider moving it into approved configuration through a separate change.

**Proposed improvement:** make eligibility the first gate, document design/measurement validity and transfer relevance at claim level, control within-source and cross-publication dependencies, and compare equal-origin weighting with the current quality-weighted result. Include author-group influence checks where relevant. The method decision approved separating knowledge basis from extraction format on 19 November; the schema extension and deterministic migration preserve legacy values; numerical weighting changes require separate review. Flag conclusions that change materially. Do not choose new numerical multipliers in this explanatory guide or change historical tiers automatically.

## 6. Source importance and runtime weights

An Analytic Hierarchy Process (AHP) share, a random-forest importance and a tool slider are different quantities. A slider intensity of 5/10 is not a 50% share of total model importance. Even two shares are difficult to compare when one model contains four variables and another contains fifty. The existing [weight-normalisation note](https://github.com/CIAT/nbs_ruralscan/blob/9d84fd9900b9c913804a9f94eb6f9779f2734994/methodology/weight_normalisation.md) and [variable-importance method](https://github.com/CIAT/nbs_ruralscan/blob/9d84fd9900b9c913804a9f94eb6f9779f2734994/methodology/T4_variable_importance.md) address these distinctions.

For compatible nonnegative source weights, relative-to-mean importance is:

`relative importance = source weight / mean weight across the complete relevant source variable set`

For hierarchical models, the primary diagnostic compares a variable's path contribution with an equal-allocation benchmark following that same hierarchy. Preserve raw weights, within-group ratios, flat ratios, source ranks and the hierarchy-adjusted ratio. Missing siblings or conflicting source tables prevent a settled estimate. Do not infer zero importance from missing data, or remove operational variables from the original denominator merely because Rural Scan routes them elsewhere.

Current recorded decisions keep pooled importance-derived weights as sensitivity scenarios in the bounded slope/rainfall comparison, with equal weights as that comparison's baseline. This does not ratify equal weights for every family, or the pooled pair as a runtime default.

Runtime weights must be declared and reviewed for the actual selected variable set. Thematic grouping and within-area correlation reduction limit double counting. The inherited framework includes AHP, CRITIC and entropy approaches, but data variability and correlation weights describe properties of the input layers, not scientific truth or stakeholder value. The accepted run policy, selected data and implementation determine which method is actually used.

Hard exclusions remain distinct from compensatory weighted scoring: a favourable score on another variable cannot cancel an applicable exclusion. Conversely, missing data must not silently become an exclusion or receive an automatic favourable score. Any missing-layer rule or renormalisation must be explicit and approved.

## 7. Worked examples

All numbers below are hypothetical teaching examples, not new EV records or proposed recipe parameters.

### Observed use cannot provide an exclusion

A WOCAT account reports use at 600–900 mm annual rainfall. A manual describes successful rainfed establishment at 800–1,200 mm under stated soil conditions. Preserve the first as occurrence and inspect whether the second is guidance, an optimum or a tested limit. Averaging their endpoints to 700–1,050 mm invents a meaning neither source supplies. A site receiving 1,300 mm remains unevaluated unless other admissible evidence addresses it.

### Duplicate documents do not create consensus

Three publications repeat one original 15° slope rule. A separate study proposes 20° under comparable conditions. The calibration pool has two known origins, not four independent votes. If their eligible weights tie, report the unresolved median set or retain alternatives; do not invent a 17.5° cutoff solely to obtain one number. A third publication of the first rule does not increase independent support.

If the first rule appears in ten extracted rows, it still supplies one origin's contribution to that comparison. If its author group later reports a genuinely new independent study, retain that new evidence and separately check sensitivity to removing the whole group's work. Authorship is not a substitute for tracing the actual data or judgement origin.

### Ordinal disagreement and missing coverage

At a particular rainfall value, approved compatible profiles report high (`0.75`, weight `0.6`) and moderate (`0.50`, weight `0.4`). Their weighted median is `0.75`; the disagreement range remains `0.50–0.75`. If only the first profile covers a different value, that cell has 60% of eligible weight represented, not full agreement. At equal weights, the two-score median set remains unresolved. If one profile reports zero and the other a positive score, the existing conflict rule prevents an executable pooled scalar.

### Importance depends on the original denominator

In a four-variable model, pH receives 30%, versus a mean of 25%: relative importance `1.2`. In a fifty-variable model, pH receives 5%, versus a mean of 2%: relative importance `2.5`. The smaller raw percentage represents greater relative emphasis in that source. Neither ratio supplies a pH suitability curve or a Rural Scan weight.

### Operational difficulty is conditional

A published manual attributes to practitioners the judgement that manual terracing becomes impractical above a particular slope without machinery. Extract that published statement and its locator; do not create a new consultation record. Preserve the implementation condition and investigate its meaning. It may describe labour or equipment constraints rather than a universal establishment limit. Routing it directly to `abs_max` would turn an investment-addressable condition into an unsupported hard exclusion.

## 8. Uncertainty and sensitivity to report

Keep uncertainty about transcription, study validity, source dependence, disagreement, transfer, dataset measurement and design choices distinct. They cannot generally be compressed into a single percentage. The existing 20% floor for ordinal profiles is a humility flag, not a confidence interval. An unobserved tail is unknown, not merely a wider error bar around a predicted score.

**Recommended sensitivity checks, where relevant and feasible:**

- Leave out one independent origin at a time; where relevant, also leave out one author group at a time. Compare all eligible origins with measured/validated subsets and test unresolved dependency assumptions.
- Compare current credibility weighting with equal-origin weighting and exclusion of assertion-only evidence.
- Retain alternative source tables, contextual profiles and approved score conventions as distinct scenarios.
- Compare accepted runtime weights with an explicitly labelled equal-weight baseline or reviewed importance-derived alternative.
- Test boundary inclusion and missing coverage; evaluate dataset binding and resolution choices separately from rule changes.
- Report affected sites, mapped area where the spatial product permits it, class changes and hotspot/rank changes. If spatial runs are unavailable, provide boundary examples and state that map sensitivity remains untested.

Search specifically for limitations, failures and negative findings within the authorised scope. More agreeing papers can still share the same original assumption. Neither a tight reported spread nor a larger citation count demonstrates reduced uncertainty. Do not silently tighten or widen a threshold as a purported correction for publication bias; propose a documented scenario or decision instead.

## 9. Record enough to reproduce the AI-assisted decision

The [synthesis decision record](https://github.com/CIAT/nbs_ruralscan/blob/9d84fd9900b9c913804a9f94eb6f9779f2734994/methodology/T4_generation_method.md#synthesis-decision-record) already requires pinned inputs, agent settings, interpretation and decision/output links. A useful review packet should contain:

| Record | Required content |
|---|---|
| Question and prior rule | Family, variable, context, application scale, previous accepted mapping and exact proposed change. |
| Inputs | Register revisions/hashes, evidence IDs, source pages/sections, native profiles, dataset bindings and policies. |
| Accounting | Every candidate's use/hold/exclusion, review state, compatible group, known study/data/judgement origin, repeated data points, author-group dependencies and uncertainty about independence. |
| Transformation | Unit conversions, class crosswalks, source weights, endpoints, missing tails, pooling method and boundary examples. |
| AI interpretation | Task prompt or immutable reference; skill/ruleset version; actual provider/model/settings where available. Record unavailable settings honestly. |
| Review | Rationale, contrary evidence, sensitivity results, exact approval scope and remaining holds. |
| Replay and release | Accepted authored inputs, compiler version/invocation, candidate-versus-accepted comparison and eventual release identifier. |

AI extraction, AI synthesis and scientific approval remain separate. For unchanged inputs and context, replay the accepted decision rather than ask a model to make the decision afresh. New evidence or a changed interpretation produces a new proposal and an explicit comparison.

## 10. Implementation boundary

The [classification contract](https://github.com/RuralScan/method/blob/main/data-model/evidence-classification.json) separates knowledge basis and extraction format. Its additive migration retains legacy compiler values, source quotations, review decisions and ruleset stamps. New extraction must provide a known basis separately from format; unknown-basis proposals remain staged for review.

This extension does not adopt new credibility multipliers or recompute accepted analytical rules using guessed classifications. Historical compiler behaviour and proposed scientific improvements are distinguished throughout this guide. Author-group influence tests and dependence-aware statistical pooling are recommendations until implemented and validated for a declared analysis.

Read the companion [registry overview](ch-evidence-registry.html) for source types, WOCAT accounts and literature-derived expert opinion. The dashboard Methods section links both chapters and the machine-readable field contract.
