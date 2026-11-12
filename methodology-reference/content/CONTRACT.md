# Chapter contract — RuralScan methodology reference

You are writing chapters of a **comprehensive scientific methodology reference for technical
users** (GIS analysts, data scientists, agronomists and ecologists on a development-bank task
team, and the scientists who will maintain the method). A reader must be able to understand,
audit and re-implement the method from these chapters without access to the authors. Depth is
the point: state the rules, the formulas, the thresholds' origin, the assumptions and the limits.
A thin summary with links out is a failure. Padding and unsupported claims are also a failure.

## Where to read and write

- WRITE ONLY to `content/<slug>.md` in this reference directory
  for the slugs assigned to you. Create no other file anywhere. Edit no repository.
- READ sources read-only. The scientific source of record is the CIAT repository at the pinned
  producer commit **`e5c8da02e72810956cfd179cb32cd137fc4ba398`** (call it `P`). Its working
  tree is AHEAD of `P` and has unrelated work in progress, so read files at the pin:
  `git -C <producer checkout> show e5c8da02e72810956cfd179cb32cd137fc4ba398:<path>`
  (list with `git -C ... ls-tree -r --name-only e5c8da02e72810956cfd179cb32cd137fc4ba398 <dir>`).
  Useful roots at `P`: `methodology/` (framework.md, modules/, families/, T4_generation_method.md,
  T3_T6_generation_method.md, T4_developer_contract.md, search_protocol.md, RULESET_VERSIONS.md,
  farming_system_classifier.md, opportunity_space_T5.md, weight_normalisation.md, …),
  `schema/spec.md`, `schema/structure/columns.json`, `schema/lookups/*.csv`, `schema/registers/*.csv`,
  `schema/T1_data_registry.csv`, `schema/T2_climate_risk.csv`, `schema/T5_opportunity_space.csv`,
  `schema/T7_geographic_context.csv`, `schema/recipes/<practice>/`, `AGENTS.md` (locked decisions),
  `.agents/skills/` (extraction and synthesis contracts), `reference/`.
