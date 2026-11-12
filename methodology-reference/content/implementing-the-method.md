---
title: "Implementing the method: requirements and recommendations"
slug: implementing-the-method
summary: After this chapter the reader will know what any software implementation of the method must respect, what the current runtime implements, what is blocked, and where the engineering recommendations for implementation are kept.
sources:
  - methodology/T4_developer_contract.md
  - AGENTS.md
  - schema/spec.md
  - schema/structure/columns.json
  - schema/recipes/agroforestry/T4_run_policy.csv
  - methodology/modules/M0_setup.md
  - methodology/modules/M1_suitability.md
  - methodology/T4_generation_method.md
  - methodology/weight_normalisation.md
  - src/nbs_ruralscan/runtime/binding.py
  - src/nbs_ruralscan/runtime/numeric.py
  - src/nbs_ruralscan/runtime/categorical.py
  - src/nbs_ruralscan/runtime/mcda.py
  - src/nbs_ruralscan/runtime/effect_rows.py
  - src/nbs_ruralscan/runtime/scorecard.py
  - docs/redesign/index.html
  - docs/redesign/00-config.html
  - runtime:README.md
  - runtime:docs/DESIGN.md
  - runtime:config/runs/agroforestry_planted_first_pass.toml
  - runtime:upstream/PIN.json
  - runtime:src/nbs_runtime/recipe_pin.json
  - method:handbook/implement-a-scan.md
  - evidence:workflows/recipe_release/README.md
  - evidence:workflows/recipe_release/pin.json
---

## Who decides what

An implementation is any software that turns the published recipe tables into maps, tables and briefs for an area of interest. Two kinds of decision govern it.

- **Method rules** say what a correct result is: which variables enter a score, how a value becomes a score, what counts as an exclusion, how unknown values propagate. The method side owns these rules; this chapter states them.
- **Engineering choices** say how a correct result is produced: platform, data access, compute, packaging, testing, interface. The runtime maintainers own these and write their recommendations in the runtime repository.

The work is split across repositories.

| Repository | What it holds | Changes analytical values? |
|---|---|---|
| Producer (the evidence and schema repository read at the pinned commit) | Evidence registers, recipe tables T0 to T7, approved run policies, generated developer packages | Yes, through review and regeneration |
| Method and evidence product repositories | The public handbook, cookbook and data-model specification; reproducible checks of the compiled recipe release | No; they verify and explain |
| Runtime | Data access, rasters, run execution, outputs, run manifests, notebooks | Never |

The producer publishes immutable developer packages; the runtime publishes results and never changes values [src: runtime:docs/DESIGN.md §Boundary]. The developer table is a non-authoritative view: corrections belong upstream in the CSV registers [src: methodology/T4_developer_contract.md §Purpose and status].

An implementation therefore never restates or edits a method value; it reports contract gaps to the producer instead of fixing values locally [src: runtime:README.md §Rules (from the CIAT handoff)]. The evidence path behind each mapping is described in [[ch:suitability-synthesis]].

## Requirements any implementation must meet

Requirements are numbered continuously so that a test or code review can cite them.

### Inputs and pinning

1. **Read every analytical rule from the tables; hardcode none.** Thresholds, functions, weights, gates and datasets come from the recipe tables and developer package, because a hardcoded value cannot be traced or updated [src: AGENTS.md §What is locked] [src: methodology/modules/M1_suitability.md §11].
2. **Use the compiled developer contract, not the raw mapping table.** The full-corpus mapping snapshot in a package is for provenance only, because it is unfiltered and unresolved [src: methodology/T4_developer_contract.md §Developer table and related files].
3. **Treat a package version as immutable and pin it.** A new version is a new folder, never an edit, and updating is a deliberate act, because following the producer's main branch automatically would silently change analytical results [src: runtime:docs/DESIGN.md §Updating from CIAT].
4. **Record the release identifier, source revision and function fingerprints with every run.** A fingerprint binds a selection to the inspected function content, so a stale decision cannot select a changed rule; a changed fingerprint holds the policy until revalidated [src: methodology/T4_developer_contract.md §Selections, corrections and rebuilds] [src: methodology/T4_developer_contract.md §Approved first-pass policy].
5. **Verify a package against its manifest before use, and expect a newer checkout to fail.** Hash verification establishes consistency with the recorded inputs, not authenticity of the research or a new approval [src: methodology/T4_developer_contract.md §Verify a delivered package].
6. **Never combine results, rows or counts from different editions.** Each run records its pin so that results from different package versions stay distinguishable [src: runtime:docs/DESIGN.md §Updating from CIAT]. The editions of the recipe release are described in [[ch:editions]].

