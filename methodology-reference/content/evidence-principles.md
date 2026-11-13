---
title: Evidence principles and provenance
slug: evidence-principles
summary: Trace any analytical value in the scan back to the source passage that supports it, and judge whether a document can serve as evidence at all.
sources:
  - methodology/T4_generation_method.md
  - methodology/T3_T6_generation_method.md
  - methodology/search_protocol.md
  - methodology/access_policy.md
  - methodology/RULESET_VERSIONS.md
  - methodology/expert_opinion_protocol.md
  - schema/spec.md
  - schema/structure/columns.json
  - AGENTS.md
  - src/nbs_ruralscan/schema_tools/validate_sources.py
  - .agents/skills/source-command-extract-evidence/references/defects.md
  - evidence:README.md
---

## Why the method is evidence-first

The Rural NbS Scan sets response curves, thresholds, effect classes and cost classes that a development-bank reviewer can challenge with one question: *why that value?* The method answers that question by construction. Every analytical value is linked to the passages of named sources that support it, and the link is checked by machine on every build. [src: methodology/T4_generation_method.md §0]

The founding rule is that a document is never turned into a threshold in one step. Reading a source (extraction) and combining several sources into one rule (synthesis) are separate stages with a stored, inspectable evidence layer between them. A model or a person who reads a paper records what that paper says, as atomic claims with their quotes. A separate, deterministic synthesis step decides what the claims add up to. [src: methodology/T4_generation_method.md §0]

Six tenets follow from that rule and apply throughout the evidence chapters. [src: methodology/T4_generation_method.md §0]

1. **Provenance on every value.** No parameter exists without linked evidence units.
2. **No silent inference.** Extraction records only what a source states. A value the source does not give is left empty, not guessed.
3. **Separation of concerns.** Discovery proposes sources, evidence substantiates claims, synthesis combines them, and a reviewer signs off.
4. **Machine learning for *which*, literature for *what shape*.** A variable-importance model may help choose variables. It never sets a response curve.
5. **Auditable lumping.** Variable harmonisation and the grouping of sub-practices into families are recorded with a rationale, never merged silently.
6. **Reproducibility.** Instructions, skills and the evidence corpus are versioned, and uncertainty is derived from the spread of evidence rather than asserted.

## The provenance chain

Every value in a finished recipe row traces a fixed chain:

```formula
recipe row → evidence_id_1 … evidence_id_n → source_id → (benchmark_tier, locator, verbatim quote)
```

- `recipe row` is a row of a generated analytical table: [[table:T4]] (suitability), [[table:T3]] (hazard response), [[table:T6]] (scorecard effects) or [[table:T6E]] (economic profile).
- `evidence_id` is the key of one atomic claim in the Evidence Register, [[table:EV]].
- `source_id` is the key of the publication, report, web page or code repository in the Source Register, [[table:SRC]].
- `benchmark_tier` is the source's credibility tier, stored once on the source row.
- `locator` says where in the source the claim sits: a PDF page, a web section, a character span, or a file and line range at a pinned commit.
- `verbatim quote` is the passage itself, sliced from the cached text of the source.

[src: schema/spec.md §Evidence & configuration layer] [src: methodology/T4_generation_method.md §5.2 Source & Evidence registers]

The chain is the deliverable's defensibility, and it is also what makes a run reproducible: given the registers at a commit, the same synthesis code reproduces the same rows. [src: methodology/T4_generation_method.md §0]

### What the build enforces

A validator runs inside the schema build and in continuous integration and fails the build if any link in the chain is broken. [src: src/nbs_ruralscan/schema_tools/validate_sources.py §module docstring] It enforces three rules:

1. Every `source_id` used by an evidence row has a cached, non-empty, parseable artefact in the local corpus: a PDF, or a text, HTML or Markdown snapshot for web sources.
2. Every quote appears verbatim in that artefact, after normalising whitespace and punctuation. Ellipsis-joined fragments are each checked. A non-English quote stored with its English translation is checked on the native text only.
3. For PDF artefacts, the quote must appear on the cited page, not merely somewhere in the document.

Only rows whose role carries no quotable claim (baseline map or mask layers) skip the quote check, and they are reported rather than skipped silently. [src: src/nbs_ruralscan/schema_tools/validate_sources.py §module docstring]

