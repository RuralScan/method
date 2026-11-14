---
title: Human review and quality control
slug: review-and-quality
summary: Review evidence units and published thresholds with the right decision and reason code, understand how several reviewers' decisions combine, and read the progress record without over-claiming.
sources:
  - AGENTS.md
  - src/nbs_ruralscan/schema_tools/review.py
  - src/nbs_ruralscan/schema_tools/submit_review.py
  - src/nbs_ruralscan/schema_tools/quarantine.py
  - src/nbs_ruralscan/schema_tools/ledger.py
  - src/nbs_ruralscan/schema_tools/table_progress.py
  - src/nbs_ruralscan/schema_tools/check_account.py
  - src/nbs_ruralscan/schema_tools/check_numbers.py
  - methodology/RULESET_VERSIONS.md
  - .agents/skills/extraction_contracts/T4_review_contract.md
  - .agents/skills/source-command-extract-evidence/references/defects.md
  - methodology/T4_generation_method.md
  - methodology/search_protocol.md
  - methodology/extraction_retrospective.md
  - schema/spec.md
  - evidence:workflows/review_exports/README.md
  - evidence:handbook/review-records.md
---

## Why people review evidence

The deterministic checks prove that a quote is real, that its numbers appear in it, and that some recognisable errors are absent. They cannot decide whether a claim is the right kind of claim, whether it was read correctly in context, or whether a published number is scientifically fit to drive a recipe. Those judgements are made by people. [src: src/nbs_ruralscan/schema_tools/check_numbers.py §module docstring] [src: .agents/skills/extraction_contracts/T4_review_contract.md §Numeric plausibility gate]

The method places the human bottleneck where it matters. Extraction fidelity, harmonisation and an adversarial review pass run first, with automated triage. People review flagged and sampled units, the family schemes and recipe content, and later-stage outputs (dataset fitness, output validation, resolution). [src: methodology/T4_generation_method.md §7. Validation & sign-off]

## The review workspace

Review happens in a dedicated workspace with two interfaces over the same records.

- **A queue-based review dashboard** with three primary queues: units to review, units waiting for answers to a reviewer's question, and units the reviewer has already decided. Secondary filters separate units by origin, by whether others have reviewed them, and by claim scope (general, species, crop), with species and crop units reviewed in their own lane. [src: AGENTS.md §What is locked]
- **A simple one-unit-at-a-time review page,** showing the extracted claim beside the highlighted source passage, the Population, Intervention, Comparator, Outcome and Study-design elements spelled out with each element flaggable, an advisory test of whether the practice is named in the quote, the source's own words for the practice, the band rule that set the strength (value, register rule, and whether the recorded strength follows it), and how many units from how many sources each generated row rests on. [src: AGENTS.md §File map]

For tabular quotes, the reviewer can view an image of the page region from the cached PDF, so a table cell is judged with its caption and headers. [src: AGENTS.md §What is locked]

## The review decision

Each reviewer gives one of three decisions per unit.

| Decision (dashboard) | Review page | Effect on the unit |
|---|---|---|
| Keep (`ok`) | Approve | evidence stands; `reviewer_ok = true`; any automatic flag is cleared |
| Drop (`drop`) | Reject, with a reason code | `review_state = dropped`; the row and its history are retained |
| Query (`query` or `flag`) | Hold | the unit stays active, unapproved, with the reviewer's question stamped and logged |

[src: src/nbs_ruralscan/schema_tools/review.py §module docstring] [src: src/nbs_ruralscan/schema_tools/review.py §apply_decisions] [src: evidence:workflows/review_exports/README.md §Preview one private export]

A drop requires a coded reason. [src: AGENTS.md §What is locked] A query's answer comes back on the evidence card, and the reviewer then makes a single keep, drop or query decision; there is no separate approval step for answers. [src: AGENTS.md §What is locked]

### Reason codes

Every decision is logged with a reason code. The active codes are listed in the review module and describe what went wrong (or, for keeps, why a flag was wrong). [src: src/nbs_ruralscan/schema_tools/review.py §REASON_CODES]

