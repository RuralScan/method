---
title: Rulesets and the learning loop
slug: rulesets-and-learning
summary: Find the exact instructions that governed any past search or evidence unit, run the retrospective after a sweep, and turn a recurring defect into a rule and a deterministic check.
sources:
  - methodology/RULESET_VERSIONS.md
  - methodology/extraction_retrospective.md
  - methodology/search_protocol.md
  - .agents/skills/source-command-extract-evidence/SKILL.md
  - .agents/skills/source-command-extract-evidence/references/defects.md
  - .agents/skills/source-command-discover-sources/SKILL.md
  - src/nbs_ruralscan/schema_tools/learnings.py
  - src/nbs_ruralscan/schema_tools/sweep_metrics.py
  - src/nbs_ruralscan/schema_tools/check_numbers.py
  - src/nbs_ruralscan/schema_tools/review.py
  - schema/structure/columns.json
  - AGENTS.md
  - evidence:rulesets/README.md
  - evidence:workflows/discovery/README.md
  - evidence:handbook/assisted-evidence-run.md
---

## Why the instructions are versioned

Searches and extractions are carried out by people and by AI assistants following written instructions: a discovery protocol, an extraction skill with its defect catalogue, and contracts for each kind of claim. Those instructions change as the method learns. A threshold extracted under an earlier instruction set may have been read under rules that have since been tightened. To audit or reproduce it, a reader needs to know which rules applied. [src: methodology/RULESET_VERSIONS.md §Ruleset versions]

The method therefore treats the instructions as a versioned artefact called the *ruleset*. Every search row and every evidence unit carries a `ruleset_version` stamp, which is a required field on the search register and an optional but standard field on the evidence register. [src: schema/structure/columns.json §SRCH] [src: schema/structure/columns.json §EV]

## What a ruleset version pins

A ruleset version identifies the complete instruction set in force: the extraction skill, its defect catalogue, the extraction contracts, the slash command that delegates to the skill, and the discovery search protocol. Each version has an entry in the version log and an archived snapshot of the instruction text. [src: methodology/RULESET_VERSIONS.md §Ruleset versions] [src: methodology/search_protocol.md §Version control of the instructions (reproducibility)]

A new version is cut, with a snapshot, whenever the extraction skill, the screening funnel or criteria, the search protocol or the discovery channels change. The intended semantic versioning is: [src: methodology/RULESET_VERSIONS.md §Ruleset versions]

- **patch** for a clarification,
- **minor** for a new rule, defect code or check,
- **major** for a process change.

New work is stamped with the version actually used. Historical records are never restamped when the rules change; units extracted under an earlier version stay valid unless a specific retroactive pass is applied and logged. [src: .agents/skills/source-command-extract-evidence/SKILL.md §Evidence extraction] Where a change is applied retroactively, it is done by reversible soft drops under a named rule, not by editing or deleting units. [src: methodology/RULESET_VERSIONS.md §v1.6.18]

## How a past search or extraction is reproduced

To reproduce a past search, a reader takes its search-register row (verbatim query strings, inclusion criteria, limits, counts, date) and the instruction snapshot its version points to. [src: methodology/search_protocol.md §Version control of the instructions (reproducibility)] The frozen captures and screening worksheet then replay exactly; re-running the query against a live index is a new run that may return different records. [src: evidence:workflows/discovery/README.md §Run a new search]

To reproduce an extraction, the reader takes the evidence unit's version, the snapshot, and the cached artefact identified by its hash, and reapplies the instructions to the cited passage.

The method is candid about the limits of this. [src: methodology/RULESET_VERSIONS.md §Historical version collisions]

- Two early version numbers each have more than one change-log entry, and one version was added as an addendum while the live skill header still showed the previous number. For those records, the stamp alone cannot always reconstruct the combined instruction set; the producing commit, the lane report and the source inventory are used alongside it. Versions are not renamed after the fact.
- From version v1.7.0 onwards, the complete active skill, catalogue, contracts, command and search protocol are snapshotted together, and tests check that the active instructions match their snapshot.
- Archived instructions omit operator-specific prompts, model responses and settings. A byte match proves which instructions were archived; it cannot establish the exact conversation of an original extraction. Some archived skill files also declare a different version in their header from the stamp on the records produced under them; the discrepancy is preserved rather than corrected. [src: evidence:rulesets/README.md §Which instructions apply to the terrace example?]

For new assisted runs, the operator records the ruleset version, the exact instruction files and their hashes, the model identifier, settings and the actual prompt, so that later runs are more fully reproducible than the early ones. [src: evidence:handbook/assisted-evidence-run.md §Record and hand over the run]

The version log does not always follow its own patch/minor convention: several entries labelled patch add a defect rule or an advisory check. Readers should rely on the content of each entry, not its label. [src: methodology/RULESET_VERSIONS.md §Ruleset versions]

