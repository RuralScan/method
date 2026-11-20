---
title: "M2b: Project disaster risk screen"
slug: m2b-project-risk
summary: After this chapter you can build and apply the investment-risk screen (Stream A asset hazard exposure from T2 and T3, Stream B operational and enabling-environment factors) as a filter or flag on the opportunity space, and know which parts are specified, generated or still open.
sources:
  - methodology/modules/M2b_project_risk.md
  - AGENTS.md
  - methodology/T3_T6_generation_method.md
  - method:data-model/evidence-classification.json
  - schema/lookups/wocat_hazard_map.csv
  - src/nbs_ruralscan/recipe/cell_synthesis.py
  - methodology/effect_evidence_followups.md
  - schema/structure/columns.json
  - schema/spec.md
  - src/nbs_ruralscan/recipe/synthesis.py
  - schema/recipes/agroforestry/T4_suitability_mappings.csv
  - schema/registers/VONT_variable_ontology.csv
  - methodology/opportunity_space_T5.md
  - schema/lookups/README.md
  - methodology/RULESET_VERSIONS.md
  - schema/lookups/m2b_variable_policy.csv
  - method:handbook/implement-a-scan.md
  - schema/recipes/forest_restoration/T3_nbs_hazard_farming.csv
  - schema/recipes/agroforestry/T3_nbs_hazard_farming.csv
  - schema/recipes/riparian_buffer/T3_nbs_hazard_farming.csv
  - schema/recipes/agroforestry/T0_nbs_registry.csv
  - schema/recipes/forest_restoration/T0_nbs_registry.csv
  - schema/recipes/mangrove_restoration/T0_nbs_registry.csv
  - schema/recipes/riparian_buffer/T0_nbs_registry.csv
  - schema/recipes/water_harvesting_conservation/T0_nbs_registry.csv
  - schema/recipes/wetland_management/T0_nbs_registry.csv
---
## Question this module answers

Module 2b (M2b) asks: if the task team invests in this nature-based solution (NbS) here, how exposed is that investment to disasters that could damage or destroy it, today and under mid-century climate change, and how thin is the operating environment it would depend on? [src: methodology/modules/M2b_project_risk.md §3] [src: methodology/modules/M2b_project_risk.md §12]

It is the spatial, scoping-grade expression of the development-bank Climate and Disaster Risk Screening approach, whose four steps (exposure, impacts, adaptive capacity, overall risk rating) broadly align with the IPCC AR6 decomposition of risk into hazard, exposure and vulnerability. [src: methodology/modules/M2b_project_risk.md §1]

### Two risk lenses

M2 maps risk to rural **livelihoods**: a need layer that feeds hotspots. M2b maps risk to the **investment**: a feasibility screen applied as a filter or flag. The two are distinct and never summed, with each other or with suitability. [src: AGENTS.md §What is locked] [src: methodology/modules/M2b_project_risk.md §2]

| | M2, risk to livelihoods | M2b, risk to the investment |
|---|---|---|
| Question | Where are people and production exposed to hazards the practice can mitigate? | Where could hazards damage the practice, and where is the enabling environment thin? |
| Hazards | T3 rows with `risk_role ∈ {livelihood_mitigation, both}` | T3 rows with `risk_role ∈ {asset_threat, both}` |
| Exposure | Rural population, farms, production | The investment footprint and supporting infrastructure |
| Role | Priority layer in M4 | Filter or flag on the opportunity space and hotspots |

[src: methodology/modules/M2b_project_risk.md §2] [src: methodology/T3_T6_generation_method.md §1]

The same hazard family can sit in both lenses with opposite roles. A created wetland reduces downstream flooding for farmers (M2 need driver), while storm surge can destroy the wetland (M2b asset threat). [src: methodology/modules/M2b_project_risk.md §2]

### What M2b is not

