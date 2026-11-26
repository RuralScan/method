---
title: "M3: Classifying the opportunity space"
slug: m3-characterisation
summary: Describe people, production and environmental concerns within candidate areas without confusing context with priority or benefit.
sources:
  - method:priority/README.md
  - method:priority/infrastructure/README.md
  - method:priority/research/2026-11-26-biodiversity-loss-classes.md
  - method:priority/conservation/README.md
  - method:data-model/priority-contract.json
  - methodology/modules/M3_characterisation.md
  - method:handbook/implement-a-scan.md
  - methodology/opportunity_space_T5.md
  - methodology/modules/M5_scorecard.md
  - methodology/framework.md
  - methodology/modules/M4_hotspots.md
  - AGENTS.md
  - schema/registers/BIND_dataset_binding.csv
  - schema/spec.md
  - methodology/T4_generation_method.md
---

## Question this module answers

Module 3 (M3) describes who and what lies within the opportunity space: rural people, production systems, environmental conditions and development concerns. It supplies context and eligible priority indicators to M4. It does not rank areas or estimate the benefits an intervention would cause. [src: methodology/modules/M3_characterisation.md §2]

## From opportunity space to priority

First classify each selected concern inside the opportunity space. Check overlapping indicators, then apply the user's weights to obtain the priority score in M4. Raw values, problem classes and weights remain visible separately. [src: method:priority/README.md]

{{priority-workflow}}

M2b sits beside this workflow as an investment-risk screen. It never contributes another weighted term. The highest score identifies the strongest combination of selected concerns, not the greatest proven benefit from an intervention. [src: method:priority/README.md]

## Inputs

Use the M1 candidate-area definition, T5 variables, context-appropriate datasets and the geographic units needed for summaries. Keep excluded and unknown areas distinguishable from assessed candidate areas. Record the dates, units, spatial support and missing-data coverage of each input. [src: methodology/modules/M3_characterisation.md §3] [src: method:handbook/implement-a-scan.md §3. Build the scoping brief]

## Priorities and descriptors

Every [[table:T5]] row has a role. **Priorities** describe concerns that may enter M4's ranking. **Descriptors** explain the landscape but carry no priority weight. Population, for example, can describe how many people live within a shortlisted area without automatically making that area a higher priority. T6 effect rows attach to priorities, not descriptors. [src: methodology/opportunity_space_T5.md §mcda_role - priority vs descriptor]

Table: Themes organising the characterisation variables.

| Theme | Question | Role |
|---|---|---|
| Climate hazard | Where is climate exposure concentrated? | Priority |
| NbS response | Where are environmental problems the practice might address? | Priority |
| People and production | Where are livelihoods and production under pressure? | Priority |
| Equity and inclusion | Whose disadvantage needs attention? | Priority |
| Context | What describes the landscape and its people? | Descriptor |

[src: methodology/opportunity_space_T5.md §The five-lens scheme (v0.3.0)]

The environmental-need theme does not measure an intervention's effect. Water stress or biodiversity loss can be present where evidence for a particular practice's response is weak. M5 presents that response evidence separately. [src: methodology/modules/M3_characterisation.md §5] [src: methodology/modules/M5_scorecard.md §6]

## Method

### 1. Assemble suitable inputs

Select data for the target geography through [[table:T1]] and [[table:BIND]], following [[ch:farming-systems-and-data]]. Preserve the difference between a gridded estimate, an administrative statistic and a mapped feature. Resampling a national statistic does not create within-country information. [src: methodology/modules/M3_characterisation.md §6] [src: methodology/opportunity_space_T5.md §Spatial-grain rule]

A priority needs subnational information to distinguish locations within a country. A country-only value remains context or a qualified flag. Report unavailable indicators and any fallback sources so the reader can see which concerns the assessment covers. [src: methodology/opportunity_space_T5.md §Spatial-grain rule]

### 2. Classify each concern and retain raw values

Each T2 or T5 priority refers to a versioned classification rule. The common scores are **none = 0, low = 0.33, medium = 0.66, high = 1**. They describe the concern being prioritised, not suitability, a probability or a measured intervention benefit. Descriptors remain in their original units. [src: method:data-model/priority-contract.json]

