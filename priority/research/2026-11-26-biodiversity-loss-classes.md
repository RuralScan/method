# Biodiversity loss: approved four-class interpretation; binding pending

26 November 2026. Pete requested biodiversity review while climate-hazard confirmation is pending, retaining infrastructure. Following presentation of this four-class proposal and its limitations, Pete replied “ok next?”. This records acceptance of the displayed interpretation. A current dataset binding and runtime release remain pending; that response does not verify a raster or approve a new dataset edition.

## Measure and proposed classes

Use the abundance-based Biodiversity Intactness Index (BII) to represent **biodiversity depletion relative to a minimally disturbed reference**. The [Natural History Museum explanation](https://www.nhm.ac.uk/our-science/services/data/biodiversity-intactness-index.html), sections “About the Biodiversity Intactness Index” and “How does the Biodiversity Intactness Index work?”, describes a model combining abundance and compositional similarity. A single BII map describes condition relative to that reference; it does not measure recent annual loss, the percentage of species extinct, or species richness alone.

The approved BII input describes “Modelled depletion relative to an undisturbed reference”. Greater depletion means greater concern for this input. Pete subsequently requested one [Biodiversity priority layer combining BII and KBA proximity](../conservation/README.md); that combined presentation replaces the loss-only menu label while retaining these BII classes unchanged.

| RuralScan display | BII remaining (%) | Depletion score, 100 − BII |
|---|---:|---:|
| None / very little — display as **Very little** | 90–100 | 0–10 |
| Low | 80 to below 90 | Above 10 to 20 |
| Medium | 60 to below 80 | Above 20 to 40 |
| High | Below 60 | Above 40 |

These intervals describe a valid percentage-scale input within 0–100. Exact equality assignments are explicit RuralScan conventions: BII 90 → Very little, 80 → Low, 60 → Medium. In depletion units, 10/20/40 are upper-inclusive, compatible with the contextual table's existing numeric convention. No new endpoint convention or schema extension is needed; a reviewed rule row and verified binding are still required. Missing remains unknown; do not silently clip unexpected values, infer validity from colour, or turn uncovered cells into Very little.

## Published basis and strength of rationale

[UNEP (2021), *GEO-6 for Youth*, printed page 22, Figure 1.5](https://www.unccd.int/sites/default/files/library/1677_G4Y.pdf#page=46), reproduces a **global** BII map attributed to Newbold et al. (2016). Its legend has five bands: below 60%, 60–80%, 80–90%, 90–95%, and above 95%. The proposed crosswalk preserves the first three bands and combines the two most-intact bands. Four concern labels and endpoint equality are RuralScan choices; UNEP does not publish these four loss-severity labels.

NHM identifies 90% as a proposed planetary-boundary reference. That provides a rationale for distinguishing comparatively intact areas, but does not establish a universally safe pixel-level cutoff or literal absence of loss. The 60% and 80% breaks are published **map-display bands**, not demonstrated universal ecological tipping points. This is a transparent published-band convention for scoping, not a claim that all three boundaries have equivalent ecological validation. The global legend avoids calibrating classes from a UK or US distribution.

Alternative screened: *State of Nature 2016*, printed pages 70–71, Figure 46, also displays BII, but uses more bands in a UK view. Its global-model explanation is useful background; it is not the selected classification legend. Equal-width or income-group terciles have not been calculated or substituted.

## Scope and binding limitations

- This measures terrestrial biodiversity condition. It is not a marine or freshwater biodiversity assessment, a threat forecast, or a direct estimate of ecosystem-service loss.
- A low depletion class can contain highly valuable intact habitat. It must not imply low conservation importance or permission to convert that habitat. KBA proximity and protected-area constraints retain their separate meanings. The subsequent combined-priority proposal combines ordinal decision classes, not raw BII with binary designation as if they measured the same quantity.
- BII is modelled from biodiversity observations and mapped pressures. Inspect uncertainty and local ecological relevance; maps are screening evidence, not site surveys or predictions of recovery from a particular NbS.
- The legacy `bii_nhm_global` pointer references the 2016 publication. Its circa-2005 layer must not be labelled current-year loss. *State of Nature 2016*, page 71, explicitly describes the 2005 pressure inputs. Prefer an appropriate newer edition if available and compatible, after confirming its reference state, native resolution, units, valid domain, masks, coverage and access conditions. Do not subtract different model editions to invent a trend.
- The global class convention does not require World Bank income groups. Country/biome adjustments remain possible where better local evidence supports them; record and justify any override.

At the initial class review no current raster had been sampled or selected; the subsequent v2.1.1 inspection below now resolves native units, years, grid and missing-value handling. Existing profile and T5 routing remain held; interpretation approval does not turn an old dataset pointer into an inspected binding. Once the input is selected and its transformation verified, the contextual row can record `method=thresholds`, depletion units, `direction=higher_is_more_concern`, cutoffs 10/20/40, the exact BII-to-depletion transformation, source/version, rationale and limitations. The table's binding currently permits positive scale only, so do not encode `100 − BII` as a silently accepted negative scale or invent a derived input asset. No core rule is activated by this approval record.

Climate hazards remain pending Brayden's reply. The Bank's [infrastructure exposure work](../infrastructure/README.md) stays active alongside the nine problems; this biodiversity proposal does not change that scope or add another problem variable.

## Source preservation

The global legend was visually checked on the original PDF (PDF page 46; printed page 22). Source bytes and locators are in the team-library mirror: `0_Methodology_&_Frameworks/priority_classification/biodiversity_loss_2026_11_26/reviewed_sources.zip`, SHA-256 `f4749c9ac11afc4a5539a912b8b17c754b6517e18992e3cb707061ad5585b8bc`.

| Member | SHA-256 |
|---|---|
| `geo4youth.pdf` | `ccfd8b38ddfc9b1df0e243d5fdb6eac9d381a68862f4dc4b61a73b6ef7b42bd3` |
| `nhm_bii.html` | `9baa9cc37626bd66ba67be981a4d97a370d9ff50d7686fc546107a9cea3ac0a6` |
| `state-of-nature-2016.pdf` | `b80b567977950229623a72f95126531509ac64dd2e06681c8475b8cb3494e510` |

Archive members were read back and verified. Remote SharePoint access was not checked. This is technical proposal provenance, not formal SRC/EV registration or scientific acceptance. Historical profiles and approvals are preserved.


## Next binding inspection: NHM v2.1.1 limited release

26 November 2026 follow-up after selecting provisional Haiti infrastructure sources. The [producer catalogue](https://data.nhm.ac.uk/dataset/bii-developed-by-nhm-v2-1-1-limited-release), resource [c4c281c4-befa-4e1b-a162-ba2f25e5ae82](https://data.nhm.ac.uk/dataset/bii-developed-by-nhm-v2-1-1-limited-release/resource/c4c281c4-befa-4e1b-a162-ba2f25e5ae82), identifies **v2.1.1 (Open Access, Limited Release)**, updated 9 October 2024, as a newer candidate than the legacy Newbold 2016 pointer. The DataCite DOI record was fetched and its title matched the provider's citation.

Pete explicitly approved the download and **CC-BY-NC-SA 4.0** licence for non-commercial inspection. The browser request used “No notification (check status manually)”; no name/email was submitted. Download request d8de77a1-d640-4a1d-8214-34f8aef1d55d completed on 26 November 2026 at 22:17:15, and the actual archive was acquired. Initial command-line HTTP 403 was an access-route issue, resolved through the normal browser. No contact message was sent. The returned outer manifest refers to an older cached request dated 10 November; preserve it alongside the actual request record, not as a new dataset edition.

The ZIP contains five GeoTIFFs and their year sidecars, README and licence. Reading every raster verified the following candidate binding:

| Property | Verified value / interpretation |
|---|---|
| Selected provisional input | **bii-2020_v2-1-1.tif**, band 1; Pete approved use as coarse context on 26 November 2026. Runtime activation remains separate |
| Available observations | **2000, 2005, 2010, 2015, 2020**; not an annual time series |
| Grid | EPSG:4326, 4,320 columns × 2,160 rows, **5 arc-minutes** (0.0833333333 degrees), about 10 km at the equator |
| Coverage | Global raster extent; valid terrestrial support follows the native mask. Extent is not complete local coverage |
| Values | Native Float64, percentage BII **0–100**, scale 1, offset 0, one band |
| Missing | **NaN nodata**; retain the mask. Do not substitute zero, intactness 100 or a Very little class |
| Actual 2020 valid domain | 2,170,764 valid cells; minimum 0.42, maximum 99.96. Across all five rasters: no unmasked nonfinite, negative or above-100 values |
| Approved interpretation | Apply the existing BII remaining-percentage bands, or explicitly derive depletion = 100 − BII before the existing 10/20/40 cuts. Retain boundary equality and raw BII |
| Use conditions | CC-BY-NC-SA 4.0, as approved for non-commercial inspection; never inherit the legacy CC-BY-4.0 label or assume permission for every downstream use |

The original README confirms the percentage units, five years and 5-arc-minute grid. Its native resolution supersedes the unrelated 0.25-degree example-map caption as evidence about this package. This is much coarser than the legacy approximately 1 km pointer: newer observation/model edition does not automatically make it better for every application.

Three diagnostic Haiti locations returned finite 2020 BII values: (-72.325, 18.54) = 3.51; (-74.1, 18.64) = 63.40; (-72.2, 19.5) = 53.72. These verify readable land cells, not national completeness or an opportunity-space result. The diagnostic bounding-box read includes ocean and neighboring territory and must not be reported as Haiti statistics.

**Remaining fit limit:** use this public edition as coarse landscape context only; resampling cannot recover farm-scale variation. Combining its classes with finer KBA distances retains two different spatial supports. Keep each input's resolution and driver visible. The producer offers a complete series and improved resolution on request; finer licensed data may be needed for pilot differentiation. Pete subsequently approved using this edition as coarse context for now; this resolves the provisional source-use choice, while preserving the resolution limitation, source conditions and separate runtime release. The existing positive-scale-only binding transform still cannot silently encode 100 − BII; an explicit reviewed transformation remains required. KBA polygon acquisition remains separate. No additional core variable is introduced.

### Acquired source preservation

Source bytes, the DataCite record, acquisition log, reproducible raster probe and results are archived in the team-library mirror at `0_Methodology_&_Frameworks/priority_classification/bii_binding_2026_11_26/reviewed_sources.zip`, SHA-256 **57e742d788a8bfb0d6e28f7da2d8b2014df5f038691da2f25832d7f01ed7f2af**. Archive members and copied bytes were read back and verified; remote SharePoint access was not checked. This is inspection provenance, not SRC/EV scientific acceptance.

| File | Bytes / SHA-256 |
|---|---|
| Producer download wrapper | 45,890,689 bytes; d5e7dfcaf2fbaac1dd1aeff3139ae753f7f9ba560be4203d5c17a79ac4b314af |
| Nested resource ZIP | 45,890,222 bytes, matching catalogue size; 4bcc68c57396a0e82670f5319fcaeb747d7a52f9d91b21d36ae6a88d099178d1 |
| 2020 GeoTIFF | 10,327,863 bytes; d2142dd8d6d0bf1a08268d9a9a03c7a9b9ab4d834714d7fea35de621559a72b4 |

`probe_bii.py` runs with rasterio 1.5.2 and numpy 2.4.6. Its JSON retains per-raster hashes, grid metadata, domain and missing-value checks and diagnostic locations. Both original archives are preserved through the nested download; no producer executable code was run.


## Approved interim use: coarse context

26 November 2026, Pete: “capture the BII resolution limitation and use it as coarse context for now, then proceed to the next remaining dataset binding. Keep infrastructure in scope too.”

Use NHM v2.1.1's **2020** raster provisionally as **coarse landscape biodiversity context**, retaining its native **5-arc-minute (approximately 10 km)** support. Show the source year and native resolution beside the input and in exported methods/limitations. A finer display or analysis grid does not provide finer biodiversity evidence: preserve the native-cell information and do not interpret interpolated variation as differences between neighboring farms, practices or KBA boundaries. No claim of current-year condition or observed annual biodiversity loss follows.

Keep the four approved BII bands and the approved maximum-of-BII-and-KBA rule, including the driver and each input's spatial support. Until authorised KBA polygons and both inputs' valid coverage are available, show the available BII input as coarse context and the combined Biodiversity priority as **Not assessed**. Do not silently substitute a BII-only combined score. This interim choice adds no core variable or independent BII weight, changes no frozen table or released evaluator, and does not resolve the explicit depletion-transform implementation hold.

Seek a suitable finer, permitted source for local differentiation when needed; its acquisition is not a prerequisite for this approved coarse-context use. National/local sources must retain their geography, period and reference definition rather than inherit global BII units by name. Next non-hazard binding inspection is [soil erosion](2026-11-26-soil-erosion-binding.md). The selected [infrastructure fallbacks and national acquisition gaps](../infrastructure/README.md#approved-haiti-fallbacks-and-remaining-national-gaps) remain active; hazard choices still await Brayden's confirmation.

## Haiti technical follow-up — 27 November 2026

[Exact native-cell intersections and depletion checks](2026-11-27-bii-haiti-binding.md) now verify country-boundary coverage and the numerical reference-minus-input operation. The shared positive-scale-only binding format is not altered; adapter adoption and KBA access remain separate holds. All existing interpretation, resolution and licence limitations remain.