- It is not the full project-level disaster risk screening, which is qualitative, multi-criteria and done at appraisal. M2b is an indicative spatial screen; the full screening is a downstream step pointed to in [[ch:m6-handoff]]. [src: methodology/modules/M2b_project_risk.md §3] [src: methodology/modules/M2b_project_risk.md §10]
- It does not model engineering failure modes or site design. [src: methodology/modules/M2b_project_risk.md §3]
- It is never added to the suitability index or the hotspot score. [src: methodology/modules/M2b_project_risk.md §7]

The principle is "scoping flags; feasibility validates": M2b shows where the investment is fragile or the enabling environment is thin; validation, free prior and informed consent (FPIC) and safeguard compliance happen downstream. [src: methodology/modules/M2b_project_risk.md §12]

## Inputs

| Input | Where it comes from | Stream |
|---|---|---|
| Selected practice, AOI, resolution, scenarios | [[table:T0]], [[table:T7]], run configuration (same as M2) | A and B |
| Asset-threat hazards and their sensitivity and weight | [[table:T3]] rows with `risk_role ∈ {asset_threat, both}`: `asset_sensitivity`, `asset_risk_weight`, `timescale_of_effect`, `confidence`, `applicability` | A |
| Hazard layers | [[table:T2]] hazard rows, through [[table:T1]] and [[table:BIND]] | A |
| Establishment period | [[table:T0]] `establishment_period_years` | A |
| Investment footprint | The M1 opportunity space ([[ch:m1-suitability]]) | A and B |
| Operational and enabling-environment variables | [[table:VONT]] variables bound through [[table:BIND]]; evidence with `use_role = operational_risk` in [[table:EV]] | B |

[src: methodology/modules/M2b_project_risk.md §4] [src: methodology/T3_T6_generation_method.md §1] [src: methodology/modules/M2b_project_risk.md §12]

## Method, Stream A: asset hazard exposure

Stream A combines T2 hazard layers with the T3 asset-threat rows, for baseline and future, modulated by the practice's establishment period. [src: methodology/modules/M2b_project_risk.md §12] [src: AGENTS.md §What is locked]

### Step A1. Scope the asset-threat hazards

From T3, take the practice's rows with `risk_role ∈ {asset_threat, both}`. This set is the complement of the M2 mitigation set in role, though a hazard can appear in both. If the practice has no screened asset hazard, M2b returns an explicit "no screened asset hazards" result, not an empty raster. [src: methodology/modules/M2b_project_risk.md §6]

### Step A2. Accepted asset-threat judgments

AI synthesises the `asset_vulnerability` evidence into proposed sensitivity,
confidence, applicability and rationale. Source-provenanced evidence and an exact
scientific acceptance are required. `nbs_effect` claims about livelihood protection
do not establish asset resilience. The workflow is described in [[ch:effect-synthesis]].

### Step A3. Asset-threat-only hazards

`sedimentation`, `extreme_rainfall` and `landslide` remain descriptive asset threats
where no corresponding T2 layer exists. Do not manufacture a mapped surface from a
textual sensitivity judgment. These hazards do not enter the six-hazard weighted set.

### Step A4. Use accepted weights without filling gaps

AI may propose asset weights with an explicit scientific rationale. Code checks
that the accepted set covers drought, flood, heat stress, fire, wind/cyclone and
waterlogging, and that weights sum to one. It never derives weights from sensitivity
ranks. Missing, stale, held or out-of-context weights mean no accepted weighted
assessment; there is no automatic equal-weight substitution. Historical outputs
retain their original provenance and are not defaults for the accepted workflow.

### Step A5. Read the vulnerability window with the establishment period

On asset-threat rows, `timescale_of_effect` means the **vulnerability window**, for example `short_term_1_3yr` for an establishment-period threat. It is to be read together with T0 `establishment_period_years`. [src: methodology/T3_T6_generation_method.md §7.5] [src: schema/spec.md §T3] The rationale is that a long-horizon investment is more exposed to slow-onset climate change than a short one: a 30-year tree-crop investment faces more change than a 3-year annual-cropping intervention. [src: methodology/modules/M2b_project_risk.md §12]

