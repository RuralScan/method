---
title: The method as a scoping walkthrough
slug: scoping-walkthrough
summary: Explore seven example stages and follow their links to the governing method.
sources:
  - docs/redesign/index.html
  - docs/redesign/help.html
  - docs/redesign/v1b-fixture.js
  - method:priority/README.md
  - docs/redesign/01-setup.html
  - methodology/modules/M0_setup.md
  - docs/redesign/02-practices.html
  - docs/redesign/03-opportunity.html
  - docs/redesign/04-risk.html
  - docs/redesign/05-hotspots.html
  - docs/redesign/06-comparison.html
  - docs/redesign/07-next.html
  - docs/redesign/00-config.html
  - method:handbook/implement-a-scan.md
---

## What the visual methodology is

The [visual methodology](https://ciat.github.io/nbs_ruralscan/redesign/index.html) is an interactive mock-up of seven stages, from defining an investment question to preparing a scoping brief. It illustrates how the method could be used; it does not run a spatial analysis or make investment recommendations. All displayed maps, counts, effects and costs are examples, not pilot results. [src: docs/redesign/index.html §Home] [src: docs/redesign/help.html §Are the maps and results real?]

Use it to explore the sequence and questions. Use the linked method chapters for scientific rules. Example controls and defaults are not approved analytical settings; the current classification and weighting contract governs M3/M4. Citations here identify the inspected version; the live mock-up may differ. [src: docs/redesign/v1b-fixture.js §header] [src: method:priority/README.md]

## Seven stages and the modules behind them

Table: Walkthrough stages and the analytical chapters that explain them.

| Stage | Question | Method |
|---|---|---|
| Setup | What decision, practice and place? | [[ch:m0-setup]] |
| Explore the practices | What could each practice do? | Practice definitions and [[ch:m5-scorecard]] |
| Opportunity space | Where could it fit, and what lies there? | [[ch:m1-suitability]], [[ch:m3-characterisation]], [[ch:m2-climate-risk]] |
| Project risk | What could damage or obstruct the investment? | [[ch:m2b-project-risk]] |
| Priority hotspots | Where do selected concerns concentrate? | [[ch:m4-hotspots]] |
| NbS comparison | Which options merit closer investigation? | [[ch:m5-scorecard]], [[ch:cost-profiles]] |
| Next steps | What must local assessment establish? | [[ch:m6-handoff]] |

[src: docs/redesign/index.html §H.3]

The stages organise a user's journey, not a second set of analytical modules. For example, Opportunity space brings suitability, landscape conditions and response evidence together while keeping their meanings distinct. [src: docs/redesign/index.html §H.6]

## Setup

Choose the investment objective, practice, area and climate scenario. Inspect the practice's footprint type and the data it would need. M0 records these choices and checks readiness; choosing a country or objective does not validate a response or calculate a map. [src: docs/redesign/01-setup.html §1.1.1] [src: methodology/modules/M0_setup.md §2]

[Open Setup](https://ciat.github.io/nbs_ruralscan/redesign/01-setup.html). Scientific guidance: [[ch:m0-setup]] and [[ch:farming-systems-and-data]].

## Explore the practices

Read the practice definition, variants, limiting conditions, evidence-supported effects and indicative costs. Keep effect direction, magnitude and confidence separate. A gap is not proof of no effect. The mock-up's worked practices and fictional counts illustrate the display; the practice pages and evidence records hold the documented content. [src: docs/redesign/02-practices.html §2.1] [src: docs/redesign/02-practices.html §2.3]

[Open Explore the practices](https://ciat.github.io/nbs_ruralscan/redesign/02-practices.html). Scientific guidance: [[table:FAM]], [[ch:m5-scorecard]] and [[ch:cost-profiles]].

## Opportunity space

Inspect candidate areas, exclusions and unknown areas separately. Then read the people, production, environmental concerns and livelihood hazards within that space. These describe local conditions, not benefits caused by an intervention. A coarse grid cell is not a farm, and a placement zone for a linear practice is not planted hectares. [src: docs/redesign/03-opportunity.html §3.1] [src: docs/redesign/03-opportunity.html §3.2]

The mock-up contains illustrative class breaks and earlier display choices. Do not copy them into an analysis: use accepted suitability responses and the classification rules explained in [[ch:m3-characterisation]]. [src: docs/redesign/v1b-fixture.js §breaks] [src: method:priority/README.md]

[Open Opportunity space](https://ciat.github.io/nbs_ruralscan/redesign/03-opportunity.html). Scientific guidance: [[ch:m1-suitability]], [[ch:m3-characterisation]] and [[ch:m2-climate-risk]].

## Project risk

Read hazard exposure beside evidence of vulnerability, then inspect access, tenure, finance and other delivery barriers. The example asks whether flagged areas should remain on the shortlist for further assessment. A flag is not a loss rate or proof of safety. M2b stays separate from the priority score. [src: docs/redesign/04-risk.html §4.1] [src: docs/redesign/04-risk.html §4.3] [src: docs/redesign/04-risk.html §4.4]

[Open Project risk](https://ciat.github.io/nbs_ruralscan/redesign/04-risk.html). Scientific guidance: [[ch:m2b-project-risk]].

## Priority hotspots

Choose which concerns matter and inspect how the ranking responds to their weights. Within the opportunity space, the current method classifies concerns, checks overlap, then combines them using explicit user weights. Show the contributors to the result; residents in a hotspot are not automatically beneficiaries. Mock-up presets do not supply scientific weights. [src: docs/redesign/05-hotspots.html §5.1] [src: docs/redesign/05-hotspots.html §5.2] [src: method:priority/README.md]

[Open Priority hotspots](https://ciat.github.io/nbs_ruralscan/redesign/05-hotspots.html). Scientific guidance: [[ch:m3-characterisation]] and [[ch:m4-hotspots]].

## NbS comparison

Compare practices on the same concerns while preserving differences in evidence, context and footprint units. Riparian kilometres are not interchangeable with planted hectares. Overlapping candidate areas do not prove that practices are compatible, and illustrative budget calculations are not a cost-benefit analysis. [src: docs/redesign/06-comparison.html §6.1] [src: docs/redesign/06-comparison.html §6.3]

[Open NbS comparison](https://ciat.github.io/nbs_ruralscan/redesign/06-comparison.html). Scientific guidance: [[ch:m5-scorecard]] and [[ch:cost-profiles]].

## Next steps

Read the shortlist with its assumptions and unresolved questions. Identify what local work must establish about land, tenure, participation, hazards, design, costs and effects. The example brief illustrates this hand-off; it is not a finding that any example site is feasible. [src: docs/redesign/07-next.html §7.2] [src: docs/redesign/07-next.html §7.3]

[Open Next steps](https://ciat.github.io/nbs_ruralscan/redesign/07-next.html). Scientific guidance: [[ch:m6-handoff]].

## Technical configuration

The optional configuration page lets an analyst inspect example datasets, responses, exclusions, correlations and classification settings. Changes affect previews, not an accepted recipe or live scientific analysis. In particular, earlier five-class controls and correlation defaults are not the current priority contract. [src: docs/redesign/00-config.html §C.2] [src: docs/redesign/00-config.html §C.4] [src: docs/redesign/00-config.html §C.5] [src: method:priority/README.md]

[Open Technical configuration](https://ciat.github.io/nbs_ruralscan/redesign/00-config.html). Scientific guidance: [[ch:farming-systems-and-data]], [[ch:suitability-synthesis]] and [[ch:m3-characterisation]].

## Assumptions and limits

The mock-up demonstrates selected practices and questions with synthetic data. It does not establish that any module has been implemented, calibrated or validated in a country. Current method contracts govern scientific use; actual application reports identify completed analyses and their evidence. Feasibility still requires local assessment. [src: docs/redesign/v1b-fixture.js §header] [src: method:handbook/implement-a-scan.md §3. Build the scoping brief]

## Where this is configured

The mock-up uses its own display files rather than live analytical tables. In an application, [[table:T0]], [[table:FAM]] and [[table:T7]] identify practices and contexts; [[table:T1]] and [[table:BIND]] identify data; [[table:T4]] holds suitability; [[table:T2]] and [[table:T5]] identify concerns; and [[table:T3]], [[table:T6]] and [[table:T6E]] provide response and cost evidence. [src: docs/redesign/v1b-fixture.js §header]