## The retrospective after every sweep

An extraction sweep is followed, every time, by a retrospective whose purpose is to make the next sweep measurably better. [src: methodology/extraction_retrospective.md §Extraction sweep retrospective] The loop has six steps. [src: methodology/extraction_retrospective.md §The loop]

1. **Measure.** Append the register's quality metrics to an append-only sweep log and print the change since the previous sweep.
2. **Gate.** Confirm the provenance guardrail, the number check, the schema structure check and the tests pass.
3. **Triage flags.** Read the flagged units and the number-check misses, group them by defect type, and ask whether any pattern is not yet in the defect catalogue.
4. **Encode the learning.** Add each new defect pattern to the catalogue and cut a new ruleset version with a snapshot. If the defect is deterministically detectable, add or extend a check so that it is caught automatically next time. If it exposes a gap in the schema, record a schema-change proposal.
5. **Commit** the metrics row and any rule or check changes together.
6. **Trend check.** If a rate did not fall, the change in step 4 was insufficient and is tightened before the next sweep.

At least one learning is encoded per sweep whenever flags exist. [src: methodology/extraction_retrospective.md §The loop]

### The metrics that must trend down

| Metric | What it measures |
|---|---|
| `numberprov_rate_pct` | share of units with a number in the relationship that is not in the quote |
| `verify_rate_pct` | share of units the adversarial relationship check finds unfaithful |
| off-scope rate | share of units flagged as the wrong kind of claim for their role |

[src: methodology/extraction_retrospective.md §The loop] [src: AGENTS.md §What is locked]

"Better" also means that the catalogue grows and that the share of defects caught deterministically, rather than by a costly model-based review, grows. [src: methodology/extraction_retrospective.md §What "better" looks like]

The recorded trajectory shows the loop working. Early sweeps had around 40 % of numeric units flagged on relationship faithfulness. [src: methodology/extraction_retrospective.md §Why] Later version entries record the register-wide number-provenance rate falling in steps from 7.7 % to 5.6 % and the verification rate from 1.0 % to 0.1 %, with several rounds adding hundreds of units and no new number-provenance flags. [src: methodology/RULESET_VERSIONS.md §v1.6.11] [src: methodology/RULESET_VERSIONS.md §v1.6.12] [src: methodology/RULESET_VERSIONS.md §v1.6.14] One ruleset revision also changed the check itself: provenance tokens were exempted, and the rate before that retrospective was 45.8 %. Rates either side of a change to the check are not one series. [src: methodology/RULESET_VERSIONS.md §v1.6.6] One deep pass pushed the number-provenance rate up for the first time in seven sweeps, which is how the rule that numbers in explanatory text also count was found. [src: .agents/skills/source-command-extract-evidence/references/defects.md §Common extraction defects]

Rates are only comparable across sweeps with comparable scope and denominators; a smaller or easier batch is not proof of improvement. [src: methodology/extraction_retrospective.md §Feedback accounting (v1.7.0)]

### Cheap checks first

The deterministic checks cost nothing to run, so they run first. Only their flagged units and units with low extraction confidence are sent to the more expensive adversarial relationship review. As the rules tighten, fewer units should need that review. [src: methodology/extraction_retrospective.md §Pre-LLM triage (efficiency)]

## Review decisions feed the loop

Human review is the second source of learning. Each decision carries a reason code, logged when applied. The retrospective tallies the codes and routes the most frequent to its fix. [src: methodology/extraction_retrospective.md §QA/QC review feeds the loop (reason codes)]

| Dominant reason | Routed fix |
|---|---|
| smuggled number | already caught by the number check; tighten the extraction rule |
| row stitching or table garble | improve table handling and the rule to quote a whole row with its header |
| wrong variable | add ontology aliases and proxy rules |
| quote too narrow | require wider context |
| off scope | tighten screening; down-weight that source class |
| false flag | loosen the check that over-flagged |

[src: methodology/extraction_retrospective.md §QA/QC review feeds the loop (reason codes)]

### Incorporation is tracked, not claimed

A learning loop is only honest if every review decision is read and acted on. A learnings cursor makes this provable: the review log grows as people review, a separate log records each retrospective (how much feedback it processed, the dominant reason, the off-scope rate and the concrete adjustment), and the build prints a note whenever review decisions outpace the last retrospective. [src: src/nbs_ruralscan/schema_tools/learnings.py §module docstring]

Since version v1.7.0 the cursor tracks content, not row counts. A changed decision, reason or note on an existing pair of evidence unit and reviewer counts as new learning work; re-applying an unchanged decision does not. A full retrospective may advance the cursor only after reading the complete feedback set. A bounded pass on one reviewer's decisions records receipts for the exact decisions inspected and leaves the global cursor unchanged; the next full retrospective supersedes them. [src: methodology/extraction_retrospective.md §Feedback accounting (v1.7.0)] [src: .agents/skills/source-command-extract-evidence/references/defects.md §Pipeline integrity (v1.7.0)]

