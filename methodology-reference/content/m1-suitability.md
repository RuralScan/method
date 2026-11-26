---
title: "M1: Suitability to opportunity space"
slug: m1-suitability
summary: Interpret family-level suitability, host requirements, exclusions, unknown areas and the candidate footprint.
sources:
  - methodology/modules/M1_suitability.md
  - schema/spec.md
  - methodology/T4_generation_method.md
  - methodology/T4_developer_contract.md
  - AGENTS.md
  - method:handbook/read-a-suitability-recipe.md
  - methodology/framework.md
  - method:handbook/implement-a-scan.md
  - methodology/recipes/water_harvesting.md
---

## Question this module answers

Module 1 (M1) asks where a nature-based solution could be considered, given terrain, climate, soils, the existing land-use system and applicable exclusions. It produces a suitability assessment and identifies the **opportunity space** for further investigation. Development priorities are assessed separately in [[ch:m4-hotspots]]; benefits and costs are compared in [[ch:m5-scorecard]]. [src: methodology/modules/M1_suitability.md §2. Question answered]

M1 applies an accepted mapping to spatial data. New mappings are proposed through [[ch:suitability-synthesis|agent-led T4 synthesis]] and recorded scientific review. The agent's evidence judgement and the subsequent spatial calculation are separate steps: a runtime evaluates the accepted response and run settings; it does not derive a threshold directly from a paper.

## Inputs

Table: Inputs needed to interpret a family-level suitability assessment.

| Input | Purpose |
|---|---|
| Practice and suitability family | Identify the intervention and its dominant limiting factors. |
| Area, grid and scenario | Define the spatial and temporal context. |
| Accepted T4 mappings | State variables, response functions, evidence and applicability conditions. |
| Dataset bindings | Supply context-appropriate inputs with compatible units and measurement basis. |
| Host requirements and exclusions | Identify where the intervention is eligible and where it is excluded. |
| Recorded run policy | State selected criteria, weights, combination method, missing-data handling and sensitivity settings. |

[src: methodology/modules/M1_suitability.md §3. Inputs] [src: schema/spec.md §T4_RUN]

## Method

### 1. Define the family and reporting unit

Suitability is assessed per **family** of sub-practices sharing a dominant limiting factor. Planting trees and retaining natural regeneration can produce similar-looking landscapes, but the latter depends on regeneration potential as well as the environmental conditions needed by trees. Combining them into one suitability rule would hide that distinction. Each grouping records its rationale and evidence; the practice chapters list the families. [src: methodology/T4_generation_method.md §2.1 Practice definition → subpractices → suitability families]

Every family also specifies the kind of spatial product it supports.

Table: Spatial products and valid footprint measures.

| Product | Interpretation | Footprint measure |
|---|---|---|
| `area_suitability` | Land that could host the practice. | Candidate area. |
| `applicability_zone` | A zone within which a linear intervention could be placed. | Candidate length or density, not the zone's full area. |
| `zonal_linear` | Candidate locations along a feature, such as a stream. | Length or a specifically delineated intervention footprint, not full raster-cell area. |
| `qualitative_only` | A practice for which this mapping scale would mislead. | Qualitative guidance rather than mapped area. |

[src: methodology/T4_generation_method.md §2.4 Spatial product type & the resolution trap] [src: schema/spec.md §FAM]

For example, flagging a 5 km grid cell for windbreaks identifies a candidate zone. It does not identify 25 km² of plantable windbreak area. Coarser grids make this distinction more important. [src: methodology/T4_generation_method.md §2.4 Spatial product type & the resolution trap]

### 2. Separate conditions, gates and operational barriers

Biophysical conditions describe the natural envelope; system conditions describe the existing crop, land use or farming system that the intervention must fit. Where a practice improves an existing host system, use its observed distribution where suitable data exist. A potential crop niche does not establish that the crop is present. Preserve any host-area fraction separately from the suitability score. [src: methodology/T4_generation_method.md §2.5 Constrain by observed distribution, not a modelled niche, where data exist] [src: methodology/T4_developer_contract.md §Planted host and exclusion contracts]

Host requirements and applicable hard exclusions are **gates**, not weighted criteria. A favourable soil score cannot compensate for an ineligible host system or a legal exclusion. A low suitability class in a source is not itself a legal exclusion. [src: methodology/T4_developer_contract.md §Planted host and exclusion contracts]

Soft, investment-addressable factors such as road access, tenure, finance, extension and labour belong in [[ch:m2b-project-risk]] and the hand-off. They do not enter structural suitability. Applicable legal and physical exclusions remain separate masks. [src: AGENTS.md §What is locked]

### 3. Prepare compatible spatial inputs

Resolve datasets for the target context and check units, depth, time period and spatial support against the selected response. Record any substitutions. [[ch:farming-systems-and-data]] describes dataset selection and binding. [src: methodology/T4_developer_contract.md §Dataset preparation proposals and source compatibility]

Respect the coarsest meaningful resolution of each variable. Compute scale-dependent derivatives such as slope at a suitable fine resolution before summarising them to a coarser grid. Computing slope from an already smoothed elevation surface can understate steepness and overstate suitable land. Retain relevant within-cell variation when reporting a candidate footprint. [src: methodology/T4_generation_method.md §2.4 Per-variable resolution validity]

### 4. Apply the accepted responses and combination policy

