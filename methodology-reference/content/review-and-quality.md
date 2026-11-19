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
  - evidence:workflows/submissions/README.md
---

## Why people review evidence

Deterministic checks establish whether a passage matches the cached artefact and flag recognisable numerical or scope defects. Passing them does not prove that every number was interpreted correctly or that every error is absent. They cannot decide whether a claim is the right kind of claim, whether it was read correctly in context, or whether a published number is scientifically fit to drive a recipe. Those judgements are made by people. [src: src/nbs_ruralscan/schema_tools/check_numbers.py §module docstring] [src: .agents/skills/extraction_contracts/T4_review_contract.md §Numeric plausibility gate]

Every extracted item receives automated/AI quality checks, including extraction fidelity, harmonisation and adversarial review. Human review is recorded separately. Flags and sampling help prioritise human attention; they do not define which items receive QC. People also review family schemes and recipe content, and later-stage outputs (dataset fitness, output validation, resolution). [src: methodology/T4_generation_method.md §7. Validation & sign-off]

## The review workspace

Use the current finding queue to inspect the claim, source passage, context and revision, then save a Keep, Drop or Query decision. A saved browser draft is local. A submitted receipt records the vote; the evidence changes only after the protected register change is accepted and appears in the applied journal. Finding review and compiled-row rating review are separate records. [src: evidence:workflows/submissions/README.md] [src: evidence:handbook/review-records.md]

For a tabular claim, inspect the page image or available source preview with its caption and headers. Where no public preview is available, use the acquired source in the team library. The review must establish what the value refers to, not merely that its characters appear somewhere on the page. [src: evidence:workflows/submissions/README.md §Source previews]

The older local dashboard and one-unit review page remain relevant when replaying historical records. Their local Apply operation and CSV import behaviour are not the current hosted submission route. The historical importer can replay disagreements differently from the consensus workflow; a private preview is neither submission nor proof of application. [src: evidence:workflows/review_exports/README.md]

## The review decision

Each reviewer gives one of three decisions per unit. The table describes the intended record state after an eligible decision is applied; saving or submitting a vote alone does not change the register.

| Decision (dashboard) | Review page | Effect on the unit |
|---|---|---|
| Keep (`ok`) | Approve | the reviewed claim stands within its approval scope; this is not numerical-calibration approval |
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
| `species_envelope` | a species or crop envelope tagged as practice-level; correct scope rather than drop solely for that mismatch; assess other defects separately |
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

Older codes merged into these (row-stitching and table-garble into `table_error`; an earlier weight code into `unusable_value`) may still appear in historical logs. [src: src/nbs_ruralscan/schema_tools/review.py §REASON_CODES] The codes are not bookkeeping: each is routed to a specific fix in the retrospective after every sweep. [src: methodology/extraction_retrospective.md §QA/QC review feeds the loop (reason codes)]

## Several reviewers: consensus and conflict

Current submissions are checked against their authenticated reviewer, original receipt, finding identity and revision. Repeated identical receipts do not create additional reviewer votes. Opposing eligible ballots remain pending for reconciliation; a challenge to an existing reviewed finding must be reconciled with its recorded decision. The operator applies accepted changes against current registers through a protected pull request. [src: evidence:workflows/submissions/README.md §Apply approved submissions]

Three states therefore remain distinct: a reviewer has expressed a judgement; eligible reviewers agree on a proposed change; the accepted change is committed and published. An uncontested ballot does not automatically bypass the integration gate. Check the applied journal and the finding at the same register revision before claiming completion. [src: evidence:handbook/review-records.md]

The historical local implementation stored decisions per evidence-unit/reviewer pair, applied agreement without a minimum reviewer quorum and reopened disagreement as conflict. Those semantics explain its saved logs. They do not mean that a late challenge in the hosted queue has already rewritten an applied record. [src: src/nbs_ruralscan/schema_tools/submit_review.py] [src: evidence:workflows/submissions/README.md]

Compiled hazard, scorecard and economic rows have their own rating-review history. Approving a source claim does not approve every derived row that cites it, and approving a row does not erase source-level limitations. [src: evidence:handbook/review-records.md]

## Soft delete: why evidence is never hard-deleted

A drop is never a deletion. It sets `review_state = dropped`. The row stays in the register as a restorable record, and is excluded from synthesis, from the progress counts and from dashboard tallies. Hard-deleting evidence is forbidden; any historic hard deletion is recovered from version history as a dropped row. [src: AGENTS.md §What is locked]

The method keeps dropped evidence for three reasons.