This guardrail exists because a register that was largely hand-typed, with quotes reconstructed from memory or abstracts, was found to be contaminated and was purged. The standing rule is that no quote, page or evidence unit may be typed from memory, an abstract, a search snippet or model knowledge. Every evidence row comes through the deterministic pipeline over a cached source artefact, and appending directly to the register or to a recipe's evidence column is forbidden. [src: AGENTS.md §Don't]

A verified quote proves that the passage exists. It does not prove that the structured fields encoded from it are faithful. The further checks that test numbers, scope, species tagging and direction are described in [[ch:extraction]].

## The registers and how they relate

Four registers hold the evidence layer that feeds the analytical tables. Each is a CSV file (the editable source of truth) with a generated JSON copy that code reads; the column set of each is frozen in a machine-checked manifest. [src: schema/structure/columns.json §SRC] [src: AGENTS.md §What this project is]

| Register | One row per | Holds | Links |
|---|---|---|---|
| [[table:SRC]] Source Register | publication, report, web page, tool or codebase | citation, DOI, tier, study context, access status, licence, artefact hash, library path or URL | referenced by EV, TOOL |
| [[table:EV]] Evidence Register | atomic claim | variable, role, relationship, context, quote, locator, scope, review state, ruleset version | → SRC, FAM, VONT |
| [[table:SRCH]] Search Register | search run (practice × family × table × process) | verbatim query, screening steps, criteria, limits, counts, ruleset version | → T0 practice |
| [[table:TOOL]] Tools and Methods Registry | tool, codebase or method framework | tool type, repository commit, variables, weighting, membership functions, linked evidence IDs | → SRC, EV |

[src: schema/spec.md §SRC] [src: schema/spec.md §EV] [src: schema/spec.md §TOOL] [src: methodology/search_protocol.md §What every search logs]

### Source Register

A source row describes the work, not any claim in it. Its required fields are `source_id`, `citation`, `benchmark_tier` and `source_kind` (`paper`, `grey_lit`, `website`, `tool` or `codebase`). [src: schema/structure/columns.json §SRC]

The tier lives only here. `benchmark_tier` takes `high`, `medium`, `low` or `external`, where `external` marks a citation-only source that was not screened and carries zero weight in synthesis. Because tier is a property of the work, it is reached from an evidence row by joining on `source_id` and is never copied onto evidence rows; re-scoring a source therefore changes it in one place. [src: schema/spec.md §SRC]

Study context on the source (`study_country`, `aez`, `farming_system`, `study_income_group`) provides defaults that individual evidence units may override for multi-site papers. `venue_type`, `method_type` and `is_seminal` record the audit-relevant parts of the credibility assessment described in [[ch:discovery]]. [src: schema/spec.md §SRC] [src: methodology/T3_T6_generation_method.md §3.3 Fixed context keys]

### Evidence Register

An evidence unit is one claim from one source about one variable for one practice and family, in one role. [src: schema/spec.md §EV] Four per-claim axes are kept orthogonal so that each can be weighted independently in synthesis: [src: methodology/T4_generation_method.md §5.2 Source & Evidence registers]

- `evidence_type`, the kind of evidence (`literature_relationship`, `ml_importance`, `scoping_candidate`, `expert`). Only literature and expert evidence may carry shape-bearing parameters; importance scores and scoping candidates inform variable selection only.
- `claim_basis`, how strongly the claim is supported within its source (`primary_measured`, `modelled`, `cited_secondary`, `expert_assertion`, `table`, `figure_read`). A low-tier paper can carry a measured threshold while a high-tier paper offers only a second-hand ranking; this field records the difference.
- `claim_scope`, what the claim is about (`practice_technology`, `species_specific`, `crop_specific`), with a `taxon` when it is not practice-level.
- `extraction_confidence`, how faithfully the claim was transcribed.

The unit's role (`use_role`) decides which table it can feed; the roles are described in [[ch:extraction]]. Optional fields keep the audit trail: `raw_name` preserves the source's own name for the variable, `lineage_of` points to the original when the claim echoes another work, and `justification_quote` and `selection_justification` capture separate verbatim passages explaining why a threshold or a variable was chosen. [src: schema/spec.md §EV]

