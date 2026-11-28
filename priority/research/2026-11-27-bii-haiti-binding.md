# BII Haiti binding: native coverage and depletion conversion

27 November 2026. Next non-hazard binding after the [acute food-insecurity approval](2026-11-27-food-insecurity-approved.md). **Haiti coverage and the explicit `100 − BII` conversion are now checked against the acquired raster.** This advances the already approved coarse-context use; it does not activate a runtime binding or resolve KBA access.

## Source and result

Source: NHM **v2.1.1 limited release**, `bii-2020_v2-1-1.tif`, percentage BII, band 1, Float64, NaN nodata, EPSG:4326, five arc-minutes. [Producer catalogue](https://data.nhm.ac.uk/dataset/bii-developed-by-nhm-v2-1-1-limited-release) and the acquired README confirm units and coarse support. Original 2020 raster SHA256: `d2142dd8d6d0bf1a08268d9a9a03c7a9b9ab4d834714d7fea35de621559a72b4`. Existing approval covers non-commercial inspection under CC BY-NC-SA 4.0; no new download or terms submission occurred.

Exact intersections of native raster-cell footprints with the pinned [Haiti boundary](haiti-diagnostic-inputs-20261126/README.md) give:

| Observation | Result |
|---|---:|
| Boundary area, EPSG:6933 | 27,116.832 km² |
| Native cells intersecting boundary | 453 |
| Valid intersecting native cells | 443 |
| Valid footprint area | 27,114.954 km² / **99.99308%** |
| Unknown footprint area | 1.877 km² / **0.00692%** |
| Valid BII range in intersecting cells | 3.51–89.12% |
| Finite out-of-domain cells | 0 |

Coverage means valid **coarse cell footprints** overlapping this boundary. It is not evidence that every fine location was observed. Coastline differences and cells spanning other countries/ocean remain consequences of native support. No center-point country mask, interpolation, upsampling or gap filling was used.

## Verified conversion and approved classes

Read the valid native percentage first; compute depletion as **100 − BII** only for finite values in [0,100]. Preserve raw BII and the native mask. Missing, nonfinite or unexpected values remain unknown; never clip them into an apparently valid class. The numerical operation and bounds are recorded in [contract.json](bii-haiti-audit-20261127/contract.json), while class boundaries come from the [approved class data](bii-haiti-audit-20261127/classes.csv), not hardcoded thresholds in the probe.

| Approved BII depletion class | Depletion interval | Share of whole pinned boundary |
|---|---|---:|
| Very little | 0–10 inclusive | 0.0000% |
| Low | >10–20 inclusive | 0.0897% |
| Medium | >20–40 inclusive | 27.6670% |
| High | >40–100 inclusive | 72.2364% |
| Not assessed | Missing/invalid | 0.0069% |

Exact BII 90 → Very little, 80 → Low, 60 → Medium; BII 0 and 100 and invalid-input cases also pass. These are the already approved [published-band interpretation](2026-11-26-biodiversity-loss-classes.md), not a new calibration. Country shares use exact clipped cell area, not cell counts. They describe the BII input alone, not a combined Biodiversity priority or an NbS opportunity footprint. No valid Very little cell occurs in this bounded check; no class is manufactured to fill the legend.

## What remains limited or held

- Source year is **2020** and native resolution is approximately **10 km**. It is modelled condition relative to a reference, not measured recent loss, species extinction, a site survey or a restoration-benefit estimate. The inspection does not validate local ecological accuracy or quantify uncertainty.
- A future NbS footprint summary must intersect that footprint explicitly and disclose the same native support. Finer boundaries may refine overlap accounting, not biodiversity evidence.
- The [approved combined rule](../conservation/README.md) still requires valid BII **and** valid KBA proximity before taking their maximum. KBA polygons remain unavailable in the inspected workstream. Combined Biodiversity therefore stays **Not assessed**; BII can appear separately as approved coarse context.
- Arithmetic and native-input semantics are verified. The shared contextual binding format still permits positive scale only. This probe records an explicit reference-minus-input operation; it does not smuggle a negative scale into that format, invent a derived source asset, or claim a released transformation adapter. Schema/adapter adoption remains a distinct step.
- No accepted BIND/T1 row, release receipt or additional core variable is created. The research contract identifies a reproducible candidate for the existing biodiversity concern.

[Infrastructure remains active](../infrastructure/README.md#approved-haiti-fallbacks-and-remaining-national-gaps), with roads/facilities/power/buildings fallbacks and national replacement needs retained. BII cannot substitute for physical hazard exposure. Hazard choices still await Brayden.

See the [audit README](bii-haiti-audit-20261127/README.md) for input hashes, original acquisition archive and replay. Next biodiversity access hold remains the authorised KBA polygon package and its source/use conditions.
