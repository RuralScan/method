# First dataset-binding candidates

These fourteen candidates supply concrete acquisition routes, fields, units, temporal/spatial support, raw-value handling and known limits for the first drought, water, carbon and IPLC batch. They are technically inspected proposals, not accepted BIND rows or calibrated pilot inputs. Existing historical configuration CSVs, classifications and decisions remain reproducible.

| Candidate | Checked route and usable detail | What still prevents adoption |
|---|---|---|
| FAO annual drought intensity | Official ArcGIS `DI_A`; choose year × season × cropland/grassland, resolve one record, request unrendered pixels; float 0–1 → wVHI percent | Local system/season fitness, reference period, valid-season denominator and classification; provider threshold equality unresolved |
| FAO annual stress extent | `ASI_A`; same explicit selectors; percentage 0–100 | Choose extent versus intensity/recurrence as the drought representative |
| FAO historical frequency / explicit recurrence | Original HDF remains held; annual ASI reconstruction checks 42 years and both published event definitions | Select AOI, season and event definition; classification still pending |
| FAO DI in Earth Engine | Optional route unavailable; official ArcGIS fallback checked | No GEE access request needed to use the fallback |
| SPEI-03 and SPEI-12 | `CSIC/SPEI/2_11`, explicit accumulation bands; 1901–2024 monthly series | Meteorological corroboration/event measure; livelihood interpretation and period reducer unresolved |
| Aqueduct annual/monthly | Native fields checked; pinned WRI production code confirms raw ratios above 1 | Four-class interpretation and AOI support need scientific/context review |
| Hansen forest loss | Current 2025 v1.13 `loss`, `lossyear`, `datamask`, `treecover2000` | Proposed forest-loss variable, not carbon mass; define forest mask and period/area denominator |
| Forest gross emissions | New producer-source v1.4.3 candidate: cumulative Mg CO2e/ha, 2001–2025; exact run/object fingerprint checked | AOI tile fingerprints, forest support and scientific definition; old 2024 mirror retained as superseded |
| Naturebase avoided forest conversion | Actual TIFF member/hash, native grid and nodata inspected | Potential descriptor; applicability and area denominator unresolved; other pathways need separate inspection |
| LandMark community overlap | Authorized June 2026 ZIP acquired; actual polygon/point schema, fields, CRS and exclusions checked | AOI completeness and source conditions; stays unscored |

## Files and checks

`candidates.csv` is the editable source. JSON-valued cells retain typed selectors, required masks, sentinel states and observation references. `columns.json` defines this new sidecar's columns; it does not modify the frozen historical T0–T7/BIND schema. Generate `candidates.json` with:

```
python3 priority/binding_candidates.py generate
python3 priority/binding_candidates.py check --evidence-repo /path/to/evidence
python3 -m unittest discover -v -s priority
```

`evidence.lock.json` pins the evidence repository commit and observation manifest hash. Every candidate references exact observation bytes at that revision. Evidence observations contain requests, raw-response hashes and local team-library copy receipts. Local hash verification does not establish remote team access or scientific acceptance.

`inspection-vectors.json` distinguishes observed samples from constructed edge cases. The small review oracle checks source encoding only: special states before unit conversion; no clipping at catalogue display limits; no missing-to-zero conversion; no annualization of cumulative emissions. It does **not** read data, align grids, classify values or validate coverage. A numeric zero returned by this oracle says only how a stored value decodes. Naturebase's zero ocean sample, for example, still needs an independent applicability mask. There is no runtime consumer of this sidecar.

## Spatial and temporal choices already narrowed

FAO annual DI/ASI are the first sampled agricultural-drought candidates. Query `Year`, `Season`, `Land_Type`; require exactly one catalog result and lock that freshly resolved raster ID with `rasterFunction=None`. OBJECTID 328/477 from the diagnostic run is not a permanent dataset identifier. Default mosaics can mix incompatible years and systems. Float32 DI differs from the service prose claiming signed integer. The near-1 km delivery grid retains GAUL2 summary support; do not treat its pixels as independent impact observations. HDF retains its 2023/2024/2025 denominator discrepancy. A new explicit 1984–2025 annual-ASI reconstruction supplies a known 42-season denominator; no new ordinal frequency cutoff is invented. Native ASI is F32 despite the service-default U8 encoding: retain half-percent precision before threshold comparison.

