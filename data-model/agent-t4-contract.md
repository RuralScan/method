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

Method owns this contract. Evidence owns preparation, validation, staging, receipt replay and packaging. The proposal, validation, human-acceptance and packaging interface is implemented; scientific acceptance of each mapping and spatial runtime integration remain separate. An existing accepted proposal must not be silently reinterpreted under a different contract. Reproducibility means replaying exact accepted bytes, not rerunning an AI model and assuming an identical scientific answer.

[Versioned operating guide](https://github.com/RuralScan/evidence/blob/94a5b1c5e2bea65c79161388e78aecb20714cd66/workflows/t4_synthesis/README.md). Fixture tests verify the software route; they are not human scientific acceptance.

## Version 1.1: exact composite and precomputed profiles

Version 1.1 extends the representation contract. It does not approve the climate or mangrove relationships, adopt new variable/dataset definitions, or implement a raster consumer. The existing CSV mapping columns and authenticated scientific-acceptance route remain unchanged.

Scalar `logistic` and `log_logistic` forms declare increasing `x20` and `x80` anchors in addition to the existing `unit` and `missing: null`. The logistic assigns membership 0.20 and 0.80 at those anchors. The log-logistic operates on positive input, preserves a zero-valued dry tail at input zero, and rejects negatives. Neither form estimates a success probability. No implicit clipping or fitted parameters are introduced.

`composite_scoping` declares its input quantities, units, validity ranges and dataset IDs; an exact scope list; typed smooth-function leaves and nested minimum operators; an optional temperature-only monthly derivation; named component screens; and missing/conditional semantics. Its parameter object is the complete profile, including `type`, `unit` and `missing`. Screens use explicit `lt/le/gt/ge` endpoint conventions. Scores and screens are distinct outputs. Composite score cutoffs and criterion weights are not inferred.

The declared thermal derivation reconstructs a no-leap 365-day climatology by periodic linear interpolation at month centres. It counts all days meeting the explicit temperature threshold and averages those days, without water or snow eligibility. Complete zero thermal days is distinct from missing data. Callers cannot inject precomputed derived values as replacements for the specified derivation. Raw storage decoding and spatial data acquisition belong to a separately reviewed binding/adapter.

`precomputed_unit_index` preserves a native score in [0,1] conditional on positive modelled source area. Score and area must refer to the same dataset release. It retains separate unknown, invalid, zero-area and excluded states. Source area in km² converts to hectares by 100. Whole units retain source estimated hectares; partial units have unresolved allocation bounds from zero to those hectares, with no polygon-area proration. Missing source coverage cannot yield complete finite AOI bounds. Unit identity and geometry status are required; deduplication does not itself establish sound topology. A score-support polygon is not an opportunity footprint.

All raw and derived profile input quantities must resolve against adopted VONT, T1 and preferred BIND definitions before an official mapping can validate. Subpractice scope must resolve to the proposal's current family; a candidate covering several practices is split into separate official family proposals. Existing evidence eligibility, reviewed claim scope, exact replacement fingerprints and authenticated human acceptance remain mandatory. Provenance-only source links cannot substitute for Evidence Register units.

## Pending override catalogue

The evidence repository keeps an authoritative pending override CSV with generated typed JSON. A candidate declares pending status and `activate=false`, an exact profile, structured rationale/mechanism/source-relationship/analyst-choice/transfer/binding/area/replacement/approval explanations, and edition-linked source references with locators. These are review records, not scientific acceptance events.

The preparation interface exposes applicable candidates in the frozen input packet so the synthesis agent can inspect their intended relationships and scope. Candidate changes make the packet stale. Pending records never change accepted mappings or opportunity area automatically. The same metadata can support dashboard explanations without conflating source admission, source-claim review, relationship approval, implementation and runtime activation.

Reference evaluation is available for reproducing declared examples. It carries no production activation. The accepted package continues to declare `runtime_implemented: false`; downstream integration must preserve component screens, unknown/conditional states, scope, separate area accounting and independent host/legal gates.
