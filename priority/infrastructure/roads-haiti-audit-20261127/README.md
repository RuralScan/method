# Haiti road geometry inspection — 27 November 2026

This audit checks the selected provisional OSM road inventory and separately inspects the older CNIGS national-source network. It computes Haiti-clipped mapped line lengths by native class, not flood exposure, route kilometres, road condition, accuracy or national completeness. No analytical classification or executable binding is accepted here.

## Inputs and provenance

- OSM © OpenStreetMap contributors, [ODbL 1.0](https://www.openstreetmap.org/copyright), distributed by [Geofabrik](https://download.geofabrik.de/central-america/haiti-and-domrep.html). `acquisition.json` pins the dated `261126` URL, HTTP object metadata and every complete road member. The filename date and object modification time are not feature survey dates. This is a newer object than the 26 November header/attribute-only inspection; that earlier snapshot remains preserved.
- CNIGS main road network from [HDX](https://data.humdata.org/dataset/haiti-roads), observation period 2013–2019. `inputs.json` pins its original ZIP and saved catalogue metadata. The catalogue is archived, with a CC0/no-restrictions licence label but `isopen=false`; retain that metadata inconsistency for source review. Ancillary condition/surface layers are excluded, not concatenated with the main network.
- Exact `USDOS/LSIB_SIMPLE/2017` Haiti fallback boundary in [shared diagnostic inputs](../../research/haiti-diagnostic-inputs-20261126/README.md). Simplified coastline can exclude mapped coastal lines; these results use that declared boundary and do not establish a country-endorsed national total.

The new OSM source members are in the team-library mirror at `0_Methodology_&_Frameworks/priority_classification/roads_haiti_2026_11_27/reviewed_sources.zip`, SHA-256 `07c56d1d1d9a732addad510c0df1afd4e60253fb07d19a994d5eff5988feb494`. All member hashes were checked after archive write. Remote SharePoint access was not verified. The national archive path/hash is in `inputs.json`; extract its `cnigs_roads.zip` member unchanged.

Large geometries remain outside Git. Summaries and code are RuralScan modifications, not provider-certified products; source-data rights are not replaced by the repository code licence.

## Replay

Use Python with pyshp 2.3.1, Shapely 2.1.2 and pyproj 3.7.2. Extract the archived OSM members and `acquisition.json` to a fresh directory. From repository root:

```sh
uv run --with pyshp==2.3.1 --with shapely==2.1.2 --with pyproj==3.7.2 python priority/infrastructure/roads-haiti-audit-20261127/analyze.py /path/to/osm-road-members /path/to/cnigs_roads.zip priority/research/haiti-diagnostic-inputs-20261126/boundary.json /tmp/roads-haiti-recheck.json
cmp priority/infrastructure/roads-haiti-audit-20261127/inspection.json /tmp/roads-haiti-recheck.json
python3 priority/infrastructure/verify_infrastructure.py
```

`acquire.py /new/scratch/directory` is the separate network-dependent acquisition route. It requests only complete road members from the dated ZIP, guards all ranges with one ETag, checks Content-Range and ZIP member CRCs, and hashes the resulting bytes. The full multi-layer ZIP was not acquired. Dated provider URLs may expire; the preserved archive supplies the replay inputs.

## Methods and limits

Every source feature is checked for empty, invalid, non-line and non-simple geometry. Invalid geometry would be excluded and counted; no repair is attempted. Valid non-simple lines remain flagged: self-intersection does not itself make a line invalid. Positive-length intersections with the pinned Haiti polygon are retained, then measured on the WGS84 ellipsoid. CNIGS is transformed from EPSG:32618; OSM is already EPSG:4326. Lengths are summed per native class and rounded to six decimals only for reproducibility, not as an accuracy claim.

Duplicate checks compare normalized, clipped geometry, irrespective of direction, and count repeated source IDs separately. No deduplication is applied. These checks do not detect near duplicates, partial overlaps, displaced parallel lines or network connectivity defects. `OBJECTID` is only a CNIGS snapshot record identifier; it is not demonstrated stable across releases. Blank CNIGS `cod_tronc` cannot be substituted as a unique ID.

All OSM classes remain explicit. `unclassified` is retained as a native road-class value, distinct from `unknown`; no arbitrary regrouping or severity classes are introduced. Bridge/tunnel encodings are preserved without interpreting missing/default values as verified absence. A downstream road-only selection must declare included classes before computing totals. Hazard coverage, opportunity-space boundaries, facility identities and source replacement are separate steps.
