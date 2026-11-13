---
title: Farming systems, contexts and data
slug: farming-systems-and-data
summary: Explains how farming-system classes are derived from Earth observation, how geographic contexts and the data registry are structured, and how a dataset is chosen for each variable in a given place, including sensitivity flags and upload prompts.
sources:
  - methodology/farming_system_classifier.md
  - schema/registers/FS_DIXON_CROSSWALK.md
  - schema/spec.md
  - schema/structure/columns.json
  - schema/T1_data_registry.csv
  - schema/T7_geographic_context.csv
  - schema/registers/BIND_dataset_binding.csv
  - schema/registers/VONT_variable_ontology.csv
  - methodology/T4_generation_method.md
  - methodology/T4_developer_contract.md
  - methodology/framework.md
  - src/nbs_ruralscan/runtime/binding.py
  - src/nbs_ruralscan/runtime/farming_system.py
  - AGENTS.md
---

## What this chapter covers

Every module needs two kinds of reference information besides the evidence: **where** an analysis is (its geographic and farming-system context) and **which data** describe each variable there. The method keeps both in tables, not code. [[table:T7]] defines contexts, [[table:T1]] catalogues datasets, [[table:BIND]] binds each variable to a dataset per context, and [[table:VONT]] carries each variable's units, resolution limits and sensitivity flag. [src: schema/spec.md §T7] [src: schema/spec.md §Evidence & configuration layer (upstream of T0–T7)]

## Farming systems

### Why a farming-system context

Farming system is a land-system context, distinct from the bioclimatic agro-ecological zone (AEZ). It is used in four places: [src: schema/registers/FS_DIXON_CROSSWALK.md §Why the swap] [src: schema/spec.md §Value governance]

- as a key of hazard-response cells (NbS × hazard × farming system) in [[table:T3]] and of the farming systems an NbS applies to in [[table:T0]];
- as a scope for context-specific T4 response parameters (`context_overrides`);
- as a scope for dataset bindings in [[table:BIND]];
- to resolve the metric of `production_gap`, which differs by system.

It is also the natural home of the "constrain by observed distribution" principle on the land-use side: where a family depends on an existing system, its observed extent gates suitability ([[ch:m1-suitability]]). [src: methodology/farming_system_classifier.md §See also]

### Six EO-derived classes

The farming-system vocabulary has six classes, derived at scoping grade from open Earth-observation (EO) layers. [src: AGENTS.md §What is locked] [src: methodology/farming_system_classifier.md §Output classes (T7 `farming_system`)]

| Class | Definition |
|---|---|
| `cropping_rainfed` | Cropland present, low irrigation, low livestock density. |
| `cropping_irrigated` | Cropland present, irrigation share above threshold. |
| `mixed_crop_livestock` | Cropland present, moderate-to-high livestock density. |
| `agro_pastoral` | Sparse cropland, grazing-dominant land cover, moderate livestock. |
| `pastoral_rangeland` | Non-cropland grassland or shrubland, high livestock density. |
| `tree_perennial` | Tree-perennial dominant (cocoa, coffee, oil palm, rubber, fruit). |

[src: methodology/farming_system_classifier.md §Output classes (T7 `farming_system`)]

A seventh value, `other`, is emitted when no rule matches (typically barren, built-up or permanent water) and is masked out before the layer enters bindings or T7. It is a real outcome, not an error. [src: methodology/farming_system_classifier.md §Output classes (T7 `farming_system`)] [src: methodology/farming_system_classifier.md §Fitness limits]

The scheme replaced an earlier nine-class typology in the style of Dixon's farming-systems classification. Dixon labels now serve only as a crosswalk for prior work: several collapse into one EO class (for example both maize-mixed and highland-mixed map to `mixed_crop_livestock`), because the EO scheme is coarser by design. The reasons for the change were that EO classes are computable from open layers without a closed vocabulary standing between AOI definition and assignment, that they do not overlap the bioclimatic AEZ concept, and that six classes suffice for binding `production_gap` at scoping grade. [src: schema/registers/FS_DIXON_CROSSWALK.md §Dixon → EO crosswalk] [src: schema/registers/FS_DIXON_CROSSWALK.md §Why the swap]

### The classifier

