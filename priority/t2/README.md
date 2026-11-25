# T2: current climate-variable registry

[T2 variables](variables.csv) · [Field schema](schema.json) · [Migration trace](migration.json) · [Machine-readable manifest](manifest.json)

T2 now registers individual climate-related variables. It does not calculate a Climate Risk Index. Its current CSV has no simplified/advanced modes, normalization formulas or default weights. All eleven existing variable IDs remain resolvable. The source CSV in `data-model/configuration/T2_climate_risk.csv` stays byte-for-byte historical, for older editions and consumers.

This migration registers definitions, not accepted classifications. Every entry is **blocked for analytical use** until its quantity, context, dataset binding and classification are resolved. The role and concern columns make the proposed routing explicit for review of this migration. They do not activate a scoring layer. No thresholds, source reviews or runtime package are created.

## Read the fields

`variable_id` and `variable` preserve identity. `label`, `quantity` and `temporal_statistic` describe the intended measurement; `unit` may be blank where the quantity is unresolved. `scenario_type` preserves the recorded scenario. `reference_period` and `context_id` stay blank unless established; a scenario name alone cannot fill them.

`candidate_dataset_id` retains the old dataset pointer for audit. It is **not a verified binding**. `dataset_id` is reserved for a verified, context-appropriate T1/BIND resolution and is empty throughout this initial migration. In particular, a precipitation proxy is not flood depth, a bioclim layer is not a future SPEI series, and a runoff label does not establish a runoff product. `binding_status=unverified` exposes that distinction.

`mcda_role` separates candidate priorities, descriptors and the investment-risk screen. Population and cropland exposure remain descriptive. The two unresolved soil sensitivity entries remain context descriptors rather than reviving a vulnerability index. Road access is an operational investment-risk/context input, not another additive climate-need term. A future change in these roles needs explicit scientific review.

`concern_id` identifies possible overlap with T5 or another scenario. It is not a claim that different physical quantities are equivalent. Choose a valid representative for a concern in the declared scenario; do not add baseline and future drought as two independent priorities, or rainfall and runoff as independently proven flood layers. T5 literature/classification work owns the subsequent cross-table reconciliation.

`classification_id` and `classification_version` will identify an exact accepted classification through the shared priority workflow. Both are empty and `classification_status=not_assessed` in this migration. The catalogue introduced by [method #100](https://github.com/RuralScan/method/pull/100) is now present on main, but remains a proposed acceptance/release contract with zero accepted calibrations; it supplies no defaults here. Finding review, classification acceptance and user weights remain separate.

`readiness=blocked` and `blockers` explain what prevents use. These are implementation readiness flags, **not human hold/reject votes**. The current schema deliberately has no ready state. A later reviewed contract must implement and test the acceptance/binding gate before it can advertise ready inputs.

## Migration and reproducibility

[Issue #101](https://github.com/RuralScan/method/issues/101) records this schema change. `migration.json` pins the full source revision, file hash and original rows, and accounts for every old field. Removed composite-index controls remain available there and in the historical CSV. No evidence IDs or reviews are moved or deleted. The migration does not widen the old compiler's `configuration/contract.json` or change evidence's existing configuration pin.

CSV is authoritative. Regenerate the descriptive manifest after an intentional CSV/schema change:

```sh
python3 priority/t2/registry.py build
python3 priority/t2/registry.py check
python3 -m unittest discover -s priority/t2 -p 'test_*.py'
```

The manifest is a versioned registry inventory, **not an accepted calibration or runtime release**. It provides formats, units/field definitions, source revision, hashes and status for software and AI consumers. It always reports zero runnable variables. Consumers must fail closed on unresolved records; they cannot infer eligibility from membership in T2.

## What remains

Resolve quantity and dataset inconsistencies, record supporting evidence through the reviewed classification route, settle context/period and accept exact rule versions. Only then can the runtime owner adopt an independently pinned package. Runtime code, T5, the evidence register and historical publication pins are unchanged by this registry migration.
