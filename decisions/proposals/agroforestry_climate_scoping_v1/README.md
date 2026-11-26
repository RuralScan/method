# Exact pending decision: agroforestry climate scoping

**Status: proposal for review only. No acceptance event, evidence Keep vote, source finding, official mapping or runtime activation is created by this packet.** Checked against RuralScan/evidence main `5a59f5ab01a00791a5de23a82e41cad1657e20f3`, containing source admission PR #116 and the T4 proposal route in PR #110. The six sources are registered with extraction pending; revision 6's statement that PR #116 is unmerged is now historical.

## Decision wording prepared for a method proposal

> Adopt, subject to explicit scientific review, a provisional landscape-scoping convention for general climatic hostility to persistent upright tree-based agroforestry. Use a family-specific aridity membership and an independently derived temperature-only membership, combined by the minimum. Membership is neither establishment probability nor expected suitable-area fraction. Preserve separate footprint screens, missing/conditional states, host-system and legal/ecosystem constraints. Do not activate through source admission or software review alone.

The exact numerical proposal remains the revision 6 configuration, with the following revision 7 scope correction and safeguards:

| Current family | Registered subpractice | Required pathway | Proposed climate treatment |
|---|---|---|---|
| `agroforestry__planted_silvoarable` | `alley_cropping`, `tree_intercropping` | planted | Planted-tree moisture curve and cold component |
| `agroforestry__regeneration_farmland` | `fmnr`, `anr_on_farm` | regeneration to persistent upright-tree outcomes | FMNR moisture curve, dry screen and cold component |
| `agroforestry__silvopastoral` | `planted_silvopasture`, `agrosilvopasture` | planted | Planted-tree moisture curve and cold component |
| `agroforestry__regeneration_farmland` | `parkland_retention` | retention only | Context only; no new climate score or exclusion. Renewal would need an explicit later scope. |

An absent, mismatched or unsupported subpractice/pathway does not inherit a family-wide score or exclusion. No automatic transfer to pastoral regeneration, low shrubs/clipped hedges, boundary/wind/contour families, shaded perennial crops, homegardens or natural open ecosystems.

## Exact choices requiring approval together

1. **Moisture functions.** Planted systems: 20/80 membership at AI0.20/0.46, using the declared log-logistic. FMNR/ANR: 20/80 at AI0.03/0.20, with AI0.05/0.20 retained as the stricter dry-end sensitivity. The ecological/climate-class anchors do not constitute observed agroforestry success thresholds.
2. **Cold derivation.** Historical CHELSA v2.1 monthly 2-m mean air temperature; no-leap 365-day periodic linear interpolation at month centres. Count all days T≥0.9°C and average their temperature. No precipitation, soil-water or snow eligibility. Released coupled CHELSA GSL/GST is not an admissible substitute.
3. **Cold scores.** Temperature logistic 20/80 at3/10°C; thermal-duration log-logistic20/80 at30/130days. `S_cold=min(S_T,S_L)`. Broad source climate belts are deliberately transferred to a new thermal-potential proxy. The old94d/6.4°C comparator is a reference inside the transition, not a new exclusion boundary.
4. **Combination.** `S_climate=min(S_family_moisture,S_cold)`. No compensating weighted mean or additional multiplication. If later included in wider suitability, enter the climate parent once; no child double counting and no inferred MCDA weight.
5. **Separate screens.** FMNR/ANR rainfed AI<0.03 is outside the proposed default opportunity. All in-scope upright-tree pathways: thermal mean<3°C or thermal days<30 is outside default opportunity; equality retained. Zero qualifying days from complete valid temperatures is known severe cold. Do not introduce a common combined-score cutoff or a planted-family AI<0.20 exclusion.
6. **Conditional and missing states.** Known host/legal exclusions prevail. Known severe cold cannot be rescued by mapped water. Potential water refuges use a conditional, unscored pathway, without automatic area. Missing one climate component leaves the total unknown; a known independent exclusion remains visible. Missing pathway is outside scope, not climate failure.
7. **Bindings and meaning.** Explicit historical pair Global-AI v3(1970–2000) and CHELSA v2.1 tas(1981–2010), at climate-grid support; mixed baselines accepted only as a scoping convention. Snow omission, mountain representation, frost and transfer limits remain visible. No future-change or calibrated success claim follows.
8. **Area and release.** Report eligible host area, conditional, excluded and unknown area separately after acceptance; never multiply hectares by membership. Scientific acceptance, implementation acceptance and source/finding review remain separate. This method proposal itself changes no live outputs.

## What the evidence check does—and does not—establish

