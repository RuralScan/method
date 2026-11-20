# Synthesis transition audit — 20 November 2026

The documented decision and implementation did not cover the same boundary. New T4
synthesis was described as agent-led, but current evidence publication still called
the historical T4 algorithm. T3/T6 scientific scoring remained deterministic, with
AI-authored explanations downstream.

## Decision trail

- [Method #64](https://github.com/RuralScan/method/issues/64) and
  `t4_agent_synthesis` in `decisions/events.csv` explicitly adopted agent-led T4
  proposals, retained historical reproduction, and left T3/T6/T6E algorithms unchanged.
- The reviewed originating chat, *Document T4 evidence guidance*, explicitly asked
  for an AI skill to construct T4. No broader T3/T6 transition decision was found in
  that chat, the method ledger, the migrated scientific ledger or the issues inspected.
  This is a limit of the reviewed record, not evidence that a broader intention never existed.
- The [20 November clarification](https://github.com/RuralScan/method/issues/85#issuecomment-7049325204)
  states that T3/T6 were expected to be AI-led too and requires removal of the
  historical T4 compiler from current documentation and code. It supersedes keeping
  T4 compilation available as a supported reproduction workflow.

## Where the boundary differed

| Surface inspected | Behaviour found | Retirement or remaining work |
|---|---|---|
| Method suitability chapter | Described an agent workflow; admitted no validated production route | Retain that boundary; remove the compiler chapter and numeric-policy interface |
| Evidence `workflows/submissions/queue_view.py` | Called `t4_build.synthesise` and `write_recipe` on every candidate build | Remove those calls; retain checksum-pinned T4 baseline rows with explicit historical status |
| Evidence release and seed checks; method cookbook builder | Exposed whole-recipe rebuilds that executed T4 synthesis | Remove rebuild entrypoints; verify existing release stores read-only |
| Older dashboard reference | Exposed numeric compilation policy and linked T4 rows to the old protocol | Remove policy page, label historical rows and link current agent guidance |
| Archived `source-command-t4-synthesise` skill | Still ran `scripts/synthesise-recipe.py` | Obsolete execution recipe; current docs must not recommend its commands |
| Effect chapter, `t3t6_build.py`, `cell_synthesis.py` | Deterministic eligibility, influence, direction/strength and confidence rules | Still implemented; an AI-led scientific proposal/acceptance route is missing |
| Archived T3/T6 synthesis skill | Instructed agents to run the engine and never re-judge a class by hand | Conflicts with the intended AI-led target; AI prose alone does not resolve this |
| Effect helpers | Import numerical and lineage utilities from the old `synthesis.py` module | Shared helper dependency remains for effects; it is not a new T4 synthesis call |
| Runtime | Evaluates accepted mappings and checks bundle provenance | Retain deterministic evaluation; it is distinct from scientific synthesis |

The inspected evidence baseline is
[`97dd21060d931b16464155d770c7eb7dd71c385a`](https://github.com/RuralScan/evidence/tree/97dd21060d931b16464155d770c7eb7dd71c385a).
It contains 54 T4 rows across six practices, including an empty mangrove T4 table.
Retaining these records does not approve them against changed evidence or make them
AI-derived. New, corrected or dropped evidence must not silently regenerate their values.
Historical code and skills remain accessible in immutable upstream editions; current
workflow retirement does not rewrite those editions or their evidence/review history.

## Outstanding agent implementation

T4 still needs a production versioned skill, structured proposal, complete candidate
accounting, scientific acceptance record and validation/packaging adapter. T3/T6 need
an equivalent contract covering cell scope, direction, strength, confidence,
applicability, dependent observations, mixed evidence, holds and uncertainty. T6E's
boundary must also be made explicit rather than inferred from shared effect code.

The accepted decision and representation should be replayable. A fresh model run
is not the reproducibility guarantee. Schema checks, provenance checks, numeric
consistency and runtime execution remain deterministic. Historical outputs should
not be overwritten or relabelled as agent-generated during this transition.

## Follow-up implementation: AI-led T3/T6

Pete explicitly authorised the new boundary in
[issue #85](https://github.com/RuralScan/method/issues/85#issuecomment-7052114229).
Decision `t3t6_agent_synthesis` now records AI scientific authoring and exact-output
acceptance, superseding provisional-setter eligibility for new scientific outputs.

Evidence now provides a versioned native agent skill, generated input snapshots,
complete candidate dispositions, authored CSV proposals, authenticated reviewer
receipts, append-only acceptance and accepted-only packaging. Publication no longer
calls T3/T6 scoring or the shared T4 helpers. Held/stale outputs block release;
withdrawals retain provenance. Runtime's `AcceptedEffects` verifies a trusted manifest
and returns authored values unchanged. The old local skill and slash command redirect
to the evidence workflow; synthesis and automatic fragility CLIs refuse execution.

Existing analytical tables are unchanged and remain historical. No real scientific
proposal has been accepted by this software change. A first bounded AI synthesis and
reviewed release remain operational work. T4's production agent adapter remains
outstanding; T6E is explicitly frozen pending its own contract. Earlier findings above
are the audit history, not instructions to run the retired algorithms.
