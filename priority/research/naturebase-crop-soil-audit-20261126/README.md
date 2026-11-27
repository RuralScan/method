# Cropland soil-carbon audit — 26 November 2026

Haiti coverage verified; scientific acceptance and runtime readiness remain false. [Findings](../2026-11-26-naturebase-crop-soil-binding.md).

- `catalogue_records.json`: public Naturebase pathway 14 metadata and request URL.
- `crp_scc/acquisition.json`: original ZIP HTTP headers/inventory and SHA256/CRC results for five selected CSV/TXT/TIF members. The full original archive was not downloaded or hashed. Embedded GDB files were not inspected.
- `crp_scc/inspection.json`: native raster metadata, input hashes, full Haiti cell-centre statistics and land-cover sample summaries.
- `crp_scc/crp_scc_tco2eha_samples.json`: 1,440 stratified samples and four separately labelled diagnostic points.
- `crp_scc/haiti_tables.json`: 53 source administrative records, retaining the one admin2 `NA`.
- `summary.json`: administrative sums and raster results, with no correction of discrepancies.
- `soils_revealed_datacite.json`: primary deposited metadata; source title and v3.0 match verified. This is not an acquired upstream raster or a formal SRC registration.
- `hosted_access.json`: advertised Naturebase COG returned 404; upstream Dataverse API returned 403.
- `provenance.json`: date, scope, status, sources and private snapshot hash.
- `manifest.json`: SHA256 of audit files excluding itself and this README.

## Reproduction

In a fresh scratch directory, copy `catalogue_records.json` and `acquire_members.py`, then run `uv run --with remotezip python acquire_members.py`. This downloads selected scientific members using HTTP ranges and assembles a local subset ZIP. Its package hash is **not** a hash of the original producer ZIP, and may vary with local ZIP metadata; compare individual member hashes.

Run `uv run --with rasterio python probe_crop_soil.py <selected.zip> <points.geojson> <boundary.json> <scratch/crp_scc>`, then run `summarize.py` from the scratch root. The latter uses files under its own sibling `crp_scc/` directory. The checked original raster has SHA256 `30848493d1cbd1e89b778c491617c3c1816f30d3745d519cd65c3199e40806ae`.

Original samples and boundary remain in private sibling `carbon-followup-20261126/stratified_points.geojson` and `boundary.json`; hashes are recorded in `inspection.json`. Boundary: GEE `USDOS/LSIB_SIMPLE/2017`, Haiti. Native cell-centre convention; no inferred hectares from pixel counts. Samples retain coordinates and IDs here and are stratified, not area-weighted.

`python3 verify_audit.py` checks counts, source/member consistency, administrative missingness, arithmetic and saved file hashes. These are data-inspection checks, not model validation or tests of local intervention effects.

Global binaries remain in private sibling `naturebase-crop-soil-20261126/`. This initial inspection did not verify Soils Revealed source rasters. The subsequent [component audit](../crop-soil-components-audit-20261126/README.md) acquired and checked all three originals. Full Naturebase geodatabase, local adoption baseline and equivalence between its bundle and upstream components remain unverified. Retain source-specific licence conditions before later reuse. No class or analytical threshold was created.

Housekeeping update: exact point and boundary inputs are now included in [the shared diagnostic input archive](../haiti-diagnostic-inputs-20261126/README.md). Original input hashes are unchanged. Use those files in the scratch layout described above; laptop-only input access is no longer required. [Third-party terms](../THIRD_PARTY_NOTICES.md) remain attached to retained source-derived values.
