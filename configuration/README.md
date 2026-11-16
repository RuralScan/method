# Release compiler configuration

RuralScan/method owns VONT (variable definitions), FAM (practice families), BIND (dataset bindings), XW (target crosswalk), BANDS (magnitude bands) and 15 policy and vocabulary tables. The [contract](contract.json) lists every compiler path, authoring file, row key and column. The [release](release.json) identifies each file by SHA-256. Its Git commit identifies the edition. The configuration vocabulary projects the archived compiler’s TOOL enums, T3 hazard types and EV use roles. A row keeps its recorded ratification or review status when released, including pending, rejected and blank statuses.

1. Propose the scientific change and record its ruling using the [method decision register](../decisions/README.md). Use an active decided code for the affected scope.
2. Branch from method main. Edit the authored CSV listed in the contract. Inspect changed keys, pending or superseded entries and effects on other tables.
3. Build the release, check it, and open a method PR. Repeat `--approve` with the corresponding decision code for each changed table. Include before/after values in the PR. Reviewers check the scope of the cited decision against the actual edits.
4. After approval, open a separate RuralScan/evidence PR to adopt the immutable release, reproduce the candidate and inspect changed recipe rows. The new method edition takes effect in evidence on merge of that adoption PR. Existing evidence editions retain their pins.

```sh
python3 configuration/release.py build --base origin/main \
  --approve schema/lookups/family_rollup_policy.csv=plantation_rollup
python3 configuration/release.py check --base origin/main
python3 -m unittest discover -v -s configuration
```

The first release imports the compiler's existing records at [CIAT e43c42bd](https://github.com/CIAT/nbs_ruralscan/tree/e43c42bd581dba791ce1f1697b6b41952ab0cfe3/schema). The worked decision `plantation_rollup` keeps plantation family rows visible and excludes their findings from the forest-restoration practice aggregate. Its clarified lookup carries the decision ID and prior content hash. The baseline hashes in the contract preserve provenance. [Method decision](../decisions/current.csv) · [Lookup](lookups/family_rollup_policy.csv)

## Ownership outside this release

| Inputs | Owner and handling |
|---|---|
| TOOL, WOCAT hazard and impact source mappings, per-finding direction exceptions | RuralScan/evidence owns the records, their source locators and supporting findings. Its reviewed configuration PR uses the selected method vocabulary. |
| Scorecard meanings, display vocabulary, comparison and pooling policies, routing and effect direction | RuralScan/method. Exact files and keys appear in the contract. |
| IPCC confidence matrix and World Bank income groups | Method reference policy. Compiler uses the archived source bytes pinned in [archive.json](archive.json) pending redistribution clearance for these external references. |
| T4 numeric compilation | Reusable conventions belong in method. Individual finding adjudications belong in evidence. Mixed archival table remains pinned until those two parts are split and reviewed. |
| Searched-with-no-evidence rows | Evidence owns the search outcome. Compiler keeps the pinned search outcomes pending a dedicated structured update. |
| Accepted T4 functions and run weights | Remain bound to their specific function fingerprints in the archived compiler. A changed function needs a separate scientific release. |
| External class legends | Method reference material. Archive references retain source and version pending redistribution review. |

The older [definition snapshot](../data-model/definition-snapshot.json) continues to resolve at its original Git revision. The five editable compiler registers are maintained in `data-model/configuration/`. Tool and source-mapping procedures are tracked in [RuralScan/evidence #40](https://github.com/RuralScan/evidence/issues/40).
