# Option 2 and mEPM: Haiti coverage and four-class compatibility

26 November 2026 (Colombia time; request confirmation 27 November UTC). Technical inspection requested by Pete. Neither alternative is activated as an executable binding. The nine core variables and optional infrastructure scope remain unchanged.

## Decision status

| Candidate | Haiti coverage established? | Fit to approved four classes | Remaining hold |
|---|---|---|---|
| Option 2: Zheng & Miao global multi-year RUSLE, v2, 1990–2020 | **Not yet.** Global scope is advertised, but the downloaded array has no geographic reference | Conditional: continuous RUSLE rates could use 0–1, >1–3, >3–5 and >5 tonnes/ha/year once units and scale are confirmed | Author-supplied coordinates/geotransform, row/column orientation, units/scale and mask semantics |
| mEPM: ESDAC `mEPM-Figure3b.tif` | **Extent includes Haiti in documentation; valid Haiti cells not yet checked** | Published code bands support a four-class aggregation, with endpoint qualification below | Provider approval/download; native mask, actual Haiti coverage, effective spatial support and endpoint convention |

Do not substitute “global extent” for valid national coverage. No Haiti percentage or class-area estimate is reported for either candidate.

## Option 2: actual file inspection

[Producer v2 record](https://zenodo.org/records/23355150), published 14 October 2026, advertises a 2.5-arc-minute grid and multi-year RUSLE outputs. The selected historical period is 1990–2020; future scenarios are separate. API licence: CC BY 4.0. The record still describes the direct supporting manuscript as under minor revision. Focused searches for the filename plus coordinates and exact manuscript title found no additional verified georeferencing documentation.

The complete `Global_soilloss_1990_2020.mat` download is 23,238,629 bytes. Publisher MD5 matches `4ef8f79711443822842a5a92ed8848a4`; SHA-256 is `7d37b9ddc39174ee0146ff022af28e94532f881454542f45664b97f747b39acf`.

Read using SciPy without executing MATLAB code. The MAT v5 file contains only `A_P2`, a Float32 array with **3,138 rows × 8,640 columns**. There are 6,039,571 finite values, 21,072,749 NaNs, 123,984 finite zeros, no negative values, and a finite range of 0–300. No coordinate arrays, spatial reference, units, scale or offset are embedded. Array shape alone does not establish geographic origin or orientation. Even assuming the advertised angular spacing, the row count covers only 130.75 degrees, not a complete pole-to-pole grid. Do not guess the northern limit or flip the array by visual resemblance.

NaNs must remain unassessed. Zero values cannot be treated as confirmed negligible erosion until the producer explains any masked/background encoding. The maximum of 300 does not by itself prove a cap. No Haiti crop, map or diagnostic class count was generated from guessed coordinates.

## mEPM: published encoding and source interpretation

The [producer README, page 2](https://esdac.jrc.ec.europa.eu/public_path/shared_folder/dataset/93/README.pdf) describes `mEPM-Figure3b.tif` as a Byte GeoTIFF, EPSG:4326, pixel size 0.0083 degrees, extent −180/−90 to 179.99/89.99. Pixel values are **class codes**, not raw tonnes/ha/year. Proposed aggregation:

| Source code | Published interval, t/ha/year | RuralScan label | Ordinal display code |
|---|---|---|---|
| 1 | 0–1 | Very little | 0 |
| 2 | 1–3 | Low | 1 |
| 3 | 3–5 | Medium | 2 |
| 4 | 5–10 | High | 3 |
| 5 | 10–20 | High | 3 |
| 6 | >20 | High | 3 |

Apply a code lookup, **never numeric 1/3/5 thresholds to these pixel codes**. Preserve source nodata and any undocumented code as unassessed; no assumption that source code 0 means “Very little”. Ordinal display codes above are distinct from the framework's normalised MCDA scores. This is a documented candidate crosswalk, not a new accepted runtime rule.

RuralScan's approved continuous-rate convention is upper-inclusive: exact 1, 3 and 5 belong to the lower class. The README writes adjoining intervals without explicit endpoint inclusion. Aggregation preserves the producer's bins, but cannot guarantee identical treatment of those exact boundaries or recover raw rates. Keep that limitation unless the producer confirms its convention.

[Bezak et al., CATENA 2024, section 3.1 and Table 5, printed page 5](https://www.unesco-floods.eu/wp-content/uploads/2023/10/Bezak-et-al.-CATENA-2024.pdf) identify Figure 3 as catchment-averaged results. The distributed filename refers to Figure 3b; **catchment support is therefore a concern to verify, not a confirmed raster property**. Its roughly 1 km grid must not be presented as independent 1 km erosion information before inspection. Inputs mix periods, including WorldClim 1970–2000 and maximum daily precipitation from 2015–2020; catalogue year 2010 does not make every input contemporary with 2010.

The model includes gully/slump processes beyond RUSLE sheet/rill loss. Numerical class compatibility does not make the physical quantities interchangeable. Its reported sediment-yield validation concerns net export at catchment scale, not direct validation of every gross-erosion pixel or Haiti. No Haiti-specific accuracy claim is made.

## Access and next verification

Pete approved the exact ESDAC form and terms on 26 November 2026. It was submitted once; the site confirmed “Your submission has been saved.” ESDAC states manual processing precedes a download email. Initial mailbox check found no ESDAC response. Terms allow use, including commercial use, but prohibit passing source data to third parties; approval to inspect is not permission to redistribute the raster or its subsets in a team library or public notebook. Keep request screenshots and personal details in the private audit folder, outside git.

On receipt: inspect the GeoTIFF's native metadata and code histogram; distinguish nodata from class 1; use a documented Haiti boundary to measure valid land coverage; verify whether repeated classes represent catchment support; preserve source bins and explain unresolved endpoints. Do not resample categorical codes with bilinear interpolation. Option 2 requires producer metadata before that same Haiti check can proceed.

## Infrastructure remains active

[Approved provisional infrastructure sources and national gaps](../infrastructure/README.md#approved-haiti-fallbacks-and-remaining-national-gaps) remain in scope: roads, power lines, buildings, schools and health facilities. Acquire suitable CNIGS/MTPTC, EDH, MENFP and MSPP/SISNU sources to replace or refine global fallbacks. Missing mapped assets remain unknown. Neither coarse erosion dataset establishes asset-level damage, sediment connectivity or avoided losses. Infrastructure exposure awaits suitable hazard footprints and inventory checks.

## Reproduction and provenance

Private audit folder: `erosion-options-20261126` beside this method checkout. It contains the downloaded MAT, exact Zenodo record, checksum verification, reproducible inspection script/results and ESDAC request screenshots. Technical locators are MAT variable `A_P2` and its native row/column indices; no geographic locators are asserted. This bounded inspection does not register dataset contents as SRC/EV evidence or bypass the formal dataset-intake rules.
