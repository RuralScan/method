---
title: Acquiring and verifying sources
slug: acquisition
summary: Turn a screened candidate into a verified, cached, team-accessible artefact with the right identity and locator rules, or record exactly why it is on hold.
sources:
  - methodology/search_protocol.md
  - methodology/access_policy.md
  - methodology/T4_generation_method.md
  - methodology/RULESET_VERSIONS.md
  - src/nbs_ruralscan/schema_tools/verify_metadata.py
  - src/nbs_ruralscan/schema_tools/validate_sources.py
  - src/nbs_ruralscan/ingest/github.py
  - schema/spec.md
  - schema/structure/columns.json
  - .agents/skills/source-command-extract-evidence/SKILL.md
  - .agents/skills/source-command-extract-evidence/references/defects.md
  - AGENTS.md
  - evidence:workflows/acquisition/README.md
---

## What acquisition must deliver

Between screening and extraction sits one question: *is the file in hand the work that was screened, and can everyone on the team open the same file at the same place?* Acquisition answers it. It produces, for each eligible source:

1. a verified bibliographic identity (DOI round-trip or title check),
2. a cached artefact in the local corpus that the provenance validator can read,
3. a team-accessible copy (a shared-library path for documents, or a URL and snapshot for web and code sources), and
4. a locator convention that later extraction will use for every quote.

[src: AGENTS.md §What is locked] [src: src/nbs_ruralscan/schema_tools/validate_sources.py §module docstring]

