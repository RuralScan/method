# Reforestation inspection audit

26 November 2026; read-only technical inspection. No accepted binding or analytical rule.

- `provenance.json`: source URLs, HTTP identity, upstream documentation hashes and pool-method locator.
- `catalogue_record.json`: public producer pathway-4 metadata, including contradictory pool listing.
- `inspection.json`: package inventory/hashes, native raster metadata, boundary and sample summaries.
- `for_ref_tco2eha_samples.json`: 1,440 stratified observations with coordinates/native indices, plus four diagnostic sites.
- `haiti_tables.json`: producer's 1 national, 10 department and 42 level-2 records, with source CSV hashes.
- `integrity_checks.json`: archive CRC, boundary bounds, top-level members and administrative sums; differences are retained, not normalised away.
- `figshare_record.json`: version-3 author archive metadata and download URLs; archive rasters not acquired.
- `gee_asset_checks.json`: failed metadata reads for three asset references found in archived author code. Failure may reflect access restrictions or missing assets.
- `probe_reforestation.py`: reused read-only package probe; extracts top-level CSV/TXT/TIF files without executing downloaded contents.
- `manifest.json`: SHA-256 of audit files, excluding this README and the manifest itself.

Reproduce using `uv run --with rasterio python probe_reforestation.py <zip> <points.geojson> <boundary.json> <fresh-output-directory>`. Original point and boundary inputs remain in private sibling `carbon-followup-20261126`; hashes pinned in `inspection.json`. All sampled coordinates are retained here. Boundary: Earth Engine `USDOS/LSIB_SIMPLE/2017`, filtered to `country_na = Haiti`.

Original global package, extracted files and archived author README/code remain in private sibling `naturebase-reforestation-20261126`. Producer code was read, not executed. The direct Europe PMC full-text request timed out; paper Methods were inspected through the publisher's indexed text and cross-checked against author code and package documentation.

Sample strata use WorldCover 2021 and do not independently identify managed systems or eligible restoration. Multiple points can occupy one coarse pixel. Native cell counts are not feasible hectare counts. Administrative sums differ from the producer's national record; downstream users must preserve that distinction.

Housekeeping update: exact point and boundary inputs are now included in [the shared diagnostic input archive](../haiti-diagnostic-inputs-20261126/README.md). Original input hashes are unchanged. Use those files in the scratch layout described above; laptop-only input access is no longer required. [Third-party terms](../THIRD_PARTY_NOTICES.md) remain attached to retained source-derived values.