| Code | Meaning |
|---|---|
| `smuggled_number` | a number in the relationship is not in the quote |
| `wrong_variable` | mapped to the wrong canonical variable, often a proxy relabelled |
| `wrong_practice` | the claim is about a different practice (PICOS failure) |
| `species_envelope` | a species or crop envelope tagged as practice-level; the fix is re-tag and keep, never drop |
| `table_error` | rows stitched across a table, or a garbled table reading |
| `off_scope` | the passage is not the kind of claim the role needs (site description, methods, carbon accounting) |
| `quote_too_narrow` | a bare cell or fragment without the sentence, header or caption |
| `relationship_missed` | the source gives a relationship (direction, curve, classes) that the unit failed to capture |
| `insufficient_context` | no caption or context to interpret the value, or an unreadable table image |
| `unusable_value` | a weight with no scale, or a land-cover rule with no class list |
| `speculative_evidence` | speculation, assumption or an ex-ante project document presented as a finding |
| `wrong_table` | the claim belongs to a different consumer, for example a soft enabling factor extracted as structural suitability |
| `constrained_aoi` | a source that scopes the practice onto residual or allocated land, understating where it can go |
| `false_flag` | an automatic flag was wrong |
| `accepted_correction` | an automatic correction is accepted |
| `confirmed_pass` | an unflagged unit is confirmed correct |
| `missed_error` | an error the checks did not catch |
| `other` | none of the above, with a note |

[src: src/nbs_ruralscan/schema_tools/review.py §REASON_CODES] [src: .agents/skills/source-command-extract-evidence/references/defects.md §Common extraction defects]

Older codes merged into these (row-stitching and table-garble into `table_error`; an earlier weight code into `unusable_value`) may still appear in historical logs. [src: src/nbs_ruralscan/schema_tools/review.py §REASON_CODES] The codes are not bookkeeping: each is routed to a specific fix in the retrospective after every sweep (see [[ch:rulesets-and-learning]]). [src: methodology/extraction_retrospective.md §QA/QC review feeds the loop (reason codes)]

## Several reviewers: consensus and conflict

Decisions are stored per pair of evidence unit and reviewer. Applying them reduces the store to consensus. [src: AGENTS.md §What is locked] [src: src/nbs_ruralscan/schema_tools/submit_review.py §module docstring]

```formula
for each evidence unit e:
  D_e = { d_r : reviewer r has a non-empty decision on e }
  if D_e is empty            → no change
  if all d_r in D_e agree    → apply that decision to e and append it to the review log
  otherwise                  → conflict: nothing applied; e is left pending
```

- `d_r` is reviewer `r`'s decision (keep, drop or query) on unit `e`.
- The review log records each applied decision with reviewer, date, reason and note.

There is no quorum: one reviewer's decision applies if no one disagrees. [src: AGENTS.md §What is locked]

Applied decisions remain viewable, re-openable and challengeable. If a second reviewer later disagrees with an applied decision, the unit is automatically re-opened as a conflict. [src: AGENTS.md §What is locked]

Application is surgical. Decisions are replayed onto the *current* registers rather than merged from a reviewer's older working copy, so one reviewer's stale copy can never revert other people's rows. The decided changes, regenerated tables and log are then submitted together for integration. Only changes confined to the evidence register, the review log and generated files, from an allowed reviewer, are integrated automatically; anything else waits for human approval. [src: AGENTS.md §What is locked] [src: src/nbs_ruralscan/schema_tools/submit_review.py §module docstring]

Compiled rows (generated hazard, scorecard and economic rows) have their own review log, keyed by row, reviewer, date and decision. [src: evidence:workflows/review_exports/README.md §Run the examples]

## Soft delete: why evidence is never hard-deleted

A drop is never a deletion. It sets `review_state = dropped`. The row stays in the register as a restorable record, and is excluded from synthesis, from the progress counts and from dashboard tallies. Hard-deleting evidence is forbidden; any historic hard deletion is recovered from version history as a dropped row. [src: AGENTS.md §What is locked]

The method keeps dropped evidence for three reasons.

1. **Reviewers are fallible.** A drop may be reversed by a later reviewer or a changed rule; deletion would make that impossible.
2. **The audit trail must show what was rejected and why.** A reader auditing a recipe row needs to see the evidence that was set aside, not only what was used.
3. **Rules change.** Each unit carries the ruleset version under which it was last evaluated, so re-evaluations are auditable. A rule that later broadens (for example, readmitting crop-level evidence for a family) can bring dropped units back without re-extraction. [src: AGENTS.md §What is locked]

Automatic quarantine follows the same model. When scope or practice checks fire on a unit no person has touched, the build soft-drops it and stamps the reason, so obvious errors do not crowd the reviewer's queue. It never re-quarantines a unit that a reviewer has approved, dropped, decided, or reopened. [src: src/nbs_ruralscan/schema_tools/quarantine.py §module docstring]

Rule changes applied retroactively also use soft drops under a named rule rather than deletion, so every affected unit is reversible. [src: methodology/RULESET_VERSIONS.md §v1.6.18]

Generated rows may not cite dropped evidence: a check on each row's account fails a row whose evidence list includes a dropped unit. [src: src/nbs_ruralscan/schema_tools/check_account.py §module docstring]

## Re-opening