### Scoring

7. **Unknown is never zero.** Missing inputs and values outside or between disagreeing intervals stay unknown, with coverage reported, because a zero reads as "unsuitable" and a mean fill reads as data [src: methodology/T4_developer_contract.md §Aggregation baseline and design history] [src: src/nbs_ruralscan/runtime/numeric.py].
8. **Gates and masks carry no weight.** Host eligibility and legal exclusion are separate, non-compensatory gates, because in a weighted sum a zero can be offset by high scores elsewhere [src: methodology/T4_developer_contract.md §Planted host and exclusion contracts] [src: docs/redesign/00-config.html §C.3].
9. **Resolve exclusion and unknown by explicit precedence, not by multiplying by a mask.** A known exclusion dominates unknown inputs; otherwise an unknown required gate propagates unknown; the implementation must define and test this precedence [src: methodology/T4_developer_contract.md §Aggregation baseline and design history].
10. **Fix the criterion set and weights before evaluation; never renormalise per pixel.** Renormalising over whichever inputs are present would silently change the index from pixel to pixel [src: methodology/T4_developer_contract.md §Aggregation baseline and design history].

```formula
S(x) = Σ_{j ∈ J} w_j × f_j(x),   w_j ≥ 0,   Σ_{j ∈ J} w_j = 1
```

where `S(x)` is the suitability score at location x, `J` the declared criterion set, `w_j` the run weight of criterion j, and `f_j(x)` the selected response of criterion j at x. If any required `f_j(x)` is unknown, `S(x)` is unknown [src: methodology/T4_developer_contract.md §Aggregation baseline and design history].

11. **Do not execute a held, unrecorded, partial or unselected mapping.** A held mapping documents a reviewed decision and has no selectable scoring function; a function with a known uncompiled continuation is partial and cannot be selected; numeric responses require an explicit selection [src: runtime:README.md §Read a six-practice recipe release] [src: methodology/T4_developer_contract.md §One dashboard for inspection] [src: methodology/T4_developer_contract.md §Selections, corrections and rebuilds]. What "held" means is explained in [[ch:suitability-synthesis]].
12. **Evaluate ordinal intervals as published: no interpolation or extrapolation.** Respect endpoint inclusivity; class scores are a documented convention, not calibrated probabilities [src: methodology/T4_developer_contract.md §Relationship functions and cross-paper harmonisation].
13. **Respect each mapping's execution role.** A row is an M1 numeric score, a host gate, a hard exclusion, an operational scenario or reference-only evidence, and only the first contributes to the weighted score [src: methodology/T4_developer_contract.md §Developer table and related files].
14. **Keep operational factors outside the suitability score.** Road and market access, tenure, finance, extension and labour are operational scenarios or project-risk inputs; only hard exclusions such as legal protected areas, water bodies and built-up land are suitability masks [src: methodology/T4_developer_contract.md §Module boundaries and output meaning] [src: AGENTS.md §What is locked].
15. **Do not treat literature weights or study counts as run weights.** Source-model importance is diagnostic and supplies sensitivity alternatives; counts describe inclusion within a cohort [src: methodology/T4_developer_contract.md §Counts, importance and runtime weights] [src: methodology/weight_normalisation.md §Scope].

### Spatial handling

