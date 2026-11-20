---
title: "M2: Rural climate risk to livelihoods"
slug: m2-climate-risk
summary: Interpret climate-related need, distinguish hazard exposure from intervention response, and compare scenarios consistently.
sources:
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
| Risk formulation | State whether the assessment includes exposure alone or also vulnerability. |
| Practice-response evidence | Distinguish a relevant hazard from evidence that a particular practice mitigates it. |
| Data and transformation record | Identify versions, units, scaling, coverage and any aggregation. |

[src: methodology/modules/M2_climate_risk.md §3]

[[table:T2]] records the risk variables and components; [[table:T3]] records practice responses to hazards. The published table is an edition-specific configuration, not proof that its defaults are calibrated for a target country. Apply the data-selection checks in [[ch:farming-systems-and-data]]. [src: schema/spec.md §T2] [src: schema/T2_climate_risk.csv]

## Method

### 1. Define the hazard question

Select the hazards relevant to the rural landscape and the practice being considered. T3 distinguishes evidence of livelihood mitigation from threats to the investment. An evidence row's presence does not establish a positive or transferable effect: read its direction, confidence and applicability alongside the hazard map. [src: methodology/modules/M2_climate_risk.md §6.1] [src: methodology/T3_T6_generation_method.md §1]

Name the actual metric for each hazard. Rainfall intensity, flood depth and drought duration describe different processes; one should not be relabelled as another without stating the proxy and its limitations. [src: methodology/modules/M2_climate_risk.md §6.2]

### 2. Describe exposure

Assemble the relevant population and production layers at their true spatial support. Report which livelihood assets are represented and which are absent. Counts and values are exposure measures, not damage estimates or counts of beneficiaries of the proposed practice. [src: methodology/modules/M2_climate_risk.md §6.3]

The baseline-exposure approach holds population and production fixed when examining future hazards. Its future result therefore describes the effect of changing hazard under that exposure assumption, not a forecast of future settlement or land use. [src: methodology/modules/M2_climate_risk.md §6.6]

### 3. State the risk formulation

The framework distinguishes a default **Mode A**, combining hazard and exposure, from **Mode B**, which also considers vulnerability through sensitivity and adaptive capacity. Mode B needs an explicit vulnerability formulation and suitable data. Merely naming the mode does not define a reproducible calculation. [src: methodology/framework.md §Climate risk formulation]

An application must document how it standardises inputs, combines multiple exposure indicators or hazards, assigns weights, handles missing values and defines display classes. These decisions determine the meaning of a composite index. This chapter does not supply an unapproved universal composition formula. Where a justified composite is unavailable, hazard-specific information and exposure summaries remain interpretable without presenting an invented combined score. [src: methodology/modules/M2_climate_risk.md §6.4] [src: methodology/modules/M2_climate_risk.md §6.5]

If vulnerability indicators are included in M2, check their use in M3/M4. Counting poverty or adaptive-capacity proxies again as independent priorities can give the same concern unintended additional weight. Record the choice and keep descriptors separate from weighted criteria. [src: methodology/modules/M2_climate_risk.md §10]

### 4. Compare baseline and future conditions consistently

Use compatible hazard quantities, periods, units and reference scales. A difference between separately rescaled maps can reflect the scaling change as well as climate change. Do not interpret a change between unlike metrics as a change in physical risk. Record the scenario, future horizon and exposure assumptions with each comparison. [src: methodology/modules/M2_climate_risk.md §6.6]

The published T2 edition contains proxy and comparability issues, including a rainfall-based flood proxy and different baseline and future drought inputs. Those entries cannot be treated as a validated paired change analysis. The application must establish compatible inputs before making that comparison. [src: schema/T2_climate_risk.csv] [src: schema/registers/BIND_dataset_binding.csv]

### 5. Summarise and test interpretation

Report hazard and exposure summaries for the chosen geographic units, with raw values, units, coverage and the meaning of any classes. If a composite or ranking is used, test plausible alternative weights and data choices and explain which conclusions change. [[ch:m4-hotspots]] describes priority sensitivity; it does not replace hazard-data validation. [src: methodology/modules/M2_climate_risk.md §6.7] [src: methodology/modules/M2_climate_risk.md §6.8]

## Reading need alongside response

High hazard exposure indicates a problem requiring attention. It does not establish that a given practice is effective at the mapped hazard severity. Read the response evidence in [[table:T3]] and [[ch:m5-scorecard]], including adverse effects, insufficient evidence and transfer conditions. The treatment of severity and effect synthesis belongs in [[ch:effect-synthesis]]. [src: methodology/T3_T6_generation_method.md §1] [src: methodology/T3_T6_generation_method.md §5.5]

For example, a flood-exposed farming area may warrant investigation of retention measures. Evidence that a practice reduces ordinary runoff does not by itself establish protection against an extreme flood. This is an illustration of the distinction between need and response, not a pilot impact estimate.

## Outputs

Retain hazard layers, exposure summaries and any documented risk index separately, with baseline and future scenarios clearly labelled. Report data coverage, scaling, weights and comparison assumptions alongside maps and geographic summaries. These outputs inform the climate-need contribution to M4; M2b investment-risk flags remain separate. [src: methodology/modules/M2_climate_risk.md §4]

## Assumptions and limits

Hazard proxies, coarse exposure data and uncertain future climate can alter the result. Relative scores describe position within a declared reference distribution, not expected losses. Future hazard combined with baseline exposure does not incorporate demographic or land-use change. [src: methodology/modules/M2_climate_risk.md §6.3] [src: methodology/modules/M2_climate_risk.md §6.6]

A livelihood-risk map does not quantify the benefit of an intervention. Feasibility work must assess local hazards, vulnerability and likely effects at the scale of the proposed design. Input comparability and documented aggregation are prerequisites for interpreting a combined or change score, not matters resolved by the label “risk”. [src: methodology/modules/M2_climate_risk.md §2] [src: methodology/framework.md §What this framework does not do]

## Where this is configured

[[table:T2]] records risk components and settings; [[table:T3]] records practice–hazard responses. [[table:T1]] and [[table:BIND]] identify data; [[table:T7]] defines contexts. The application records its mode, scenarios, exposure assumptions, transformations, weights and missing-data handling. [[table:T5]] supports checks against counting the same concern twice in prioritisation.
