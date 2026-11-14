---
title: Finding and screening sources
slug: discovery
summary: Plan, run, screen and log a bounded source search for one practice, family and table so that another analyst can see exactly what was searched, what was kept and why.
sources:
  - methodology/search_protocol.md
  - methodology/T4_generation_method.md
  - methodology/T3_T6_generation_method.md
  - .agents/skills/source-command-discover-sources/SKILL.md
  - schema/spec.md
  - schema/structure/columns.json
  - src/nbs_ruralscan/schema_tools/ledger.py
  - AGENTS.md
  - evidence:workflows/discovery/README.md
  - evidence:handbook/assisted-evidence-run.md
---

## What discovery is for

Discovery finds *what to look for and where*. It proposes candidate sources and candidate variables. It is allowed to be speculative because nothing it proposes reaches an analytical value without passing through acquisition, extraction, the provenance checks and review. [src: methodology/T4_generation_method.md §3. Discovery]

Discovery is not exhaustive. The method deliberately does not sweep tens of thousands of abstracts. It assembles a bounded, authority-weighted set of sources per practice and table, expands it only where that set leaves obvious gaps, and records the bounds so that a reader knows what the search could and could not have found. [src: methodology/T4_generation_method.md §Bounded, authority-weighted seed-set rule]

Each analytical table has its own corpus. A large stocktake of spatial-suitability and MCDA papers was the starting corpus for suitability ([[table:T4]]). It is a weak source for hazard response ([[table:T3]]) and scorecard effects ([[table:T6]]), which need effectiveness, impact and evaluation literature. Existing suitability papers are not proof of effect coverage, or the reverse. [src: methodology/T4_generation_method.md §Bounded, authority-weighted seed-set rule] [src: methodology/T3_T6_generation_method.md §6. Sources]

## The unit of search

A search is defined by four keys: practice, suitability family, table and discovery process. [src: methodology/search_protocol.md §The rule]

- **Practice and family.** An empty family is the *generic parent search*: one broad query over the practice and all its synonyms. A named family is a *sub-practice-targeted search*, which keeps the parent synonyms and adds the family's own vocabulary (for example, alley cropping or tree intercropping for planted silvoarable agroforestry). [src: methodology/search_protocol.md §Generic (parent) search vs sub-practice search]
- **Table.** One of T4, T3 or T6. Establishment suitability, restoration priority, species matching, observed distribution, soft operational feasibility and effects are different lanes; adjacent useful work is recorded as a named referral, not tagged to the wrong table. [src: .agents/skills/source-command-discover-sources/SKILL.md §Scope and coverage]
- **Process.** One of the four discovery processes below.

The generic and targeted searches are different nets with different recall. The union of the targeted family searches is not the parent search, and searches are never summed. A family with no targeted search is shown as "covered by the generic net, not targeted", never as done. [src: methodology/search_protocol.md §Generic (parent) search vs sub-practice search]

## The four discovery processes

For each authorised family and table, each of the four processes is run or explicitly accounted for, and each is logged before the search is claimed done. [src: methodology/search_protocol.md §The rule]

| Process | What it covers | Channels |
|---|---|---|
| `stock` | the benchmarked stocktake corpus (peer-reviewed, already tiered) | reconciliation of the existing screened pool |
| `updated_lit` | a focused peer-reviewed sweep beyond the stocktake | OpenAlex title search; Lens.org |
| `grey` | reports, manuals, briefs, project evaluations, practice databases | functional web search in several languages; CGSpace repository API; WOCAT; AGRIS (manual) |
| `tool` | tools, methods and codebases | GitHub, GitLab, project and academic platforms |

[src: methodology/search_protocol.md §The 4 discovery processes] [src: .agents/skills/source-command-discover-sources/SKILL.md §Search and screen]

**Stock** reconciles the original screened pool: titles, local artefacts and sources that were screened in but never taken in. **Updated literature** reuses title-search machinery, starting from reviews and seminal methods and then seeking primary studies for criteria the seeds leave uncovered. **Grey** uses organisation-neutral functional searches plus targeted checks of agency repositories, practice databases and evaluation reports. **Tool** inspects the actual methods, scripts and parameter files of candidate repositories; a README, project name or demo dataset is not evidence that a tool encodes a rule for a practice. [src: .agents/skills/source-command-discover-sources/SKILL.md §Search and screen]