16. **Report each family's output according to its spatial product type.** Applicability-zone, zonal-linear and qualitative-only products are never reported as pixel area, because a linear practice occupies a small fraction of a pixel and the over-estimate grows with pixel size; report length, density or qualitative extent instead [src: methodology/T4_generation_method.md §2.4 Spatial product type & the resolution trap] [src: AGENTS.md §What is locked].
17. **Do not run a variable coarser than its minimum meaningful resolution without flagging it.** The binding variable, the most resolution-sensitive selected one, sets the run's maximum coarseness; the resolution audit flags any breach [src: methodology/T4_generation_method.md §Per-variable resolution validity] [src: methodology/modules/M0_setup.md §8].
18. **Derive, then aggregate.** Compute derivatives such as slope at native resolution, then summarise to the grid, because coarse slope flattens and biases suitability upwards [src: methodology/T4_generation_method.md §Per-variable resolution validity].

### Data

19. **Resolve datasets by most-specific context.** Precedence is admin region, admin country, hydrobasin, farming system, AEZ, global, with ties broken by preference rank [src: schema/spec.md §BIND] [src: src/nbs_ruralscan/runtime/binding.py].
20. **Never hide an upload-required dataset.** When the winning binding requires upload, use the best catalogued binding, flag the user and record the substitution; M0 additionally blocks a run when a required dataset is unreachable and has no upload path [src: schema/spec.md §BIND] [src: methodology/modules/M0_setup.md §6].
21. **Prefer server-side hosting.** Within the three sourcing tiers (Earth Engine catalogue, community-hosted, upload), take a fitness-equivalent server-side version so that cropping and resampling happen before transfer; data are pulled into Python for computation [src: AGENTS.md §What is locked].
22. **Confirm native units and scale; convert once.** Native unit, scale and temporal reducer remain null in the package until confirmed against actual asset metadata; for multi-layer soil inputs the order is scale, then thickness-weighted summary, then response, and a missing layer propagates unknown [src: methodology/T4_developer_contract.md §Selections, corrections and rebuilds] [src: methodology/T4_developer_contract.md §Dataset preparation proposals and source compatibility].
23. **Keep the target country and the evidence country apart.** A target country resolves dataset bindings; it does not assert that a response from another country transfers [src: methodology/T4_developer_contract.md §Target country and evidence country are different filters].
24. **Flag sensitive variables; do not resolve them.** Variables with high context sensitivity (population, poverty, production statistics) carry a recommendation for a country-endorsed source; the flag does not change the analysis [src: schema/spec.md §VONT].

### Risk and effects

25. **Never sum the two risk lenses.** Risk to livelihoods (M2) is a need layer feeding hotspots; risk to the investment (M2b) is a filter or flag applied to the opportunity space [src: AGENTS.md §What is locked] [src: methodology/T4_developer_contract.md §Module boundaries and output meaning]. See [[ch:m2b-project-risk]].
26. **Select effect rows by most-specific scope and carry their confidence and transfer class.** A global row that is out of context for the area of interest returns `no_applicable_evidence`, which is a valid output: show the gap, never the class as if it applied [src: src/nbs_ruralscan/runtime/effect_rows.py] [src: AGENTS.md §What is locked]. See [[ch:m5-scorecard]].

### Outputs

27. **Write a run manifest.** It records adoption of input proposals, decision references, actual bands, provider and version, scale application, spatial processing and sensitivity outputs [src: methodology/T4_developer_contract.md §Dataset preparation proposals and source compatibility]; M0 specifies recipe, schema and dataset versions in the run configuration [src: methodology/modules/M0_setup.md §6].
28. **List holds; do not hide them.** Outstanding choices (transfer, dataset reconciliation, legal mask, local host inputs, final criteria and weights) remain visible, and every readiness state retains `execution_ready=false` until a spatial run is validated [src: methodology/T4_developer_contract.md §Acceptance and limitations] [src: methodology/T4_developer_contract.md §Reconciled implementation readiness].
29. **Keep pixel states and coverage apart.** Scored, excluded and unknown are distinct states; a partial host fraction is retained as its own layer and never multiplied into the score [src: methodology/T4_developer_contract.md §Approved first-pass policy].

