# Drought: proposed four-class intensity display

25 November 2026. First unresolved problem in the nine-variable visual scope. Proposal for interpretation review; no classes or numeric cutoffs adopted in this pass.

FAO's Agricultural Stress Index System (ASIS) Drought Intensity product classifies regionally aggregated weighted vegetation health into Mild, Moderate, Severe and Extreme drought, with a separate no-water-stress condition. FAO's FAQ explains the seasonal agricultural meaning and GAUL level 2 reporting support. [FAO FAQ, questions 2–3](https://www.fao.org/giews/earthobservation/faq.jsp).

| RuralScan display | Published FAO category |
|---|---|
| None / very little | No water stress |
| Low | Mild drought |
| Medium | Moderate drought |
| High | Severe or Extreme drought |

This preserves provider categories, merging the two highest and relabelling the display. It is a RuralScan four-class convention, not a claim that FAO itself publishes these four labels. Retain the native category alongside the display class. The lowest class means no stress detected by this indicator for the reported period, not permanent absence of drought or livelihood risk.

The existing inspected DI_A service candidate supplies continuous weighted vegetation-health values, not verified category codes. Earlier research transcribed the published legend's numeric bands, but exact endpoint equality remains unresolved. Do not silently apply those boundaries to continuous values. Adopt this category interpretation first; verify provider classification semantics before translating it into numerical rules. The official legend URL remains recorded in the earlier research note; direct image retrieval returned 403 in this pass.

This is agricultural drought intensity for the selected source observation, not the percentage of years with drought, a household-loss measure or a future projection. Preserve reporting period, crop/pasture coverage and source support. Off-season, no-season, water, missing and outside-host-system codes must not become the lowest class. The rendered kilometre grid does not create kilometre-scale independent observations from GAUL2 summaries.

No new seasonal-fit assessment or hydrological modelling is requested here. FAO recurrence work already saved in `bindings/hold-resolution.md` remains separate: intensity thresholds cannot classify historical event frequency. The visual mock-up's rainfall-deficit-frequency example and FAO agricultural intensity measure are different quantities; adopting this proposal would make that choice explicit.

Source review: reread FAO FAQ questions 2–3 and seasonal/non-seasonal indicator guidance on 25 November 2026, alongside the existing inspected `fao_di_annual_candidate`. No new data acquired or runtime rule activated.
