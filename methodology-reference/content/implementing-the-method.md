---
title: Applying and reporting a country scan
slug: implementing-the-method
summary: Prepare and interpret a country scoping brief with traceable inputs, clear output meanings and explicit limits.
sources:
  - method:handbook/implement-a-scan.md
  - methodology/T4_developer_contract.md
  - runtime:docs/DESIGN.md
  - methodology/modules/M0_setup.md
  - methodology/T4_generation_method.md
  - methodology/modules/M3_characterisation.md
  - methodology/modules/M5_scorecard.md
---

## From method to a country application

A country application turns the method into a scoping brief for a defined decision and area. It records the inputs used, the analytical choices made, the resulting shortlist and the checks that remain for local assessment. This chapter describes what the brief needs to contain. Software setup and developer guidance belong in the [runtime repository](https://github.com/RuralScan/runtime) and the linked implementation handbook. [src: method:handbook/implement-a-scan.md §3. Build the scoping brief]

The methodology is a draft analytical specification. Its published evidence edition is not a claim that every module has been implemented or validated in a country. A particular application's report must distinguish completed analyses from exploratory results and omitted stages, using the release and run records for that application. [[ch:editions]] identifies the evidence snapshots; [[ch:reproduce]] explains their checks. [src: methodology/T4_developer_contract.md §Acceptance and limitations] [src: runtime:docs/DESIGN.md §Run configuration]

## Define and record the application

State the decision question, selected practice and suitability family, area boundary and its source, analysis grid, baseline period and any future scenario. Record the evidence edition, scoring package and software revision separately: matching a package checksum establishes which files were used, not that the method has been validated locally. [src: methodology/modules/M0_setup.md §6] [src: methodology/T4_developer_contract.md §Verify a delivered package]

For each input, record the dataset version, units, spatial support, processing and missing-data coverage. Explain substitutions for preferred local datasets. For each response, record why its context and measurement basis are applicable to the target. [[ch:farming-systems-and-data]] owns data-selection guidance; [[ch:m1-suitability]] owns interpretation of the suitability result. [src: methodology/T4_developer_contract.md §Dataset preparation proposals and source compatibility] [src: methodology/T4_developer_contract.md §Target country and evidence country are different filters]

## Present a decision-ready scoping brief

Table: Minimum information accompanying a scoping result.

| Part of the brief | What the reader needs |
|---|---|
| Scope and provenance | Decision question, boundary, family, dates, grid and versions. |
| Opportunity space | Meaning of the score or classes; host requirements and exclusions applied; unknown areas and coverage; footprint in the family's valid reporting unit. |
| Needs and priorities | Raw indicators beside transformed values, selected priorities, weights, reference frame and the factors driving each shortlisted area's rank. |
| Investment risk | Hazard threats and operational barriers shown separately from livelihood need. |
| Benefits and costs | Evidence-supported effects, confidence, transfer conditions and indicative economic denominators. |
| Sensitivity | Which plausible changes in inputs or settings alter the shortlist. |
| Next steps | Site checks, consultation, safeguards and feasibility questions linked to each promising area. |

[src: method:handbook/implement-a-scan.md §3. Build the scoping brief]

Every reported number needs a unit, denominator and coverage statement. A population count inside candidate areas is not a beneficiary estimate; a suitable zone for a linear intervention is not its planted area; an ordinal benefit rating is not a predicted percentage improvement. These distinctions belong beside the result, not only in technical appendices. [src: methodology/T4_generation_method.md §2.4 Spatial product type & the resolution trap] [src: methodology/modules/M3_characterisation.md §4] [src: methodology/modules/M5_scorecard.md §6]

## Check that conclusions match the analysis

Keep **scored**, **excluded** and **unknown** areas distinct. State which required gates and masks were applied; an omitted legal or host-system check cannot be read as evidence of eligibility. A held numerical calibration supplies no suitability score, even if its underlying quotation has passed review. [src: methodology/T4_developer_contract.md §Planted host and exclusion contracts] [src: methodology/T4_developer_contract.md §Reconciled implementation readiness]

Describe a partial result by the dimensions it covers. A terrain-and-soil index, for example, supports comparison of those conditions; it does not establish complete agroforestry suitability or plantable hectares. Likewise, synthetic examples demonstrate software behaviour and must not be reported as findings about a real place. [src: method:handbook/implement-a-scan.md §2. Run and interpret the first pass]

Keep the run configuration, input and output identifiers, map legends and decision record together. Revising a dataset or analytical rule creates a new recorded application; retain the earlier version so differences can be explained. [src: runtime:docs/DESIGN.md §Run configuration] [src: runtime:docs/DESIGN.md §Updating from CIAT]

## Assumptions and limits

Software checks establish reproducibility and conformance to recorded rules. They do not establish the local validity of a dataset, response function or legal mask. Field assessment and stakeholder review remain necessary before a shortlist informs site design or investment commitment. [src: methodology/T4_developer_contract.md §Verify a delivered package]

The hand-off should state the uncertainties that could change the decision and the next assessment needed to resolve each. [[ch:m6-handoff]] describes that step. Engineering progress and open development tasks are maintained with the software; they are not additional analytical findings.

## Where this is configured

The application uses the tables described in each module chapter and records its choices in the run configuration and output manifest. [[table:T4_RUN]] records suitability execution settings; [[table:T1]] and [[table:BIND]] record dataset choices. The [runtime repository](https://github.com/RuralScan/runtime) holds software instructions and release-specific implementation details.
