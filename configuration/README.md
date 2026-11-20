# Method definitions and accepted scientific outputs

Method owns definitions, vocabularies and constraints. Evidence pins their exact Git
revision and hashes. New T3/T6 scientific synthesis follows
[decision t3t6_agent_synthesis](../decisions/current.csv) and the
[agent effects contract](../data-model/agent-effects-contract.json).
AI interprets evidence and authors all scientific judgments. Code validates types,
references, provenance and acceptance, then packages exact authored outputs.

`release.json` retains its existing format identifier for compatibility with pinned
editions. Its historical scoring lookups are reference context, not an active scoring
algorithm. Changing a definition does not re-rate evidence. It requires fresh reviewed
proposals where it changes their input packet. The separate agent contract is pinned
by evidence's `workflows/synthesis/contract.lock.json`.

Editable definitions live in `data-model/configuration/`; the release inventory and
hash checks remain enforced. Evidence's VONT, FAM, BIND, XW and BANDS copies are pinned
mirrors verified against the selected method revision, never a moving branch.

Archived confidence matrices, weighting factors and former T4 inputs remain only for
understanding immutable historical editions. The T4 compiler and automatic T3/T6
scoring are retired from supported scientific production. T6E remains a historical
snapshot pending a separately accepted economic synthesis workflow.

[Reference material](reference/README.md) · [Effect workflow](../methodology-reference/content/effect-synthesis.md)