**Inputs.** Five open layers, all registered in [[table:T1]]: [src: methodology/farming_system_classifier.md §Input layers (T1)]

| Role | Dataset | Resolution |
|---|---|---|
| Cropland (primary) | `glad_global_cropland_2019` | 30 m |
| Cropland and irrigation (auxiliary) | `esa_worldcereal_2021` | 10 m |
| Livestock density, tropical livestock units (TLU) per km² | `glw4_livestock_2020` | about 10 km |
| Irrigation share (area equipped) | `fao_gmia_v5` | about 10 km |
| Tree-perennial mask | `hansen_treecover2000` with `mapspam_cocoa_2020` | 30 m and 10 km |

The classifier function takes pre-aligned arrays on the analysis grid; reprojection, resampling, masking and TLU computation happen upstream. [src: methodology/farming_system_classifier.md §Input layers (T1)]

**Decision tree.** Rules are applied in priority order; the first match wins. [src: methodology/farming_system_classifier.md §Decision tree] [src: src/nbs_ruralscan/runtime/farming_system.py]

```formula
if P ≥ θ_tree:                         class = tree_perennial
else if C ≥ θ_crop and I ≥ θ_irr:      class = cropping_irrigated
else if C ≥ θ_crop and L ≥ θ_mixed:    class = mixed_crop_livestock
else if C ≥ θ_crop:                    class = cropping_rainfed
else if L ≥ θ_past:                    class = pastoral_rangeland
else if L ≥ θ_agro:                    class = agro_pastoral
else:                                  class = other
```

- `P`: tree-perennial fraction of the cell; `C`: cropland fraction; `I`: irrigation share (area equipped); `L`: ruminant livestock density in TLU per km².
- `θ`: the thresholds in the table below.

[src: methodology/farming_system_classifier.md §Decision tree]

The order is deliberate. Tree-perennial dominance is the most decisive signal and overrides a crop-livestock mosaic under a perennial canopy. Irrigation precedes livestock because irrigated cropping is operationally distinct from rainfed mixed systems. Pastoral precedes agro-pastoral because high livestock density without cropland is unambiguous, while agro-pastoral is the middle case. [src: methodology/farming_system_classifier.md §Decision tree]

**Default thresholds.**

| Threshold | Default | Stated rationale |
|---|---:|---|
| `θ_crop` (cropland present) | 0.10 | A cell counts as cropland when at least 10 % is cropland; deliberately admits smallholder mosaics. |
| `θ_irr` (irrigation share) | 0.20 | Area equipped for irrigation above 20 % makes the cell irrigated; to be checked against WorldCereal irrigation where they agree. |
| `θ_mixed` | 5.0 TLU/km² | Ruminant density above which cropland is mixed. |
| `θ_agro` | 5.0 TLU/km² | Same threshold for non-cropland to be agro-pastoral. |
| `θ_past` | 20.0 TLU/km² | Ruminant density above which non-cropland is pastoral. |
| `θ_tree` | 0.50 | Tree-perennial fraction above 50 % makes the cell tree-perennial. |

[src: methodology/farming_system_classifier.md §Default thresholds (v0.3.0 scoping-grade)]

These are presented as defensible scoping-grade starting points. They are not validated against ground truth at global level, and per-AOI tuning is expected before use. The livestock thresholds are attributed to mixed-system literature without a specific citation in the pinned file. [src: methodology/farming_system_classifier.md §Default thresholds (v0.3.0 scoping-grade)] Any AOI override is to be recorded in the run configuration. [src: methodology/farming_system_classifier.md §Per-AOI tuning]

Two features of the rules deserve attention. First, the text definition of `agro_pastoral` mentions grazing-dominant land cover, but the decision tree uses only livestock density for cells below the cropland threshold; land cover is not tested. Second, with the defaults `θ_mixed = θ_agro`, a single livestock threshold separates rainfed from mixed on cropland and "other" from agro-pastoral off cropland. [src: methodology/farming_system_classifier.md §Output classes (T7 `farming_system`)] [src: methodology/farming_system_classifier.md §Decision tree]

### Worked illustration: per-AOI tuning

