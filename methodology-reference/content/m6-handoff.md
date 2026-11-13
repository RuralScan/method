---
title: Module 6 - Implementation hand-off
slug: m6-handoff
summary: Know exactly what a scoping run passes to feasibility (shortlist, flags, sensitive-variable prompts, safeguard triggers, guidance for unmapped practices and recorded design lessons) and where the scan's authority ends.
sources:
  - methodology/modules/M6_handoff.md
  - methodology/feasibility_notes.md
  - methodology/framework.md
  - methodology/T4_generation_method.md
  - methodology/modules/M2b_project_risk.md
  - methodology/modules/M3_characterisation.md
  - methodology/modules/M4_hotspots.md
  - methodology/modules/M5_scorecard.md
  - methodology/T3_T6_generation_method.md
  - schema/registers/FAM_family_registry.csv
  - schema/registers/VONT_variable_ontology.csv
  - schema/spec.md
  - AGENTS.md
  - method:handbook/implement-a-scan.md
---

## Question this module answers

Module 6 (M6) answers: scoping is done, so what comes next for this nature-based solution here? Which validation, consultations and feasibility analyses should follow, using which methods and tools? [src: methodology/modules/M6_handoff.md §2]

M6 is the scan's **scope boundary**. It is content, not computation: short, targeted guidance notes that point a project team to the tools, consultations and analyses it would commission next. It is not a feasibility assessment, an ecosystem-service model or a cost-benefit analysis. It does not imply that every scoped practice proceeds to feasibility. [src: methodology/modules/M6_handoff.md §1] [src: methodology/modules/M6_handoff.md §2]

The governing principle, stated across the method: **scoping flags; feasibility validates.** [src: AGENTS.md §What is locked] [src: methodology/T4_generation_method.md §2.6]

## Inputs

| Input | From | Used for |
|---|---|---|
| Selected practice or stacked cluster | M0, [[table:T0]] | One hand-off card per practice, or a combined card where several overlap. |
| Ranked priority units | M4 | "Validate these units in the field." |
| Scorecard and cost profile | M5, [[table:T6]], [[table:T6E]] | Indicative economic snapshot and the benefits being bought. |
| Sensitive variables consumed | [[table:VONT]] `context_sensitivity` | Country-endorsed source prompts. |
| IPLC overlap flag | M3 | FPIC and ESS7 safeguard trigger. |
| Binding operational levers | M2b Stream B | Pre-feasibility checks. |
| Dominant farming system | [[table:T7]] in ranked units | Keys the design step for tree-based practices. |
| Descriptors | [[table:T5]] `context` theme | Population in priority units, accessibility, agrarian structure. |
| Parked and qualitative families | [[table:FAM]] | Guidance where no map is produced. |
| Recorded feasibility lessons | feasibility notes | Design and budgeting implications found in the evidence. |

[src: methodology/modules/M6_handoff.md §3] [src: methodology/modules/M6_handoff.md §10]

## Method

The hand-off is built in seven parts. [src: methodology/modules/M6_handoff.md §6]

### 1. State the stage pathway

Show the four stages and what each adds: Scoping (this scan), Pre-feasibility, Feasibility and design, Implementation. The point is to place every output of the scan at the first stage. [src: methodology/modules/M6_handoff.md §6]

### 2. Give the indicative economic snapshot

Render the cost and return denominators that the M5 profile actually carries, labelled as planning level. A full cost-benefit analysis is done at feasibility. [src: methodology/modules/M6_handoff.md §6] The snapshot renders only the denominators the tables hold. It never computes new ones. Cost per tonne of CO2e avoided is a feasibility figure and is not generated at all. [src: methodology/modules/M5_scorecard.md §10] [src: schema/spec.md §T6 - NbS Scorecard - Effects and Economic Profile] Numeric ranges exist only where the economic gates passed (see [[ch:cost-profiles]]); elsewhere the snapshot says the evidence is insufficient.

### 3. List recommended next steps, each tied to a scan output

The default next steps are:

- validate the priority units in the field (from the M4 ranking);
- map stakeholders and tenure;
- carry out a full cost-benefit and financing scan;
- screen safeguards and environmental, social and governance risks.