Six newly admitted method/context sources have no new evidence units. The three Niger references pass the pending FMNR rule and remain moisture-limited under the cold minimum. Three selected southern treeline references pass the broad cold screen. These are targeted contradiction/sensitivity checks, not field validation of accuracy. Acquisition update after proposal registration: Berdugo’s 29-page accepted manuscript was recovered from the UPF repository, DOI/title verified and hash-matched in the shared-library mirror. [Draft evidence PR #117](https://github.com/RuralScan/evidence/pull/117) proposes its source admission; the supplement remains a separate acquisition gap. This closes the manuscript recovery hold without changing the numerical proposal or conferring scientific approval.

The remaining substantive decision is acceptance of the transparent proxy and policy transfers above. No farm survey, species palette, density target, engineering model or global survival calibration is being made a prerequisite for this restricted scoping claim. Scientific reviewers may reject or narrow the convention; source admission cannot settle that judgment.

## Official route available now

**A pending method proposal can be prepared now. An executable official T4 proposal cannot represent this complete policy unchanged under contract v1.0.0.** The official route supports only piecewise, threshold, ranked-class and qualitative single-variable mappings, one current family per proposal. It has no declared log-logistic/logistic forms, temperature derivation, nested climate minimum, pathway predicate or separate score/screen state contract.

A piecewise approximation is possible only as a newly declared scientific representation, with an approved domain, error tolerance and explicit tails. It would not reproduce the current smooth function and must not be substituted silently. The preferable next implementation is a bounded contract/definition extension for the exact proposed policy, followed by fresh proposals after adoption.

Under the existing contract, a **qualitative `aridity_index` row with `readiness=calibration_hold`, `dataset_id=null`, `evidence_ids=[]`, `weight_default=null`** can represent the pending question. A separate proposal is needed per family and must still account for every prepared candidate. It would not be an executable climate rule, and accepting a held row would block calibrated packaging. Preparing another such placeholder is optional; the method proposal plus existing review page already exposes the same unresolved decision.

## Minimum technical prerequisites for exact T4 packaging

| Item | Current state | Required bounded action |
|---|---|---|
| Current family/subpractice identities | All named IDs exist; F2 includes retention and F3 includes mixed systems | Add exact executable pathway/subpractice scope, preserving current FAM; no new family needed |
| Aridity variable | VONT `aridity_index` exists, dimensionless | Add reviewed preferred contextual binding to the exact source release |
| Thermal quantities | Temperature-only season mean and duration absent from current VONT | Define quantities/units/support and derivation; never reuse mean annual temperature or coupled GSL/GST |
| Dataset and BIND | No current aridity BIND; no thermal BIND | Reviewed method definitions/release, then evidence adoption; include preferred status, units, masks and baselines |
| Smooth response forms | Unsupported by v1 exact parameter validator | Reviewed contract extension, or explicitly reviewed approximation; no arbitrary undeclared JSON parameters |
| Nested minimum and separate screens | Not a mapping-package execution policy | Typed climate-parent and screen semantics in method/runtime contract; no unapproved weight inference |
| Source-backed policy transfer | Admitted method papers are not structural-suitability claims by default | Pin method references and exact source editions/locators separately; extract only genuine practice-suitability claims; do not fabricate EV thresholds |
| Source identity projection | Acquisition identity exists but T4 input SRC rows omit required boolean flags | Repair consumer projection from authenticated acquisition verification; no hand-set flags or weakened verification |
| Prior rows | Historical F1 temperature and precipitation mappings exist | Name exact replacement/withdrawal IDs and hashes only after accepted replacement coverage is specified |
| Acceptance | None for this convention | Review method proposal, then immutable per-family T4 packets; eligible human original scientific-acceptance receipt; implementation separately |

## Approval process—not approval recorded

Proposed method decision ID: `agroforestry_climate_scoping_v1`. Record an **action `propose`**, sequence1 only after checking the current register for collisions, with the exact packet's public permalink. A method PR can publish this open question without an action `decide`. Do not use source-admission PR approval as the scientific acceptance.

After the method definitions/contract are reviewed and adopted, prepare immutable T4 inputs from the new official evidence edition; author separate current-family proposals with complete candidate dispositions and exact replacement fingerprints. Publish their hashes/commit for review. The eligible human—not the agent—must create the original `RuralScan T4 scientific acceptance v1` issue if accepting those exact bytes. Packaging still states `runtime_implemented:false`; runtime integration requires its own reviewed consumer configuration.

Immediate next step: publish the exact scoped method proposal and the narrow contract/definition work needed to encode it. Keep all scientific statuses pending. No more open-ended site-feasibility research is required to do that.

## References checked

- [Official T4 proposal route at source-admission edition](https://github.com/RuralScan/evidence/blob/5a59f5ab01a00791a5de23a82e41cad1657e20f3/workflows/t4_synthesis/README.md)
- [Pinned T4 contract](https://github.com/RuralScan/evidence/blob/5a59f5ab01a00791a5de23a82e41cad1657e20f3/workflows/t4_synthesis/contract.json)
- [Source admission PR #116](https://github.com/RuralScan/evidence/pull/116)
- [Method decision protocol](https://github.com/RuralScan/method/blob/bf213ff960d5ac711baf433dcf7a4fea80cc2218/decisions/README.md)

The protocol link identifies the inspected full method revision. Accepted downstream editions must likewise pin immutable revisions.

## Exact authored configuration

[Climate and scope policy](combination_policy.json) · [Thermal anchors](thermal_policy.csv) · [Moisture anchors](moisture_policy.csv) · [Selected thermal reference checks](thermal_reference_checks.csv). These files are proposed, not accepted implementation or a runtime package.
