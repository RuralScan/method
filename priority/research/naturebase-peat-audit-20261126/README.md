# Peat pathway inspection audit — 26 November 2026

Research inspection only. Neither pathway is scientifically accepted or runtime-ready for Haiti. See [findings](../2026-11-26-naturebase-peat-bindings.md).

## Contents

- `catalogue_records.json`: public Naturebase metadata for pathways 17 and 30.
- `wet_per/` and `wet_ipm/`: acquisition headers, complete original archive inventory, SHA256/CRC verification for selected scientific members, raster inspection, samples and 53 Haiti administrative rows each.
- `drainage_checks.json`: exact GEE asset metadata, native-grid counts and masks for FAO 2018 drainage and the community Global Peatland Map.
- `peatmap_checks.json`: original North America ZIP hash, source projections, pre-filter feature counts and Haiti-intersecting feature IDs. The `AREA` source attribute is preserved without assuming its units or summing it as eligible hectares.
- `positive_controls.json`: first positive native cell encountered by row-major block search in each Naturebase file, outside Haiti. This is a basic file-content check, not a global validation sample.
- `hosted_access.json`: restoration advertised COG returns 404; management metadata contains no COG URL.
- `provenance.json`: dates, source links, analytical status and acquisition scope.
- `manifest.json`: SHA256 of all audit files except itself and this README.

## Reproduction

Use a fresh scratch directory. Copy `catalogue_records.json` and `acquire_members.py` there, then run `uv run --with remotezip python acquire_members.py`. This retrieves top-level CSV/TXT/TIF members by HTTP ranges and assembles local subset ZIPs. Original full Naturebase ZIPs were not downloaded or hashed. Embedded GDB members were inventoried only; no whole-archive CRC claim is made.

Run `uv run --with rasterio python probe_peat.py <selected.zip> <points.geojson> <boundary.json> <fresh-output-directory>`. Original point and boundary SHA256 hashes are in each `inspection.json`; current originals remain in private sibling `carbon-followup-20261126/stratified_points.geojson` and `boundary.json`. Sample coordinates are preserved in this audit. Boundary is GEE `USDOS/LSIB_SIMPLE/2017`, filtered to Haiti. Four extra diagnostic points in sample files are excluded from the 1,440 stratified count.

With authenticated Earth Engine access, `uv run --with earthengine-api python probe_drainage.py` reproduces native-projection support checks without filling masks. Country pixel counts differ across grids and are not areas. A zero sum with zero unmasked observations is not observed absence.

Download the public PEATMAP archive from the source URL in `peatmap_checks.json`, then run `uv run --with fiona --with shapely --with pyproj python probe_peatmap.py <North_America.zip> <boundary.json> <output.json>`. Counts are taken before applying the spatial filter; intersections are checked after transforming the Haiti boundary into the source CRS.

Run `uv run --with rasterio python probe_positive_controls.py <wet_per.tif> <wet_ipm.tif> <output.json>` to repeat the positive-cell control. Run `python3 verify_audit.py` for compact internal consistency and manifest checks. These checks establish reproducibility of inspected outputs, not Haiti ground-truth accuracy or model validity.

Global rasters/ZIPs and raw boundary geometry are not committed here. Original private cache: `../naturebase-peat-20261126` relative to the method checkout. Current public files may change; compare saved headers/member hashes before claiming a byte-identical rerun. Locally assembled subset ZIP hashes can change with ZIP metadata even if selected members are identical.

Housekeeping update: exact point and boundary inputs are now included in [the shared diagnostic input archive](../haiti-diagnostic-inputs-20261126/README.md). Original input hashes are unchanged. Use those files in the scratch layout described above; laptop-only input access is no longer required. [Third-party terms](../THIRD_PARTY_NOTICES.md) remain attached to retained source-derived values.
