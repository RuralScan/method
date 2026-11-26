# Carbon loss: proposed forest-emissions classification

26 November 2026. Next non-climate variable after biodiversity. Proposal for interpretation review; no class cutoffs, successor variable or runtime rule approved here. Climate hazards remain pending Brayden; [infrastructure exposure](../infrastructure/README.md) stays in scope.

## Measure

Use **modelled gross forest-related greenhouse-gas emissions per hectare** as a bounded carbon-loss proxy. The existing inspected candidate, `forest_gross_emissions_2025_candidate`, supplies cumulative **Mg CO2e/ha over 2001–2025** (model v1.4.3, producer run 20260327). Mg and metric tonnes are equivalent. Keep that period explicit; do not label the cumulative value an annual rate or tonnes of elemental carbon.

[Gibbs et al. (2025), sections 2.1 and 4.3](https://essd.copernicus.org/articles/17/1217/2025/) describe the GFW gain–loss model, including forest disturbance emissions, organic-soil drainage and non-CO2 greenhouse gases. Forest removals are a separate output. Gross emissions retain the loss signal even where removals offset it in net flux. The model is not a direct measurement of carbon stock change and does not cover all rural land-carbon losses; low-severity disturbances and uncertainty are limitations.

The paper describes 2001–2023, as does the [WRI catalogue page](https://datasets.wri.org/datasets/gfw-forest-carbon-gross-emissions) retrieved in this review. They support the method, not the later version identity. The existing [producer-pin inspection](../bindings/hold-resolution.md#forest-emissions-source-identity) establishes the separate 2001–2025 candidate. Do not mix the catalogue's older download version with the inspected candidate.

## Proposed classes and rationale

The reviewed paper and catalogue do not establish universal none/low/medium/high emission-severity thresholds. Use the already agreed distribution-based fallback rather than invent physical severity cutoffs:

| Display class | Proposed rule |
|---|---|
| Low | Positive emissions at or below the fixed global reference's one-third quantile |
| Medium | Above the one-third quantile and at or below the two-thirds quantile |
| High | Above the two-thirds quantile |
| None / very little | **Unassigned with the current binding**; no justified positive cutoff or verified zero state |

These are relative **emission-intensity** classes, not ecological damage thresholds, total-area emissions, or benefit/cost estimates. Use one fixed global, area-representative reference sample of eligible forest locations with valid positive values from the same edition and period. Sample locations uniformly by eligible physical area; do not give equal influence to unequal-area latitude/longitude pixels. Apply the ordinary documented sample quantiles, retain ties, and save the sample, hash, support, size and realized cutoffs. Collapsed cuts require review. Numerical cutoffs have **not** been calculated in this proposal.

The reference is global rather than split by World Bank income tiers: a tonne of emissions represents the same physical quantity across economies. Country or ecological-context overrides can be documented if the analytical objective warrants them; do not silently refit classes to each project area. Revisit calibration explicitly when the source edition or cumulative period changes. A fixed global reference is not approval to compare incompatible model versions.

## Coverage and zero handling

The inspected native TIFF declares **zero as nodata**. The existing decoder therefore returns unknown. Preserve that rule: neither raw zero nor absence of a mapped Hansen loss event alone verifies zero emissions, and neither can become the None class. A future provider-supported coverage/non-event mask could justify a separate “no mapped emissions for the assessed processes and period” state; that has not been established here. It would still not prove no carbon loss from all processes.

Eligible forest support must be pinned before calibrating. Retain the producer's documented forest definition and exclusions or an explicitly reviewed alternative; do not silently adopt a canopy threshold. This candidate cannot fill soil-carbon decline on cropland/grassland or non-forest wetland/peat coverage gaps. Some forest-related soil/peat emissions are included, so “all soil and peat excluded” would also be incorrect. Missing or outside-support areas remain unknown/not assessed, not Low.

Preserve raw emissions and coverage alongside classes. Modelled sequestration potential, carbon-stock snapshots and forest-loss area are different quantities and cannot substitute for this input. Keep `carbon_sequestration_potential` only as the legacy visual ID until the successor/routing decision is explicit. No new tenth problem is introduced.

## Status and source preservation

Proposed: forest-only proxy; fixed global positive-value terciles; no None/very-little class from current encoding. Required before adding calibrated rules: interpretation approval, eligible support/reference sample, numeric calibration and reviewed binding/routing. No new global raster acquisition or pilot analysis was undertaken.

The original paper HTML and WRI catalogue HTML, with URLs and section locators, are retained in the team-library mirror under `0_Methodology_&_Frameworks/priority_classification/carbon_loss_2026_11_26/reviewed_sources.zip`. Archive SHA-256: `53b9ad65b94a647296a41f27e2c3a31ed70e1979d31e92f29cfcd9b84aede4f7`. Members were read back and hashes verified; remote SharePoint access was not checked. Existing raster inspection provenance remains pinned through the binding registry. This is classification research, not a new formal SRC/EV intake or runtime acceptance.