**Where sources disagree.** The M1 module text applies exclusions "as a hard filter" with excluded cells set to 0, and lists a slope cut-off among the masks [src: methodology/modules/M1_suitability.md §6.5]; the developer contract keeps an explicit excluded state, forbids reliance on mask multiplication, and states that historical M1 text must not supply hidden thresholds [src: methodology/T4_developer_contract.md §Aggregation baseline and design history]. M1 derives weights by hybrid AHP, CRITIC and Entropy reconciliation [src: methodology/modules/M1_suitability.md §6.4], whereas the only approved run policy uses fixed design weights [src: schema/recipes/agroforestry/T4_run_policy.csv]. The schema's scenario note sets a toggled-off variable's suitability to 1.0 inside the composite surface [src: schema/spec.md §Implementation notes], while the contract keeps soft operational factors out of the M1 score. In each case the developer contract is the current implementation baseline; it records the baseline without claiming to resolve every earlier design statement [src: methodology/T4_developer_contract.md §Aggregation baseline and design history].

## What the runtime implements today

The runtime is a Python package with notebooks that reads one pinned developer package and turns it into spatial results [src: runtime:README.md].

**Scope.** It implements one approved policy for one family: the planted-silvoarable family of [[practice:agroforestry]]. The score is a partial terrain-and-soil index of three criteria, plus a host gate and a legal-exclusion mask; the runtime README calls it "not complete agroforestry suitability" [src: runtime:README.md]. The approved policy is the pinned producer file:

{{csv:schema/recipes/agroforestry/T4_run_policy.csv|cols=variable_group,rule_id,group_weight,criterion_weight,aggregation,sensitivity_aggregation,missing_values}}

Terrain and soil each take half of the weight, soil split equally between organic carbon and pH; aggregation is a weighted linear combination with a minimum-factor sensitivity, and unknown values propagate. The responses come from compatible pools of Indian planted-silvoarable sources, and the policy requires a transfer decision for any target [src: methodology/T4_developer_contract.md §Approved first-pass policy] [src: schema/spec.md §T4_RUN].

**Kind of index.** The runtime evaluates stepwise ordinal intervals without interpolation, applies host gates on exact class codes, and combines scores into `excluded`, `unknown` or `scored` states, passing the eligible fraction through separately [src: runtime:src/nbs_runtime/responses.py] [src: runtime:src/nbs_runtime/gates.py] [src: runtime:src/nbs_runtime/aggregate.py]. The aggregation logic is inferred from the producer's six policy cases, and the runtime runs those plus 40 response cases as tests [src: runtime:docs/DESIGN.md §What we inherit].

**Grid and data.** The configured area is a placeholder bounding box over Haiti with no recorded boundary source; the target country is set for binding only, with the applicability decision empty [src: runtime:config/runs/agroforestry_planted_first_pass.toml]. The detailed run uses a 250 m grid because SoilGrids, half the weight, is native at 250 m. Slope is derived from SRTM at about 30 m and then averaged; soil uses SoilGrids at 0 to 5, 5 to 15 and 15 to 30 cm, converted once and thickness-weighted; land cover is stored as WorldCover class shares per cell. Earth Engine is reached through xee in tiles and each layer is cached [src: runtime:docs/DESIGN.md §Layers, resolution and the cache]. A quick overview at 5 km skips the host gate and averages inputs before applying functions; it is not a substitute for the 250 m calculation [src: runtime:docs/DESIGN.md §Two ways to run].

**Modes.** In `policy` mode every non-excluded pixel is unknown, because no legal mask has been assessed; in `exploratory` mode the legal mask is not applied and every map and manifest says so. Synthetic data exercise the pipeline offline and are never reported as a place [src: runtime:docs/DESIGN.md §Overview and sensitivity].

