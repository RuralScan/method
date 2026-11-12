---
title: The method as a scoping walkthrough
slug: scoping-walkthrough
summary: After this chapter you can follow the method stage by stage as a task team would use it, see what a full realisation of the method looks like, and find the method chapter behind each stage.
sources:
  - docs/redesign/index.html
  - docs/redesign/01-setup.html
  - docs/redesign/02-practices.html
  - docs/redesign/03-opportunity.html
  - docs/redesign/04-risk.html
  - docs/redesign/05-hotspots.html
  - docs/redesign/06-comparison.html
  - docs/redesign/07-next.html
  - docs/redesign/00-config.html
  - docs/redesign/help.html
  - docs/redesign/v1b-fixture.js
  - docs/redesign/v1b-classification.js
  - docs/redesign/v1b-road-example.js
  - docs/redesign/v1b-map.js
  - methodology/modules/M0_setup.md
  - methodology/modules/M1_suitability.md
  - methodology/modules/M2_climate_risk.md
  - methodology/modules/M2b_project_risk.md
  - methodology/framework.md
  - methodology/opportunity_space_T5.md
  - methodology/T3_T6_generation_method.md
  - methodology/T3_T6_developer_handover.md
  - methodology/T4_developer_contract.md
  - schema/spec.md
  - methodology/modules/M4_hotspots.md
  - methodology/modules/M6_handoff.md
  - schema/T5_opportunity_space.csv
  - schema/registers/FAM_family_registry.csv
  - schema/lookups/scorecard_rows.csv
  - schema/lookups/scorecard_chip_scale.csv
  - schema/lookups/scorecard_confidence_badge.csv
---
## What the visual methodology is

The reference describes the method module by module ([[ch:scope-and-framework]]). The visual methodology describes the same method as seven stages that a task team would walk through, from setting the scope to writing a scoping brief. It is an interactive mock-up (a wireframe), version 2.1, built as linked pages.

Its home page states its status: it is "an idealised implementation of the method", presented as an interactive mock-up. The pages "illustrate how the methodology could work in practice; they are not a commitment to deliver a software platform", and "all displayed data are examples; no figure is a pilot result". [src: docs/redesign/index.html §Home] The help page adds that the walkthrough "does not run a live spatial analysis or provide investment recommendations". [src: docs/redesign/help.html §Are the maps and results real?]

- **Every number and map is example data.** The maps are a synthetic surface (seeded value noise) on real Sierra Leone boundaries. The fixture contains "no thresholds, weights or evidence" and is "not derived from any schema table (T0–T7) or register". [src: docs/redesign/v1b-fixture.js §header] Effect chips, cost ranges, hazard classes and district ranks are authored illustrations, never evidence.
- **It is a statement of intent, not an implementation.** No scoring runs: weight, rule and class edits change local previews only. [src: docs/redesign/05-hotspots.html §5.3] [src: docs/redesign/00-config.html §C.2]
- **Where it differs from the module specifications** (see below), the tables and specifications at the pinned revision remain the source of record for anything a pipeline executes.