Searches also follow references from strong seeds back to original methods and forward to later applications, and distinguish new independent studies from reused methods, reviews, translations and companion reports. [src: .agents/skills/source-command-discover-sources/SKILL.md §Search and screen]

## The bounded, authority-weighted seed set

Per practice and table, discovery assembles a capped seed set of roughly 10 to 20 authoritative sources, in approximate order of authority. [src: methodology/T4_generation_method.md §Bounded, authority-weighted seed-set rule]

1. **Authority sources with project relevance:** the development bank's rural NbS catalogue and project evidence (implementation completion reports and independent evaluation reviews), decision-support tools named in the terms of reference, GEF and NBS investment materials, IPCC assessment chapters, FAO frameworks and practice databases, WRI restoration materials, and CGIAR system-level reviews.
2. **High-leverage "diamond" classes:** WOCAT technology questionnaires (structured, grounded in lower-income contexts, covering requirements, impacts, costs and adoption), evidence gap maps (3ie, Campbell Collaboration, CEE), specialist practice databases from research centres, Indigenous and community land layers, and climate-smart agriculture adoption and barrier syntheses.
3. **Peer-reviewed syntheses:** global-scale suitability models and MCDAs, major meta-analyses and reviews, and monitoring, evaluation and learning (MEL) reports from large programmes.
4. **Primary studies,** admitted only when the seed set above is thin.

FAO Ecocrop is restricted to modelling the understorey crop envelope of shaded perennial-crop systems and is excluded for general practice suitability. Global suitability models provide provisional defaults that local context overrides and dataset bindings can refine. [src: methodology/T4_generation_method.md §Bounded, authority-weighted seed-set rule]

Evidence gap maps play a second role: they show where empirical support is absent, so the method can avoid claiming precision it does not have. [src: methodology/T4_generation_method.md §Bounded, authority-weighted seed-set rule]

Adoption and dis-adoption studies and MEL reports are treated as observed-reality evidence, not a separate stream. They extend the "constrain by observed distribution" principle to the human side: if a practice is not adopted where its bioclimatic envelope is favourable, a system or operational constraint is binding. They are tagged `method_type = adoption_study` or `mel_report` and tiered like any other source. [src: methodology/T4_generation_method.md §Evidence-source principle]

### Why effect searches target syntheses first

For hazard-response and scorecard effects, discovery searches for meta-analyses, systematic reviews, evidence gap maps and reviews first, then MEL and impact-assessment grey literature (completion reports, independent evaluations, programme impact studies), and seeks primary studies only to fill cells the syntheses leave empty. [src: methodology/search_protocol.md §Learnings from the agroforestry synthesis-first round] [src: methodology/T3_T6_generation_method.md §3.5 Single-pass extraction and deferred pointers]

The reasons are practical and statistical. One good synthesis replaces many primary extractions. Pooled estimates are what the effect engine is built to reconcile, and syntheses are weighted above single studies and practitioner ratings in synthesis (see [[ch:effect-synthesis]]). Ex-ante project appraisal documents are proposals, never effect evidence. [src: methodology/T4_generation_method.md §Screening funnel] [src: methodology/search_protocol.md §Learnings from the agroforestry synthesis-first round]

A reusable block of study-type terms (systematic review, systematic map, scoping review, evidence and gap map, evidence synthesis, umbrella review, review of reviews and similar) is kept verbatim and joined into synthesis-first queries. [src: methodology/search_protocol.md §Bibliographic sources]

Effect evidence must come from effect-targeted discovery. When effect evidence that had been found incidentally through suitability searches was reviewed, only the units found by searches aimed at effects were carried forward; the suitability corpus is not a substitute. [src: methodology/T3_T6_generation_method.md §6. Sources]

## Writing search strings

### Title-only queries

Programmatic literature queries target title fields (for OpenAlex, the `display_name.search` filter) rather than full text, to avoid high-citation noise and non-specific matches. [src: methodology/T4_generation_method.md §Screening funnel]

### Multilingual synonyms from AGROVOC

