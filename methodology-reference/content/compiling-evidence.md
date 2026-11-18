---
title: Compiling evidence into rule tables
slug: compiling-evidence
summary: Know where compiling sits between reviewed findings and the rule tables a scan reads, how it is run today, and what a planned move to an AI agent would and would not change.
sources:
  - methodology/T4_generation_method.md
  - methodology/T3_T6_generation_method.md
  - src/nbs_ruralscan/recipe/synthesis.py
  - src/nbs_ruralscan/recipe/cell_synthesis.py
---

## What compiling is

Compiling turns reviewed findings into the rows of the rule tables that a scan reads. A finding is one statement taken from one source and held in [[table:EV]]. A rule-table row is what a scan uses: a suitability mapping in [[table:T4]], a hazard response in [[table:T3]], a scorecard effect in [[table:T6]] or an indicative cost profile in [[table:T6E]].

Compiling comes after review and before any scan. It reads findings and never writes or alters them, so the record of what the sources say stays separate from the judgement of how to combine it. [src: methodology/T4_generation_method.md] [src: methodology/T3_T6_generation_method.md]

## How it is run today

Fixed compiler code applies the rules set out in the next three chapters: [[ch:suitability-synthesis]], [[ch:effect-synthesis]] and [[ch:cost-profiles]]. The same findings always give the same rows. Every row in this edition was compiled this way. [src: src/nbs_ruralscan/recipe/synthesis.py] [src: src/nbs_ruralscan/recipe/cell_synthesis.py]

## Planned change: compiling by an AI agent

This section describes a plan. Nothing in it is in use, and no row in this edition was produced by it.

The plan is to move compiling out of the evidence repository. An AI agent, working to a written skill, would read the reviewed findings held there and produce the rule tables that the runtime reads. The evidence repository would then hold findings, sources, searches and review records, and nothing derived from them.

Three rules of the present method carry over, because they do not depend on who or what does the compiling. Every row names the findings it rests on. A calibration that reviewers have held, or have not recorded, is never turned into a score. People review compiled rows before a scan uses them.

The following are not yet decided:

- how the agent's rows are checked against the rules in the next three chapters, and whether the same findings must always give the same rows;
- how its rows are reviewed and approved;
- when it replaces the present compiler;
- [how several findings from one source should count](https://github.com/RuralScan/method/issues/44), in display and in compiling.

Until this section is replaced, the next three chapters describe compiling as it is done.

## Assumptions and limits

This chapter states a direction, not a tested route. The agent's skill is not written, so it cannot be audited or re-implemented from this methodology yet. A reader who needs to reproduce a row should use the next three chapters and the present compiler.

## Where this is configured

Today the rules sit in the lookups and registers named in the next three chapters, and the compiled rows sit in [[table:T4]], [[table:T3]], [[table:T6]] and [[table:T6E]]. The agent's skill has no published location yet.
