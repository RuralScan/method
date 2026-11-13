# Rural Scan methodology

Rural Scan scopes where nature-based solutions could fit rural landscapes, which climate risks matter, and how people, production systems and development priorities overlap those opportunities.

It supports early investment scoping. It does not replace feasibility studies, engineering design, ecosystem-service modelling or full cost-benefit analysis.

**Status: draft technical reference.** This repository contains an incomplete definition baseline, not a runnable application or a complete analytical release. Scientific limitations and unresolved dependencies are listed in the [baseline reference](data-model/baseline.md).

## Start here

[Open the live evidence dashboard](https://ruralscan.github.io/method/) to inspect suitability relationships, hazard ratings and their sources. Open [T3 hazard review](https://ruralscan.github.io/method/#review-t3) or [T4 suitability review](https://ruralscan.github.io/method/#review-t4) for finding cards. The version selector includes November 11–13 design drafts. [Build and verify a dashboard draft](dashboard/README.md).

- [Understand the approach](handbook/start-here.md): seven modules and the evidence-to-rule chain.
- Download the bench-terrace evidence tables and their field definitions from the [machine-readable evidence catalogue](https://ruralscan.github.io/method/catalog.json).
- [Choose a practice and suitability family](cookbook/README.md). Compare spatial outputs and family-level evidence counts. [Download the six-practice print edition](cookbook/rural-scan-cookbook.html).
- [Work through the Haiti notebook and prepare a scoping brief](handbook/implement-a-scan.md).
- [Read the data model](data-model/spec.md): fields, controlled vocabularies, table structure and configuration.
- [Label schema tables in figures, notebooks and printouts](design/README.md).
- [Browse all six practice definitions](data-model/configuration/recipes). [Check their source versions, dependencies and limitations](data-model/baseline.md).
- [Run the implementation](https://github.com/RuralScan/runtime): data access, computation and reproducible notebooks.
- [Open the public evidence workbook](https://github.com/RuralScan/evidence/blob/1532768de6c688e2c8eb26097eb7618848390b1d/workflows/public_workbook/README.md) to trace a compiled row to its claims and sources. Download the HTML for offline use.
- [Explore the evidence workflow](https://github.com/RuralScan/evidence): discovery, extraction, review and compilation.

## How the repositories fit together

`method` contains concepts, schema definitions, analytical configuration, recipe guidance and visual identity. `evidence` contains source records, claims and the workflows that compile candidate tables. `runtime` contains data access, spatial computation and executable examples.

Definitions feed evidence compilation. Runtime consumes immutable analytical releases with explicit compatibility and input hashes. A draft configuration or reviewed claim does not by itself establish an executable or transferable analytical rule.

The [licence](LICENSE) covers the included original material. Dataset and publication terms remain with their sources.