Any active, queried or dropped unit can be re-opened. Re-opening returns the unit to the active state, restores its most recent automatic flag text so it re-enters the worklist, and logs the reset under the reviewer's name, even if the unit was never approved, so that an old query cannot hide it. [src: src/nbs_ruralscan/schema_tools/review.py §reopen_units]

## Numeric plausibility review

Exact transcription proves that a number came from the source. It does not prove that the number is fit to drive an executable recipe. Before any published class, range or cutoff is proposed for numeric calibration, extractors, independent reviewers and synthesis all record a plausibility assessment. [src: .agents/skills/extraction_contracts/T4_review_contract.md §Numeric plausibility gate]

| Aspect | Questions | Examples of concern |
|---|---|---|
| Measurement and precision | units, statistic, averaging period, spatial support, class widths, endpoint inclusion; does claimed precision exceed measurement or interpolation uncertainty and temporal variability? | **narrow bands** and **false precision** |
| Scientific meaning | what mechanism and evidence justify each transition? Is the boundary a validated response, or a local rank, quantile, map-class break or expert choice? | **unexplained jumps**, abrupt exclusions, missing tails |
| Proxy semantics | does the measured quantity stand for the named variable? | **proxy substitution** (for example temperature standing in for another variable) |
| Transfer | in which practice, family, climate, region and measurement context was the rule derived and tested? Does it overlap other criteria? | **unsupported transfer**; a local ordering treated as a global response |

[src: .agents/skills/extraction_contracts/T4_review_contract.md §Numeric plausibility gate]

The disposition records the source values, the concern, any available justification, missing validation and the exact scope of approval. An unresolved assessment becomes a calibration or transfer hold. The raw values are preserved and any independently supported variable use or direction is kept, but the values are not promoted to an executable curve, score, pooled cutoff or hard exclusion. If measurement uncertainty is not reported, the review says so; it never invents an error estimate. [src: .agents/skills/extraction_contracts/T4_review_contract.md §Numeric plausibility gate]

A worked warning in the contract: a published rainfall table placing moderate suitability between 1,150 and 1,170 mm per year, a band 20 mm wide derived from an interpolated ten-year average, is flagged for its narrowness and its regional qualitative direction retained. This is not a universal minimum band width, not proof that the paper is wrong, and not permission to round or widen its classes; a narrow band can be defensible when mechanism, measurement and validation support it. Any replacement or transfer needs explicit approval. [src: .agents/skills/extraction_contracts/T4_review_contract.md §Numeric plausibility gate]

Regional origin alone is not a plausibility defect. A complete quantitative table or a conditional recommendation from one region is kept in full, with its caveats, for comparison with compatible independent studies; one source need not set the final rule by itself. Neither automatic promotion nor a blanket downgrade to direction-only evidence is acceptable. [src: .agents/skills/extraction_contracts/T4_review_contract.md §Retain complete quantitative source recommendations]

### Why a qualitative keep is not numeric approval

A reviewer's keep decision approves a unit within the scope reviewed: that the passage supports the claim, the variable is used, and the direction holds. It does not approve the numbers as an executable calibration. Variable use, direction and calibration are assessed separately, and a generic keep is explicitly not numerical approval. [src: .agents/skills/extraction_contracts/T4_review_contract.md §Numeric plausibility gate] [src: .agents/skills/extraction_contracts/T4_review_contract.md §Three independent assessments]

The reason is structural. Direction-only evidence cannot create scores, interpolation, cutoffs or default weights, so if a keep were read as approving the numbers, a published class could become a recipe threshold without anyone having checked its scientific basis. The review card therefore states the exact approval question, what approval retains, and what it cannot activate. Held or unrecorded calibration is never presented as a score, a range or "reviewed". [src: .agents/skills/extraction_contracts/T4_review_contract.md §Agreement and review output]

### The adversarial reviewer checklist

An independent reviewer reports separate findings for variable use, direction, numeric calibration, scope and transfer, and table coverage, and challenges omissions as well as additions. The checklist asks whether every table row was inventoried (including soil properties and unsuitable classes), whether directions and source values were kept as well as weights, whether a map legend describes suitability rather than merely low and high measurements, whether shared weights stay at their stated level, whether page and image references are correct, whether regional, crop, species and priority contexts are kept apart, and whether plausibility was assessed separately from quote matching. [src: .agents/skills/extraction_contracts/T4_review_contract.md §Adversarial reviewer checklist]

Agreement is reported as separate counts of variable use, direction and calibrated functions, deduplicated by independent lineage, variable and compatible context. Opposite directions are preserved as disagreement. Reviewed and unreviewed tallies are kept distinct. A count is not a runtime weight, confidence score or percentage without an explicit eligible denominator. [src: .agents/skills/extraction_contracts/T4_review_contract.md §Agreement and review output]

### OCR-derived evidence