1. Reviewers are fallible. A drop may be reversed by a later reviewer or a changed rule; deletion would make that impossible.
2. The audit trail must show what was rejected and why. A reader auditing a recipe row needs to see the evidence that was set aside, not only what was used.
3. Rules change. Each unit carries the ruleset version under which it was last evaluated, so re-evaluations are auditable. A rule that later broadens (for example, readmitting crop-level evidence for a family) can bring dropped units back without re-extraction. [src: AGENTS.md §What is locked]

In the pinned producer implementation, automatic quarantine follows the same model. When scope or practice checks fire on a unit no person has touched, the build soft-drops it and stamps the reason, so obvious errors do not crowd the reviewer's queue. It never re-quarantines a unit that a reviewer has approved, dropped, decided, or reopened. [src: src/nbs_ruralscan/schema_tools/quarantine.py §module docstring]

Rule changes applied retroactively also use soft drops under a named rule rather than deletion, so every affected unit is reversible. [src: methodology/RULESET_VERSIONS.md §v1.6.18]

Generated rows may not cite dropped evidence: a check on each row's account fails a row whose evidence list includes a dropped unit. [src: src/nbs_ruralscan/schema_tools/check_account.py §module docstring]

## Re-opening

For a current finding, submit a challenge or correction against its recorded revision and reconcile it through the submission workflow. The historical local review implementation can reopen any active, queried or dropped unit. Its reopening operation returns the unit to the active state, restores its most recent automatic flag text so it re-enters the worklist, and logs the reset under the reviewer's name, even if the unit was never approved, so that an old query cannot hide it. [src: src/nbs_ruralscan/schema_tools/review.py §reopen_units]

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

A reviewer's keep decision approves only the interpretation actually reviewed. It does not imply that variable use, direction and numerical calibration all passed. It does not approve the numbers as an executable calibration. Variable use, direction and calibration are assessed separately, and a generic keep is explicitly not numerical approval. [src: .agents/skills/extraction_contracts/T4_review_contract.md §Numeric plausibility gate] [src: .agents/skills/extraction_contracts/T4_review_contract.md §Three independent assessments]

The reason is structural. Direction-only evidence cannot create scores, interpolation, cutoffs or default weights, so if a keep were read as approving the numbers, a published class could become a recipe threshold without anyone having checked its scientific basis. The review card therefore states the exact approval question, what approval retains, and what it cannot activate. Held or unrecorded calibration is never presented as a score, a range or "reviewed". [src: .agents/skills/extraction_contracts/T4_review_contract.md §Agreement and review output]

### Worked illustration: keep the source profile, hold its use

The rainfall-class warning above has three possible dispositions, not one yes/no verdict. A reviewer can confirm that the source uses rainfall, accept its regional ordering, and leave the numerical transfer unresolved. The record should say which of those judgements passed and why the calibration remains held. A later generic Keep must not silently remove that hold.

For the hypothetical soil-loss claim in [[ch:evidence-principles]], a source check may confirm the 20% figure yet reveal that the treatment included fertiliser alongside bunds. Correct the attribution or query it before accepting a practice-specific effect. Finding the number on the page resolves transcription; it does not isolate the bunds' contribution. [src: .agents/skills/extraction_contracts/T4_review_contract.md §Three independent assessments] [src: methodology/RULESET_VERSIONS.md §v1.6.7]

### The adversarial reviewer checklist

An independent reviewer reports separate findings for variable use, direction, numeric calibration, scope and transfer, and table coverage, and challenges omissions as well as additions. The checklist asks whether every table row was inventoried (including soil properties and unsuitable classes), whether directions and source values were kept as well as weights, whether a map legend describes suitability rather than merely low and high measurements, whether shared weights stay at their stated level, whether page and image references are correct, whether regional, crop, species and priority contexts are kept apart, and whether plausibility was assessed separately from quote matching. [src: .agents/skills/extraction_contracts/T4_review_contract.md §Adversarial reviewer checklist]

Agreement is reported as separate counts of variable use, direction and calibrated functions, deduplicated by independent lineage, variable and compatible context. Opposite directions are preserved as disagreement. Reviewed and unreviewed tallies are kept distinct. A count is not a runtime weight, confidence score or percentage without an explicit eligible denominator. [src: .agents/skills/extraction_contracts/T4_review_contract.md §Agreement and review output]

### OCR-derived evidence

For OCR-derived units, complete the page-image sample check specified in [[ch:acquisition]] before approval. Text-layer matching alone cannot resolve a misrecognised printed value. [src: methodology/search_protocol.md §Scanned PDFs (no text layer)]

## The progress ledger in the pinned edition

