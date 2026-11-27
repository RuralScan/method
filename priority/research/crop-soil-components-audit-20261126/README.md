# Cropland component audit — 26 November 2026

See [findings](../2026-11-26-crop-soil-components.md). This audit separates upstream candidates; it does not decompose Naturebase's combined raster or activate a binding.

## Acquired and checked

- Two original biochar TIFFs and their README, obtained through Harvard Dataverse's public browser download controls. File IDs and CC0 licence are recorded in `provenance.json`; SHA256, MD5 and byte lengths in `biochar_checks.json`. Full producer MD5 strings were not independently compared; recorded MD5 values are computed local hashes.
- `biochar_checks.json` and two `*_samples.json` files retain native-grid Haiti results, masks, diagnostics and sample identifiers. JSON records the TIFF's NaN nodata as the string `NaN`.
- `HA17D3_datacite.json` / `Y6NGFM_datacite.json` pin source titles, versions and deposited metadata. Crossref responses verify titles of the two cited scientific articles; no formal SRC promotion is implied.
- The three Soils Revealed GEE collections were probed. `component_checks.json` records their not-found-or-inaccessible responses; these are access failures, not zero-coverage results.
- Producer application code is pinned to commit `9eb9e12a434d997edaacd52f935d0d5fe9a819d7` of `Vizzuality/soils-revealed`. `soc-stock-future-change.js` maps scenario names to GEE collections; `soils_revealed_constants.js`, future metadata around lines 1065–1080, defines meanings, time period, limitations and licence. Software licence does not replace dataset licence.

## Soil originals: approved and Haiti checked

User explicitly approved the CC BY 4.0 **Accept** action and all three downloads on 26 November 2026. No name/email was submitted. All three global originals were acquired through the approved browser download controls, and every MD5 matched its publisher file page. Full SHA256, MD5 and byte counts are in `soil_raster_checks.json`. Earlier HTTP 403 and GEE errors remain historical access observations, not evidence of no coverage.

`fetch_haiti_windows.py` acquired native input and joint Haiti windows through HTTP Range GET from their official Dataverse original-file endpoints, with no resampling. `crop_I_window_provenance.json` and `crop_MGI_window_provenance.json` record source IDs, global headers and exact windows. Temporary signed transport URLs are not retained. The approximately 300 KB TIFF clips remain private; hashes in `soil_window_checks.json` refer to those subsets, **not the global-file producer checksums**.

`soil_window_checks.json` and the three `*_window_samples.json` files verify all three soil scenarios on the same native Haiti footprint, their sparse support against independent WorldCover samples, and the joint-versus-sum comparison. `crop_MG_raster_checks.json` and `crop_MG_original_samples.json` preserve the first complete-original inspection. Full-original verification is now complete: `soil_raster_checks.json` and the three `*_original_samples.json` files independently reproduce all native subset statistics, masks, 1,440 sampled values and the joint-versus-sum comparison. All three producer MD5 checksums match.

The original global binaries, browser terms screenshot and available webpage snapshots remain in private sibling `crop-soil-components-20261126/`; they are not included in this compact audit.

## Reproduction

Download `bc_100_tech.tif` (file 7354744), `bc_100_constrained.tif` (7354742) and `ReadMe.txt` (7354746) from the dataset URL in `provenance.json`. Place the TIFFs beside `probe_biochar.py`. Run `uv run --with rasterio python probe_biochar.py` in a scratch copy. The script expects a sibling `../haiti-diagnostic-inputs-20261126/` directory containing `boundary.json` and `stratified_points.geojson`; input hashes are recorded. Preserve masks. Sample points are a stratified diagnostic, not an area-weighted survey.

`uv run --with earthengine-api python probe_components.py` repeats the source-code-derived GEE access check with authenticated Earth Engine. It must not replace failed assets with guessed paths or fill their absence with zeros. If access becomes available, it queries 2038 and saves native-grid and sample results. That code path was not exercised successfully in this inspection.

For soil checks, put the downloaded no-till original beside `fetch_haiti_windows.py` and `probe_soil_rasters.py` in the same scratch layout. Run `uv run --with rasterio python fetch_haiti_windows.py`, then `uv run --with rasterio python probe_soil_rasters.py --haiti-windows`. The first script reads only the required native windows from the two approved public originals. Generic Python HTTP requests may return 403 where curl succeeds; the acquisition script uses curl for the public redirect and GDAL range reads. It does not need account credentials. For complete-original verification, place all three exact producer filenames beside the probe and omit `--haiti-windows`.

`python3 verify_audit.py` validates recorded biochar support, soil masks and sampled non-additivity, approval/acquisition status, producer checksum where acquired, and manifest hashes. These checks are not field validation. `manifest.json` covers audit files except itself and this README.

Shared original inputs are now included in [the diagnostic input archive](../haiti-diagnostic-inputs-20261126/README.md); copy them into the documented scratch layout. [Third-party terms](../THIRD_PARTY_NOTICES.md) apply to source data and the preserved producer code.
