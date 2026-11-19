---
title: Evidence records and source appraisal
slug: evidence-principles
summary: Understand what the evidence records represent, what each source can establish, and how claims support different analytical tables.
sources:
  - schema/spec.md
  - schema/structure/columns.json
  - methodology/T4_generation_method.md
  - methodology/T3_T6_generation_method.md
  - methodology/search_protocol.md
  - methodology/access_policy.md
  - method:data-model/evidence-classification.json
  - evidence:workflows/extraction/classification.md
---

## From a source to an analytical decision

The evidence system supports several different questions: where a practice can fit, how it responds to hazards, what outcomes it delivers and what implementation might cost. A source can contribute to more than one question, but its claims need separate interpretation for each. A rainfall range at an existing project, a measured yield change and a reported establishment cost are not interchangeable evidence of suitability. [src: schema/spec.md §Evidence & configuration layer]

The common principle is to keep the source, the extracted claim and the analytical decision separate. Extraction records what a source states, with its context and locator. Review checks that interpretation. Synthesis decides what eligible claims support for a particular table and scope. A verified quotation does not, by itself, establish a transferable threshold, a causal effect or a locally applicable cost. [src: methodology/T4_generation_method.md §0] [src: methodology/T3_T6_generation_method.md §3]

This chapter explains those shared foundations. The next four chapters follow the work in order: [[ch:discovery]], [[ch:acquisition]], [[ch:extraction]] and [[ch:review-and-quality]]. After review, [[ch:compiling-evidence]] explains compatibility, dependence and weighting across tables. The three specialist chapters then give the actual suitability, effect and economic compilation rules.

## What each record represents

The provenance chain for a literature-supported analytical value is:

```formula
analytical row → evidence identifier → source identifier → locator and source quotation
```

The analytical row also needs the synthesis policy and recorded decisions that transformed the claims. Provenance answers where a value came from; reproducing it additionally requires the same evidence, policy, context and compiler version. [src: methodology/T4_generation_method.md §Synthesis decision record] [src: methodology/T3_T6_generation_method.md §7]

| Record | What one record represents | What it does not establish |
|---|---|---|
| [[table:SRC]] Source Register | A publication, report, website, tool or codebase, with identity, access information, context and source-level credibility | An independent experiment, or equal quality for all claims within the work |
| [[table:EV]] Evidence Register | An atomic claim, linked to its source, variable, practice/family, quotation, locator, context and review state | A second independent vote whenever another row is extracted |
| [[table:SRCH]] Search Register | A search within a declared practice, family, table and process, including queries, criteria and counts | Evidence sufficiency, or a complete source-to-search membership map merely because counts exist |
| [[table:TOOL]] Tools and Methods Registry | Metadata about a tool's variables, algorithms, configuration, version and linked evidence | Scientific validation of the tool's defaults |
| [[table:VONT]], [[table:FAM]], [[table:XW]] | Variable definitions, suitability families and routes from measured outcomes to table targets | Proof that similarly named quantities or practices are interchangeable |
| [[table:BIND]] Dataset bindings | The spatial dataset representing a variable for a specified context | Validation of the scientific rule applied to that map |

[src: schema/spec.md §Evidence & configuration layer] [src: methodology/search_protocol.md]

Source fields describe the work as a whole: citation, source kind, method, venue, credibility tier, geography and access. Evidence fields describe the particular statement: meaning, scope, relationship, conditions, quotation and review history. A high-tier review can repeat an untested threshold; a local report can contain a carefully measured result. Source-level assessment therefore cannot replace claim-level appraisal. The field dictionary gives the complete definitions in [[table:SRC]] and [[table:EV]]; [[ch:extraction]] explains how to populate them. [src: schema/spec.md §SRC] [src: schema/spec.md §EV]

CSV records are authoritative and generated JSON is a derived product. Column definitions are versioned and checked; a documented concept is not evidence that a dedicated column exists or is fully populated. Dependence information, for example, uses existing lineage and context where their semantics fit, supplemented by the synthesis record rather than invented fields. [src: schema/structure/columns.json] [src: method:data-model/evidence-classification.json]

## Which question and table a claim can support

The analytical destination follows the meaning of the claim, not the source's title or format. The same publication may contain several claims with different destinations. [src: methodology/T3_T6_generation_method.md §3] [src: schema/spec.md §EV]

| Question | Analytical destination | Required distinction |
|---|---|---|
| Where can the practice establish or integrate with its host system? | [[table:T4]] suitability | An implementation constraint or response differs from a descriptor of where a study happened |
| How does the practice affect a hazard, or how does a hazard threaten the investment? | [[table:T3]] hazard response and asset threat | Benefit to livelihoods and damage to the practice are separate directions of causation |
| What changes in an outcome relevant to a priority? | [[table:T6]] scorecard effects | The measured outcome, comparator and beneficiary must support the route to the priority; a proxy remains labelled |
| What does implementation cost, or what economic outcome is reported? | [[table:T6E]] economic profiles | A comparable cost indicator needs its denominator and context; an ordinal rating is not a monetary value |
| What enables or obstructs implementation? | Operational-risk and implementation guidance in M2b and M6 | Investment-addressable access, labour or tenure conditions do not become permanent biophysical exclusions |

