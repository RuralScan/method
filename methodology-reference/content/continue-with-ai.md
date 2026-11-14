---
title: Continue the evidence base with an AI system
slug: continue-with-ai
summary: Set up and run the agent-plus-human system that adds sources, findings and re-synthesised rows to the evidence base, knowing which instructions, checks and human decisions govern each step and what is not yet written down.
sources:
  - AGENTS.md
  - CLAUDE.md
  - PLAYBOOK.md
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
  - evidence:.github/workflows/evidence-checks.yml
  - method:dashboard/ai.html
---

## What this chapter is for

Continuing the evidence base means three kinds of work: finding and acquiring more sources, extracting more findings (evidence units) from them, and re-running synthesis so that suitability rules, hazard rows and scorecard rows reflect the enlarged and reviewed evidence. The rules for each step are set out in [[ch:discovery]], [[ch:acquisition]], [[ch:extraction]], [[ch:review-and-quality]], [[ch:suitability-synthesis]], [[ch:effect-synthesis]] and [[ch:rulesets-and-learning]]. This chapter explains how to set up and operate the system that applies those rules: an AI coding agent of your choice, a set of versioned instruction files, deterministic checks, and people who approve what enters the record.

The governing principle: model output is a proposal; only validated, human-reviewed records enter the registers [src: evidence:README.md §Planned structure] [src: AGENTS.md §Don't] [src: .agents/skills/source-command-extract-evidence/SKILL.md §Close the work]. The chapter describes the producer repository at the revision pinned for this edition, and says explicitly where the public evidence repository has moved on since.

Read this first if you are starting now. The instructions, the deterministic checks and the synthesis engines are in the producer repository. Since this edition, submitting findings, extraction proposals and review votes has moved to the evidence repository, and the producer repository no longer accepts those writes. A team starting today therefore reads its instructions and runs its tools from the producer repository, and submits through the evidence repository as described under "Submitting work since this edition".

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

## Before you start

The prerequisites below are gathered from separate files; no single setup guide exists (see the last list in this chapter).

- **Python 3.12 or later and uv.** The package declares `requires-python = ">=3.12"`; continuous integration installs Python 3.12 through uv [src: pyproject.toml §project] [src: .github/workflows/ci.yml §checks]. Add dependencies with `uv add`, and run the checks with uv [src: AGENTS.md §Run / preview / deploy].
- **Git and the GitHub command-line client.** Review submission uses Python, Git and the GitHub CLI; the reviewer must be signed in [src: docs/REVIEWER_GUIDE.md §Each review session] [src: PLAYBOOK.md §Review flagged evidence (QA/QC → main)]. Write access to the producer repository is required for decisions that change the register [src: docs/REVIEWER_GUIDE.md §QA/QC Reviewer Guide].
- **A clone of the producer repository, set up once.** Run the setup script after cloning [src: AGENTS.md §Run / preview / deploy]:

```sh
bash scripts/setup-repo.sh
```

  The script registers three merge drivers (generated JSON, register CSVs, keyed JSON) and sets `core.autocrlf false` [src: scripts/setup-repo.sh]; `AGENTS.md` mentions only the first [src: AGENTS.md §Run / preview / deploy].
- **A clone of the evidence repository**, if you will use its model-neutral workflows, ruleset catalogue, run records or submission desk. Its workflows ask for Python 3.12 and uv for acquisition and extraction, and Python 3.10 or later for the offline screening replay [src: evidence:workflows/acquisition/README.md §Worked example · WOCAT terrace manual] [src: evidence:workflows/discovery/README.md §Replay the terrace screening example].
- **Access to the team source library and a hydrated local corpus.** The corpus is not version-controlled, so a fresh clone has no sources; it is copied from a local mirror of the team library whose root is set with the `NBS_LIBRARY_ROOT` environment variable [src: docs/HYDRATION.md §One-time: point at the library]. Without it, the review apply step fails its provenance guardrail [src: docs/REVIEWER_GUIDE.md §One-time setup]. How a new team obtains library access is not documented.
- **Credentials named by steps.** `LENS_TOKEN` for Lens.org discovery [src: scripts/discover-sources.py]; `OPENALEX_API_KEY` when keyed OpenAlex access is used in the evidence repository's capture tool [src: evidence:workflows/discovery/README.md §Capture records]. Unpaywall lookups take a contact email parameter [src: methodology/search_protocol.md §OA-recovery]. DOI verification calls Crossref online [src: src/nbs_ruralscan/schema_tools/verify_metadata.py]. No other credentials are named for the evidence steps.
- **The review server** runs locally on port 8765, or another port given as an argument [src: docs/REVIEWER_GUIDE.md §Each review session].
- **Tesseract**, for scanned PDFs only: the OCR adapter adds an invisible Tesseract text layer [src: methodology/search_protocol.md §Scanned PDFs (no text layer)].
- **An AI coding agent.** No file states which agent, model or effort level to use; see the gaps list below.

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

**Using a different agent.** `AGENTS.md` describes itself as the canonical agent guide under the cross-tool `AGENTS.md` convention, read directly by coding agents; `CLAUDE.md` only imports it [src: AGENTS.md §opening note] [src: CLAUDE.md]. The skills are plain Markdown files that name the further files to read; none gives agent-specific loading steps. The evidence repository supplies model-neutral task briefs for each stage (framing queries, screening, extraction and an independent challenge of each staged claim) that a researcher can perform directly or give to an assistant [src: evidence:handbook/assisted-evidence-run.md §1. Frame and capture the search] [src: evidence:handbook/assisted-evidence-run.md §4. Extract and challenge each claim].

## The operating loop

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
| 12 Suitability synthesis | T4-synthesise skill; `scripts/synthesise-recipe.py` | Trial outputs; live CSV only after review | Structure, coverage, generate | Applicability, functions, masks and weights |
| 13 Effect synthesis | T3/T6-synthesise skill; `scripts/synthesise-t3t6.py` | Recipe CSVs and run report | Pre-synthesis gates; `check_account` | None at this step; rows reviewed at step 15 |
| 14 Prose | `scripts/write-prose.py` | Staging bundle; prose sidecar via `merge` | `check_account` refuses on any flag | Writer flags uncertain phrasing for a person |
| 15 Row review | `scripts/build-row-review-batch.py`; `scripts/apply-row-review-export.py` | Review log only | None | Approve, hold or reject each row |
| 16 Ledger and search register | `ledger` and `search_log` modules | Stamps for completed work only | `ledger.check` fails the build | None |
| 17 Retrospective | `/sweep-retro` command | Metrics, catalogue, checks, snapshot | Trend of flag rates | Ruleset change through review |

Table sources: the skills and scripts named in each row, cited in the subsections below, and [src: AGENTS.md §What is locked] [src: src/nbs_ruralscan/recipe/prose.py].

### Frame, discover and screen

The discovery skill requires practice, family, table and purpose before searching, and reconciliation with existing records [src: .agents/skills/source-command-discover-sources/SKILL.md §Scope and coverage]. When delegation is authorised, literature, grey and tool lanes run as separate agents writing only to staging [src: .agents/skills/source-command-discover-sources/SKILL.md §Agent contract]. A Lens.org query is staged with:

```sh
python3 scripts/discover-sources.py lens "<query>" --out pipeline/staging/discovery/<name>.json \
    [--size 50] [--year-from 2015] [--process updated_lit] [--tables "T3|T6"] [--reviews]
```

[src: scripts/discover-sources.py]. AGRIS is a manual browser lane; its command writes a template, not results [src: .agents/skills/source-command-discover-sources/SKILL.md §Search and screen]. The screening funnel and credibility rubric are in [[ch:discovery]].

### Register, verify and acquire

The registrar turns lane outputs into pending acquisition queue rows, search-register rows with verbatim queries and counts, ledger stamps and a tracked copy of each report; targeted searches require explicit per-lane protocols passed as `--family <id> --searched-by <identity> --protocols <lane=file.json>` [src: scripts/register-discovery.py] [src: methodology/search_protocol.md §What every search logs]. Metadata verification then round-trips each DOI through Crossref and rebuilds the citation; a DOI-less source needs its title found on the opening pages of the cached file; the offline `check` runs in the build [src: src/nbs_ruralscan/schema_tools/verify_metadata.py]. Before any source is labelled paywalled, the open-access recovery protocol must be exhausted [src: methodology/search_protocol.md §OA-recovery]. Files that a person downloaded are filed with an identity check by `scripts/intake-downloads.py` [src: scripts/intake-downloads.py]. Scanned PDFs are OCR'd once:

```sh
uv run python scripts/ocr-scan.py <source_id> [--force]
```

[src: methodology/search_protocol.md §Scanned PDFs (no text layer)]. Rules are in [[ch:acquisition]].

### Hydrate

Sources being swept have no source-register row yet, so hydration for a sweep reads the queue:

```sh
python3 scripts/hydrate-corpus.py --queue --nbs <nbs_id>
```

[src: PLAYBOOK.md §Acquisition queue]. The source-register row is created at the central merge, after extraction [src: docs/HYDRATION.md §The order of operations (pre-SRC sources)]. Pending rows do not block a sweep; the register is append-only and later arrivals are extracted on top [src: docs/HYDRATION.md §Hydrating for a sweep].

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

The two producer guides disagree on one point: the playbook says the Windows submission uses Git Bash, the reviewer guide says Bash is not required [src: PLAYBOOK.md §Review flagged evidence (QA/QC → main)] [src: docs/REVIEWER_GUIDE.md §Each review session]. The wrapper's own comment supports the reviewer guide [src: scripts/submit-review.sh].

### Synthesise

Suitability synthesis starts from reviewed evidence and the last accepted decision; unreviewed diagnostics need an explicit flag and an isolated output directory [src: .agents/skills/source-command-t4-synthesise/SKILL.md §Reproducible workflow]:

```sh
PYTHONPATH=src python scripts/synthesise-recipe.py <nbs_id> --dry-run
PYTHONPATH=src python scripts/synthesise-recipe.py <nbs_id> \
  --output-dir <isolated-trial-directory> --report <trial-report.json>
```

Only after review of the differences does the agent regenerate the live CSV:

```sh
PYTHONPATH=src python scripts/synthesise-recipe.py <nbs_id>
python src/nbs_ruralscan/schema_tools/generate.py schema
python src/nbs_ruralscan/schema_tools/structure.py schema
PYTHONPATH=src python -m nbs_ruralscan.schema_tools.t4_coverage
```

[src: .agents/skills/source-command-t4-synthesise/SKILL.md §Reproducible workflow]. Effect synthesis runs the gates on pooled units first, then the engine:

```sh
python3 scripts/synthesise-t3t6.py <nbs_id> --dry-run     # preview table
python3 scripts/synthesise-t3t6.py <nbs_id>               # writes the recipe CSVs + report
python3 src/nbs_ruralscan/schema_tools/generate.py schema  # regenerate JSON
python3 -m nbs_ruralscan.schema_tools.check_account schema/recipes/<nbs_id>/T6_nbs_scorecard.json
```

[src: .agents/skills/source-command-t3t6-synthesise/SKILL.md]. Class, levels and confidence are engine outputs; a disagreement is fixed at the evidence unit and the engine re-run [src: .agents/skills/source-command-t3t6-synthesise/SKILL.md]. See [[ch:suitability-synthesis]] and [[ch:effect-synthesis]].

### Prose and row review

Row prose stays empty until the gated prose writer runs [src: .agents/skills/source-command-t3t6-synthesise/SKILL.md]. The writer may draw only on a bundle of the rows' used units:

```sh
python3 scripts/write-prose.py bundle <nbs_id>            # rows needing prose + their used units
python3 scripts/write-prose.py check  <nbs_id> <prose.json>   # validate, write nothing
```

A third subcommand, `merge`, runs the account check, refuses on any flag, and records the prose in a sidecar keyed to the rows' current evidence IDs [src: scripts/write-prose.py]. Generated rows are then reviewed in row batches; a row decision is a review record appended to a log, and changes nothing in the registers or recipes. Holds and rejects become the orchestrator's list of evidence, routing or prose to fix before regenerating [src: scripts/build-row-review-batch.py] [src: scripts/apply-row-review-export.py].

### Ledger, search register and retrospective

Search and screening stages are stamped by the step that did them, through the ledger module's `mark` command; extraction and review are derived from the register. The ledger check runs in the build [src: src/nbs_ruralscan/schema_tools/ledger.py]:

```sh
uv run python3 -m nbs_ruralscan.schema_tools.ledger check
```

A search not passed through the registrar is logged with the search-log module's `log` command, which takes the practice, table, category, family, verbatim terms, limits, ruleset version and run ID [src: src/nbs_ruralscan/schema_tools/search_log.py]. After every sweep the retrospective measures, gates, triages and encodes learnings [src: methodology/extraction_retrospective.md §The loop]:

```sh
uv run python3 src/nbs_ruralscan/schema_tools/sweep_metrics.py --label <sweep>
```

The learnings cursor (`learnings status`, `learnings record`) proves which review decisions have been turned into adjustments [src: src/nbs_ruralscan/schema_tools/learnings.py]; `record` is used only after the complete current feedback set has been read [src: .claude/commands/sweep-retro.md §Feedback accounting (v1.7.0)].

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
| Keep, drop, reclassify or query a finding | Quote beside the source passage, role, family, units | Evidence register review fields and the review log; drops need a coded reason [src: AGENTS.md §What is locked] |
| Numeric plausibility | Band width, precision, jumps, proxies, transfer | Hold or approval kept separate from qualitative keep [src: .agents/skills/extraction_contracts/T4_review_contract.md] |
| Suitability rule change | Differences against the accepted recipe; applicability, functions, tails, masks, weights | Batch audit synthesis decision record [src: .agents/skills/source-command-t4-synthesise/SKILL.md §Translating evidence into a rule] |
| Generated row review | Class, confidence, prose, the evidence it rests on | Row review log [src: scripts/apply-row-review-export.py] |
| Merge to the main line | The submission's changed files and CI result | Branch protection requires checks and one approval; review-only submissions from allowlisted reviewers are approved by automation [src: .github/workflows/auto-merge-review.yml] |
| Ruleset change | Retrospective triage | Version log row and archived snapshot [src: methodology/RULESET_VERSIONS.md §Ruleset versions] |

No pinned file states a separate explicit "start" approval for large sweeps beyond the authorised-scope rule above.

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

Run records are private and are not part of the registers [src: evidence:workflows/run_record/README.md §Create and verify]. The method dashboard states that some original prompts and model settings for historical work are unavailable and that the gap should stay explicit [src: method:dashboard/ai.html §What the audit can establish].

## Submitting work since this edition

Everything above describes the producer repository at the pinned revision. Since then the evidence repository has added a submission route. This section describes the evidence repository at its current revision, which is later than the pin.

- **Register baseline.** The evidence repository holds a `registers/` seed copied from a producer commit later than the pin. Its manifest lists each file's source path, SHA-256, size and record count, plus Git objects for external inputs; the public copy of the method-decision ledger omits the task-assignment column [src: evidence:registers/manifest.json] [src: evidence:workflows/evidence_snapshot/README.md §Register migration seed].
- **Submission desk.** Finding votes and extraction proposals become public issues in the evidence repository under the submitter's own GitHub account; the issue number is the receipt. A local desk binds to 127.0.0.1 on port 8934 [src: evidence:workflows/submissions/README.md §Use the local desk for browser or CSV entry]:

```sh
source_repo=/path/to/nbs_ruralscan
git fetch origin main
pin=$(git rev-parse origin/main)
gh api user --jq .login
python3 workflows/submissions/serve.py --ciat-repo "$source_repo" --revision "$pin"
```

  Exported CSVs and staged extraction files are submitted per lane and revision [src: evidence:workflows/submissions/README.md §Submit an exported CSV or extraction file]:

```sh
python3 workflows/submissions/intake.py csv votes.csv --lane T4 --revision "$pin"
python3 workflows/submissions/intake.py extraction t4-units.json --lane T4 --revision "$pin"
python3 workflows/submissions/intake.py extraction effects.json --lane T3/T6 --revision "$pin"
```

- **Protected register workflow.** A maintainer who has reviewed an extraction labels its issue `approved-extraction`. `workflows/submissions/registers.py`, given issue numbers, the producer clone and a local corpus, previews by default and with `--open-pr` opens a protected register pull request carrying the receipts. It checks reviewer identity, the original issue body, the matching finding and source, and agreement across eligible ballots; opposing votes stay pending, and a receipt ledger prevents duplicate application. A register pull request needs approval and current checks [src: evidence:workflows/submissions/README.md §Apply approved submissions]. The repository's continuous integration verifies the official registers and reproduces the review queue [src: evidence:.github/workflows/evidence-checks.yml].
- **Authority at the time of writing.** The register command refuses to publish until a retirement marker is present on the producer repository's main line [src: evidence:workflows/submissions/README.md §Apply approved submissions]. When this chapter was written, that marker was present on the producer repository's main line, the producer's own review, ingest and import tools refused new writes for the hazard, suitability and scorecard evidence, and the evidence repository's receipt journal recorded one applied submission [src: evidence:registers/applied-receipts.json]. Both observations are later than the pinned revision. Two guides in the evidence repository still describe the earlier arrangement: the snapshot guide says the producer repository retains authority to update the registers during a preparation stage [src: evidence:workflows/evidence_snapshot/README.md §Register migration seed], and the operator handbook says live registration, correction and review take place in the producer repository [src: evidence:handbook/assisted-evidence-run.md §Run an assisted evidence search and extraction]. Treat the submissions guide as current, and confirm the marker before submitting.
- **What has no route yet.** The submission desk takes finding votes and extraction proposals for the suitability lane and the hazard and scorecard lane. Reviews of generated rows and method decisions are stated to keep their existing separate workflows [src: evidence:workflows/submissions/README.md §Preview historical CIAT submissions for one revision], and the producer's row-review importer is among the tools that now refuse writes, so no current route for recording a row review was found.

## What is public, what is not, and what is unwritten

**(a) Public and runnable today (evidence repository)**

- Offline screening replay and new-search capture, worksheet and staging tools [src: evidence:workflows/discovery/README.md §Replay the terrace screening example] [src: evidence:workflows/discovery/README.md §Run a new search].
- Source verification, acquisition and identity check [src: evidence:workflows/acquisition/README.md §Worked example · WOCAT terrace manual].
- Page-anchored PDF extraction to private staging, and a bridge that runs the producer's checks on disposable copies [src: evidence:workflows/extraction/README.md §Recheck the historical record in CIAT].
- Model-neutral task briefs for each stage [src: evidence:handbook/assisted-evidence-run.md §1. Frame and capture the search].
- Ruleset catalogue and hash check; run records [src: evidence:rulesets/README.md §Verify against a local clone] [src: evidence:workflows/run_record/README.md §Create and verify].
- Register seed and verification; submission desk; protected register workflow [src: evidence:workflows/evidence_snapshot/README.md §Register migration seed] [src: evidence:workflows/submissions/README.md §Apply approved submissions].
- Review-record previews for saved decisions, CSV exports and browser backups [src: evidence:handbook/review-records.md §Find the right review record].

**(b) Present only in the producer repository (at the pin)**

- The live skills, contracts, defect catalogue and slash commands [src: AGENTS.md §Current pipeline maintenance].
- The registrar, queue acquisition, library hydration and OCR adapter [src: scripts/register-discovery.py] [src: docs/HYDRATION.md §One-time: point at the library].
- The staging ingest, auto-quarantine and full build gates [src: scripts/ingest-effects-staging.py] [src: .github/workflows/ci.yml §checks].
- The review server and one-click submission [src: docs/REVIEWER_GUIDE.md §Each review session].
- Synthesis engines, prose writer, row review, ledger, learnings cursor and sweep metrics [src: .agents/skills/source-command-t4-synthesise/SKILL.md §Reproducible workflow] [src: scripts/write-prose.py] [src: src/nbs_ruralscan/schema_tools/ledger.py].

**(c) Not written anywhere**

For each item, no file found at the pinned revision or in the evidence repository states this:

- which model, model family or effort level to use for orchestration, sub-agent lanes, independent challenge or prose writing;
- expected cost, token use or run time per sweep;
- how to load the skills into a particular agent other than by reading `AGENTS.md` and the skill files;
- a single end-to-end setup guide for a new team (the prerequisites above are assembled from several files);
- how a new team obtains access to the team source library;
- how many sub-agent lanes to run, or how to size a lane;
- a structured register field for model identity or settings;
- a record format for the operator's authorisation of scope before a sweep.

## Assumptions and limits

- The steps described at the pinned revision assume write access to the producer repository and access to the team library. Since the move described above, new findings and votes are submitted through the evidence repository instead; the team library is still needed to check any quote against its source.
- The pinned files contain internal contradictions, listed where they arise: the T3/T6 skill's version references, duplicate version-log entries, the playbook and reviewer guide on Windows submission, and the setup script against `AGENTS.md`. The playbook's discovery workflow also tells the reader to add candidates to the source register and log quotes in the evidence register, which conflicts with the same playbook's acquisition section, the hydration guide (source row created at the central merge) and the ban on hand-appending evidence [src: PLAYBOOK.md §Perform literature & tools discovery] [src: PLAYBOOK.md §Acquisition queue] [src: docs/HYDRATION.md §The order of operations (pre-SRC sources)] [src: AGENTS.md §Don't]. Follow the stricter rule.
- Passing every automated check does not prove semantic fidelity; quote matching cannot show that the encoded meaning is right [src: .agents/skills/source-command-extract-evidence/SKILL.md §Close the work].
- Historical runs cannot be fully reproduced: archives identify instructions, not prompts, models or settings [src: evidence:rulesets/README.md §Which instructions apply to the terrace example?].
- Effort counts from a continued sweep are not evidence strength, and counts from different editions are never combined; see [[ch:evidence-base]] and [[ch:editions]].
- The submission route is in transition. This chapter fixes the producer description at the pin and the evidence-repository description at its current revision; either may have changed since.