The establishment periods recorded per practice are:

{{csv:schema/recipes/agroforestry/T0_nbs_registry.csv|cols=nbs_id,establishment_period_years,time_to_benefit_years}}

{{csv:schema/recipes/forest_restoration/T0_nbs_registry.csv|cols=nbs_id,establishment_period_years,time_to_benefit_years}}

{{csv:schema/recipes/mangrove_restoration/T0_nbs_registry.csv|cols=nbs_id,establishment_period_years,time_to_benefit_years}}

{{csv:schema/recipes/riparian_buffer/T0_nbs_registry.csv|cols=nbs_id,establishment_period_years,time_to_benefit_years}}

{{csv:schema/recipes/water_harvesting_conservation/T0_nbs_registry.csv|cols=nbs_id,establishment_period_years,time_to_benefit_years}}

{{csv:schema/recipes/wetland_management/T0_nbs_registry.csv|cols=nbs_id,establishment_period_years,time_to_benefit_years}}

The modulation is specified only qualitatively. No function at the pin turns an establishment period into a weight on baseline versus future hazard, and mangrove restoration has no establishment period recorded. An application must state how it uses the period, for instance by choosing which future horizon the screen reports for long-horizon practices.

### Step A6. Compose the asset-hazard rating

The module sheet's suggested composition is multiplicative per hazard, weighted across hazards, normalised to 0–1 and classified Low to Very High, mirroring the screening approach's overall risk rating. [src: methodology/modules/M2b_project_risk.md §6]

```formula
PR_s(p) = N( Σ_{h ∈ H_A} w_h · H_{h,s}(p) · A(p) )
class_s(p) ∈ {Low, Medium, High, Very High}   (cut-offs not specified)
Δ_s(p) = PR_s(p) − PR_baseline(p)
```

- `PR_s(p)`: project-risk score at pixel `p` under scenario `s`.
- `H_A`: the screened asset-threat hazards that have a T2 hazard layer.
- `w_h`: `asset_risk_weight`, or the equal-weight fallback.
- `H_{h,s}(p)`: normalised hazard layer, assembled with the same datasets and harmonisation as M2.
- `A(p)`: asset exposure, the investment-footprint proxy (default the M1 opportunity-space mask, optionally weighted by suitability) plus supporting infrastructure layers.
- `N(·)`: rescaling to 0–1.

[src: methodology/modules/M2b_project_risk.md §6] The sheet describes the composition only in words. The written form of `PR_s`, including how the footprint term `A(p)` enters the product, is not specified by the method; it is the standard form and needs confirmation before use.

The original draft multiplied by a separate per-hazard "asset fragility" term (`T3.asset_fragility`). [src: methodology/modules/M2b_project_risk.md §6] [src: methodology/modules/M2b_project_risk.md §9] The implemented schema carries that quantity as `asset_sensitivity`, and `asset_risk_weight` is already the normalisation of `asset_sensitivity`. [src: schema/spec.md §T3] Using both the weight and a fragility multiplier would apply sensitivity twice; the formula above uses the weight alone. Multiplicative against additive composition, the footprint proxy and the class cut-offs are all open questions. [src: methodology/modules/M2b_project_risk.md §11]

For future scenarios, rerun hazard assembly with future datasets, hold exposure and sensitivity constant, and recompose. [src: methodology/modules/M2b_project_risk.md §6]

## Method, Stream B: operational and enabling environment

### Why these variables live here

Stream B covers the investment-readiness factors a task team needs to see: things a project can change, such as roads, extension or credit. The method separates two kinds of operational constraint [src: schema/spec.md §T4] [src: AGENTS.md §What is locked]:

