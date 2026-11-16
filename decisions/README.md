# Record a scientific method decision

RuralScan/method owns new scientific rulings and their supersession history. Submit the exact wording through a method PR. A proposal on a branch becomes an official entry when a reviewer accepts the PR and it merges into `main`. The GitHub review and merge identify who accepted it. RuralScan/evidence can cite a decision by the pair **method revision + decision ID** and consume the published CSV when compiling an edition.

Finding votes and rating reviews have their own register paths in RuralScan/evidence. A scientific decision changes method policy. An implementation event identifies the code or definitions that put that ruling into effect. A method decision on its own leaves the implementation status pending. [Finding and rating review routes](https://github.com/RuralScan/evidence/blob/017544fe55929cd03579494bbd4062db67697363/workflows/submissions/README.md)

## Read a decision at an edition

Use Python 3.9+ and Git. Run from a RuralScan/method checkout. Capture the SHA once and keep it with the consuming edition.

```sh
git fetch origin main
method_sha=$(git rev-parse origin/main)
python3 decisions/register.py show t3t6_provisional_setter --revision "$method_sha"
```

The result contains the method SHA, current decision, ordered method events and the historical scientific row when one exists. The reader verifies the legacy CSV against its pinned digest. For offline use, add `--evidence-repo /path/to/evidence` **before** the subcommand. The clone must contain the revision in [baseline.json](baseline.json).

For an evidence build, fetch the machine-readable projection by the same full SHA. Select rows by `decision_id`, retain the method SHA on the edition, and cite `decision_ref` for the ruling and `implementation_ref` for the implementing change. The source of a proposal is in `proposal_ref`.

```sh
curl --fail --location --output method-decisions.csv \
  "https://raw.githubusercontent.com/RuralScan/method/$method_sha/decisions/current.csv"
```

[Current projection](current.csv) · [Append-only method events](events.csv)

## Propose, decide or implement a change

1. Branch from the current method main revision. Choose a stable code for a new question. For an existing question, look up its code and `latest_sequence` in the projection.
2. Write the next event in a local JSON file. `sequence` starts at 1 or advances by one from the published value. Supply the actual recording date, scope, statement and public source. The template below illustrates a proposal. Replace the sample values with the scientific question and its source.
3. Run `record` and inspect the event and projection diff. A retry of the same event leaves one record. A different event using the same code and sequence requires reconciliation with the current history.
4. Open a PR with the scope, rationale and supporting source. For a decision, ask the reviewer to approve the exact outcome. For an implementation, link the change and inspect whether it covers the stated scope. The CI job verifies the historic prefix, derived CSV and newly cited implementation Git objects. Use the merged method SHA in downstream evidence work.

```json
{
  "decision_id": "example_scientific_question",
  "sequence": 1,
  "action": "propose",
  "recorded_on": "2026-11-16",
  "scope": "T3 hazard ratings",
  "statement": "Which hazard ratings should this rule cover?",
  "source_ref": "https://github.com/RuralScan/method/issues/17"
}
```

```sh
git switch -c method-decision/my-question origin/main
python3 decisions/register.py record /path/to/event.json
python3 decisions/register.py check --base "$(git rev-parse origin/main)" --verify-implementations
git diff -- decisions/events.csv decisions/current.csv
git add decisions/events.csv decisions/current.csv
git commit -m "Propose the scientific question"
git push -u origin HEAD
gh pr create --repo RuralScan/method --base main --fill
```

| Action | Scientific event | Published result |
|---|---|---|
| `propose` | A new question, its scope and proposal source | `open` |
| `park` / `reopen` | Why an open question was paused or a parked question was resumed | `parked` / `open` |
| `decide` | The accepted ruling and its source, against an open or parked code | `decided`, implementation `pending` |
| `implement` | What implemented the ruling, a supporting source and an `implementation_ref` to a GitHub file or commit at a full SHA | `decided`, implementation `implemented` |

To replace a decided rule, propose a new code and put the old code in the new `decide` event’s `supersedes` field. Multiple target codes are space-separated. The projection marks each predecessor `superseded` and names its successor in `superseded_by`. Older pinned editions still resolve the ruling used in that edition. A subsequent `implement` event can document a newer implementing revision. Prior implementation links stay in the event history. Code and recorded dates travel with the scientific text. Team assignments and administrative notes belong outside the register.

## Trace a real ruling

The code `t3t6_provisional_setter` records an existing publication rule. A T3 or T6 rating stays visible when a confirmed rating setter is held or unreviewed. It carries a provisional label. Incomplete setter coverage with no confirmed unresolved setter yields an undetermined status. The registration date in this register identifies when the code was recorded. The scientific source, implementation and test are independently addressable.

- [Published rule and scope](https://github.com/RuralScan/evidence/blob/017544fe55929cd03579494bbd4062db67697363/workflows/review_status/README.md#L11-L13)
- [Implemented setter and coverage calculation](https://github.com/RuralScan/evidence/blob/017544fe55929cd03579494bbd4062db67697363/workflows/review_status/build.py#L152-L165)
- [Held-setter replay through the compiler](https://github.com/RuralScan/evidence/blob/017544fe55929cd03579494bbd4062db67697363/workflows/review_status/test_status.py#L133)

## Historical records and verification

The historical baseline is the byte-verified, nine-column scientific projection in RuralScan/evidence. Its 165 codes enter at sequence zero. The original questions, options, recommendations, outcomes and source locators remain available through `show` or the CSV’s `legacy_ref`. The index links the exact baseline row for historical text. Historical implementation status is `unverified` for a decided ruling until a separate implementation event supplies evidence. Git history and the source digest preserve earlier editions. New rulings can continue an archived open question or supersede an archived decided code. [Original scientific projection](https://github.com/RuralScan/evidence/blob/017544fe55929cd03579494bbd4062db67697363/registers/methodology/decisions/method_decisions.csv)

```sh
python3 -m unittest discover -v -s decisions
python3 decisions/register.py check --base "$earlier_method_sha" --verify-implementations
```

For concurrent branches, take the current main event sequence, replay your event and rebuild the projection. To repair an interrupted local projection write, run `python3 decisions/register.py build`. The PR check compares every published event byte with its base.
