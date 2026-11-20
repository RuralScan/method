---
title: Farming systems, contexts and data
slug: farming-systems-and-data
summary: Select context-appropriate spatial inputs and understand the limits of farming-system classes, dataset bindings and global defaults.
sources:
  - schema/spec.md
  - schema/registers/FS_DIXON_CROSSWALK.md
  - methodology/farming_system_classifier.md
  - methodology/T4_developer_contract.md
  - methodology/framework.md
  - AGENTS.md
  - methodology/T4_generation_method.md
  - methodology/modules/M0_setup.md
  - schema/registers/BIND_dataset_binding.csv
  - schema/registers/VONT_variable_ontology.csv
---

## What this chapter covers

Spatial data must match both the decision and the place. This chapter explains how farming systems and geographic contexts guide data selection, how local sources can replace global defaults, and what a run records about scale and uncertainty. Dataset records and field definitions remain in the data-model section, avoiding a second catalogue here. [src: schema/spec.md §Evidence & configuration layer (upstream of T0–T7)]

## Farming-system and geographic context

A farming system describes the land-use and production system, while an agro-ecological zone describes bioclimatic context. Both can affect whether evidence transfers, which response parameters apply and which dataset measures a variable appropriately. [src: schema/registers/FS_DIXON_CROSSWALK.md §Why the swap] [src: schema/spec.md §T7]

Table: Farming-system classes used by the published vocabulary.

| Class | Meaning |
|---|---|
| `cropping_rainfed` | Cropland with low irrigation and low livestock density. |
| `cropping_irrigated` | Cropland with a substantial irrigation share. |
| `mixed_crop_livestock` | Cropland combined with moderate or high livestock density. |
| `agro_pastoral` | Sparse cropland in a grazing-dominated system. |
| `pastoral_rangeland` | Rangeland with substantial livestock use. |
| `tree_perennial` | A system dominated by perennial tree crops. |

[src: methodology/farming_system_classifier.md §Output classes (T7 `farming_system`)]

These are scoping categories, not field boundaries or a globally validated land-use map. A classification needs evidence of cropland, irrigation, livestock and tree-crop distribution at compatible spatial support. General tree cover alone does not establish a perennial-crop system; modelled livestock density is particularly uncertain for mobile herds. Check the classification against relevant national statistics and local knowledge before using it to support a decision. [src: methodology/farming_system_classifier.md §Fitness limits] [src: methodology/farming_system_classifier.md §Validation (forward)]

[[table:T7]] holds geographic contexts: countries, administrative regions, hydrobasins, agro-ecological zones and farming systems. It provides the identifiers used to match evidence, response parameters and datasets. A context description is not itself an evidence-derived suitability threshold. [src: schema/spec.md §T7]

## Choose data by fitness for purpose

For each variable, ask what quantity the analysis needs, at what location, time, depth and resolution. Check the dataset's measurement basis, coverage, uncertainty, licence and version. A more accessible source is not preferable if it measures the wrong quantity. [src: schema/spec.md §T1] [src: methodology/T4_developer_contract.md §Dataset preparation proposals and source compatibility]

Table: Checks when selecting a spatial input.

| Check | Practical consequence |
|---|---|
| Quantity and units | Confirm that the measured variable, scale and units match the response or indicator. |
| Spatial support | Distinguish grid cells, administrative statistics and mapped features; do not imply precision absent from the source. |
| Time and depth | Record baseline period, projection scenario and any soil depth or temporal aggregation. |
| Coverage | Report gaps and substitutions, including missing local data. |
| Provenance | Record provider, dataset version, access route, citation, licence and processing. |
| Transfer | Check local relevance independently of whether the dataset can be downloaded. |

[src: schema/spec.md §T1] [src: methodology/T4_developer_contract.md §Dataset preparation proposals and source compatibility]

The dataset and binding tables displayed in this methodology belong to the **published evidence edition**. They are not a definitive list of the latest pilot inputs or planned replacements. Each application must name the dataset versions it actually used. A replacement is recorded through the dataset registry and binding, not silently substituted in this narrative. [src: schema/spec.md §T1] [src: schema/spec.md §BIND]