A response translates an input, in its specified units, into the suitability interpretation recorded in T4. Use only an explicitly selected, complete response whose numerical calibration and applicability have been accepted. Do not infer thresholds from demonstration curves, source-use ranges or the name of a response type. Response definitions and the evidence-to-mapping decision have their detailed home in [[ch:suitability-synthesis]]. [src: methodology/T4_developer_contract.md §Selections, corrections and rebuilds] [src: method:handbook/read-a-suitability-recipe.md §Check the decision before scoring]

The run records its criterion set and how related variables are represented, so multiple indicators of the same underlying condition do not silently multiply its influence. Source-quality weights, numbers of papers and importance scores from published models are not automatically run weights. [src: methodology/framework.md §Variable selection (two stages)] [src: methodology/T4_developer_contract.md §Counts, importance and runtime weights]

Where the accepted run policy specifies a weighted linear combination, the calculation is:

```formula
S(x) = Σ_j w_j f_j(x),       w_j ≥ 0,       Σ_j w_j = 1
```

Here `S(x)` is the suitability index at location `x`, `f_j(x)` is the selected response for criterion `j`, and `w_j` is its recorded run weight. This is the combination used by the recorded first-pass policy. Fix criteria and weights before evaluation and do not renormalise them separately at each pixel when inputs are missing. [src: methodology/T4_developer_contract.md §Aggregation baseline and design history] [src: methodology/T4_developer_contract.md §Approved first-pass policy]

Weighted combination allows a high score on one criterion to offset a low score on another. Gates remain outside that combination. Test plausible alternatives, including limiting-factor behaviour where required by the run policy, and report whether they change the candidate areas. [src: methodology/T4_developer_contract.md §Approved first-pass policy]

### 5. Preserve pixel states and explain the opportunity-space boundary

Table: Interpretation of spatial states before reporting an opportunity space.

| State | Interpretation |
|---|---|
| Excluded | A known exclusion or failed host requirement applies. |
| Unknown | No known exclusion applies, but a required input or gate is unresolved. |
| Scored | Required inputs and gates support evaluation under the selected policy. |

[src: methodology/T4_developer_contract.md §Aggregation baseline and design history]

Known exclusion takes precedence over unknown inputs. Otherwise missing required information remains unknown, not zero and not suitable by default. Report input and score coverage beside the map. [src: methodology/T4_developer_contract.md §Planted host and exclusion contracts]

State the rule used to select candidate areas and any display-class boundaries. Relative classes describe a location's position within a reference area; they are not universal thresholds of success. Changing the area or class breaks can change a relative shortlist. Keep excluded and unknown cells visible as separate states. [src: methodology/modules/M1_suitability.md §6.8 Classification & fingerprint extraction] [src: method:handbook/implement-a-scan.md §2. Run and interpret the first pass]

## Worked illustration: evidence without a score

A site receives 350 mm of annual rainfall. A reviewed bench-terrace mapping records a reported use range of 200–600 mm for one design, but its numerical calibration remains held. The site lies within that reported range; this alone does not supply a rainfall suitability score or show that terraces will work there. The analyst retains the observation and the hold, rather than converting the range into a curve. [src: method:handbook/read-a-suitability-recipe.md §Find the family and input] [src: method:handbook/read-a-suitability-recipe.md §Check the decision before scoring]

This distinguishes three claims: the source used a variable, it supports a direction or association, and it supports a transferable numerical response. Acceptance of one does not establish the others. [src: methodology/T4_generation_method.md §Directional evidence is distinct from numeric calibration]

## Outputs

Retain the suitability result, candidate-area definition, exclusions, unknown areas and data coverage together. Summarise footprint in the family's valid unit, with the selected variables, responses, weights, input versions and sensitivity results. A partial terrain-and-soil index must be labelled by that scope rather than as complete suitability. These outputs supply M3 characterisation and M4 prioritisation. [src: methodology/modules/M1_suitability.md §4. Outputs] [src: method:handbook/implement-a-scan.md §2. Run and interpret the first pass]

## Assumptions and limits

Suitability scores express the recorded evidence and scoring convention, not a probability of establishment or investment success. Transfer from another region requires a reasoned applicability decision. Local land use, hydrology, soils and legal restrictions can differ from global layers, and coarse grids can conceal constraints. Literature also tends to report successful applications more often than failures. [src: methodology/T4_developer_contract.md §Target country and evidence country are different filters] [src: methodology/recipes/water_harvesting.md §7.6 Constraints and limitations] [src: methodology/T4_generation_method.md §6.1 Publication bias & uncertainty (pragmatic)]

Sensitivity to weights does not capture all uncertainty in data, responses or transfer. Held calibration remains unscored. Field assessment and feasibility work must establish the local conditions on which the intervention depends. [src: methodology/T4_generation_method.md §Directional evidence is distinct from numeric calibration] [src: methodology/T4_developer_contract.md §Module boundaries and output meaning]

## Pending overrides and opportunity area

Proposed climate and precomputed mangrove rules remain pending and inactive. Their scores, independent exclusion screens, conditional pathways and unknown states must stay separate. Membership does not multiply hectares; mangrove support polygons are not restoration footprints. Inspect scope and approval status in [[ch:t4-overrides]] before interpreting a candidate. [src: evidence:suitability/overrides/README.md]

## Where this is configured

[[table:FAM]] defines families and product types. [[table:T4]] records mappings and evidence; [[table:T4_RUN]] records execution policy. [[table:VONT]], [[table:T1]], [[table:BIND]] and [[table:T7]] define variables, datasets and contexts. See [[ch:suitability-synthesis]] for T4 synthesis and [[ch:implementing-the-method]] for application reporting.
