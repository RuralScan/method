---
title: Scope and analytical framework
slug: scope-and-framework
summary: Explains what decision the Rural NbS Scan supports, how its layers and modules fit together, which principles bind every module, and what the method deliberately does not do.
sources:
  - AGENTS.md
  - methodology/framework.md
  - methodology/README.md
  - methodology/modules/README.md
  - methodology/modules/M1_suitability.md
  - methodology/T4_generation_method.md
  - methodology/T4_developer_contract.md
  - methodology/recipes/water_harvesting.md
  - schema/spec.md
  - reference/R/spatMCDA.R
  - src/nbs_ruralscan/runtime/mcda.py
  - method:handbook/start-here.md
  - method:handbook/implement-a-scan.md
---

## Purpose and the decision supported

The Rural NbS Scan is a method for the spatial prioritisation of nature-based solutions (NbS) in rural, agricultural and forestry landscapes. Its user is an investment task team scoping a rural operation. The scan answers four linked questions for a chosen area of interest (AOI): where a given NbS could be considered, how large its footprint could be, which development priorities (poverty, biodiversity, climate risk, gender and inclusion) that footprint intersects, and what the evidence says the practice can plausibly deliver. [src: AGENTS.md §What this project is]

The method is a **scoping tool, not a feasibility tool**. It does not perform detailed ecosystem-service modelling, full cost-benefit analysis or site-level engineering design. Those activities are downstream of scoping and are pointed to in the implementation hand-off module ([[ch:m6-handoff]]). The governing rule is short: scoping flags, feasibility validates. [src: AGENTS.md §What this project is] [src: methodology/framework.md §What this framework does not do]

Read every output with that boundary in mind. A suitability surface identifies candidate areas for investigation, not land on which a practice will succeed. A scorecard cell summarises what the reviewed literature supports and how strongly, not a measured return for a project. [src: method:handbook/start-here.md §Follow a rule back to evidence]

## Three layers

The method separates three layers so each can change without forcing changes in the others. [src: methodology/framework.md §Architectural layering]

| Layer | Role | Where it lives |
|---|---|---|
| Framework | Cross-cutting methodology, the multi-criteria decision analysis (MCDA) engine, standardisation library and table schema. Independent of any one NbS. | `methodology/framework.md`, `schema/` |
| Recipe | Per-NbS configuration: variables, response functions, weights, sub-practice families, datasets. One recipe per NbS. | `methodology/recipes/<nbs_id>.md` and `schema/recipes/<nbs_id>/` |
| Runtime | A reusable Python package that pulls geospatial data and computes with xarray, rioxarray and xee (Earth Engine to xarray), plus pilot notebooks. | `src/nbs_ruralscan/`, `pipeline/` |

[src: methodology/framework.md §Architectural layering] [src: AGENTS.md §Three layers]

The consequence is that adding an NbS means writing a new recipe and appending schema rows. No code change is required. New analytical methods beyond the inherited primitives (below) require a recorded methodology change and sign-off, not an edit to code. [src: methodology/framework.md §Authoring conventions]

The recipe narratives are explanatory. For current mapping values, evidence support and readiness, the versioned tables and their release reports are authoritative, not the narrative text. [src: methodology/README.md §Which reference answers my question?]

## Seven modules and the M2b addendum

The analysis is organised as seven modules, M0 to M6, plus an addendum module, M2b. Each module has a specification sheet that acts as its input and output contract. [src: methodology/framework.md §Seven analytical modules (+ M2b project-risk addendum)] [src: methodology/modules/README.md §Index]