Query terms combine the practice's synonyms, sub-practice names and translations drawn from the FAO AGROVOC thesaurus in English, Spanish, French and Portuguese, so that literature from the lower-income contexts the scan serves is not missed. [src: methodology/T4_generation_method.md §Screening funnel] Practice-level searches OR the full synonym set; dropping a synonym narrows recall, so any omission is a logged decision. [src: methodology/search_protocol.md §Synonym policy]

Experience with these queries produced specific rules. [src: methodology/search_protocol.md §Learnings from the agroforestry synthesis-first round] [src: methodology/search_protocol.md §WOCAT technology sheets]

- OpenAlex title search is accent-sensitive, so accented and unaccented forms are both run.
- French queries must not include words shared with English (such as *afforestation*, *impacts*, *erosion*); one such query returned hundreds of English papers.
- Ambiguous words are qualified. Portuguese and Spanish *seca* also matches "dry matter" and pulls in tillage agronomy; French *haies* (hedges) pulls in English "hay".
- Web and database strings stay organisation-neutral and functional ("agroforestry climate adaptation manual"). Institutional authority is judged at screening, not built into the query. [src: methodology/T4_generation_method.md §Screening funnel]

### Verbatim capture

The search register records the exact query string actually run, copied from the search configuration or run script, never a paraphrase. This rule exists because a paraphrase once silently dropped the climate block and all practice synonyms from a recorded search. If the verbatim string lives in a file, that file is cited in the search note. [src: methodology/search_protocol.md §Search-term capture must be VERBATIM]

## Bibliographic sources used and not used

The source list was compared with an external umbrella-review protocol and kept deliberately lean. [src: methodology/search_protocol.md §Bibliographic sources]

| Source | Status | Reason |
|---|---|---|
| OpenAlex, CGSpace, World Bank documents, FAO repository, 3ie, Campbell | used | core literature and evaluation repositories |
| WOCAT, ICRAF/TECA, GEF, WRI, IEG, HAL, SciELO | used | practice-level grey and regional literature |
| Lens.org | used, scripted | adds preprints and theses that OpenAlex misses |
| AGRIS (FAO) | used, manual only | multilingual agricultural grey literature from lower-income countries; its search sits behind a browser challenge with no API, so a person runs it in a browser and records the inspected results |
| AGRICOLA | not used | US-centred; overlaps AGRIS |
| Web of Science, Scopus, CAB Abstracts, ProQuest theses | not used | institutional and not scriptable; low marginal yield over OpenAlex and Lens for narrow practice-by-hazard questions |
| Google Scholar | not used as a search lane | used only per source during open-access recovery |

[src: methodology/search_protocol.md §Bibliographic sources]

Two features of that external protocol were not adopted: a 2015 publication floor, because effect evidence needs older drought-year trials, and a single-database recall benchmark, because the method benchmarks against frozen seed rows instead. Semantic Scholar rate-limits and is not relied on for counts. [src: methodology/search_protocol.md §Bibliographic sources] [src: methodology/search_protocol.md §Learnings from the agroforestry synthesis-first round]

## The five-step screening funnel

Screening is applied per practice and table in five fixed steps. The step names are recorded on every search row. [src: methodology/T4_generation_method.md §Screening funnel] [src: methodology/search_protocol.md §What every search logs]

1. **Frame the claim and search for syntheses first.** State the specific claim being sourced (for example, the slope above which erosion dominates for planted silvoarable agroforestry) and look for syntheses before primary studies.
2. **Source-type triage.** Authority order is synthesis, then primary, then grey. Within types the diamond classes are preferred for breadth, and primary studies are admitted for depth on a specific threshold.
3. **Relevance screen** on three dimensions: practice (does it cover this practice or family?), outcome or hazard (does it cover the variable, effect or exposure?) and system (is the agro-ecological and income context relevant?). Preference for lower- and middle-income contexts is a tie-break, not a veto on global syntheses.
4. **Credibility scoring** on six axes, producing `benchmark_tier` (below).
5. **Saturation stop and cap** (below).

Borderline papers are reviewed by people before registration to fix the study boundary; the source gives as examples rejecting urban forestry and pure physiology while accepting mechanical wind models and temperate baselines. [src: methodology/T4_generation_method.md §Screening funnel] Borderline inclusions stay as review holds rather than being decided by the screener alone. [src: .agents/skills/source-command-discover-sources/SKILL.md §Scope and coverage]

