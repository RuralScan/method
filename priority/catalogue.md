# Priority classification catalogue and release proposal

Status: **proposed storage and review contract; no accepted calibration release**. The adopted scoring method remains [priority v1.0.0](../data-model/priority-contract.json). This proposal adds audit, evidence and review machinery without changing class scores, weights, endpoints or supported methods.

## Record ownership and smallest store

| Record | Owner and location | Meaning |
|---|---|---|
| Thirty-row semantic/binding audit | Method: `priority/audit.json`, readable `audit.md` | Exact historical T2/T5 rows and T1/VONT/BIND joins; proposed concerns and blockers |
| Source observations | Evidence: `workflows/priority_classification/packets/` at full Git SHA | Source identity, artefact hash, locator, reported values and interpretation limits; currently unreviewed staging |
| Classification proposal | Method: `priority/proposals/<id>-<version>.json` | Exact scientific quantity, context, binding, rule, uncertainty and dependency hashes |
| Scientific disposition | Existing method `decisions/events.csv` → `current.csv` | Protected human PR decision, not a finding vote or author assertion |
| Review inventory | Method: `priority/release.json` | Byte/proposal hashes, source lock and zero accepted runtime rules; explicitly not a runtime package |
| Accepted package (gated) | Method: `priority/releases/<sha256>.json`, pinned by Git SHA | Only individually accepted, complete rules; append-only, never overwrite |
| Run choices | Runtime analysis manifest | Representative concerns, scenario, context, aligned input hashes and user weights |

The new JSON sidecar leaves historical CSV columns intact. This is not an addition to the old compiler-definition manifest: that manifest enforces an unchanged CSV inventory, and evidence's adopter explicitly allows only five mirrored registers and named lookups. Widening it would silently change two consumer contracts. Proposed priority release metadata is a separate, typed, content-addressed interface. Before activation, accept `priority_catalogue_release` and complete source review and binding verification. The separate evidence adoption lock/receipt is implemented in the companion evidence change. No existing compiler pin changes here.

## Exact review decisions requested

1. **Storage and release:** adopt the sidecar ownership above; reuse method decisions for classifications; require exact proposal/context hashes plus canonically reviewed source findings and verified bindings before a runtime release. Keep existing evidence compiler adoption unchanged.
2. **Drought:** accept, revise or hold `spei12_event` as an event-level reverse-direction candidate only. Copernicus PDF page 6 Table 2 supports cuts −2, −1.5, −1 with upper-inclusive raw intervals. Mapping dry classes to high/medium/low and the remaining observations to none of this dry-event signal is the proposed interpretation. This does not approve chronic aridity, long-term drought-frequency thresholds, a CSIC product binding or any country default. `drought_climatology` keeps all cuts null pending its statistic and period.
3. **Water stress:** recommended initial disposition is hold numerical classification while retaining the provider's five categories and special arid status for description. An alternative proposal would add a three-class *threshold* method, low/medium/high at 0.2 and 0.4 with no invented none. That would require a reviewed contract extension, endpoint policy and arid handling. It is **not implemented**. A four-class [0, 0.2, 0.4] interpretation would reserve none for verified zero ratio; that too is a policy choice, not a WRI conclusion. Current `cuts` remain null.
4. **IPLC and carbon:** keep classifications held. Propose a mapped-presence/unknown safeguard overlay for IPLC rather than numerical severity. Carbon requires an additional-change/potential product and management counterfactual; GSOCmap stock cannot supply it. Historical T5 roles are not silently rewritten.

All concern groups in the audit are proposals. Shared identity identifies possible double counting; it does not make temperature and heat-day frequency, rainfall and inundation, or road distance and travel time interchangeable. Baseline and future cases remain alternatives. The four T5 descriptors remain outside scoring. National-only GII and employment cannot become within-country differentiation by rasterization.

## Validation and lifecycle

`python3 priority/catalogue.py check --evidence-repo /path/to/evidence --base origin/main`

The checker accounts for every legacy row, locks source and binding dependencies, checks rule structure, class scores, endpoints, finite ordered cuts, domain, conversion metadata and immutable published proposal versions. It verifies exact evidence packet bytes using Git. The scalar classifier is a review-test oracle only; no raster or notebook implementation is introduced.

Lifecycle uses existing method decisions rather than a parallel approval ledger:

- Inventoried/evidence-needed: audit records and blockers; no rule acceptance implied.
- Proposed/in review: a versioned proposal plus `propose` method event, reviewed in a PR. `author_assessment=held` is an author recommendation, not a human disposition.
- Human hold: `park` event with rationale. Reopen with `reopen`.
- Human accept/reject: a `decide` event under the proposal's `decision_id`. Acceptance must use exactly `Accept priority proposal sha256:<canonical-content-hash> for context sha256:<context-hash>.` A rejection uses an explicit rejection outcome and never passes the release gate.
- Superseded: a new version and decision code, linked by `supersedes`; retain the old proposal and event chain. Existing method register retry/prefix checks preserve history.

Canonical content is UTF-8 JSON, sorted keys, no ASCII escaping, compact separators, one final newline and no NaN/infinity. Hash the entire proposal, including bindings, source references, rationale and blockers. The manifest also records the original file-byte hash. Any semantic edit needs a successor version and fresh acceptance; a previous decision cannot approve changed content. Relevant dependency changes invalidate the current candidate until re-audited. Immutable older pins remain reproducible.

