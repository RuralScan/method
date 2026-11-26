# Road infrastructure: first binding inspection

26 November 2026. Next dataset-binding work after adding the separate [KBA conservation overlay](../conservation/README.md). This advances the Bank's active [infrastructure exposure request](README.md). It is a technical source inspection, not a selected pilot inventory, accepted BIND record, road-quality classification or computed exposure result.

## Acquisition and observed schema

Candidate route: OpenStreetMap (OSM) through [Geofabrik regional extracts](https://download.geofabrik.de/). The provider's [technical documentation](https://download.geofabrik.de/technical.html), “JSON index of all downloads”, supplies `index-v1-nogeom.json`; its regional ID and URLs permit deliberate extract selection. PBF retains fuller tagging than the provider's selected Shapefile attributes. Prefer a fit-for-purpose country inventory where available; a hosted equivalent must retain required road classes, provenance and coverage before substituting it. No fitness-equivalent server-side road route has been verified in this inspection.

A [Haiti and Dominican Republic extract](https://download.geofabrik.de/central-america/haiti-and-domrep.html) was used only as a diagnostic because Haiti appears in the existing visual example. This does not select the pilot country. The provider index resolved the actual URL:

`https://download.geofabrik.de/central-america/haiti-and-domrep/haiti-and-domrep-latest-free.shp.zip`

HTTP Range reads guarded by `If-Match` inspected the ZIP directory, complete roads DBF, PRJ and first 100 SHP bytes. Each response retained the same ETag. Only 2,274,149 bytes were transferred from the 200,068,505-byte archive; the full geometry was not acquired or checked.

| Observed property | Value |
|---|---|
| Object Last-Modified | 2026-11-26 15:30:28 UTC; object time, not individual feature survey dates |
| ETag | `"beccd99-6612f9f91c52a"`; object consistency marker, not a file SHA-256 |
| Member prefix | `gis_osm_roads_free_1` |
| Header geometry type | 3, PolyLine; does not establish individual feature validity |
| PRJ | WGS 84 geographic coordinates in degrees |
| DBF records | 332,090 across the combined extract; includes road and non-road classes |
| Actual fields | `osm_id`, `code`, `fclass`, `name`, `ref`, `oneway`, `maxspeed`, `layer`, `bridge`, `tunnel` |
| Actual `fclass` values | 28, including road classes, tracks, footways, paths, cycleways, steps and unknown |

The complete attribute inspection found 30,262 `path`, 11,814 `footway`, 533 `steps` and 12 `unknown` records. These are feature-record counts, not road kilometres or proof of completeness. `osm_id` is a character field; preserve it as text. Its uniqueness and geometric segmentation have not been verified. The [OSM highway definition](https://wiki.openstreetmap.org/wiki/Key:highway) also covers paths and related features, so a blanket `highway=*` query is not a road-only inventory.

## Proposed binding behaviour

- Retain `fclass`; define the included road classes in configuration before computing totals. Report rural tracks separately unless the inventory scope explicitly includes them. Keep pedestrian paths/steps and unknown classes separately, rather than silently counting them as motor-road length or discarding their existence.
- Keep bridges and tunnels visible. Two-dimensional overlap cannot establish that a bridge deck or tunnel is inundated; these segments require qualification rather than a damage claim. Preserve source encodings until their meaning is verified; no meaning is assigned here to blank or default attribute values.
- Clip actual line geometry to the declared screening area and valid hazard coverage. Calculate geodesic or suitable projected lengths in kilometres, never degrees. Report mapped length, assessed length, potentially exposed length and unassessed length by included class. Hazard definition, event/return period and exposure threshold must be explicit. No exposure percentage without its assessed-length denominator.
- Deduplicate overlapping extracts and review multipart/segmented ways. Parallel carriageways may be separate mapped lines: label outputs mapped line-kilometres, not unique route-kilometres, unless a corridor-collapse method is adopted.
- Freeze source bytes/hash and timestamp for each analysis. The inspected `latest` object is mutable; the provider's dated files are preferable where available. An OSM update timestamp is not a guarantee of current field conditions. ODbL attribution and applicable data/output obligations accompany use.

## Remaining holds and next inventory

Source access and actual road-layer fields are verified. Full geometry checks, pilot-country selection, local completeness comparison, configured class list, retained dated extract and compatible hazard selection remain outstanding. These limitations prevent a claim that the road binding is release-ready. No data-quality or exposure severity cutoffs are invented.

Next inventory is **health facilities and schools**, prioritising suitable national inventories; retain power lines and buildings where coverage permits. Facility presence, absence and inventory completeness need separate checks. Brayden's hazard confirmation remains pending. The KBA work and infrastructure inventory work do not add problems to the nine-variable core menu.

## Preserved inspection

Reviewed provider pages, the extraction script, source manifest, road DBF, PRJ, SHP header and inspection summary are stored in the existing team-library mirror:

`0_Methodology_&_Frameworks/priority_classification/kba_infrastructure_2026_11_26/reviewed_sources.zip`

Archive SHA-256: `9b3700255c41c4cb8adc0248ae241557a78cec51bccd8f6ee74a2b6d40e3dcb4`.

Road DBF SHA-256: `93489f4801cd53ba5ddf19199926773beed52f94c68742e38c5bd1ed02b7caa0`.

Inspection JSON SHA-256: `61f4df3e2c675747103eec7eb499b5dca4ab7161aac2c475156e805c6d61a830`.

Archive members were read back and hash-verified. Remote SharePoint/team access was not checked. This technical research does not bypass the formal dataset-intake/evidence route or create an acceptance receipt in the evidence-pinned binding catalogue. No KBA polygons were acquired in this archive.
