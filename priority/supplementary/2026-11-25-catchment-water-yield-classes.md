# Catchment water yield: interpretation review

25 November 2026. Next priority row after gender inequity; intervening T5 rows are descriptors. Proposal only: no role, metric or classes changed.

The current profile for `catchment_water_yield` is held because it mixes downstream supply deficit (baseline need) with yield change (an intervention effect). It has no selected dataset or unit. Higher water yield is not inherently greater concern, while low yield alone does not establish unmet demand.

InVEST's Annual Water Yield documentation distinguishes water production from water consumed and downstream benefits. It cautions that its water-yield outputs do not by themselves identify how much water benefits downstream users. Interpretation belongs at subwatershed scale; pixel maps are provided for model checking, not local decisions. Annual averages also omit delivery timing. These limitations explain why a water-yield map alone cannot establish scarcity severity. [Official InVEST 3.19 guide: How it Works; Interpreting Results; Limitations and Simplifications](https://storage.googleapis.com/releases.naturalcapitalproject.org/invest/3.19.0/userguide/en/annual_water_yield.html).

A hosted candidate exists for descriptive hydrology: HydroATLAS in Earth Engine includes annual-average land-surface runoff (`run_mm_syr`) at basin support. This is a catalogue observation, not an inspected or adopted binding. It supplies neither downstream demand nor a severity classification. [Earth Engine HydroATLAS catalogue: Table Schema](https://developers.google.com/earth-engine/datasets/catalog/WWF_HydroATLAS_v1_Basins_level11).

## Proposed approach for discussion

Do not assign None / Low / Medium / High need classes to raw catchment water yield. Keep any future yield/runoff values as descriptive context with their units, catchment support and source period. Use the already approved water-stress classes for the current scarcity concern, rather than adding an unvalidated second score from yield alone.

If a separate downstream supply concern is needed later, first select a published or locally justified measure of unmet supply for identified receiving users and an applicable classification. Keep it distinct from modelled NbS yield changes, which belong in the response/effect stream. Missing supply or demand data mean unknown, not no deficit.

This recommendation does not change T5's priority designation or activate HydroATLAS. It proposes leaving the current row unclassified and treating raw yield descriptively; an approved routing change can be recorded separately. No hydrological model, seasonal-fit analysis or new dataset processing is needed for this classification review.

## Search record

Bounded primary-source review on 25 November 2026 used:

- `site.naturalcapitalproject.stanford.edu annual water yield model limitations water supply hydropower classification`
- `site.hydrosheds.org HydroATLAS runoff water yield variable mm year`

Read the official InVEST 3.19 Annual Water Yield guide and the Earth Engine HydroATLAS catalogue. Neither supplies transferable four-band need thresholds for raw catchment yield. This is an interpretation review, not an exhaustive threshold search or formal source registration. No data acquired or class adopted.