- **Hard exclusions** (legal protected areas, water bodies, urban footprints, formally designated reserves) cannot be legislated away on a scoping timescale. They stay in T4 as suitability masks with `is_scenario_candidate = false`.
- **Soft, investment-addressable factors** (road and market access, extension, tenure security, finance, labour) are not built into the opportunity surface. Applied as hard masks, they would over-constrain the opportunity space and hide places where investment could *create* feasibility.

The practical test is whether switching the variable off in a what-if scenario is a reasonable policy question. If it is, the variable is soft and belongs to Stream B. If it is not (a water body), it is hard and belongs in T4. [src: schema/spec.md §T4]

Evidence about soft enabling factors is extracted with `use_role = operational_risk`, never as `structural_suitability`; extracting it as structural suitability is a recorded defect (`wrong_table`). [src: AGENTS.md §What is locked] The historical T4 edition contains these variables as recipe rows, flagged `suitability_dimension = operational_constraint` when every contributing unit is `operational_risk`, and excludes them from the support and selection surface that drives the suitability MCDA. They are catalogued and traceable without setting the suitability base. [src: AGENTS.md §What is locked] At the pin, agroforestry is the only practice with such rows: the eight levers below plus `protected_area_status`, which is the one row with `is_scenario_candidate = false`. [src: schema/recipes/agroforestry/T4_suitability_mappings.csv]

The module sheet describes each lever as a T4 row with `is_scenario_candidate = true`. [src: methodology/modules/M2b_project_risk.md §12] The later locked routing keeps the row but removes it from structural suitability. Read the T4 row as a catalogue entry for the M2b screen, not as a suitability input.

### The eight levers

| Lever | Variable | Indicative data | WOCAT indirect driver |
|---|---|---|---|
| Accessibility | [[var:accessibility_travel_time]] | Nelson / Weiss travel-time surfaces | `m` (market access, roads) |
| Electrification | [[var:electrification_index]] | Bank energy data, VIIRS night-lights | `i` (infrastructure) |
| Tenure, including Indigenous Peoples and local communities (IPLC) | [[var:tenure_security]] | LandMark, WWF/ICCA, Prindex | `t` (land tenure) |
| Conflict and fragility | [[var:conflict_fragility_index]] | ACLED, the Bank fragility and conflict list | `p` (political stability, security) |
| Governance and extension | [[var:extension_governance]] | Worldwide Governance Indicators, country uploads | `e`, `g` |
| Finance and credit | [[var:finance_credit_access]] | Project-funding density, FinScope | `f` (financial access) |
| Market and value chain | [[var:market_value_chain]] | FAOSTAT, country uploads | `m` |
| Labour | [[var:labour_availability]] | ILO, LSMS-ISA, country uploads | `l` (labour availability) |

[src: methodology/modules/M2b_project_risk.md §12] [src: schema/registers/VONT_variable_ontology.csv]

The alignment with WOCAT questionnaire drivers gives each lever a traceable definition. Two levers carry published motivation in the sheet: secure tenure as a precondition for long-horizon tree investment, and credit to bridge the establishment phase (Global Center on Adaptation 2022). [src: methodology/modules/M2b_project_risk.md §12] Infrastructure is not a top-level opportunity-space theme: it is either a descriptor (market access) or a Stream B lever. [src: methodology/opportunity_space_T5.md §What did NOT make it (and why)]

### Variable policy: what Stream B must not hold

A lookup lists variables that may not be emitted as `operational_risk` evidence (`exclude`, which the ingest gate refuses) or that are feasibility-level detail (`flag`, an advisory scope signal). [src: schema/lookups/README.md] [src: methodology/RULESET_VERSIONS.md §v1.9.0]

{{csv:schema/lookups/m2b_variable_policy.csv|cols=variable,decision,reason}}

