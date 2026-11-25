# Changelog

What changed in the Rural NbS Scan methodology, newest first. The build reads this file to make the
change history on "About versions and changes", and the release notes on GitHub are taken from it.

Version numbers follow `VERSION.json`: major.minor.patch. The top entry here must be the version in that
file, with the same date; the build fails otherwise. `README.md` says when each part of the number moves.

## [0.19.0] - 2026-11-25

- Show reviewed-and-kept versus total retained findings in Practices and Evidence base, from one pinned official review queue.
- Keep pending, held, rejected and broader evidence accessible, including findings with no compiled recipe row.
- Preserve earlier family scopes while source-scope review is pending; deduplicate parent totals by evidence ID.
- Add linked finding drill-downs and machine-readable coverage exports, with historical recipe outputs clearly distinguished.

## [0.18.0] - 2026-11-24

- Define explicit T2/T5 problem classes, shared concern identities and user-weighted priority scores.
- Show the classification-to-priority workflow in section 2.8, with missing data and investment risk kept distinct.
- Assess CRITIC against its published example and controlled sensitivity tests; retain it as a diagnostic.
- Separate current priority definitions from uncalibrated historical tables and index settings.

## [0.17.0] - 2026-11-24

- Introduce the data model with a linked narrative explaining the role of every table before the relationship diagram.
- Distinguish finding review, AI synthesis, scientific acceptance and runtime use, including historical outputs and unfinished synthesis routes.
- Explain where investment-risk screening sits across the tables without treating the module as a separate table.

## [0.16.1] - 2026-11-24

- Give every data-model table a full-name tooltip explaining its purpose and where the link leads.
- Name both tables in relationship hints and clarify that the lines show references, not synthesis order.
- Derive the displayed table count from the current manifest instead of retaining the retired table's count.

## [0.16.0] - 2026-11-20

- Make T3/T6 scientific synthesis AI-led, with complete candidate accounting and exact-output human acceptance.
- Retire automatic effect scoring; code validates, packages and reads accepted judgments without re-rating.
- Specify immutable proposals, stale-input holds, accepted withdrawals and runtime manifest verification.
- Preserve existing T3/T6 and T6E as historical outputs; do not retrospectively label them AI-accepted.

## [0.15.1] - 2026-11-20

- Pin the evidence workflow that retains historical T4 rows without re-synthesis.
- Retire the remaining cookbook rebuild path and obsolete T4 commands in draft guidance.
- Label older dashboard mappings as historical and point to current agent-led synthesis.

## [0.15.0] - 2026-11-20

- Retire the historical T4 compiler chapter and numeric-policy interface from current documentation; retain immutable evidence editions.
- Describe T4 baseline retention and the outstanding agent proposal/acceptance implementation.
- Distinguish the recorded T4 decision from the intended, still unimplemented AI-led T3/T6 workflow.

## [0.14.4] - 2026-11-20

- Repair data-model references and clarify which Git edition identifies the specification.
- Expose the exact confidence matrix and badge lookup with hashes and immutable origins.
- Clarify six-hazard weight completeness, pinned register ownership and retained versus reviewed evidence.
- Explain the legacy knowledge-basis spelling without changing claims, weights or analytical outputs.

## [0.14.3] - 2026-11-20

- Move NBS Invest from the header to the footer and add the official Alliance logo alongside it.
- Keep one Review queue link in the header and remove its duplicate from the version bar.
- Rename the page-feedback control to Comment on this page, keeping it distinct from evidence-review decisions.
- Analytical values and the evidence-base edition are unchanged.

## [0.14.2] - 2026-11-20

- Reuse the GitHub organisation's NBS Rural Scan logo and scoping tagline in the site header, with its original source recorded.
- Keep the programme credit, theme controls and linked version information alongside the project branding.
- Remove the repeated standalone Methodology label beside the linked methodology version.
- Analytical values and the evidence-base edition are unchanged.

## [0.14.1] - 2026-11-20

- Bring version explanations, full change history, source revisions and feedback together on About versions and changes.
- Link the methodology and evidence-base version numbers directly to their explanations; remove separate header links for version help and change history.
- Preserve older change-history links and version anchors; analytical values and the evidence-base edition are unchanged.

## [0.14.0] - 2026-11-20

- Shorten the method chapters and give shared explanations one home, with links to the detailed evidence methods.
- Remove superseded weighting routines, R-port descriptions and repeated development-status inventories from the method narrative.
- Explain dataset selection without presenting the historical registry as the current pilot dataset list.
- Refocus the application chapter on the scoping brief, reproducibility and interpretation of partial results.
- Preserve evidence provenance, scientific limits and numbered table and figure captions; analytical tables and the evidence edition are unchanged.

## [0.13.0] - 2026-11-19

- Add a title-based citation with the edition, URL and existing team credit.
- Reconcile registered, retained and dropped finding counts across practice summaries and evidence downloads.
- Distinguish automated/AI quality checks on every extracted item from separately recorded human review.
- Replace ambiguous empty-output labels and explain that zero compiled rows does not mean no evidence.
- Separate the excluded rooftop-harvesting record from the land-based practice table while retaining its provenance.

