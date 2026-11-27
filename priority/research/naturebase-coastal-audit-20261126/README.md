# Coastal restoration inspection audit

26 November 2026. Technical inspection only; no accepted binding or classification.

- `provenance.json`: source routes, HTTP identity, component-listing result and documentation hashes.
- `catalogue_record.json`: public pathway-16 metadata.
- `inspection.json`: full ZIP inventory, hashes, raster header, sample summaries and Haiti cell-centre result.
- `wet_cwr_tco2eha_samples.json`: 1,440 stratified point observations and four diagnostics.
- `haiti_tables.json`: all Haiti producer CSV records; source hashes and trailing unnamed blank columns retained.
- `integrity_checks.json`: archive CRC, embedded geodatabase schemas, all-touched sensitivity and administrative sums.
- `haiti_geodatabase_rows.json`: Haiti identity and coastal fields only, including the unusable `wet_cwr_ha` values.
- `component_listing.xml`: public listing under `Data-download/wet_`; not a claim to have inspected every publisher storage location.
- `upstream_zenodo_record.json`: mangrove-only archive metadata and file routes.
- `upstream_haiti_records.json`: national mangrove row and acquired export/CSV hashes. Carbon values are stock quantities from a different accounting model; no annual conversion made.
- `probe_coastal.py`: read-only native-raster and boundary probe reused from previous inspections.
- `manifest.json`: SHA-256 hashes excluding this README and manifest itself.

Reproduce raster inspection with `uv run --with rasterio python probe_coastal.py <zip> <points.geojson> <boundary.json> <fresh-output-directory>`. Input hashes are in `inspection.json`; originals remain in private sibling `carbon-followup-20261126`. Sample coordinates are preserved here. Boundary: `USDOS/LSIB_SIMPLE/2017`, `country_na = Haiti`; cell-centre convention, with all-touched sensitivity recorded separately.

Global ZIP, extracted raster/geodatabase, mangrove export ZIP and original READMEs remain in private sibling `naturebase-coastal-20261126`. Geodatabase schemas and Haiti attributes were read with Fiona/OpenFileGDB; downloaded source code was not executed. No raw global raster or geometry is added to the repository.

Current WorldCover mangrove samples are not historical restoration-ground-truth points. Administrative totals cover combined coastal mitigation, not mangrove-only benefits. `wet_cwr_ha` is preserved for diagnosis, not accepted as hectares; no inferred correction was applied.

Housekeeping update: exact point and boundary inputs are now included in [the shared diagnostic input archive](../haiti-diagnostic-inputs-20261126/README.md). Original input hashes are unchanged. Use those files in the scratch layout described above; laptop-only input access is no longer required. [Third-party terms](../THIRD_PARTY_NOTICES.md) remain attached to retained source-derived values.
