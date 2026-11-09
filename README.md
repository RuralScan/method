# Rural Scan methodology

Rural Scan scopes where nature-based solutions could fit rural landscapes, which climate risks matter, and how people, production systems and development priorities overlap those opportunities.

It supports early investment scoping. It does not replace feasibility studies, engineering design, ecosystem-service modelling or full cost-benefit analysis.

**Status: draft technical reference.** This repository contains an incomplete definition baseline, not a runnable application or a complete analytical release. Scientific limitations and unresolved dependencies are listed in the [baseline reference](data-model/baseline.md).

## Start here

- [Understand the approach](handbook/start-here.md): seven modules and the evidence-to-rule chain.
- [Work through the Haiti notebook and prepare a scoping brief](handbook/implement-a-scan.md).
- [Read the data model](data-model/spec.md): fields, controlled vocabularies, table structure and configuration.
- [Inspect the baseline](data-model/baseline.md): source versions, dependencies and known limitations.
- [Run the implementation](https://github.com/RuralScan/runtime): data access, computation and reproducible notebooks.
- [Explore the evidence workflow](https://github.com/RuralScan/evidence): discovery, extraction, review and compilation.

## How the repositories fit together

`method` contains concepts, schema definitions, analytical configuration, recipe guidance and visual identity. `evidence` contains source records, claims and the workflows that compile candidate tables. `runtime` contains data access, spatial computation and executable examples.

Definitions feed evidence compilation. Runtime consumes immutable analytical releases with explicit compatibility and input hashes. A draft configuration or reviewed claim does not by itself establish an executable or transferable analytical rule.

The [licence](LICENSE) covers the included original material. Dataset and publication terms remain with their sources.
