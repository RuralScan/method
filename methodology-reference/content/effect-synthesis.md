---
title: Hazard and scorecard effects (T3/T6)
slug: effect-synthesis
summary: AI synthesises scientific effect judgments; reviewed proposals become immutable outputs that code validates, packages and reads without re-rating.
sources:
  - method:data-model/agent-effects-contract.json
  - method:data-model/spec.md
  - method:decisions/current.csv
  - evidence:workflows/synthesis/README.md
  - evidence:.agents/skills/source-command-t3t6-synthesise/SKILL.md
---

## Scientific responsibility

**T3/T6 synthesis is AI-led.** The AI reads source-provenanced evidence, assesses compatibility and dependence, and authors scientific judgments and their rationale. A reviewer accepts the exact proposed outputs. Code validates references, types, review eligibility, input freshness and acceptance integrity; packages accepted values; and reads those values at runtime. It does not choose direction, strength, confidence, applicability, weights or wording. [src: method:decisions/current.csv §t3t6_agent_synthesis]

This decision extends the agent-led approach to effects. It supersedes the historical automatic effect-scoring procedure for new outputs. Historical T3/T6 values remain explicitly historical until replaced by accepted proposals. Retiring the shared generator also freezes existing T6E values; new economic synthesis is outside this decision. T4's historical compiler remains retired. [src: method:decisions/current.csv §t3t6_agent_synthesis]

## What the AI synthesises

[[table:T3]] separates mitigation of risks to livelihoods from threats to the investment. [[table:T6]] describes practice effects on [[table:T5]] priorities. Keep the two risk lenses separate. A practice reducing flood losses does not establish its own resistance to flood damage. Cost profiles belong in [[table:T6E]], not new T6 effect proposals. [src: method:data-model/agent-effects-contract.json]

The proposal identifies one practice and table, the exact affected cells, and every existing row it replaces. Cell identity includes family and applicability scope; T3 also includes hazard, risk role and farming system. Unchanged rows are not silently reinterpreted. A withdrawal is explicit and traceable; it is not a zero-effect row. [src: evidence:workflows/synthesis/README.md]

The AI must explain:

- **Routing:** why each claim addresses the practice, family, outcome and risk role. Crosswalks provide vocabulary and routing context; they do not decide scientific relevance. Qualitative-only families stay out of these landscape tables. Per-species effects may support practice judgments where applicable; do not import T4's species-envelope exclusion into effects.
- **Dependence:** which claims share a study, dataset, review or modelling lineage. Identify overlapping primary studies and reviews. More quotations from one origin do not become independent support.
- **Compatibility:** comparator, outcome, units, denominator, duration, spatial scale, hazard severity, implementation and context. Do not pool incompatible quantities or mistake site descriptions for effects.
- **Direction and strength:** positive, negative, null, mixed or conflicting evidence, with the appropriate table's vocabulary. A null effect requires evidence; missing evidence stays data-deficient. Explain heterogeneity instead of masking it with a median.
- **Confidence:** assess evidence level and agreement separately, then author a confidence judgment with its own rationale. The archived confidence matrix, fixed design weights, rank mappings, lineage discounts, caps and family maxima no longer calculate new judgments. IPCC-style labels are qualitative confidence, not probabilities.
- **Applicability:** where the judgment applies and where transfer is uncertain or unsupported. Do not silently generalise high-income temperate findings to low-income drylands or transfer family-specific findings to a whole practice.
- **Uncertainty and sensitivity:** competing explanations, unresolved disagreement, sparse evidence and how plausible alternative inclusion or interpretation choices would affect the conclusion.

These are scientific reasoning requirements, not an arithmetic scoring recipe. [src: evidence:.agents/skills/source-command-t3t6-synthesise/SKILL.md]

## Evidence and numerical outputs

Preparation snapshots the broad practice effect corpus, source records, applied review history, definitions, configuration and the synthesis skill. Every candidate gets an explicit include, exclude, context or hold disposition, reason and origin. Included claims need reviewed evidence, verified source identity, a quoted passage and a locator; held, dropped or unresolved claims cannot support accepted outputs. A source should be opened and checked wherever the extracted passage cannot resolve an interpretation. Do not invent unseen source content. [src: evidence:workflows/synthesis/README.md]

Numerical summaries remain optional. The AI must establish compatible measures and independent origins, explain any conversion and state uncertainty. Validation requires at least two declared origins for a numerical magnitude summary; that count alone does not prove compatibility or independence. Review must assess the reasoning. No code fills missing magnitudes, estimates scientific weights or maps a reported number to an effect class. [src: method:data-model/agent-effects-contract.json]

Asset-risk weights, if proposed, are authored scientific values. A packaged weighted set must cover the six core hazards and sum to one within tolerance. Code checks those constraints without computing weights. Missing weights mean no accepted weighted assessment; runtime must not introduce an equal-weight fallback. Asset-only hazards without T2 layers remain descriptive. [src: evidence:workflows/synthesis/README.md]

## Proposal, review and publication

1. **Prepare.** Generate an unscored input packet for the authorised practice/table. Preserve its bytes. Record the task, actual model identity, prompt, skill version and settings; say when settings are not exposed.
2. **Synthesise.** The AI authors `rows.csv`, complete candidate dispositions, the scientific reasoning and a before/after comparison. CSV is the source of truth. Generated JSON carries the exact same authored values.
3. **Validate and stage.** Validate the proposal against current evidence and exact previous-row fingerprints, then commit its four files under an immutable proposal ID. Validation is not scientific acceptance.
4. **Accept or hold.** An eligible human reviewer records an original issue receipt identifying the proposal's full Git revision and SHA-256, the decision and the reason. The workflow authenticates the original author and body. Acceptance is separate from extraction review and from approving software that implements this workflow.
5. **Package.** Replay the append-only decision journal and export only current accepted outputs. Reject stale inputs, unresolved holds, tampering and incomplete weighted sets. Historical values do not fill gaps in the accepted package.
6. **Run.** Pin the package manifest hash independently. Runtime verifies every file and row's acceptance provenance, then returns the explicitly selected accepted record without re-rating or inferring context.

[src: evidence:workflows/synthesis/README.md]

A changed evidence packet, configuration, source identity or applied review history makes the relevant acceptance stale. Existing values stay visible for audit; publication waits for a new reviewed proposal. Changed scientific judgments or prose on accepted rows require a new proposal. An explicit hold blocks release. Accepted withdrawals remain in provenance so removed rows cannot silently return. [src: evidence:workflows/synthesis/README.md]

## Reproducibility and migration

Reproducibility means replaying exact accepted outputs, their input packet, skill/model provenance and acceptance receipt. It does not mean expecting a fresh model run to reproduce the same judgment. A new model run creates a new proposal for comparison and review. [src: evidence:workflows/synthesis/README.md]

No existing row is retrospectively labelled AI-authored or scientifically accepted by this transition. The production queue retains historical rows alongside explicitly marked accepted outputs. An accepted-only package is a partial collection of explicit records, not a complete default recipe. Consumers must report missing accepted cells rather than use the archived recipe as an implicit fallback. [src: evidence:workflows/synthesis/README.md]