The reasoning: adoption is an outcome of the enabling environment, not a cause of operational risk, so adoption evidence may inform effect conditionality or implementation guidance but never M2b; practice-specific implementation detail (rootstock, planting material, restorable patch size) is feasibility content. The same ruleset also requires that a policy mention, a context figure or a chain of inference is not treated as cause and effect. [src: schema/lookups/m2b_variable_policy.csv] [src: methodology/RULESET_VERSIONS.md §v1.9.0]

### The safeguard flag

Tenure carries an explicit safeguard flag. A hotspot that overlaps IPLC customary land raises `FPIC_REQUIRED = true` in the Module 6 hand-off and adds a scorecard note; LandMark and WWF/ICCA layers are the spatial input and the Bank's Environmental and Social Standard 7 is the policy hook. [src: methodology/modules/M2b_project_risk.md §12] The flag says consent is required; it does not assess whether consent has been or could be obtained.

### How Stream B is applied

Each lever is a scenario lever ("what if road access improved?") and an input to a filter or flag. It is never summed into hotspots and never promoted to a hard exclusion on the scoping timescale. [src: methodology/modules/M2b_project_risk.md §12] No composition function, threshold or combined Stream B index is specified; the sheet lists institutional and social constraints among its open questions. [src: methodology/modules/M2b_project_risk.md §11] An application therefore reports each lever separately within the opportunity space, states the dataset and its context sensitivity, and lets the analyst set any flag threshold explicitly.

## Applying the screen to the opportunity space

M2b is evaluated inside the M1 opportunity space, because asset risk only matters where the team would actually invest. [src: methodology/modules/M2b_project_risk.md §1]

1. Standalone first. The method is built as a separate project-risk view first, to validate the method and outputs. [src: methodology/modules/M2b_project_risk.md §8]
2. Then a hotspot scope. Once agreed, the rating becomes a third scope on M4 Priority Hotspots, next to the suitability scope and the priority scope. The analyst chooses to **exclude** or **flag** High and Very High project-risk areas from the hotspot intersection. [src: methodology/modules/M2b_project_risk.md §8] The full M2b lens combines this project-risk scope with operational readiness. [src: methodology/modules/M2b_project_risk.md §12]
3. Filter, never sum. Because the rating acts as a mask or flag, sharing a hazard layer with M2 or with suitability is allowed: the same hazard enters two lenses in two roles and no single additive score is inflated. The one prohibited move is adding the project-risk score as another term in the M4 sum. [src: methodology/modules/M2b_project_risk.md §7]

```formula
Hotspot_exclude(p) = Hotspot(p)  if class_s(p) ∉ T_excl, else masked
Hotspot_flag(p)    = Hotspot(p), with flag(p) = [class_s(p) ∈ T_excl]
```

- `Hotspot(p)`: the M4 hotspot score at pixel `p`, computed without any M2b term.
- `class_s(p)`: the Stream A project-risk class under scenario `s`.
- `T_excl`: the classes the analyst chooses to screen, by default High and Very High.

[src: methodology/modules/M2b_project_risk.md §8] The sheet names the exclude and flag options but does not write them out; this form is not specified by the method; it is the standard form and needs confirmation before use.

The product handbook states the same rule for analysts: M2b produces a separate project-risk flag or filter, and its score stays out of the livelihood-need sum. [src: method:handbook/implement-a-scan.md §3. Build the scoping brief]

## Outputs

| Output | Form | Use |
|---|---|---|
| Project-risk raster, baseline | GeoTIFF, 0–1 | Project-risk view; later the M4 scope |
| Project-risk raster per future scenario | GeoTIFF, 0–1 | Durability under climate change |
| Per-hazard asset-threat surfaces | GeoTIFF per hazard × scenario | Drill-down |
| Overall rating and ranked units | CSV per admin unit: mean rating, share High or Very High, dominant asset-threat hazard, change against baseline | Rating card and ranked list |
| Run metadata | JSON: hazards, sensitivities, weights, fallbacks | Audit trail |

[src: methodology/modules/M2b_project_risk.md §5] [src: methodology/modules/M2b_project_risk.md §6]