## Where this is configured

- Registers: [[table:SRC]], [[table:EV]], [[table:SRCH]], [[table:FAM]], [[table:VONT]], [[table:XW]], [[table:BANDS]], [[table:TOOL]].
- Lookups and manifest: `schema/lookups/` (for example `variable_direction_sense.csv`, `crop_scope_policy.csv`), `schema/structure/columns.json`.
- Instructions: `AGENTS.md`, `.agents/skills/`, `.agents/skills/extraction_contracts/`, `.agents/skills/_versions/`, `.claude/commands/`, `methodology/RULESET_VERSIONS.md`, `methodology/search_protocol.md`, `methodology/extraction_retrospective.md`.
- Staging and corpus: `pipeline/staging/`, `.cache/corpus/`, `pipeline/acquisition_queue.csv`.
- Progress and logs: `pipeline/progress_ledger.csv`, `pipeline/metrics/review_log.csv`, `pipeline/metrics/row_review_log.csv`, `pipeline/metrics/sweep_log.csv`, `pipeline/metrics/learnings_log.csv`, `methodology/discovery_logs/`.
- Review decisions: `pipeline/review/decisions.json` (local pending decisions, not committed at the pin), `docs/review/` (review-page batches).
- Evidence repository: `rulesets/catalog.json`, `registers/manifest.json`, `workflows/submissions/`, `workflows/run_record/`, `handbook/assisted-evidence-run.md`.
- See also [[ch:reproduce]] for rebuilding a published edition.
