---
title: "M3: Characterising the opportunity space"
slug: m3-characterisation
summary: Describe people, production and environmental concerns within candidate areas without confusing context with priority or benefit.
sources:
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

### 2. Identify related indicators before prioritisation

Group indicators by their meaning, then inspect their relationships within the area of interest. Select and record representatives where related layers would otherwise count the same underlying pattern repeatedly. Retain the full set for interpretation and record which indicator each representative stands for. Statistical correlation alone does not establish that two policy concerns are interchangeable. [src: methodology/framework.md §Variable selection (two stages)] [src: methodology/modules/M3_characterisation.md §4]

Check overlap with the M2 vulnerability formulation. A concern already included in a climate-risk composite should not silently gain extra weight through another entry in M4. Descriptors carry no weight and can remain available for explanation. [src: methodology/modules/M3_characterisation.md §9]

### 3. Standardise priorities and retain raw values

Apply the declared direction and scaling rule to each eligible priority. Keep raw values and units beside the transformed layer. The reference frame determines whether the score expresses absolute severity or relative position within the study area; [[ch:m4-hotspots]] owns that explanation. Descriptors remain in their original interpretable units. [src: methodology/modules/M3_characterisation.md §13] [src: methodology/modules/M4_hotspots.md §9]

### 4. Summarise the candidate areas

Describe the opportunity space and its geographic subdivisions using quantities appropriate to each dataset: totals, shares or distributions with stated denominators. Examples include population, production value, dominant farming systems and the distribution of environmental concerns. Report missing-data coverage and use the family's valid footprint unit. [src: methodology/modules/M3_characterisation.md §6] [src: method:handbook/implement-a-scan.md §3. Build the scoping brief]

A count of residents within a candidate zone is not a count of beneficiaries. It describes spatial overlap; whether those residents benefit depends on access, design, participation and where the intervention's effects occur. M5 addresses effect interpretation and M6 the local assessment. [src: methodology/modules/M3_characterisation.md §4] [src: methodology/modules/M5_scorecard.md §6]

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

[[table:T5]] identifies themes and roles; [[table:T1]] and [[table:BIND]] describe data and contextual choices; [[table:VONT]] describes units, resolution and sensitivity; [[table:T7]] defines summary units. The application records transformations, indicator selection, unavailable data and overlap checks with [[table:T2]].