## Server-side-first sourcing

Among sources that are fit for purpose, prefer the Google Earth Engine catalogue, then community-hosted sources, then supplied data. Where equivalent server-hosted data exist, crop, mosaic and process them before transfer where practical. Platform convenience does not override scientific suitability. [src: methodology/framework.md §Dataset sourcing (three-tier preference)] [src: AGENTS.md §What is locked]

Hosting does not remove scale constraints. Derive scale-sensitive quantities such as slope from sufficiently fine inputs before aggregating. Enlarging a coarse raster to a fine grid adds cells, not information. Check each variable's resolution limits in [[table:VONT]] and report processing in the run record. [src: methodology/T4_generation_method.md §2.4 Per-variable resolution validity]

## Resolve the dataset for the target context

[[table:T1]] describes datasets; [[table:BIND]] connects a variable to its preferred dataset for a context. A global default can be refined by a more specific region, country, hydrobasin, farming system or agro-ecological zone. Where several bindings match, the documented precedence and preference rank decide which applies. [src: schema/spec.md §BIND]

A dataset override and a response override answer different questions. The first selects the data; the second changes the response parameters where evidence supports that change. Selecting a country-specific dataset does not approve transfer of a response from another country. [src: schema/spec.md §BIND] [src: methodology/T4_developer_contract.md §Target country and evidence country are different filters]

A binding marked `requires_upload` identifies a preferred input that must be supplied. If a suitable fallback is used, state the substitution and its implications. If no required input is available, keep the result unavailable rather than inventing a value or silently dropping the requirement. [src: schema/spec.md §BIND] [src: methodology/modules/M0_setup.md §6. Sub-steps]

### Example: a local crop map and a global fallback

A family that improves an existing tree-crop system may use a global crop-allocation map as its default host distribution. A country-specific crop map can take precedence where available. Until it is supplied, the global map is a disclosed fallback. Its coarse allocation does not establish that every mapped cell contains an eligible field, and neither map establishes the crop's biophysical response. [src: schema/registers/BIND_dataset_binding.csv] [src: methodology/T4_developer_contract.md §Planted host and exclusion contracts]

The same principle applies to `production_gap`: a crop-yield gap, a rangeland productivity gap and a mixed-system indicator are different quantities. Their metric and denominator must be appropriate to the farming system and retained in comparisons. [[ch:m3-characterisation]] explains their use. [src: AGENTS.md §What is locked]

## Context-sensitive data

Population, poverty, production and related nationally derived indicators may differ from official country estimates. Flag these inputs and recommend confirmation with a country-endorsed source. The scan identifies the question; it does not negotiate or endorse national statistics. [src: methodology/T4_generation_method.md §2.6]

[[table:VONT]] records context-sensitivity flags. A missing flag is not evidence that a variable is insensitive. Keep source qualifications with the output and carry them into [[ch:m6-handoff]], rather than treating a global default as locally validated. [src: schema/registers/VONT_variable_ontology.csv] [src: methodology/T4_generation_method.md §2.6]

## Assumptions and limits

Global products can be dated, coarse or modelled. Tree cover can conflate natural forest, plantations and shaded crops; irrigation products can miss small schemes; livestock maps may poorly represent mobile herds. These limitations can change both the farming-system label and the inferred candidate area. [src: methodology/farming_system_classifier.md §Fitness limits]

Administrative statistics retain the spatial support of their source. A national indicator cannot explain variation within a country simply because it is displayed on a raster. Missing local inputs and uncertainty in host-system mapping remain visible in the scoping brief and become questions for local validation. [src: schema/spec.md §T1] [src: methodology/T4_developer_contract.md §Planted host and exclusion contracts]

## Where this is configured

[[table:T1]] holds dataset metadata; [[table:BIND]] holds contextual choices and upload flags; [[table:T7]] defines geographic and farming-system contexts; [[table:VONT]] defines variables, units, scale and sensitivity. [[table:T4]] records response overrides separately. The application records the versions and processing actually used.