Project progress is recorded per practice, table, discovery process and family in a progress ledger. It answers questions such as "has a targeted search been run for this family and table?" from a record, never from whether evidence happens to exist, because absence of evidence does not show that a search was not run. [src: src/nbs_ruralscan/schema_tools/ledger.py §module docstring]

The ledger separates stages that must be stamped from facts that can be derived. [src: src/nbs_ruralscan/schema_tools/ledger.py §module docstring]

Authored stages (searched, screened, verified) cannot be derived from data. The pipeline step that does the work stamps them as not started, in progress or done. Derived facts (extraction and review) are read live from the Evidence Register.

A reconciliation check runs in every build and fails it when: [src: src/nbs_ruralscan/schema_tools/ledger.py §check]

1. a search is marked done with no matching search-register row (no claimed search without its logged protocol);
2. verification is marked done for a cell with no evidence units;
3. a status, table or process value is invalid.

It also warns, without failing, about cells that hold evidence from a process whose search is not marked done, which signals ad hoc or incomplete coverage. [src: src/nbs_ruralscan/schema_tools/ledger.py §coverage_warnings]

The project's locked description of the ledger lists a fuller lifecycle (searched, screened, extracted, verified, reviewed) with stage-order enforcement and a requirement that reviewed stages rest on approved units. The ledger code at the pinned revision stores only the three authored stages and derives extraction and review from the register; the stage-order and reviewed rules are not visible in its check. [src: AGENTS.md §What is locked] [src: src/nbs_ruralscan/schema_tools/ledger.py §check]

For the generated effect tables, a separate report places each practice and table in a seven-stage pipeline: searched, acquired, extracted, reviewed, synthesised, prose written, benchmarked. Every number in it is read from an existing artefact. It measures pipeline position, not evidence quality. [src: src/nbs_ruralscan/schema_tools/table_progress.py §module docstring]

Source records follow the same discipline. A newly acquired source starts as `pending`; it becomes `swept` only when an inventory accounts for its relevant pages, tables, continuations, figures and supplements. Completion is never inferred from the presence of a source or evidence rows. [src: .agents/skills/source-command-extract-evidence/references/defects.md §Pipeline integrity (v1.7.0)]

### Why progress cannot be claimed without a record

Progress claims feed decisions: whether a family has evidence enough to synthesise, whether a scorecard cell is empty because nothing exists or because nobody looked. A claim that is not backed by a register record cannot be audited, and an unaudited "done" hides exactly the gaps a scoping tool must show. The checks make specific unsupported claims fail the build, while other gaps produce warnings. They do not prove that a completed search was exhaustive or that every lifecycle rule was enforced. [src: AGENTS.md §What is locked]

Two corollaries follow. Effort counts (sources searched, units extracted, units reviewed) measure work, not the strength of evidence. And a local vote, a successful rehearsal or a feedback report does not establish that a review was submitted; only the corresponding event and state in the committed records do. [src: evidence:handbook/review-records.md §Find the right review record]

## Assumptions and limits

- **Consensus is not a second scientific review.** One eligible ballot can be uncontested; a protected application PR is a separate integration gate. Neither establishes that two people independently assessed the claim.
- **QC and human approval are different records.** Every extracted item receives automated/AI checks. A missing human approval is not a missing QC pass, and a clean automated result is not proof of scientific validity. Report recorded human decisions separately; do not infer universal human review from universal QC.
- **Reason codes are coarse.** They route fixes well but compress nuanced judgements; the free-text note carries the detail.
- **Plausibility review is documentary.** It records the scientific concern and the justification available; it is not automated validation and introduces no universal thresholds.
- **Ledger rules and their description differ** at the pinned revision, as noted above; readers should rely on the build check, not the description, for what is enforced.
- **Feasibility still validates.** Approved scoping evidence does not replace site-level verification of thresholds, datasets and costs in a feasibility study.

## Where this is configured

- Review fields on [[table:EV]] (`reviewer_ok`, `review_state`, `ruleset_version`); search protocols in [[table:SRCH]].
- Current submission, reconciliation and application: `workflows/submissions/` in the evidence repository; receipts and the applied journal identify published changes.
- Historical decision store, review log and consensus: `src/nbs_ruralscan/schema_tools/review.py`, `submit_review.py`.
- Automatic quarantine: `src/nbs_ruralscan/schema_tools/quarantine.py`.
- Numeric plausibility gate and reviewer checklist: `.agents/skills/extraction_contracts/T4_review_contract.md`.
- Progress ledger: `src/nbs_ruralscan/schema_tools/ledger.py`; effect-table progress: `src/nbs_ruralscan/schema_tools/table_progress.py`.
- Related chapters: [[ch:extraction]], [[ch:suitability-synthesis]], [[ch:effect-synthesis]].