## From recurring defect to deterministic check

The defect catalogue is the memory of the loop: each entry names a pattern, the reason it matters and the correct encoding. Where a pattern can be detected without judgement, it gains a check. The table below pairs the main recurring defects with the check that now catches them. [src: .agents/skills/source-command-extract-evidence/references/defects.md §Common extraction defects]

| Recurring defect | How it was caught before | Deterministic catch now |
|---|---|---|
| Quote reconstructed from memory or abstract | contamination audit | provenance guardrail fails the build if the quote is not on the cited page |
| Number imported from elsewhere in the paper | two adversarial review waves | number-provenance check over the whole relationship, including strings and number words |
| Quote from a study-site, methods or accounting section | human review (most early drops) | scope check section signals, feeding auto-quarantine |
| Bare table cell or whole table as quote | human review | quote-width check (minimum length; 160-word maximum) |
| Species claim tagged as practice-level | human review | species check on taxon field, quote and citation |
| Wrong practice borrowed from sweep context | human review | PICOS check, feeding auto-quarantine |
| Context recorded under many key spellings | failed applicability grouping | context-key check against a fixed vocabulary |
| Strength from adjectives | review | band check against the magnitude register |
| Direction coded as "good = positive" | reviewer confusion over a correctly coded benefit | direction-sense lookup, required verbatim cue, cue-conflict check; build fails on a variable with no sense row |
| Study descriptors written into the outcome field | build flags after a lane passed staging | staging gate runs the same whole-relationship number check as the build |
| Wrong DOI stitched to a right title | audit of the acquisition queue | Crossref round trip in every build |
| Wrong document cached under a DOI-less source | title mismatch found by chance | title-in-opening-pages check |
| Adoption rate extracted as an operational factor | review drops | policy lookup; staging gate refuses the unit |
| Scored class edge or recommended range encoded as a hard limit | reviewers removing inferred limits | advisory scope signals for ranked-class limits, recommended ranges and design geometry |