**Ordinal simulation.** Because class scores are a convention, the runtime keeps the class order and the class each pixel falls in, and redraws class scores many times in increasing order, giving a median and a 5 to 95% range beside the producer's own index. It quantifies sensitivity to the scale and weights only; it uses an uninformative prior, so its median sits below the convention, and it is not validation [src: runtime:docs/DESIGN.md §Ordinal simulation].

**Variable audit.** A second notebook inspects variables one at a time (map, histogram, range, no-data share, plausibility check), reading each variable's role from the pinned package rather than its own catalogue. It is inspection, not an input to the index [src: runtime:docs/DESIGN.md §Variable audit].

**Pinning.** The developer package is copied read-only with its producer commit and file hashes; the sync script refuses a file that disagrees with the producer's manifest [src: runtime:docs/DESIGN.md §Updating from CIAT] [src: runtime:upstream/PIN.json]. Separately, a reader verifies a six-practice recipe release against a bundled pin (release identifier, source revision, practice list) and reports each practice's spatial execution status [src: runtime:README.md §Read a six-practice recipe release] [src: runtime:src/nbs_runtime/recipe_pin.json]. Each run records a fingerprint of its configuration and area next to the package pin, and saves outputs with a manifest [src: runtime:docs/DESIGN.md §Run configuration] [src: runtime:README.md §Quickstart].

**On hold.** The planner reports as holds: the boundary and its source, the transfer decision, adoption of the soil input proposal, and the assessed legal mask [src: method:handbook/implement-a-scan.md §1. Check the inputs before making a map].

The runtime's pinned recipe release has a different release identifier and source revision from the release this reference is built on [src: runtime:src/nbs_runtime/recipe_pin.json] [src: evidence:workflows/recipe_release/pin.json]. Read runtime results against the runtime's own pin and do not compare figures arithmetically across the two; see [[ch:editions]].

## From the seven stages to components

The visual methodology presents an idealised implementation in seven stages plus a technical configuration page, using example data; it is a design aid, not a working tool [src: docs/redesign/index.html §H.3 How the method flows]. The walkthrough is in [[ch:scoping-walkthrough]].

| Stage | What an implementation needs | Method chapter | State today |
|---|---|---|---|
| 01 Setup | User choices of practice, family, area, resolution, climate mode and scenarios; recipe resolution; data-readiness and ingestion checks; a run configuration | [[ch:m0-setup]] | Partly implemented: one TOML run configuration, bounding-box area and a hold report; the M0 readiness report and ingestion check are specified, not implemented |
| Technical configuration | Binding resolution and upload prompts; inspection of response functions, masks, correlation clusters and class breaks | [[ch:farming-systems-and-data]], [[ch:m1-suitability]] | Binding resolver exists in the producer code, not in the runtime; datasets are fixed for the first pass; variable audit notebook covers inspection only |
| 02 Explore the practices | Practice definitions, families, effect and cost rows | [[ch:m5-scorecard]], [[ch:cost-profiles]] | Tables readable through the runtime's recipe-release reader; no presentation layer |
| 03 Opportunity space | Per-family suitability: responses, host gates, hard masks, correlation reduction, weights, classification, footprint by product type; then livelihood risk (M2) and characterisation (M3) within it | [[ch:m1-suitability]], [[ch:m2-climate-risk]], [[ch:m3-characterisation]] | One family, three criteria implemented as a partial index; legal mask blocked; other criteria blocked by held calibration; correlation reduction, classification, M2 and M3 specified, not implemented |
| 04 Project risk | Asset hazard exposure (Stream A) and operational levers (Stream B), applied as a filter | [[ch:m2b-project-risk]] | Specified, not implemented; some operational variables load in the audit notebook for inspection only |
| 05 Priority hotspots | Priority layers, correlation reduction, user and objective weights, overlay, sensitivity, ranking | [[ch:m4-hotspots]] | Specified, not implemented in the runtime; a numpy port of the reference MCDA exists in the producer code |
| 06 NbS comparison | Effect rows resolved for the area with confidence and transfer class; cost profiles; comparison within product type | [[ch:m5-scorecard]], [[ch:effect-synthesis]] | Rows generated; scope resolver exists in the producer code; not implemented in the runtime |
| 07 Next steps | Shortlist, holds and local checks assembled into a scoping brief | [[ch:m6-handoff]] | Specified, not implemented |