[src: schema/spec.md §T3] [src: schema/spec.md §T4] [src: schema/spec.md §T6] [src: methodology/modules/M2b_project_risk.md]

Other tables contribute configuration rather than using the same claim-pooling procedure. [[table:T0]] records the practice and scope. [[table:T1]] identifies spatial datasets; [[table:T2]] configures climate hazards and their interpretation. [[table:T5]] defines priorities and descriptors, while [[table:T7]] defines geographic contexts. Their choices still need provenance and justification, but source counts cannot decide a stakeholder preference, validate a map or define a geographic classification. The dataset-selection method is in [[ch:farming-systems-and-data]], the hazard method in [[ch:m2-climate-risk]], and priority construction in [[ch:m3-characterisation]] and [[ch:m4-hotspots]]. [src: schema/spec.md]

## Scientific basis, extraction format and confidence

Several distinct judgements travel with an evidence unit. Keep them separate when reading or reviewing it.

| Aspect | Question it answers | Interpretation |
|---|---|---|
| Knowledge basis | How was the claim established? | Measured, modelled, cited from another work, expert assertion, or unresolved |
| Extraction format | Where was the claim read? | Prose, table, figure, code, or unknown; none is a credibility rank |
| Evidence form | What kind of contribution is recorded? | A relationship, variable-importance result, scoping candidate or expert statement |
| Claim scope | What does the claim concern? | Practice, species or crop, with the relevant taxon retained |
| Extraction confidence | How faithfully was it transcribed? | Confidence in extraction, not in validity, transferability or the final map |
| Review state | What has been checked or held? | Approval applies to a declared interpretation; it does not automatically approve numerical calibration or local application |

[src: schema/spec.md §EV] [src: method:data-model/evidence-classification.json]

The classification contract separates `knowledge_basis` from `extraction_format`. A table can contain measured results or expert-selected criteria; a figure can show observations or a simulation. Unknown basis remains unknown. The pinned historical evidence edition uses a mixed `claim_basis` field, retained to reproduce its analytical outputs. The new classification does not retroactively reappraise those claims or change their weights. [[ch:extraction]] explains the intake and migration boundary. [src: method:data-model/evidence-classification.json] [src: evidence:workflows/extraction/classification.md]

## What different sources can establish

Source screening assesses relevance and credibility using the rubric in [[ch:discovery]]. The table below explains how that assessment affects interpretation, rather than adding another universal ranking of source types.

| Source or study type | Useful contribution | Limitation to carry into synthesis |
|---|---|---|
| Field experiment or monitored study | Performance under specified management and conditions | Sites, comparator, duration and sampling design constrain causal interpretation and transfer; an effect is not automatically a suitability limit |
| Observational or adoption study | Existing use, associations, barriers and dis-adoption | Confounding and access affect observed distribution; non-adoption does not prove biophysical unsuitability |
| Systematic review or meta-analysis | Consistency, heterogeneity and coverage across studies | Its question may differ from the target table; overlapping primary studies cannot be counted again as independent support |
| Spatial model or land-evaluation study | Explicit criteria, native classes, assumptions and model weights | Classes may be borrowed or judgement-based; validating a map does not independently validate every threshold |
| Institutional manual or project report | Conditional guidance, implementation experience, costs and failures | Recommendations, targets and measured results must be distinguished; organisational authority does not supply a missing comparator |
| Practice-database account | Detailed descriptions, observed settings and practitioner assessments | Measurement and judgement may coexist; interpret each field and claim separately |
| Tool or codebase | Reproducible rules, defaults and classifications | A runnable default can be a design choice; trace cited origins and pin the code version |

These distinctions follow the source screening and extraction rules. They apply across suitability, effect and economic evidence. A claim should retain its strongest defensible use without being promoted to a stronger claim merely because another table needs a number. [src: methodology/search_protocol.md] [src: methodology/T4_generation_method.md §3] [src: methodology/T3_T6_generation_method.md §3]

### WOCAT accounts: read the field before using the value

