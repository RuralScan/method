---
title: Evidence registry and source limitations for T4
slug: evidence-registry
summary: Interpret source records, atomic claims, knowledge basis and extraction format without confusing provenance with scientific strength.
sources:
  - method:data-model/evidence-classification.json
  - methodology/T4_generation_method.md
  - schema/spec.md
---

T4 defines how spatial variables contribute to the suitability of a Nature-based Solution (NbS) family. An AI skill can help interpret the evidence and propose these rules, but the defensible product is a reviewed, reproducible chain from each rule to its sources, claims, context and synthesis decision. A correctly quoted publication does not, by itself, validate a numerical rule or its transfer to a new landscape.

Much of this system already exists. Its explanation is distributed across the [T4 generation method](https://github.com/CIAT/nbs_ruralscan/blob/9d84fd9900b9c913804a9f94eb6f9779f2734994/methodology/T4_generation_method.md), [schema specification](https://github.com/CIAT/nbs_ruralscan/blob/9d84fd9900b9c913804a9f94eb6f9779f2734994/schema/spec.md), [extraction skill](https://github.com/CIAT/nbs_ruralscan/blob/9d84fd9900b9c913804a9f94eb6f9779f2734994/.agents/skills/source-command-extract-evidence/SKILL.md), [T4 review contract](https://github.com/CIAT/nbs_ruralscan/blob/9d84fd9900b9c913804a9f94eb6f9779f2734994/.agents/skills/extraction_contracts/T4_review_contract.md) and [synthesis skill](https://github.com/CIAT/nbs_ruralscan/blob/9d84fd9900b9c913804a9f94eb6f9779f2734994/.agents/skills/source-command-t4-synthesise/SKILL.md). This chapter brings those pieces together and distinguishes the current classification extension from historical compiler behaviour. It describes the local repository at revision `9d84fd9900b9c913804a9f94eb6f9779f2734994`; the November classification extension is defined in the current method contract; historical analytical policies remain separately versioned.

## 1. Sources, claims and rules are different records

One source can contain several claims with different strengths and uses. A paper may contain measured trial results, borrowed thresholds and an expert-chosen weighting scheme. Giving the publication one credibility tier does not make every claim equally reliable.

```text
Search and screening → Source → Atomic claims → Review → Synthesis decision → T4 → Release
                                  ↑                            ↑
                         Family and variable definitions    Dataset binding
```

The diagram shows the workflow; it does not imply a direct foreign-key link from every search record to every source. Explicit screened-source membership is also needed for defensible search denominators.

| Record | Unit and purpose | Important distinction |
|---|---|---|
| **SRC — Source Register** | One publication, report, website, tool or codebase; identity, access, context and source-level credibility. | A source record is not an independent experiment or an approved rule. |
| **EV — Evidence Register** | One atomic claim linked to its source, variable and family, with quotation, locator, context and review state. | Several claims from one source do not create several independent votes. |
| **VONT — Variable Ontology** | Canonical variable meaning, aliases, units and spatial constraints. | Similar names do not establish equivalent quantities: soil organic matter and soil organic carbon need a justified conversion. |
| **FAM — Suitability families** | Subpractices grouped by their dominant limiting factor; also defines spatial product type. | A broad agroforestry claim is not automatically applicable to every family. |
| **BIND — Dataset bindings** | Links a variable to a spatial dataset for a particular context, with more-specific overrides. | Evidence about a variable and the map used to represent it have separate uncertainties. |
| **SRCH — Search Register** | Search scope, process, terms, eligibility, counts, date and ruleset version. | Search completion is not evidence sufficiency; absence of claims is not proof that searching never happened. |
| **T4 and authored inputs** | Reviewed response rules, masks, settings, holds and context-specific decisions compiled into recipe mappings. | Evidence approval and approval to execute a numerical rule are separate decisions. |

CSV registers are authoritative; JSON is generated. T4 design settings and holds have [declared authoring inputs](https://github.com/CIAT/nbs_ruralscan/blob/9d84fd9900b9c913804a9f94eb6f9779f2734994/schema/recipe_inputs/t4/README.md), and accepted tables travel together in a [recipe release](https://github.com/CIAT/nbs_ruralscan/blob/9d84fd9900b9c913804a9f94eb6f9779f2734994/docs/RECIPE_RELEASES.md). Evidence changes use the validated intake/review workflow, rather than direct row edits by an AI.

## 2. What the registries contain

### Source metadata

| Field group | Current fields and interpretation |
|---|---|
| Identity | `source_id`, `citation`, `doi`. A DOI is optional; source identity must still be verified against the acquired artifact. Verification state also uses the intake/metadata-verification machinery, not an assumed CSV column. |
| Source classification | `source_kind`: `paper`, `grey_lit`, `website`, `tool`, `codebase`. `venue_type`: journal, institutional report, preprint or grey. `method_type` describes the method used. These answer different questions. |
| Discovery channel | `source_category`: `stock`, `updated_lit`, `grey`, `tool`. This records the discovery category, not a complete assessment of study design or independence. |
| Credibility | `benchmark_tier`: `high`, `medium`, `low`, `external`. The method defines `external` as an unscreened citation pointer, not substantive synthesis support. |
| Context | `study_country`, `region`, `coords`, `aez`, `farming_system`, `study_income_group`, `spatial_scale`, `analysis_resolution_m`, `nbs_ids`. |
| Access and reproducibility | `url`, `library_path`, `artifact_sha1`, `retrieved_at`, `access_status`, `license`. A current web page and the frozen artifact used for extraction can differ. |
| Processing | `vars_extracted`, `extraction_status`, `extraction_date`, `extraction_run_id`, `extractor`. Extraction status says what work occurred, not whether every resulting rule is scientifically approved. |

The [column manifest](https://github.com/CIAT/nbs_ruralscan/blob/9d84fd9900b9c913804a9f94eb6f9779f2734994/schema/structure/columns.json) additionally permits optional fields such as `is_seminal` and `extraction_status_by_family`; these are absent from the inspected SRC CSV header. They should not be advertised as comprehensively populated. The source specification also contains older field descriptions; the manifest, actual headers, validators and current decisions must be reconciled when publishing a definitive data dictionary.

### Atomic claim metadata

| Field group | EV fields and interpretation |
|---|---|
| Identity and target | `evidence_id`, `source_id`, `nbs_id`, `suitability_family_id`, `variable`. |
| Four classifications | `use_role`, `evidence_type`, `claim_basis`, `claim_scope`; detailed below. |
| Source statement | `quote`; `locator_type` and either `page` or `locator`; `commit_sha` for code-line provenance. Supported locators are `page`, `section`, `char_span`, `file_line`. |
| Extracted content | `relationship` holds structured values, direction, classes or retained source profiles; `context` holds the conditions needed to interpret them. These are structured objects, not permission to infer missing values. |
| Meaning and attribution | `raw_name`, `observed_dataset`, `taxon`, `attribution`, `lineage_of`. Model-use lineage can be recorded separately in `context.model_use`; borrowed response thresholds need not share the origin of a paper's model weights. |
| Supporting explanation | `justification_quote` and `justification_page` explain a source's threshold rationale; `selection_justification` and its page explain why it selected the variable. |
| Quality and history | `extraction_confidence`, `reviewer_ok`, `review_state`, `ruleset_version`. Dropped evidence remains recoverable; it is excluded from synthesis rather than deleted. |

`extraction_confidence=high` means high confidence in the transcription. It does **not** mean strong empirical evidence, global transferability or low uncertainty in the final suitability map. Similarly, `reviewer_ok` retains the claim within its reviewed scope; calibration and dataset-binding holds can remain.

## 3. Four separate ways to classify evidence

### Analytical destination through use_role

| Value | Question answered | Destination |
|---|---|---|
| `structural_suitability` | Where can this practice establish or integrate with its host system? | T4, including relevant hard exclusions. |
| `nbs_effect` | How does the practice change an outcome? | T3/T6/T6E through the outcome crosswalk. |
| `asset_vulnerability` | How does a hazard damage the practice itself? | T3 asset threat and M2b Stream A. |
| `operational_risk` | Which enabling conditions affect implementation? | M2b Stream B and Module 6; outside core T4 suitability. |
| `dataset`, `climate_risk`, `priority_need` | Data or other analytical roles retained in the vocabulary. | Not substitutes for an authorised T4/effect claim. Dataset intake remains subject to its adapter restrictions. |

Road access, tenure, finance, extension and labour generally belong in operational risk. A measured yield gain belongs in effects. Neither becomes a structural suitability threshold merely because the study reports its location.

### Evidence form through evidence_type

| Value | What it captures | Limit |
|---|---|---|
| `literature_relationship` | A source-reported relationship or criterion. | May be empirical, modelled, borrowed or asserted; publication alone does not establish its basis. |
| `ml_importance` | Machine-learning importance of a predictor. | Importance does not provide a suitability direction, causal effect or response curve. |
| `scoping_candidate` | A candidate variable or selection signal. | Cannot supply missing curve parameters. |
| `expert` | An attributable expert statement; current task covers statements reported in literature. | Assess the publication's reported basis, context and uncertainty; do not infer an elicitation process or add AI-generated opinion. |

Only literature/expert forms can carry shape parameters under the current evidence validator. That permission is necessary, not sufficient, for executable calibration.

### Basis through claim_basis

Current values are `primary_measured`, `modelled`, `cited_secondary`, `expert_assertion`, `table`, `figure_read`. The first four concern how knowledge was obtained. The last two concern how it was presented or extracted. **A table can report an expert judgement; a figure can display a controlled experiment.**

**Accepted separation, 19 November 2026:** separate epistemic basis from extraction format. The first describes how the claim was established; the second describes where/how it was extracted. Presentation format must not confer scientific strength. The new fields are `knowledge_basis` and `extraction_format`; their controlled vocabulary and deterministic migration are specified in the [classification contract](https://github.com/RuralScan/method/blob/main/data-model/evidence-classification.json). Legacy `claim_basis` remains for the pinned compiler. Historical weighting changes require a separate release. The additive migration preserves existing fields and historical evidence.

For migration, inspect the underlying source: a table of expert-selected classes remains expert judgement extracted from a table. A table of measured responses remains measurement extracted from a table. Where the basis is undocumented, retain an unresolved classification rather than infer measurement from layout. Preserve original tags and the correction trail.

### Applicability through claim_scope

`practice_technology`, `species_specific` and `crop_specific` separate a practice's requirements from those of a named organism. Species/crop claims retain `taxon` and remain available. Species-specific envelopes do not define practice-level T4. Crop admission follows the explicit [crop-scope policy](https://github.com/CIAT/nbs_ruralscan/blob/9d84fd9900b9c913804a9f94eb6f9779f2734994/schema/lookups/crop_scope_policy.csv), including authorised family exceptions. Rules for effect synthesis differ and must not be imported into T4.

## 4. What different sources can justify

Discovery priority and evidential strength are different. WOCAT and institutional syntheses can be excellent places to find relevant practices without automatically supplying the strongest numerical calibration.

| Source or study type | Useful contribution | Main limitation and review response |
|---|---|---|
| Systematic review or meta-analysis | Consistency, heterogeneity and coverage across studies. | May synthesise benefits rather than establishment; overlapping primary studies must not be counted again. Check the actual question and underlying studies. |
| Field experiment or monitored performance study | Establishment or performance under specified conditions. | Tested sites, species, duration and management limit transfer. An outcome response is not automatically an eligibility threshold. |
| Observational or adoption study | Existing use, local context, barriers and dis-adoption. | Confounding, reporting and access affect observed distribution. Non-adoption does not establish biophysical unsuitability. |
| Spatial model or land-evaluation paper | Explicit variable choices, native classes, assumptions and weights. | Classes may be borrowed, judgement-based or local ranks. Map validation does not independently validate every class boundary. |
| Institutional manual or implementation guide | Mechanisms, conditional siting guidance and recognised exclusions. | Recommendations may concern engineering dimensions or particular systems; distinguish guidance from measured limits. |
| Project monitoring, evaluation or completion report | Implementation experience, costs, failure and enabling conditions. | Attribution, missing comparators and selective reporting constrain causal claims. Keep project and population scope. |
| WOCAT Technology or Approach account | Concrete practice descriptions, observed settings, practitioner experience and implementation conditions. | Heterogeneous measurement and judgement; see the claim-specific treatment below. |
| Expert judgement reported in literature | Published practitioner assessments, panel judgements, author-selected criteria and conditional implementation guidance. | Assess expertise, elicitation method, rationale, shared information and uncertainty only to the extent reported. Undocumented details remain unknown. |
| Tool, codebase or decision-support model | Reproducible operational rules, defaults and classifications. | Implemented defaults may be design choices rather than validated ecological relationships. Pin code version and trace its cited origins. |
| Map or dataset | Spatial representation of a variable or observed host system. | Classification error, age, resolution and proxy meaning affect application independently of evidence quality. |

The existing six-axis credibility rubric examines evidence strength, transparency, authority/venue, contextual relevance, recency and seminality, with independence/conflict-of-interest considerations. A reputable institution does not remove a claim's design limitations. A local expert may provide better contextual knowledge than an unrelated experiment, while still providing a different kind of evidence. Record both strengths instead of forcing a universal ranking.

## 5. WOCAT site accounts require claim-level interpretation

The World Overview of Conservation Approaches and Technologies (WOCAT) distinguishes **Technologies**, the physical land-management practices, from **Approaches**, the means of implementing them. It recommends field collection and consultation with land users, and uses compiler, reviewer and publisher roles. These are valuable documentation and quality-control processes. [WOCAT documentation guidance](https://wocat.net/en/database/how-to-document-an-slm-practice/)

Its questionnaire covers site conditions separately from impacts. The Food and Agriculture Organization's description identifies rainfall, slopes and soils as environmental descriptors, and describes impact ratings and perceptions of climate sensitivity. [FAO questionnaire description](https://www.fao.org/land-water/land/land-governance-and-planning/land-resources-planning-toolbox/detail/wocat-core-questionnaire-on-slm-technologies-%28wocat_qt%29/en)

**Interpretation for Rural Scan:** database review does not establish that every value was measured, that impacts have a counterfactual, or that observed locations define the full feasible range. Review the specific entry and claim. Potential selection toward documented successes, sparse failure information, bundled measures and shared projects should be investigated rather than assumed absent or used to dismiss all accounts.

| Account content | Appropriate use | Unsupported inference |
|---|---|---|
| Rainfall or slope where a technology is used | Observed setting and transfer context. | Land outside that range is unsuitable. |
| Explicit generalising siting requirement, with rationale | Candidate T4 condition, subject to scope and calibration review. | Every statement in the same entry is a siting rule. |
| Practitioner-rated improvement | Contextual effect evidence with its actual basis and ordinal scale. | A measured percentage gain, causal effect or T4 membership score. |
| Climate tolerance or sensitivity | Asset-vulnerability evidence where the wording supports it. | The practice reduces livelihood exposure to that hazard by the same amount. |
| Labour, access, finance or implementation support | Operational risk and implementation guidance. | A permanent biophysical exclusion. |
| Linked Approach and Technology, or a project report describing the same intervention | Complementary details and documented lineage. | Independent replications merely because records or URLs differ. |

Hypothetical example: an account describes a practice used at 600–900 mm annual rainfall. Preserve that range as reported occurrence. A second, explicit statement that establishment fails below a stated moisture condition would be a separate claim needing its own basis, quote and context. The first range cannot supply that missing failure boundary.

There is already a relevant [project audit of WOCAT Approach 1971](https://github.com/CIAT/nbs_ruralscan/blob/9d84fd9900b9c913804a9f94eb6f9779f2734994/methodology/audits/roam_wocat_t4_20261102/README.md): it retained two pending qualitative T4 claims without fabricating a numeric curve. It also documented site-transfer limits, expert/field-visit basis and overlap with another account. This is a useful worked example of claim-specific admission.

## 6. Expert judgement extracted from literature

**Scope, 19 November 2026:** Rural Scan is deriving expert opinion from existing literature and published accounts for this work. It is not conducting interviews, recruiting panels or running a new elicitation exercise. The relevant methodological task is to identify and appraise expert judgement already embedded in a source.

For each claim, extract what the source actually reports: who supplied the judgement (authors, practitioners or a panel), their relevant expertise, how values were chosen, practice and geographic scope, supporting rationale, uncertainty, disagreement and any cited origin. An undocumented method stays undocumented. Distinguish a formal published elicitation from an unexplained author-selected threshold; do not classify an unexplained number as measured or expert-derived merely by guessing its origin.

Keep the published document/account as the source record, with its archived artifact and real page/section locator. Record an established judgement basis as `expert_assertion`; retain the evidence form according to the existing extraction contract rather than automatically converting every literature row to `evidence_type=expert`. Mixed papers can contain both empirical results and expert-selected classes, classified claim by claim. Do not invent interview records, transcripts, participants or confidence bounds.

Publication in a journal does not turn an expert assertion into empirical calibration. A panel consensus is not automatically one independent vote per participant, and repeated publication of the same panel's judgement does not add independent support. Preserve conditional ranges, contrary views and missing calibration. Statements about labour or machinery remain operational conditions where appropriate. AI interpretation is a synthesis proposal, not an additional expert source.

The existing [expert-opinion protocol](https://github.com/CIAT/nbs_ruralscan/blob/9d84fd9900b9c913804a9f94eb6f9779f2734994/methodology/expert_opinion_protocol.md) concerns direct elicitation and is outside this task's scope. Formal integration should give literature-derived expert judgement its own appraisal guidance rather than require a new consultation process. Existing elicitation guidance, such as [EFSA's](https://www.efsa.europa.eu/en/efsajournal/pub/3734), can inform appraisal of a publication's reported method; it does not imply that Rural Scan performs that method itself.

### Multiple records and shared author groups

Distinguish evidence rows, reporting publications and underlying study/data/judgement origins. Multiple table cells, class bands, figures or quotations can document one response profile; they do not multiply its synthesis weight. Companion papers, project reports and WOCAT entries may reuse the same sites, dataset, model or expert panel, including when the author lists differ.

Shared authorship is a dependency flag, not proof of duplication. The same group can produce genuinely new studies; different groups can reuse the same data. Record confirmed reuse, partially overlapping samples and unresolved dependencies separately. Preserve all useful claims and provenance, while controlling their influence at the appropriate origin level. The companion guide specifies the proposed handling and author-group sensitivity checks.

## 7. Classification implementation and remaining scientific review

The [classification contract](https://github.com/RuralScan/method/blob/main/data-model/evidence-classification.json) defines separate basis and format fields. Historical values are preserved; table/figure records receive unknown knowledge basis rather than inferred measurement status. Current intake checks the separate fields. Unknown-basis new proposals remain staged pending source review.

The pinned analytical compiler still uses legacy classifications to reproduce historical results. Claim-level reappraisal, replacement credibility multipliers, formal dependence-aware statistical pooling and new runtime weights require separate scientific decisions. Methods and review cards should show the new labels without implying those analytical changes have occurred.

Expert judgement is appraised from publications. Repeated observations and publications remain visible, with their dependencies and unresolved independence documented. No direct elicitation exercise is implied.