## [0.12.0] - 2026-11-19

- Add labelled worked illustrations across the evidence workflow, including shared origins, conflicting effects and incomparable costs; keep linked example headings clear of the sticky navigation.
- Give shared appraisal and dependence guidance one home; remove repeated band and comparator tables from extraction.
- Correct contradictions about agent-led T4 synthesis, species scope, current review submission and historical compiler behaviour.
- Clarify confidence conventions, non-significant results, incomplete independence checks and the limits of unharmonised cost figures.
- Preserve the pinned analytical outputs and numerical policies; examples are explanatory, not new evidence or calibration.

## [0.11.0] - 2026-11-19

- Describe agent-led T4 synthesis separately from deterministic validation, packaging and runtime evaluation.
- Move the earlier T4 filtering and weighting algorithms into a clearly labelled historical reproduction chapter.
- Number and caption every table and figure, with a build check enforcing the requirement across generated pages.

## [0.10.0] - 2026-11-19

- Integrate source appraisal into the opening evidence chapter and place shared synthesis guidance after review.
- Explain distinct evidence requirements for suitability, hazard and scorecard effects, economic profiles, datasets, priorities and context.
- Consolidate repeated registry and weighting explanations; keep detailed algorithms in their table-specific chapters.
- Clarify dependence controls and literature-derived expert judgement across the existing chapters.
- Preserve links to the earlier guides while directing readers to their integrated locations.

## [0.9.0] - 2026-11-19

- Explain evidence registry fields, source limitations and literature-derived expert judgement.
- Separate knowledge basis from extraction format while preserving historical compiler inputs.
- Add guidance on combining T4 evidence, source and author-group dependencies, weighting and uncertainty.

## [0.8.2] - 2026-11-18

- On the overview, the table of what is settled no longer describes suitability scores as under
  review. It says that no suitability rule has an approved numerical score, what the method can
  and cannot do as a result, and that the scores are left for the planned move of compiling to an
  AI agent. Counts that were not about review are removed from that row.

## [0.8.1] - 2026-11-18

- The version line at the top of each page no longer breaks in the middle of a phrase when the
  window is narrow. It gives the two numbers and leaves the date to the version menu above it.

## [0.8.0] - 2026-11-18

- Version numbers start here. The methodology carries a version number and the evidence base it
  reports carries a release number. Both are shown at the top of every page and explained under
  Editions and checks.
- New chapter in Evidence methods: Compiling evidence into rule tables. It says where compiling
  sits, how it is run today, and that a move to an AI agent is planned and not yet in use. The
  three chapters after it move down one number.
- On the overview, “How the method was built” is now plain text, and “What is settled, and what is
  not” is a table.
- Fourteen lists of a bold phrase followed by a sentence became plain tables or plain text, among
  them the neighbouring-practice boundaries on the practice pages. No rule changed.
- Numbered steps no longer open with a bold phrase: the number already leads.
- The Evidence methods part opens with a figure of its five steps: what happens, who does it and
  what each step leaves. Chapter tables no longer show word counts.

## Before version numbers

Entries from before this methodology carried a version number, by date.

### 17 November 2026, after the first review round

- After the first review round, the overview was rewritten as one story: the problem, what the
  method does about it, who it is for, how it works, and what is settled. Its sections are
  numbered.
- One figure now shows the whole method: how evidence becomes rules, then the seven stages that
  apply them.
- Counts of practices and evidence moved to the Practices part. The worked example moved to the
  Evidence base part and now follows a terrace slope rule.
- The name is now “Methodology”. Module chapters are titled in one style.
- Two chapters on operating the evidence base (continuing the work with an AI system, and
  versioning the instructions) are no longer published, to shorten the text. They remain in the
  repository.
- After a second review round, the overview lists its sections in the side bar, a plain table
  replaces the two boxes on who the method is for, the visual methodology is linked beside the
  figure instead of in its own section, and links that leave the site open in a new tab.

### 17 November 2026

- Listed in the site’s version menu under “Under review”. The menu on these pages now has the same
  three groups as the live dashboard: Live, Under review and Earlier drafts.
- The help page names the project contacts and team.

### 16 November 2026

- Front page rebuilt: the practices covered, how much evidence each has, and the method told as
  seven questions.
- The methodology takes the live evidence dashboard’s look, and that house style is recorded and
  checked by the build.
- One top bar shared with the visual methodology: version menu, theme switch, review tool and
  change history. Programme logo and a help page added.
- The chapter on continuing the evidence base with an AI system now describes the routes for
  recording work in the evidence and method repositories.
- Published at an address that is not yet listed, with a request to search engines not to index it.

### 14 November 2026

- Evidence base rebuilt for use: downloads of every table, a field guide, and queries that the
  build runs.
- New chapter: continue the evidence base with an AI system.
- Review page updated: finding reviews are submitted from the live dashboard and recorded in the
  evidence repository.

### 12 November 2026

- Added the scoping walkthrough, which follows the visual methodology stage by stage, and the
  chapter on implementing the method.

### 11 November 2026

- First build: the method by module, the evidence methods, the data model, every practice and every
  compiled row.
