# Chapter contract — RuralScan methodology reference

Write a scientific methodology that a development-bank task team can read and an analyst can audit. Explain the decision, inputs, method, output meaning and material limits. Use plain language. Lead with the reader’s decision, explain technical terms on first use, and link to detailed contracts rather than repeating their instructions. Keep historical examples distinct from current rules. Include equations when they define the reported result; keep detailed evidence-synthesis rules in their owning chapter and link to them elsewhere.

## Sources and editorial scope

Read the revisions selected by `build/core.py` and the evidence release pin; `P` below means that pinned producer revision. Distinguish an immutable evidence edition from the current runtime implementation. A historical script or prototype is not evidence that its algorithm remains the current method. Check current runtime documentation when describing implementation, and record the revision inspected in the review response.

Chapter edits do not change analytical tables or approve a new algorithm. Preserve the scientific constraints below. Keep unresolved implementation choices in the repository review record; describe limitations in a public chapter only when they affect what a reader can conclude. Never imply that removing a development-status paragraph validates the analysis.

Use a versioned pull request, update `VERSION.json` and `CHANGELOG.md`, and build the pages with their link, provenance and caption checks. Preserve unrelated work.

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
fenced code, **bold**, *italic*, `code`. Every table needs a descriptive caption: put `Table: <description>` immediately before its pipe table. The build supplies its number. No HTML. No images. No footnotes.

Formulas go in fenced blocks tagged `formula`, written in plain text with Unicode
(`×`, `Σ`, `≤`, subscripts as `w_i`). Define every symbol directly under the block.

### Links and directives (the generator resolves these; use them, do not hand-write URLs)

- Chapter: `[[ch:<slug>]]` or `[[ch:<slug>|link text]]`. Valid slugs are listed below.
- Data-model table entry: `[[table:T4]]` (IDs: T0 T1 T2 T3 T4 T5 T6 T6E T7 SRC EV VONT FAM BIND SRCH XW BANDS TOOL T4_RUN).
- Variable: `[[var:<variable_id>]]` (IDs from `schema/registers/VONT_variable_ontology.csv`).
- Practice: `[[practice:<nbs_id>]]` (agroforestry, forest_restoration, mangrove_restoration,
  riparian_buffer, water_harvesting_conservation, wetland_management).
- Source citation, placed at the end of the sentence or paragraph it supports:
  `[src: <path at P> §<section heading or number>]`, e.g. `[src: methodology/modules/M2_climate_risk.md §4]`.
  For the product repos: `[src: method:handbook/implement-a-scan.md §Inputs]`, `[src: evidence:workflows/discovery/README.md §Screening]`.
  For the runtime repository (published main branch): `[src: runtime:docs/DESIGN.md §Boundary]`.
  For the producer repository at the revision where its evidence records became read-only (later
  than `P`; use only for the retirement itself and what it left in place): `[src: retired:AGENTS.md §…]`.
- Pinned rule table, rendered from the file at `P` so numbers are never retyped:
  `{{csv:schema/lookups/design_weights.csv}}` on its own line. Optional filters:
  `{{csv:schema/lookups/effect_locus.csv|cols=nbs_id,suitability_family_id,locus}}`,
  `{{csv:schema/T2_climate_risk.csv|where=hazard_id=drought|limit=20}}`.
  Optional `exclude=column=value` omits matching rows from this display only; it never changes the register. Use `caption=Descriptive caption` to identify the displayed subset.
  Check the column names in the file before using `cols=`, `where=` or `exclude=`.

## Content rules

1. **Traceable.** Every rule, threshold, weight, enum and formula is followed by a `[src: …]`
   citation to the file that states it. Resolve superseded wording against the governing source. If an unresolved difference affects interpretation, state its practical consequence and cite the relevant sources; put the detailed reconciliation in the review record. If you
   cannot find the source for something you believe is true, leave it out.
2. **No retyped rule tables.** Where a rule lives in a lookup or register CSV, use `{{csv:…}}`
   and explain it in prose. You may quote a single constant inline (for example a 0.7 haircut)
   with its citation.