| Module | Question answered | Tables read | Specification status at the pin |
|---|---|---|---|
| M0 Setup and scope ([[ch:m0-setup]]) | Which NbS, AOI, resolution, climate scenario and risk mode; are the data reachable? | T0, T1, T7 | draft v0.1 |
| M1 Suitability to opportunity space ([[ch:m1-suitability]]) | Where could this NbS biophysically and systemically be considered? | T1, T4, T7 | draft v0.1 |
| M2 Rural climate risk ([[ch:m2-climate-risk]]) | Where are rural **livelihoods** exposed to climate hazards, baseline and future? | T1, T2 | draft v0.1 |
| M2b Project disaster-risk screen ([[ch:m2b-project-risk]]) | Where could hazards damage the **investment**, and where do operational barriers apply? | T2, T3 | draft v0.1 |
| M3 Opportunity-space characterisation ([[ch:m3-characterisation]]) | Who and what is inside the opportunity space (poverty, biodiversity, inclusion, production, population)? | T1, T5 | ratified v1.0 |
| M4 Priority hotspots ([[ch:m4-hotspots]]) | Where within the opportunity space do the task team's priorities concentrate? | T5 | ratified v1.0 |
| M5 NbS scorecard and response ([[ch:m5-scorecard]]) | What can this NbS plausibly address, with what confidence, and at what indicative cost? | T3, T6 | ratified v1.0 |
| M6 Implementation hand-off ([[ch:m6-handoff]]) | What must feasibility work validate next? | T0, T6 | draft v0.1 |

[src: methodology/framework.md §Seven analytical modules (+ M2b project-risk addendum)] [src: methodology/modules/README.md §Index]

"Draft" and "ratified" describe the specification sheets. Neither status means that the module has been run, validated or calibrated in a country application.

### How outputs flow between modules

1. **M0** captures the user's choices, resolves the recipe and dataset bindings, checks every required dataset is reachable, and writes a run configuration that every downstream module reads. [src: methodology/modules/M0_setup.md §5. Dependencies]
2. **M1** reads the run configuration and the family's T4 mappings and produces a continuous suitability surface and an **opportunity-space mask**. [src: methodology/modules/M1_suitability.md §4. Outputs]
3. **M2** may run in parallel with M1; its livelihood-risk surface is displayed alongside the opportunity space. [src: methodology/modules/M1_suitability.md §5. Dependencies]
4. **M2b** is applied as a filter or flag on candidate areas. It is never added to the M2 livelihood-risk index. [src: AGENTS.md §What is locked]
5. **M3** extracts characterisation variables within the M1 opportunity-space mask. **M4** runs a separate priority MCDA constrained to that mask. [src: methodology/modules/M1_suitability.md §5. Dependencies]
6. **M5** does not read M1 rasters. It retrieves scorecard rows for the same NbS identifier. **M6** is narrative and draws on everything upstream. [src: methodology/modules/M1_suitability.md §5. Dependencies]

### Two risk lenses, never summed

The method distinguishes two kinds of risk. M2 measures risk to rural livelihoods: it is a *need* layer and feeds hotspotting. M2b measures risk to the NbS investment itself, following a development-bank disaster-screening lens; it acts as a feasibility filter or scope flag. The two are kept separate and M2b is applied as a filter, never summed with M2. [src: AGENTS.md §What is locked]

M2 has two operational modes. **Mode A** (hazard × exposure) is the default. **Mode B** is the full IPCC AR6 decomposition, risk = hazard × exposure × vulnerability, where vulnerability is a function of sensitivity and adaptive capacity. Mode B is selectable but not default, because vulnerability variables also appear among M3/M4 priorities and using them in both places double-counts. The run records which mode was used so that runs in different modes are not compared by accident. [src: methodology/framework.md §Climate risk formulation] [src: AGENTS.md §What is locked]

## Rules live in tables, not in code

The pipeline reads every analytical rule, dataset reference, response function and weight from schema tables T0 to T7 and the evidence and configuration registers upstream of them. Analytical rules are never hardcoded. The schema is the methodology in machine-readable form. [src: AGENTS.md §Schema (the analytical backbone)] [src: methodology/framework.md §Authoring conventions]

| Table | Purpose |
|---|---|
| [[table:T0]] | NbS registry: one row per NbS; all other tables join on `nbs_id`. |
| [[table:T1]] | Data registry: every dataset used anywhere, with access route, licence, citation and limitations. |
| [[table:T2]] | Climate-risk formulation for M2 and M2b. |
| [[table:T3]] | NbS × hazard × farming system: livelihood mitigation and asset threat. |
| [[table:T4]] | Suitability variable mappings, keyed to suitability family. |
| [[table:T5]] | Opportunity-space (priority and descriptor) variables. |
| [[table:T6]] | Scorecard effects linked to T5 priorities; costs sit in [[table:T6E]]. |
| [[table:T7]] | Geographic context: agro-ecological zones, farming systems, administrative units, hydrobasins. |