Each step names the scan layer it builds on, for example "validate these units, which are very-high suitability and hotspot". [src: methodology/modules/M6_handoff.md §6] [src: methodology/modules/M6_handoff.md §8] The scoping brief keeps, for each promising area, explicit questions on land use, tenure, safeguards and design for field or feasibility work. [src: method:handbook/implement-a-scan.md §3. Build the scoping brief]

### 4. Signpost feasibility methods and tools

Point to the valuation toolbox from the project's stocktake review, grouped as nature-based methods and integrated methods:

- **Nature-based:** IPCC Tier 1 to 3 carbon accounting, RUSLE erosion modelling, and ecosystem-service models such as InVEST, ARIES and Co$tingNature.
- **Integrated:** cost-benefit analysis and multi-criteria decision analysis.

Tool names are references, not endorsements. [src: methodology/modules/M6_handoff.md §6] The block carries the **proportionality principle**: simple methods (benefit transfer, proxy indicators) are enough early on, and detailed spatial modelling is reserved for high-priority sites. [src: methodology/modules/M6_handoff.md §6]

### 5. Add the design step for tree-based practices

For tree-based practices, add "right tree, right place": species or mixture selection, establishment feasibility and resilience to future climate. This step is keyed to the dominant farming-system class in the ranked units. [src: methodology/modules/M6_handoff.md §6] [src: methodology/modules/M6_handoff.md §10] It is the first place species-level reasoning enters. The scan reasons per suitability family and keeps species and crop envelopes out of practice-level suitability, retaining them for this later layer. [src: AGENTS.md §What is locked]

### 6. Tailor to the context

Add country- and practice-specific guidance, cross-linked to the scenario what-ifs, for example an investment in road access relaxing an operational constraint. [src: methodology/modules/M6_handoff.md §6] The soft, investment-addressable enabling-environment factors are road and market access, value-chain depth, tenure security, extension and governance, finance and credit, and labour. They are routed to the M2b operational-risk filter and to this hand-off as next-step guidance, not to structural suitability. Only hard exclusions (legal protected areas, water bodies, urban footprints) act as suitability masks. [src: AGENTS.md §What is locked] Any Stream B lever that is binding, because its data require upload or it scores low in M2b, appears under consultations and pre-feasibility checks. [src: methodology/modules/M6_handoff.md §10] [src: methodology/modules/M2b_project_risk.md §12]

### 7. State the scope boundary

End with an explicit statement: the tool stops at scoping, next steps are indicative, and not every scoped practice proceeds. [src: methodology/modules/M6_handoff.md §6]

## The sensitive-variable recommendation

Some variables are nationally derived and sovereignty-sensitive. A global model of population, poverty or crop production can diverge from, or appear to contradict, a country's official figures. [[table:VONT]] marks these `context_sensitivity = high`. [src: methodology/T4_generation_method.md §2.6]

The hand-off card lists **every high-sensitivity variable the run consumed**, each with a prompt to confirm the source with the country. [src: methodology/modules/M6_handoff.md §6] [src: methodology/modules/M6_handoff.md §10] The variables flagged at the pin are:

{{csv:schema/registers/VONT_variable_ontology.csv|where=context_sensitivity=high|cols=canonical_variable_id,label,context_sensitivity}}

The recommendation has a fixed scope:

- The scan **flags** the variable and **recommends** that its source be confirmed or replaced with a country-endorsed source during feasibility.
- The scan **does not** negotiate, validate or endorse national data. That is downstream work, outside rapid scoping.
- The flag is a labelling layer only. It does not change the suitability or hotspot analysis. [src: methodology/T4_generation_method.md §2.6] [src: schema/spec.md §VONT - Variable Ontology]

The prose examples and the register do not fully agree. Population and production statistics are the guidance's examples of high sensitivity, but the T5 descriptors `rural_population` and `agricultural_production_value` are recorded as `medium` at the pin. [src: methodology/T4_generation_method.md §2.6] [src: schema/registers/VONT_variable_ontology.csv] Until the register is reconciled, a hand-off should list those two as well whenever they appear in a run.

## The safeguard trigger

