# Methodology feedback response — 20 November 2026

Target edition: **0.14.0 (draft)**. Editorial consolidation of the Method section; no analytical table, evidence record, release pin or runtime algorithm changes. Source review: 15 exported notes plus the accompanying message. The export identifies several paragraphs only as `p` or `li`, without quoting the selection; this response addresses their chapter-level concerns without claiming a more precise anchor.

## Response to the 15 notes

| Note | Concern | Response |
|---|---|---|
| 1 | Overview is too technical | Replace software architecture and repeated procedural detail with the decision sequence and common principles. |
| 2 | Obsolete script reference in overview | Remove inherited R/NumPy and MCDA primitive material. |
| 3 | M1 reads as a catalogue of mistakes | State the governing rules directly; retain limits that affect interpretation and put unresolved reconciliation below. |
| 4 | M1 relies on the old R/MCDA method | Remove the inherited function catalogue and AHP/CRITIC/entropy derivation. |
| 5 | M1 describes a method no longer used | Remove inherited perturbation defaults and automatic quartile/top-half selection; require the application's recorded policy and class boundary. Retain the weighted-sum semantics actually used by the current approved first pass. |
| 6 | Dataset list is outdated | Replace the apparent current-input list with selection criteria and an explicit distinction between the published edition and actual pilot inputs. Updating dataset records is a separate evidence/configuration change. |
| 7 | Server-side sourcing is repeated | Keep its explanation in Farming systems, contexts and data; link there from the overview. |
| 8 | M2 highlights unfinished work | Remove development inventories and speculative composition equations. Keep proxy and baseline/future comparability qualifications needed to interpret an application. |
| 9 | M3 highlights unfinished work | Replace implementation/manifest inventories with the characterisation workflow, data support and interpretation limits. |
| 10 | M4 contains obsolete specifics | Remove inherited weighting code, unapproved encoding formulas and perturbation defaults; focus on recorded priorities, weights, drivers and sensitivity. |
| 11 | M4 limits are a development backlog | Replace with genuine limits: relative ranks, ordinal weight conventions, correlated concerns, data gaps and field validation. |
| 12 | M5 cites an obsolete implementation as current | Refocus on interpreting T3/T6/T6E; remove the old scorecard implementation inventory and duplicated display algorithms. Detailed evidence synthesis retains its own chapter. |
| 13 | M6 highlights unfinished work | Remove draft task lists and function-signature status; retain feasibility, safeguard, sensitive-data and uncertainty requirements. |
| 14 | Implementation chapter reads as developer instructions | Rewrite as Applying and reporting a country scan: scope, provenance, output meaning and the scoping brief. Link software instructions to the runtime. |
| 15 | Runtime-status section does not belong in the method | Remove that section and the component-by-component implementation inventory. State specification versus actual application once in the application chapter. |

The visual walkthrough's large design-difference table and missing-feature inventories are also removed; its example-only status remains prominent. Inherited primitive attribution blocks are removed from the active practice pages and historical compiler vocabulary table, where they falsely suggested continued use of the old weighting scheme. Original source history and citations are retained.

## Runtime cross-check

Inspected RuralScan/runtime main at `9d8acd5980822e4c455411510911cdf494078f24`. Its README still scopes the spatial application to the planted-silvoarable first pass: a partial terrain-and-soil index. `src/nbs_runtime/aggregate.py` combines selected criteria by the approved weights, preserves excluded/unknown/scored states, and keeps host fraction separate. No AHP, CRITIC, entropy or `spatMCDA` reference was found in its source, notebooks, design notes or README.

Since the previously cited `e690d4e` version, runtime main contains boundary-loading, baseline-result naming and environment/data-handling changes. This PR therefore removes stale detailed runtime claims rather than substituting another implementation inventory into the method. Runtime code and its working checkout are unchanged.

## Reconciliation remaining before final hand-off

- Confirm the actual pilot dataset inventory and register versions, bands, units, depths, dates and context-specific bindings. Historical T1/BIND/T7 records are not silently updated by prose.
- Confirm the current M1 selection, class boundaries, aggregation and sensitivity policies beyond the existing first pass. Removing old algorithms does not approve replacements.
- Reconcile M2 hazard metrics, baseline/future comparability, exposure composition, mode flags and any combined-risk calculation against the actual implementation. The public chapter retains the input-comparability constraint.
- Reconcile M3/T5 indicator definitions and reference frames, including missing ontology fields and production-gap inputs. M4's actual weighting, classification and ranking conventions must be recorded with pilot results.
- Reconcile M2b composition, establishment-period treatment and operational flag thresholds against the implemented screen. Do not infer an approved composite from the old draft equations.
- Keep the evidence edition, runtime scoring package and pilot run revisions distinct; validate claims of executed or locally validated modules from run evidence.
- The historical visual prototype still contains illustrative settings. It remains labelled as a design aid with synthetic examples, not an executable specification or source of analytical values.

These are follow-up reconciliation tasks, not claims of completed validation. Removed development details remain recoverable from the prior Git revision. No review note is marked resolved in the source system and no message is sent to the reviewer.

## Validation and size

Across the 12 Method chapters, prose excluding source-citation markup falls from 37,876 to 16,481 words (56.5%). Specialist Evidence methods remain intact apart from removal of the obsolete inheritance block in the historical compiler chapter. Shared explanations have one owning chapter.

The full local build generated 1,630 pages and passed all 31 checks, including source/row provenance, internal links and anchors, balanced markup, package equality, names, and one numbered descriptive caption for every table and figure. The three caption-enforcement tests passed. Version and changelog advance together from 0.13.0 to 0.14.0. Public analytical records and evidence-edition identifiers are unchanged.
