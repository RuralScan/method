# Health facilities and schools: binding follow-up

26 November 2026. Advances the Bank's infrastructure exposure request after the [road inspection](2026-11-26-roads-binding.md). The [KBA distance bands and maximum-of-BII-and-KBA interpretation](../conservation/README.md) are approved. Infrastructure remains an optional exposure stream alongside the nine core priorities.

## Source choice

Prefer a current, suitable national health-facility master list and education-ministry school inventory. WHO's [Geolocated Health Facilities Data initiative](https://www.who.int/news-room/questions-and-answers/item/global-health-facilities-database), “What is the purpose?” and “Why only four data elements?”, supports country-maintained lists with identifiers, names, types and locations. This initiative is not evidence that a complete, current global download has been acquired.

Haiti is a diagnostic example inherited from the visual method, not a new pilot-country decision. [MSPP's official tools page](https://mspp.gouv.ht/services-et-outils) identifies its Carte Sanitaire. Direct retrieval of the mapping site timed out in this inspection; that does not establish that it is inaccessible to users. The [HaitiData portal](https://haitidata.org/) returned its application shell, not a verified downloadable school inventory.

The HDX website page for health data returned 403 through the web tool, but its public catalogue API and actual Shapefile download worked. The API therefore resolved this access obstacle without an access request.

| Candidate | What was actually verified | Remaining limitation |
|---|---|---|
| [PAHO/WHO Haiti health sites on HDX](https://data.humdata.org/dataset/location-of-health-facilities-hospital-in-haiti) | Metadata plus full 48,633-byte Shapefile ZIP; 730 records in a WGS 84 point layer; 250 lack geometry; names, category, institution type/code and coordinates | Catalogue period ends July 2023; resource updated December 2023. Current operation, administrative attribution and completeness are not established |
| [MENFP education facilities on HDX](https://data.humdata.org/dataset/haiti-education-facilities) | National education-ministry source and XLS download route identified in catalogue | Metadata dates observations September 2021; filename says 2022 and resource updated September 2022. Workbook not inspected or adopted; no inferred 2026 coverage |
| [Geofabrik OSM regional extract](https://download.geofabrik.de/central-america/haiti-and-domrep.html) | Full point and polygon POI layers acquired through guarded range requests; actual fields and class counts inspected | Combined Haiti/Dominican Republic extract; incomplete mapping and duplicate representations need checking; no current operating-status field |

Keep national lists as the preferred route and OSM as a transparent fallback or gap-check. Do not silently union inventories or assume two records represent two facilities. Country overrides need the actual source, date and coverage assessment.

## Observed health-file details

Actual PAHO/WHO fields include `Institutio` (institution name), `Cat?gorie` (damaged category header), `Institut_1` (observed ownership/type labels), `Institut_2` (numeric institution-code candidate), `LatDD`, `LongDD` and administrative fields. Preserve native column identity and damaged text until an explicit mapping is reviewed; do not silently guess repaired labels or code stability.

Typed record/geometry inspection found **250 null geometries and missing coordinate pairs**, leaving 480 located records at 371 distinct coordinate pairs. Shared coordinates can represent co-located facilities or duplicated/geocoded records; do not collapse them without review. There are 29 missing institution codes and 5 repeated-code excess records among 701 nonmissing codes (696 distinct). Raw DBF missing-number markers must decode as missing, not as populated values or zero. The `adm1_fr` column contains only four labels: Artibonite 436, Ouest 126, Centre 100 and Nord 68. Geometry spans a wider bounding extent. Administrative attribution and true coverage need checking against authoritative boundaries before this is used as a national inventory. Do not infer that blank areas have no facilities or treat the bounding box as complete coverage.

The catalogue describes operating facilities, but its period and resource dates cannot establish present-day operation. The native table has no explicit current operational-status or per-facility update-date column. Metadata freshness is distinct from observation freshness. The older XLS resource in the same health package was not substituted for the inspected Shapefile.

## Observed OSM fallback

The previously inspected road archive remained unchanged: ETag `"beccd99-6612f9f91c52a"`, Last-Modified 2026-11-26 15:30:28 UTC. Guarded HTTP Range reads acquired complete `gis_osm_pois_free_1` and `gis_osm_pois_a_free_1` layers, including DBF, SHP, SHX, PRJ and CPG, transferring 3,386,969 bytes. WGS 84 coordinates and UTF-8 encoding are explicit. ETag is a consistency marker, not a content hash; individual member hashes are preserved.

Both attribute tables have only `osm_id`, `code`, `fclass`, `name`. They do not provide enrolment, beds, staffing, operating status, service capacity, access restrictions or per-feature observation dates. Retain OSM IDs as text, qualified by source/layer; a feature ID is not necessarily a stable facility identifier.

| Native class | Point records | Polygon records |
|---|---:|---:|
| school | 5,340 | 1,643 |
| hospital | 1,336 | 329 |
| clinic | 260 | 115 |
| doctors | 122 | 28 |

Counts cover the combined extract, **not Haiti alone**, and are not deduplicated institution counts. School names are blank for 487 point and 433 polygon records. Missing names do not mean nonexistent schools. Kindergartens, colleges, universities, pharmacies and other health-related classes are also present; retain their native type rather than automatically folding all education or healthcare features into the requested categories.

OSM supports both point and area representations of [schools](https://wiki.openstreetmap.org/wiki/Tag:amenity%3Dschool) and [healthcare facilities](https://wiki.openstreetmap.org/wiki/Key:healthcare). Preserve both when acquiring data, then reconcile duplicates. Use actual polygons for footprint overlap where present; do not invent an area by buffering a point. One campus can contain multiple buildings or institutions, so the counting unit must be explicit.

## Binding and exposure rule

For the next configuration proposal, keep schools separate from hospitals/clinics and retain other types as optional classes. Prefer authoritative facility IDs where verified; otherwise retain provenance and a reviewed deduplication key. No national inventory is chosen merely because a file can be downloaded. All selected OSM school/hospital/clinic/doctors geometries passed basic nonempty/validity checks in both layers; this does not verify positional accuracy, current existence or cross-layer uniqueness.

Report mapped, assessed, potentially exposed and unassessed facilities by type after deduplication and coverage review. A point supports location-based exposure; a campus polygon supports footprint intersection. Choose and record a geometry convention before comparing sites. Hazard footprint, reference/event period and exposure criterion must be explicit. A mapped overlap is not a claim of damage, people protected, continuity of service or NbS protection benefit.

Missing inventory or hazard coverage remains unknown. Operating status remains unknown unless supported by dated source evidence. No high/medium/low infrastructure thresholds or default weights are introduced here. Roads remain active; power lines and buildings remain in scope where suitable inventories are available. The next inventory inspection can address power lines while pilot context and Brayden's hazard selection remain pending.

## Status

Technical acquisition/schema checks progressed for health facilities and the OSM school/health fallback. MENFP school data remain a source lead with an identified download route. National completeness, latest authoritative editions, facility identity/duplicates, actual pilot context and hazard alignment remain open. This is inspection research; no accepted BIND row, formal source registration, facility exposure result or runtime release is claimed.

## Preserved source inspection

Source metadata/pages, original PAHO/WHO ZIP, both OSM POI layers, inspection scripts and geometry checks are stored in the existing team-library mirror at `0_Methodology_&_Frameworks/priority_classification/facility_bindings_2026_11_26/reviewed_sources.zip`. Archive SHA-256: `95da36a51cd95bb594cc278198d36b9104307ae06110b9c5aa0d8d8bd50ec864`. Original PAHO/WHO ZIP SHA-256: `69b1f85eb659b8ee1f143d78eba4101b2ef1c2b9ce0fae430b19133c5bfd6805`. Individual member hashes are in the archived manifest; all archive members were read back and verified. Remote SharePoint/team access was not checked. No spreadsheet was acquired or formally ingested.
