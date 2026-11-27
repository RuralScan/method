# Savanna agroforestry inspection audit

26 November 2026; technical inspection only. No accepted executable binding or analytical rule.

- `provenance.json`: source URLs, HTTP identity, failed COG route, upstream GEE lead and documentation hashes.
- `catalogue_record.json`: producer's public pathway-11 metadata snapshot.
- `inspection.json`: full package member inventory, ZIP/raster SHA-256, native raster metadata, Haiti boundary summary and sample counts.
- `grs_sba_tco2eha_samples.json`: 1,440 original stratified point observations with native row/column plus four diagnostics.
- `haiti_tables.json`: national, 10 department and 42 level-2 records. `NA` remains a literal missing-value marker. Source CSV hashes retained.
- `integrity_checks.json`: archive CRC result, global positive-control pixel and Haiti boundary bounding box.
- `probe_savanna.py`: reused read-only cropland package probe; no source-specific analytical rules. Extracts top-level CSV/TXT/TIF files only.
- `manifest.json`: file hashes, excluding this README and the manifest.

Reproduce with `uv run --with rasterio python probe_savanna.py <zip> <points.geojson> <boundary.json> <fresh-output-directory>`. Original inputs remain in private sibling `carbon-followup-20261126`; hashes pinned in `inspection.json`. Every sampled coordinate is preserved here. Boundary is Earth Engine `USDOS/LSIB_SIMPLE/2017` filtered to `country_na = Haiti`.

Original package and extracted global data stay in private sibling `naturebase-savanna-20261126`, outside the repository. Stratified samples are diagnostics, not area-weighted estimates or ground-truth accuracy measurements. Repeated points within a coarse cell are not independent native observations.

Housekeeping update: exact point and boundary inputs are now included in [the shared diagnostic input archive](../haiti-diagnostic-inputs-20261126/README.md). Original input hashes are unchanged. Use those files in the scratch layout described above; laptop-only input access is no longer required. [Third-party terms](../THIRD_PARTY_NOTICES.md) remain attached to retained source-derived values.
