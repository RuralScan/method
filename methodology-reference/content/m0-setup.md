---
title: "M0: Setup and scope"
slug: m0-setup
summary: Record the decision, area, scientific inputs and data needed before analysis.
sources:
  - methodology/modules/M0_setup.md
  - method:handbook/implement-a-scan.md
  - method:priority/README.md
  - method:data-model/agent-t4-contract.md
  - methodology/T4_generation_method.md
  - methodology/T4_developer_contract.md
  - method:handbook/read-a-suitability-recipe.md
  - schema/spec.md
---

## Question this module answers

Module 0 (M0) records what the team wants to assess, where, and with which evidence and data. Its output is a **run configuration**: a saved record of those choices. Setup checks readiness; it does not establish local suitability or approve scientific rules. [src: methodology/modules/M0_setup.md §1. Purpose] [src: method:handbook/implement-a-scan.md §1. Check the inputs before making a map]

## Inputs

Table: Choices to record before a scan.

| Choice | What to record |
|---|---|
| Decision and practice | Investment question, selected practice and suitability family. |
| Area | Boundary, its source and relevant geographic contexts. |
| Scale | Analysis grid and the footprint unit the family supports. |
| Time | Baseline period, future scenarios and comparison horizon. |
| Scientific inputs | Accepted mappings and classification rules, with their versions and applicability. |
| Spatial data | Dataset versions, units, coverage and any required local uploads. |

[src: method:handbook/implement-a-scan.md §3. Build the scoping brief] [src: method:priority/README.md] [src: method:data-model/agent-t4-contract.md]

Choose the grid to suit the variables and intervention. A demonstration default does not establish an appropriate analysis scale. [[ch:farming-systems-and-data]] explains the data checks; [[ch:m1-suitability]] explains valid footprint measures. [src: methodology/T4_generation_method.md §2.4 Per-variable resolution validity]

## Method

### 1. Scope capture

Record the decision, practice, family, area boundary and scenarios. Use the country's relevant administrative units without assuming that every country uses districts or counties. Geographic contexts in [[table:T7]] help select data; they do not establish that evidence from another place transfers. [src: methodology/modules/M0_setup.md §6. Sub-steps] [src: methodology/T4_developer_contract.md §Target country and evidence country are different filters]

### 2. Recipe resolution

A **recipe** is the documented configuration for a practice. Inspect its suitability mappings, priority variables and evidence. Keep historical outputs distinct from newly accepted proposals. Selecting a recipe does not approve missing calibration, transfer or execution settings. [src: method:handbook/read-a-suitability-recipe.md §Check the decision before scoring] [src: method:data-model/agent-t4-contract.md]

### 3. Data-readiness check

For each required variable, identify a compatible dataset and how it will be accessed. Check quantity, units, period, depth, coverage and resolution. Record preferred local sources and any proposed substitute; a downloadable global layer is not automatically an acceptable replacement. [[ch:farming-systems-and-data]] gives the full selection procedure. [src: schema/spec.md §BIND] [src: methodology/T4_developer_contract.md §Dataset preparation proposals and source compatibility]

### 4. Ingestion validation

Confirm that required data can be read. An unavailable required input remains a blocker until it is supplied or an appropriate substitute is recorded. The current T4 proposal contract does not silently replace a preferred binding that requires a local upload. [src: methodology/modules/M0_setup.md §6. Sub-steps] [src: method:data-model/agent-t4-contract.md]

### 5. Variable-configuration surfaces

Keep suitability settings separate from priority settings. The former describe where a practice could fit; the latter express which development concerns the user values. Changing a user weight does not change the evidence or approve a suitability response. [src: methodology/modules/M0_setup.md §7. Variable Cards consumed] [src: method:priority/README.md]

### 6. Emit the run configuration

Save the choices with input versions, processing, scientific decisions and output identifiers. Keep units, denominators and coverage beside reported numbers. This record lets another analyst reproduce the application and explain later changes. [src: method:handbook/implement-a-scan.md §3. Build the scoping brief]

## Outputs

Provide the saved configuration, a data-readiness report and a record of scale limits, substitutions and unresolved requirements. Downstream modules use the same recorded scope and scenarios. [src: methodology/modules/M0_setup.md §4. Outputs]

### Acceptance criteria

Before analysis, check that required inputs and versions are identified, data access works, scale limits are visible and unresolved requirements are not treated as passed. These are readiness checks, not evidence that the method has been validated in the target landscape. [src: methodology/modules/M0_setup.md §8. Tests / acceptance criteria]

## Worked illustration

An analyst selects a country and a tree-planting family. A global soil layer is available, but a preferred local layer has not been supplied and transfer of the proposed response remains unresolved. The analyst records both requirements. Selecting the country or downloading the global layer does not resolve either scientific question. This illustrates setup, not a completed country result. [src: method:handbook/implement-a-scan.md §1. Check the inputs before making a map] [src: method:data-model/agent-t4-contract.md]

## Assumptions and limits

Readiness is not local validity. A complete configuration can still contain coarse data, uncertain responses or imperfect host-system maps. Keep those qualifications visible and carry nationally sensitive statistics into the hand-off for confirmation. [src: methodology/T4_developer_contract.md §Reproducible chain] [src: methodology/T4_generation_method.md §2.6]

## Where this is configured

[[table:T0]] and [[table:FAM]] identify practices and families. [[table:T1]], [[table:BIND]], [[table:T7]] and [[table:VONT]] describe data, contexts and scale. [[table:T4]] records suitability mappings; [[table:T2]] and [[table:T5]] identify climate and priority variables. The run configuration records the selected versions and settings. See [[ch:implementing-the-method]] for reporting and software guidance.