- Product-facing companions (read from the working tree, read-only):
  the method repository (handbook/, cookbook/, data-model/spec.md)
  and the evidence repository (workflows/*/README.md, handbook/, examples/).
- Git: only `git show`, `git ls-tree`, `git log`. Never checkout, pull, fetch, stash, reset, add,
  commit. Run no build or generate script. No network.

## File format

```
---
title: <chapter title, plain words>
slug: <assigned slug>
summary: <one sentence, what the reader can do after this chapter>
sources:
  - <path at P, or method:<path>, or evidence:<path>>
---
<markdown body, starting at ## headings; no # heading>
```

Markdown allowed: `##`/`###` headings, paragraphs, bullet and numbered lists, pipe tables,
fenced code, **bold**, *italic*, `code`. No HTML. No images. No footnotes.

Formulas go in fenced blocks tagged `formula`, written in plain text with Unicode
(`×`, `Σ`, `≤`, subscripts as `w_i`). Define every symbol directly under the block.

### Links and directives (the generator resolves these; use them, do not hand-write URLs)

- Chapter: `[[ch:<slug>]]` or `[[ch:<slug>|link text]]`. Valid slugs are listed below.
- Data-model table entry: `[[table:T4]]` (IDs: T0 T1 T2 T3 T4 T5 T6 T6E T7 SRC EV VONT FAM BIND SRCH XW BANDS TOOL T4_RUN T4_NUMERIC_POLICY).
- Variable: `[[var:<variable_id>]]` (IDs from `schema/registers/VONT_variable_ontology.csv`).
- Practice: `[[practice:<nbs_id>]]` (agroforestry, forest_restoration, mangrove_restoration,
  riparian_buffer, water_harvesting_conservation, wetland_management).
- Source citation, placed at the end of the sentence or paragraph it supports:
  `[src: <path at P> §<section heading or number>]`, e.g. `[src: methodology/modules/M2_climate_risk.md §4]`.
  For the product repos: `[src: method:handbook/implement-a-scan.md §Inputs]`, `[src: evidence:workflows/discovery/README.md §Screening]`.
  For the runtime repository (published main branch): `[src: runtime:docs/DESIGN.md §Boundary]`.
- Pinned rule table, rendered from the file at `P` so numbers are never retyped:
  `{{csv:schema/lookups/design_weights.csv}}` on its own line. Optional filters:
  `{{csv:schema/lookups/effect_locus.csv|cols=nbs_id,suitability_family_id,locus}}`,
  `{{csv:schema/T2_climate_risk.csv|where=hazard_id=drought|limit=20}}`.
  Check the column names in the file before using `cols=` or `where=`.
- `{{attribution:primitives}}` on its own line where the inherited framework primitives are
  introduced (the five fuzzy membership functions; hybrid AHP + CRITIC + Entropy weighting; the
  reference MCDA implementation; the recipe-template and sub-practice-family patterns). Do not
  write the attribution yourself.

## Content rules

1. **Traceable.** Every rule, threshold, weight, enum and formula is followed by a `[src: …]`
   citation to the file that states it. If two sources disagree, say so and cite both. If you
   cannot find the source for something you believe is true, leave it out.
2. **No retyped rule tables.** Where a rule lives in a lookup or register CSV, use `{{csv:…}}`
   and explain it in prose. You may quote a single constant inline (for example a 0.7 haircut)
   with its citation.
3. **Specification vs application.** Say precisely what is specified, what is implemented in the
   evidence pipeline, and what is left to a country application. Do not claim a module has been
   run, validated or calibrated unless a pinned file records it. Where the source marks something
   draft, pending, held or deferred, carry that status.
4. **Scientific invariants that must survive** (do not soften or contradict):
   - Scoping tool, not feasibility: scoping flags, feasibility validates.
   - Suitability is reasoned per suitability family (sub-practices grouped by shared dominant
     limiting factor), each with a spatial product type; linear, zonal and qualitative products
     are never reported as pixel area.
   - Held or unrecorded numerical calibration is never a score, a range or "reviewed".
   - Soft enabling-environment variables are operational-risk inputs, not structural suitability;
     only hard exclusions are suitability masks.
   - Risk to livelihoods (M2, a need layer) and risk to the investment (M2b, a filter) are
     distinct and never summed.
   - Effect rows are generated by cell synthesis; confidence has two axes (evidence, agreement)
     plus a transfer class; evidence from outside the target context is always labelled.
   - Costs are indicative and ordinal, not cost-benefit analysis.
   - Effort counts are not evidence strength; counts from different editions are never combined.
5. **Public-product boundary.** No personal names, initials, handles, team roles or assignments;
   no dates of internal rulings, meeting notes, PR or issue numbers, sprint or round names; no
   contract, budget, funder-acceptance or project-management content. Translate "ruled on <date>"
   into the rule itself. Software/tool names and published sources (WOCAT, IPCC AR6, MapSPAM,
   CHELSA, etc.) are fine. Refer to internal instruments by function ("the extraction ruleset",
   "the review workspace"), with ruleset version numbers where they define behaviour.
6. **Voice.** British English. Precise, plain, technical. Short paragraphs. Define each term on
   first use. Prefer "the method does X because Y" to passive description. No marketing, no
   "robust", "cutting-edge", "comprehensive", "seamless". No em dashes.
7. **Honest limits.** Every chapter ends with `## Assumptions and limits` (what the method cannot
   tell you, known weaknesses, what a feasibility study must still do) and `## Where this is
   configured` (which tables, registers and lookups hold the rules, using `[[table:…]]` links).

## Standard skeleton for a module chapter (M0–M6, M2b)

`## Question this module answers` · `## Inputs` (tables, variables, user choices) ·
`## Method` (numbered steps with formulas; one `###` per step where long) · `## Outputs`
(what is produced, at what grain, how to read it) · `## Worked illustration` (only from pinned
material; omit if none) · `## Assumptions and limits` · `## Where this is configured`.

Target 1,500–3,000 words per module or method chapter; go longer where the source has the
substance. Do not pad.

## Chapter slugs (the complete set; link only to these)

Part 1 Method: `scope-and-framework` · `scoping-walkthrough` · `m0-setup` · `m1-suitability` · `farming-systems-and-data` ·
`m2-climate-risk` · `m2b-project-risk` · `m3-characterisation` · `m4-hotspots` · `m5-scorecard` ·
`m6-handoff` · `implementing-the-method`

Part 2 Evidence methods: `evidence-principles` · `discovery` · `acquisition` · `extraction` ·
`review-and-quality` · `suitability-synthesis` · `effect-synthesis` · `cost-profiles` ·
`rulesets-and-learning`

Part 4 Practices (family schemes): `practice-agroforestry` · `practice-forest_restoration` ·
`practice-mangrove_restoration` · `practice-riparian_buffer` ·
`practice-water_harvesting_conservation` · `practice-wetland_management`

Generated by the build, not by you (you may link to them): data-model dictionary (`[[table:…]]`),
variable ontology (`[[var:…]]`), practice data pages (`[[practice:…]]`), and the pages
`[[ch:editions]]`, `[[ch:glossary]]`, `[[ch:evidence-base]]`, `[[ch:reproduce]]`.

## Final message

Return 5 lines maximum: files written with word counts, any source you could not open, and any
place where sources contradict each other or where you had to leave a gap.