The classifier document records a tuning for a pilot AOI in Sierra Leone dominated by smallholder rainfed cropping with cocoa and oil-palm systems, small-scale lowland irrigation and modest livestock density. It lowers the irrigation share to 0.10 (small lowland schemes fall below the coarse irrigation map's 20 % threshold), the mixed and agro-pastoral livestock thresholds to 3.0 TLU/km², the pastoral threshold to 15.0, and the tree-perennial threshold to 0.40 (shaded cocoa and oil-palm patches register around 40 % perennial fraction). The same values are carried in a country-scoped binding row. [src: methodology/farming_system_classifier.md §Per-AOI tuning] [src: schema/registers/BIND_dataset_binding.csv]

These overrides are expert adjustments motivated by known biases in the inputs. No pinned file records their validation against census or survey data.

### Fitness limits and validation

The classifier is scoping grade only and must not be used for site-level decisions or project-finance allocation. Its known weaknesses are: [src: methodology/farming_system_classifier.md §Fitness limits]

- **Livestock density is modelled** (dasymetric). Uncertainty is highest in pastoral and mobile-herd contexts, exactly where the pastoral versus agro-pastoral boundary is drawn.
- **Irrigation is coarse.** The 5 arc-minute irrigation map under-estimates small-scale irrigation; the 10 m cropland-and-irrigation product is the recommended auxiliary.
- **Inputs lag.** Cropland 2019, livestock around a 2015 baseline, irrigation around 2013: none reflects land-use change after 2020.
- **Tree cover is undifferentiated.** All tree cover is a candidate for `tree_perennial`, so smallholder shaded cocoa, oil-palm estates and natural forest can be conflated. A planted-forest layer is identified as a high-leverage improvement but is not implemented. Commodity-specific tree-crop maps, finer irrigation maps and cereal-class products are listed as follow-up improvements; crop-allocation maps are noted as weak on tree perennials.

[src: methodology/farming_system_classifier.md §Fitness limits] [src: methodology/farming_system_classifier.md §Dataset improvements]

**Validation rule.** Compare classifier output per AOI with agricultural census data (admin1 statistics on cropping and livestock area), household survey data where it covers the AOI, and expert review. A drift between EO and census statistics greater than 20 % at admin1 should trigger threshold re-tuning, not acceptance of the EO surface as ground truth. [src: methodology/farming_system_classifier.md §Validation (forward)] This rule is specified as forward work; no pinned file records it having been applied.

## Geographic contexts (T7)

[[table:T7]] defines the controlled vocabulary of contexts the pipeline looks up when reading raster or vector data. Each row names a context, its type, the dataset that holds its boundary or classification, the field in that dataset, and the value identifying the context. [src: schema/spec.md §T7]

Context types are `aez`, `farming_system`, `admin_country`, `admin_region` and `hydrobasin`. Contexts can be hierarchical through `parent_context_id`, so a sub-zone can sit within a zone. [src: schema/spec.md §T7]

{{csv:schema/T7_geographic_context.csv|cols=context_id,context_type,context_name,parent_context_id,dataset_id,value_in_dataset,is_active}}

T7 governs open vocabularies by foreign key. A farming-system value used in T3 or T0 must be a T7 row with `context_type = farming_system`, with `all` as the only wildcard. To extend the vocabulary, add a row; never invent a value inline. [src: schema/spec.md §Value governance]

**Two inconsistencies at the pin.** First, the six farming-system rows in T7 name `esa_worldcover_2021` as their classification dataset, while the classifier's documented inputs are the cropland, livestock, irrigation and tree layers above, and the global farming-system binding is a derived run-time layer marked `requires_upload`. The T7 dataset reference should be read as a placeholder for the classifier output. Second, the T0 field description still gives older Dixon-style example values and describes the farming-system vocabulary as FAO/IIASA-sourced; the EO-derived classes supersede both. [src: schema/T7_geographic_context.csv] [src: methodology/farming_system_classifier.md §Input layers (T1)] [src: schema/registers/BIND_dataset_binding.csv] [src: schema/spec.md §T0] [src: schema/registers/FS_DIXON_CROSSWALK.md]

The AEZ rows carry descriptive text, including indicative rainfall and temperature ranges and references to studies from each zone. These descriptions document the context; they are not themselves evidence units and do not set thresholds.

## The data registry (T1)

Every dataset used anywhere must have a [[table:T1]] record, and the pipeline looks datasets up there rather than hardcoding URLs. Which NbS use a dataset is derived from joins, not stored. [src: schema/spec.md §T1]

Key fields and their rules: [src: schema/spec.md §T1]

- `analytical_module` classifies the dataset's role: climate hazard, climate impact, structural suitability, adaptive capacity, exposure, opportunity space or geographic context. Climate datasets also carry `hazard_type` and `scenario_type`.
- `grain_type` is `grid`, `admin` or `vector`. A grid dataset states `spatial_resolution_m`; an admin dataset states `admin_level` (admin0, admin1, admin2) instead. An admin or vector dataset is never given a fictitious resolution in metres.
- `access_type` is direct download, GEE asset, API or proprietary licensed, with `download_url`, `gee_asset_id` or a free-form `access_params` object for endpoints such as STAC collections.
- `description` comes from the provider's official metadata; `citation` is taken from the provider's recommended citation or resolved from the DOI, never hand-authored; `license`, `version` and `limitations` are required.

{{csv:schema/T1_data_registry.csv|cols=dataset_id,analytical_module,grain_type,spatial_resolution_m,admin_level,access_type,version}}

**Spatial grain as a rule, not a field.** For priority variables, the grain used in M4 is derived at run time from `grain_type` and `admin_level`. A priority that resolves only at admin0 (country) becomes a qualified flag rather than a hotspot-discriminating layer; admin1 or finer is required for differentiation within the MCDA. This mirrors the resolution trap on the human-system side. [src: schema/spec.md §T1] [src: schema/spec.md §v0.3.0 change note A]

**Variable-input metadata.** `access_params` may also hold `variable_inputs` per canonical variable: provider-documented asset and band, source units, scale and offset, transformation, available depths, verification details and remaining checks. This metadata does not override a binding, select a depth, assert live access or infer that two measurement methods are equivalent. Unknown metadata stays absent; native unit, scale and temporal reducer remain null until confirmed from the actual asset. [src: schema/spec.md §T1 access metadata: variable inputs] [src: methodology/T4_developer_contract.md §Selections, corrections and rebuilds]

## Server-side-first sourcing

The data-sourcing order is a three-tier preference: GEE catalogue asset, then community-hosted GEE asset, then upload. Fitness for purpose comes first: a better dataset is not replaced by an inferior one because the inferior one is hosted. [src: methodology/framework.md §Dataset sourcing (three-tier preference)]

Within the tiers, server-side hosting is preferred (GEE catalogue, community GEE, then other large catalogue services such as STAC or open-data buckets) over flat-file download. The reason is practical and analytical: resampling, cropping and mosaicking happen on the server before transfer, so download functions stay simple and consistent. Data are pulled into Python and processed with xarray and rioxarray, with GEE reached through xee. Where a fitness-equivalent GEE-hosted version exists, it is used. [src: AGENTS.md §What is locked]

Server-side resampling does not relax the resolution rules. Scale-dependent derivatives such as slope must still be derived at native resolution before aggregation, so a server-side workflow must derive first and aggregate second. [src: methodology/T4_generation_method.md §2.4 Per-variable resolution validity]

## Dataset binding (BIND)

### Purpose

[[table:BIND]] binds a variable to a dataset per geographic context, so a global recipe can be refined for an AOI without forking it. Each variable has a `global` binding as its default; a country, region, hydrobasin, farming system or AEZ can override it with a better local dataset. [src: schema/spec.md §BIND]

BIND chooses *which dataset*. Response *parameters* are refined separately through `T4.context_overrides`. The two refinements are compositional: a country binding can supply a national map while an AEZ override adjusts the response to it. [src: schema/spec.md §BIND] [src: AGENTS.md §What is locked]

Fields: `variable` (a canonical variable), `scope_type` and `scope_id` (a T7 context, blank for global), `dataset_id`, an optional `band` naming the layer within a multi-band asset (for example a bioclimatic band), `preference_rank`, `status` and `fitness_note`. [src: schema/spec.md §BIND]

Status takes three values: `catalogued` (in T1 and fetchable), `community` (community-hosted) and `requires_upload` (a better dataset is known but the user must supply it; `dataset_id` is blank). [src: schema/spec.md §BIND]

### Most-specific context wins

For each variable in an AOI, the resolver collects bindings whose scope matches one of the AOI's T7 contexts (a global binding always matches), sorts them by specificity and then by `preference_rank`, and takes the first. [src: schema/spec.md §BIND] [src: src/nbs_ruralscan/runtime/binding.py]

```formula
specificity:  admin_region (5) > admin_country (4) > hydrobasin (3) > farming_system (2) > aez (1) > global (0)
winner = argmin over matching bindings of (−specificity, preference_rank)
```

- Matching bindings: those with `scope_type = global` or `scope_id` in the AOI's set of T7 context identifiers.
- `preference_rank`: lower is preferred; it breaks ties within the same specificity.

[src: src/nbs_ruralscan/runtime/binding.py]

If the winner is `catalogued` or `community`, its dataset is used. If the winner is `requires_upload`, the resolver falls back to the best fetchable matching binding, sets a needs-upload flag and produces a user prompt naming the preferred dataset and the fallback in use. The substitution is to be recorded in the run configuration and the resolution audit. If no fetchable binding exists, no dataset is returned and the prompt says so. The collected prompts form the AOI's data-gap report. [src: src/nbs_ruralscan/runtime/binding.py] [src: schema/spec.md §BIND]

The same precedence governs `T4.context_overrides`. [src: schema/spec.md §BIND]

**Per-pixel versus per-AOI resolution.** The classifier document says that for variables resolved per farming system (such as `production_gap`), the binding uses the classifier output to choose a dataset per pixel. The pinned resolver works on the AOI's set of contexts and returns one dataset per variable. An AOI containing several farming systems therefore needs per-system resolution performed by the consuming implementation; the pinned resolver does not do it. [src: methodology/farming_system_classifier.md §BIND integration] [src: src/nbs_ruralscan/runtime/binding.py]

### Bindings at the pin

{{csv:schema/registers/BIND_dataset_binding.csv|cols=binding_id,variable,scope_type,scope_id,dataset_id,band,preference_rank,status}}

Reading the table shows how the rules play out:

- **Climate bands from one asset.** Annual precipitation, mean annual temperature and the heat-stress proxy all bind globally to one bioclimatic dataset and select different bands through `band`. [src: schema/registers/BIND_dataset_binding.csv]
- **A country upload outranking a global default.** Cocoa distribution binds globally to a crop-allocation map (physical-area fraction, explicitly not a suitability score) and, for one country, to a national EO cocoa map flagged `requires_upload`. In that country the national map wins on specificity; until it is supplied, the global map is used and the user is prompted. [src: schema/registers/BIND_dataset_binding.csv]
- **Metric resolved per farming system.** `production_gap`, the shortfall against attainable productivity of the dominant farming system, binds per farming-system class: a yield gap for cropping, a net-primary-productivity gap for rangeland, and composites for mixed and agro-pastoral systems. All six bindings are `requires_upload` with no global fallback, so production gap is unavailable until supplied. The livestock side is noted as often thin. [src: schema/registers/BIND_dataset_binding.csv] [src: AGENTS.md §What is locked]
- **Derived layers.** The farming-system layer itself is a `requires_upload` binding describing the classifier recipe and its inputs, with a country-scoped tuned variant. [src: schema/registers/BIND_dataset_binding.csv]
- **Supporting, not proof.** Several system-constraint inputs (grazing system present, managed pasture, field boundary zone, degraded or depleted farmland, farmland context) are `requires_upload` with notes that the available global layers (grassland class, ruminant density) support but do not establish them. [src: schema/registers/BIND_dataset_binding.csv]
- **Complementary ranks.** Distance to water bodies binds first to a stream network derived from a 90 m hydrography dataset and second to a 30 m surface-water layer that covers lakes and wide rivers but not headwaters; the note records that 5 to 30 m evidence bands are finer than the network's meaningful resolution. [src: schema/registers/BIND_dataset_binding.csv]
- **Soft enabling factors.** Accessibility, electrification, tenure, conflict, governance, finance, value-chain and labour variables are bound globally, several at admin0 only with subnational data marked as uploads. These feed the M2b operational stream and hand-off, not the suitability score ([[ch:m2b-project-risk]]). [src: schema/registers/BIND_dataset_binding.csv] [src: AGENTS.md §What is locked]

### `requires_upload` in practice

`requires_upload` is a signal, not a failure. It means a better local dataset is known to exist or to be needed. The runtime proceeds with the fallback where one exists and tells the user what to supply. The method therefore distinguishes three situations that a report should keep apart: data used as intended; data substituted by a global fallback pending upload; and data unavailable (no fallback), where the variable cannot be computed and, if required, the run is blocked at setup ([[ch:m0-setup]]). [src: src/nbs_ruralscan/runtime/binding.py] [src: methodology/modules/M0_setup.md §6. Sub-steps]

A binding does not establish that a response transfers. A target country selects datasets; it does not approve a response observed in another country. [src: methodology/T4_developer_contract.md §Target country and evidence country are different filters]

## Context sensitivity: flag, do not resolve

Variables differ in how freely a global dataset transfers and how politically charged the numbers are. [[table:VONT]] carries this as `context_sensitivity`: [src: methodology/T4_generation_method.md §2.6] [src: schema/spec.md §VONT]

- **`low`**: generalisable physical variables (slope, climate, terrain). A global dataset transfers; set the global binding.
- **`medium`**: context-dependent but not political (soils, land cover, infrastructure). Local data are better where available, through a binding override.
- **`high`**: nationally derived or sovereignty-sensitive (population, poverty, crop production). A global model can diverge from, or appear to contradict, official national figures. The scoping output should recommend a country-endorsed source and treat the global default as provisional.

[src: methodology/T4_generation_method.md §2.6]

Variables flagged `high` at the pin:

{{csv:schema/registers/VONT_variable_ontology.csv|where=context_sensitivity=high|cols=canonical_variable_id,label,canonical_unit}}

**The scope line.** The flag is a label read by Variable Cards, the data-gap prompt and the hand-off. It does not change the analysis. The scan marks the variable and recommends confirmation during feasibility; it does not negotiate, validate or endorse national data. Naming the sensitive variables precisely is part of good scoping; doing the confirmation is not. [src: methodology/T4_generation_method.md §2.6] [src: AGENTS.md §What is locked] [[ch:m6-handoff]] describes how the flags are carried forward.

About a fifth of ontology rows carry no `context_sensitivity` value at the pin; for those, no flag is raised, which should not be read as `low`. [src: schema/registers/VONT_variable_ontology.csv]

## Assumptions and limits

- **Scoping-grade classes.** Farming-system classes come from coarse, partly modelled and dated inputs with untested global thresholds. They are adequate for stratifying evidence and choosing datasets; they are not a land-use map for site decisions.
- **Classes are not validated.** The census-comparison rule (re-tune if drift exceeds 20 % at admin1) is specified but not recorded as applied.
- **Tree cover conflation.** Natural forest, plantations and shaded perennial crops are not separated, which matters for any family gated on tree crops or on natural forest.
- **Registry gaps.** T7 farming-system rows reference a placeholder dataset; some T0 guidance still uses superseded labels; many ontology rows lack a sensitivity flag.
- **Per-AOI binding only.** Per-pixel dataset choice by farming system is described but not implemented in the pinned resolver.
- **Uploads are frequent.** Production gap, farming system and many system-constraint inputs have no catalogued global dataset. A first-pass run will often depend on fallbacks or be unable to compute these variables.
- **Feasibility must still** obtain country-endorsed data for sensitive variables, verify local land use and grazing on the ground, confirm units, depths and temporal support of any uploaded dataset, and validate farming-system boundaries against national statistics.

## Where this is configured

- Contexts (AEZ, farming system, administrative units, hydrobasins): [[table:T7]].
- Datasets, access routes, grain, licence and limitations: [[table:T1]].
- Variable-to-dataset bindings per context, bands and upload flags: [[table:BIND]].
- Canonical variables, units, candidate datasets, resolution limits and context sensitivity: [[table:VONT]].
- Response re-parameterisation per context: `context_overrides` in [[table:T4]].
- Farming systems an NbS applies to: [[table:T0]]; hazard-response cells by farming system: [[table:T3]].
