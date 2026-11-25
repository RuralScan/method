---
title: "M2: Rural climate risk to livelihoods"
slug: m2-climate-risk
summary: Interpret climate-related need, distinguish hazard exposure from intervention response, and compare scenarios consistently.
sources:
  - method:priority/t2/README.md
  - method:priority/t2/variables.csv
  - method:priority/README.md
  - method:data-model/priority-contract.json
  - methodology/modules/M2_climate_risk.md
  - AGENTS.md
  - schema/spec.md
  - schema/T2_climate_risk.csv
  - methodology/T3_T6_generation_method.md
  - methodology/framework.md
  - schema/registers/BIND_dataset_binding.csv
---

## Question this module answers

Module 2 (M2) examines where rural people and production systems are exposed to climate hazards, under a stated baseline and future scenario. It describes **climate-related need**, which can inform the priority analysis in [[ch:m4-hotspots]]. It does not estimate how much a proposed intervention will reduce losses. [src: methodology/modules/M2_climate_risk.md §2]

Keep this distinct from [[ch:m2b-project-risk]], which screens threats to the investment itself. A hazard may create a need for intervention and also threaten that intervention. The two risk lenses are never summed. [src: AGENTS.md §What is locked]

## Inputs

Table: Information required for a livelihood climate-risk assessment.

| Input | Purpose |
|---|---|
| Area, analysis grid and period | Define where and when conditions are assessed. |
| Hazard metrics | Describe hazard intensity or frequency for each stated scenario. |
| Exposure | Locate rural people, production or other livelihood assets potentially affected. |
| Classification rule | State units, direction, thresholds or the declared relative reference. |
| Practice-response evidence | Distinguish a relevant hazard from evidence that a particular practice mitigates it. |
| Data and transformation record | Identify versions, units, scaling, coverage and any aggregation. |

[src: methodology/modules/M2_climate_risk.md §3]

[[table:T2]] records named climate-risk variables and classification references; [[table:T3]] records practice responses to hazards. The current T2 registry preserves all eleven IDs, with candidate datasets and explicit blockers. None is yet an accepted, runnable classification. Historical mode and default-weight fields remain in the archived CSV, not the current interface. [src: method:priority/t2/README.md] Apply the data-selection checks in [[ch:farming-systems-and-data]]. [src: method:data-model/spec.md §T2] [src: method:priority/README.md]

## Method

### 1. Define the hazard question

Select the hazards relevant to the rural landscape and the practice being considered. T3 distinguishes evidence of livelihood mitigation from threats to the investment. An evidence row's presence does not establish a positive or transferable effect: read its direction, confidence and applicability alongside the hazard map. [src: methodology/modules/M2_climate_risk.md §6.1] [src: methodology/T3_T6_generation_method.md §1]

Name the actual metric for each hazard. Rainfall intensity, flood depth and drought duration describe different processes; one should not be relabelled as another without stating the proxy and its limitations. [src: methodology/modules/M2_climate_risk.md §6.2]

### 2. Describe exposure

Assemble the relevant population and production layers at their true spatial support. Report which livelihood assets are represented and which are absent. Counts and values are exposure measures, not damage estimates or counts of beneficiaries of the proposed practice. [src: methodology/modules/M2_climate_risk.md §6.3]

The baseline-exposure approach holds population and production fixed when examining future hazards. Its future result therefore describes the effect of changing hazard under that exposure assumption, not a forecast of future settlement or land use. [src: methodology/modules/M2_climate_risk.md §6.6]

### 3. Classify variables without constructing a separate risk index

T2 is the registry of climate-risk variables. The current priority route uses individual, named concerns with explicit classification rules; it does not calculate a composite Climate Risk Index or switch between Mode A and Mode B. Exposure summaries remain available as context. Historical T2 mode, normalization and default-weight fields describe earlier editions, not active defaults. [src: method:priority/README.md]

Each variable records its unit, scenario, context, shared concern identity and classification-rule reference. M3 maps the declared concern to none, low, medium or high and M4 applies user priorities once. A T2 hazard that is also listed in T5 enters the priority stack through one explicit representative. The rule does not estimate losses or assume that the practice reduces the hazard. [src: method:data-model/priority-contract.json] [[ch:m3-characterisation]]

### 4. Compare baseline and future conditions consistently

Use compatible hazard quantities, periods, units and reference scales. A difference between separately rescaled maps can reflect the scaling change as well as climate change. Do not interpret a change between unlike metrics as a change in physical risk. Record the scenario, future horizon and exposure assumptions with each comparison. [src: methodology/modules/M2_climate_risk.md §6.6]

The T2 migration records unresolved proxy and comparability issues, including a rainfall-based flood proxy and different baseline and future drought inputs. Those entries cannot be treated as a validated paired change analysis. [src: method:priority/t2/variables.csv] The application must establish compatible inputs before making that comparison. [src: schema/T2_climate_risk.csv] [src: schema/registers/BIND_dataset_binding.csv]

### 5. Summarise and test interpretation

Report hazard and exposure summaries for the chosen geographic units, with raw values, units, coverage and the meaning of any classes. For priority ranking, test plausible alternative weights and data choices and explain which conclusions change. [[ch:m4-hotspots]] describes priority sensitivity; it does not replace hazard-data validation. [src: methodology/modules/M2_climate_risk.md §6.7] [src: methodology/modules/M2_climate_risk.md §6.8]

## Reading need alongside response

High hazard exposure indicates a problem requiring attention. It does not establish that a given practice is effective at the mapped hazard severity. Read the response evidence in [[table:T3]] and [[ch:m5-scorecard]], including adverse effects, insufficient evidence and transfer conditions. The treatment of severity and effect synthesis belongs in [[ch:effect-synthesis]]. [src: methodology/T3_T6_generation_method.md §1] [src: methodology/T3_T6_generation_method.md §5.5]

For example, a flood-exposed farming area may warrant investigation of retention measures. Evidence that a practice reduces ordinary runoff does not by itself establish protection against an extreme flood. This is an illustration of the distinction between need and response, not a pilot impact estimate.

## Outputs

Retain hazard layers, their problem classes and exposure summaries separately, with baseline and future scenarios clearly labelled. Report data coverage, scaling, weights and comparison assumptions alongside maps and geographic summaries. These outputs inform the climate-need contribution to M4; M2b investment-risk flags remain separate. [src: methodology/modules/M2_climate_risk.md §4]

## Assumptions and limits

Hazard proxies, coarse exposure data and uncertain future climate can alter the result. Relative scores describe position within a declared reference distribution, not expected losses. Future hazard combined with baseline exposure does not incorporate demographic or land-use change. [src: methodology/modules/M2_climate_risk.md §6.3] [src: methodology/modules/M2_climate_risk.md §6.6]

A livelihood-risk map does not quantify the benefit of an intervention. Feasibility work must assess local hazards, vulnerability and likely effects at the scale of the proposed design. Input comparability and documented aggregation are prerequisites for interpreting a combined or change score, not matters resolved by the label “risk”. [src: methodology/modules/M2_climate_risk.md §2] [src: methodology/framework.md §What this framework does not do]

## Where this is configured

[[table:T2]] records climate-risk variables and classification references; [[table:T3]] records practice–hazard responses. [[table:T1]] and [[table:BIND]] identify data; [[table:T7]] defines contexts. The application records scenarios, exposure assumptions, classification rules, reference populations, user weights and missing-data handling. [src: method:priority/README.md] [[table:T5]] supports checks against counting the same concern twice in prioritisation.