SPEI-12 connects the existing T2 drought ID; SPEI-03 and FAO connect T5 drought. All share `concern_id=drought`, so selecting more than one source does not authorize counting the same concern repeatedly. Required AOI, years and seasonal/temporal statistic have no silent default. A display range of ±2.33 would discard observed drought/wetness extremes.

Aqueduct annual `bws_raw` is a ratio, not percent or the 0–5 risk score. Numeric values >1 remain unchanged. `bws_cat=-1` marks arid/low use even when raw=1; raw=9999 is a physical-scarcity sentinel; missing/-9999 stays unknown. Preserve category and label alongside raw values. Annual data has basin/admin/aquifer intersection geometry, so counting every fragment as an independent basin biases aggregation. The annual statistic is demand-weighted monthly ratios with a 2019 target baseline from smoothed historical trends, not a simple historical average or a 2010–2080 time series. Monthly numeric fields can be absent.

Forest loss and modelled forest emissions are **separate proposed variables**, never aliases for `carbon_sequestration_potential`. Hansen `lossyear` is masked outside detected events; valid land plus `loss=0` is needed for no-event interpretation. The old mirror covers 2001–2024 and remains superseded. The new producer-source model v1.4.3 covers 2001–2025, matching the year edition of the Hansen candidate. An explicitly adopted division by 25 would yield a period-average rate, not yearly event observations. Native producer zero is nodata. Wetland/peat degradation and soil-carbon decline remain coverage gaps; stock maps and Naturebase mitigation potential cannot fill them by relabeling.

Naturebase avoided forest conversion is one inspected pathway among twenty. The actual member `for_afc_tco2eha.tif` differs from the README name; its header says EPSG:4326. Modelled mean annual mitigation uses 2017–2021 rates assumed constant over the accounting horizon. The downloaded member hash is pinned, but scientific counterfactual, fractional area and hierarchy checks remain before any summary. No all-pathway total is assigned to an individual NbS.

## Adoption path

Complete named technical holds and pilot/context checks; register/acquire source findings through the existing evidence route; obtain their human review; prepare exact variable/context/binding interpretation and approval through the existing method decision route. These candidates cannot create `priority/binding-verifications` receipts. The current package checker still requires real T1/BIND rows, exact binding/context hashes and human decisions. An eventual approved configuration migration must add those rows deliberately, regenerate dependent records and preserve old snapshots. Merging this inspection catalogue alone does not authorize that migration or any runtime release.

## Resolved holds

[Resolution record](hold-resolution.md) distinguishes corrected encoding, tested replacement routes, completed LandMark acquisition and remaining context/scientific decisions. [Machine-readable hold status](holds.json) prevents treating successful access as pilot approval.

## Follow-up overlays

[KBA conservation importance](../conservation/README.md) is approved as an input to the single Biodiversity priority layer requested by Pete; its official acquisition route is identified, with 1.5/5 km proximity bands approved; polygon inspection/access remain pending. [Road infrastructure](../infrastructure/2026-11-26-roads-binding.md) and [health facilities/schools](../infrastructure/2026-11-26-facility-bindings.md) now have technical inspection records; national source coverage and runtime adoption remain pending. These records do not silently append unverified candidates to the fourteen-row evidence-pinned catalogue.

[Haiti national-source and power/building inspection](../infrastructure/2026-11-26-haiti-national-infrastructure.md) advances actual national-source acquisition and verifies the power/building fallbacks. It preserves partial/non-spatial/old-source limitations and does not activate unreviewed bindings.


26 November next steps: [Haiti infrastructure fallbacks](../infrastructure/README.md#approved-haiti-fallbacks-and-remaining-national-gaps) are now selected provisionally, with national acquisition gaps and existing T1/BIND/T7 context handling recorded. [BII follow-up](../research/2026-11-26-biodiversity-loss-classes.md#next-binding-inspection-nhm-v211-limited-release) records the approved acquisition and full native-raster inspection of NHM v2.1.1: five years through 2020, 5-arc-minute grid, percentage BII and NaN nodata. Coarse spatial support, an explicit depletion transform and runtime acceptance remain open. Neither follow-up changes runtime readiness.