Format validation does not authenticate human approval. GitHub's protected, reviewed method PR and merged main revision establish authority. Agents must not record `decide` on behalf of a reviewer. This branch records proposal events only. Review of this PR's machinery does not accept the individual classifications.

## Immutable release and adoption route

`catalogue.py` still produces a **review manifest only**, always with `accepted_rules=[]`. `package.py` adds private accepted-package preparation and replay; it cannot merge or publish. All real candidates remain blocked. Tests use synthetic decisions and never create project approvals.

Storage acceptance requires the exact `ruling` text: `Accept priority catalogue sidecar storage and release contract v1.` A decided rejection cannot pass. Each classification requires the exact proposal/context acceptance above. The cited method PR must be human-merged to main, contain that ruling, and introduce it relative to its first parent. An unrelated later merge cannot authenticate an older decision.

Binding verification lives in immutable `priority/binding-verifications/<binding-sha256>-<context-sha256>.json`. Required fields: `format=ruralscan.priority-binding-verification.v1`, `binding_sha256`, `context_sha256`, `variables`, `binding_ids`, `checks`, `evidence` (URL and locator), and `decision_id`. Checks record observations for asset identity, units/conversion, nodata/domain, spatial support, temporal statistic, scenario and context resolution. Exact acceptance is `Accept priority binding verification sha256:<record-hash>.` The package gate resolves those BIND IDs to the rule's variables, T1 dataset and field; requires all five T1/T2/T5/VONT/BIND input hashes; and rejects changed inputs or decisions. Human verification remains necessary for spatial and scientific fitness.

Source references use evidence-owned `psrc_<hash>` and `pfind_<hash>` identities. The packet, source acquisition and finding bytes must agree. Findings must be kept at both the selected evidence revision and the current inspected main base. A later hold, rejection, conflict or reopening blocks new preparation/adoption. No self-asserted `review_state=kept` can satisfy this gate.

```sh
python3 priority/package.py prepare --method-revision FULL_MERGED_SHA --method-base FULL_MAIN_SHA \
  --evidence-repo /path/to/evidence --evidence-base FULL_EVIDENCE_MAIN_SHA \
  --proposal priority/proposals/example-0.2.0.json --out /private/new-release
```

The command needs authenticated read access through `gh` and the evidence source-check dependencies. Use trusted repository checkouts and explicit current main bases. Preparing an artifact does not publish it: publication requires a separate reviewed method PR adding the generated bytes under `priority/releases/`. Evidence adoption executes the producer from that merged release commit and records its independent full pin. The package contains no self-referential Git SHA.

Tests exercise complete synthetic package construction/replay, source gating, exact approval provenance, tampering and stale definitions. Evidence tests separately exercise actual acquisition and source-review resolution. There is no real accepted package to test or adopt yet.

The gated production route follows these requirements:

1. Read exact merged method and evidence revisions; verify they belong to the approved repository histories. Verify source registration, kept finding receipts and bindings against their pinned artefacts, not self-asserted strings in a proposal.
2. Require the storage decision and each classification decision to be decided at that method revision, with exact acceptance text, matching context and human protected-PR provenance. Reject held/rejected/superseded states, unresolved blockers, missing ontology or binding, descriptors and investment-risk roles.
3. Package the original accepted proposal bytes, dependency manifest, source/finding receipt hashes and decision references. Include the priority-contract digest. Do not include default user weights. Name the package by SHA-256 of canonical payload; a retry is identical, never another decision.
4. Consumer pins `{repository, revision, path, sha256}`. A branch name or mutable `latest` is insufficient. Do not place the package's own Git SHA inside its contents; that would be circular.
5. Evidence adopts only through a separate protected PR, verifying the package and adding a receipt. Its existing compiler pin remains independent. Stale or unresolvable source/binding inputs fail closed. No priority rule is routed through T4/effect votes.
6. Runtime validates exact binding, raw units, spatial support, scenario, period and masks before classification. One explicitly chosen representative per concern; repeated concern IDs fail. Missing positive-weight inputs give unknown; descriptors and M2b cannot enter the stack.
7. Roll back by selecting a previously accepted immutable package and recording a new adoption receipt. Keep both packages and all decisions. Historical reproduction is distinct from selecting a superseded rule for new production.

The package gate is stricter than the pure `eligible()` structural predicate. It verifies merged decision provenance and source acquisition/review references; it does not replace human scientific or spatial fitness review. Multiple rules may share a concern in the catalogue as alternatives; runtime must select only one per concern. No file in this change is an accepted release.

## Bounded evidence and conformance

Five source packets support five rule proposals. Drought event severity is the only populated cutoff candidate; drought climatology, Aqueduct mapping, IPLC presence and carbon potential keep unverified cuts empty. Sources are pinned in [evidence.lock.json](evidence.lock.json), with limits and precise locators. The PDFs were inspected visually. Copernicus's current PDF is dated 2026, although search results returned an older edition; the saved artefact hash resolves that ambiguity.

[Conformance vectors](test-vectors.json) cover reverse/forward endpoints, true zero, unknown, held rules, domains, units, fixed weights, mask states, duplicate concerns and scenario incompatibility. They are an integration specification for runtime [issue #12](https://github.com/RuralScan/runtime/issues/12), not evidence of runtime adoption. The draft evaluator in [PR #11](https://github.com/RuralScan/runtime/pull/11) remains unmerged.
