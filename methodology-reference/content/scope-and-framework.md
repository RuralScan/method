---
title: Scope and analytical framework
slug: scope-and-framework
summary: Understand the questions, module sequence and common principles of the rural scoping method.
sources:
  - AGENTS.md
  - methodology/framework.md
  - method:handbook/implement-a-scan.md
  - methodology/modules/README.md
  - methodology/modules/M1_suitability.md
  - methodology/T4_generation_method.md
  - method:handbook/read-a-suitability-recipe.md
  - schema/spec.md
  - methodology/T4_developer_contract.md
  - methodology/recipes/water_harvesting.md
---

## Purpose and the decision supported

The Rural NbS Scan helps an investment team identify where nature-based solutions (NbS) merit closer investigation in rural, agricultural and forestry landscapes. It connects four questions: where a practice could be considered, which development priorities occur there, what benefits and risks the evidence supports, and what local assessment should follow. [src: AGENTS.md §What this project is]

The output is a **scoping brief**, not a feasibility assessment. A candidate area is not a confirmed site, and an effect rating is not a forecast of project returns. Field assessment, consultation, safeguards, engineering design and cost-benefit analysis follow in feasibility work. [src: methodology/framework.md §What this framework does not do] [src: method:handbook/implement-a-scan.md §3. Build the scoping brief]

## How the analysis fits together

The modules separate suitability, development need and the evidence of a practice's response. Keeping these questions separate helps a team explain why an area or practice is shortlisted. [src: methodology/framework.md §Seven analytical modules (+ M2b project-risk addendum)]

Table: Questions and outputs of the scoping modules.

| Module | Question | Output |
|---|---|---|
| [[ch:m0-setup|M0: Setup]] | What decision, practice and area are being assessed? | Recorded scope, data choices and scenarios. |
| [[ch:m1-suitability|M1: Suitability]] | Where could the practice be considered? | Candidate areas, exclusions and areas with insufficient information. |
| [[ch:m2-climate-risk|M2: Livelihood climate risk]] | Where are people and production exposed to climate hazards? | Climate-related need. |
| [[ch:m2b-project-risk|M2b: Investment risk]] | What could damage the intervention or obstruct delivery? | Separate risk flags and implementation questions. |
| [[ch:m3-characterisation|M3: Characterisation]] | Who and what lies within the candidate areas? | People, production and environmental context. |
| [[ch:m4-hotspots|M4: Priorities]] | Where do the team's chosen priorities concentrate? | Ranked areas and the factors driving their rank. |
| [[ch:m5-scorecard|M5: Comparison]] | What can each practice plausibly deliver? | Benefits, trade-offs, confidence and indicative costs. |
| [[ch:m6-handoff|M6: Next steps]] | What must local assessment establish? | Shortlist and questions for feasibility work. |

[src: methodology/modules/README.md §Index] [src: method:handbook/implement-a-scan.md §3. Build the scoping brief]

M1 defines the candidate space within which M3 describes conditions and M4 ranks priorities. M2 supplies climate-related need; M2b supplies a separate investment-risk screen. M5 brings the evidence on benefits and costs into the comparison, and M6 assembles the hand-off. [[ch:scoping-walkthrough]] illustrates this sequence. [src: methodology/modules/M1_suitability.md §5. Dependencies]

## Principles shared by every module

**Assess suitability by family.** Different variants of one practice can have different limiting factors. Planted trees and regeneration-based agroforestry, for example, need different evidence and inputs. A suitability family groups variants that share the dominant limiting factor; each family also defines whether its footprint can be reported as area, length or qualitative guidance. See [[ch:m1-suitability]]. [src: methodology/T4_generation_method.md §2.1 Practice definition → subpractices → suitability families] [src: methodology/T4_generation_method.md §2.4 Spatial product type & the resolution trap]

**Keep need and investment risk separate.** A flood-prone area may have a strong need for risk reduction while also posing a threat to a proposed intervention. M2 describes the first question and M2b the second. Their scores are never added together. Road access, tenure and other investment-addressable barriers belong with operational risk and next steps, rather than being built into structural suitability. [src: AGENTS.md §What is locked]

**Trace analytical choices to evidence.** A table value links to extracted claims and then to the source, quotation and page or other locator. Extraction records what the source says; synthesis considers how claims support a mapping or effect rating. New T4 proposals use agent-led synthesis followed by recorded review. An accepted extraction alone does not approve a numerical response or its transfer to another country. [[ch:evidence-principles]] explains the records; [[ch:suitability-synthesis]] explains the T4 workflow. [src: methodology/T4_generation_method.md §0. Why this method exists] [src: method:handbook/read-a-suitability-recipe.md §Check the decision before scoring]

**Keep analytical rules in versioned tables.** Practice definitions, datasets, responses, weights and evidence links travel together as a documented configuration. A run records which edition and settings it used. The data-model section supplies field definitions; the module chapters explain how to interpret the resulting outputs. [src: schema/spec.md §Table overview] [src: method:handbook/implement-a-scan.md §3. Build the scoping brief]

**Match data to the question.** Choose data for their relevance, scale, coverage and provenance before considering hosting convenience. Use observed host-system distributions where the intervention improves an existing crop or land use. A global dataset or a country code does not establish that a response is applicable locally. Dataset selection and resolution rules have one home in [[ch:farming-systems-and-data]]. [src: methodology/T4_generation_method.md §2.5 Constrain by observed distribution, not a modelled niche, where data exist] [src: methodology/T4_developer_contract.md §Target country and evidence country are different filters]

**Show uncertainty in the decision.** Keep unknown inputs distinct from exclusions and low scores. Check whether plausible changes in inputs, responses or priority weights change the shortlist. Study counts describe coverage, not scientific strength, and repeated or dependent claims do not supply independent confirmation. See [[ch:compiling-evidence]] for combining evidence and [[ch:m4-hotspots]] for ranking sensitivity. [src: methodology/T4_developer_contract.md §Aggregation baseline and design history] [src: methodology/T4_generation_method.md §6.1 Publication bias & uncertainty (pragmatic)]

## Assumptions and limits

The scan relies on spatial data and literature that may represent the target landscape unevenly. Coarse data can hide local constraints, and published findings tend to report success more often than failure. A shortlist therefore identifies where further investigation is worthwhile; it does not establish land availability, local effectiveness or financial viability. [src: methodology/recipes/water_harvesting.md §7.6 Constraints and limitations] [src: methodology/T4_generation_method.md §6.1 Publication bias & uncertainty (pragmatic)]

This draft describes the analytical approach. The evidence edition documents the records behind it; an application report must identify the stages actually run, the inputs used and the validation performed. See [[ch:implementing-the-method]] for that reporting boundary and [[ch:m6-handoff]] for the feasibility hand-off.

## Where this is configured

Practice and family definitions are in [[table:T0]] and [[table:FAM]]. Data and geographic context are in [[table:T1]], [[table:BIND]] and [[table:T7]]. Analytical settings are in [[table:T2]], [[table:T3]], [[table:T4]], [[table:T4_RUN]], [[table:T5]], [[table:T6]] and [[table:T6E]]. The evidence records behind them are described in [[ch:evidence-principles]]. [[ch:editions]] identifies the published snapshots.