The rating is relative within the opportunity space. It is a screening flag; a Low class means "no screened asset hazard stands out here", not "safe".

## Worked illustration

The pinned forest restoration T3 table is the only practice at the pin whose asset rows meet the completeness rule, so it is the one case where `asset_risk_weight` is populated. No M2b surface has been computed from it.

{{csv:schema/recipes/forest_restoration/T3_nbs_hazard_farming.csv|where=risk_role=asset_threat|cols=record_id,hazard_type,asset_sensitivity,asset_risk_weight,evidence_level,agreement_level,confidence,timescale_of_effect}}

Reading the global rows (record identifiers without a family or scope segment): the six core hazards are all assessed, with sensitivities drought `moderate` (rank 2), flood `very_high` (3), heat stress, fire and wind/cyclone `low` (1 each) and waterlogging `none` (0). The ranks sum to 8, so the weights are 2/8 = 0.25, 3/8 = 0.375, 1/8 = 0.125 for each low hazard, and 0 for waterlogging, matching the table. The extreme-rainfall (`low`) and landslide (`moderate`) rows have no weight, because asset-only hazards are outside the rule. Most family rows are data-deficient (blank sensitivity, `very_low` confidence) and carry no weight; only the NbS roll-up sets the weights. [src: schema/recipes/forest_restoration/T3_nbs_hazard_farming.csv] [src: src/nbs_ruralscan/recipe/cell_synthesis.py §asset_risk_weights]

For the other five practices at least one core hazard lacks an assessed global asset row (agroforestry has no assessed heat-stress or waterlogging row; riparian buffers have only flood), so M2b would use equal weights for them. [src: schema/recipes/agroforestry/T3_nbs_hazard_farming.csv] [src: schema/recipes/riparian_buffer/T3_nbs_hazard_farming.csv]

## Assumptions and limits

- **Thin evidence.** Asset vulnerability rests largely on WOCAT practitioner ratings with limited literature, so many cells are `limited` evidence with low or very low confidence, and the equal-weight fallback is common. [src: methodology/T3_T6_generation_method.md §9]
- **Declare the formulation.** Any combined assessment must state its composition, footprint measure, class boundaries and treatment of the establishment period. Operational flags remain separate unless a documented method supports their combination.
- **Asset-only hazards cannot be mapped yet**, because T2 has no hazard layer type for them.
- **Equal weighting is a default, not a finding.** It means "insufficient evidence to differentiate", not "all hazards matter equally".
- **Soft factors are flagged, not judged.** Stream B layers are often national or modelled and context-sensitive; the scoping output should recommend country-endorsed sources rather than validate them.
- **Safeguards are triggered, not discharged.** The FPIC flag records a requirement; it does not replace consultation.
- **Feasibility must still do:** the full project-level climate and disaster risk screening at appraisal, site-level hazard and engineering assessment, tenure and consent processes, and local verification of access, markets, finance and labour.

## Where this is configured

- [[table:T3]]: `risk_role`, `asset_sensitivity`, `asset_risk_weight`, `timescale_of_effect` (vulnerability window), `confidence`, `applicability`.
- [[table:T2]]: hazard layers shared with M2 (`hazard_type`, `scenario_type`, normalisation).
- [[table:T0]]: `establishment_period_years`.
- [[table:T4]]: hard exclusions as masks (`is_scenario_candidate = false`); soft levers catalogued as `operational_constraint` rows outside the suitability surface.
- [[table:EV]]: `use_role = asset_vulnerability` and `use_role = operational_risk` units, with `hazard_severity`.
- [[table:VONT]] and [[table:BIND]]: the Stream B variables and their datasets.
- [[table:T1]]: datasets.
- Lookups: `schema/lookups/m2b_variable_policy.csv` (exclusions and flags for Stream B evidence) and `schema/lookups/wocat_hazard_map.csv` (WOCAT hazard keys to T3 hazard types).