Where Indigenous Peoples' and local community (IPLC) land, from LandMark and the WWF/ICCA registry, overlaps the opportunity-space mask, the hand-off **must** set `FPIC_REQUIRED` and raise World Bank Environmental and Social Standard 7 (ESS7) in the consultations block. [src: methodology/modules/M6_handoff.md §10] [src: methodology/modules/M2b_project_risk.md §12] The same caveat appears in the M5 comparison view, so it is not hidden in the hand-off alone. [src: methodology/modules/M5_scorecard.md §10]

IPLC coverage is patchy, so the flag is phrased accordingly. Absence of mapped IPLC land is not evidence that no IPLC are present, and a negative flag never clears the safeguard question. [src: methodology/modules/M6_handoff.md §10] As with sensitive variables, the scan flags and the project team carries out the FPIC and ESS7 procedures. [src: methodology/modules/M2b_project_risk.md §12]

## Guidance for families the scan does not map

Every suitability family carries a spatial product type. Some families are `qualitative_only`: their practice is sub-pixel or settlement-driven, so a raster suitability surface would mislead. These families are flagged, not mapped. Their hand-off is a scorecard entry and an M6 note. [src: methodology/T4_generation_method.md §2.4]

{{csv:schema/registers/FAM_family_registry.csv|where=spatial_product_type=qualitative_only|cols=suitability_family_id,nbs_id,name,dominant_limiting_factor}}

The registry holds two kinds of row with this type:

- **Real practices kept out of mapping.** Multistrata homegardens are proximity-driven at sub-pixel scale. Household rooftop harvesting is settlement-driven and not a rural-landscape suitability surface. Constructed treatment wetlands are an engineering siting problem for point-source and drainage loads. [src: schema/registers/FAM_family_registry.csv] A `qualitative_only` family is parked out of the generated T3 and T6 tables. Its evidence stays in the register for Module 6. [src: AGENTS.md §What is locked]
- **Cross-family tagging rows.** The `__cross_family` rows hold evidence that applies across all families of a practice. They are not practices. Their evidence pools into the practice roll-up, and the forest-restoration one is explicitly exempt from parking. [src: schema/registers/FAM_family_registry.csv]

For parked families the hand-off should say three things. First, the practice was considered and why it is not mapped. Second, what the retained evidence says, read from the register rather than restated. Third, what siting or design work would be needed to assess it.

Families that are mapped but are not area products need the same care. For `applicability_zone` and `zonal_linear` families (windbreaks, contour buffers, riparian buffers), the hand-off reports candidate length, density or zone, never pixel area, because the overstatement grows with pixel size. [src: methodology/T4_generation_method.md §2.4] See [[ch:m1-suitability]].

## Feasibility notes

The evidence pipeline keeps finding lessons that are not scoping content but matter for investment design: attribution traps, maintenance burdens and opportunity costs. They are collated in a running record for the teams writing feasibility and implementation guidance. Each entry records the practice, the lesson, the design implication and an evidence pointer. [src: methodology/feasibility_notes.md §Notes for the feasibility / implementation guidelines (Module 6)] The entries at the pin:

| Practice | Finding | Design implication |
|---|---|---|
| Mangrove restoration | In the one ex-post evaluation held, household poverty and income gains in the project area were attributed to resettlement and technology transfer bundled with the planting, not to the mangroves. No evidence unit credits them to the practice. | A restoration investment that promises welfare outcomes must budget the complementary livelihood package explicitly. |
| Created wetlands | Sediment and particulate phosphorus retention in created riverine basins declined after about ten years, while nitrate removal persisted. A wetland traps sediment already eroded; it does not prevent erosion upstream. | Put sediment management in the recurrent-cost case, and pair the wetland with upstream erosion control when soil loss is the problem. |
| Wetland restoration and rewetting | Households already earn income from the wetlands that restoration would alter (cultivation, product sales, fishing). | Count forgone wetland-use income as a project cost and plan replacement livelihoods. |
| Coastal wetlands | Most salt-marsh deterioration comes from moderate storms of roughly monthly frequency; intense hurricanes contribute under 1% of long-term marsh erosion. | Budget continuous edge maintenance under the everyday wave climate, not a post-cyclone repair reserve. |

[src: methodology/feasibility_notes.md §Notes for the feasibility / implementation guidelines (Module 6)]

These notes connect to synthesis rules. A bundled intervention is never credited in full to one practice. Existing-use income is treated as the counterfactual, not a benefit of restoring. Both rules are described in [[ch:effect-synthesis]]. [src: AGENTS.md §What is locked] The notes are a living record of findings, not a complete feasibility checklist.