Sources for the state column: [src: runtime:docs/DESIGN.md §Layout] [src: runtime:README.md] [src: src/nbs_ruralscan/runtime/binding.py] [src: src/nbs_ruralscan/runtime/mcda.py] [src: src/nbs_ruralscan/runtime/effect_rows.py].

## What blocks a full implementation

**Held and unrecorded calibration.** Many suitability mappings have reviewed evidence of use or direction but no approved numerical calibration; such a mapping has no scoring function and cannot be executed (requirement 11). Counts by practice are in [[ch:status]]. Transcription and approval of variable use do not approve calibration [src: methodology/T4_generation_method.md §Numeric plausibility before recipe calibration].

**Practices with no suitability mappings.** The forest restoration and mangrove restoration mapping tables are empty at the pin [src: schema/recipes/forest_restoration/T4_suitability_mappings.csv] [src: schema/recipes/mangrove_restoration/T4_suitability_mappings.csv]. Only agroforestry has an approved run policy [src: schema/recipes/agroforestry/T4_run_policy.csv].

**Open module steps.** M0 leaves open whether a multi-practice run uses one configuration or several, how an upload is ingested, and the default administrative level [src: methodology/modules/M0_setup.md §11]. The contract cannot certify area-specific correlation reduction or objective weights without spatial data [src: methodology/T4_developer_contract.md §Aggregation baseline and design history]. The disagreements listed under the requirements remain unresolved in the source text.

**Datasets.** Bindings with `requires_upload` need a user-supplied local dataset before the better source can be used [src: schema/spec.md §BIND]. Native unit, scale and temporal reducer fields stay null until confirmed [src: methodology/T4_developer_contract.md §Selections, corrections and rebuilds]. The legal gate needs an assessed boolean mask for the jurisdiction; absence from a global protected-area layer is not a legal assessment [src: methodology/T4_developer_contract.md §Planted host and exclusion contracts].

**Inputs awaiting confirmation in the runtime design note.**

- Applicability of the source pools to the target, and the official boundary and its source.
- Adoption or replacement of the 0 to 30 cm soil proposal, with a decision reference.
- An assessed legal mask; until then policy mode returns unknown.
- Host inputs (a documented local source for the grassland class), Earth Engine adapters, and band and unit contracts.
- Whether the default precipitation and temperature binding (CHELSA) or the hosted alternative (WorldClim) is intended.
- Whether coarse cells should be scored from mean inputs or by scoring fine cells and averaging; the method's derive-then-aggregate rule asks for a within-pixel distribution, which the first pass does not carry.
- Two readings of host eligibility: eligible when any fine cell is, and unknown rather than excluded when no host is eligible but some is unknown.

[src: runtime:docs/DESIGN.md §Open decisions (owner)] [src: runtime:docs/DESIGN.md §Overview and sensitivity] [src: runtime:docs/DESIGN.md §Variable audit] [src: methodology/T4_generation_method.md §Per-variable resolution validity]

## Recommendations for technical implementation

These recommendations are the runtime maintainers' to write and are kept in the runtime repository, [RuralScan/runtime](https://github.com/RuralScan/runtime); this section lists what they need to cover and will link to them when published. Each row states the question, the method constraint that bounds any answer, and what the runtime design note already says.

