---
title: Extracting evidence units
slug: extraction
summary: Produce evidence units that a reviewer and the synthesis engine can trust, and know which deterministic check catches which extraction error.
sources:
  - .agents/skills/source-command-extract-evidence/SKILL.md
  - .agents/skills/source-command-extract-evidence/references/defects.md
  - .agents/skills/extraction_contracts/T3_T6_extraction_contract.md
  - .agents/skills/extraction_contracts/T4_review_contract.md
  - .agents/skills/extraction_contracts/DIRECTION_ADDENDUM.md
  - methodology/T4_generation_method.md
  - methodology/T3_T6_generation_method.md
  - methodology/RULESET_VERSIONS.md
  - methodology/extraction_retrospective.md
  - methodology/search_protocol.md
  - schema/spec.md
  - schema/structure/columns.json
  - schema/lookups/variable_direction_sense.csv
  - schema/lookups/crop_scope_policy.csv
  - schema/lookups/comparator_policy.csv
  - schema/lookups/m2b_variable_policy.csv
  - schema/lookups/wocat_impact_map.csv
  - schema/lookups/wocat_hazard_map.csv
  - schema/registers/BANDS_magnitude_bands.csv
  - src/nbs_ruralscan/schema_tools/validate_sources.py
  - src/nbs_ruralscan/schema_tools/check_numbers.py
  - src/nbs_ruralscan/schema_tools/check_scope.py
  - src/nbs_ruralscan/schema_tools/check_quote.py
  - src/nbs_ruralscan/schema_tools/check_species.py
  - src/nbs_ruralscan/schema_tools/check_picos.py
  - src/nbs_ruralscan/schema_tools/check_context.py
  - src/nbs_ruralscan/schema_tools/check_bands.py
  - src/nbs_ruralscan/schema_tools/check_direction.py
  - src/nbs_ruralscan/schema_tools/quarantine.py
  - AGENTS.md
  - evidence:workflows/extraction/README.md
---

## What extraction does and does not do

Extraction records *what one source says about one variable*, as atomic, quoted claims. It does not write analytical table rows, choose a final threshold, decide whether a finding transfers to a target country or map an outcome to a scorecard priority. Those are synthesis decisions taken later, over the pooled evidence, by deterministic code. [src: .agents/skills/extraction_contracts/T3_T6_extraction_contract.md §0. What you are NOT doing] [src: methodology/T4_generation_method.md §0]