The method treats acquisition as a gate, not a convenience. A source that cannot be cached cannot be registered, and extraction refuses a source whose identity has not been verified. [src: AGENTS.md §Don't] [src: src/nbs_ruralscan/schema_tools/verify_metadata.py §module docstring]

## Open-access recovery before "paywalled"

A source may be labelled paywalled only when no free copy of the same work has been found after a defined recovery pass. A single failed download, or a bibliographic database reporting the work as closed, is not proof. Over-labelling sources as paywalled pushes needless institutional-access work onto the people acquiring them. [src: methodology/search_protocol.md §OA-recovery]

The recovery pass has four steps, run in order. [src: methodology/search_protocol.md §OA-recovery]

1. **Unpaywall by DOI.** If Unpaywall reports the work as open access, its best open location is taken. This is a browser or repository acquisition, not an institutional one. Unpaywall is treated as authoritative over OpenAlex's open-access flag, which lags and misses green open access.
2. **Web search for each source (required).** Search the distinctive title with the first author and year. Accept only a free, directly downloadable copy of the *same* paper (matching title, authors and year) from author or institutional repositories, agency repositories, project sites, publisher open-access pages or regional platforms. Reject "request PDF" stubs, abstract pages and related but different papers.
3. **Green open access, preprints and open data.** Check subject and institutional repositories, author postprints, preprint servers and open data deposits, even when the article itself is closed.
4. **ResearchGate and Academia.** These block automated access, so a tool can never confirm or deny a copy there. They are flagged for a person to check; the method never records "not on ResearchGate" from a tool.

Only a source that survives steps 1 to 3 is routed for institutional access. [src: methodology/search_protocol.md §OA-recovery]

The second step carries most of the yield. In one recovery pass over a 227-source queue, about half the sources (111) were found freely available, of which only 23 had been caught by Unpaywall; the rest surfaced only through web search. [src: methodology/search_protocol.md §OA-recovery] A later pass found that most failures previously recorded as "paywalled" were bot walls, not paywalls: content-delivery challenges on major publishers and repositories, repository software exposing files only through specific API paths, and dead links with archived captures. The rule that followed is that a human hand-off list is never built from earlier failure notes; the recovery pass is run first and the residue is sorted into free-click, institutional and ResearchGate buckets. [src: methodology/search_protocol.md §OA-recovery pass]

Access status is then recorded on the source as `open_access`, `paywalled` or `unknown`, verified against Unpaywall by DOI, with the licence. Access status governs what may be shared (short quotes for all; never redistribution of paywalled files), not whether a source may be used as evidence. [src: methodology/access_policy.md §What can be shared] [src: schema/structure/columns.json §SRC]

## Bibliographic identity

### DOI to citation round trip

Discovery assembles DOIs and citations from search results, and a mis-stitched DOI resolves to a different paper. A wrong DOI would fetch the wrong PDF, and every quote extracted from it would be real text attributed to the wrong work. [src: src/nbs_ruralscan/schema_tools/verify_metadata.py §module docstring]

The method therefore round-trips every DOI through Crossref before acquisition: [src: src/nbs_ruralscan/schema_tools/verify_metadata.py §module docstring]

1. resolve the DOI;
2. compare the resolved title with the citation's title by token overlap against a threshold;
3. if they match, stamp `doi_verified = true` and rebuild the citation from the authoritative Crossref record (which also corrects wrong author lists);
4. if they do not match, or the DOI is dead, clear the DOI and acquire the work by title.

An offline check runs in every build and in continuous integration: any queued source with a DOI that is not verified fails the check. [src: src/nbs_ruralscan/schema_tools/verify_metadata.py §module docstring]

The trust anchor is the title, not the DOI. A DOI recovered automatically by title search is only a candidate for a person to verify, because title search itself can mis-match. [src: AGENTS.md §What is locked] A temporary network failure does not count as a mismatch; the DOI stays available for retry. [src: methodology/RULESET_VERSIONS.md §v1.6.11] [src: evidence:workflows/acquisition/README.md §Bibliographic identity and access]

This lock was introduced after an audit found about 44 queue rows whose correct title had been joined to a wrong author or DOI, with six DOIs resolving to a different or dead paper. [src: AGENTS.md §What is locked]

### Title verification for sources without a DOI

Grey literature, agency manuals and practice-database sheets often have no DOI. For these the method checks the file itself: the citation's title must appear in the opening pages of the cached artefact, with token coverage of at least 0.8, and the result is stamped as `title_verified`. The artefact must also have been downloaded from the publisher's own domain, which is recorded with the source URL and checked at review. [src: methodology/RULESET_VERSIONS.md §v1.6.0] [src: src/nbs_ruralscan/schema_tools/verify_metadata.py §module docstring]

On its first run this check caught two wrong documents: a practice-database endpoint serving a different technology sheet, and a later paper cached under the name of an earlier wetland source. [src: methodology/RULESET_VERSIONS.md §v1.6.0]

### Metadata identity is not artefact identity

A verified DOI proves that the citation and the DOI agree. It does not prove that the downloaded PDF is that paper. New PDF intake, source promotion and staging therefore also require an opening-title match against the artefact. Wrong documents, scans whose titles cannot be read, and chapter titles found only in the body of a larger document stay as identity holds; they are never relabelled as paywalled. A title found only in the body may be a bibliography entry, so a whole PDF is never marked verified because it cites the wanted paper. [src: .agents/skills/source-command-extract-evidence/references/defects.md §Adversarial pipeline checks] [src: .agents/skills/source-command-extract-evidence/references/defects.md §Pipeline integrity (v1.7.0)]

### The extraction gate

Extraction may proceed on a source only if `doi_verified = true`, or if the source has no DOI and `title_verified = true`. [src: src/nbs_ruralscan/schema_tools/verify_metadata.py §module docstring] [src: .agents/skills/source-command-extract-evidence/SKILL.md §Source and coverage checks]

## Cached artefacts and team access

Every registered source has two kinds of copy.

- **The local cache.** A file in the corpus directory named by `source_id`: a PDF, or a `.txt`, `.html` or `.md` snapshot. The provenance validator reads this copy. An unknown file extension in the cache is a hard failure. The cache is never committed to the public repository. [src: src/nbs_ruralscan/schema_tools/validate_sources.py §module docstring] [src: AGENTS.md §What is locked] [src: methodology/access_policy.md §Standing rules]
- **The team copy.** Evidence must be acquirable by the whole team, not only on the machine that found it. A PDF is uploaded to the shared source library and its path is recorded in `SRC.library_path`. A website or repository has `SRC.url` set and a snapshot saved. Missing library paths, URLs or locators are reported as notes by the source validator. [src: AGENTS.md §What is locked]

The source record also carries the artefact hash (`artifact_sha1`), retrieval time and source kind, so that a later change in the file is detectable. [src: schema/structure/columns.json §SRC] A changed transcript or rendering produces a new hash and requires re-emission of the evidence, never hand editing. [src: methodology/search_protocol.md §WOCAT technology sheets]

## Locator rules by format

A locator says where in the artefact a quote sits. Four locator types are permitted: `page`, `section`, `char_span` and `file_line`. [src: schema/structure/columns.json §EV]

| Format | Artefact of record | Locator | Identity check |
|---|---|---|---|
| Native PDF | the PDF | `page` (the quote must be on that page) | DOI round trip or title in opening pages |
| Scanned PDF | the PDF with an added OCR text layer | `page` of the scan | as PDF; sample of quotes checked against page images |
| Word document | the master `.docx` plus a PDF rendered once | `page` of the rendered PDF | title in the rendered PDF |
| Web page | saved snapshot (`.txt`, `.html` or `.md`) with URL | `section`, anchor or selector | page title or opening heading |
| Practice-database questionnaire (WOCAT) | PDF export plus a deterministic transcript of the embedded questionnaire | `page` for the PDF; `section` as `questionnaire_group/field` for the transcript | title; publisher endpoint |
| Code repository | source files at a pinned commit | `file_line`, `path:Lstart-Lend`, plus `commit_sha` | repository, commit and path |

[src: methodology/search_protocol.md §Scanned PDFs (no text layer)] [src: methodology/search_protocol.md §Word documents (.docx)] [src: methodology/search_protocol.md §WOCAT technology sheets] [src: AGENTS.md §Don't] [src: evidence:workflows/acquisition/README.md §Bibliographic identity and access]

### PDF pages

The PDF is the most common artefact. Its text layer is indexed once, with every passage keeping its page number, and tables and figures indexed as their own nodes with captions and pages. Quotes are later sliced from this text layer, so page locators are exact by construction. [src: methodology/T4_generation_method.md §5.1 Document ingestion]

### Scanned PDFs

A scan has page images but no text, so no quote can be sliced from it. The rule is: [src: methodology/search_protocol.md §Scanned PDFs (no text layer)]

1. Run optical character recognition once and never again. Each image-only page is rendered at 300 dpi and an invisible text layer is added beneath the image; pages that already carry text are copied unchanged.
2. The OCR'd file is the artefact of record; the original scan is kept untouched beside it. Page locators match the scan's pages.
3. Quotes are sliced from the OCR text like any PDF. OCR errors therefore sit visibly inside the quote. A garbled or out-of-order passage (two-column pages) is a blocker, never retyped or stitched.
4. Every unit from such a source carries a flag that its text is OCR-derived. Before any is approved, a person checks a sample of its quotes against the page images: at least three per source or a fifth of its units, whichever is larger.

### Word documents

A `.docx` has no stable pages, so quotes cannot be verified against it directly. [src: methodology/search_protocol.md §Word documents (.docx)]

1. The master `.docx` is kept unchanged in the library beside its rendering.
2. The artefact of record is a PDF rendered once with a headless office suite; the renderer and version are recorded with the PDF's hash.
3. Locators are pages of the rendered PDF.
4. The document is never re-rendered after extraction, because a new rendering can re-flow pages and orphan every locator. A changed master becomes a new source.
5. The title check runs on the rendered PDF. A published PDF of the same document, when it appears, supersedes the rendering as a new source row.

Internal authorship of a document is recorded so that the independence axis of the credibility rubric can be applied.

### Web snapshots

A web source needs a URL, a saved snapshot and, for every evidence unit, a locator saying where on the page the quote came from: a section heading, an anchor or a selector. A bare domain link is not provenance. [src: AGENTS.md §What is locked] [src: AGENTS.md §Don't]

### Practice-database questionnaires

A WOCAT technology entry is two artefacts under one source identifier. The PDF export carries page locators and is the artefact for suitability units. A transcript rendered deterministically from the embedded questionnaire data carries section locators (`questionnaire_group/field`, for example `impacts_ecological_soil/soil_loss`) and is the artefact for effect and asset-vulnerability units; each quote is a transcript line. [src: methodology/search_protocol.md §WOCAT technology sheets]

The adapter's rendering and its value-to-direction and coping-to-hazard mappings are unit-tested. Cost totals in the transcript are computed exactly as WOCAT's own export computes them, using the sheet's own exchange rate and calculation base, and are cross-checked against the PDF export's printed USD total; a mismatch above 2 % is reported and not ingested. Sheets with no calculation base or exchange rate emit no cost unit. [src: methodology/search_protocol.md §WOCAT technology sheets] The PDF must be taken from WOCAT's own database export, because a legacy endpoint uses a different identifier scheme and returns the wrong sheet. [src: .agents/skills/source-command-extract-evidence/references/defects.md §Common extraction defects]

### Code at a pinned commit

Tools are interrogated through their code, not their README. A dedicated adapter fetches each source file at a fixed commit, caches it with a provenance sidecar (repository, commit, path, hash) and scans for lines that look like hard-coded parameters (weights, thresholds, reclassification tables, masks, buffer distances, land-cover gates), each with its file and line. Pinning the commit makes a `file_line` locator immutable. [src: src/nbs_ruralscan/ingest/github.py §module docstring]

The adapter does not decide which candidate line maps to which variable or family. That judgement, which includes the practice-in-source and scope tests, stays with the extractor and then passes the central guardrail. Blind automatic emission would repeat mis-mapping at scale. Species-specific scripts (for example per-species growth models) are skipped as species envelopes rather than practice rules. [src: src/nbs_ruralscan/ingest/github.py §module docstring] [src: AGENTS.md §Don't] Code sources must resolve to immutable commits, with distinct identities per repository, path and revision. [src: .agents/skills/source-command-extract-evidence/references/defects.md §Pipeline integrity (v1.7.0)]

## Formats with no rule are paused

When a source arrives in a format with no handling rule, acquisition stops. The missing pieces are defined first: an acquisition adapter, locator semantics and a quality check. Nothing from that format is registered until they exist. The method does not improvise by forcing a new format into an existing rule. [src: AGENTS.md §What is locked]

Datasets (CSV, spreadsheets, R objects) remain paused. A dataset has no verbatim-page semantics. The intended adapter would treat a dataset as `source_kind = dataset`, store a snapshot and hash, use `table_row` locators with the serialised row as the quote, and link each row to its primary study's DOI through lineage. Until it exists, a dataset is used only as a discovery seed list: its DOIs enter the acquisition queue and the primary studies are extracted from their own documents. [src: methodology/search_protocol.md §Datasets (.csv / .xlsx / R)]

## What makes a source ineligible

A screened candidate does not become an extractable source if any of the following holds.

- **No verified identity.** The DOI failed the round trip and the title could not be confirmed in the artefact, or the artefact's opening title does not match. [src: src/nbs_ruralscan/schema_tools/verify_metadata.py §module docstring] [src: .agents/skills/source-command-extract-evidence/references/defects.md §Adversarial pipeline checks]
- **No artefact the team can open.** No copy can be cached, or no library path or URL and snapshot can be recorded. [src: AGENTS.md §Don't]
- **Unsupported format.** A dataset or any other format without an approved adapter. [src: methodology/search_protocol.md §Datasets (.csv / .xlsx / R)]
- **Wrong publisher route** for a DOI-less source. [src: src/nbs_ruralscan/schema_tools/verify_metadata.py §module docstring]
- **Unreadable text** that cannot be OCR'd into a usable layer, or text whose reading order makes the claim unquotable. [src: methodology/search_protocol.md §Scanned PDFs (no text layer)]

Ineligibility is recorded as a hold with its reason, not as a silent removal. Acquired is also not extracted: a newly promoted source starts as `pending` and reaches `swept` only when an inventory accounts for its relevant pages, tables, figures and supplements. [src: .agents/skills/source-command-extract-evidence/references/defects.md §Pipeline integrity (v1.7.0)] [src: schema/spec.md §SRC]

## Assumptions and limits

- **Recovery is bounded.** The open-access pass reduces but does not remove access bias. Sources behind institutional access may remain unacquired, and the evidence base can under-represent them.
- **Title matching has thresholds.** Token-overlap checks can miss a correct match with a garbled title or pass a near-identical companion paper. Holds and human checks catch some of these, not all.
- **Editions differ.** Page locators bind to the specific file hashed at acquisition. A different edition of the same work requires re-slicing and new page locators.
- **OCR quality varies.** Verified quotes from OCR text prove agreement with the OCR layer, not with the printed page; the human sample check is what links them.
- **Datasets are excluded for now,** so meta-datasets and open data that carry rich effect or cost information enter only through their primary studies.

## Where this is configured

- Source identity, access and artefact fields: [[table:SRC]]; locator fields on [[table:EV]]; tool metadata on [[table:TOOL]].
- Recovery, format and locator rules: `methodology/search_protocol.md`.
- Sharing policy: `methodology/access_policy.md`.
- Identity gate: `src/nbs_ruralscan/schema_tools/verify_metadata.py`; provenance guardrail: `src/nbs_ruralscan/schema_tools/validate_sources.py`; code adapter: `src/nbs_ruralscan/ingest/github.py`.
- Related chapters: [[ch:discovery]], [[ch:extraction]], [[ch:evidence-principles]].
