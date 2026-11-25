# Authored T4 mappings and scientific acceptance

The [machine-readable contract](agent-t4-contract.json) defines `ruralscan.agent-t4-contract.v1`. It implements the adopted agent-led T4 method without changing historical T4 records. A finding Keep decision is not approval of a numerical curve. The accepted-output format is separate from the historical T4 CSV manifest. [Schema change record](https://github.com/RuralScan/method/issues/113).

## Proposal and input boundary

One proposal covers one current suitability family. Frozen inputs contain the practice's candidate findings, source identities, reviewer decisions, definition hashes and exact skill. The agent records model, full prompt, exposed settings, every candidate's disposition and originating study, compatibility, dependence, uncertainty and comparison with prior mappings.

Each mapping records its stable ID; practice and family; variable and dataset; spatial context/support; representation; evidence IDs; separate variable-use, direction, calibration, precision and mechanism rationales; binding, transfer, exclusion and weight explanations; and calibrated or held status. Each supporting finding needs an applicability explanation. Broader evidence stays visible; sibling or unresolved historical family scope is not silently reassigned.

The first interface supports piecewise profiles with explicit tails, thresholds with explicit endpoint operators, ranked classes, and qualitative interpretations. Missing values remain unknown. Boundary examples cover endpoints and both sides, missing input and unknown classes. Validation checks that examples reproduce the authored representation; scientific review checks whether that representation is defensible. Other response forms need a reviewed contract extension.

Source observations and model importance do not supply failure limits or criterion weights. Recorded calibration, transfer and applicability holds remain binding. Crop admission follows the pinned policy; species envelopes and soft operational evidence do not set structural suitability. An unresolved dataset binding can remain a qualitative/calibration-held mapping; it cannot enter a calibrated package. Applicable preferred bindings are checked against the pinned BIND rows; no silent substitution for a required local upload.

## Human acceptance and replay

An original human issue names the exact proposal hash and full Git revision, with scientific reasons and scope. The evidence route authenticates reviewer identity and eligibility, rejects edited or wrong-lane receipts, and records an append-only event. Validation or merging software alone does not grant scientific approval. Agents must not create human acceptance on reviewers' behalf.

Replacement and withdrawal name exact prior mapping hashes. The fingerprint excludes only historical editorial justification; it retains all scientific fields and the complete rationale of an accepted AI mapping. A new mapping ID cannot bypass replacement review for the same scientific cell. Reversal uses a new proposal restoring earlier accepted values, not a history rewrite. Changed evidence, sources, reviews, skills or definitions make input packets stale. Later scientific holds and rating challenges block packaging of the challenged output.

## Package boundary

`ruralscan.accepted-t4.v1` contains exact accepted mappings, explicit withdrawals, input/proposal/row hashes and receipt provenance. Historical values never fill missing accepted outputs. Held or stale active mappings block packaging.

This is a partial mapping package, not a complete recipe or T4_RUN policy. It declares `runtime_implemented: false`. Context selection, spatial execution and whole-recipe weights require separate implementation and approval. Source importance, evidence counts and historical weights do not supply missing runtime settings.

Method owns this contract. Evidence owns preparation, validation, staging, receipt replay and packaging. The contract and companion implementation must both be approved before production use. An existing accepted proposal must not be silently reinterpreted under a different contract. Reproducibility means replaying exact accepted bytes, not rerunning an AI model and assuming an identical scientific answer.

[Evidence implementation for review](https://github.com/RuralScan/evidence/pull/110) · [Versioned operating guide](https://github.com/RuralScan/evidence/blob/a0c0b3049a53d424a71a54b6812c6bd916586cf2/workflows/t4_synthesis/README.md). The evidence PR must be merged after this contract is approved; its fixture tests are not human scientific acceptance.