**Thresholds are the default.** Record three ordered cutoffs in native units, the direction of concern, context and justification. A value exactly on a cutoff belongs to the lower raw-value interval; reverse the class labels where lower raw values mean more concern. Keep the source values and units available beside the classes. [src: method:priority/README.md §Classification]

**Terciles are a relative alternative.** Use an explicitly identified reference area/population and period, retaining its realised cutoffs for comparisons. Three groups cannot create a fourth no-problem class: define a defensible no-problem condition first, or use only low, medium and high. Do not split tied values to force equal group sizes. Collapsed cutoffs require another rule. Quintiles are not used. [src: method:priority/README.md §Classification]

A missing value is **unknown**, never none. A rule needs its own reference, units, scope and decision record; this method supplies no unreviewed universal cutoffs for poverty, drought or other concerns. AI may propose a classification with supporting reasoning; validating its format does not approve its science. [src: method:priority/README.md §Execution and approval boundary]

**Poverty must be contextualized to the setting.** Select an appropriate poverty measure, poverty line, reference year and class interpretation. Do not transfer US concentrated-poverty thresholds to international poverty estimates. Prefer suitable published classifications; otherwise default to global reference distributions within each World Bank income tier, recording the grouping vintage, weighting and fixed cutoffs. Regional or national adaptations require documented contextual justification. These classes are relative to the comparison group, not universal severity thresholds. A subnational all-population estimate remains area context, not a rural-only estimate; missing or a low relative rank does not establish absence of poverty. [src: method:priority/README.md §Poverty must be contextualized]

### 3. Check overlap and correlations before weighting

Group variables by meaning, then inspect their raw and classified relationships inside the opportunity space. Choose and record one representative for each shared concern. A climate variable appearing in both T2 and T5 must not enter twice under different names. Preserve the omitted variables for interpretation and explain the choice. Correlation alone does not make distinct policy concerns interchangeable. [src: method:priority/README.md §Correlation and weighting]

The reference evaluator reports correlations but does not automatically delete variables or change weights. CRITIC is assessed as a comparison method in [[ch:m4-hotspots]], not adopted as a hidden correction to user priorities. The final selection and any retained correlated concerns belong in the sensitivity record. [src: method:priority/README.md §Correlation and weighting]

### 4. Summarise the candidate areas

Describe the opportunity space and its geographic subdivisions using quantities appropriate to each dataset: totals, shares or distributions with stated denominators. Examples include population, production value, dominant farming systems and the distribution of environmental concerns. Report missing-data coverage and use the family's valid footprint unit. [src: methodology/modules/M3_characterisation.md §6] [src: method:handbook/implement-a-scan.md §3. Build the scoping brief]

A count of residents within a candidate zone is not a count of beneficiaries. It describes spatial overlap; whether those residents benefit depends on access, design, participation and where the intervention's effects occur. M5 addresses effect interpretation and M6 the local assessment. [src: methodology/modules/M3_characterisation.md §4] [src: methodology/modules/M5_scorecard.md §6]

## Biodiversity context at its supported resolution

Use the selected NHM Biodiversity Intactness Index v2.1.1 2020 raster provisionally as coarse landscape context. Its 5-arc-minute grid is approximately 10 km at the equator. State the year and native resolution in the display and methods; resampling does not reveal farm-scale variation or fine changes at conservation-site boundaries. Preserve missing cells and distinguish modelled condition relative to a reference from observed annual loss. [src: method:priority/research/2026-11-26-biodiversity-loss-classes.md §Approved interim use: coarse context]

Retain the approved four BII classes and the higher-of-BII-and-KBA rule for the single Biodiversity priority entry. Keep each input's resolution and the controlling input visible. Both inputs must be valid: where KBA data are unavailable, the BII input may be shown as coarse context while the combined priority remains Not assessed. This interim use does not add another weight or claim that runtime adoption is complete. [src: method:priority/conservation/README.md §Interim BII resolution decision]

## Infrastructure exposure and national datasets

