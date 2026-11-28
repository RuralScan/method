# Issue 76 reconciliation — 27 November 2026

Reviewed all 15 notes in [method issue 76](https://github.com/RuralScan/method/issues/76) and the additional request for shorter, less technical prose. Source baseline: merged method `6ca13a2d9671ce436e0c18bd4ca0f48595f2b9e7` (v0.30.0). Earlier responses are preserved in [the first editorial response](method-feedback-2026-11-20.md) and [the plain-language follow-up](plain-language-2026-11-26.md).

Most exported selections identify only `p` or `li` and do not quote the selected text. Dispositions below therefore address the chapter-level concern; they do not claim exact deleted selections or reviewer endorsement. “Addressed” means the current wording answers that concern, not that scientific calibration or a pilot application is complete.

## Disposition of each note

| Note | Concern | Verified response and disposition |
|---|---|---|
| 1 | Overview is too technical | **Addressed earlier.** [Scope](../content/scope-and-framework.md#how-the-analysis-fits-together) starts with the decision sequence and module outputs; software architecture is absent. |
| 2 | Overview cites an obsolete script | **Addressed earlier.** No R/NumPy or inherited primitive catalogue remains in the overview. Source history remains available without presenting it as the current implementation. |
| 3 | M1 reads as a catalogue of mistakes | **Addressed earlier.** [M1 method](../content/m1-suitability.md#method) states gates, accepted responses, spatial states and reporting requirements directly. Calibration holds remain because they change what a score can mean. |
| 4 | M1 relies on the old R/MCDA method | **Addressed earlier.** The inherited function and automatic-weighting catalogue is removed. The conditional weighted-sum explanation cites the recorded first-pass policy; its presence does not reinstate the old software method. |
| 5 | M1 describes a method no longer used | **Addressed at chapter level earlier.** Unapproved perturbation defaults, quartile/top-half selection and automatic weighting are absent. M1 requires the accepted response and recorded run policy; pending overrides remain inactive. The export is insufficient to identify a narrower selected passage. |
| 6 | Dataset table is outdated | **Addressed earlier; navigation completed here.** [Data selection](../content/farming-systems-and-data.md#choose-data-by-fitness-for-purpose) replaces the apparent current dataset list with fitness criteria and an explicit historical-edition label. New links lead to newer research and binding assessments, without calling them an adopted pilot inventory. M3 now reflects the separately recorded acute IPC interpretation approval. |
| 7 | Server-side sourcing is repeated | **Addressed earlier.** [Sourcing](../content/farming-systems-and-data.md#server-side-first-sourcing) has one explanatory home. The overview links to data selection instead of repeating the sourcing sequence. |
| 8 | M2 lists unfinished work | **Completed here.** [M2 inputs](../content/m2-climate-risk.md#inputs) now states selection requirements instead of an eleven-entry readiness inventory. [Scenario comparison](../content/m2-climate-risk.md#4-compare-baseline-and-future-conditions-consistently) explains metric incompatibility directly. The registry retains its detailed holds. |
| 9 | M3 lists unfinished work | **Addressed earlier.** [M3](../content/m3-characterisation.md) explains classification, overlap and summaries. Dataset qualifications concern actual interpretability, coverage and adoption status; they are not an engineering task list. The stale acute-food proposal label is corrected here without asserting a released binding. |
| 10 | M4 includes obsolete or excessive detail | **Addressed earlier; tightened here.** [M4](../content/m4-hotspots.md#method) uses the current priority contract and explicit user weights. The CRITIC paragraph now explains the diagnostic role and implications; implementation tests remain in the linked assessment. |
| 11 | M4 limits are a development backlog | **Addressed earlier.** [Limits](../content/m4-hotspots.md#assumptions-and-limits) concern weight conventions, reference frames, correlations, missing data and local validation. These affect interpretation and remain. |
| 12 | M5 presents retired code as current | **Addressed earlier.** [M5](../content/m5-scorecard.md#method) explains effects, applicability, disagreement and indicative costs; the old implementation inventory is absent. Detailed synthesis is linked from its owning chapters. |
| 13 | M6 lists unfinished work | **Addressed earlier.** [M6](../content/m6-handoff.md#method) specifies field assessment, consultation and feasibility outputs. Missing evidence and safeguards remain material hand-off questions, not software tasks. |
| 14 | Implementation chapter reads as developer instructions | **Addressed earlier.** [Applying and reporting a country scan](../content/implementing-the-method.md) is organised around a scoping brief and defensible conclusions. Setup and developer instructions are linked elsewhere. |
| 15 | Remove the runtime-status section | **Addressed earlier.** The old section and component inventory are absent. Application reporting retains one explicit distinction between specified methods and analyses actually executed. |

## Additional plain-language comment

The first pass removed repeated implementation catalogues; the second shortened setup, investment risk, hand-off and the walkthrough. This pass avoids another broad rewrite. Across the same 12 Method chapters, a reproducible whitespace-word count is **39,441 before the first pass versus 12,859 now: 67.4% shorter**, including later scientific explanations. Count headings and tables; exclude front matter, `[src: …]` tokens and Markdown URL targets. This counting convention differs from the older audit's totals; do not combine them. Baseline: `ad024fa4267bda7275b90b5d5b5e24cffd3e1fac`.

## Current-status correction

The acute IPC class interpretation was approved in merged `c625db11e6bc22fde60230d35470e510daf06e97`, separately from the v0.30 source branch. [The recorded approval](../../priority/research/2026-11-27-food-insecurity-approved.md) now supplies M3's status. Native phases, the mandatory Phase 5 critical flag and the separate risk-of-famine flag survive. Geometry, accepted spatial binding and runtime release remain unresolved. No approval event or class file is changed here.

## Verification and closure boundary

This is an editorial patch (v0.30.1): four chapters, version/changelog and this response. Numerical contracts, priority research, evidence pins, decisions and runtime are unchanged. The 1,639-page local reference build passes every executed check, including provenance, links and captions; three caption tests pass. All pre-existing rendered anchors in the four edited chapters survive against v0.30.0, and pending-override JSON is byte-identical. The private names list was unavailable locally, so the attribution check was skipped and the preview is not for publication. Publication uses a separate reviewed gh-pages pin and requires that check in CI.

Keep issue 76 open while these residual corrections and publication await merge. After both are merged and the selected edition is live, the editorial issue can close. Its closure must not imply approval of other scientific choices, source rights, dataset bindings or runtime work. Those remain with their existing workstreams. Original issue notes and comment are preserved.
