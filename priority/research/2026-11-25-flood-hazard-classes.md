# Flooding: proposed river-inundation classes

25 November 2026. Next variable in the nine-problem review. Proposal only: no flood classes or default return period approved. [Brayden's confirmation is requested](2026-11-25-climate-hazard-alignment.md).

Measure: modelled river-flood inundation depth, in metres, for a declared return period. A 100-year scenario is a candidate because GloFAS publishes it as a standard static display; it is not yet the selected RuralScan default. A return period describes event probability, not a prediction that the event occurs regularly every 100 years. Compare classes only within the same scenario.

The [official CEMS flood-inundation documentation](https://confluence.ecmwf.int/plugins/viewsource/viewpagesrc.action?pageId=340780077), subsection “Global 'Flood hazard 100 year return period' layer”, and its linked legend publish depth bands 0.09–<1 m, 1–<3 m, 3–<10 m and ≥10 m, with permanent water separate. Proposed four-label crosswalk:

| RuralScan display | Published depth category / condition |
|---|---|
| None / very little | Confirmed not flooded within assessed coverage for the selected scenario |
| Low | 0.09 to below 1 m |
| Medium | 1 to below 3 m |
| High | 3 to below 10 m, or 10 m and above |

Rationale: retain the published category breaks and combine the two deepest bands. These labels summarize depth, not expected damage, safety for people, crop loss or NbS protection benefits. Preserve native depth and category. The lowest class does not mean no flood risk under other scenarios or flood mechanisms.

The legend alone does not settle data encoding for dry land, masked cells or depths below 0.09 m. Verify those states in the selected distribution before producing classes. Missing coverage, permanent water and spurious depths must retain explicit flags; they must not become None. Use verified native categories where available; do not substitute the existing upper-inclusive numerical convention for this legend's lower-inclusive bands.

The [official Earth Engine catalogue](https://developers.google.com/earth-engine/datasets/catalog/JRC_CEMS_GLOFAS_FloodHazard_v2_1) offers `JRC/CEMS_GLOFAS/FloodHazard/v2_1`, with separate depth/category bands for seven return periods (10, 20, 50, 75, 100, 200, 500 years), plus permanent-water and spurious-depth masks, at about 90 m. Prefer this hosted route if it meets the use case; the candidate has not been sampled or accepted here. Band descriptions/ranges are not a complete category decoder.

CEMS documentation limits GloFAS river simulations to catchments exceeding 500 km²; pluvial and coastal flooding are excluded. Consequently this is a river-flood screening layer, not complete flooding coverage. It does not establish protection by existing defences or site-level engineering performance. Reuse a verified selected scenario for [infrastructure exposure](../infrastructure/README.md), keeping inventory coverage and assessed denominators explicit.

Original official documentation, catalogue HTML and inspected legend PNG are archived with the drought verification packet: `0_Methodology_&_Frameworks/priority_classification/drought_flood_alignment_2026_11_25/reviewed_sources.zip`, SHA-256 `0ef2fd6ddbe77574a1ddc76f208a69fc59cf5ad8be033aa25822dbcfe5c2bfc4`. The legend was inspected on a white background because its source image has transparency. Remote team access was not checked.
