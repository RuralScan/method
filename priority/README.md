# Classify problems and weight priorities

[Machine-readable contract](../data-model/priority-contract.json). This is the current T2/T5 priority interface. The CSVs in `data-model/configuration/` and their frozen definition snapshot retain historical inputs; their old normalization, default-weight and climate-mode fields do not supply defaults to this route. Adopting the new contract does not calibrate those historical variables or change any evidence finding.

The [current T2 registry](t2/README.md) preserves all eleven IDs with explicit candidate data and readiness blockers. Its historical CSV remains available for reproduction. T2 is a registry of climate-risk variables. There is no combined Climate Risk Index or Mode A/B calculation in this route. T5 identifies priorities and descriptors. Each selected variable refers to one classification rule and a shared `concern_id`. The same climate concern appearing in both registries must enter the stack once. M2b investment risk remains a separate screen.

## Classification

Retain raw values and units. Class scores are **none 0, low 0.33, medium 0.66, high 1**. These are ordinal decision conventions, not probabilities or estimated benefits. A high score means more of the selected concern. Benefit, potential and safeguard indicators still need their own explicit interpretation; a label cannot supply it.

Thresholds are the default. Specify three strictly increasing cutoffs in native units. Every cutoff is an upper bound included in the lower raw-value interval. With higher values meaning more concern, the four intervals receive none, low, medium, high. Reverse the labels when lower values mean more concern. Record exact units, context, version and justification. Values outside a dataset's valid domain must be supplied as missing by the dataset adapter, not forced into a class.

Terciles are an explicit relative alternative. Supply and identify a separate reference sample, with its area/population and period. Calculate its one-third and two-thirds quantiles using linear interpolation at `(n - 1) * q`; save sample hash, sample count and realized cutoffs. Apply these fixed cutoffs to comparison periods, rather than recalculating them for every map. Remove missing values and any explicitly defined no-problem observations before fitting. With no defensible no-problem condition, use only low, medium and high; never make the lowest tercile mean none. Keep tied values together. Collapsed cutoffs fail instead of arbitrarily splitting identical observations. Quintiles are not supported.

### Poverty must be contextualized

Choose the poverty measure, poverty line, reference year and classification for the setting. Prefer suitable published classifications; do not transfer US concentrated-poverty thresholds to international poverty estimates. A national poverty line may be appropriate for a country application; international comparisons require a consistent line and purchasing-power-parity vintage. Subnational all-population rates describe area context and must not be presented as rural-only estimates.

Where no suitable published classes exist, the default poverty calibration uses a global reference distribution within each World Bank income tier: low, lower-middle and upper-middle income. Regional or national adaptations require documented contextual justification. Record the grouping vintage, included areas, weighting and fixed cutoffs. Income groups identify the comparison set; they do not themselves establish poverty severity. Review these choices against the intended setting before application. Missing remains unknown, and no positive “none/very little” band is assumed. The [initial low- and middle-income calibration](research/2026-11-25-poverty-context-calibration.md) includes the separate tier results and pooled comparisons; its numerical cutoffs remain provisional, not accepted runtime rules.

Missing data remains unknown. Missingness cannot mean no problem. The rule reference records a justification; validators check structure and provenance fields, not the truth of that justification or the authenticity of scientific approval. Illustrative rules are marked as such and cannot be passed off as calibrated country defaults.

## Correlation and weighting

Inspect relationships within the declared opportunity area, retaining raw and classified indicators. Group variables by meaning first. Choose one representative per shared concern and record the reason. Statistical correlation alone cannot establish that two different policy concerns should be merged. Record retained correlated concerns and assess their influence in sensitivity runs.

The reference evaluator accepts explicit nonnegative weights on the selected concern set. A weight of zero omits that concern. It normalizes positive weights once for the whole stack:

`H(x) = sum(u_j * p_j(x)) / sum(u_j)`.

The denominator does not vary by pixel. Any missing positive-weight criterion gives an unknown score; missing zero-weight criteria do not block scoring. Outside the opportunity mask, the pixel is excluded; an unknown mask remains unknown. All-zero weights are an error. Output scores remain on 0–1 without a second min–max stretch or quintile map classification. Contributions sum to the score. User weights, class scores and synthesis evidence influence are separate quantities.

CRITIC is available for comparison only. It does not silently supply weights, change representatives or combine with user priorities. See the [assessment](../methodology-reference/reviews/critic-assessment-2026-11-24.md) for evidence and reproducible experiments.

## Execution and approval boundary

A reference evaluator is proposed in [runtime draft PR #11](https://github.com/RuralScan/runtime/pull/11); adoption is tracked in [runtime issue #12](https://github.com/RuralScan/runtime/issues/12). Runtime main has not adopted that draft. Its proposed `nbs_runtime.priority` module carries an independently pinned copy of the method contract. An analysis records its context, variable/rule versions, data references, aligned input hashes, reference-sample hashes, selection reasons and final weights. The initial example and tests use synthetic data. No real country thresholds or newly approved pilot results are bundled.

The API operates on aligned pixel sequences. A spatial caller remains responsible for CRS, grid alignment, valid-domain masks, dataset fitness and the actual geographic scope. This route does not alter the existing T4 notebook or run a live pilot. To adopt it for a pilot, supply reviewed classifications and dataset bindings, document the correlation review, then inspect the resulting coverage and sensitivity with the intended users.

## Classification catalogue under review

[Variable-by-variable audit](audit.md) · [Catalogue, acceptance and release proposal](catalogue.md) · [Runtime conformance vectors](test-vectors.json). The catalogue has no accepted runtime rules. Source observations, classification acceptance and user weights remain separate.

Current consolidated route: [T5 profiles, routing and preservation](consolidation.md). Historical 0.1 proposals remain immutable; IPLC is now unscored in the current sidecar.

The [contextual classification table](classifications/README.md) extends T5 with a rule-set reference: one variable can select a rule by country, region or World Bank income tier. It contains three provisional poverty rules and the next variable's published-band soil erosion proposal. CSVs are authoritative; generated JSON and review selection are checked in CI. These records do not activate a runtime release.

Dataset follow-up: [first inspected binding candidates](bindings/README.md), with exact evidence pins, CSV-generated proposals and remaining adoption checks.
