---
title: Continue the evidence base with an AI system
slug: continue-with-ai
summary: Set up and run the agent-plus-human system that adds sources, findings and re-synthesised rows to the evidence base, knowing which instructions, checks and human decisions govern each step, where each kind of record is written today and which routes are still planned.
sources:
  - AGENTS.md
  - CLAUDE.md
  - PLAYBOOK.md
  - ONBOARDING.md
  - pyproject.toml
  - .github/workflows/ci.yml
  - .github/workflows/auto-merge-review.yml
  - scripts/setup-repo.sh
  - docs/HYDRATION.md
  - docs/REVIEWER_GUIDE.md
  - methodology/RULESET_VERSIONS.md
  - methodology/search_protocol.md
  - methodology/extraction_retrospective.md
  - .agents/skills/source-command-discover-sources/SKILL.md
  - .agents/skills/source-command-extract-evidence/SKILL.md
  - .agents/skills/source-command-t4-synthesise/SKILL.md
  - .agents/skills/source-command-t3t6-synthesise/SKILL.md
  - .agents/skills/source-command-new-recipe/SKILL.md
  - .agents/skills/source-command-update-variable-card/SKILL.md
  - .agents/skills/extraction_contracts/T4_review_contract.md
  - .agents/skills/extraction_contracts/T3_T6_extraction_contract.md
  - .agents/skills/extraction_contracts/DIRECTION_ADDENDUM.md
  - .agents/skills/extraction_contracts/T5_contract.md
  - .claude/commands/sweep-retro.md
  - .claude/commands/t3t6-synthesise.md
  - schema/spec.md
  - src/nbs_ruralscan/schema_tools/ledger.py
  - src/nbs_ruralscan/schema_tools/search_log.py
  - src/nbs_ruralscan/schema_tools/learnings.py
  - src/nbs_ruralscan/schema_tools/quarantine.py
  - src/nbs_ruralscan/schema_tools/validate_sources.py
  - src/nbs_ruralscan/schema_tools/verify_metadata.py
  - src/nbs_ruralscan/recipe/prose.py
  - scripts/discover-sources.py
  - scripts/register-discovery.py
  - scripts/intake-downloads.py
  - scripts/ingest-effects-staging.py
  - scripts/build-review-batch.py
  - scripts/apply-review-export.py
  - scripts/build-row-review-batch.py
  - scripts/apply-row-review-export.py
  - scripts/write-prose.py
  - scripts/submit-review.sh
  - evidence:README.md
  - evidence:handbook/assisted-evidence-run.md
  - evidence:handbook/review-records.md
  - evidence:rulesets/README.md
  - evidence:rulesets/catalog.json
  - evidence:registers/manifest.json
  - evidence:workflows/discovery/README.md
  - evidence:workflows/acquisition/README.md
  - evidence:workflows/extraction/README.md
  - evidence:workflows/evidence_snapshot/README.md
  - evidence:workflows/run_record/README.md
  - evidence:workflows/submissions/README.md
  - evidence:workflows/submissions/registration.md
  - evidence:workflows/submissions/recipe-rows.md
  - evidence:workflows/submissions/check_registers.py
  - evidence:workflows/review_exports/README.md
  - evidence:publication/recipe-candidate.json
  - evidence:registers/applied-receipts.json
  - evidence:registers/methodology/decisions/method_decisions.csv
  - evidence:configuration/README.md
  - evidence:.github/workflows/evidence-checks.yml
  - method:dashboard/ai.html
  - method:decisions/README.md
  - method:configuration/README.md
  - retired:.ciat-evidence-readonly
  - retired:AGENTS.md
  - retired:methodology/migration/2026-11-05/migration-map.csv
---

> **Historical draft, not current operating instructions.** T3/T6 scientific
> synthesis now follows [[ch:effect-synthesis]] and RuralScan/evidence's
> `workflows/synthesis/README.md`. AI authors judgments; code validates and packages
> exact accepted outputs. The automatic effect generator is retired. T6E stays
> historical. The remaining draft below documents the earlier transition.


## What this chapter is for

Continuing the evidence base means three kinds of work: finding and acquiring more sources, extracting more findings (evidence units) from them, and re-running synthesis so that suitability rules, hazard rows and scorecard rows reflect the enlarged and reviewed evidence. The rules for each step are set out in [[ch:discovery]], [[ch:acquisition]], [[ch:extraction]], [[ch:review-and-quality]], [[ch:suitability-synthesis]], [[ch:effect-synthesis]] and [[ch:rulesets-and-learning]]. This chapter explains how to set up and operate the system that applies those rules: an AI coding agent of your choice, a set of versioned instruction files, deterministic checks, and people who approve what enters the record.

