# Cropland agroforestry inspection audit

Read-only technical inspection, 26 November 2026. No accepted binding or rule.

- `provenance.json`: source URLs, access result, source hashes and publication/HTTP identity.
- `catalogue_record.json`: public producer record used to discover download and COG URLs.
- `inspection.json`: package/raster hashes, native header, Haiti boundary and sample summaries.
- `crp_cba_tco2eha_samples.json`: all 1,440 stratified observations plus four diagnostics, coordinates and native pixel indices.
- `haiti_tables.json`: Haiti administrative rows only; source CSV hashes preserved. `NA` remains literal `NA`.
- `zip_inventory.json`: full outer archive member inventory; nested archive not recursively inspected.
- `probe_cropland.py`: read-only reproducible header, raster sample and boundary check. Extracts only top-level CSV/TXT/TIF files, does not execute downloaded contents.
- `manifest.json`: SHA-256 of audit files, excluding this README and manifest itself.

Run with `uv run --with rasterio python probe_cropland.py <downloaded-zip> <stratified_points.geojson> <boundary.json> <output-dir>`. Use a fresh output directory. Input hashes are pinned in `inspection.json`; original points and boundary remain in the private sibling `carbon-followup-20261126` directory. All point coordinates used by the probe are also preserved in the sample observations. National boundary is the Earth Engine `USDOS/LSIB_SIMPLE/2017` feature collection filtered to `country_na = Haiti`.

Sample counts are stratified diagnostics, not accuracy statistics or area-weighted estimates. Multiple 10 m WorldCover sample points can fall in one Naturebase cell. National mask uses cell centres, not all-touched inclusion. No national mitigation total is reconstructed from geographic raster cells.

Housekeeping update: exact point and boundary inputs are now included in [the shared diagnostic input archive](../haiti-diagnostic-inputs-20261126/README.md). Original input hashes are unchanged. Use those files in the scratch layout described above; laptop-only input access is no longer required. [Third-party terms](../THIRD_PARTY_NOTICES.md) remain attached to retained source-derived values.