A paper is read once for every authorised role, not once per variable. The extractor traverses each paper, captures every relevant variable and relationship in a single pass, and records the variables it found on the source record. Harmonisation, weighting and synthesis follow. [src: methodology/T4_generation_method.md §3. Discovery] Where a lane is authorised for one table only, claims for other tables are not extracted but left as structured deferred pointers (source, page, claim kind, the source's wording, a note), so a later pass is a lookup rather than a re-read. [src: methodology/T3_T6_generation_method.md §3.5 Single-pass extraction and deferred pointers]

## The extraction pipeline

Every evidence unit is produced by the same deterministic route over a cached artefact: build a page-tagged index, retrieve passages by keyword and structure, emit units from the page-stamped passages, validate them, and save them to a staging area. [src: methodology/T3_T6_generation_method.md §3. The evidence atom: effect claims] [src: AGENTS.md §Don't]

Retrieval is deliberately vectorless: keyword search and navigation of the document's structure (sections, tables and figures with captions and pages) rather than embedding similarity. This is deterministic and auditable ("retrieved Table 3, p.7" can be reproduced), precise for known targets (a canonical variable with its aliases and units), and keeps tables intact. When a threshold appears only in a figure, a targeted reading of that one page image is permitted. [src: methodology/T4_generation_method.md §5.1 Document ingestion]

Before extracting, the extractor inventories the relevant pages, tables, continuations, figures and supplements and gives every relevant claim either an evidence identifier or an explicit hold, exclusion or referral with its page. A successfully retrieved paragraph does not establish that a table is complete, and existing records for a source do not prove it was fully extracted. [src: .agents/skills/source-command-extract-evidence/SKILL.md §Source and coverage checks] [src: .agents/skills/source-command-extract-evidence/references/defects.md §Main-paper extraction accounting (v1.6.15)]

Extraction agents write only to staging. They never edit registers, recipes or schema and never run version-control commands. A central, orchestrated step runs the staging gate and then the build checks; an agent's self-check is advisory. [src: AGENTS.md §Don't]

## The evidence unit

An evidence unit is one row of [[table:EV]]. Its required fields are listed below. [src: schema/structure/columns.json §EV]

| Field | Meaning |
|---|---|
| `evidence_id` | unique identifier |
| `source_id` | the source in [[table:SRC]] |
| `nbs_id`, `suitability_family_id` | practice and family the claim pertains to |
| `variable` | canonical variable from [[table:VONT]] |
| `use_role` | which consumer the unit may feed (below) |
| `evidence_type` | literature relationship, ML importance, scoping candidate or expert |
| `claim_basis` | measured, modelled, cited second-hand, expert assertion, table or figure reading |
| `claim_scope` | practice, species or crop (below) |
| `extraction_confidence` | fidelity of the transcription |
| `quote` | verbatim passage |
| `locator_type` | `page`, `section`, `char_span` or `file_line` |

Conditional fields are `taxon` (required when the claim is species- or crop-specific), `page` or `locator`, and `commit_sha` for code. Optional fields include the structured `relationship`, the `context` object, `lineage_of`, `raw_name`, `attribution`, separate justification quotes, `review_state` and `ruleset_version`. [src: schema/structure/columns.json §EV] [src: schema/spec.md §EV]

Units must be readable without the paper. Every acronym for a practice, treatment or measured variable is expanded; the practice is described in plain words; the baseline is always recorded; an absolute amount is given beside a relative change where the source states one; a stated effect size is encoded rather than left as narrative; and the source table or figure is named with its caption. [src: .agents/skills/source-command-extract-evidence/references/defects.md §Reviewer-readable units]

## Quotes are sliced, never retyped

The quote is cut programmatically from the page's extracted text, not typed. The provenance validator checks quotes against the same text layer, so a sliced quote passes by construction, whereas a retyped quote silently normalises characters (ligatures, dashes, spacing) and fails. [src: .agents/skills/source-command-extract-evidence/references/defects.md §Common extraction defects]

The rules on quote extent follow from what reviewers and checks need. [src: .agents/skills/source-command-extract-evidence/references/defects.md §Common extraction defects]

- **One contiguous passage.** Text is never stitched across passages or pages. Two-column PDFs can interleave columns in the text layer; a claim that does not survive contiguously is reported as a blocker with its page or image locator, not forced into a stitched quote.
- **Never a bare cell.** A quote carries the threshold sentence, or the table row with its header and caption, so it shows what the number means.
- **Never a whole table.** A quote that swallows a table hides which row was meant and lets the number check pass on other rows' numbers.
- **Start at the criterion.** A span that opens on a trend or study-site clause trips the scope check even when the rule inside is sound; the slice starts at the criterion sentence.

## Claim scope: practice, species and crop

Many "suitability" papers model a single tree or crop species, so their climate optima are the species' envelope, not the practice's. Every claim is therefore tagged: [src: methodology/T4_generation_method.md §5.2 Source & Evidence registers]

- `practice_technology`: the constraint comes from the practice itself (slope and erosion, soil depth, mechanisation, land cover). Safe for practice-level rows.
- `species_specific`: the constraint is the envelope of a tree grown for timber, service or fodder, or of a wild-harvested tree even if it fruits.
- `crop_specific`: the constraint is the envelope of a cultivated cash or food crop, including cultivated food trees.

What decides between species and crop is the product and its cultivation, not whether the plant is a tree. [src: methodology/RULESET_VERSIONS.md §v1.4.1] A `taxon` is recorded whenever the scope is not practice-level. [src: schema/spec.md §EV]

Species and crop evidence is never dropped. It is kept in the register and routed out of the practice-level surface, so that it remains available for a future species-level layer. The defect is the mis-tag: a species claim left as practice-level, which lets a species' rainfall optimum set a practice's rainfall envelope. On review, the fix for such a unit is to re-tag it and keep it. [src: .agents/skills/source-command-extract-evidence/references/defects.md §Common extraction defects]

Crop-specific evidence is re-admitted to practice-level cells only where the crop *is* the practice effect. The policy is held in a lookup: [src: AGENTS.md §What is locked]

{{csv:schema/lookups/crop_scope_policy.csv|cols=nbs_id,suitability_family_id,allow_crop_scope}}

A blank family applies to every family of that practice. In shaded perennial-crop agroforestry the understorey crop defines the system; in water harvesting the host crop's yield response is the practice effect; in paludiculture the cultivated wetland crop is the practice. Species-specific evidence is never re-admitted. [src: schema/lookups/crop_scope_policy.csv]

## PICOS: the practice must be in the source

The method applies the Population, Intervention, Comparator, Outcome and Study-design frame to the link between a source and a practice. The intervention (the practice or sub-practice) must appear explicitly in the source text or tool description before a unit is tagged to that practice or family. A demo dataset, a worked example, a file title, or the focus of the current sweep is not evidence of association. If the practice is not stated, the practice field is left blank, cross-cutting or agnostic. [src: AGENTS.md §Don't]

The test has known edge cases, each now a rule. [src: .agents/skills/source-command-extract-evidence/references/defects.md §Common extraction defects]

- A generic MCDA engine that ships an agroforestry example is not an agroforestry tool.
- Reforestation, afforestation, pure forestry or plantation, and the climate-smart agriculture umbrella are not agroforestry.
- An experiment that mimics the practice (artificial shade nets standing in for shade trees) is not the practice.
- Reduced tillage (ripping, zero or minimum tillage) is not water harvesting unless a capture structure (basin, pit, zaï, tied ridge, bund, half-moon, terrace, micro-catchment) is part of the treatment; synthetic mulch is never a nature-based component.
- A general cross-cutting envelope claim is tagged to the cross-family row, not defaulted to the first family.

Since ruleset v1.6.9, effect units carry the source's own description of the practice, including anything applied alongside it, so the practice test is read from the paper rather than inferred from the tag. [src: methodology/RULESET_VERSIONS.md §v1.6.9]

## Use roles and what each feeds

A unit's role decides which consumer it can reach. [src: methodology/T3_T6_generation_method.md §3.1 Roles] [src: schema/spec.md §EV] [src: .agents/skills/source-command-extract-evidence/SKILL.md §Establish scope]

| `use_role` | The source says | Feeds |
|---|---|---|
| `structural_suitability` | where the practice can be established: biophysical envelope, host system, hard exclusion | [[table:T4]] suitability |
| `operational_risk` | a soft enabling factor limits or enables implementation (access, tenure, finance, labour, extension) | the investment-risk operational filter and implementation guidance; kept out of T4 |
| `nbs_effect` | the practice changes an outcome (yield, erosion, carbon, income, a hazard's impact) | [[table:T3]] and/or [[table:T6]] via [[table:XW]] |
| `asset_vulnerability` | a hazard damages or kills the practice asset | T3 asset-threat rows only |
| `dataset` | a dataset operationalises a variable | [[table:T1]] |
| `climate_risk`, `priority_need` | reserved | not emitted |

The suitability-versus-operational split is a scientific invariant. Soft, investment-addressable factors (distance to road, travel time to market, value chains, tenure security, extension, credit, labour) are not structural suitability. Extracting them as `structural_suitability` is the `wrong_table` defect. Only hard exclusions (legal protected areas, water bodies, urban footprints) stay in T4, as masks. [src: AGENTS.md §What is locked] [src: .agents/skills/source-command-extract-evidence/references/defects.md §Common extraction defects]

An operational-risk unit must name a factor that limits or enables implementation, with cause and effect in the quote. Adoption rate is an outcome of the enabling environment, not an operational factor, and some practice-specific implementation details belong to feasibility. The policy lookup: [src: .agents/skills/source-command-extract-evidence/references/defects.md §Operational-risk (M2b) evidence]

{{csv:schema/lookups/m2b_variable_policy.csv|cols=variable,decision,reason}}

`exclude` means the staging gate refuses the unit in this role; `flag` means the detail is left as a pointer for implementation hand-off. [src: .agents/skills/source-command-extract-evidence/references/defects.md §Operational-risk (M2b) evidence]

### Suitability claims: three separate assessments

For a suitability claim the extractor assesses three things independently. [src: .agents/skills/extraction_contracts/T4_review_contract.md §Three independent assessments]

1. **Variable use:** did the source actually use the variable in its suitability calculation? Mention is not use.
2. **Suitability direction:** does suitability increase, decrease, peak in an optimum range, or respond non-monotonically as the variable rises? The values are `increasing`, `decreasing`, `optimum_range`, `non_monotonic` or `unclear`.
3. **Numeric calibration:** are units, class boundaries, endpoint meanings and scores sufficient for an executable function?

A claim can pass the first two and fail the third. It is then kept as direction evidence with a calibration hold, never dropped, and never used to create scores, interpolations, cutoffs or default weights. [src: .agents/skills/extraction_contracts/T4_review_contract.md §Three independent assessments]

Before any of this, a suitability lane records a page-linked quote showing that the source actually selects, maps or explains where the practice can be implemented. A study location, a measured benefit or the word "suitability" in a title is not enough. [src: .agents/skills/source-command-extract-evidence/SKILL.md §T4 source-purpose gate]

Shape parameters use canonical keys only: `abs_min`, `opt_low`, `opt_high`, `abs_max` and `unit`, because the synthesiser reads only those. [src: methodology/RULESET_VERSIONS.md §v1.4] A hard `abs_min` or `abs_max` requires the source to say that land beyond the value is excluded or unsuitable. The edge of a scored class, a recommended or commonly used range, a maximum taken across several structures, and a buffer or reserve width are not limits; they are retained in a source profile with their stated role. [src: .agents/skills/source-command-extract-evidence/references/defects.md §Limits, geometry and duplicates]

A single study's own site conditions (its rainfall, soil, tree density) are n = 1 context, not a generalising rule. The principle of constraining by observed distribution is a runtime dataset-gating layer, not a licence to encode one paper's site measurement as a threshold. Fixed-form practice-database entries are recorded as observed presence, not thresholds. [src: .agents/skills/source-command-extract-evidence/references/defects.md §Common extraction defects]

### Effect claims: the relationship object

An effect unit carries a structured relationship. [src: .agents/skills/extraction_contracts/T3_T6_extraction_contract.md §2.2]

```json
{
  "direction": "positive | negative | none",
  "direction_cue": "<shortest verbatim phrase carrying the movement>",
  "strength_class": "slight | moderate | strong | unspecified",
  "metric": "smd_hedges_g | pct_change | ln_response_ratio | absolute | ordinal_rating | narrative | contrast | complete_contrast",
  "magnitude": 23.0, "magnitude_low": 11.0, "magnitude_high": 35.0,
  "unit": "percent",
  "framing": "presence | loss",
  "significance": "sig | ns | not_reported",
  "n": 14,
  "design": "meta_analysis | rct | quasi_experimental | observational | model | case_study | expert | practitioner_rating",
  "outcome_raw": "maize grain yield, alley cropping vs sole crop"
}
```

The variable is the canonical outcome the paper measured, not the scorecard priority it might serve; the crosswalk does the routing, so a proxy is never relabelled silently. [src: methodology/T3_T6_generation_method.md §3.2 The effect-claim `relationship` object] Every number in the magnitude fields and `n` must be in the quote; with no number, the metric is `narrative`. A non-significant result is kept with `significance = ns`; nulls and negative findings are never dropped. [src: .agents/skills/extraction_contracts/T3_T6_extraction_contract.md §2.2]

Significance uses the 5 % convention: a result with 0.05 ≤ P < 0.10 is `ns` even if the authors call it significant at 10 %, with their wording recorded in a note. [src: .agents/skills/source-command-extract-evidence/references/defects.md §Operational-risk (M2b) evidence]

Strength comes from the magnitude bands register, never from adjectives such as "significantly" or "dramatically". [src: .agents/skills/extraction_contracts/T3_T6_extraction_contract.md §2.2]

{{csv:schema/registers/BANDS_magnitude_bands.csv|cols=band_id,metric,strength_class,abs_min,abs_max,unit,centre,source_scale_value}}

`abs_min` is inclusive and `abs_max` exclusive, on the absolute magnitude. The percentage bands are a scoping convention marked for ratification in the register. [src: schema/spec.md §BANDS] A reported range is classed by its weaker end, not its midpoint, and a range spanning zero has no assured strength. A comparison of one plot per farm with no statistical test is capped at `moderate`. [src: .agents/skills/source-command-extract-evidence/references/defects.md §Reviewer-readable units]

Every effect unit must also state the mechanism: how the practice changes the outcome. A bare rating, a restated rating, an observation with no cause, credit to a different practice or an invalid pathway is not evidence of an effect. [src: methodology/RULESET_VERSIONS.md §v1.6.18]

Effect units use fixed context keys only: `country` (ISO3), `region` (informational), `aez`, `farming_system`, `income_group` and `climate_zone`, plus hazard keys on hazard units. Other context goes in a free-text note. A blank income group where the country is known is a defect. [src: methodology/T3_T6_generation_method.md §3.3 Fixed context keys]

## Direction on the variable as named

`relationship.direction` is the movement of the outcome variable *as named*, as the quote states it. It is never "good" or "bad". Reduced erosion on `erosion_hazard` is `negative`, because erosion went down, even though it is a benefit. A runoff-reduction variable that rises is `positive`, because the variable is named as the reduction. [src: .agents/skills/extraction_contracts/DIRECTION_ADDENDUM.md §The rule (unchanged, restated)]

The meaning of positive and negative for every effect variable, and whether a high value is good or bad, is held in a lookup that the extractor reads before coding:

{{csv:schema/lookups/variable_direction_sense.csv|cols=variable,quantity,positive_means,negative_means,high_is}}

From ruleset v1.6.17, every unit with a direction also carries `direction_cue`, the shortest verbatim phrase from the quote that carries the movement. The self-check is to write "`<variable>` went up or down according to `<cue>`" and map up to positive and down to negative. Thinking "this is good, so positive" is the sign-frame defect. [src: .agents/skills/extraction_contracts/DIRECTION_ADDENDUM.md §New required key: `relationship.direction_cue`] [src: .agents/skills/extraction_contracts/DIRECTION_ADDENDUM.md §Self-check before emitting (say it in words)] The conversion to a benefit frame happens later, through the crosswalk's polarity. [src: schema/spec.md §XW]

`framing = loss` marks a source that measured what happens when vegetation or the practice is lost or absent. The direction is recorded as measured and the engine flips it into the intervention-present frame; the extractor never pre-flips. [src: .agents/skills/extraction_contracts/T3_T6_extraction_contract.md §2.2]

Two related traps: a weakening service (sediment retention declining with age) is encoded on the service variable with the decay described, never as the opposite harm; and a spread of estimates across implementers or sites is dispersion, coded `direction = none`, not a sign. [src: .agents/skills/source-command-extract-evidence/references/defects.md §Common extraction defects]

## Special encodings

### Contrasts

Some sources report a with-and-without (or after-and-before) pair. These use `metric = contrast` with `value_with` and `value_without`, both verbatim; the strength class is derived from their ratio against the response-ratio bands, and a zero baseline yields `strong`. An all-or-nothing statement with no number ("only fields with pits produced a harvest") is `complete_contrast`, strong by definition. Spelled-out multipliers ("two to three times", "doubled") count as numbers in the quote, and stated multipliers use a fold-change unit centred on 1. [src: methodology/RULESET_VERSIONS.md §v1.6.2]

### Hazard severity and magnitude

On every unit with a hazard type, the extractor records `hazard_severity` (mild, moderate, severe, extreme) from the author's own characterisation of the event, with the verbatim `severity_cue`, or `unspecified` when the source gives none. Severity is never inferred from rainfall statistics. The event's stated magnitude (dry-spell length, season rainfall, return period) is recorded verbatim in `hazard_magnitude`. A failure under an extreme event and a gain under a mild one are both kept: they mark the edges of the practice's response range. [src: .agents/skills/source-command-extract-evidence/references/defects.md §Reviewer-readable units] [src: methodology/RULESET_VERSIONS.md §v1.6.3]

A hazard type is set only when the source names the hazard. An ordinary dry season is not a drought, and general shade or wind benefit with no event is not heat or storm mitigation. [src: .agents/skills/source-command-extract-evidence/references/defects.md §Direction on the variable as named (v1.6.17)] [src: .agents/skills/extraction_contracts/T3_T6_extraction_contract.md §3. Defects specific to effect claims]

### Bundled interventions, counterfactuals and beneficiaries

Since ruleset v1.6.7, three context fields stop effects from being over-credited. [src: methodology/RULESET_VERSIONS.md §v1.6.7]

- `attribution` (`isolated` or `bundled`) with `bundle_components` and `component_share_pct`: a bundled programme's effect is never credited in full to one practice. Synthesis weights it by the stated share of the sample using the practice component, with a floor of 0.25, or by a flat 0.6 when the share is unstated. A marginal component ("an option in some communities") is excluded rather than discounted.
- `normal_year_reference` (`present` or `absent`): a hazard-year claim with no normal-year comparison is weighted ×0.7, because otherwise resilience and ordinary production gains cannot be told apart.
- `beneficiary` (`farm_household`, `community` or `society`): avoided-damage value to society stays out of the poverty priority.

An effect estimated against an unmeasured but physically implied no-practice case is tagged `counterfactual = implied` and also weighted ×0.7. [src: methodology/RULESET_VERSIONS.md §v1.9.7]

### Comparators

Studies of what existing forest or wetland does, or what its loss costs, are evidence for keeping it, not for planting or restoring it within a project horizon. Such units carry a comparator tag, and a policy lookup routes them: [src: methodology/RULESET_VERSIONS.md §v1.6.4]

{{csv:schema/lookups/comparator_policy.csv|cols=nbs_id,comparator,rollup_included,home_family}}

`rollup_included = false` keeps the unit out of the practice-level roll-up. A home family names the one family row it may enter. A restored wetland compared with an intact reference wetland is kept as a recovery note and never sets a class, because falling short of an intact system is not harm. [src: schema/lookups/comparator_policy.csv]

### Process metadata and descriptors

Run dates, ruleset stamps and review tags never go in `relationship`; they go in the context note. Study descriptors (buffer width, project length, comparator figures from elsewhere in the paper) never go in `outcome_raw` unless the number is in the quote. Both rules exist because these numbers otherwise read as smuggled values and bury real errors. [src: .agents/skills/source-command-extract-evidence/references/defects.md §Common extraction defects]

### Costs

An economic magnitude requires a per-unit denominator (per hectare, per hectare per year, per beneficiary, per tonne CO2e, per farmer). A project total is recorded with a total unit and fails the economic gate by design. A cost is routed by what the money buys (initial works versus ongoing operations), never by its denominator, so an annualised establishment cost stays an establishment cost. [src: .agents/skills/extraction_contracts/T3_T6_extraction_contract.md §2.2] [src: .agents/skills/source-command-extract-evidence/references/defects.md §Common extraction defects] Cost profiles are covered in [[ch:cost-profiles]].

### Ex-ante documents and baselines

Project appraisal documents, proposals and results frameworks state what a project will do; only ex-post completion, evaluation and impact reports supply effects. A baseline survey's treatment-versus-comparison differences reflect sampling design, not effects; the endline carries the effect. [src: .agents/skills/source-command-extract-evidence/references/defects.md §Common extraction defects]

## Tools as sources

A tool's hard-coded thresholds, default weights, criteria and exclusion rules are evidence claims, extracted from its source files at a pinned commit with `file_line` locators. The tool gets a Source Register row and a TOOL metadata row, and its evidence units are linked back. [src: AGENTS.md §Don't] [src: schema/spec.md §TOOL]

A tool's parameter is a design choice, not a measured finding, so its units carry `claim_basis = expert_assertion` and are weighted down in synthesis. The spec's TOOL section also names `tool_default` as an alternative basis value, which is not in the Evidence Register's claim-basis list; current practice uses `expert_assertion`. [src: AGENTS.md §Don't] [src: schema/spec.md §TOOL] [src: schema/spec.md §EV] Engines that compute weights at run time and hard-code nothing yield no extractable claim. Species-specific scripts are ignored as species envelopes. [src: AGENTS.md §Don't]

A tool that uses rainfall or pH to select species is not calibrating a practice-establishment curve. That method use is retained separately, scoped to species selection, and counted apart from practice-level agreement. [src: .agents/skills/source-command-extract-evidence/references/defects.md §Main-paper extraction accounting (v1.6.15)]

### Practice-database adapters

WOCAT questionnaire fields are emitted by a rule-based adapter driven by two lookups, which map questionnaire impact fields to canonical variables and coping fields to hazard types:

{{csv:schema/lookups/wocat_impact_map.csv|cols=wocat_group,wocat_field,canonical_variable_id,right_label,use_role,requires_comment}}

{{csv:schema/lookups/wocat_hazard_map.csv|cols=wocat_group,wocat_key,hazard_type}}

The adapter assigns the family from the sheet's own suitability evidence, so the practice follows the family, never the command-line argument. Every impact field requires a compiler comment: bare ratings are not ingested, and commented ratings still pass a mechanism check. Several mapping rows are recorded as pending ratification in the lookup. [src: methodology/search_protocol.md §WOCAT technology sheets] [src: methodology/RULESET_VERSIONS.md §v1.6.18] [src: schema/lookups/wocat_impact_map.csv]

## Multilingual quotes

A quote from a non-English source is stored in its native language followed by an English translation in brackets: `"[Native Text] (English: [Translated Text])"`. [src: methodology/T4_generation_method.md §Screening funnel] The provenance check runs on the native text only, and the native text must stand on its own as a substantive anchor; a translated-only claim or an empty native substring cannot pass. [src: src/nbs_ruralscan/schema_tools/validate_sources.py §module docstring] [src: .agents/skills/source-command-extract-evidence/references/defects.md §Adversarial pipeline checks] The number check reads decimal commas and thousands points, so magnitudes in Spanish, French and Portuguese sources are not lost. [src: methodology/RULESET_VERSIONS.md §v1.6.1]

## The deterministic checks

Quote verification proves a passage exists. It does not prove that the encoded numbers, scope, practice or direction are faithful: in early sweeps a third to a half of numeric units had misread or imported numbers despite real quotes. [src: .agents/skills/source-command-extract-evidence/references/defects.md §Common extraction defects] The method therefore runs a set of cheap, deterministic checks on every build, before any costlier adversarial review. [src: methodology/extraction_retrospective.md §Pre-LLM triage (efficiency)]

| Check | Catches | Effect |
|---|---|---|
| Provenance guardrail | missing artefact; quote not verbatim in the artefact; PDF quote not on the cited page | fails the build |
| Number provenance | a number in `relationship` (including in strings, ranges and spelled-out words) not present in the quote | advisory flag |
| Quote width | quotes shorter than the minimum (bare cells) or over 160 words (whole tables; 320 with a translation) | advisory flag |
| Scope | quotes from study-site, methods, carbon accounting or problem-statement sections; site context framed as a rule; land-capability schemes; land cover with no class list; inferred hard limits, recommended ranges and design geometry encoded as limits | advisory; some signals feed auto-quarantine |
| Practice (PICOS) | a suitability unit whose quote signals a different practice and carries no signal of the tagged one | advisory; feeds auto-quarantine |
| Species | a taxon set on a practice-level unit; a taxon named in the quote or citation of a practice-level unit | advisory |
| Context | unknown context keys; out-of-vocabulary values; missing income group; severity without hazard or without its verbatim cue; unlogged severity; missing practice description | advisory |
| Bands | strength class disagreeing with its magnitude band; adjective strength with no number; unknown metric | advisory |
| Direction | effect or crosswalk variable with no sense row; crosswalk polarity disagreeing with the sense table | fails the build |
| Direction cue | missing cue; cue not verbatim; cue whose movement word contradicts the coded direction | advisory |

[src: src/nbs_ruralscan/schema_tools/validate_sources.py §module docstring] [src: src/nbs_ruralscan/schema_tools/check_numbers.py §module docstring] [src: src/nbs_ruralscan/schema_tools/check_quote.py §module docstring] [src: src/nbs_ruralscan/schema_tools/check_scope.py §module docstring] [src: src/nbs_ruralscan/schema_tools/check_picos.py §module docstring] [src: src/nbs_ruralscan/schema_tools/check_species.py §module docstring] [src: src/nbs_ruralscan/schema_tools/check_context.py §module docstring] [src: src/nbs_ruralscan/schema_tools/check_bands.py §module docstring] [src: src/nbs_ruralscan/schema_tools/check_direction.py §module docstring] [src: .agents/skills/source-command-extract-evidence/references/defects.md §Limits, geometry and duplicates]

Most checks are advisory because their signals are proxies: a genuine suitability claim can mention carbon, and a paper can contrast agroforestry with reforestation. They triage for human review rather than overrule it. [src: src/nbs_ruralscan/schema_tools/check_scope.py §module docstring] [src: src/nbs_ruralscan/schema_tools/check_picos.py §module docstring]

Off-scope and wrong-practice signals feed an automatic quarantine that soft-drops matching units on the write path of the build, so they do not reach the reviewer's default queue. It never touches a unit a person has approved, dropped, decided or reopened, stamps the reason on the unit, and is reversible. [src: src/nbs_ruralscan/schema_tools/quarantine.py §module docstring] Advisory signals designed for re-slicing or judgement (span bleed, inferred limits, recommended ranges, design geometry) are never auto-quarantined. [src: .agents/skills/source-command-extract-evidence/references/defects.md §Common extraction defects] [src: methodology/RULESET_VERSIONS.md §v1.10.1]

The staging gate runs the same unit-level checks as the build, so a lane cannot pass a file that the build would flag. [src: methodology/RULESET_VERSIONS.md §v1.6.10] It also rejects typed-payload errors (duplicate keys, non-finite numbers, Booleans used as numbers) and refuses units from unregistered or unverified sources, empty quotes or page zero. [src: .agents/skills/source-command-extract-evidence/references/defects.md §Adversarial pipeline checks] [src: .agents/skills/source-command-extract-evidence/references/defects.md §Pipeline integrity (v1.7.0)]

No check proves scientific plausibility. A correctly transcribed class can still be unfit for a recipe; that judgement is part of review (see [[ch:review-and-quality]]). [src: src/nbs_ruralscan/schema_tools/check_numbers.py §module docstring]

## Assumptions and limits

- **Extraction is interpretive.** Choosing the variable, role, scope and direction involves judgement that checks only partly constrain. The adversarial review checks omissions as well as additions, but neither proves completeness.
- **Text layers limit what can be quoted.** Two-column layouts, image-only tables and page breaks leave some claims unquotable; they are blockers, not evidence.
- **Context is only as good as the source.** Many sources state no income group, agro-ecological zone or farming system; units then carry less transferable context and synthesis treats them conservatively.
- **Severity is mostly unspecified.** Authors rarely characterise the hazard event, so the severity field is sparse.
- **Second-hand readings drift.** Units citing other works are kept as pointers to the primary, which supersedes them once acquired; until then they carry the risk of misreading. [src: .agents/skills/source-command-extract-evidence/references/defects.md §Common extraction defects]
- **Several lookups are pending ratification,** including parts of the WOCAT maps and the percentage bands; their values may change.

## Where this is configured

- Evidence rows: [[table:EV]]; routing and bands: [[table:XW]], [[table:BANDS]]; canonical variables: [[table:VONT]]; families: [[table:FAM]]; tools: [[table:TOOL]].
- Lookups: `schema/lookups/variable_direction_sense.csv`, `crop_scope_policy.csv`, `comparator_policy.csv`, `m2b_variable_policy.csv`, `wocat_impact_map.csv`, `wocat_hazard_map.csv`.
- Instructions: `.agents/skills/source-command-extract-evidence/SKILL.md` (ruleset v1.10.1), its defect catalogue, and the contracts in `.agents/skills/extraction_contracts/`.
- Checks: `src/nbs_ruralscan/schema_tools/` (`validate_sources`, `check_numbers`, `check_quote`, `check_scope`, `check_picos`, `check_species`, `check_context`, `check_bands`, `check_direction`, `quarantine`).
- Related chapters: [[ch:acquisition]], [[ch:review-and-quality]], [[ch:suitability-synthesis]], [[ch:effect-synthesis]], [[ch:rulesets-and-learning]].