The product workflow records each inspected record with one of six dispositions: `include`, `reuse` (an existing source needed in a new scope), `exclude` (with a specific reason), `hold` (with what is uncertain and what would resolve it), `unscreened` (retrieved but not assessed) and `duplicate` (a second identity of the same work). [src: evidence:workflows/discovery/README.md §Record screening decisions]

## The six-axis credibility rubric

Each source that passes relevance is assessed on six orthogonal axes and an independence discount. [src: methodology/T4_generation_method.md §Screening funnel]

| Axis | What is judged | Recorded on SRC as |
|---|---|---|
| Evidence strength | design (RCT, quasi-experimental, observational, correlational, expert); upweight empirical validation or performance metrics such as map ROC/AUC, measured yields or verified costs | summarised in tier |
| Methodological transparency | pre-registration, data availability, reproducible code | summarised in tier |
| Authority and venue | peer-reviewed journal over institutional report over preprint over grey | `venue_type` |
| Context relevance and transferability | income group, agro-ecological zone, farming system; lower- and middle-income preference as tie-break | `study_income_group`, `aez`, `farming_system` |
| Recency | newer preferred, unless the source is seminal | `is_seminal` |
| Seminality and influence | landmark status, citation influence | `is_seminal` |
| Independence and conflict of interest | advocacy, industry-funded, promotional or single-perspective sources take a tier-down adjustment | summarised in tier |

[src: methodology/T4_generation_method.md §Screening funnel] [src: schema/spec.md §SRC]

The axes are not stored separately on every row. The audit-relevant fields are kept on the source record and the tier carries the summary. An older three-part rubric (content, impact, data quality) is one summary view of the same axes and produces the same tier. [src: methodology/T4_generation_method.md §Screening funnel]

`benchmark_tier` takes `high`, `medium`, `low` or `external`. `external` is for citation-cascade pointers that were not screened and carries zero synthesis weight. Discovery prefers high and medium sources and admits low ones only when the seed set is genuinely thin for a variable. [src: schema/spec.md §SRC] [src: methodology/T4_generation_method.md §Bounded, authority-weighted seed-set rule] A proposed tier must carry its reasons; unknown attributes remain unknown. [src: .agents/skills/source-command-discover-sources/SKILL.md §Search and screen]

How tiers become numbers in synthesis is covered in [[ch:suitability-synthesis]] and [[ch:effect-synthesis]]. Grey literature receives an additional positive-bias discount for effect claims, because practitioner and agency reports tend to overstate benefits. [src: methodology/T3_T6_generation_method.md §6. Sources]

## The saturation stop

Discovery stops adding sources when two conditions hold together: new sources add no new variables or thresholds, and tier coverage is adequate, which for shape-bearing claims means at least one high-tier and two medium-tier sources. The hard cap is about 20 sources per practice and table, lifted only with a recorded justification. [src: methodology/T4_generation_method.md §Screening funnel]

A cap, an unavailable channel or a language gap is not evidence of saturation. Each run must report why work stopped and what remains. [src: .agents/skills/source-command-discover-sources/SKILL.md §Search and screen]

## What a search record holds

Each search run writes one row to the Search Register, [[table:SRCH]], per practice, family, table, process and run. [src: methodology/search_protocol.md §What every search logs]

| Field | Content |
|---|---|
| `nbs_id`, `suitability_family_id`, `table`, `category` | the search key; empty family means the generic parent search; `category` is the process |
| `search_terms` | the exact query strings run |
| `screening_steps` | the five funnel steps applied |
| `inclusion_criteria` | what counted and what was excluded |
| `limits` | caps, for example records retrieved per query, screened and extracted |
| `n_retrieved`, `n_screened`, `n_included` | PRISMA-style counts |
| `search_date`, `run_id`, `searched_by` | when and under which run |
| `ruleset_version` | the instruction set that governed the search |
| `discovery_log_ref` | link to the narrative discovery log |

[src: methodology/search_protocol.md §What every search logs] [src: schema/structure/columns.json §SRCH]

The required fields are the search identifier, practice, table, process, search terms, date and ruleset version. The table field accepts T4, T3 and T6; the process field accepts the four processes. [src: schema/structure/columns.json §SRCH]

### The PRISMA-style counts