| Topic | Question to answer | Method constraint | Current answer |
|---|---|---|---|
| Platform and delivery form | Notebook, installable package, service, or a combination? | Rules read from tables (1); notebooks are the minimum delivery form [src: AGENTS.md §What is locked] | A Python package with two notebooks and a run configuration file [src: runtime:docs/DESIGN.md §Layout]. Service form: to be written |
| Data access and caching | How are layers fetched, cached and invalidated? | Server-side first (21); units confirmed and converted once (22) | Earth Engine through xee in tiles, a per-layer cache keyed by grid and assets so a new package reuses it [src: runtime:docs/DESIGN.md §Layers, resolution and the cache] |
| Compute and scaling | How does cost grow with area and resolution, and what runs large areas? | Resolution validity (17, 18) bounds how coarse a run may go | Cost is set by fine pixels read; polygons and batch exports suggested for large areas [src: runtime:docs/DESIGN.md §Layers, resolution and the cache]. Scaling targets: to be written |
| Grid and resolution policy | How is the grid chosen per run and per variable? | Binding variable sets maximum coarseness; derive then aggregate (17, 18) | 250 m set by the soil input; results, not inputs, summarised to coarse blocks [src: runtime:docs/DESIGN.md §Overview and sensitivity]. General policy for other families: to be written |
| User uploads and licensed data | How are uploads validated, stored and recorded, and how are licences respected? | Upload-required bindings flagged and substitutions recorded (20); sensitive variables flagged (24) | To be written |
| Conformance testing | How is agreement with the developer contract demonstrated? | Contract tests on small synthetic arrays are not pilot validation [src: methodology/T4_developer_contract.md §Acceptance and limitations] | Producer response and policy cases run as tests [src: runtime:docs/DESIGN.md §What we inherit]. Coverage of later modules: to be written |
| Release pinning and upgrade | How is a new package or release adopted? | Immutable versions; fingerprint changes hold policies (3, 4) | New folder per version, hash-checked sync, tests, one change per upgrade [src: runtime:docs/DESIGN.md §Updating from CIAT] |
| Reproducibility and run manifests | What is recorded so a result can be reproduced? | Manifest contents (27); holds listed (28) | Configuration and area fingerprints, package pin, simulation seed, outputs saved with a manifest [src: runtime:docs/DESIGN.md §Run configuration] [src: runtime:config/runs/agroforestry_planted_first_pass.toml]. Manifest schema: to be written |
| From one family to multi-practice scans | How does the runtime grow beyond one family and module? | Per-family reasoning and product types (16); two risk lenses (25) | Tables for later modules are added to the allow-list as each module starts [src: runtime:docs/DESIGN.md §What we inherit]. Architecture: to be written |
| User interface options | What interfaces, from notebooks to the full realisation in the visual methodology? | Holds, unknowns and labels must stay visible (28, 29) | Notebooks only; anything further: to be written |

## Assumptions and limits

- Passing conformance cases shows response semantics are honoured on small arrays, not that data adapters, legal masks or transfer are valid [src: methodology/T4_developer_contract.md §Verify a delivered package].
- No file at the pin records a validated spatial run. Every readiness state keeps `execution_ready=false` [src: methodology/T4_developer_contract.md §Reconciled implementation readiness]. Runtime maps are partial, exploratory or synthetic as labelled.
- The current first pass is a partial terrain-and-soil index from regional source pools. It is not full suitability, does not establish plantable area, and does not approve transfer to the configured target. A national estimate of area needs a boundary, host data, exclusion masks, a supported resolution and resolved applicability [src: method:handbook/implement-a-scan.md §2. Run and interpret the first pass].
- Scoping flags; feasibility validates. A feasibility study must still confirm land use, tenure, safeguards, legal restrictions, local data and site design.
- Statements about the runtime reflect its published main branch and may age.

## Where this is configured

- Suitability mappings and their roles: [[table:T4]]; approved run policies: [[table:T4_RUN]]; numeric harmonisation: [[table:T4_NUMERIC_POLICY]].
- Families and product types: [[table:FAM]]; variables, minimum resolution and context sensitivity: [[table:VONT]].
- Datasets and access metadata: [[table:T1]]; context-aware bindings: [[table:BIND]]; geographic contexts: [[table:T7]].
- Risk and effects: [[table:T2]], [[table:T3]], [[table:T6]], [[table:T6E]].
- The column structure of every table is frozen in `schema/structure/columns.json` [src: schema/structure/columns.json].
- Engineering choices, run configurations and manifests live in the runtime repository; reproduction of the recipe release is described in [[ch:reproduce]].