The pages are live at [the visual methodology home page](https://ciat.github.io/nbs_ruralscan/redesign/index.html). The live pages may be later than this edition; every citation in this chapter points to the pinned files.

Four things stay separate on every page: suitability, livelihood need, what the evidence says the practice does, and project risk, which "is a flag, never added to the others". [src: docs/redesign/index.html §H.4]

A control bar on every stage carries its state across pages: practice, opportunity extent (classes Very high, High, Moderate, Low; default Very high + High), view (5 km cells, Admin 2, Admin 3), climate (Baseline 1995–2014 or SSP2-4.5 about 2050) and, on Stage 5, a hotspot score (High+ or Very high). [src: docs/redesign/v1b-map.js §controlBar] [src: docs/redesign/index.html §H.5]

## Seven stages and the modules behind them

| Stage | Question it answers | Method chapters | Fit |
|---|---|---|---|
| 1 Setup | What problem, which practices, where? | [[ch:m0-setup]], [[ch:farming-systems-and-data]] | One-to-one with M0, with dataset binding behind it |
| 2 Explore the practices | Which practices could answer this? | Practice chapters ([[ch:practice-agroforestry]], [[ch:practice-riparian_buffer]], [[ch:practice-forest_restoration]] and others), [[ch:m5-scorecard]], [[ch:cost-profiles]] | No module of its own |
| 3 Opportunity space | Where could the practice establish? | [[ch:m1-suitability]], [[ch:m3-characterisation]], [[ch:m2-climate-risk]], [[ch:m5-scorecard]] | Spans several modules |
| 4 Project risk | Would hazards put the planting at risk? | [[ch:m2b-project-risk]] | One-to-one with M2b |
| 5 Priority hotspots | Where does it meet the project's priorities? | [[ch:m4-hotspots]], [[ch:m3-characterisation]] | One-to-one with M4, with M3 standardisation behind it |
| 6 NbS comparison | Which deserve a closer look? | [[ch:m5-scorecard]], [[ch:cost-profiles]] | One-to-one with M5 |
| 7 Next steps | What must feasibility confirm? | [[ch:m6-handoff]] | One-to-one with M6 |

[src: docs/redesign/index.html §H.3] [src: docs/redesign/index.html §H.6]

Stage 2 has no module of its own. It draws on the practice chapters, the family registry ([[table:FAM]]), the generated effect rows ([[table:T6]], [[table:T3]]), the cost profile ([[table:T6E]]) and the source register ([[table:SRC]]). Stage 3 is not M1 alone: it presents suitability (M1), the opportunity-space characterisation (M3), the livelihood climate-risk layer (M2) and the response rows that M5 presents, all within the opportunity space. The technical configuration page sits outside the stage sequence; it holds what M0, M1 and M3 configure.

## Setup

**The question.** What should the investment improve, with which practice, and where? [src: docs/redesign/01-setup.html §1.1.1]

**What the user chooses.** Three choices, pre-filled with an example. Objectives (climate resilience, livelihoods, biodiversity, water security, gender equity), which "change the wording of later stages" and "do not re-weight any map". The practice, with its footprint type: planted silvoarable agroforestry (hectares), riparian buffers (kilometres of stream zone), assisted natural regeneration (hectares). Geography and climate: a country or uploaded boundary, cell size 1, 5 or 10 km, and baseline 1995–2014 with or without SSP2-4.5 2050. [src: docs/redesign/01-setup.html §1.1.1]

**What the stage shows.** The scope, and a pointer to two optional activities kept out of the walkthrough: choosing datasets and tuning rules. [src: docs/redesign/01-setup.html §1.1.2]

**The method behind it.** M0 records the practice, the AOI as [[table:T7]] contexts, the administrative level, resolution, climate mode and scenarios, resolves the recipe and the dataset bindings ([[table:BIND]]), and runs a data-readiness and resolution-honesty check ([[ch:m0-setup]]). The practice's footprint type is the family's spatial product type in [[table:FAM]] ([[ch:m1-suitability]]). Screen: [Stage 01 Setup](https://ciat.github.io/nbs_ruralscan/redesign/01-setup.html).

## Explore the practices

**The question.** Which practices could answer this challenge, and what is each one? [src: docs/redesign/02-practices.html §Stage 02]

**What the user chooses.** One of three worked examples. The page states that these "demonstrate different practice types; they are not the full NbS catalogue". Choosing one sets it in the control bar. [src: docs/redesign/02-practices.html §Stage 02]

**What the stage shows.** 2.1 What it is: the practice and its families, each with its limiting condition and product type. 2.2 Where it fits: the variables, their dimension (biophysical, existing land-use system, hard exclusion) and which one limits. 2.3 What it addresses: one row per problem with an effect word (weak, moderate or strong benefit; no clear effect; adverse), a confidence word (low, medium, high) and a study count, all labelled "illustrative, not an evidence synthesis". The reading rules: direction, magnitude and confidence are separate; conflicting evidence keeps both directions visible; low confidence does not mean no effect. 2.4 What it costs: indicative ranges (example establishment cost for planted silvoarable agroforestry USD 420 to 1,150 per ha) with no linked cost evidence, not to be used for budgeting. 2.5 Key reading: syntheses and primers from the source register. [src: docs/redesign/02-practices.html §2.1] [src: docs/redesign/02-practices.html §2.3] [src: docs/redesign/02-practices.html §2.4] [src: docs/redesign/02-practices.html §2.5]

**The method behind it.** Families, limiting factors and product types are in [[table:FAM]] and the practice chapters. Effect rows are generated by cell synthesis with two-axis confidence and a transfer class ([[ch:effect-synthesis]], [[ch:m5-scorecard]]). Costs are ordinal classes with gated value ranges ([[ch:cost-profiles]]). Readings come from [[table:SRC]]. Screen: [Stage 02 Explore the practices](https://ciat.github.io/nbs_ruralscan/redesign/02-practices.html).

## Opportunity space

**The question.** Where could the chosen practice establish? [src: docs/redesign/03-opportunity.html §Stage 03]

**What the user chooses.** The suitability classes that form the opportunity space (control bar); a baseline or "change, baseline to 2050" map; classes to summarise on the people-and-land and livelihood-risk sub-tabs; filters and sort order for the problem table.

**What the stage shows.**

- *3.1 Map and footprint.* "Four classes, one rule set": Very high to Low ranks how well each cell fits the envelope; every later stage uses the selected classes. Excluded cells (hatched) are removed by law or land cover; no-data cells (dotted) are counted as neither. "A cell is not a farm": a 5 km cell is 2,500 ha. The 2050 view "moves the envelope, not the farms". [src: docs/redesign/03-opportunity.html §3.1] An inset shows a 100 ha exclusion parcel inside one cell: the cell keeps its class and the parcel is reported as a separate shape. [src: docs/redesign/03-opportunity.html §Stage 03] The example breaks fall at the 30th, 60th and 85th percentiles of eligible cells. [src: docs/redesign/v1b-fixture.js §breaks]
- *3.1.1 to 3.1.3.* Exclusions come from mapped boundaries (built-up land, mangrove and wetland, protected areas), not scores; excluded, low and no data must never be merged; roads, markets and tenure stay off the map because investment can change them. [src: docs/redesign/03-opportunity.html §3.1.2] [src: docs/redesign/03-opportunity.html §3.1.3]
- *3.2 People and land.* Poverty, food insecurity, soils, biodiversity, carbon and water stress, classed by C.5 settings; they "describe needs", not the practice's effect. [src: docs/redesign/03-opportunity.html §3.2]
- *3.3 Risk to rural livelihoods.* Population shares in hazard risk classes, baseline and about 2050: "need, not project risk", never added to it. [src: docs/redesign/03-opportunity.html §3.3]
- *3.4 Problems.* For ten problems, the share of the opportunity space in each national fifth (20% is the reference), beside the illustrative response, which is "pooled evidence from elsewhere, not local measurement". [src: docs/redesign/03-opportunity.html §3.4]
- *3.5 Rural services.* A fictional two-department example of roads, schools and clinics exposed to flood, landslide or wildfire. [src: docs/redesign/03-opportunity.html §3.5]

**The method behind it.** Suitability, family product types, masks and classes are M1 ([[ch:m1-suitability]]); the fingerprint, T5 variables and problem distribution are M3 ([[ch:m3-characterisation]], [[table:T5]]); livelihood risk is M2 ([[ch:m2-climate-risk]], [[table:T2]], [[table:T3]]); the response columns are the M5 presentation of [[table:T6]] ([[ch:m5-scorecard]]). Screen: [Stage 03 Opportunity space](https://ciat.github.io/nbs_ruralscan/redesign/03-opportunity.html).

## Project risk

**The question.** What could harm the planting, and who could the project affect? [src: docs/redesign/04-risk.html §Stage 04]

**What the user chooses.** The hazard view (fire, flood, or both), and on 4.4 what happens to places that are needed but risky: keep them with the flag, or take High-flag places off the shortlist before hotspots are found. The screen calls this "the task team's call, recorded in the brief". [src: docs/redesign/04-risk.html §4.4]

**What the stage shows.**

- *4.1 Hazard map.* Fire and flood exposure of the opportunity space over a five-year establishment period. "A flag is exposure, not a loss rate"; "there is no overall risk score". [src: docs/redesign/04-risk.html §4.1] Per hazard, High is the top quarter nationally (burned-area frequency, 1-in-100-year flood depth), Moderate the next quarter, Low the lower half, as example quantiles. [src: docs/redesign/04-risk.html §4.1.2] Adding fire and flood "would hide which hazard is driving a flag, and so which response fits". [src: docs/redesign/04-risk.html §4.1.3]
- *4.2 Asset vulnerability.* Example threat class, establishment sensitivity and evidence class per practice and hazard, "not combined with exposure into a score". [src: docs/redesign/04-risk.html §4.2]
- *4.3 Flags for follow-up.* A desk review of road access, market access, land tenure, extension, finance and credit, conflict and fragility, and labour, with possible sources; gaps go into the brief. The worked concern is fencing that blocks a seasonal grazing route. [src: docs/redesign/04-risk.html §4.3]
- *4.4 Trade-off.* Hectares kept or removed by district under each choice. [src: docs/redesign/04-risk.html §4.4]

**The method behind it.** M2b Stream A (asset hazard exposure from [[table:T2]] and [[table:T3]] asset-threat rows, modulated by the establishment period in [[table:T0]]) and Stream B (operational and enabling-environment levers), applied as a filter or flag and never summed ([[ch:m2b-project-risk]]). Screen: [Stage 04 Project risk](https://ciat.github.io/nbs_ruralscan/redesign/04-risk.html).

## Priority hotspots

**The question.** Where does the opportunity meet the project's priorities? [src: docs/redesign/05-hotspots.html §Stage 05]

**What the user chooses.** The map variant (hotspots, need, suitability × need, district summary); the hotspot score (High+ or Very high) in the control bar; on 5.2, objectives (tick two or three), a weight preset (climate adaptation, livelihood, biodiversity, balanced, custom) and a per-layer weight of none, low, medium or high. The example preset is balanced, with every weighted layer at medium. [src: docs/redesign/05-hotspots.html §5.2]

**What the stage shows.** 5.1: "A hotspot is an intersection, not a sum": a cell in the opportunity space whose need is at or above the chosen hotspot score. Correlated need layers are clustered, one representing each group; "residents are not beneficiaries"; a national gender index (example 0.61) is context because "it cannot rank districts". [src: docs/redesign/05-hotspots.html §5.1] 5.2: layers grouped as climate hazard, NbS response, people and production (weighted), equity and inclusion (flags) and context (descriptors), each with a data-sensitivity mark. [src: docs/redesign/05-hotspots.html §5.2] 5.3: four steps from opportunity space to hotspot classes. [src: docs/redesign/05-hotspots.html §5.3] 5.4 and 5.5: a district ranking with a narrative, and a hotspot fingerprint. [src: docs/redesign/05-hotspots.html §5.4] [src: docs/redesign/05-hotspots.html §5.5]

**The method behind it.** M4 standardises priorities, turns user settings into weights, optionally reconciles them with AHP + CRITIC + Entropy, combines them by weighted linear overlay inside the M1 mask, classifies, ranks administrative units and tests sensitivity ([[ch:m4-hotspots]]). Correlation reduction and the priority versus descriptor split are M3 ([[ch:m3-characterisation]]). Screen: [Stage 05 Priority hotspots](https://ciat.github.io/nbs_ruralscan/redesign/05-hotspots.html).

## NbS comparison

**The question.** How do the practices compare on a common footing? The page promises "a side-by-side, not a ranking". [src: docs/redesign/06-comparison.html §Stage 06]

**What the user chooses.** Which practices are active (others are muted), and on 6.3 a budget amount, currency (USD, EUR, XOF), price year and whether costs count establishment only or three years of maintenance. [src: docs/redesign/06-comparison.html §6.3]

**What the stage shows.** 6.1: footprint (Very high + High), overlap with need, top problems with strength and confidence, indicative cost, and affordable area at an example USD 5,000,000. Areas are nominal and riparian kilometres "are not comparable with hectares"; footprint is room, not a target; overlap is not compatibility. [src: docs/redesign/06-comparison.html §6.1] 6.2: every problem row for every practice; an empty cell means no evidence was pooled, "not that there is no effect". [src: docs/redesign/06-comparison.html §6.2] 6.3: affordable area = budget ÷ cost per unit, USD only, undiscounted. [src: docs/redesign/06-comparison.html §6.3] 6.4: five scorecard indicators with what the scan can and cannot report. [src: docs/redesign/06-comparison.html §6.4]

**The method behind it.** M5 presents generated [[table:T6]] and [[table:T3]] rows through fixed display lookups and keeps costs in [[table:T6E]] ([[ch:m5-scorecard]], [[ch:cost-profiles]]). Screen: [Stage 06 NbS comparison](https://ciat.github.io/nbs_ruralscan/redesign/06-comparison.html).

## Next steps

**The question.** What must feasibility confirm before anyone invests? [src: docs/redesign/07-next.html §Stage 07]

**What the user chooses.** Nothing analytical; the brief is generated from the current selection and can be copied.

**What the stage shows.** Figure 7.1 is a scoping brief: scope line, hotspot map, assumptions (nominal cell areas, the published envelope unadjusted locally, global exclusion boundaries, 5 km need proxies, a five-year establishment period, undiscounted mixed-source costs) and questions split into feasibility, design and implementation actions, stamped "Scoping grade. Not a feasibility finding." [src: docs/redesign/07-next.html §Figure 7.1] 7.2 separates what can be reused (maps, summaries, caveated figures, assumptions) from what must be redone locally (costs, parcel-scale exclusions, local need, participation). [src: docs/redesign/07-next.html §7.2] 7.3 lists what happens outside the scan: local co-production, feasibility studies and a monitoring baseline. [src: docs/redesign/07-next.html §7.3]

**The method behind it.** M6 states the stage pathway, the indicative economic snapshot, next steps tied to scan outputs, feasibility signposts, the sensitive-variable recommendation and the safeguard trigger ([[ch:m6-handoff]]). Screen: [Stage 07 Next steps](https://ciat.github.io/nbs_ruralscan/redesign/07-next.html).

## Technical configuration

**The question.** What sits underneath the walkthrough? "The walkthrough never needs this page." [src: docs/redesign/00-config.html §Technical configuration]

**What the user chooses.** C.1: the dataset for each variable (grain, year, tier, context override, sensitivity); a change is a proposal applied only after a compatibility check. C.2: variable cards for slope, precipitation and land cover, each with a membership curve and raw and transformed maps. C.3: masks (protected areas, water bodies, built-up land, and an optional 25 degree slope preview not applied to the walkthrough); soft access, finance and tenure factors are listed as "not masks". C.4: an absolute correlation threshold (default |r| = 0.70), one representative per cluster within a theme. C.5: per need or hazard indicator, direction, 2, 3 or 5 classes, and quantile or threshold cuts (default three quantile classes, higher is worse). C.6: save and load settings. [src: docs/redesign/00-config.html §C.1] [src: docs/redesign/00-config.html §C.2] [src: docs/redesign/00-config.html §C.3] [src: docs/redesign/00-config.html §C.4] [src: docs/redesign/00-config.html §C.5] [src: docs/redesign/00-config.html §C.6] [src: docs/redesign/v1b-classification.js §get]

**What the stage shows.** C.3 states the rule that a zero score is not an exclusion: in a weighted combination a zero can be offset, whereas a hard mask removes the cell before combination. [src: docs/redesign/00-config.html §C.3] C.5 labels people-and-land classes Better or Worse (Best and Worst with five classes) and hazards Low, Moderate or High risk; quantile breaks come from baseline values within the baseline opportunity extent and classify both baseline and future values. [src: docs/redesign/00-config.html §C.5]

**The method behind it.** Dataset binding and context sensitivity ([[ch:farming-systems-and-data]], [[table:BIND]], [[table:VONT]]); membership functions and masks ([[ch:m1-suitability]], [[table:T4]]); two-stage variable selection with |r| > 0.7 ([[ch:m3-characterisation]]). Screen: [Technical configuration](https://ciat.github.io/nbs_ruralscan/redesign/00-config.html).

## Where the visual methodology and the written specification differ

The visual methodology and the written module specifications were revised at different times, and in several places they now describe different things. The table records the differences, most consequential first. It does not resolve them. Until they are reconciled, the tables and module specifications at the pinned revision remain the source of record for anything a pipeline executes.

| Topic | What the visual methodology shows | What the written module specification says | Status |
|---|---|---|---|
| Project-risk composition | One flag per hazard, three classes per hazard (top quarter, next quarter, lower half), no overall risk score; only fire and flood mapped. [src: docs/redesign/04-risk.html §4.1.2] [src: docs/redesign/04-risk.html §4.1.3] | A weighted multiplicative composite across asset-threat hazards, normalised to 0 to 1 and classed Low, Medium, High, Very High (cut-offs unspecified); exclude or flag High and Very High. Composition is listed as an open question. [src: methodology/modules/M2b_project_risk.md §6] [src: methodology/modules/M2b_project_risk.md §8] [src: methodology/modules/M2b_project_risk.md §11] ([[ch:m2b-project-risk]]) | Visual methodology is the later statement |
| Soft enabling factors | Desk checks with suggested sources (roads, markets, tenure, extension, finance, conflict, labour), gaps carried into the brief; not mapped. [src: docs/redesign/04-risk.html §4.3] Other screens still call them "levers" shown in Stage 4. [src: docs/redesign/03-opportunity.html §3.1.3] [src: docs/redesign/00-config.html §C.3] | Eight mapped Stream B levers, including electrification, with indicative datasets, each a what-if scenario lever and a filter or flag input. [src: methodology/modules/M2b_project_risk.md §12] | Visual methodology is the later statement |
| Safeguard for Indigenous peoples' and local communities' land | IPLC lands an overlay flag that is not weighted; potential impacts referred to environmental and social specialists, who assess consent requirements under the Environmental and Social Framework. [src: docs/redesign/05-hotspots.html §5.2] [src: docs/redesign/07-next.html §7.3] | An overlap of IPLC land with the opportunity space must set `FPIC_REQUIRED` and raise ESS7 in the hand-off. [src: methodology/modules/M6_handoff.md §10] [src: methodology/modules/M2b_project_risk.md §12] ([[ch:m6-handoff]]) | Open |
| Budget | Affordable area = budget ÷ cost per unit, USD only, with an optional three years of maintenance. [src: docs/redesign/06-comparison.html §6.3] | The scan does not allocate budget or select a portfolio [src: methodology/framework.md §What this framework does not do]; costs are ordinal classes, value ranges are shown as is and consumers never compute new ratios. [src: methodology/T3_T6_developer_handover.md §3] ([[ch:cost-profiles]]) | Written specification is better founded (on the ordinal, ungated-ratio rule for mixed-year, mixed-currency costs) |
| Weighting input | Objectives (five, tick two or three) choose which need layers appear; four presets plus custom set each layer to none, low, medium or high; Stage 1 says objectives do not re-weight any map. [src: docs/redesign/01-setup.html §1.1.1] [src: docs/redesign/05-hotspots.html §5.2] | Per-priority none, low, medium or high, coded 0 to 3 and normalised; no presets. M0 has no objectives input. [src: methodology/modules/M4_hotspots.md §6] [src: methodology/modules/M0_setup.md §3. Inputs] ([[ch:m4-hotspots]], [[ch:m0-setup]]) | Open |
| Hybrid weighting | "The method combines expert weights with data-driven ones", AHP, CRITIC and entropy. [src: docs/redesign/05-hotspots.html §5.3] | Reconciliation is optional and off in the default configuration; the user's weights are used directly. [src: methodology/modules/M4_hotspots.md §6] | Open |
| Which T5 layers are weighted | Gender inequality and IPLC lands are flags, not weighted; water stress sits under climate hazard; water quality and catchment water yield are absent. [src: docs/redesign/05-hotspots.html §5.2] | `gender_inequity` and `iplc_lands` are priorities in `equity_inclusion`; `water_stress` is `people_production`; `water_quality_risk` and `catchment_water_yield` are priorities. A national gender index becomes a qualifier through the spatial-grain rule. [src: schema/T5_opportunity_space.csv] [src: methodology/opportunity_space_T5.md §Spatial-grain rule] | Written specification is better founded (the T5 table is the ratified row set) |
| Suitability classes | Very high, High, Moderate, Low; the user selects any set of classes (default Very high + High); example breaks at the 30th, 60th and 85th percentiles; excluded and no data kept separate. [src: docs/redesign/03-opportunity.html §3.1] [src: docs/redesign/v1b-fixture.js §breaks] | Four quartile classes labelled unsuitable, marginal, moderate, highly suitable, with the opportunity space fixed as the top two; the same file's purpose and output sections describe five classes including excluded. [src: methodology/modules/M1_suitability.md §6.8 Classification & fingerprint extraction] [src: methodology/modules/M1_suitability.md §1. Purpose] M4 lets the user choose which classes count. [src: methodology/modules/M4_hotspots.md §8] ([[ch:m1-suitability]]) | Open |
| Livelihood climate risk | Each hazard (drought, flood, soil erosion, heat) shown separately as population shares in quantile risk classes of a hazard indicator; no exposure term, no mode. [src: docs/redesign/03-opportunity.html §3.3] [src: docs/redesign/00-config.html §C.5] | A composite index, normalised weighted sum of hazard × exposure (Mode A) or × vulnerability (Mode B); erosion is a T6 priority, not a T3 hazard. [src: methodology/modules/M2_climate_risk.md §6.5] [src: schema/spec.md §T3] ([[ch:m2-climate-risk]]) | Open |
| Problem rows and effect wording | Stage 2 rows include rural income, water quality and carbon; Stage 3 has ten rows including soil degradation, carbon loss and water stress; words weak, moderate, strong benefit, no clear effect, adverse; low, medium, high confidence with a study count. [src: docs/redesign/02-practices.html §2.3] [src: docs/redesign/03-opportunity.html §3.4] | Fixed generated rows: erosion, drought, flood, heat; biodiversity loss, carbon removals, rural poverty, gender inequality, food insecurity, water-table depletion (pooling water stress, catchment water yield and water quality); slight, moderate, strong benefit or harm; special chips for studies disagree, too little evidence, not assessed. [src: schema/lookups/scorecard_rows.csv] [src: schema/lookups/scorecard_chip_scale.csv] ([[ch:m5-scorecard]]) | Written specification is better founded (rows and scale are generated from lookups) |
| Asset vulnerability source | Example classes High, Moderate, Low per hazard; some tagged "Expert judgement". [src: docs/redesign/04-risk.html §4.2] | `asset_sensitivity` none to very high, generated from a WOCAT seed and literature; no external expert elicitation; data-deficient cells left blank. [src: methodology/T3_T6_generation_method.md §9] [src: methodology/T3_T6_generation_method.md §7.5] | Written specification is better founded (on generated, evidence-traced rows) |
| Road and rural-services exposure | Roads, schools and health facilities exposed to flood, landslide or wildfire; an optional priority with weight 0 to 50% (default 20%): selected score = (1 − w) × base + w × exposed share of assessed road length. [src: docs/redesign/03-opportunity.html §3.5] [src: docs/redesign/v1b-road-example.js §render] | Infrastructure is not a top-level opportunity-space theme; it is a descriptor or a Stream B lever. [src: methodology/opportunity_space_T5.md §What did NOT make it (and why)] | Open |
| Practice families | Assisted natural regeneration split into fallow regeneration, farmer-managed regeneration, enrichment planting; riparian into buffer strips and riparian forest restoration, labelled applicability zone; agroforestry linear plantings reported in km. [src: docs/redesign/02-practices.html §2.1] | Forest restoration families are passive, assisted, active planting, plantation, protection and community forest management; farmer-managed regeneration is the agroforestry regeneration family; both riparian families are `zonal_linear`; the agroforestry linear family is `applicability_zone`. [src: schema/registers/FAM_family_registry.csv] | Written specification is better founded (the family registry) |
| Optional slope mask | A slope-above-threshold mask preview (25 degrees), not applied to the walkthrough. [src: docs/redesign/00-config.html §C.3] | Hard masks are legal or physical exclusions; a low suitability class is not an exclusion. [src: methodology/T4_developer_contract.md §Planted host and exclusion contracts] | Written specification is better founded (slope is a suitability response) |
| Resolution, scenarios, classes | Cells 1, 5 or 10 km, walkthrough at 5 km; climate "Baseline 1995–2014" and "SSP2-4.5 about 2050"; four need classes and a High+ or Very high hotspot cut. [src: docs/redesign/01-setup.html §1.1.1] [src: docs/redesign/v1b-fixture.js §rollup] | M0 offers 5 km, 1 km, 500 m (default 5 km), M1 10 km to 100 m (default 1 km); T2 scenarios `baseline`, `future_ssp126`, `future_ssp245`, `future_ssp585`; M4 asks for five hotspot classes. [src: methodology/modules/M0_setup.md §3. Inputs] [src: methodology/modules/M1_suitability.md §3. Inputs] [src: schema/spec.md §T2] [src: methodology/modules/M4_hotspots.md §4] | Open |

Some rows overlay differences inside the written specification itself (M1's class count, the default resolution, soft-lever routing); the module chapters record those.

## What the visual methodology does not show

Some parts of the method have no counterpart on any screen.

- **Calibration status of suitability mappings.** The C.2 curves carry example parameters and no calibration status. For the pinned edition, a held or unrecorded calibration is never a score, a range or "reviewed"; the defensible statement is whether a site lies within a documented use range, with the score unassigned ([[ch:m1-suitability]], [[ch:suitability-synthesis]]). The curves are not approved responses.
- **Transfer class and applicability of effect rows**, and effect locus, directness, the maladaptation caution and the `no_applicable_evidence` state ([[ch:effect-synthesis]], [[ch:m5-scorecard]]).
- **Two-axis confidence.** The evidence and agreement axes behind the three confidence words are not shown.
- **Sensitivity outputs** from M1 and M4 ([[ch:m1-suitability]], [[ch:m4-hotspots]]).
- **The data-readiness check**, needs-upload prompts and the resolution-honesty flag ([[ch:m0-setup]]).
- **The two modes of livelihood risk** and the Mode B double-count guard ([[ch:m2-climate-risk]]), and T3 livelihood rows keyed by farming system.
- **Practices beyond the three examples**, and most families of those three ([[ch:practice-mangrove_restoration]], [[ch:practice-water_harvesting_conservation]], [[ch:practice-wetland_management]]).

The reverse also holds. The screens carry elements that no chapter specifies:

- the affordable-area calculation (6.3) and the five-indicator reporting table (6.4);
- the rural-services exposure example and its weighted road-exposure priority (3.5, 5.2, 5.4);
- user-set class counts, directions and cut points for need and hazard indicators (C.5);
- a sub-cell exclusion parcel that leaves the cell's class unchanged and is reported as its own shape (3.1);
- residents per cell from a district total spread evenly, an example device with no method behind it [src: docs/redesign/v1b-fixture.js §residents];
- two concept-only assistance features for drafting the brief and querying the evidence base (7.2).

## Assumptions and limits

- **Example data only.** No figure, class, chip, cost or rank on the screens is a result; a reader who needs a value must go to the generated tables. [src: docs/redesign/v1b-fixture.js §header]
- **A statement of intent.** The screens do not establish that any stage has been implemented, run, validated or calibrated; the module chapters record that status.
- **Not the source of record.** Where screens and specifications differ, the pinned tables and specifications govern execution. Being later is not the same as being reconciled.
- **Scoping, not feasibility.** No site design, cost-benefit analysis or ecosystem-service modelling; residents are not beneficiaries; overlap is not compatibility. Feasibility must still confirm land, tenure and consent, replace sensitive global data with country-endorsed sources, quantify costs and effects with site data, and design layouts. [src: docs/redesign/index.html §H.4] [src: docs/redesign/07-next.html §7.3]
- **Two risk lenses stay apart.** Livelihood risk (a need layer) and investment risk (a filter or flag) are never summed, with each other or with suitability.
- **Partial coverage.** Three practices, one country geometry, two project-risk hazards; nothing about other practices or hazards can be read from the screens.

## Where this is configured

The visual methodology reads no table: its pages and fixtures are self-contained display files. [src: docs/redesign/v1b-fixture.js §header] What each stage would read in a realisation of the method is configured as follows.

- Setup: [[table:T0]], [[table:T7]], [[table:T1]], [[table:BIND]], [[table:VONT]].
- Explore the practices: [[table:FAM]], [[table:SRC]], [[table:T6]], [[table:T3]], [[table:T6E]].
- Opportunity space: [[table:T4]], [[table:T5]], [[table:T2]].
- Project risk: [[table:T3]] asset-threat rows, [[table:T2]], [[table:T0]] establishment period, [[table:T4]] operational rows outside the suitability surface.
- Priority hotspots: [[table:T5]] and the run configuration.
- NbS comparison: [[table:T6]], [[table:T3]], [[table:T6E]] and the scorecard lookups in `schema/lookups/`.
- Next steps: the M6 hand-off, drawing on [[table:T0]] and [[table:T6]].