The counts follow the PRISMA flow in simplified form: records returned, records screened for relevance, records included. [src: methodology/T4_generation_method.md §Reproducible discovery log] They describe the bounded set actually inspected, not a search engine's approximate hit total. Unknown counts stay blank. The included count is the candidate set for that table and process before deduplication against the acquisition queue, so it can exceed the number of newly acquired sources. Zero-yield searches are recorded explicitly and do not imply saturation or extraction. [src: .agents/skills/source-command-discover-sources/SKILL.md §Agent contract] [src: methodology/search_protocol.md §What every search logs]

Within a process, the same record returned by several queries counts once. Stock reconciliation and fresh literature counts are never combined. [src: .agents/skills/source-command-discover-sources/SKILL.md §Agent contract] Counts measure search effort, not the strength of evidence.

### Narrative discovery logs

Each practice and table also has a narrative log in PRISMA-lite form: date, search strings, sources queried, counts at each stage and exclusions with reasons. The search register is the structured record; the log is its prose companion. [src: methodology/T4_generation_method.md §Reproducible discovery log] [src: methodology/search_protocol.md §How it locks together]

### Search status and the ledger

A progress ledger records, per practice, table, process and family, whether the search stage is not started, in progress or done. The build fails if the ledger claims a search is done with no matching search-register row: a search cannot be claimed without its logged protocol. [src: src/nbs_ruralscan/schema_tools/ledger.py §check] [src: methodology/search_protocol.md §How it locks together] The ledger is described in [[ch:review-and-quality]].

## Outputs of a discovery run

A discovery run produces four files, written to a staging area only, never directly to the registers. [src: .agents/skills/source-command-discover-sources/SKILL.md §Agent contract]

1. **Candidates:** each candidate's identifier, citation, URL, process, tables, families and a relevance note, with language, method subtype, proposed tier and rationale, lineage and existing source identifiers where known. Authors, years and DOIs are never invented; a candidate with missing identity stays a hold.
2. **Report:** the verbatim queries, dates, channels actually used, screening decisions and exclusions, credible omissions, stop reason and next actions.
3. **Protocols:** one object per table and process with the search terms, criteria, limits and counts.
4. **Screening record:** every inspected record's identity, disposition, reason and evidence of relevance.

A central registration step then validates scope and metadata, deduplicates by DOI, title and report identity against the Source Register and acquisition queue, records reuse of known sources for the new scope without adding duplicate votes, and writes the search rows. [src: .agents/skills/source-command-discover-sources/SKILL.md §Central closeout]

A source already registered for another practice, table or family is not discarded as a duplicate. It is tracked as a reuse task, because a paper read for suitability has not necessarily been read for effects, and its new scope needs explicit work. [src: methodology/search_protocol.md §What every search logs]

Replaying the frozen inputs reproduces the screening bundle. Re-querying a live index starts a new run and may return a different set. [src: evidence:workflows/discovery/README.md §Run a new search]

## Assumptions and limits

- **Bounded search misses things.** A capped, authority-weighted seed set trades recall for traceability. Unsearched channels (the large commercial indexes) and languages beyond the four used are recorded omissions.
- **Optimistic literature.** Searching for where a practice works finds more successes than failures. A deliberate failure and maladaptation stream is named in the method but its dedicated machinery is deferred. [src: methodology/T4_generation_method.md §Source-type register]
- **Live indexes change.** OpenAlex and Lens results drift over time; only the frozen captures are reproducible.
- **Screening judgement.** Tiers and relevance decisions involve judgement. The rubric makes the reasoning auditable; it does not make it objective.
- **Generic coverage is not targeted coverage.** A family covered only by the parent search may lack its specific literature.
- **Historical search rows** from before family-level logging are recorded at the generic level only. [src: methodology/search_protocol.md §Status]

## Where this is configured

- Search records: [[table:SRCH]]; source tiers and context: [[table:SRC]].
- Protocol: `methodology/search_protocol.md`; screening rubric: `methodology/T4_generation_method.md` §3.
- Discovery instructions: `.agents/skills/source-command-discover-sources/SKILL.md` (discovery ruleset v1.8.1).
- Narrative logs: `methodology/discovery_logs/`.
- Related chapters: [[ch:evidence-principles]], [[ch:acquisition]], [[ch:rulesets-and-learning]], [[ch:reproduce]].
