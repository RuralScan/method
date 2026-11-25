# Resolution of dataset-binding holds

The follow-up resolves access/encoding/version issues using actual producer services and an authorized LandMark download. It does not create scientific acceptance or a runnable pilot release. Original observation bytes and the older candidate routes remain available for reproduction; selected replacements are named explicitly.

| Hold | Result | Concrete binding action |
|---|---|---|
| Aqueduct raw >1 versus technical-note clipping text | Resolved by WRI's pinned production notebook | Keep unbounded nonnegative raw ratios and native categories. Annual scarcity logic is not an ordinary ratio of annual totals. |
| FAO ASI service pixel type | Resolved; native raster is F32, default service U8 can round | Request F32 with the None renderer or raw `getSamples`. A real 0.5% sample survives export; compare thresholds before any display quantization. |
| FAO HDF denominator/end year | Provider HDF remains unresolved; usable replacement prepared | `fao_asi_recurrence_candidate` explicitly reads 1984–2025, one selected season and land type per year. Forty-two annual observations give a known denominator. |
| FAO Earth Engine permissions | Optional route remains inaccessible; access hold bypassed | Use already-sampled official ArcGIS DI/ASI. No access-request email needed. |
| Mutable forest-emissions mirror / 2024–2025 mismatch | Resolved through a new producer-source candidate | `forest_gross_emissions_2025_candidate`: model v1.4.3, run 20260327, cumulative 2001–2025, matched 2025 loss edition. Old v1.4.2 mirror is retained as a superseded alternative. |
| LandMark download authorization and file schema | Resolved after Pete's exact form approval | Official June 2026 ZIP acquired and SHA-256 pinned. Use `landmark_i`, actual community layers and geometry types; retain per-source metadata. |
| AOI, farming systems, growing season and local coverage | Awaiting the pilot country/AOI | These cannot be established from global diagnostic points. No location or completeness assumption is invented. |
| Four-class calibration, DI endpoint equality and representative concern | Scientific interpretation remains pending | Verified native values are usable for review. Dataset access does not approve ordinal thresholds or double-counting choices. |
| Naturebase applicability and area denominator | Context/source applicability remains pending | Retain as an unscored potential descriptor. Zero ocean pixels are not a land/applicability mask; other pathways have not been raster-checked. |

## Drought recurrence

The candidate measures the percentage of valid selected growing seasons where ASI affected area is strictly greater than either 30% or 50%, following FAO's two published event definitions. The user must choose the definition and crop/pasture season for the intended context; neither is silently selected. This is an unclassified frequency, not a new four-level priority score or household-loss estimate.

The checked period contains 42 annual records (1984–2025 inclusive). Eight diagnostic locations produced 336 raw observations: four locations had all 42 valid observations, while four lay outside the selected host system. Observed event counts at the four covered locations were 1, 3, 0 and 3 for >30%, and 0, 1, 0 and 0 for >50%. Native half-percent values survive the F32 export. Special codes are not drought events. A missing/invalid season makes the proposed complete-period value unknown while retaining counts and completeness. This avoids silently changing the denominator. The initial HDF product's rounded integer samples still cannot distinguish its competing 2024/2025 end-year claims; its original hold stays recorded.

`recurrence-vectors.json` reproduces these diagnostics. The review oracle checks the arithmetic and period completeness only. It does not acquire rasters, align spatial grids or approve a pilot method.

## Forest-emissions source identity

The public producer-native route comes from WRI's pinned `carbon-budget` constants. GFW's API declares dataset `gfw_forest_carbon_gross_emissions/v20260327` immutable and links model v1.4.3's 2001–2025 products. The direct data-lake object returned 403; the producer's published source tile is readable through HTTP Range.

A 128×128 window in tile `10S_060W` was read with its exact ETag in `If-Match`; the sample TIFF is hashed. The native tile is float32 at 0.00025°, with **zero declared as nodata**. This differs from derived GFW assets that declare NaN. Do not transfer missing-value conventions between the two routes. ETag is an object consistency validator, not a SHA-256. The recorded S3 version ID is useful provenance, but explicit historical-version GET returned 403; do not claim historical-version access. Record/check fingerprints for every tile a pilot uses and stop if an object changes. Only the diagnostic window is locally cached, not the 727 MB full tile or the global collection.

The producer's `GFW2025` loss input and the existing Hansen 2025 candidate share the year edition. Pixel alignment, exact forest support and local coverage remain run checks. No arbitrary canopy cutoff is introduced; no cumulative total is mislabeled an annual observation.

## LandMark acquisition and coverage

Pete approved the exact professional details, purpose and terms submission. The official page confirmed success and supplied the June 2026 community-data ZIP. It contains **327,379 polygon records** and **2,646 point records**, in **EPSG:3857**. A full streamed attribute audit found only `Indigenous Lands` and `Community Lands`, all marked `download=Yes`, with unique nonempty `landmark_i` IDs within each layer. Polygon metadata has 5,912 missing `data_date` values; do not invent update dates. These are feature counts, not a census of distinct communities or nationally complete coverage.

The shared README includes indicative-layer documentation, but the acquired package's actual layer values exclude that layer. Its text boxes identify a 26 May 2026 version date while the official package is labeled June; preserve the archive hash and both labels rather than equating the API package with this download.

README exclusions include Philippine polygons; some Peruvian polygons; Indonesian and Indian points; Suriname indicative polygons; Montenegrin polygons; livestock-route polygons in Tanzania, Ethiopia and Kenya; and Mongolian pasture-user-group polygons. Thus even an apparently empty country overlay is not evidence of no community lands. Retain the contributing source, its conditions and dates. Polygon area must use an appropriate geodesic/equal-area calculation; points remain presence information and are not buffered into invented land areas. IPLC remains unscored.

The ZIP and technical observations were copied to the existing team-library mirror with matching hashes. Remote SharePoint/team access remains unverified. No canonical source/dataset registration, human scientific review or runtime release is implied.

## Source records

Method's evidence lock resolves all observations at an exact commit. New records are `aqueduct_production_semantics`, `fao_annual_recurrence`, `forest_emissions_producer_pin`, `landmark_current_metadata` and `landmark_official_download`. Each contains provider URLs, source locators, raw-response hashes and limitations. Prior records are unchanged. [Evidence #105](https://github.com/RuralScan/evidence/pull/105) and [method #108](https://github.com/RuralScan/method/pull/108) are the merged starting point, not the new resolution PRs.
