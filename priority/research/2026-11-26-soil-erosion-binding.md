# Soil erosion binding: global context and a finer cropland candidate

26 November 2026. Next non-hazard binding after Pete approved BII as coarse context. The four [approved erosion classes](2026-11-25-soil-erosion-global-classes.md) stay unchanged: 0–1 / >1–3 / >3–5 / >5 tonnes/ha/year. Infrastructure remains an [active optional exposure stream](../infrastructure/README.md), with its selected Haiti fallbacks and national gaps.

## Source choice by land-system coverage

| Candidate | Appropriate scope | Access and remaining limitation |
|---|---|---|
| GloSEM v1.1, 2012, distributed 25 km | Broad global model context spanning cropland, forest and natural-area support | Existing documentation-only candidate remains unchanged. Original 250 m model detail is not present in the distributed 25 km product. ESDAC requests registration and imposes third-party transfer conditions; no request submitted here |
| **GloSEM v1.3, 2019, approximately 100 m** | **Cropland only**, including fractional cropland in mixed cells | Author-published Figshare release is openly accessible under CC0. Exact package and companion crop-support layer identified; no unreviewed substitution across forests or rangelands |

Primary sources: [ESDAC global product](https://esdac.jrc.ec.europa.eu/content/global-soil-erosion), [author collection](https://doi.org/10.6084/m9.figshare.c.5844758.v1), [2019 baseline item](https://doi.org/10.6084/m9.figshare.19181234.v1), and the authors' [Scientific Data paper](https://www.nature.com/articles/s41597-022-01489-x), **Data Records** and **Usage Notes**. The collection DOI's title was checked against DataCite. The paper explicitly identifies Figshare as a distribution route; this is not an unauthorised third-party mirror.

The finer release is a scoped candidate for cropland applications, not a new tenth variable. A finer grid does not imply equally fine observations for every model input. The 2019 label identifies the baseline cropland scenario, not a field measurement of erosion during that year. Do not treat a newer cropland product as a complete replacement for all rural land systems. Keep observation/model period, crop support and source transitions explicit if a future contextual binding uses different sources in different areas. No global source replacement or executable binding is activated in this inspection.

## Exact candidate inputs and interpretation

| Item | Producer metadata |
|---|---|
| Model/version and baseline | GloSEM 1.3, scenario 2019; select this baseline, not a 2070 scenario |
| Erosion file | Figshare article 19181234, file 34079996, `Data2_SOIL_DISPLACEMENT_ESTIMATE_2019.rar`, 16,574,457,781 bytes |
| Raster inside archive | Full archive listing and extraction confirm `Data2_SOIL_DISPLACEMENT_ESTIMATE_2019/SOIL_DISPLACEMENT_ESTIMATE_2019.tif`, 15,087,631,858 bytes uncompressed; archive also contains an external overview and small sidecars |
| Crop support | Figshare article 19181096, file 34079810, `ESA100_Cropland_fraction.tif`, 3,940,398,319 bytes; CGLS-LC100 Collection 3, 2019 |
| Units | Erosion rate: Mg ha−1 yr−1, numerically equal to tonnes/ha/year. Crop fraction: percent |
| Published grid | WGS84, 0.00099 degrees, approximately 100 m near the equator; native metadata must be checked per file |
| Access/licence | Both Figshare item records specify CC0; retain author attribution and exact version/file identity |

The paper's **Usage Notes** states that soil-displacement rates do not include the fractional cropland cover. Classify the rate itself with the approved 1/3/5 breaks. For an eventual cropland total, combine the rate with actual pixel area in hectares and cropland fraction divided by 100; keep a valid crop-support and erosion mask. Multiplying by crop fraction before applying severity bands would change the meaning of the approved classes. Do not interpret absent or unsupported crop cells as Very little erosion in forest or rangeland. No arbitrary cropland-percentage cutoff is adopted here.

The initial bounded HTTP range requests returned 206 with the expected total file sizes and identifiable payloads (RAR5 and BigTIFF). First 65,536 bytes of each were saved and hashed. Parsing the RAR prefix establishes the TIFF entry and compression; it does not inspect the complete archive, raster values, nodata or Haiti erosion coverage. At that initial stage, full-file MD5 values remained provider declarations. The subsequent complete erosion-archive checksum and extraction are verified below; the companion crop file remains range-inspected only. HTTP ETags are object consistency markers, not SHA-256.

## Native crop-support inspection

A bounded, ETag-guarded read of the producer's companion TIFF succeeded using fresh Figshare redirects for each range. The redirects expire quickly; a stale redirected URL returning 403 is not evidence that the public file is inaccessible. The successful probe transferred 50,055,225 bytes, mostly TIFF index metadata, rather than the complete 3.94 GB file.

Verified crop-support properties: EPSG:4326; 362,880 columns × 141,120 rows; 0.0009920634920634888-degree pixels; origin (-180, 80), extent approximately -180 to 180 longitude and -60 to 80 latitude; Int8 percentages; **nodata -128**; 128 × 128 tiles. These are the companion crop raster's properties. The independently verified erosion grid below has the same pixel spacing and northern origin, but fewer rows.

Three diagnostic 5 × 5 Haiti windows were retained. Around (-72.325, 18.54) and (-74.1, 18.64), all 25 cells were nodata. Around (-72.2, 19.5), 13 cells held valid crop fractions of 1–12%, while 12 were nodata. These are diagnostic windows, not a national coverage estimate or evidence that unsupported cells contain no crops. Preserve the native mask and do not turn -128 into zero or a low erosion class. No erosion severity is calculated from crop fractions.

## Completed native erosion-raster checks

Pete authorised full extraction and inspection on 26 November. [CI run 45911571306](https://github.com/RuralScan/method/actions/runs/45911571306) downloaded all **16,574,457,781 bytes**, verified the producer MD5 **ba910ecf8fe95fc60a054c5cc42671d2**, listed the complete RAR and extracted the selected baseline TIFF without error. Archive SHA-256: **35d0456971ffae373b24773054ef24571d1d939df41eb261ed9a133a1eff719e**. Extracted TIFF SHA-256: **03ed8f920fd10c21418f26602a4c7f758d0f1ccae8ae1c752a9945290a9b8d14**. These are full-file digests, unlike the initial prefix hashes. The duplicate laptop download was stopped; its partial file is not the verified full archive.

| Native property | Verified result |
|---|---|
| CRS and grid | EPSG:4326; 362,880 columns × 137,631 rows; 0.000992063492063489-degree pixels; nominal approximately 100 m product |
| Extent | Longitude approximately -180 to 180; latitude **-56.53869047619 to 80** |
| Band / storage | One Float32 band; 128 × 128 blocks; scale 1 and offset 0 |
| Missing code | **-3.4028234663852886e+38**; mask it before classifying. It differs from crop support's -128 |
| Crop alignment | Pixel spacing and northern origin match; the crop raster extends farther south to -60. Align by coordinates and shared footprint, not array shape |
| Paired Haiti windows | All three 5 × 5 windows have the same row/column positions and masks as the independently inspected crop support. Two have no valid cells; the third has 13 valid crop cells (1–12% crop fraction), each with erosion value 200 |
| Sparse encoding check | 288 unresampled 256 × 256 windows, 18,874,368 cells: 1,223,246 valid, including 4,197 valid zeros; no unmasked negative or non-finite values in those windows |

A native-resolution diagnostic extract covers [-74.5, 18, -71.6, 20.1]. It contains **1,301,825 valid erosion cells** and 4,886,166 masked cells. Valid values range from approximately 1.2649 to 200 tonnes/ha/year. Applying the approved 1/3/5 cutoffs read from the classification CSV gives 0 / 3,644 / 19,146 / 1,279,035 valid-cell counts across Very little / Low / Medium / High. These counts test classification handling only: the box includes ocean and neighbouring Dominican Republic, is not clipped to Haiti or an opportunity area, and has no complete paired crop-support read. They are **not Haiti national percentages, cropland areas or loss totals**. Sparse global windows likewise are not representative global statistics.

**Upper-tail limitation:** 390,583 valid cells in that box (approximately 30%) equal exactly 200, including every valid cell in the third small diagnostic window. This observed pile-up is recorded without claiming a documented cap/truncation rule: the inspected article did not establish one. These stored rates fall in the approved High class; retain them and flag the upper-tail uncertainty. Do not infer precise extreme losses or compute a defensible total-loss estimate without clarifying this behaviour and completing paired crop-area support. No arbitrary correction, clipping or new class cutoff is introduced.

## Remaining release work

The native erosion-raster acquisition and encoding hold is closed. Scientific field validation, complete AOI crop-support checks and executable binding integration are separate work. The technical inspection does not change the nine-variable scope, approved four classes or frozen T1/BIND tables. The broader-land-system GloSEM candidate remains uninspected; forest/rangeland coverage must not be filled with the cropland-only product. [Other datasets](2026-11-26-erosion-dataset-alternatives.md) records alternatives and why their process definitions matter.

No new request form, terms agreement or outreach was submitted. No climate-hazard choice is made on Brayden's behalf. Infrastructure remains active using its selected provisional inventories and recorded national-data acquisition needs; the local Haiti gully layer is additional context with partial coverage and unresolved reuse terms, not evidence of avoided infrastructure damage.

## Inspection provenance

Primary article XML was obtained from the Europe PMC full-text service, preserving section locators **Data Records** and **Usage Notes**. Figshare item records, DataCite collection record, original archive/TIFF prefixes, native crop metadata and diagnostic arrays, range hashes and reproducible probe are in the team-library mirror: `0_Methodology_&_Frameworks/priority_classification/soil_erosion_binding_2026_11_26/reviewed_sources.zip`, SHA-256 **f827a81dd8766bb0c8c4530b95ce05c423d4295e3edb6ebc2f32180f30c09163**. Every member and the copied archive were read back and verified; remote SharePoint access was not checked. Formal evidence registration and runtime release are not implied.

The RAR prefix SHA-256 is `f56a08cfbc3e75323ac57322d07b59c62db653505441d6c944ff6259571e3c56`; crop TIFF prefix SHA-256 is `f7c8fc819083bde120ab2c7b20513473cb8cd4ad4012c8e81ea4681448471a6b`. Each prefix is exactly 65,536 bytes, not a full-file digest. `library_versions.json` pins the successful probe's tifffile, zarr, imagecodecs and numpy versions. No provider executable code was run.

The completed native inspection and alternatives packet is retained separately at `0_Methodology_&_Frameworks/priority_classification/soil_erosion_native_inspection_2026_11_26/reviewed_sources.zip`, SHA-256 **5b2e4dd690750f16a44f91313d61fe6b584b23730bef1f1acacfe919e1b35230** (38 members). It includes full-file verification records, archive listing, exact workflow/script, environment versions, original-grid diagnostic TIFF/arrays, paired crop-mask comparison, source snapshots and local Haiti WFS audit. All members and the copied archive were read back and verified; remote SharePoint access was not checked. Large global originals were inspected on an ephemeral runner and remain acquirable from the recorded public producer URL; they are not bundled in this small packet. The one-time CI workflow is removed from the final PR, with its executed version retained in git history and the packet.