Units quoted from OCR text cannot be approved until a person has checked a sample of their quotes against the page images: at least three per source or a fifth of its units, whichever is larger. [src: methodology/search_protocol.md §Scanned PDFs (no text layer)]

## The progress ledger

Project progress is recorded per practice, table, discovery process and family in a progress ledger. It answers questions such as "has a targeted search been run for this family and table?" from a record, never from whether evidence happens to exist, because absence of evidence does not show that a search was not run. [src: src/nbs_ruralscan/schema_tools/ledger.py §module docstring]

The ledger separates stages that must be stamped from facts that can be derived. [src: src/nbs_ruralscan/schema_tools/ledger.py §module docstring]

- **Authored stages** (searched, screened, verified) cannot be derived from data. The pipeline step that does the work stamps them as not started, in progress or done.
- **Derived facts** (extraction and review) are read live from the Evidence Register.

A reconciliation check runs in every build and fails it when: [src: src/nbs_ruralscan/schema_tools/ledger.py §check]

1. a search is marked done with no matching search-register row (no claimed search without its logged protocol);
2. verification is marked done for a cell with no evidence units;
3. a status, table or process value is invalid.

It also warns, without failing, about cells that hold evidence from a process whose search is not marked done, which signals ad hoc or incomplete coverage. [src: src/nbs_ruralscan/schema_tools/ledger.py §coverage_warnings]

The project's locked description of the ledger lists a fuller lifecycle (searched, screened, extracted, verified, reviewed) with stage-order enforcement and a requirement that reviewed stages rest on approved units. The ledger code at the pinned revision stores only the three authored stages and derives extraction and review from the register; the stage-order and reviewed rules are not visible in its check. [src: AGENTS.md §What is locked] [src: src/nbs_ruralscan/schema_tools/ledger.py §check]

For the generated effect tables, a separate report places each practice and table in a seven-stage pipeline: searched, acquired, extracted, reviewed, synthesised, prose written, benchmarked. Every number in it is read from an existing artefact. It measures pipeline position, not evidence quality. [src: src/nbs_ruralscan/schema_tools/table_progress.py §module docstring]

Source records follow the same discipline. A newly acquired source starts as `pending`; it becomes `swept` only when an inventory accounts for its relevant pages, tables, continuations, figures and supplements. Completion is never inferred from the presence of a source or evidence rows. [src: .agents/skills/source-command-extract-evidence/references/defects.md §Pipeline integrity (v1.7.0)]

### Why progress cannot be claimed without a record

Progress claims feed decisions: whether a family has evidence enough to synthesise, whether a scorecard cell is empty because nothing exists or because nobody looked. A claim that is not backed by a register record cannot be audited, and an unaudited "done" hides exactly the gaps a scoping tool must show. Tying each stage either to a logged protocol or to live register facts makes over-claiming a build failure rather than a matter of trust. [src: AGENTS.md §What is locked]

Two corollaries follow. Effort counts (sources searched, units extracted, units reviewed) measure work, not the strength of evidence. And a local vote, a successful rehearsal or a feedback report does not establish that a review was submitted; only the corresponding event and state in the committed records do. [src: evidence:handbook/review-records.md §Find the right review record]

## Assumptions and limits

- **No quorum.** A single reviewer can apply a decision when no one else has reviewed the unit. Most units are reviewed by one person, if at all.
- **Coverage is partial.** Review concentrates on flagged and sampled units. An unflagged, unreviewed unit has passed the deterministic checks only.
- **Reason codes are coarse.** They route fixes well but compress nuanced judgements; the free-text note carries the detail.
- **Plausibility review is documentary.** It records the scientific concern and the justification available; it is not automated validation and introduces no universal thresholds.
- **Ledger rules and their description differ** at the pinned revision, as noted above; readers should rely on the build check, not the description, for what is enforced.
- **Feasibility still validates.** Approved scoping evidence does not replace site-level verification of thresholds, datasets and costs in a feasibility study.

## Where this is configured

- Review fields on [[table:EV]] (`reviewer_ok`, `review_state`, `ruleset_version`); search protocols in [[table:SRCH]].
- Decision store, review log and consensus: `src/nbs_ruralscan/schema_tools/review.py`, `submit_review.py`.
- Automatic quarantine: `src/nbs_ruralscan/schema_tools/quarantine.py`.
- Numeric plausibility gate and reviewer checklist: `.agents/skills/extraction_contracts/T4_review_contract.md`.
- Progress ledger: `src/nbs_ruralscan/schema_tools/ledger.py`; effect-table progress: `src/nbs_ruralscan/schema_tools/table_progress.py`.
- Related chapters: [[ch:extraction]], [[ch:rulesets-and-learning]], [[ch:suitability-synthesis]], [[ch:effect-synthesis]].
