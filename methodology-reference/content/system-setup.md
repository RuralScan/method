---
title: System, setup and continuing the work
slug: system-setup
summary: Find the right repository, start a bounded evidence task, and follow the human decisions needed before an agent's proposal becomes an accepted output.
sources:
  - method:README.md
  - method:decisions/README.md
  - method:configuration/README.md
  - method:handbook/implement-a-scan.md
  - evidence:handbook/assisted-evidence-run.md
  - evidence:handbook/evidence-hierarchy.md
  - evidence:workflows/submissions/README.md
  - evidence:workflows/submissions/registration.md
  - evidence:workflows/submissions/recipe-rows.md
  - evidence:workflows/discovery/README.md
  - evidence:workflows/run_record/README.md
  - evidence:workflows/synthesis/README.md
  - evidence:workflows/t4_synthesis/README.md
  - evidence:rulesets/README.md
  - runtime:README.md
  - retired:.ciat-evidence-readonly
---

## Choose where to work

The system separates **method definitions**, **evidence and review**, and **spatial execution**. An agent can draft a change; it cannot turn a passing software check into scientific approval. Start with the repository that owns the record you need to change. [src: method:README.md] [src: evidence:workflows/t4_synthesis/README.md]

Table: Repositories and their boundaries.

| Repository | What it holds | Open it when you need to… |
|---|---|---|
| [RuralScan/method](https://github.com/RuralScan/method) | Definitions, method decisions, contracts and these pages; the `gh-pages` branch publishes the site. | Change a practice definition, methodological rule or explanation. |
| [RuralScan/evidence](https://github.com/RuralScan/evidence) | Official source, finding and search registers; review receipts; operating workflows; scientific proposals and acceptance history. | Search, register sources, extract, correct or review findings, or propose a synthesis. |
| [RuralScan/runtime](https://github.com/RuralScan/runtime) | Data access, spatial computation and worked notebooks. | Apply a supported analytical package to a landscape. |
| [CIAT/nbs_ruralscan](https://github.com/CIAT/nbs_ruralscan) | Retired evidence records, historical instructions and pinned validation dependencies; also the [visual method](https://ciat.github.io/nbs_ruralscan/redesign/). | Read or replay history, supply pinned checks, or inspect the visual mock-up. Do not resume its evidence writers. |

The CIAT repository is not wholly frozen: its visual documentation can change. Its evidence registers and review write routes are retired. Current instructions live in the evidence workflows and their linked skills; historical ruleset archives retain their original stamps. A slash command is an adapter, not authority to bypass those routes. [src: retired:.ciat-evidence-readonly] [src: evidence:rulesets/README.md]

## How changes reach readers

**Method definition → evidence proposal → human decision → accepted package → compatible runtime.** Each arrow carries revisions and hashes. The website publishes a particular methodology source; its analytical edition, review-coverage snapshot and live review queue can have different revisions. [[ch:editions|Editions and checks]] lists those pins. Rebuilding a page does not approve evidence or update a runtime package. [src: method:configuration/README.md] [src: evidence:workflows/synthesis/README.md]

A pull request proposes a versioned change. Its checks validate the files and provenance; the required human decision depends on the change. A finding vote, a rating review, a method decision and scientific acceptance of a synthesis are distinct. [[ch:review-and-quality|Human review]] explains finding decisions; the acceptance gates below explain their downstream effect.

## Set up for the task

**Review only:** open the [review queue](https://ruralscan.github.io/method/#review-queue), choose your reviewer name and inspect the source beside each finding. Connect your acquired PDF folder when a public preview is unavailable. Save Keep, Drop or Query, then use **Submit my decisions**. Small batches open a prefilled GitHub issue; large batches require attaching the downloaded CSV. A browser draft is not a submitted receipt, and a receipt is not an applied decision. [src: evidence:workflows/submissions/README.md]

**Evidence work:** use Git, Python 3.12 and GitHub CLI. The shell examples below are for macOS/Linux. Work in a new folder with a clean evidence checkout and a separate directory for run files. The CIAT clone supplies historical Git objects only. After creating and activating the environment below, install the dependencies listed in the evidence checkout's [check workflow](https://github.com/RuralScan/evidence/blob/94a5b1c5e2bea65c79161388e78aecb20714cd66/.github/workflows/evidence-checks.yml); record the actual environment and commit used. Authenticate `gh` under your own account before proposing writes. [src: evidence:workflows/submissions/registration.md]

```sh
git clone https://github.com/RuralScan/evidence.git evidence
git clone --bare https://github.com/CIAT/nbs_ruralscan.git ciat-history.git
cd evidence
# Retain this inspected revision with the run.
git rev-parse HEAD
python3.12 -m venv .venv
. .venv/bin/activate
gh api user --jq .login
```

Start with this offline smoke test. It needs no model, account submission or source download:

```sh
run_dir=$(mktemp -d)
python workflows/discovery/screen.py stage \
  workflows/discovery/example/plan.json \
  workflows/discovery/example/decisions.json --out "$run_dir/terrace"
cat "$run_dir/terrace/report.md"
```

Expect **3 records retrieved, 3 screened, 1 included**: one reused WOCAT source, one excluded stone-line passage and one held seasonal-rainfall record. This replays stored decisions; it is not a new search or human sign-off. Then follow the [assisted-run handbook](https://github.com/RuralScan/evidence/blob/94a5b1c5e2bea65c79161388e78aecb20714cd66/handbook/assisted-evidence-run.md) for verified acquisition, source access and extraction. [src: evidence:workflows/discovery/README.md]

For country execution, use [[ch:implementing-the-method|Applying a country scan]]. For rebuilding this website, use [[ch:reproduce|Reproduce and check]]. Those setups have different inputs and should remain separate.

## Continue an existing run

1. **Recover the checkpoint.** Read the scope, run ID, repository revisions, actual instructions, source hashes, staged outputs, receipts and unresolved holds. Check what has merged before retrying. [src: evidence:workflows/run_record/README.md]
2. **Bound the next task.** Name the practice, family, table, question, sources or search channels, limits and expected output. Give the agent the relevant workflow and skill at their recorded revisions, plus applicable review feedback. [src: evidence:handbook/assisted-evidence-run.md]
3. **Inspect the originals.** Verify source identity and the acquired file; read the quoted page, headers, units and context. Stage claims and an independent challenge. Preserve unknowns, contrary evidence and unchecked scope. [src: evidence:handbook/assisted-evidence-run.md]
4. **Preview the change.** Use the appropriate route below against the inspected base. If main advances, reconcile intervening changes. Preserve receipt IDs so retries do not apply the same work twice. [src: evidence:workflows/submissions/registration.md]
5. **Close with evidence.** Retain checks, unresolved questions, proposal or receipt link, merged revision when available and next action. Record actual model identifier, prompt, exposed settings and hashes; mark unavailable information unknown. [src: evidence:workflows/run_record/README.md]

## Choose the update route

Table: Common continuation tasks and the record they produce.

| Task | Route and expected result |
|---|---|
| Add or revise a practice/family | Propose definitions and a [coded decision](https://github.com/RuralScan/method/blob/0bc7380aa579d876be2c42863245e21f8ed0e51f/decisions/README.md) in `method`; release reviewed configuration, then [adopt it](https://github.com/RuralScan/evidence/blob/94a5b1c5e2bea65c79161388e78aecb20714cd66/configuration/README.md) in `evidence`. Check supported IDs and consumers before adding a new practice; definition adoption alone does not add its workflow or runtime support. Preserve existing IDs and historical scope. Keep broader evidence visible without assigning it automatically to each child. |
| Update search terms or add sources | Start a new scoped capture with actual queries and screening reasons. [Registration commands](https://github.com/RuralScan/evidence/blob/94a5b1c5e2bea65c79161388e78aecb20714cd66/workflows/submissions/registration.md): `discovery` records SRCH, queue and optional progress; `source-batch` registers verified bundles together. `queue` repairs eligible queued metadata before acquisition is repeated. |
| Correct an existing finding | Submit an extraction correction through the [finding intake route](https://github.com/RuralScan/evidence/blob/94a5b1c5e2bea65c79161388e78aecb20714cd66/workflows/submissions/README.md). Human extraction approval precedes the protected register PR; the card records changed fields and reopens for review. |
| Review a rating or clarify wording | Use the [row-review route](https://github.com/RuralScan/evidence/blob/94a5b1c5e2bea65c79161388e78aecb20714cd66/workflows/submissions/recipe-rows.md). Rating history is separate from finding votes. Accepted AI rows require a new scientific proposal even for wording changes. |
| Change a scientific rule | Record the method decision and its implementation separately, then adopt the reviewed definition revision. A decision alone does not implement or recalibrate anything. |
| Generate T4 or T3/T6 outputs | Use the [T4](https://github.com/RuralScan/evidence/blob/94a5b1c5e2bea65c79161388e78aecb20714cd66/workflows/t4_synthesis/README.md) or [T3/T6](https://github.com/RuralScan/evidence/blob/94a5b1c5e2bea65c79161388e78aecb20714cd66/workflows/synthesis/README.md) proposal, validation, scientific acceptance and packaging route. Existing historical rows are not accepted fallbacks. |

Detailed commands: [src: method:decisions/README.md] [src: method:configuration/README.md] [src: evidence:handbook/evidence-hierarchy.md] [src: evidence:workflows/submissions/registration.md] [src: evidence:workflows/submissions/recipe-rows.md] [src: evidence:workflows/t4_synthesis/README.md] [src: evidence:workflows/synthesis/README.md]

## How human review constrains agents

**Finding review limits usable support.** Keep approves the claim within its recorded scope, not a threshold or global transfer. Query preserves the unresolved question; Drop retains history but excludes the finding. Conflicting eligible votes remain pending rather than becoming a consensus event. Unreviewed or held findings can remain visible in historical synthesis, but cannot silently support a newly accepted calibrated mapping or effect output. [src: evidence:workflows/submissions/README.md] [src: evidence:workflows/t4_synthesis/README.md] [src: evidence:workflows/synthesis/README.md]

**Scientific acceptance binds exact bytes.** The agent must account for every candidate, explain inclusion, exclusion, context and holds, and justify compatibility, independence, transfer and proposed values. An eligible human reviews the exact proposal revision and hash. A Keep vote, successful validation or ordinary software PR approval does not substitute for that acceptance. Agents must not invent human votes or acceptance receipts. [src: evidence:workflows/t4_synthesis/README.md] [src: evidence:workflows/synthesis/README.md]

**Later review can stop reuse.** Changed evidence, source metadata, reviews or definitions can make an accepted input packet stale. Holds or relevant rating rejections block packaging. Corrections need a new proposal and comparison, not edits to an accepted snapshot or a fallback to historical values. Runtime adoption remains separate. [src: evidence:workflows/t4_synthesis/README.md] [src: evidence:workflows/synthesis/README.md]

**Feedback must change the next task explicitly.** Carry the reviewer’s finding ID, reason and scope into the next brief; show the proposed correction and check it against the source. Propose reusable instruction/check changes with their version and evidence. Keep the feedback-to-fix links and measured results in the run record. The official sweep-metrics/learnings-cursor route remains [planned](https://github.com/RuralScan/evidence/issues/41); do not claim that feedback was incorporated merely because it was read. [src: evidence:handbook/assisted-evidence-run.md] [src: evidence:workflows/submissions/README.md]

## Technical implementation

**In preparation:** the consolidated implementation explanation and linked proposals. The [runtime repository](https://github.com/RuralScan/runtime) already contains a worked notebook and implementation documentation; this heading does not imply that repository is empty. [[ch:implementing-the-method|Applying and reporting a country scan]] describes the present example and its limits. An accepted T4 package is still a partial mapping package with `runtime_implemented: false`; it does not establish whole-recipe weighting or raster execution. [src: method:handbook/implement-a-scan.md] [src: evidence:workflows/t4_synthesis/README.md]

## Assumptions and limits

The setup test demonstrates software replay only. Automated checks cannot establish scientific meaning or independent origins. A fresh model run may produce different judgements; reproducibility requires retaining and replaying the exact accepted proposal. Source access and redistribution terms still apply. Follow the workflow revision recorded for the task, not an old command copied from a historical guide. [src: evidence:workflows/run_record/README.md] [src: evidence:workflows/synthesis/README.md]

## Where this is configured

[[table:SRC]], [[table:EV]] and [[table:SRCH]] hold sources, claims and searches. [[table:FAM]], [[table:VONT]] and [[table:BIND]] define scope and representation. Operating workflows and skills live in `RuralScan/evidence`; `RuralScan/method` owns method definitions and decisions. Their detailed contracts and immutable source links are listed above. See [[ch:editions|Editions and checks]] for this page's operating and analytical revisions.