[src: schema/spec.md §Table overview]

Two rules keep this principle enforceable. First, each table is a CSV that people edit, plus a typed JSON generated from it; the JSON is never edited by hand and the build fails if it is stale. Second, foreign keys are validated on load: every dataset, NbS, variable, evidence, source and family identifier must exist in its governing table, and a missing target raises an explicit error rather than a silent gap. Open vocabularies such as farming systems and agro-ecological zones are governed by rows in T7, never by values invented inline. [src: schema/spec.md §Implementation notes] [src: schema/spec.md §Value governance]

The column set of every table is frozen in a manifest and machine-validated. Structural changes go through the manifest, never through silent reshaping of data files. [src: AGENTS.md §Schema (the analytical backbone)] The data-model dictionary pages describe each table field by field.

## Evidence-first provenance, in brief

Values in the evidence-based tables (T3, T4, T6) trace a chain: table row → evidence units → source, with tier, page or locator, and verbatim quote. The guiding rule is never to go from a PDF to a threshold in one step. Extraction (what a source says) and synthesis (combining sources into a mapping) are separate stages with a traceable evidence layer between them. [src: methodology/T4_generation_method.md §0. Why this method exists] [src: AGENTS.md §What is locked]

The evidence layer comprises a source register ([[table:SRC]]), an evidence register of atomic claims ([[table:EV]]), a variable ontology ([[table:VONT]]), a family registry ([[table:FAM]]) and a dataset binding registry ([[table:BIND]]). [src: schema/spec.md §Evidence & configuration layer (upstream of T0–T7)]

Six defensibility tenets apply throughout: provenance on every value; no silent inference (missing values are null, not guessed); separation of discovery, evidence, synthesis and sign-off; machine learning may rank *which* variables matter but never sets the *shape* of a response; auditable lumping of variables and sub-practices; and reproducibility of prompts, skills and corpus. [src: methodology/T4_generation_method.md §0. Why this method exists]

Two further distinctions shape what an analyst can claim. A claim about one species or crop (`claim_scope = species_specific` or `crop_specific`) is retained but never sets a practice-level row, except where a recipe explicitly re-admits crop-specific evidence for families whose host crop is the point of the practice. And an approved extraction is not automatically a transferable threshold or an executable rule: variable use, direction and numeric calibration are assessed separately. [src: AGENTS.md §What is locked] [src: methodology/T4_generation_method.md §Directional evidence is distinct from numeric calibration]

Effect tables are produced differently from suitability tables. T3 and T6 rows are generated by synthesis over every evidence unit hitting a cell, with confidence expressed on two axes (evidence and agreement) and a transfer class that labels evidence from outside the target context. Costs are indicative and ordinal, not cost-benefit analysis. [src: AGENTS.md §What is locked] The evidence chapters ([[ch:evidence-principles]], [[ch:suitability-synthesis]], [[ch:effect-synthesis]], [[ch:cost-profiles]]) give the full rules.

## Inherited framework primitives

{{attribution:primitives}}

The framework adopts a small set of analytical primitives as canonical and uses them across all recipes. [src: methodology/framework.md §Inherited framework primitives]

| Primitive | Used by |
|---|---|
| Five fuzzy membership functions (increasing sigmoid, linear, Gaussian, generalised bell, inverted sigmoid) to standardise each criterion to 0–1 | M1, M3, M4 |
| Hybrid weighting: expert analytic hierarchy process (AHP) reconciled with objective CRITIC and entropy weights through a mixing parameter α | M1, M3, M4 |
| Reference MCDA implementation (weighted overlay, classification, sensitivity) | M1, M3, M4 |
| Recipe template column structure | all recipes |
| Sub-practice family pattern | all recipes with within-NbS variation |
| Sensitivity perturbation (±10 % weight shuffle) | M1, M3, M4 |

[src: methodology/framework.md §Inherited framework primitives]

