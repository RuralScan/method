# Drought: approved intensity display; hazard alignment pending

25 November 2026. Pete approved the four-class interpretation and requested numeric boundary verification, followed by flooding. He then required alignment with Brayden's intended climate hazard variables. The approved FAO interpretation is preserved below; its selection as the core drought hazard remains pending that confirmation. See the [alignment record](2026-11-25-climate-hazard-alignment.md).

FAO's Agricultural Stress Index System (ASIS) Drought Intensity product classifies regionally aggregated weighted vegetation health into Mild, Moderate, Severe and Extreme drought, with a separate no-water-stress condition. FAO's FAQ explains the seasonal agricultural meaning and GAUL level 2 reporting support. [FAO FAQ, questions 2–3](https://www.fao.org/giews/earthobservation/faq.jsp).

| RuralScan display | Published FAO category |
|---|---|
| None / very little | No water stress |
| Low | Mild drought |
| Medium | Moderate drought |
| High | Severe or Extreme drought |

This preserves provider categories, merging the two highest and relabelling the display. It is a RuralScan four-class convention, not a claim that FAO itself publishes these four labels. Retain the native category alongside the display class. The lowest class means no stress detected by this indicator for the reported period, not permanent absence of drought or livelihood risk.

## Numeric boundary verification

The official [DI_A ImageServer](https://asis-esri.fao.org/image/rest/services/DI_A/ImageServer) supplies continuous float32 values with the `None` renderer, and categorical values with `DI Renderer`. Its `rasterAttributeTable` supplies the category labels. Paired nearest-neighbour TIFF exports of the same locked 2024 / Season 1 / Cropland observation establish the equality assignments:

| RuralScan display | Weighted vegetation health, percent scale | Native float32 fraction | Provider rendered code |
|---|---|---|---|
| High | Below 35 | Below 0.35 | 25 (Extreme) or 35 (Severe) |
| Medium | 35 to below 38 | 0.35 to below 0.38 | 38 (Moderate) |
| Low | 38 to below 42 | 0.38 to below 0.42 | 42 (Mild) |
| None / very little | 42 and above | 0.42 and above | 251 (None) |

These ranges apply only to valid, covered observations in the native 0–1 domain. The underlying Extreme/Severe split is below 25 versus 25 to below 35. The live renderer assigns equality at 42 to None, resolving the FAQ's less precise “above 42” wording for this inspected service.

Verification used a 1,000 × 400 diagnostic sample, not a pilot analysis. All 26,614 pixels with recognized ordinary classes agreed with lower-inclusive boundaries at native float32 precision. Exact native boundaries occurred at 0.25 (5 samples, code 35), 0.35 (42, code 38), 0.38 (64, code 42), and 0.42 (97, code 251). The sample also contained 288,697 raw-zero/rendered-zero cells with no recognized category: they were excluded, not treated as valid zero stress. The service returned no TIFF nodata declaration, so a zero-only validity check is insufficient. Tests of `getSamples` did not establish rendered categorical output; do not assume its result uses the export renderer.

Prefer the verified provider category with explicit coverage checks. If reproducing the numeric comparison, preserve native float32 precision: for example, native 0.42 is approximately 0.4199999869 when widened to float64. Comparing that widened number against decimal 0.42 misclassifies the boundary. The current contextual table's upper-inclusive numeric rule cannot express these semantics unchanged. No rule has been forced into that format and no core binding has been switched while hazard alignment is unresolved.

Raw and rendered special codes differ. In the raw candidate, 251 means off-season; in the rendered table, 251 means None. Rendered 252/253/254/255 mean off-season/no-data/no-season/no-cropland-or-grassland. Preserve the encoding and all unknown/coverage states; never join these vocabularies by numeric code alone.

This is agricultural drought intensity for the selected source observation, not the percentage of years with drought, a household-loss measure or a future projection. Preserve reporting period, crop/pasture coverage and source support. Off-season, no-season, water, missing and outside-host-system codes must not become the lowest class. The rendered kilometre grid does not create kilometre-scale independent observations from GAUL2 summaries.

No new seasonal-fit assessment or hydrological modelling is requested here. FAO recurrence work already saved in `bindings/hold-resolution.md` remains separate: intensity thresholds cannot classify historical event frequency. The visual mock-up's rainfall-deficit-frequency example and FAO agricultural intensity measure are different quantities. Brayden has been asked to confirm the intended drought indicator before choosing between them or a meteorological index.

Source review: FAO FAQ questions 2–3, existing `fao_di_annual_candidate`, and fresh paired official-service diagnostic exports on 25 November 2026. No runtime rule activated. Original responses, TIFFs, request script and verification summary are retained in the team-library mirror at `0_Methodology_&_Frameworks/priority_classification/drought_flood_alignment_2026_11_25/reviewed_sources.zip`, SHA-256 `0ef2fd6ddbe77574a1ddc76f208a69fc59cf5ad8be033aa25822dbcfe5c2bfc4`. Archive members were read back and hashes checked; remote team access was not checked. The transient locked object ID was 328; future requests must resolve the documented year/season/land-type selector afresh.

Next variable: [flooding proposal](2026-11-25-flood-hazard-classes.md), subject to the same hazard-alignment confirmation.
