# Confidence lookups for reuse

This reference edition exposes the exact Rural Scan confidence derivation and display
mapping. Both files have immutable origins and SHA-256 digests in
[manifest.json](manifest.json). Cite the full method Git commit containing this manifest
and the selected file hash. The manifest format version describes its shape; the commit
identifies the content edition.

| File | Purpose |
|---|---|
| [ipcc_confidence_matrix.csv](ipcc_confidence_matrix.csv) | Nine evidence-level × agreement-level combinations mapped to five confidence labels. Byte-identical to the archived compiler input. |
| [scorecard_confidence_badge.csv](../lookups/scorecard_confidence_badge.csv) | Five confidence labels mapped to three display badges. Already part of the method compiler release; the reference manifest pins that same file. |

The first table is **Rural Scan's discrete operational convention using IPCC confidence
language**, not an IPCC-issued numeric standard, probability or independent validation.
The files are original project configuration distributed under the repository's
[MIT licence](../../LICENSE); no external figure or report is reproduced here. The badge
is a display reduction: keep the original five-level confidence in stored data.
Evidence quantity/quality and agreement must first be assessed using the
[effect-synthesis method](../../methodology-reference/content/effect-synthesis.md).
These two lookups alone do not reproduce its evidence weighting, caps or transfer checks.

## Verify an edition

From the root of the chosen method checkout:

```python
import hashlib
import json
from pathlib import Path

manifest = json.loads(Path("configuration/reference/manifest.json").read_text())
archive = json.loads(Path("configuration/archive.json").read_text())
release = json.loads(Path("configuration/release.json").read_text())
for name, entry in manifest["files"].items():
    actual = hashlib.sha256(Path(name).read_bytes()).hexdigest()
    assert actual == entry["sha256"], name
assert manifest["files"]["configuration/reference/ipcc_confidence_matrix.csv"]["sha256"] == archive["lookups"]["ipcc_confidence_matrix"]
assert manifest["files"]["configuration/lookups/scorecard_confidence_badge.csv"]["sha256"] == release["files"]["schema/lookups/scorecard_confidence_badge.csv"]["sha256"]
print("Verified confidence matrix and badge lookup")
```

This publication does not adopt a new compiler policy or change any evidence pin.
Existing evidence editions continue to consume the exact hashes in their method pin.
For standalone downloads, use each `origin` repository, full revision and path in the
manifest, then verify SHA-256 before use. Avoid floating `main` URLs in saved analyses.

## Other archived inputs

The remaining inputs named in [archive.json](../archive.json) are available at their
exact public upstream revision. Anonymous downloads and all four archival hashes were
verified on 20 November 2026. These are historical inputs, not assertions that the data
are current or transferable. Download bytes must match the listed SHA-256.

| Input | Immutable download | SHA-256 |
|---|---|---|
| `t4_numeric_compilation_policy` | [CSV](https://raw.githubusercontent.com/CIAT/nbs_ruralscan/e43c42bd581dba791ce1f1697b6b41952ab0cfe3/schema/lookups/t4_numeric_compilation_policy.csv) · [source](https://github.com/CIAT/nbs_ruralscan/blob/e43c42bd581dba791ce1f1697b6b41952ab0cfe3/schema/lookups/t4_numeric_compilation_policy.csv) | `0613e337b0bb4d98a507f66d8c1ffe1080d94de0da3a18bc495eab4d8cd6bc73` |
| `wb_income_groups` | [CSV](https://raw.githubusercontent.com/CIAT/nbs_ruralscan/e43c42bd581dba791ce1f1697b6b41952ab0cfe3/schema/lookups/wb_income_groups.csv) · [source](https://github.com/CIAT/nbs_ruralscan/blob/e43c42bd581dba791ce1f1697b6b41952ab0cfe3/schema/lookups/wb_income_groups.csv) | `286c52a26a23daa78009907ea32c9a359b5042b38e67492218bc4eceb751d662` |
| `searched_no_evidence` | [CSV](https://raw.githubusercontent.com/CIAT/nbs_ruralscan/e43c42bd581dba791ce1f1697b6b41952ab0cfe3/schema/lookups/searched_no_evidence.csv) · [source](https://github.com/CIAT/nbs_ruralscan/blob/e43c42bd581dba791ce1f1697b6b41952ab0cfe3/schema/lookups/searched_no_evidence.csv) | `37d30ba30352f4d108c7afedacfa038ab3a7d1e6c3ef1caebf0d45601b37a9c8` |

The T4 table contains finding-specific adjudications alongside reusable conventions;
use the [historical compiler explanation](../../methodology-reference/content/t4-legacy-compiler.md#the-numeric-compilation-policy)
and retain every hold. The income-group table is an archived classification, not a live
World Bank feed. Searched-with-no-evidence rows are recorded search outcomes, not zero
NbS effects. This index does not relocate ownership or clear pending local redistribution
of those tables.

[Current T4 synthesis](../../methodology-reference/content/suitability-synthesis.md) ·
[T3/T6 synthesis](../../methodology-reference/content/effect-synthesis.md) ·
[T5 characterisation](../../methodology-reference/content/m3-characterisation.md) ·
[Dixon-to-EO crosswalk](https://github.com/CIAT/nbs_ruralscan/blob/e43c42bd581dba791ce1f1697b6b41952ab0cfe3/schema/registers/FS_DIXON_CROSSWALK.md)