Roads, power lines, buildings, schools and health facilities may be overlaid with the selected hazards for desk scoping. Report mapped, assessed, potentially exposed and unassessed assets with their source dates and spatial coverage. Exposure does not establish damage, service disruption or protection by an NbS. Building footprints do not identify occupants or critical services, and mapped line length does not establish electricity-network capacity. [src: method:priority/infrastructure/README.md]

Acquire suitable national datasets from the responsible ministries, utilities and mapping agencies for country applications, including worked examples. Use these to replace global versions through context-specific bindings after checking observation dates, completeness, geometry, asset definitions, duplicates and use conditions. National origin alone does not guarantee currency or fitness; replace only the coverage the source supports. Global layers remain explicitly labelled fallbacks where suitable national data are unavailable. Preserve source boundaries and reconcile overlaps rather than adding inventories together. Missing features or missing hazard coverage remain unknown, never zero exposure. Record outstanding national-data acquisition needs in the hand-off. [src: method:priority/infrastructure/README.md §National data should replace global fallbacks where suitable]

T1 records source coverage and spatial support; BIND links each variable to a global default or a more specific country/region context in T7. Its specified fallback rule keeps missing national-data requirements visible while a global source is used. A national source may cover only some departments or asset types, so country coverage must not be interpreted as completeness. The Haiti source-selection table records provisional inventories and the national replacements still required; executable switching and coverage-aware combination must be verified in the runtime before claiming they occur automatically. [src: method:priority/infrastructure/README.md §How existing tables represent global and national data]

## Example: the production gap

`production_gap` is the shortfall between actual and attainable productivity of the dominant farming system. The appropriate quantity differs across systems: a crop-yield gap for cropping, a productivity measure for rangeland, and a documented combination for mixed systems. Context-specific bindings identify the relevant input. [src: AGENTS.md §What is locked] [src: schema/registers/BIND_dataset_binding.csv]

A crop-yield percentage and a rangeland productivity gap should not be pooled as though they were the same raw measurement. Retain their definitions, denominators and system context. If no suitable input exists, report that the priority was unavailable; do not fill the gap with a convenient but unrelated layer. [src: methodology/opportunity_space_T5.md §Priorities (13)] [src: schema/spec.md §BIND]

## Carry sensitive-data and safeguard questions forward

Population, poverty and production estimates may need confirmation with national sources. Apply the context-sensitivity guidance in [[ch:farming-systems-and-data]] and retain those qualifications in the hand-off. [src: methodology/T4_generation_method.md §2.6]

Mapped overlap with Indigenous Peoples' and local community land is a prompt for safeguard assessment and consultation. Absence of a mapped polygon is not evidence of absence of people or rights. [[ch:m6-handoff]] explains the next-step guidance; the overlap itself is not a completed safeguard assessment. [src: methodology/modules/M3_characterisation.md §12]

## Outputs

Provide raw and transformed priority layers, descriptive summaries, geographic distributions, data coverage and the record of representative-indicator choices. M4 uses eligible priorities to rank areas; M5 reads problem presence alongside response evidence; M6 receives contextual and validation questions. [src: methodology/modules/M3_characterisation.md §4]

## Assumptions and limits

Characterisation is limited by the dates, spatial support and coverage of its inputs. Relative scores do not establish absolute severity. Correlated variables can still represent distinct concerns, and a substituted source can change the meaning of an indicator. Country and field validation must confirm the locally important conditions before investment decisions. [src: methodology/opportunity_space_T5.md §Spatial-grain rule] [src: methodology/framework.md §Variable selection (two stages)] [src: method:handbook/implement-a-scan.md §3. Build the scoping brief]

## Where this is configured

[[table:T5]] identifies themes and roles; [[table:T1]] and [[table:BIND]] describe data and contextual choices; [[table:VONT]] describes units, resolution and sensitivity; [[table:T7]] defines summary units. [[table:T2]] supplies climate-variable definitions. Both registries reference the shared classification contract; the run record retains resolved cutoffs, reference hashes, indicator selection, unavailable data and user weights. [src: method:data-model/priority-contract.json]
