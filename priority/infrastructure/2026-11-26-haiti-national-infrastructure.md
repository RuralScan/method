# Haiti national infrastructure sources, power lines and buildings

26 November 2026. Pete requested national datasets for the Haiti examples and explicit methods guidance to acquire national inventories to replace global versions. The [infrastructure method](README.md#national-data-should-replace-global-fallbacks-where-suitable) and M3 reference now capture that requirement. This is a source acquisition and binding inspection, not an exposure result or a claim that the demonstrator is connected to these data.

## National and Haiti-specific sources found

| Asset | Source and acquisition | What it can replace or support | Limits before use |
|---|---|---|---|
| Roads | **CNIGS 2019 road package**, acquired from [HDX](https://data.humdata.org/dataset/haiti-roads) | Candidate national geometry replacement for OSM roads; 47,317 main-network records, all passing basic geometry checks | Older inventory; completeness/current routes and code definitions still need assessment. The two ancillary condition/surface layers are partial |
| Schools | **MENFP school list**, acquired from [HDX](https://data.humdata.org/dataset/haiti-education-facilities) | National-ministry source for names, type and administrative reconciliation | 4,122 records in four departments, **no coordinates**. Cannot replace point/polygon locations without a validated match or georeferenced source |
| School locations | **CNIGS HaitiData: Sud PEQH and Nippes PRGRD** layers, acquired from [dataset 29](https://opendata.haitidata.org/catalogue/#/dataset/29) and [dataset 83](https://opendata.haitidata.org/catalogue/#/dataset/83) | Government-hosted project locations that can refine those project subsets | Sud: 99 records, 11 null geometries; Nippes: 5 points. Neither is a national census. Observation date and reuse terms need confirmation |
| Health facilities | **MSPP/SISNU Carte Sanitaire**, identified through [MSPP's official tools page](https://mspp.gouv.ht/services-et-outils) | Preferred current national master-list acquisition route | Direct map retrieval timed out in both local and web checks. Current master export remains unacquired. The older PAHO/WHO file has the [previously recorded coordinate/identity gaps](2026-11-26-facility-bindings.md) |
| Power lines | Seek **EDH and relevant network operators' GIS inventories** | National/operator transmission and distribution geometry, voltage, status and update dates | No downloadable national/operator network verified in this bounded search. Public OSM fallback checked below; it must not be relabelled a national utility inventory |
| Buildings | **Recovery Observatory/CNES-SERTIT Jérémie inventory**, acquired from its [project page](https://www.recovery-observatory.org/drupal/en/groups/mapping-buildings/inventory-city-j%C3%A9r%C3%A9mie), within the CNIGS/CIAT-coordinated [building-mapping work](https://www.recovery-observatory.org/drupal/en/node/847) | Historical, geographically bounded building evidence and a route to national/project custodians | 2014/2016/2017 urban observations, not a current nationwide footprint layer. Seek current CNIGS/MTPTC/local-authority data for the target area; Google remains a provisional fallback |

A dataset held by a national institution can still be local, old or non-spatial. Do not automatically override a global layer across all Haiti because one national-source file was acquired. Replace only the verified geography, period and asset types, and record source transitions in the output. Institutional source preference does not waive access/use conditions or coverage checks.

## Search and acquisition trail

The [CNIGS page](https://cnigs.ht/haitidata/) identifies HaitiData as its geospatial platform. The public landing-page configuration resolves the current [Open Data catalogue](https://opendata.haitidata.org/) and `api/v2/resources/`. The complete response contained **129 resources**, with no next page; titles, descriptions and available links were inspected. No current nationwide power-line or building-footprint dataset was found in that catalogue. Its electricity-related household-area indicators are not line networks, and housing characteristics are not individual building footprints; they were not substituted.

HDX API searches covered `Haiti roads`, `Haiti electricity`, `Haiti buildings`, `CNIGS`, and `Haiti health facilities` (up to 40 returned records per query). Search responses are retained; the broad health query was not exhaustive. Further web searches covered EDH power-network GIS, national building data and Recovery Observatory products. An old global transmission product derived from 2016 OSM and electrification-model outputs do not establish a current utility inventory. Failed site access and unsuccessful searches do not prove that national data do not exist.

Acquisition needs are concrete: CNIGS/MTPTC should supply the latest applicable roads/building geometries and codebooks; MENFP/CNIGS the georeferenced school master list with stable school IDs; MSPP/SISNU the dated health-facility master export with coordinates and operational status; EDH/network operators the dated line/cable and substation inventory, voltage and status fields, coverage and permitted sharing. No messages or access requests were sent in this step.

## Inspected national road and school files

The original CNIGS road ZIP contains three Shapefiles in **WGS 84 / UTM zone 18N (EPSG:32618)**. The main `Réseau_Routier` layer has 47,317 line records, no empty geometries and no basic validity failures. Actual attributes include `cod_tronc`, `code_route`, `type_tronc`, `cls_admin`, `etat_util`, `source` and `Longueur`; preserve provider code values pending the codebook. Main-layer `type_rev` is blank throughout, so road-surface completeness must not be inferred from the column's presence.

The ancillary `Praticabilité` layer has 595 records, including 31 empty geometries; `Revetement` has 839 records, including 51 empty geometries. These are measured-line layers (PolylineM). Keep their scope and native encoding separate; do not append their geometries to the main network or count overlapping segments twice. Geometry validity is not network-topology or completeness validation. HDX identifies a 2013–2019 dataset period; a recent catalogue publication does not make the surveyed network current.

MENFP's XLS has one sheet, `Ecole`, with its header on Excel row 3: `Departement`, `Adm1_Pcode`, `Commune`, `Adm2_Pcode`, `Nom`, `Type`. It contains 759 records for Grande'Anse, 769 for Nippes, 976 for Ouest and 1,618 for Sud. Administrative codes locate administrative areas, not individual schools; do not assign every school to a commune centroid. HDX's observation date is September 2021 while the filename/resource date refers to 2022. Preserve that distinction. No general workbook edits or formal evidence-register intake were performed.

The two government-hosted project school layers were acquired through WFS in explicit EPSG:4326. Sud contains `CODE_ECOLE` and school/type/location attributes; Nippes supplies `Name` and `fid`. The returned feature totals matched the downloaded record counts, but this establishes download completeness only. Their November 2026 publication dates do not establish field-observation dates. Catalogue licences are `not_specified`; public access alone does not settle redistribution.

## Historical building inventory acquired

The original Jérémie ZIP contains a study-area polygon and the building layer for 2014/2016/2017. The building layer has **12,857 polygon records: 12,856 valid nonempty geometries and one empty geometry**, in EPSG:32618. Attributes include source dates, `Fonction`, `Type_toitu` and `Etat_date1/2/3`; interpretation of coded function/condition values requires the source nomenclature. Keep the original ZIP member names and UTF-8 attribute encoding; the ZIP filename encoding is imperfect. This is a partner-produced city inventory associated with national/project actors, not a Haitian national census. It can support a historical Jérémie example, but cannot silently replace current rural building data.

## Power-line fallback: actual Haiti query

A read-only Overpass query selected OSM ways tagged `power=line`, `minor_line` or `cable` within the Haiti administrative-area selector. POST returned 502; the GET route succeeded without an error remark. Source timestamp: **2026-11-26 21:52:35 UTC**. The response contains **310 mapped ways: 259 line and 51 minor_line**; no cable ways were returned. All have at least two coordinates and pass basic line-geometry checks.

**272 ways lack voltage; 277 lack operator.** One also has highway tags and needs review. Retain these as raw OSM observations, not automatically accepted utility records. The returned `line` label does not independently verify a voltage or engineering network class. Zero returned cables does not establish absence of underground infrastructure. Ways are segmented mapping objects, not counts of distinct circuits.

The query selects intersecting ways; an eventual run must clip geometry to its actual analysis boundary. Use mapped line-kilometres with assessed/unassessed coverage. Retain overhead/underground and voltage distinctions where actually known. Hazard intersection cannot establish outage, failure, downstream customers affected or protection by an NbS. Incomplete volunteered mapping prevents a national network-length or reliability claim. Preserve ODbL attribution and the raw query/version.

## Building fallback: verified Earth Engine route

[Google Open Buildings v3](https://developers.google.com/earth-engine/datasets/catalog/GOOGLE_Research_open-buildings_v3_polygons) is available as `GOOGLE/Research/open-buildings/v3/polygons`. A server-side spatial query returned five actual polygons within a small Port-au-Prince diagnostic rectangle; all five passed basic nonempty/validity checks. This confirms access and field semantics only, not representative accuracy, coverage or a pilot sample. The large global collection was not downloaded.

Actual fields are `area_in_meters` (square metres), `confidence`, `full_plus_code` and `longitude_latitude`; geometries are polygons. The provider dates inference to May 2023; the asset metadata update is June 2023. Neither supplies a current observation date for every footprint. Keep confidence visible and select a documented, context-appropriate inclusion policy before counting. The five sampled confidence values do not calibrate that policy.

Google footprints supply no building function, occupancy or operating status. They cannot identify schools, health facilities or critical infrastructure without a verified inventory linkage. Use footprint area/counts after duplicate/coverage checks, not an inferred number of households, residents, assets protected or buildings currently standing. Prefer this verified server-hosted route to a global flat-file download while seeking suitable national replacements. Vector acquisition through the Earth Engine API does not change the raster xee computation pathway.

## Readiness

National-source files and scoped project data are preserved for review. Power/building fallback access is verified. Replacement is not yet activated: codes, date/coverage fit, facility identity, current national power/building exports and use conditions remain unresolved where noted. No accepted BIND migration, infrastructure weighting, exposure computation or runtime release is implied. Climate-hazard selection still awaits Brayden's confirmation.

## Source preservation

Original national road/school files, scoped school GeoJSON, historical Jérémie ZIP, public catalogue responses, power query/response, Earth Engine metadata/sample, source-page snapshots and inspection scripts/results are stored in the team-library mirror: `0_Methodology_&_Frameworks/priority_classification/haiti_national_infrastructure_2026_11_26/reviewed_sources.zip`. SHA-256: `4f2475317c7c8cadafb9e8e5d4b43d5e9cba53441b6ba431aed0786b932d6e30`. All members were read back and hash-verified; remote SharePoint/team access was not checked. The archived manifest provides member hashes. The national-data inspection is separate from formal evidence-register intake; no new dataset-intake adapter or accepted analytical rule was silently created.

## Follow-up decision

Pete approved using provisional fallbacks while the national gaps remain open. The [selected sources and acquisition-gap table](README.md#approved-haiti-fallbacks-and-remaining-national-gaps) now records the choice for each asset type and explains global/country/region handling in existing T1/BIND/T7 fields.