The governing principle: model output is a proposal; only records that pass the deterministic checks enter the registers, and people then decide which findings are kept, held or dropped [src: evidence:README.md §Planned structure] [src: AGENTS.md §Don't] [src: .agents/skills/source-command-extract-evidence/SKILL.md §Close the work]. The chapter works from two revisions and keeps them apart. The scientific edition this methodology describes is the producer repository at revision `e5c8da02`: its rules, instruction files and engines are cited at that revision, as in every other chapter. The operating procedures for recording new work are those of the evidence repository at revision `8c6f793f`, which is later. A command or path cited to the producer belongs to the scientific edition; a command cited to the evidence repository is how the same work is recorded now.

Read this first if you are starting now. Since this edition, the producer repository's evidence records are read-only: a marker file on its main line names every protected path and the evidence repository as their destination, and at that revision the producer's registrar, staging ingest and review writers refuse to run, and its continuous integration rejects any change to a protected path [src: retired:.ciat-evidence-readonly]. The producer still holds the historical records, the instruction files and the compiler that the evidence repository pins. New evidence work is recorded in the evidence repository, always the same way: a proposal is prepared, opened as a protected pull request, checked by continuous integration and merged by a person.

Finding votes and extraction proposals continue as before. Seven further routes work at the operating revision:

1. recording a discovery run, including its search record and acquisition candidates;
2. stamping progress from the step that produced it;
3. registering an acquired source before its first extraction;
4. rebuilding the compiled tables and changing row wording;
5. recording a review of a compiled rating;
6. recording a scientific method decision, in the method repository;
7. releasing changed definitions and rule tables from the method repository and adopting them for compilation, and updating the tool register and source-specific mappings that the evidence repository owns.

One route is planned and not yet built: recording a retrospective with its sweep metrics and learnings cursor. A few compiler inputs are also still held at archived revisions, most importantly the accepted suitability functions and their weights. Both are listed under "Recording work now".

The loop below is written from the producer's instruction files, because that is where the rules and the engines are. Each step then names the route that records it today.

## The system in one view

The system has nine moving parts. An orchestrating agent reads versioned instructions, delegates bounded lanes to sub-agents, and owns every write to the registers. Sub-agents write only to a staging folder. Deterministic checks run centrally, not inside the agent. People decide what is kept, what is held and which rules change [src: AGENTS.md §Don't] [src: .agents/skills/source-command-discover-sources/SKILL.md §Agent contract].

| Part | What it is | Where it lives (at the pinned revision) | Who or what may change it |
|---|---|---|---|
| Instruction sets | Skills (task procedures), extraction contracts (claim shapes), slash-command wrappers, the defect catalogue | `.agents/skills/`, `.claude/commands/`, `AGENTS.md` | A ruleset bump with an archived snapshot, after a retrospective [src: methodology/RULESET_VERSIONS.md §Ruleset versions] |
| Orchestrating agent | Runs a skill, splits work into lanes, reconciles lane outputs, runs registration scripts and gates | The operator's own environment | Acts only within the scope the operator authorises [src: .agents/skills/source-command-extract-evidence/SKILL.md §Establish scope] |
| Sub-agents | Bounded discovery or extraction lanes | Write only under `pipeline/staging/` | Never edit registers, recipes or schema; never run version-control commands [src: AGENTS.md §Don't] |
| Source corpus | Cached PDFs, web and code snapshots that every quote is checked against | `.cache/corpus/` (not version-controlled); team library holds the originals | Filled by hydration and intake scripts, never committed [src: docs/HYDRATION.md §Corpus hydration] |
| Central checks | Provenance, number, scope, species, direction, context, band, metadata and structure checks | `src/nbs_ruralscan/schema_tools/` | Code changes through review; new checks come from retrospectives [src: methodology/extraction_retrospective.md §The loop] |
| Registers | Sources, evidence units, searches, families, variables, crosswalks, bands | `schema/registers/` (CSV is the source of truth) | Registration and ingest scripts; review apply; never hand-appended [src: AGENTS.md §Architecture] [src: AGENTS.md §Don't] |
| Review workspace | Local review server and dashboard, plus a one-unit review page with exportable decisions | `src/nbs_ruralscan/schema_tools/review_server.py`, `docs/review.html` | Human reviewers; decisions applied by consensus [src: AGENTS.md §What is locked] [src: AGENTS.md §File map] |
| Progress ledger and search register | Status per practice, table, process and family; the logged protocol of every search | `pipeline/progress_ledger.csv`, `schema/registers/SRCH_search_register.csv` | Stamped by the step that did the work; the build fails on unprovable claims [src: AGENTS.md §What is locked] |
| Retrospective loop | Metrics, defect triage, catalogue and check updates, a learnings cursor | `pipeline/metrics/`, `methodology/extraction_retrospective.md` | Run after every sweep [src: methodology/extraction_retrospective.md §The loop] |

The table gives locations in the producer repository at the scientific edition. The registers, progress ledger, review logs and metrics now live under `registers/` in the evidence repository, with the same relative paths, and are changed only through its protected pull requests [src: evidence:workflows/evidence_snapshot/README.md §Register migration seed] [src: evidence:workflows/submissions/README.md §Which records can I update?]. The instruction sets and the engines are still read from the producer.

## Before you start

Two setups are described. The first is what you need to record work now. The second is what you need only to reproduce the scientific edition or to run the producer's checks on private copies. No single setup guide covers the evidence pipeline end to end; both lists are assembled from several files.

### To record work now (evidence repository)

- **An up-to-date clone of the evidence repository.** Every operator command is run from it and names the full revision of its main line that you inspected [src: evidence:workflows/submissions/registration.md §Register discovery, sources and progress].
- **Python 3.12 with the evidence check dependencies.** Continuous integration installs PyMuPDF, requests and NumPy at fixed versions on Python 3.12; the operator and apply commands use the same environment [src: evidence:.github/workflows/evidence-checks.yml] [src: evidence:workflows/submissions/README.md §Apply approved submissions]. The acquisition tool also needs uv; the offline screening replay runs on Python 3.10 or later with the standard library [src: evidence:workflows/acquisition/README.md §Worked example · WOCAT terrace manual] [src: evidence:workflows/discovery/README.md §Replay the terrace screening example].
- **Git and the GitHub command-line client, signed in as yourself.** Submissions are public issues under the submitter's own account, and the original issue supplies the reviewer identity and time; no typed name can replace it [src: evidence:workflows/submissions/README.md §Use the local desk for browser or CSV entry] [src: evidence:workflows/submissions/recipe-rows.md §Reviewer: browser or CLI].
- **A clone of the producer repository, used read-only.** The evidence tools read the pinned compiler and the instruction archives from it. They do not write to it [src: evidence:workflows/submissions/registration.md §Register discovery, sources and progress] [src: evidence:rulesets/README.md §Verify against a local clone].
- **A single-user computer for the local desk.** The desk binds to 127.0.0.1 on port 8934 and uses the local user's GitHub credentials. On a shared or remotely exposed machine, use the command line instead [src: evidence:workflows/submissions/README.md §Use the local desk for browser or CSV entry].
- **Access to the team source library and a local corpus.** Registering a PDF source needs a locally synchronised copy of the team's `library/` folder, because the command compares the shared copy's bytes with the acquisition receipt [src: evidence:workflows/submissions/registration.md §Register an acquired source]. Applying an extraction needs the acquired corpus [src: evidence:workflows/submissions/README.md §Apply approved submissions]. Restricted source files stay in the library and are never placed in a public issue. How a new team obtains library access is not documented.
- **Credentials named by steps.** `LENS_TOKEN` for Lens.org searches and `OPENALEX_API_KEY` for keyed OpenAlex access [src: evidence:workflows/discovery/README.md §Capture records]; `UNPAYWALL_EMAIL` to enable open-access recovery for a verified DOI [src: evidence:workflows/acquisition/README.md §Bibliographic identity and access]. DOI checks call Crossref online [src: evidence:workflows/acquisition/README.md §Bibliographic identity and access]. No other credentials are named.
- **An AI coding agent, if you use one.** The evidence repository's task briefs are model-neutral: a researcher can perform each interpretive step directly or give the brief to an assistant [src: evidence:handbook/assisted-evidence-run.md §Run an assisted evidence search and extraction]. No file states which model or effort level to use for each step; see the gaps list below.

### To reproduce the scientific edition (producer repository, read-only)

These items serve the producer commands quoted in the loop below. They let you read the instructions, run the checks and run trial syntheses on private copies. They do not record anything: the producer refuses the writes.

- **Python 3.12 or later and uv.** The package declares `requires-python = ">=3.12"`; continuous integration installs Python 3.12 through uv [src: pyproject.toml §project] [src: .github/workflows/ci.yml §checks].
- **The setup script, once after cloning** [src: AGENTS.md §Run / preview / deploy]:

```sh
bash scripts/setup-repo.sh
```

  The script registers three merge drivers (generated JSON, register CSVs, keyed JSON) and sets `core.autocrlf false` [src: scripts/setup-repo.sh]; `AGENTS.md` mentions only the first [src: AGENTS.md §Run / preview / deploy].
- **A hydrated local corpus.** The corpus is not version-controlled; it is copied from a local mirror of the team library whose root is set with the `NBS_LIBRARY_ROOT` environment variable [src: docs/HYDRATION.md §One-time: point at the library].
- **The producer's review server**, which ran locally on port 8765 at the scientific edition [src: docs/REVIEWER_GUIDE.md §Each review session]. It is not the current review route; use the live dashboard and the evidence repository's desk.
- **Tesseract**, for scanned PDFs only: the OCR adapter adds an invisible Tesseract text layer [src: methodology/search_protocol.md §Scanned PDFs (no text layer)].
- **The agent the producer team used.** The producer's onboarding guide names Claude Code and says it reads `AGENTS.md` at the start of every session [src: ONBOARDING.md §5. How to actually work with Claude Code].

## Where the instructions live

At the pinned revision there are six skills, four active extraction contracts, one defect catalogue and seven slash-command files.

| Name | What it governs | Stated version | Path |
|---|---|---|---|
| Discover sources | Bounded search, screening, lane outputs, central registration | v1.8.1 | `.agents/skills/source-command-discover-sources/SKILL.md` |
| Extract evidence | Scope, source checks, extraction, validation, staging ingest | v1.10.1 | `.agents/skills/source-command-extract-evidence/SKILL.md` |
| Defect catalogue | Known extraction defects to avoid, numbered | Follows the extraction ruleset | `.agents/skills/source-command-extract-evidence/references/defects.md` |
| T4 synthesise | Translating reviewed suitability evidence into rule proposals and compiling the recipe | None stated | `.agents/skills/source-command-t4-synthesise/SKILL.md` |
| T3/T6 synthesise | Cell synthesis of hazard and scorecard rows | None stated (refers to ruleset v1.6.0 contracts) | `.agents/skills/source-command-t3t6-synthesise/SKILL.md` |
| New recipe | Scaffolding a new practice recipe | None stated | `.agents/skills/source-command-new-recipe/SKILL.md` |
| Update variable card | Authoring a variable card | None stated | `.agents/skills/source-command-update-variable-card/SKILL.md` |
| T4 review contract | Source-purpose gate, three independent assessments, numeric plausibility | v1.6.16 in its header | `.agents/skills/extraction_contracts/T4_review_contract.md` |
| T3/T6 extraction contract | Effect-claim shape | v1.7.0 in its header | `.agents/skills/extraction_contracts/T3_T6_extraction_contract.md` |
| Direction addendum | Direction on the variable as named, with a verbatim cue | v1.6.17 | `.agents/skills/extraction_contracts/DIRECTION_ADDENDUM.md` |
| T5 contract | Justifications for opportunity-space variables | None stated | `.agents/skills/extraction_contracts/T5_contract.md` |
| Slash commands | `extract-evidence`, `t4-synthesise`, `t3t6-synthesise`, `new-recipe`, `update-variable-card`, `sweep-retro`, `fix-pr-conflicts` | None stated | `.claude/commands/` |

[src: .agents/skills/source-command-discover-sources/SKILL.md] [src: .agents/skills/source-command-extract-evidence/SKILL.md] [src: .agents/skills/source-command-t4-synthesise/SKILL.md] [src: .agents/skills/source-command-t3t6-synthesise/SKILL.md] [src: .agents/skills/extraction_contracts/T4_review_contract.md] [src: .agents/skills/extraction_contracts/T3_T6_extraction_contract.md] [src: .agents/skills/extraction_contracts/DIRECTION_ADDENDUM.md]

**Slash commands and skills.** The skill is the canonical instruction; the command file is a thin wrapper. The extraction command tells the agent to read and follow the extraction skill as "the single active instruction source", and the T4 synthesis command does the same for its skill [src: .claude/commands/extract-evidence.md] [src: .claude/commands/t4-synthesise.md]. Two commands are not wrappers. The retrospective command carries its own steps and has no matching skill [src: .claude/commands/sweep-retro.md]. The T3/T6 command duplicates its skill's text but omits the skill's reference to the direction addendum [src: .claude/commands/t3t6-synthesise.md] [src: .agents/skills/source-command-t3t6-synthesise/SKILL.md]; follow the skill.

**Version disagreements to know about.** The T3/T6 synthesis skill names an engine contract that exists only in the v1.6.0 archive and asks for evidence at "ruleset v1.6.0", while the active extraction ruleset is v1.10.1 [src: .agents/skills/source-command-t3t6-synthesise/SKILL.md] [src: methodology/RULESET_VERSIONS.md §Ruleset versions]. The version log itself records that v1.6.0 and v1.6.14 each have more than one entry and that one addendum was added while the skill header still showed the previous version, so a historical stamp cannot always reconstruct the exact instructions [src: methodology/RULESET_VERSIONS.md §Historical version collisions]. The evidence repository's catalogue records a similar case: two archived extraction skills with identical contents declare v1.4.1 in their headers although they sit under v1.5.1 and v1.6.0 [src: evidence:rulesets/README.md §Which instructions apply to the terrace example?].

**Reproducing a past run.** Search records and evidence units carry a `ruleset_version` that points to an archive under `.agents/skills/_versions/<version>/` [src: methodology/RULESET_VERSIONS.md §Ruleset versions]. From v1.7.0 the skill, catalogue, contracts, command and search protocol are snapshotted together; before that, use the producing commit and lane report alongside the stamp [src: methodology/RULESET_VERSIONS.md §Historical version collisions]. See [[ch:rulesets-and-learning]].

**Where the instructions are kept now, and where they are going.** The live skills, extraction contracts and slash commands have not moved. They are read from the producer repository, which is read-only; at the retirement revision its agent guide still identifies discovery v1.8.1 and extraction v1.10.1 as the operative entry points, the same versions as in the table above [src: retired:AGENTS.md §Current pipeline maintenance]. The evidence repository hosts the runnable workflows and the handbook, and its ruleset catalogue indexes five archived instruction sets by producer commit and file hash; it does not hold the instructions themselves [src: evidence:rulesets/README.md §Which instructions apply to the terrace example?] [src: evidence:rulesets/catalog.json]. The stated plan is that model-neutral operating procedures move to the evidence repository's handbook, workflows and a `rulesets/current/` directory, that immutable instruction archives move to `rulesets/versions/`, that tool-specific skills and slash commands become thin adapters, and that the method repository owns the conceptual scientific method [src: retired:methodology/migration/2026-11-05/migration-map.csv]. Neither ruleset directory exists at the operating revision. Until they do, read the instructions in the producer at the revision you record, and stamp every new record with the version actually used.

**Using a different agent.** `AGENTS.md` describes itself as the canonical agent guide under the cross-tool `AGENTS.md` convention, read directly by coding agents; `CLAUDE.md` only imports it [src: AGENTS.md] [src: CLAUDE.md]. The skills are plain Markdown files that name the further files to read; none gives agent-specific loading steps. The evidence repository supplies model-neutral task briefs for each stage (framing queries, screening, extraction and an independent challenge of each staged claim) that a researcher can perform directly or give to an assistant [src: evidence:handbook/assisted-evidence-run.md §1. Frame and capture the search] [src: evidence:handbook/assisted-evidence-run.md §4. Extract and challenge each claim].

## The operating loop

The loop has 17 steps. The first table and the subsections after it quote the producer's commands at the scientific edition (revision `e5c8da02`). They still read and run on private copies, which is how a rule or a trial synthesis is reproduced, but the producer no longer accepts the records they wrote. The second table gives, for every step, the route that records it now.

1. Frame the scope and reconcile existing records.
2. Discover sources in four processes and stage candidates.
3. Screen candidates and record dispositions.
4. Register the round centrally.
5. Verify citation metadata.
6. Recover open-access copies; acquire and file the source.
7. Hydrate the local corpus.
8. Extract to staging.
9. Validate centrally; ingest what passes; auto-quarantine flagged units.
10. Review findings.
11. Apply and submit decisions.
12. Synthesise suitability rules.
13. Synthesise hazard and scorecard rows.
14. Write row prose.
15. Review generated rows.
16. Confirm the ledger and search register.
17. Run the retrospective; change the ruleset if needed.

| Step | Entry point (verbatim) | What the agent may write | Automated checks that gate it | Human decision |
|---|---|---|---|---|
| 1–3 Frame, discover, screen | Discover-sources skill; `scripts/discover-sources.py lens` | `candidates.json`, `report.md`, `protocols.json`, `screening.json` in staging only | Scope and metadata validation, dedupe against sources and queue | Borderline inclusions stay holds for a person [src: .agents/skills/source-command-discover-sources/SKILL.md §Scope and coverage] |
| 4 Register | `scripts/register-discovery.py` | Orchestrator only: queue rows, SRCH rows, ledger stamps, discovery log copy | Family IDs validated against FAM; `ledger.check` | None stated beyond scope |
| 5 Verify metadata | `verify_metadata.py` subcommands `verify`, `verify-titles`, `check` | Queue verification stamps | `check` runs in the build and CI | Auto-recovered DOIs are candidates for a person to verify [src: AGENTS.md §What is locked] |
| 6 Acquire | `scripts/acquire-queue.py`; `scripts/intake-downloads.py` | Corpus and library copies, queue status | Opening-title identity check | A person downloads paywalled or blocked sources and checks ResearchGate copies |
| 7 Hydrate | `scripts/hydrate-corpus.py --queue --nbs <nbs_id>` | Local corpus only | Missing-file report | None |
| 8 Extract | Extract-evidence skill; `python -m nbs_ruralscan.ingest.build <pdf_dir>` | Staging only | `validate_units` (advisory self-check) | None |
| 9 Validate and ingest | `scripts/ingest-effects-staging.py ... --dry-run`, then without `--dry-run` | Orchestrator only: EV rows | Verbatim page check, numbers, context, bands, identity, VONT, family; auto-quarantine | None; quarantine is reversible |
| 10–11 Review and apply | Review server; review page exports | None (people decide) | Provenance guardrail on apply; CI on the submission | Keep, drop with reason, reclassify, query |
| 12 Suitability synthesis | Agent-led proposal; production adapter pending | Traceable proposal and accepted mapping | Schema, provenance and representation validation | Applicability, functions, masks and weights |
| 14 Prose | `scripts/write-prose.py` | Staging bundle; prose sidecar via `merge` | `check_account` refuses on any flag | Writer flags uncertain phrasing for a person |
| 15 Row review | `scripts/build-row-review-batch.py`; `scripts/apply-row-review-export.py` | Review log only | None | Approve, hold or reject each row |
| 16 Ledger and search register | `ledger` and `search_log` modules | Stamps for completed work only | `ledger.check` fails the build | None |
| 17 Retrospective | `/sweep-retro` command | Metrics, catalogue, checks, snapshot | Trend of flag rates | Ruleset change through review |

Table sources: the skills and scripts named in each row, cited in the subsections below, and [src: AGENTS.md §What is locked] [src: src/nbs_ruralscan/recipe/prose.py].

**Where each step is recorded now.** Every command in this table is run from a checkout of the evidence repository. "Operator command" means `workflows/submissions/register_operation.py`, which previews by default and opens a protected pull request when `--open-pr` is placed before the subcommand.

| Step | Route now | What becomes official, and where | Status |
|---|---|---|---|
| 1–3 Frame, discover, screen | `workflows/discovery/capture.py`, then `screen.py worksheet` and `screen.py stage`, in a private run directory | Nothing yet; the bundle is private until registered | Working |
| 4 Register the round | Operator command, `discovery` subcommand | Search record, new acquisition-queue rows, discovery report, explicit reuse of existing sources | Working |
| 5 Verify metadata | `workflows/acquisition/run.py verify`; checks replayed when the source is registered | Verification result in the acquisition receipt and the queue record | Working |
| 6 Acquire and file | `run.py acquire` and `check`; approved PDF copied to the team library | Private bundle and receipt; the shared library copy | Working |
| 6b Register the source | Operator command, `source` subcommand | Source-register row with `extraction_status=pending`; queue record marked acquired | Working (new step) |
| 7 Hydrate | No separate step: the source and apply commands read the synchronised library and a local corpus | Nothing | Not needed as a recorded step |
| 8 Extract | `workflows/extraction/extract.py` to private staging | Nothing yet | Working |
| 9 Validate and ingest | `workflows/submissions/intake.py extraction`, then a maintainer's approval label and `registers.py --open-pr` | Evidence-register rows; a receipt in the applied journal | Working |
| 10–11 Review and apply | Submit review in the live dashboard, or the local desk, or a vote CSV; applied with `registers.py --open-pr` | Finding review log and evidence-register review fields | Working |
| 12–13 Synthesise | Automatic: applying any finding, source or row change recompiles all four table families with the pinned compiler | Compiled rows in `publication/review-queue.json`; hashes in `publication/recipe-candidate.json` | Working for recompilation and for released definitions and rule tables; accepted suitability functions and weights are still held |
| 14 Row wording | Local row desk, Suggest clearer wording, or `recipe_rows.py wording`; applied with the operator command, `row` subcommand | `recipe-inputs/wording.jsonl` | Working |
| 15 Row review | Local row desk, Review this rating, or `recipe_rows.py rating`; applied with the `row` subcommand | Rating review log and `row-reviews/receipts.jsonl` | Working |
| 16 Progress stamps | `--stamp` on the discovery operation; the `verification` subcommand | Progress ledger | Working |
| 17 Retrospective | Keep measurements and proposed adjustments in the private run record | Nothing official yet | Planned |

[src: evidence:workflows/discovery/README.md §Run a new search] [src: evidence:workflows/acquisition/README.md §Acquire another candidate] [src: evidence:workflows/extraction/README.md §Extract a different claim] [src: evidence:workflows/submissions/registration.md §Register discovery, sources and progress] [src: evidence:workflows/submissions/recipe-rows.md §Operator: preview, open protected PR, verify] [src: evidence:workflows/submissions/README.md §Which records can I update?]

### Frame, discover and screen

The discovery skill requires practice, family, table and purpose before searching, and reconciliation with existing records [src: .agents/skills/source-command-discover-sources/SKILL.md §Scope and coverage]. When delegation is authorised, literature, grey and tool lanes run as separate agents writing only to staging [src: .agents/skills/source-command-discover-sources/SKILL.md §Agent contract]. A Lens.org query is staged with:

```sh
python3 scripts/discover-sources.py lens "<query>" --out pipeline/staging/discovery/<name>.json \
    [--size 50] [--year-from 2015] [--process updated_lit] [--tables "T3|T6"] [--reviews]
```

[src: scripts/discover-sources.py]. AGRIS is a manual browser lane; its command writes a template, not results [src: .agents/skills/source-command-discover-sources/SKILL.md §Search and screen]. The screening funnel and credibility rubric are in [[ch:discovery]].

*Now.* The evidence repository's capture tool saves one file per executed query, and its screening tool turns a closed plan and a completed worksheet into the same four staging files [src: evidence:workflows/discovery/README.md §Capture records] [src: evidence:workflows/discovery/README.md §Stage and inspect]. A worked run follows the loop.

### Register, verify and acquire

The registrar turns lane outputs into pending acquisition queue rows, search-register rows with verbatim queries and counts, ledger stamps and a tracked copy of each report; targeted searches require explicit per-lane protocols passed as `--family <id> --searched-by <identity> --protocols <lane=file.json>` [src: scripts/register-discovery.py] [src: methodology/search_protocol.md §What every search logs]. Metadata verification then round-trips each DOI through Crossref and rebuilds the citation; a DOI-less source needs its title found on the opening pages of the cached file; the offline `check` runs in the build [src: src/nbs_ruralscan/schema_tools/verify_metadata.py]. Before any source is labelled paywalled, the open-access recovery protocol must be exhausted [src: methodology/search_protocol.md §OA-recovery]. Files that a person downloaded are filed with an identity check by `scripts/intake-downloads.py` [src: scripts/intake-downloads.py]. Scanned PDFs are OCR'd once:

```sh
uv run python scripts/ocr-scan.py <source_id> [--force]
```

[src: methodology/search_protocol.md §Scanned PDFs (no text layer)]. Rules are in [[ch:acquisition]].

*Now.* The producer's registrar refuses to write. Its successor is the operator command's `discovery` subcommand, which replays the closed plan and decisions and proposes the search record, the queue rows, the report and the progress stamp in one pull request [src: evidence:workflows/submissions/registration.md §Record a discovery run]. Verification and acquisition use the evidence repository's acquisition tool, which performs the same DOI round trip and opening-title check and writes a private receipt [src: evidence:workflows/acquisition/README.md §Bibliographic identity and access].

### Hydrate

Sources being swept have no source-register row yet, so hydration for a sweep reads the queue:

```sh
python3 scripts/hydrate-corpus.py --queue --nbs <nbs_id>
```

[src: PLAYBOOK.md §Acquisition queue]. At the scientific edition the source-register row was created at the central merge, after extraction [src: docs/HYDRATION.md §The order of operations (pre-SRC sources)]. Pending rows did not block a sweep; the register is append-only and later arrivals are extracted on top [src: docs/HYDRATION.md §Hydrating for a sweep].

*Now.* The order is reversed: a source is registered before its first extraction. A verified, queued source enters the source register with `extraction_status=pending`, with no finding and no extraction proposal needed. Extraction proposals are accepted only for sources already in the register [src: evidence:workflows/submissions/registration.md §Register an acquired source] [src: evidence:workflows/submissions/README.md §Which records can I update?]. A source that arrives unsolicited is first screened and queued through a discovery run, then registered.

### Extract and validate

The extraction skill requires the agent to build a deterministic index, retrieve page-stamped passages and inspect tables and continuations rather than only search hits [src: .agents/skills/source-command-extract-evidence/SKILL.md §Source and coverage checks]:

```sh
python -m nbs_ruralscan.ingest.build <pdf_dir>
```

Units are validated with `validate_units` and saved to staging only. The orchestrator then runs the staging ingest as a dry run, with explicit `--allow-structural` or `--allow-operational` flags when those roles are authorised, and repeats without `--dry-run` only after all gates pass [src: .agents/skills/source-command-extract-evidence/SKILL.md §Extract and validate]:

```sh
python3 scripts/ingest-effects-staging.py pipeline/staging/riparian_effects_A.json ... --run-id <id> [--dry-run]
```

[src: scripts/ingest-effects-staging.py]. The ingest is "the ONE place extraction output becomes evidence" and re-runs the verbatim, number, context, band, identity, variable and family checks, refusing on any failure [src: scripts/ingest-effects-staging.py]. On the write path of the build, an auto-quarantine step soft-drops units flagged by scope and practice checks, never touching a unit a person has decided [src: src/nbs_ruralscan/schema_tools/quarantine.py]. Then regenerate JSON from the CSVs:

```sh
python3 src/nbs_ruralscan/schema_tools/generate.py schema
```

[src: AGENTS.md §Run / preview / deploy]. What each check catches is in [[ch:extraction]].

*Now.* Extraction is staged privately with the evidence repository's page-anchored PDF tool, and the producer's content checks are run on a disposable copy before hand-over [src: evidence:workflows/extraction/README.md §Extract a different claim] [src: evidence:handbook/assisted-evidence-run.md §4. Extract and challenge each claim]. The staged file is then submitted as an extraction proposal, a public issue; it becomes evidence only after a maintainer has reviewed it and a protected pull request has applied it [src: evidence:workflows/submissions/README.md §Apply approved submissions]. The producer's staging ingest refuses to write.

### Review and apply

Start the review server, open the dashboard and work the queues; one action applies decisions and submits them [src: docs/REVIEWER_GUIDE.md §Each review session]:

```sh
uv run python3 -m nbs_ruralscan.schema_tools.review_server
```

The headless equivalent is:

```sh
uv run python -m nbs_ruralscan.schema_tools.submit_review --ship <your-handle> --auto
```

[src: docs/REVIEWER_GUIDE.md §Each review session]. A compatibility wrapper, `scripts/submit-review.sh`, calls the same module [src: scripts/submit-review.sh]. Focused batches for the one-unit review page are built with `scripts/build-review-batch.py`, which reads the register and cached PDF and never edits evidence; their CSV exports are applied with `scripts/apply-review-export.py` through the same apply function, register and soft-delete rules as the dashboard [src: scripts/build-review-batch.py] [src: scripts/apply-review-export.py]. Consensus, reason codes and re-opening are in [[ch:review-and-quality]].

*Now.* None of these producer commands records a decision any more. A reviewer chooses Submit review on a finding in the live dashboard, or uses the local desk or a vote CSV; each creates a public issue under the reviewer's own account, and a maintainer applies eligible, agreeing votes through a protected pull request [src: evidence:workflows/submissions/README.md §Submit evidence and recipe reviews] [src: evidence:workflows/submissions/README.md §Apply approved submissions]. The commands are under "Recording work now".

The producer guides disagree on one point: the playbook and the onboarding guide say the Windows submission uses Git Bash, the reviewer guide says Bash is not required [src: PLAYBOOK.md §Review flagged evidence (QA/QC → main)] [src: ONBOARDING.md §4] [src: docs/REVIEWER_GUIDE.md §Each review session]. The wrapper's own comment supports the reviewer guide [src: scripts/submit-review.sh].

### Synthesise

T4 synthesis starts from reviewed evidence and the last accepted decision. The agent
proposes the mapping and documents candidate use, scope, alternatives and uncertainty;
scientific review accepts or holds that proposal. Deterministic checks validate and
package the accepted representation. See [[ch:suitability-synthesis]].

The historical T4 compiler is retired. Do not use its former CLI or archived skill
commands. Until the production proposal/acceptance adapter exists, publication keeps
explicitly historical T4 baseline rows; new evidence does not regenerate them.

Effect synthesis runs the gates on pooled units first, then the engine:

```sh
python3 src/nbs_ruralscan/schema_tools/generate.py schema  # regenerate JSON
python3 -m nbs_ruralscan.schema_tools.check_account schema/recipes/<nbs_id>/T6_nbs_scorecard.json
```

[src: .agents/skills/source-command-t3t6-synthesise/SKILL.md]. Class, levels and confidence are engine outputs; a disagreement is fixed at the evidence unit and the engine re-run [src: .agents/skills/source-command-t3t6-synthesise/SKILL.md]. See [[ch:suitability-synthesis]] and [[ch:effect-synthesis]].

*Now.* Nobody runs the engines by hand to publish. The evidence repository pins the producer's compiler at revision `e43c42bd` and reruns it on the current registers whenever a finding, source or row change is applied, for all four table families. The result is a candidate: `publication/recipe-candidate.json` records the compiler revision, the SHA-256 of every input file and one output hash per practice and table [src: evidence:publication/recipe-candidate.json] [src: evidence:workflows/submissions/recipe-rows.md §Candidate and method acceptance]. A candidate is not a method edition. Accepting one is a separate pull request in the method repository that names the evidence revision, the manifest and its hash, the practices and tables adopted, the previous edition and the changed rows. The trial commands above remain the way to study what a change would do before proposing it. A change to a rule table or a definition is not made in the recipe: it is decided and released in the method repository and then adopted by the evidence repository, as described under "Recording work now".

### Prose and row review

Row prose stays empty until the gated prose writer runs [src: .agents/skills/source-command-t3t6-synthesise/SKILL.md]. The writer may draw only on a bundle of the rows' used units:

```sh
python3 scripts/write-prose.py bundle <nbs_id>            # rows needing prose + their used units
python3 scripts/write-prose.py check  <nbs_id> <prose.json>   # validate, write nothing
```

A third subcommand, `merge`, runs the account check, refuses on any flag, and records the prose in a sidecar keyed to the rows' current evidence IDs [src: scripts/write-prose.py]. Generated rows are then reviewed in row batches; a row decision is a review record appended to a log, and changes nothing in the registers or recipes. Holds and rejects become the orchestrator's list of evidence, routing or prose to fix before regenerating [src: scripts/build-row-review-batch.py] [src: scripts/apply-row-review-export.py].

*Now.* Both have a route through the local row desk, described under "Recording work now". Wording is proposed per row and recorded as an authored input, separate from the compiled output; generated rows are never edited by hand. If a row's evidence, a locator or its analytical result later changes, the compiler withholds the old wording, shows the compiled text and lists the row as stale [src: evidence:workflows/submissions/recipe-rows.md §Operator: preview, open protected PR, verify].

### Ledger, search register and retrospective

Search, screening and verification stages are stamped by the step that did them, through the ledger module's `mark` command; extraction and review are derived from the register. The ledger check runs in the build [src: src/nbs_ruralscan/schema_tools/ledger.py]:

```sh
uv run python3 -m nbs_ruralscan.schema_tools.ledger check
```

A search not passed through the registrar is logged with the search-log module's `log` command, which takes the practice, table, category, family, verbatim terms, limits, ruleset version and run ID [src: src/nbs_ruralscan/schema_tools/search_log.py]. After every sweep the retrospective measures, gates, triages and encodes learnings [src: methodology/extraction_retrospective.md §The loop]:

```sh
uv run python3 src/nbs_ruralscan/schema_tools/sweep_metrics.py --label <sweep>
```

The learnings cursor (`learnings status`, `learnings record`) proves which review decisions have been turned into adjustments [src: src/nbs_ruralscan/schema_tools/learnings.py]; `record` is used only after the complete current feedback set has been read [src: .claude/commands/sweep-retro.md §Feedback accounting (v1.7.0)].

*Now.* Search records and progress stamps are written by the operator command: `--stamp` on a discovery run records searched and screened status for its exact practice, family, table and process, and the `verification` subcommand records technical verification from applied extraction receipts. Extracted and reviewed counts are derived from the evidence register and the finding reviews, as before [src: evidence:workflows/submissions/registration.md §Record verification progress]. The sweep metrics and the learnings cursor were migrated as records, but appending to them is a planned route; until it exists, keep the measurements and proposed adjustments in the run record.

## A bench-terrace discovery run, step by step

This walk-through follows one bounded question through the current route: which sources give annual rainfall guidance for bench terraces? The scope is the practice `water_harvesting_conservation`, the family `water_harvesting__terracing` and the suitability table (T4). It uses the evidence repository's teaching example, which is a fixed selection of three known citations and adds no search coverage [src: evidence:workflows/discovery/README.md §Replay the terrace screening example]. At the operating revision no operation had yet been recorded on the main line through the three registration routes; they are exercised by the repository's acceptance tests on fixtures. Read this as how a run goes, not as a record of one.

Set up once per operation, from the evidence checkout [src: evidence:workflows/submissions/registration.md §Register discovery, sources and progress]:

```sh
git fetch origin main
base=$(git rev-parse origin/main)
ciat=/path/to/nbs_ruralscan
writer=workflows/submissions/register_operation.py
```

Keep the full `base` you inspected. If the main line advances, inspect the intervening changes before preparing another proposal.

### Frame, capture and screen

Write one plan for the scope and one discovery process (stock, updated literature, grey literature or tools), with a unique run ID, inclusion criteria, actual limits and a stopping rule. Then run each authorised query and keep what came back [src: evidence:workflows/discovery/README.md §Capture records]:

```sh
python3 "$workflow/capture.py" openalex 'bench terraces rainfall' \
  --limit 20 --out "$run_dir/openalex.json"
```

Close the plan with the real date, searcher, screener, stop reason and omissions, generate the worksheet, enter a disposition and a reason for every inspected record, and stage [src: evidence:workflows/discovery/README.md §Record screening decisions] [src: evidence:workflows/discovery/README.md §Stage and inspect]:

```sh
python3 "$workflow/screen.py" worksheet "$run_dir/plan.json" \
  --out "$run_dir/decisions.json"
python3 "$workflow/screen.py" stage "$run_dir/plan.json" "$run_dir/decisions.json" \
  --out "$run_dir/staged"
```

An agent may propose queries and draft dispositions. A query is only "proposed" until there is a saved result from running it, and weak exclusions, disputed identities, holds and proposed tiers are inspected by a person before staging [src: evidence:handbook/assisted-evidence-run.md §1. Frame and capture the search] [src: evidence:handbook/assisted-evidence-run.md §2. Screen the frozen records].

### Case 1: the search returns nothing

A successful request that returns no records is an observed zero. It is staged like any other capture and yields a search protocol with zero counts. A failed request is different: it produces an error, and the unavailable channel is recorded in the plan's omissions or retried under a new filename [src: evidence:workflows/discovery/README.md §Capture records] [src: evidence:workflows/discovery/README.md §Stage and inspect].

Register the run all the same:

```sh
python "$writer" --ciat-repo "$ciat" --base "$base" discovery \
  --plan "$run/plan.json" --decisions "$run/decisions.json" --stamp
```

A completed search with zero results gets a search record, and with `--stamp` the same pull request records searched and screened progress for that exact practice, family, table and process [src: evidence:workflows/submissions/registration.md §Record a discovery run]. This is the point of the route. Whether a family has been searched is answered from the search register and the progress ledger, never inferred from whether evidence happens to exist. To try different terms, capture the new query under a new run ID; the earlier zero stays on record.

### Case 2: the source is already registered

In the teaching selection the WOCAT water-harvesting guidelines already have a source ID, so the record is given the disposition `reuse` with that ID and a reason this scope needs the source. The other two records are an exclusion (the passage concerns stone lines) and a hold (its rainfall classes are seasonal, not annual). The staged report reads three records retrieved, three screened, one included [src: evidence:workflows/discovery/README.md §Replay the terrace screening example].

The discovery pull request then carries the search record, the report and the explicit reuse ID, and adds no acquisition-queue row for that source; counts are stated before queue deduplication [src: evidence:workflows/submissions/registration.md §Record a discovery run] [src: evidence:workflows/discovery/README.md §Validate the handoff on a historical copy]. A known matching source keeps its canonical ID [src: evidence:workflows/submissions/registration.md §Register an acquired source]. Because the source is already in the register, findings from it can go straight to the submission desk [src: evidence:workflows/acquisition/README.md §Acquire another candidate]. Check the edition first: for a proposed reuse the acquisition tool reads the source register to confirm the canonical ID, the citation and any shared DOI, and a changed publisher edition goes on hold [src: evidence:workflows/acquisition/README.md §Acquire another candidate] [src: evidence:workflows/acquisition/README.md §Worked example · WOCAT terrace manual].

### Case 3: a new source must be registered before extraction

A record screened `include` that matches no existing source becomes a candidate, and the discovery pull request adds it to the acquisition queue. Nothing can be extracted from it yet.

**Verify and acquire.** Run `verify`, `acquire` and `check` with the candidate ID and an acquisition plan. For a DOI source the tool round-trips the DOI through Crossref and checks the title; for a DOI-less manual it checks the publisher route and the title in the file's opening pages. The result is a private bundle with a receipt, or a receipt explaining the hold [src: evidence:workflows/acquisition/README.md §Acquire another candidate] [src: evidence:workflows/acquisition/README.md §Bibliographic identity and access].

**File the shared copy.** For a PDF, store the approved copy in the team's source library and note its shared locator [src: evidence:workflows/acquisition/README.md §Acquire another candidate].

**Register the source.** Supply the screened candidate, the acquisition plan, the verified bundle, a credibility assessment and, for a PDF, the local synchronised library root and the project-relative library path [src: evidence:workflows/submissions/registration.md §Register an acquired source]:

```sh
python "$writer" --ciat-repo "$ciat" --base "$base" source \
  --candidates "$run/screened/candidates.json" --plan "$run/acquire.json" \
  --bundle "$run/acquired" --assessment "$run/assessment.json" \
  --library-root "$synced_library" --library-path "$team_library_path"
```

**Merge, then extract.** After the pull request is merged, pin the new revision of the evidence repository and submit the first extraction proposal against it. Each extraction must still pass its lane and locator checks [src: evidence:workflows/submissions/registration.md §Register an acquired source].

**Who checks what.** The file itself is checked in two places and by two different parties, because it cannot be made public.

| Check | Who or what performs it | Where |
|---|---|---|
| The acquired file is the cited work (signature, opening title, hashes) | The acquisition tool, run by the operator | The operator's machine; recorded in the private receipt |
| The copy in the team library has the same bytes as the receipt | The operator command, before it prepares the pull request | The operator's machine, against the synchronised library |
| The queued identity, the DOI or title result, the source assessment, the edition hash and the shared locator are right | A person reviewing the pull request | The pull request |
| The public bibliographic and provenance checks reproduce, and the register change reproduces from the recorded operation against the pull request's base | Continuous integration | The evidence repository's required check |

[src: evidence:workflows/submissions/registration.md §Register an acquired source] [src: evidence:.github/workflows/evidence-checks.yml]. Continuous integration never sees the restricted file. It can confirm that the public record is consistent and reproducible; only the operator's check and the shared library tie that record to the document. The operation's public record carries the bibliographic and provenance results; the document itself stays with the run and in the team library.

### Finding the record afterwards

Each operation is recorded under `operations/` in the same commit as its register changes, and a plain edit to a register file cannot stand in for it [src: evidence:workflows/submissions/registration.md §Record verification progress]. A reviewer therefore starts from the merged pull request and finds:

- the search, by run ID, in the search register, with its report under the discovery logs;
- a new candidate in the acquisition queue, and after registration in the source register with `extraction_status=pending`;
- after the first extraction is applied, the proposal's issue number in the applied journal and the finding in the live review queue at the new revision [src: evidence:handbook/review-records.md §Find the right review record].

### Technical verification is not human sign-off

The last stamp in the walk-through is verification [src: evidence:workflows/submissions/registration.md §Record verification progress]:

```sh
python "$writer" --ciat-repo "$ciat" --base "$base" verification \
  --practice "$practice" --family "$family" --table "$table" --process "$process" \
  --run-id "$verification_run" --date "$step_date" --operator "$operator" \
  --status in_progress --receipts "$extraction_receipt"
```

The writer checks the named extraction receipts against the applied journal, the cited source edition and the current findings in that scope; search and screening must already be recorded as complete there. `done` is allowed only when the receipts cover every active finding in the scope. What this stamp records is technical: the findings exist, came through the applied route and match their sources' editions. It says nothing about whether a person agrees with any finding. Human decisions on findings go through the review queue, and the reviewed count is derived from those decisions, never stamped. Merging a registration pull request records the operation. It is not a scientific judgement on the source or on any finding drawn from it.

## Rules the agent must never break

Each rule is explained in full in the linked chapter.

1. **No hand-authored evidence.** No quote, page or unit may come from memory, an abstract, a snippet or model knowledge; the provenance guardrail fails the build otherwise [src: AGENTS.md §Don't] [src: src/nbs_ruralscan/schema_tools/validate_sources.py]. See [[ch:extraction]].
2. **Quotes are sliced from the page text, not retyped.** Text that is not contiguous in the text layer is a blocker, never stitched [src: AGENTS.md §Don't]. See [[ch:extraction]].
3. **Sub-agents write only to staging and never run version-control commands.** Their self-checks are advisory; the central gates are what count [src: AGENTS.md §Don't].
4. **No unverified DOI reaches evidence.** Extraction refuses a source without a verified DOI, or without a verified title when there is no DOI [src: AGENTS.md §What is locked] [src: src/nbs_ruralscan/schema_tools/verify_metadata.py]. See [[ch:acquisition]].
5. **No source is called paywalled before open-access recovery is exhausted** [src: methodology/search_protocol.md §OA-recovery]. See [[ch:acquisition]].
6. **The practice must be named in the source.** A demo dataset, file title or the sweep's focus is not evidence of association [src: AGENTS.md §Don't]. See [[ch:extraction]].
7. **Direction is on the variable as named,** with a verbatim cue [src: AGENTS.md §Don't] [src: .agents/skills/extraction_contracts/DIRECTION_ADDENDUM.md]. See [[ch:extraction]].
8. **Every number in a relationship must appear in its quote** [src: AGENTS.md §Don't]. See [[ch:extraction]].
9. **Approval of a finding does not approve a numerical calibration.** Unresolved bands stay out of executable recipes; values are never silently widened, rounded or scored [src: AGENTS.md §Don't] [src: .agents/skills/extraction_contracts/T4_review_contract.md]. See [[ch:review-and-quality]].
10. **Soft enabling-environment evidence is never extracted as structural suitability** [src: AGENTS.md §What is locked]. See [[ch:extraction]].
11. **Soft deletion only.** A drop sets a review state and the row remains restorable; hard deletion is forbidden [src: AGENTS.md §What is locked]. See [[ch:review-and-quality]].
12. **Never edit generated JSON by hand;** edit the CSV and regenerate [src: AGENTS.md §Architecture].
13. **No progress claim without a record.** Mark only work actually completed [src: AGENTS.md §What is locked] [src: .agents/skills/source-command-discover-sources/SKILL.md §Central closeout].
14. **No new sweep without authorised scope.** The extraction skill forbids expanding into a new search or full corpus sweep without task scope, and the T4 synthesis skill states that synthesis does not authorise a new sweep [src: .agents/skills/source-command-extract-evidence/SKILL.md §Establish scope] [src: .agents/skills/source-command-t4-synthesise/SKILL.md §Reproducible workflow].

## Human approval points

| Decision | What the human looks at | What is recorded and where |
|---|---|---|
| Authorise scope and delegation | Practice, family, table, roles, limits, whether lanes may be delegated | Scope in the lane briefs and search plan; no dedicated approval record found [src: .agents/skills/source-command-discover-sources/SKILL.md §Agent contract] |
| Borderline screening | Holds and weak exclusions | Disposition in the screening file and report [src: .agents/skills/source-command-discover-sources/SKILL.md §Scope and coverage] |
| Candidate DOI from title search | Resolved record against the citation | Verification stamp in the acquisition queue [src: AGENTS.md §What is locked] |
| Manual acquisition | Publisher or repository copy; ResearchGate checks that tools cannot make | Queue status and note; file in the team library [src: methodology/search_protocol.md §OA-recovery] [src: PLAYBOOK.md §Acquisition queue] |
| OCR quality | Sampled quotes against the page image | Review batch decision before any OCR unit is approved [src: methodology/search_protocol.md §Scanned PDFs (no text layer)] |
| Keep, drop, reclassify or query a finding | Quote beside the source passage, role, family, units | Evidence register review fields and the review log; drops need a coded reason [src: AGENTS.md §What is locked]. Now submitted as a public issue under the reviewer's account and applied in the evidence repository |
| Approve a proposed extraction | The cited source and the exact proposed changes | The `approved-extraction` label on the original issue, applied by a maintainer before a protected pull request can apply it [src: evidence:workflows/submissions/README.md §Apply approved submissions] |
| Register a source | Queued identity, DOI or title result, assessment, edition hash, shared locator | Approval of the registration pull request [src: evidence:workflows/submissions/registration.md §Register an acquired source] |
| Numeric plausibility | Band width, precision, jumps, proxies, transfer | Hold or approval kept separate from qualitative keep [src: .agents/skills/extraction_contracts/T4_review_contract.md] |
| Suitability rule change | Differences against the accepted recipe; applicability, functions, tails, masks, weights | Batch audit synthesis decision record [src: .agents/skills/source-command-t4-synthesise/SKILL.md §Translating evidence into a rule] |
| Generated row review | Class, confidence, prose, the evidence it rests on | Row review log [src: scripts/apply-row-review-export.py]. Now approve, hold or reject through the row desk; a hold needs a reason and a reject a coded reason [src: evidence:workflows/submissions/recipe-rows.md §Reviewer: browser or CLI] |
| Row wording | The proposed mechanism and conditions, or the suitability explanation, against the row's evidence | `recipe-inputs/wording.jsonl`, through a protected pull request [src: evidence:workflows/submissions/recipe-rows.md §Operator: preview, open protected PR, verify] |
| Accept a candidate as a method edition | Row differences and stale wording against the previous edition | A separate pull request in the method repository naming the evidence revision and manifest hash [src: evidence:workflows/submissions/recipe-rows.md §Candidate and method acceptance] |
| Merge to the main line | The submission's changed files and CI result | At the pinned revision the main line required passing checks and one approval, and an automated workflow approved submissions that changed only review records [src: AGENTS.md §What is locked] [src: .github/workflows/auto-merge-review.yml]. That workflow has since been removed from the producer repository. Now every official change is a protected pull request in the evidence repository that needs approval and current checks [src: evidence:workflows/submissions/README.md §Apply approved submissions] |
| Ruleset change | Retrospective triage | Version log row and archived snapshot [src: methodology/RULESET_VERSIONS.md §Ruleset versions] |
| Method decision | The exact wording of the ruling, its scope and its source | A coded event in the method repository's decision register, accepted by review and merge of a method pull request [src: method:decisions/README.md §Propose, decide or implement a change] |
| Definition or rule-table change | Before and after values, and whether the cited decision covers the edit | A method release approved table by table against a decision code, then a separate adoption pull request in the evidence repository [src: method:configuration/README.md §Release compiler configuration] |

No pinned file states a separate explicit "start" approval for large sweeps beyond the authorised-scope rule above.

**What each human act authorises.** Agents stage evidence and propose wording; they sign off nothing. Five human acts have distinct meanings and are recorded separately, and none implies another:

- **A submission receipt** shows that a vote or proposal was made, by whom and when. It is not yet a recorded decision.
- **An applied finding decision** is a reviewer's keep, hold or drop on one claim from one source. Votes from the dashboard and from CSV files enter the same consensus check; opposing votes stay pending [src: evidence:workflows/submissions/README.md §Apply approved submissions].
- **An approved extraction** means a maintainer checked the proposed finding against its source. The finding then enters the register and is still open for finding review.
- **A rating review** is a judgement on a compiled row as presented. It approves no finding, changes no threshold and accepts no method edition; a reject does not remove the row [src: evidence:workflows/submissions/recipe-rows.md §Review a rating or change row wording] [src: evidence:workflows/submissions/recipe-rows.md §Reviewer: browser or CLI].
- **A method decision** changes a rule. It is recorded under its own code through a pull request in the method repository; the review and merge identify who accepted it. A decision on its own leaves implementation pending, until a separate event names the code or definitions that put it into effect [src: method:decisions/README.md §Record a scientific method decision].

Passing the automated checks, a merged registration and a verification stamp are technical states. They show that a record is well formed, reproducible and applied through the right route. None of them is a human sign-off on the science.

## Recording which instructions and models were used

**Instruction versions.** `SRCH.ruleset_version` is required on every search row and `EV.ruleset_version` is carried on evidence units; both point to the version log and its archive [src: methodology/search_protocol.md §What every search logs] [src: methodology/RULESET_VERSIONS.md §Ruleset versions]. Historical units are never restamped [src: .agents/skills/source-command-extract-evidence/SKILL.md §Evidence extraction].

**Run and actor fields.** Search rows may carry `run_id` and `searched_by` [src: methodology/search_protocol.md §What every search logs]. Source rows may carry `extraction_run_id` and `extractor`, defined as free text for "who/what did the extraction" [src: schema/spec.md]. Prose sidecar entries record a `written` date and a `writer` label [src: src/nbs_ruralscan/recipe/prose.py]. These are free text. The pinned registers have no structured field for model identifier, version, settings or prompt.

**The evidence repository's catalogue.** Each catalogue entry names a producer commit, the archive entry point, the declared version and the SHA-256 of every file in that archive; a check script verifies the archives offline against a producer clone [src: evidence:rulesets/catalog.json] [src: evidence:rulesets/README.md §Verify against a local clone]:

```sh
python3 -IB rulesets/check.py --ciat-repo /path/to/nbs_ruralscan
```

A byte match proves which instructions were archived, not the conversation or settings of an original run [src: evidence:rulesets/README.md §Which instructions apply to the terrace example?].

**Run records.** The evidence repository asks each assisted stage to retain the provider, exact model identifier as exposed, settings, actual prompt and its digest, marking an unavailable identifier as unknown [src: evidence:handbook/assisted-evidence-run.md §Record and hand over the run]. The run-record tool hashes the retained files into a private record with `provider`, `model` and `prompt` fields for AI-assisted stages; `manual` and `replay` stages omit them [src: evidence:workflows/run_record/README.md §Describe the stages]:

```sh
python3 -IB workflows/run_record/record.py create --run-dir "$work" --description "$work/description.json"
python3 -IB workflows/run_record/record.py verify --run-dir "$work" --sha256 "$digest"
```

Run records are private and are not part of the registers. For a real proposal the record also keeps the issue receipt from the submission desk and, once applied, the register pull request and the merged revision [src: evidence:workflows/run_record/README.md §Create and verify]. The method dashboard states that some original prompts and model settings for historical work are unavailable and that the gap should stay explicit [src: method:dashboard/ai.html §What the audit can establish].

## Recording work now

This section describes the evidence repository at revision `8c6f793f`. It is later than the scientific edition, and it is the authority for how new work is recorded. The producer repository is read-only for these records.

### The baseline and the rule for every route

The evidence repository holds a `registers/` copy taken from producer revision `e43c42bd`. The producer was the writer when that copy was taken; the evidence repository is the writer now. A manifest lists each file's source path, SHA-256, size and record count, and the public copy of the method-decision ledger omits the task-assignment column [src: evidence:registers/manifest.json] [src: evidence:workflows/evidence_snapshot/README.md §Register migration seed].

Every route has the same four stages. A proposal is prepared and previewed; it is opened as a protected pull request; continuous integration independently reproduces the change from the recorded operation or the original issue against the pull request's base; and a person approves and merges. The official data revision is the merge into the main line [src: evidence:workflows/submissions/registration.md §Register discovery, sources and progress] [src: evidence:.github/workflows/evidence-checks.yml]. Identical retries add nothing; an edited issue cannot be replayed and must be filed afresh.

### Finding votes and extraction proposals

These two submissions came first and still work. On the live dashboard, Submit review on a finding opens a public issue under the reviewer's own GitHub account; the issue number is the receipt [src: evidence:workflows/submissions/README.md §Submit evidence and recipe reviews]. The local desk does the same for one finding, a vote CSV or a staged extraction file, and binds to 127.0.0.1 on port 8934 [src: evidence:workflows/submissions/README.md §Use the local desk for browser or CSV entry]:

```sh
source_repo=/path/to/nbs_ruralscan
git fetch origin main
pin=$(git rev-parse origin/main)
gh api user --jq .login
python3 workflows/submissions/serve.py --ciat-repo "$source_repo" --revision "$pin"
```

Without a browser [src: evidence:workflows/submissions/README.md §Submit an exported CSV or extraction file]:

```sh
python3 workflows/submissions/intake.py csv votes.csv --lane T4 --revision "$pin"
python3 workflows/submissions/intake.py extraction t4-units.json --lane T4 --revision "$pin"
python3 workflows/submissions/intake.py extraction effects.json --lane T3/T6 --revision "$pin"
```

A maintainer who has reviewed an extraction labels its issue `approved-extraction`. `workflows/submissions/registers.py`, given issue numbers, the producer clone and a local corpus, previews by default and with `--open-pr` opens a protected register pull request. It checks reviewer identity, the original issue body, the matching finding and source, and agreement across eligible ballots; opposing votes stay pending, and a receipt ledger prevents duplicate application [src: evidence:workflows/submissions/README.md §Apply approved submissions]. At the operating revision the applied journal held one receipt, an extraction correction [src: evidence:registers/applied-receipts.json].

### Seven further routes that work

| Route | Command or action | What it records |
|---|---|---|
| 1. Discovery run and acquisition queue | Operator command, `discovery --plan … --decisions …` | The real query, scope, screening decisions and counts in the search register; eligible new candidates in the acquisition queue; the discovery report. A zero-result search still gets a record |
| 2. Progress stamps | `--stamp` on the discovery operation; `verification` with applied extraction receipts | Searched, screened and verified status in the progress ledger, for one exact practice, family, table and process |
| 3. Source registration before extraction | Operator command, `source` | A source-register row with `extraction_status=pending`, with no finding needed |
| 4. Recompilation and row wording | Automatic recompilation on every applied change; Suggest clearer wording on the row desk or `recipe_rows.py wording`; applied with `row` | Compiled rows and the candidate manifest; authored wording in `recipe-inputs/wording.jsonl` |
| 5. Rating reviews | Review this rating on the row desk or `recipe_rows.py rating`; applied with `row` | An approve, hold or reject appended to the rating review log and `row-reviews/receipts.jsonl` |
| 6. Method decisions | In the method repository: `decisions/register.py record`, then a method pull request | A coded propose, park, reopen, decide or implement event in `decisions/events.csv`, and the current state of every code in `decisions/current.csv` |
| 7. Definitions, rule tables, tools and mappings | Method-owned: `configuration/release.py build` and a method pull request, then `configuration.py pin` and an adoption pull request in the evidence repository. Evidence-owned: `configuration.py record` and an evidence pull request | The method release and its file hashes; the evidence repository's method pin; source-backed changes to the tool register, the WOCAT mappings and the per-finding direction exceptions in `configuration/changes.json` |

[src: evidence:workflows/submissions/registration.md §Record a discovery run] [src: evidence:workflows/submissions/registration.md §Record verification progress] [src: evidence:workflows/submissions/registration.md §Register an acquired source] [src: evidence:workflows/submissions/recipe-rows.md §Operator: preview, open protected PR, verify] [src: method:decisions/README.md §Propose, decide or implement a change] [src: method:configuration/README.md §Release compiler configuration] [src: evidence:configuration/README.md §Update compiler configuration]

Routes 1 to 3 are walked through above. Routes 4 and 5 share one desk and one operator subcommand. Routes 6 and 7 are described after them.

**The row desk is available now, on the reviewer's own computer.** Start the local desk as shown above, at the full evidence revision shown on the dashboard, and choose "Review a compiled rating or propose row wording". Select a practice, table and row; read its text, rating and linked findings; then choose Review this rating or Suggest clearer wording. All four tables have a row desk, including the economic profile. Submitting creates a public issue under your account [src: evidence:workflows/submissions/recipe-rows.md §Reviewer: browser or CLI]. The same route works from the command line:

```sh
git fetch origin main
pin=$(git rev-parse origin/main)
rows=workflows/submissions/recipe_rows.py
python "$rows" inspect --revision "$pin" --practice agroforestry --table T3 --record agroforestry__drought__all
python "$rows" rating --revision "$pin" --practice agroforestry --table T3 --record agroforestry__drought__all \
  --decision hold --reason other --note "Describe what needs checking"
python "$rows" wording --revision "$pin" --practice agroforestry --table T3 --record agroforestry__drought__all \
  --wording wording.json
```

The last two commands preview the exact receipt; `--submit` sends it. Wording is a small JSON file: mechanism and conditions for hazard, scorecard and economic rows, or a justification for a suitability row. The desk binds the practice, table, record, evidence IDs, register revision and hashes of the visible row and its evidence, so a receipt cannot be moved to a different row or edition.

An operator then applies one receipt per protected pull request [src: evidence:workflows/submissions/recipe-rows.md §Operator: preview, open protected PR, verify]:

```sh
python "$writer" --ciat-repo "$ciat" --base "$base" row "$receipt"
python "$writer" --ciat-repo "$ciat" --base "$base" --open-pr row "$receipt"
```

A rating review preserves existing finding approvals and compiled values. Suitability wording may change the explanation but not the mapping's inputs, gates, weights or thresholds. At the operating revision no rating or wording had yet been applied through this route: the rating review log held only the 37 events carried over from the producer, and the candidate manifest lists the wording input with the hash of an empty file [src: evidence:publication/recipe-candidate.json].

**The public dashboard does not yet link to the row desk.** The live dashboard is the 10 November design and stays the live design. Its "My reviewed" list reads applied rating history for the hazard, suitability and scorecard tables; it has no economic-profile queue. Its row cards do not yet carry the two actions, Review this rating and Suggest clearer wording. Adding them is a design integration task with a fixed contract: each action links to the reviewer's running local desk at `http://127.0.0.1:8934/rows`, passing the full evidence revision, the practice, the table and the record or mapping ID, with `kind=rating` or `kind=wording` to preselect the action. The desk rejects a link from a different edition, the page must tell reviewers how to start the desk when it is not running, and the public dashboard holds no write credentials [src: evidence:workflows/submissions/recipe-rows.md §Dashboard integration (November 10 design)]. Until the links exist, start the desk and find the row there.

### Method decisions (route 6)

The method repository owns new scientific rulings and their supersession history. A decision is a coded event, written to a local JSON file with its sequence number, date, scope, statement and public source, recorded with the register tool and opened as a method pull request [src: method:decisions/README.md §Propose, decide or implement a change]:

```sh
git switch -c method-decision/my-question origin/main
python3 decisions/register.py record /path/to/event.json
python3 decisions/register.py check --base "$(git rev-parse origin/main)" --verify-implementations
```

The actions are `propose` (a new question, published as open), `park` and `reopen`, `decide` (the accepted ruling, published as decided with implementation pending) and `implement` (what put the ruling into effect, with a reference to a file or commit at a full revision). To replace a decided rule, propose a new code and name the old one in the new decision's `supersedes` field; older editions still resolve the ruling they used. A proposal becomes official when a reviewer accepts the pull request and it merges. The evidence repository cites a decision by the pair method revision and decision code.

The register keeps the 165 historical decision codes from the earlier ledger, whose scientific projection is published in the evidence repository [src: evidence:registers/methodology/decisions/method_decisions.csv]. At the revision this methodology was built from, one new code had been recorded through the route, with its propose, decide and implement events. Historical codes show implementation as unverified until an implementation event supplies evidence [src: method:decisions/README.md §Historical records and verification].

### Definitions, rule tables, tools and mappings (route 7)

Ownership decides the route.

**Method-owned.** The variable definitions, practice families, dataset bindings, target crosswalk, magnitude bands and 15 policy and vocabulary tables belong to the method repository. A change takes four steps: record the ruling in the decision register; edit the authored file on a branch; build and check a release, approving each changed table against its decision code, and open a method pull request; then open a separate pull request in the evidence repository that adopts the immutable release, rebuilds the candidate and shows the changed recipe rows [src: method:configuration/README.md §Release compiler configuration]:

```sh
python3 configuration/release.py build --base origin/main \
  --approve schema/lookups/family_rollup_policy.csv=plantation_rollup
python3 configuration/release.py check --base origin/main
```

and, in the evidence repository [src: evidence:configuration/README.md §Adopt a method release]:

```sh
python3 workflows/submissions/configuration.py pin "$method_sha"
python3 workflows/submissions/configuration.py build --ciat-repo "$ciat_checkout"
python3 workflows/submissions/check_registers.py --base origin/main --ciat-repo "$ciat_checkout"
```

A later method merge takes effect in compilation only after a new adoption pull request merges. Existing editions keep their pins. A row keeps its recorded ratification status when released, including pending, rejected and blank: release is not approval.

**Evidence-owned.** The tool register, the WOCAT hazard and impact mappings and the per-finding direction exceptions belong to the evidence repository. A change is an event naming the table, the row key, the expected hash of the row before the change, the method revision, the changed fields, a reason and source provenance; it is recorded, rebuilt, verified and opened as a pull request. Every cited finding must belong to the stated source, and a person checks that the source supports the changed fields [src: evidence:configuration/README.md §Propose an evidence-owned change]. At the operating revision two such changes had been applied and one method release adopted.

**Still held.** Some compiler inputs have no change route yet and stay pinned at archived revisions [src: method:configuration/README.md §Ownership outside this release]:

- accepted suitability functions and run weights, which remain bound to their function fingerprints in the archived compiler; a changed function needs a separate scientific release;
- the numeric compilation policy for suitability, which mixes reusable conventions with individual finding adjudications and stays pinned until the two are split;
- searched-with-no-evidence rows, pending a structured update;
- the IPCC confidence matrix, the World Bank income groups and external class legends, pending clearance to redistribute them.

A run that would change a gate, a weight or a threshold in a suitability recipe therefore still stops at a proposal.

### One route that is planned

| Route | What you can do now | What is missing | Open plan |
|---|---|---|---|
| Sweep metrics and the learnings cursor | Keep measurements and proposed adjustments in the run record | A protected append with run, evidence and ruleset pins, and proof linking processed feedback to the instruction or check that changed | [Plan for recording retrospectives](https://github.com/RuralScan/evidence/issues/41) |

[src: evidence:workflows/submissions/README.md §Which records can I update?]

### How the validator bounds all of this

The register check verifies the migrated inventory against the manifest and replays each new change against its base revision. It also verifies the adopted method files against the method pin and replays the evidence-owned configuration changes. Its finding writer may change only the evidence register, the source register and the finding review log. The search register, acquisition queue, progress ledger and source register may change only together with a recorded operation, and the rating review log only through a replayed rating receipt. The tool register and the five method-owned registers are checked through the configuration history instead. Every other migrated file must still match its manifest hash [src: evidence:workflows/submissions/check_registers.py]. The earlier restriction to three files was the first stage of the move, not its final state.

### The guides to follow

Five guides in the evidence repository once described the earlier arrangement and have been corrected. They are current at the operating revision:

- the assisted-run handbook, which sends completed searches and verified sources to the registration commands [src: evidence:handbook/assisted-evidence-run.md §Run an assisted evidence search and extraction];
- the review-records guide, which points a new compiled-row review to the row desk [src: evidence:handbook/review-records.md §Find the right review record];
- the review-export guide, which separates replaying a historical CSV from making a live submission [src: evidence:workflows/review_exports/README.md §Preview a browser review CSV];
- the run-record guide, which stores the issue receipt and the merged pull request [src: evidence:workflows/run_record/README.md §Create and verify];
- the snapshot guide, which says the producer was the writer when the starting copy was taken and links the current routes [src: evidence:workflows/evidence_snapshot/README.md §Register migration seed].

## What is public, what is not, and what is unwritten

**(a) Public and runnable today (evidence repository)**

- Offline screening replay and new-search capture, worksheet and staging tools [src: evidence:workflows/discovery/README.md §Replay the terrace screening example] [src: evidence:workflows/discovery/README.md §Run a new search].
- Source verification, acquisition and identity check [src: evidence:workflows/acquisition/README.md §Worked example · WOCAT terrace manual].
- Page-anchored PDF extraction to private staging, and a bridge that runs the producer's checks on disposable copies [src: evidence:workflows/extraction/README.md §Recheck the historical record in CIAT].
- Model-neutral task briefs for each stage [src: evidence:handbook/assisted-evidence-run.md §1. Frame and capture the search].
- Ruleset catalogue and hash check; run records [src: evidence:rulesets/README.md §Verify against a local clone] [src: evidence:workflows/run_record/README.md §Create and verify].
- The registers and their verification; the submission desk for finding votes and extraction proposals; the protected register workflow [src: evidence:workflows/evidence_snapshot/README.md §Register migration seed] [src: evidence:workflows/submissions/README.md §Apply approved submissions].
- The operator command for discovery runs, source registration and progress stamps [src: evidence:workflows/submissions/registration.md §Register discovery, sources and progress].
- The row desk and its command-line equivalent for rating reviews and row wording; automatic recompilation and the candidate manifest [src: evidence:workflows/submissions/recipe-rows.md §Review a rating or change row wording] [src: evidence:publication/recipe-candidate.json].
- Adoption of a method release, and source-backed changes to the tool register and source-specific mappings [src: evidence:configuration/README.md §Update compiler configuration].
- In the method repository: the decision register and the configuration release [src: method:decisions/README.md §Record a scientific method decision] [src: method:configuration/README.md §Release compiler configuration].
- Review-record previews for saved decisions, CSV exports and browser backups [src: evidence:handbook/review-records.md §Find the right review record].

**(b) Read from the producer repository, which is read-only**

- The live skills, contracts, defect catalogue and slash commands [src: AGENTS.md §Current pipeline maintenance].
- The compiler and central checks that the evidence repository pins and reruns: the synthesis engines, the prose validator and the content gates [src: .agents/skills/source-command-t4-synthesise/SKILL.md §Reproducible workflow] [src: src/nbs_ruralscan/recipe/prose.py].
- The historical records, review batches and instruction archives.
- Writers that are now historical. The registrar, the staging ingest, the review server, one-click submission and both review-export importers refuse to run at the retirement revision. The ledger, search-log, sweep-metrics and learnings commands still run on a local copy, but the producer's continuous integration rejects any change to the files they write [src: scripts/register-discovery.py] [src: scripts/ingest-effects-staging.py] [src: docs/REVIEWER_GUIDE.md §Each review session] [src: src/nbs_ruralscan/schema_tools/ledger.py]. Their successors are listed under "Recording work now"; sweep metrics and the learnings cursor have none yet.
- Queue acquisition, library hydration and the OCR adapter, which have no counterpart in the evidence repository beyond its own acquisition tool [src: docs/HYDRATION.md §One-time: point at the library].

**(c) Not written anywhere**

For each item, no file found at the pinned revision or in the evidence repository states this:

- which model or effort level to use for orchestration, sub-agent lanes or independent challenge (the prose writer's default label names one model family and one command file names another [src: scripts/write-prose.py] [src: .claude/commands/fix-pr-conflicts.md]);
- expected cost, token use or run time per sweep;
- how to load the skills into an agent other than the one the team used;
- an end-to-end setup guide for the evidence pipeline (each evidence workflow states its own requirements; the prerequisites above are assembled from several files);
- how a new team obtains access to the team source library;
- how many sub-agent lanes to run, or how to size a lane;
- a structured register field for model identity or settings;
- a record format for the operator's authorisation of scope before a sweep;
- where the operating instructions will be kept once they leave the producer repository (the plan names two ruleset directories that do not yet exist).

## Assumptions and limits

- The producer commands quoted in this chapter are those of the scientific edition and no longer record anything. Recording work needs the evidence repository, a GitHub account, a read-only producer clone and, for sources and extractions, the team library. The team library is still the only way to check a quote against its source.
- The routes were verified at the operating revision by reading the guides and code and by the repositories' own tests, which use fixtures. Real use so far is thin: one extraction correction, one new method decision, one adopted method release and two evidence-owned configuration changes. No discovery run, source registration, progress stamp, rating review or wording change had been applied on the main line. Expect rough edges on first real use.
- Retrospectives cannot yet be recorded officially, and the accepted suitability functions, their weights and the numeric compilation policy cannot yet be changed. A run that needs one of these stops at a proposal.
- The public dashboard does not yet link its row cards to the row desk, so rating reviews and wording proposals start from the local desk.
- The pinned files contain internal contradictions, listed where they arise: the T3/T6 skill's version references, duplicate version-log entries, the playbook and reviewer guide on Windows submission, and the setup script against `AGENTS.md`. The playbook's discovery workflow also tells the reader to add candidates to the source register and log quotes in the evidence register, which conflicts with the same playbook's acquisition section, the hydration guide (source row created at the central merge) and the ban on hand-appending evidence [src: PLAYBOOK.md §Perform literature & tools discovery] [src: PLAYBOOK.md §Acquisition queue] [src: docs/HYDRATION.md §The order of operations (pre-SRC sources)] [src: AGENTS.md §Don't]. Follow the stricter rule.
- Passing every automated check does not prove semantic fidelity; quote matching cannot show that the encoded meaning is right [src: .agents/skills/source-command-extract-evidence/SKILL.md §Close the work].
- Historical runs cannot be fully reproduced: archives identify instructions, not prompts, models or settings [src: evidence:rulesets/README.md §Which instructions apply to the terrace example?].
- Effort counts from a continued sweep are not evidence strength, and counts from different editions are never combined; see [[ch:evidence-base]] and [[ch:editions]].
- The routes are still being built. This chapter fixes the scientific description at producer revision `e5c8da02` and the operating description at evidence revision `8c6f793f`; the evidence repository will have moved on by the time you read this. Two of the routes described here shipped within hours of each other while this chapter was being written. Check the submissions guide before relying on a command quoted here.

## Where this is configured

- Registers: [[table:SRC]], [[table:EV]], [[table:SRCH]], [[table:FAM]], [[table:VONT]], [[table:XW]], [[table:BANDS]], [[table:TOOL]].
- Lookups and manifest: `schema/lookups/` (for example `variable_direction_sense.csv`, `crop_scope_policy.csv`), `schema/structure/columns.json`.
- Instructions: `AGENTS.md`, `.agents/skills/`, `.agents/skills/extraction_contracts/`, `.agents/skills/_versions/`, `.claude/commands/`, `methodology/RULESET_VERSIONS.md`, `methodology/search_protocol.md`, `methodology/extraction_retrospective.md`.
- Staging and corpus: `pipeline/staging/`, `.cache/corpus/`, `pipeline/acquisition_queue.csv`.
- Progress and logs: `pipeline/progress_ledger.csv`, `pipeline/metrics/review_log.csv`, `pipeline/metrics/row_review_log.csv`, `pipeline/metrics/sweep_log.csv`, `pipeline/metrics/learnings_log.csv`, `methodology/discovery_logs/`.
- Review decisions: `pipeline/review/decisions.json` (local pending decisions, not committed at the pin), `docs/review/` (review-page batches).
- Evidence repository, current records: `registers/` (the same relative paths as the producer's registers, ledger, logs and metrics), `registers/manifest.json`, `registers/applied-receipts.json`, `operations/`, `recipe-inputs/wording.jsonl`, `row-reviews/receipts.jsonl`, `publication/review-queue.json`, `publication/recipe-candidate.json`, `configuration/` (`method-pin.json`, `changes.json`, `lookups/`, `method-lookups/`).
- Evidence repository, procedures: `workflows/submissions/` (`README.md`, `registration.md`, `recipe-rows.md`), `workflows/discovery/`, `workflows/acquisition/`, `workflows/extraction/`, `workflows/run_record/`, `rulesets/catalog.json`, `handbook/assisted-evidence-run.md`, `handbook/review-records.md`.
- Method repository: `decisions/` (`events.csv`, `current.csv`), `configuration/` (`contract.json`, `release.json`, `lookups/`), `data-model/configuration/`.
- See also [[ch:reproduce]] for rebuilding a published edition.