The World Overview of Conservation Approaches and Technologies (WOCAT) distinguishes Technologies, the land-management practices, from Approaches, the means of implementing them. Its documentation process includes field collection, consultation and review. Those processes make accounts valuable sources of implementation knowledge; they do not make every reported value a controlled measurement. [WOCAT documentation guidance](https://wocat.net/en/database/how-to-document-an-slm-practice/)

Environmental descriptors and reported impacts answer different questions. Rainfall, slope and soil at a documented site describe its setting. Impact ratings and perceived climate sensitivity require interpretation on their own scales and with their reported basis. [FAO questionnaire description](https://www.fao.org/land-water/land/land-governance-and-planning/land-resources-planning-toolbox/detail/wocat-core-questionnaire-on-slm-technologies-%28wocat_qt%29/en)

| Account content | Appropriate use | Unsupported promotion |
|---|---|---|
| Rainfall or slope at the documented site | Occurrence and transfer context | A universal T4 lower or upper limit |
| Explicit generalising siting requirement | Candidate T4 condition, subject to review | Permission to treat every site descriptor as a rule |
| Practitioner-rated improvement | Ordinal effect evidence for an eligible T3/T6 target | A measured percentage change or causal effect size |
| Sensitivity to drought or flooding | Asset-vulnerability evidence where wording supports it | Evidence that the practice reduces livelihood exposure to that hazard |
| Establishment or maintenance cost | T6E evidence with its reported unit, scope and period | A locally applicable cost estimate or cost-benefit ratio |
| Labour, access or implementation support | Operational risk and M6 guidance | A permanent biophysical exclusion |

These are interpretation rules, not a presumption that all WOCAT accounts have the same quality. Check each account for bundled measures, attribution, measurement methods, transfer limits and selective reporting. Linked Technology, Approach and project records may describe one intervention; multiple URLs do not establish independent replication. Acquisition of questionnaire fields is covered in [[ch:acquisition]], and their claim encodings in [[ch:extraction]].

For example, a practice documented at 600–900 mm annual rainfall provides an observed setting. It does not establish failure below 600 mm or above 900 mm. A separate, explicit failure statement would need its own quotation and basis. Likewise, a favourable ordinal impact rating cannot supply a missing percentage yield gain.

### Expert judgement reported in literature

Expert opinion in this workflow comes from existing publications and documented accounts. It does not involve new interviews, panels or elicitation. Register the publication as the source and extract the actual passage; do not invent a transcript, participants or uncertainty bounds. [src: method:data-model/evidence-classification.json]

Appraise what the publication reports: whose judgement it is, relevant expertise, how criteria were chosen, supporting rationale, practice and geographic scope, disagreement, uncertainty and any cited origin. An explicitly documented panel method and an unexplained author-selected threshold warrant different interpretations. Missing methodological detail remains missing; an unexplained number is not assigned a basis by guesswork.

Classify claims individually. A paper can contain empirical measurements alongside expert-selected classes. Publication in a journal does not convert the latter into empirical calibration. A panel average is not automatically a statistical confidence interval, and repeated publications of the same panel judgement do not add independent support. AI interpretation is a synthesis proposal, not an extra expert source. Guidance on expert elicitation can help appraise a published method without making direct elicitation part of this workflow. [EFSA guidance](https://www.efsa.europa.eu/en/efsajournal/pub/3734)

## Provenance and the limits of verification

An eligible claim needs an acquired artefact, verified identity, a reproducible locator and its source wording. A bare URL, search snippet or remembered quotation is insufficient. The provenance checks establish that the passage occurs in the cited artefact and, for PDF evidence, on the cited page. Numerical and scope checks then assess the encoding. Acquisition details belong in [[ch:acquisition]] and extraction checks in [[ch:extraction]]. [src: methodology/search_protocol.md] [src: src/nbs_ruralscan/schema_tools/validate_sources.py]

Evidence records remain recoverable. A dropped claim is excluded from synthesis rather than deleted, and historical ruleset stamps are preserved. Generated analytical rows are rebuilt from the authorised evidence and configuration, rather than silently edited to obtain a preferred result. Review and reopening procedures are in [[ch:review-and-quality]]. [src: evidence:README.md]

A source the team cannot acquire, or a format without an agreed intake adapter and locator semantics, remains on hold. Dataset intake as a source of quoted claims is distinct from selecting a spatial dataset for T1/BIND. The former requires a suitable intake method; the latter follows the spatial data-selection workflow. [src: methodology/search_protocol.md §Datasets (.csv / .xlsx / R)]

## Assumptions and limits

Provenance establishes traceability, not truth. Source validity, independence, applicability and the adequacy of the synthesis still need appraisal. Documented successes can overrepresent favourable conditions, and evidence gaps can reflect search coverage rather than absence of an effect. The source and claim counts shown in the evidence base measure records and coverage, not independent replication or certainty. [src: methodology/T4_generation_method.md §6.1 Publication bias & uncertainty]

These records support scoping. A local feasibility assessment must still establish site conditions, dataset fitness, implementation design and costs. Shared evidence principles do not imply one pooling algorithm for every table; [[ch:compiling-evidence]] explains the differences.

## Where this is configured

Source identity and context sit in [[table:SRC]]; claims and review state in [[table:EV]]; searches in [[table:SRCH]]; tool metadata in [[table:TOOL]]. [[table:VONT]], [[table:FAM]], [[table:XW]] and [[table:BIND]] define meanings, families, routes and spatial representation. The classification contract defines separate basis and format fields. Full field definitions belong in the Data model section; acquisition, extraction, review and synthesis procedures follow in this section.