### Search Register

A search row records how a set of candidate sources was found: the exact query strings, the screening funnel applied, the inclusion criteria, the caps, the counts at each stage, the run identifier and the ruleset version that governed it. It holds the protocol of a search; a separate progress ledger holds its status. The two are reconciled by the build (see [[ch:review-and-quality]]). [src: methodology/search_protocol.md §How it locks together]

### Tools and Methods Registry

A tool is a source, reviewed like any other. A tool gets a Source Register row (`source_category = tool`) and a TOOL row, which extends it with metadata: which variables, weighting scheme, membership functions and datasets the tool uses, its maturity and licence. The TOOL row does not replace extraction. The tool's hard-coded thresholds and weights become evidence units linked back through `evidence_ids`. [src: schema/spec.md §TOOL]

### Other registers in the evidence layer

Three further registers make evidence units aggregatable and route them to consumers. The Variable Ontology, [[table:VONT]], maps the many surface names of a variable to one canonical identifier. The family registry, [[table:FAM]], defines the suitability families to which suitability evidence is keyed. For effect evidence, the target crosswalk, [[table:XW]], is the only place an outcome variable measured by a paper becomes a key in [[table:T3]] or [[table:T6]]. [src: schema/spec.md §VONT] [src: schema/spec.md §XW]

## The living-database model

The evidence base is designed to grow without rewriting what it already holds. Adding evidence is append-only: new source rows and new evidence rows. The synthesis engine recalculates consensus weights, medians and confidence from whatever the register contains each time it runs. [src: AGENTS.md §Style & conventions]

Three consequences follow.

- **No evidence is hard-deleted.** A reviewer's drop sets a review state that excludes the unit from synthesis while keeping it as a restorable record. Deletion would break the audit trail and remove the ability to reverse a mistaken judgement. [src: AGENTS.md §What is locked] The mechanics are in [[ch:review-and-quality]].
- **Historical records keep their instructions.** Each search and evidence row carries the version of the extraction ruleset under which it was produced. Units are not silently restamped when the rules change. [src: methodology/RULESET_VERSIONS.md §Ruleset versions] See [[ch:rulesets-and-learning]].
- **Generated rows are outputs, never inputs.** Recipe rows are rebuilt from evidence. A value cannot be fixed by editing the generated row; it is fixed by correcting or adding evidence. [src: AGENTS.md §What is locked]

## Replication for synthesis

The synthesis engine counts independent sources to decide how much weight a consensus carries and to compute weighted medians of thresholds. It can only do this if each distinct finding is present. The method therefore requires that every distinct literature threshold be recorded as its own evidence unit, even when it looks redundant with a threshold already in the register. Skipping "duplicates" at extraction would understate agreement and bias the medians. [src: AGENTS.md §Style & conventions]

Replication is not double-counting. The method separates two cases.

- **Independent replication** is a different study reporting a similar value. It is kept as a separate unit and counts as a separate vote.
- **Echo** is a paper repeating another's finding. It is kept, tagged `claim_basis = cited_secondary` with the original named in `lineage_of`, and synthesis collapses echoes to their origin. Ten papers repeating one original slope limit are one claim. [src: methodology/T4_generation_method.md §6.1 Publication bias & uncertainty]

Likewise, one dataset gives one effect unit: several outputs from a single simulation, or a season summary beside per-technique rows from the same season, are not independent findings. [src: .agents/skills/source-command-extract-evidence/references/defects.md §Limits, geometry and duplicates]

A source's own record of which variables it supplied (`SRC.vars_extracted`) must match the variables that actually have evidence rows for it, so that coverage cannot be claimed for variables never extracted. [src: AGENTS.md §Style & conventions]

## What counts as a source

The method admits four kinds of source, each with its own acquisition and locator rules (see [[ch:acquisition]]).

| Kind | Examples | Locator |
|---|---|---|
| Peer-reviewed literature | primary studies, meta-analyses, systematic reviews | PDF page |
| Grey literature | agency manuals, project completion and evaluation reports, working papers | PDF page, or page of a once-rendered PDF for Word masters |
| Practitioner databases | WOCAT technology questionnaires, practice databases | PDF page for the export; section of a deterministic transcript for questionnaire fields |
| Tools and code | suitability or MCDA codebases, published model code, method frameworks | file and line range at a pinned commit |