## Outputs

| Output | Content |
|---|---|
| Stage pathway | Scoping, pre-feasibility, feasibility and design, implementation, with the scan placed at the first stage. |
| Economic snapshot | Planning-level cost and return denominators from the profile; insufficient-evidence states where gates fail. |
| Next steps | Field validation of named units, stakeholder and tenure mapping, cost-benefit and financing scan, safeguards screen; each linked to its scan layer. |
| Methods block | Feasibility tools with the proportionality principle. |
| Per-practice card | Methods, consultations, analyses to commission, design step, sensitive-variable prompts, FPIC and ESS7 flag, binding operational levers, context from descriptors. |
| Unmapped-practice notes | Parked `qualitative_only` families and how to assess them. |
| Scope statement | The explicit boundary line. |

[src: methodology/modules/M6_handoff.md §4] [src: methodology/modules/M6_handoff.md §10]

## The limits of the scan

The framework names what scoping does not do. These are the points where feasibility takes over. [src: methodology/framework.md §What this framework does not do]

- **No ecosystem-service modelling.** InVEST, ARIES and similar models are downstream.
- **No site-level design.** Opportunity space and hotspots come from gridded data at scoping resolution; they identify candidate areas, not plots.
- **No cost-benefit analysis.** Costs are indicative and ordinal, with no inflation adjustment and no discounting. [src: methodology/T3_T6_generation_method.md §7.7]
- **No optimisation.** The scan does not allocate budget or select a portfolio.
- **No detailed climate impact modelling** beyond hazard exposure.
- **No validation of national data.** Sensitive variables are flagged, not checked. [src: methodology/T4_generation_method.md §2.6]
- **No calibrated local suitability numbers where calibration is held.** A held or unrecorded numerical calibration is never presented as a score, range or reviewed value; such rules stay directional until resolved. [src: AGENTS.md §What is locked]
- **No transfer by assumption.** Effect classes from outside the target income band or agro-ecological context are labelled with their transfer class, or replaced by a gap for the AOI. [src: methodology/T3_T6_generation_method.md §5.5]
- **No summing of the two risks.** Livelihood risk (M2) is a need layer; investment risk (M2b) is a filter. A combined risk number in a feasibility document would not come from this scan. [src: AGENTS.md §What is locked]

## Assumptions and limits

- **Draft status.** The M6 specification is a draft. Its guidance notes, method library and design-step content are to be authored and reviewed by domain specialists, and placeholders are expected to be marked honestly where content is missing. [src: methodology/modules/M6_handoff.md §7] [src: methodology/modules/M6_handoff.md §9]
- **Not implemented at the pin.** The hand-off assembly is described as function signatures; no hand-off card has been produced. [src: methodology/modules/M6_handoff.md §10]
- **Open questions recorded in the source:** whether the method library should be a structured table or guidance notes; how prescriptive to be on tool choice (list options or recommend per context); and how to combine guidance when several practices overlap in a stacked cluster. [src: methodology/modules/M6_handoff.md §11]
- **Indicative throughout.** Every number passed on comes from scoping-grade inputs and evidence synthesis. Feasibility must re-derive what the investment case depends on.
- **Flags can be false negatives.** A missing IPLC polygon, a missing upload or a missing evidence row is absence of data, not absence of the issue.
- **What feasibility must still do:** confirm boundaries, land availability and tenure on the ground; replace sensitive global datasets with country-endorsed ones; carry out FPIC and ESS7 procedures where triggered; quantify the effects and costs that matter with site data; design species and layouts; and decide, on those results, whether the practice proceeds.

## Where this is configured

- [[table:VONT]]: `context_sensitivity`, which drives the country-endorsed source prompts.
- [[table:FAM]]: `spatial_product_type`, which identifies the families that are parked or reported as length or zone.
- [[table:T5]] and [[table:BIND]]: the IPLC layer and its binding; descriptors used as context.
- [[table:T6]] and [[table:T6E]]: the effect and cost rows behind the snapshot.
- [[table:T0]]: practice identity and establishment period.
- [[table:T7]]: farming-system classes that key the design step.
- The feasibility notes record and the M6 guidance notes: narrative content, outside the schema.
