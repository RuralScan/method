# Haiti roads: full geometry and national-source comparison

27 November 2026. The selected provisional OSM road layer now has a complete geometry inspection, Haiti clipping, native-class length summaries and exact-duplicate/identity checks. The older CNIGS national-source network was processed separately. These close the bounded geometry/length checks from the [first roads inspection](2026-11-26-roads-binding.md), not national completeness, source replacement or runtime adoption.

## Findings

| Check | OSM / Geofabrik dated `261126` extract | CNIGS 2013–2019 main network |
|---|---:|---:|
| Source records | 332,117, Haiti and Dominican Republic | 47,317 |
| Records with positive line length inside pinned Haiti boundary | 130,800 | 46,853 |
| Native classes present inside Haiti | 23 `fclass` values | 6 `type_tronc` codes |
| All-class mapped line length inside boundary | 44,739.815 km | 17,002.750 km |
| Missing selected identifiers inside Haiti | 0 (`osm_id`) | 0 (`OBJECTID`, snapshot-local) |
| Repeated selected identifiers inside Haiti | 0 | 0 |
| Exact duplicate clipped geometries | 0 | 0 |
| Empty or invalid source geometries | 0 | 0 |

The OSM all-class length **includes paths, footways, steps and tracks**. It is not a motor-road total, unique-route length or assessed/exposed denominator. CNIGS uses different classes, dates and mapping conventions; its shorter total does not measure missing roads or establish OSM accuracy. Neither inventory is validated as complete. Parallel carriageways, partial overlaps and near duplicates remain outside the exact-duplicate check.

Among Haiti-intersecting records, 239 OSM and one CNIGS record have non-simple source line geometry (self-intersections). They remain valid lines and are retained with this flag; no automatic repair was applied. Across the entire combined-country OSM extract, 770 source records are non-simple. These counts are not a network-connectivity assessment.

The dated OSM object was modified 27 November 2026 at 07:23:42 UTC. The acquisition read 53,246,041 bytes from a 200,071,976-byte multi-layer ZIP, retaining complete road SHP/SHX/DBF/PRJ/CPG members. These are a newer snapshot than the earlier DBF/header inspection; source counts need not match. ETag guards keep range reads consistent; member SHA-256 hashes, not ETag alone, pin the replay inputs.

## What the binding can now describe

OSM geometry is WGS84 linework. Preserve `osm_id` as text, `fclass`, name/ref and bridge/tunnel fields. Report mapped lengths by class before selecting a road-only subset; retain tracks and pedestrian features visibly. `unclassified` and `unknown` are different native categories and must not be merged by their names. Unknown condition, access, passability or survey age cannot be inferred from geometry or a recent extract timestamp.

CNIGS `OBJECTID` is unique in this inspected snapshot, not a demonstrated persistent network ID. The intended `cod_tronc` field is blank for all inspected Haiti records. `cls_admin`, `source`, `etat_util`, `type_rev` and node identifiers are also blank throughout those records. Use populated `type_tronc` codes without expanding their abbreviations until a codebook is obtained. Keep condition/surface ancillary layers separate. The catalogue is archived and the recorded observation period ends in 2019; current CNIGS/MTPTC data remain an acquisition need.

No concatenation, automated national override or topology repair was performed. Same-boundary clipping makes the descriptive summaries reproducible, not directly equivalent. The pinned LSIB simplified boundary is an international fallback and can omit mapped coastal segments; seek country-endorsed boundaries when appropriate.

## Native OSM class inventory

| Native class | Haiti-intersecting records | Clipped mapped line km |
|---|---:|---:|
| `bridleway` | 3 | 0.564 |
| `cycleway` | 8 | 0.761 |
| `footway` | 5,515 | 847.367 |
| `living_street` | 469 | 105.390 |
| `path` | 27,825 | 7,463.727 |
| `pedestrian` | 91 | 10.170 |
| `primary` | 1,147 | 1,037.919 |
| `primary_link` | 18 | 2.175 |
| `residential` | 39,483 | 8,714.976 |
| `secondary` | 1,312 | 1,616.243 |
| `secondary_link` | 29 | 1.199 |
| `service` | 11,125 | 1,094.054 |
| `steps` | 123 | 4.834 |
| `tertiary` | 1,668 | 1,991.230 |
| `tertiary_link` | 15 | 0.495 |
| `track` | 25,686 | 9,949.794 |
| `track_grade1` | 52 | 16.221 |
| `track_grade2` | 101 | 39.259 |
| `track_grade3` | 108 | 45.886 |
| `track_grade4` | 125 | 42.947 |
| `track_grade5` | 56 | 23.755 |
| `unclassified` | 15,840 | 11,730.483 |
| `unknown` | 1 | 0.366 |

## Native CNIGS class inventory

Codes below remain uninterpreted pending the provider codebook.

| `type_tronc` | Haiti-intersecting records | Clipped mapped line km |
|---|---:|---:|
| `RA` | 12,988 | 9,714.465 |
| `RC` | 813 | 861.564 |
| `RD` | 1,883 | 1,577.558 |
| `RI` | 3 | 18.163 |
| `RN` | 1,831 | 886.292 |
| `RU` | 29,335 | 3,944.708 |

## Remaining work and reproducibility

The [audit package](roads-haiti-audit-20261127/README.md) gives exact source hashes, archived inputs, length/duplicate methods and replay commands. Offline validation checks source pins, native-class/identity totals and the absence of an exposure or runtime claim. Original geometries remain outside Git with their source conditions.

Before operational use, declare the road classes included, review any network/topology concerns, and establish fit against current national data. Hazard coverage, event/return period and exposure definition await Brayden; therefore no flood intersection, exposure percentage or avoided-damage result is reported. No four-class infrastructure severity scheme is introduced.

[Schools, health facilities, power lines and buildings](README.md) remain in scope with their selected provisional fallbacks and national replacement needs. KBA request remains under provider review. This audit does not add a tenth core variable or activate T1/BIND records.