[src: methodology/search_protocol.md §WOCAT technology sheets] [src: methodology/search_protocol.md §Word documents (.docx)] [src: schema/spec.md §TOOL]

Expert opinion enters the same register through the same fields. An elicited assertion is stored as an evidence unit with `evidence_type = expert` and `claim_basis = expert_assertion`, its transcript registered as a source. The expert elicitation protocol is a draft. [src: methodology/expert_opinion_protocol.md §4. Translating Expert Claims to the Schema] [src: AGENTS.md §Don't]

### What does not count

- **A document the team cannot open.** A PDF must be in the shared library with its path recorded; a web or code source must have a URL, a cached snapshot and a locator. A source that cannot be cached cannot be registered. [src: AGENTS.md §Don't]
- **A bare URL.** A link without a saved snapshot and the section the quote came from is not provenance. [src: AGENTS.md §Don't]
- **A README, landing page or abstract standing in for a tool.** The tool's actual code or method documentation must be read. [src: AGENTS.md §Don't]
- **A search snippet or web-summary figure.** Numbers repeated across web summaries that cannot be traced to a document are not evidence. [src: methodology/search_protocol.md §Learnings from the agroforestry synthesis-first round]
- **An ex-ante project document as effect evidence.** A project appraisal document or results framework states what a project will do. It may inform suitability scoping context but never an effect claim. [src: .agents/skills/source-command-extract-evidence/references/defects.md §Common extraction defects]
- **A dataset (CSV, spreadsheet, R object) as a source of claims.** Datasets have no verbatim page semantics. They are paused until a dataset-intake adapter is defined and are used only as discovery seed lists, whose cited primaries are acquired and extracted from their own documents. [src: methodology/search_protocol.md §Datasets (.csv / .xlsx / R)]
- **A format with no handling rule.** It is paused until an acquisition adapter, locator semantics and a quality check are defined. [src: AGENTS.md §What is locked]

### Copyright and sharing

Source files and snapshots are kept out of the public repository regardless of licence. What is committed is the ingestion code, the register schemas and the structured evidence units, whose quotes are short passages used as citations. Each source's access status is checked against Unpaywall by DOI and recorded with its licence; paywalled or unknown-status sources are shown only as short quotes. [src: methodology/access_policy.md §Standing rules] [src: methodology/T4_generation_method.md §5.1 Document ingestion]

## Assumptions and limits

- **Provenance is not truth.** The chain proves a claim was transcribed from a real passage. It cannot prove the source is right, that the claim transfers to a new context, or that a published class is scientifically plausible. Those judgements belong to credibility scoring, synthesis weighting and human review.
- **The evidence base is optimistic.** Papers report where a practice works more often than where it fails, so thresholds and effects skew favourable. The method counters this directionally (lineage deduplication, capturing failure and exclusion statements, conservative reconciliation) and states the bias rather than correcting it statistically. [src: methodology/T4_generation_method.md §6.1 Publication bias & uncertainty]
- **Coverage depends on what was searched.** Absence of evidence for a variable or cell is not evidence of absence; it may reflect an unsearched channel or language.
- **Counts are effort, not strength.** The number of units or sources in the register measures work done. It is not a confidence score, and counts from different register editions are never combined.
- **Scoping, not feasibility.** The evidence layer supports scoping-grade rules. A feasibility study must still validate site conditions, local datasets and costs against primary data.

## Where this is configured

- Source, evidence, search and tool records: [[table:SRC]], [[table:EV]], [[table:SRCH]], [[table:TOOL]].
- Harmonisation and routing: [[table:VONT]], [[table:FAM]], [[table:XW]].
- Frozen column sets: `schema/structure/columns.json`.
- Provenance guardrail: `src/nbs_ruralscan/schema_tools/validate_sources.py`.
- Access and sharing rules: `methodology/access_policy.md`.
- Related chapters: [[ch:discovery]], [[ch:acquisition]], [[ch:extraction]], [[ch:review-and-quality]], [[ch:rulesets-and-learning]], [[ch:suitability-synthesis]], [[ch:effect-synthesis]], [[ch:evidence-base]].