[src: AGENTS.md §Don't] [src: src/nbs_ruralscan/schema_tools/check_numbers.py §module docstring] [src: .agents/skills/source-command-extract-evidence/references/defects.md §Common extraction defects] [src: .agents/skills/source-command-extract-evidence/references/defects.md §Operational-risk (M2b) evidence] [src: .agents/skills/source-command-extract-evidence/references/defects.md §Limits, geometry and duplicates] [src: methodology/RULESET_VERSIONS.md §v1.6.0] [src: methodology/RULESET_VERSIONS.md §v1.6.10] [src: methodology/RULESET_VERSIONS.md §v1.6.17]

Some checks are tuned against the drops that motivated them before they ship. The site-context signal, for example, was set to catch all six motivating drops while raising no false positives on genuine rules in the same set. Checks whose signals are proxies stay advisory, and checks designed to prompt re-slicing or judgement are never allowed to drop units automatically. [src: methodology/RULESET_VERSIONS.md §v1.3] [src: methodology/RULESET_VERSIONS.md §v1.10.1]

Not every defect can be automated. Choosing the right canonical variable, judging whether a claim is a generalising rule, or deciding whether a published band is plausible remain human judgements recorded in the catalogue and contracts.

## Ruleset history by behaviour change

The history below is grouped by what changed in the behaviour of discovery and extraction. Version numbers are given where they define behaviour. [src: methodology/RULESET_VERSIONS.md §Ruleset versions]

### Baseline (v1.0)

Formalised the four discovery processes, the five-step screening funnel, the initial defect catalogue (wrong table, wrong practice, missed relationship, constrained area of interest, uninterpretable weight, speculation, insufficient context), a positive-bias discount for grey literature, the practice-in-source rule, and the first deterministic guards (provenance, numbers, scope, practice, quarantine).

### Search protocol

- **Generic versus targeted searches** were separated, search terms had to be captured verbatim, and practice searches had to carry the full synonym set (v1.1).
- **New bibliographic channels**: a scriptable scholarly index and a manual multilingual agricultural index were added, and large commercial indexes were deliberately skipped (v1.6.5).
- **Discovery became its own instruction set** with explicit per-family protocols, staged literature, grey and tool lanes, and exact counts (v1.8.1).

### Scope and routing of claims

- **Species and crop evidence is tagged and kept,** never dropped, with a deterministic mis-tag check; the crop-versus-species boundary is set by product and cultivation (v1.2, v1.4.1).
- **A study's own site conditions are context, not a rule** (v1.3).
- **Soft enabling factors** go to the operational-risk role; adoption rate is excluded from it; quotes for operational claims come from the main text with cause and effect (v1.9.0).
- **A suitability lane must first show the source's spatial-targeting purpose** (v1.9.5).
- **Practice boundaries** were sharpened: reduced tillage is not a capture structure, and synthetic mulch is never nature-based (v1.6.14, v1.9.2).

### Quotes and numbers

- **Quotes are sliced from the text layer,** never retyped; unquotable passages are blockers (v1.5.1).
- **Shape parameters use canonical keys only,** because non-canonical keys were silently invisible to synthesis (v1.4).
- **Locale number formats, ligatures, number words and multipliers** are read by the number check (v1.6.1, v1.6.12, v1.6.14).
- **Process metadata and study descriptors** stay out of the claim fields (v1.6.6, v1.6.10).
- **Quote width** is bounded at both ends (v1.6.8).
- **Corrections must pass the same number check** as extractions (v1.10.1).

### Effect tables

- Effect extraction was **paused** as per-paper row extraction failed on the shape of the evidence (v1.5.0), then **reactivated as generated tables** built by cell synthesis, with the effect and asset-vulnerability roles, the structured relationship object, fixed context keys, magnitude bands, and deferred pointers for single-pass reading (v1.6.0).
- **Encodings** were added for with-and-without contrasts (v1.6.2), author-stated hazard severity (v1.6.3) and stated hazard magnitude (v1.9.7), comparators for existing ecosystems (v1.6.4), bundled interventions, absent normal-year references and beneficiaries (v1.6.7), the source's own description of the practice (v1.6.9), and cost nature (v1.6.13).
- **Interpretation rules** were added: a decaying service is not a harm and a baseline is not an effect (v1.6.11); a spread is not a sign and an annualised establishment cost is not recurrent (v1.6.12); direction is on the variable as named with a verbatim cue (v1.6.17); every effect needs a stated mechanism (v1.6.18); significance uses the 5 % convention (v1.9.1); a range is classed by its weaker end (v1.9.9); one dataset yields one unit (v1.10.1).
- **Readability**: acronyms expanded, baselines and absolute amounts recorded, source tables named (v1.9.3).

### Suitability completeness and calibration

- **Table and continuation inventories** and full-paper claim accounting are required before a source is called swept (v1.6.14, v1.6.15).
- **Variable use, direction and numeric calibration are assessed separately;** direction without calibration is retained evidence, superseding earlier advice to discard it (v1.6.16).
- **Compiler status may not hide a source relationship** (v1.9.4).
- **Numeric plausibility review** is mandatory before calibration, and complete regional tables are retained for compatible-source synthesis (v1.9.6, v1.9.8).
- **Observed practice ranges are not suitability bounds;** a hard limit needs the source to say land beyond it is excluded; buffer widths are design geometry (v1.10.0, v1.10.1).

### Pipeline integrity

- **Identity before payload**: registered and verified source, opening-title match, positive page, no self-granted approval; acquired is not extracted (v1.7.0).
- **Adversarial hardening**: metadata identity is not artefact identity; translations cannot manufacture provenance; typed payloads are strict; rediscovery is tracked reuse; compilation cannot reassign scope (v1.8.0).
- **Title verification** for sources without a DOI, and fixed-form practice-database entries recorded as observed presence (v1.6.0).

## Assumptions and limits

- **Early stamps are imperfect.** Version collisions and header mismatches mean some historical records need the commit and lane report alongside the stamp.
- **Prompts are not fully archived** for early runs; reproduction recovers the instructions, not the exact model interaction.
- **Metrics are proxies.** Falling flag rates show that known defects are rarer. They do not measure defects no check detects, and they depend on comparable scope.
- **The loop is retrospective.** Rules improve after errors are found; units extracted before a rule existed keep their version and may carry the old defect until a targeted backfill.
- **Learning depends on review volume.** Where few decisions are made, few patterns surface.

## Where this is configured

- Version log: `methodology/RULESET_VERSIONS.md`; snapshots under `.agents/skills/_versions/<version>/`.
- Active instructions: `.agents/skills/source-command-extract-evidence/SKILL.md` and its defect catalogue (`references/defects.md`), `.agents/skills/extraction_contracts/`, `.agents/skills/source-command-discover-sources/SKILL.md`, `methodology/search_protocol.md`.
- Retrospective procedure: `methodology/extraction_retrospective.md`; metrics: `src/nbs_ruralscan/schema_tools/sweep_metrics.py`; learnings cursor: `src/nbs_ruralscan/schema_tools/learnings.py`.
- Version stamps on [[table:SRCH]] and [[table:EV]].
- Related chapters: [[ch:extraction]], [[ch:review-and-quality]], [[ch:discovery]], [[ch:editions]], [[ch:reproduce]].