The reference MCDA script was ported from R to a pure-numpy Python module that implements CRITIC, entropy and AHP weights, α-reconciliation, weighted overlay, quartile classification and the perturbation sensitivity run. [src: src/nbs_ruralscan/runtime/mcda.py] Two refinements apply to the inherited set. The schema now holds one canonical list of nine response types (`trapezoidal`, `gaussian`, `linear_increasing`, `linear_decreasing`, `sigmoid`, `inverted_sigmoid`, `threshold`, `ranked_classes`, `piecewise`) that supersedes the earlier "five-function" wording. And the current execution baseline is a weighted linear combination with separate exclusion and eligibility masks, recorded as a baseline rather than a ratified resolution of every earlier design statement. [src: schema/spec.md §Relationship-type reference (`relationship_type` + `relationship_params`)] [src: methodology/T4_developer_contract.md §Aggregation baseline and design history] [[ch:m1-suitability]] gives formulas, parameters and implementation status.

## Suitability is reasoned per family

An NbS is not one suitability problem. Sub-practices are grouped into **suitability families** by their shared dominant limiting factor, the factor that decides where they can go and therefore sets the leading variable and the whole variable set. T4 is keyed to the family, not to the NbS. Every family carries a `spatial_product_type` that determines what can be reported: linear, zonal and qualitative products are never reported as pixel area. [src: AGENTS.md §What is locked] [src: methodology/T4_generation_method.md §2.1 Practice definition → subpractices → suitability families] [[ch:m1-suitability]] sets out the full logic.

## Two-stage variable selection

Every recipe reduces its variables before they enter an MCDA, in two stages. [src: methodology/framework.md §Variable selection (two stages)]

1. **Thematic grouping.** An expert step, done once per NbS when the recipe is built. Variables fall into six standard themes: topographic, hydrological, soil, climatic, land use and land cover, and socio-economic plus hazard.
2. **Correlation-based reduction.** An empirical step, done per AOI. After fuzzy standardisation, compute pairwise correlation, cluster variables with |r| > 0.7, and keep one representative per cluster (the highest-variance member unless an expert has flagged a primary).

[src: methodology/framework.md §Variable selection (two stages)]