3. **Specification vs application.** Keep method specification, evidence-edition contents and results of a country application distinct. Give the common reporting boundary in the application chapter rather than repeating development inventories in every module. Do not claim a module has been
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
   - Current effect outputs come from AI-authored proposals with explicit human scientific acceptance; deterministic validation and packaging do not choose ratings. Historical compiled rows remain labelled as such. Confidence has two axes (evidence, agreement)
     plus a transfer class; evidence from outside the target context is always labelled.
   - Costs are indicative and ordinal, not cost-benefit analysis.
   - Effort counts are not evidence strength; counts from different editions are never combined.
5. **Public-product boundary.** No personal names, initials, handles, team roles or assignments;
   no dates of internal rulings, meeting notes, PR or issue numbers, sprint or round names; no
   contract, budget, funder-acceptance or project-management content. Translate "ruled on <date>"
   into the rule itself. Software/tool names and published sources (WOCAT, IPCC AR6, MapSPAM,
   CHELSA, etc.) are fine. Refer to internal instruments by function ("the extraction ruleset",
   "the review workspace"), with ruleset version numbers where they define behaviour.
   One exception: where a route or feature is planned and not built, a chapter may link to its
   open public plan. The link text describes the plan in words; no issue number is shown.
   A second exception, for one generated page only: `help.html` names the project contacts and
   team. That section is read at build time from the visual methodology's help page; no chapter and
   no file in this folder names a person.
6. **Voice.** British English. Precise, plain, technical. Short paragraphs. Define each term on
   first use. Prefer "the method does X because Y" to passive description. No marketing, no
   "robust", "cutting-edge", "comprehensive", "seamless". No em dashes.
7. **Honest limits.** Every chapter ends with `## Assumptions and limits` (what the method cannot
   tell you, known weaknesses, what a feasibility study must still do) and `## Where this is
   configured` (which tables, registers and lookups hold the rules, using `[[table:…]]` links).

## Standard skeleton for a module chapter (M0–M6, M2b)

`## Question this module answers` · `## Inputs` (tables, variables, user choices) ·
`## Method` (numbered steps with formulas; one `###` per step where long) · `## Outputs`
(what is produced, at what grain, how to read it) · `## Worked illustration` (from cited material or explicitly hypothetical) · `## Assumptions and limits` · `## Where this is configured`.

Hypothetical worked illustrations are allowed when explicitly labelled. Their numbers must not be presented as registered findings, calibrated thresholds or new policy. Show the decision and its consequence; verify any arithmetic against the stated method. Keep each detailed rule or lookup in one home chapter and cross-link it elsewhere.

Use the length needed for the decision and its interpretation, not a minimum word count. Prefer short module chapters with one home for each shared explanation. Evidence-method chapters may be longer where reproducibility requires the detail. Do not duplicate full registries already accessible in the data-model section.

## Chapter slugs (the complete set; link only to these)

Part 1 Method: `scope-and-framework` · `scoping-walkthrough` · `m0-setup` · `m1-suitability` · `farming-systems-and-data` ·
`m2-climate-risk` · `m2b-project-risk` · `m3-characterisation` · `m4-hotspots` · `m5-scorecard` ·
`m6-handoff` · `implementing-the-method`

Part 2 Evidence methods (shared foundations, acquisition-to-review sequence, common synthesis, then table-specific synthesis workflows): `evidence-principles` · `discovery` · `acquisition` · `extraction` ·
`review-and-quality` · `compiling-evidence` · `suitability-synthesis` · `effect-synthesis` · `cost-profiles`

Part 8 System and setup: `system-setup`

Not published (kept in `content/unpublished/`, do not link): `rulesets-and-learning` · `continue-with-ai`

Part 4 Practices (family schemes): `practice-agroforestry` · `practice-forest_restoration` ·
`practice-mangrove_restoration` · `practice-riparian_buffer` ·
`practice-water_harvesting_conservation` · `practice-wetland_management`

Generated by the build, not by you (you may link to them): data-model dictionary (`[[table:…]]`),
variable ontology (`[[var:…]]`), practice data pages (`[[practice:…]]`), and the pages
`[[ch:editions]]`, `[[ch:glossary]]`, `[[ch:evidence-base]]`, `[[ch:reproduce]]`.

## Final message

Return 5 lines maximum: files written with word counts, any source you could not open, and any
place where sources contradict each other or where you had to leave a gap.

## Priority workflow

`{{priority-workflow}}` renders the ordered M1–M4 classification and weighting diagram.
Its four class scores come from `data-model/priority-contract.json`; text, order and caption
remain accessible without scripts or hover. M2b is labelled as a separate screen.