Cluster membership is preserved and shown to the user, who in a technical mode may promote any clustered variable to be the representative. One representative per cluster enters the MCDA. Expanding variables into the MCDA without correlation reduction is not permitted. [src: methodology/framework.md §Variable selection (two stages)] [src: AGENTS.md §Don't]

Which variables are candidates in the first place is decided upstream from three signals: literature prevalence (`paper_support_pct = 100 × n_sources / corpus_n`), machine-learning importance, and thematic fit. A variable below a default prevalence floor of 20 % is flagged for a recorded inclusion decision, not dropped automatically, because prevalence reflects convention and citation echo as much as importance. [src: methodology/T4_generation_method.md §6. Synthesis → T4 rows]

## Three-tier dataset sourcing

For each variable, the data registry entry uses the first option that is fit for purpose: [src: methodology/framework.md §Dataset sourcing (three-tier preference)]

1. a Google Earth Engine (GEE) catalogue asset, if a credible one exists;
2. a community-hosted GEE asset;
3. an upload, if the best-fit dataset is not already hosted.

Fitness for purpose precedes platform: a better dataset is not swapped for an inferior one simply because the inferior one is already hosted. Within the tiers, server-side hosting (GEE catalogue, community GEE, then other large catalogue services such as STAC endpoints) is preferred over flat-file download so that resampling, cropping and mosaicking happen before transfer. Data are pulled into Python, with GEE reached through xee rather than a native Earth Engine application. [src: methodology/framework.md §Dataset sourcing (three-tier preference)] [src: AGENTS.md §What is locked] [[ch:farming-systems-and-data]] covers the data registry, context-specific dataset binding and upload flags.

## Spatial standardisation and uncertainty

Datasets are brought to a standard global reference frame and pre-processed at a ladder of resolutions (10 km, 5 km, 1 km, 500 m, 100 m), so analysis resolution is a run parameter. The pipeline produces a resolution audit table recording which inputs are at native resolution and which were resampled. Upsampling by more than one tier triggers a visible warning, because synthetic fine-scale variability is misleading. [src: methodology/framework.md §Spatial standardisation]

Uncertainty is handled pragmatically. Weights are perturbed (±10 % by default) to produce sensitivity maps, and where available the `uncertainty_pct` field of a T4 row is meant to propagate to bands on the final surface. [src: methodology/framework.md §Uncertainty & sensitivity] The evidence base is known to skew optimistic (papers map where a practice works, rarely where it fails); the method responds by deduplicating by source lineage, extracting failure and exclusion thresholds deliberately, and refusing to let a suspiciously tight consensus narrow stated uncertainty. [src: methodology/T4_generation_method.md §6.1 Publication bias & uncertainty (pragmatic)]

## Variable Cards

Each variable a user sees is explained by a Variable Card with six fixed slots: what it is; why it matters for this NbS; how to read it; what it represents (its correlation cluster); where it comes from; and a response preview (membership curve plus raw and transformed maps). [src: AGENTS.md §What is locked] Cards are display metadata that travel with the analysis; they are not analytical inputs. [src: methodology/modules/M1_suitability.md §3. Inputs]

## What is out of scope

The framework does not do any of the following: [src: methodology/framework.md §What this framework does not do]

- ecosystem-service modelling (no InVEST, ARIES or similar);
- site-level feasibility design;
- full cost-benefit analysis (only indicative economic profiles);
- optimisation;
- detailed climate-impact modelling beyond hazard exposure.

It also does not negotiate, validate or endorse national data. Where a variable is nationally derived or politically sensitive, the scan flags it and recommends confirmation with a country-endorsed source during feasibility. [src: methodology/T4_generation_method.md §2.6]

## Assumptions and limits

- **Scoping grade throughout.** Every surface is suitable for identifying where to look next, not for allocating finance or siting works. Field validation, tenure and safeguards checks, community consultation, hydrological or geotechnical assessment, and cost-benefit analysis remain feasibility tasks. [src: methodology/recipes/water_harvesting.md §7.6 Constraints and limitations]
- **Specification is ahead of application.** Five module specifications (M0, M1, M2, M2b and M6) are drafts; M3 to M5 are ratified specifications. No pinned file records a full end-to-end country run validated against ground truth. A published first-pass notebook computes a partial terrain-and-soil index only, with outstanding holds on AOI boundary, transfer of evidence to the target country, soil inputs and legal exclusions. [src: methodology/modules/README.md §Index] [src: method:handbook/implement-a-scan.md §1. Check the inputs before making a map]
- **Design history is not fully reconciled.** Earlier design text describes a limiting-factor minimum for structural suitability; the implementation baseline is a compensatory weighted sum with separate masks. Historical module text includes example thresholds and scenario wording that later routing decisions superseded and that must not be used as hidden thresholds. [src: methodology/T4_developer_contract.md §Aggregation baseline and design history]
- **Evidence optimism.** The literature over-states suitable area. The method's mitigations reduce but do not remove this bias; formal publication-bias statistics are not used because the extracted quantities are thresholds without standard errors. [src: methodology/T4_generation_method.md §6.1 Publication bias & uncertainty (pragmatic)]
- **Global data, local decisions.** Default datasets are global. Context-specific bindings and upload flags mitigate, but do not eliminate, mismatch with national data.

## Where this is configured

- NbS identity and scope: [[table:T0]]; families: [[table:FAM]].
- Datasets: [[table:T1]]; context-specific dataset choice: [[table:BIND]]; geographic and farming-system contexts: [[table:T7]].
- Suitability rules: [[table:T4]], run policies [[table:T4_RUN]], numeric compilation policy [[table:T4_NUMERIC_POLICY]].
- Climate-risk formulation: [[table:T2]]; hazard responses: [[table:T3]].
- Priorities: [[table:T5]]; scorecard effects: [[table:T6]]; indicative costs: [[table:T6E]].
- Evidence layer: [[table:SRC]], [[table:EV]], [[table:VONT]], [[table:XW]], [[table:BANDS]], [[table:TOOL]], [[table:SRCH]].
- Edition-specific versions of these tables: [[ch:editions]]; how to reproduce a release: [[ch:reproduce]].
