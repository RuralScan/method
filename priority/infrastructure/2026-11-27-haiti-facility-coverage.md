# Haiti schools and health facilities: coverage and duplicate checks

27 November 2026. Full country and identity diagnostics now extend the [earlier source inspection](2026-11-26-facility-bindings.md). **Counts below are mapped features, not deduplicated institutions or proof of national completeness.** Existing OSM fallbacks remain provisional; current MENFP/MSPP master lists are still needed.

## Haiti coverage

| OSM class | Points in pinned Haiti boundary | Polygons intersecting boundary | Combined features | Features using CNIGS departmental union instead |
|---|---:|---:|---:|---:|
| School | 4,567 | 572 | 5,139 | 5,213 |
| Hospital | 1,145 | 134 | 1,279 | 1,301 |
| Clinic | 154 | 12 | 166 | 173 |
| Doctors | 65 | 2 | 67 | 68 |
| All selected health classes | 1,364 | 148 | 1,512 | 1,542 |

Schools and health features occur in **all 10 departments**. This establishes spatial presence, not the proportion of real facilities mapped, service accessibility or operating status. Hospital/clinic/doctors labels are native OSM tags, not an externally verified clinical classification. Retain types separately.

Boundary sensitivity is material: the CNIGS union includes 88 OSM points and 19 polygons excluded by the simplified LSIB country boundary; three OSM points pass LSIB but fall outside the CNIGS union. These are boundary disagreements, not automatically erroneous facilities. Both counts are saved. Country selection remains the previously pinned LSIB baseline for reproducibility, with CNIGS as an explicit comparison.

### Departmental distribution under the pinned boundary

Polygon counts use an interior point of the clipped footprint for single-department tabulation; points retain their locations. Counts remain unreconciled features.

| Department | School features | Health features |
|---|---:|---:|
| Artibonite | 634 | 233 |
| Centre | 263 | 73 |
| Grande-Anse | 196 | 64 |
| Nippes | 48 | 36 |
| Nord | 421 | 152 |
| Nord-Est | 183 | 82 |
| Nord-Ouest | 107 | 95 |
| Ouest | 2,588 | 552 |
| Sud | 452 | 142 |
| Sud-Est | 246 | 81 |
| UNMATCHED | 1 | 2 |

## Duplicate and co-location findings

| Check | Finding | Treatment |
|---|---|---|
| Repeated OSM IDs within each selected layer | None | Keep source/layer-qualified identities; cross-layer numeric IDs are not a shared namespace |
| Exactly coincident OSM points | 25 groups, 41 records beyond one per location | Four groups share a nonblank normalized name and native class; strongest duplicate candidates. Other groups have different/missing names or types |
| OSM points covered by same-theme polygons | 136 pairs: 103 school, 33 health | 12 pairs share normalized nonblank names (10 school, 2 health); 97 involve missing names; 27 have different names |
| Positive-area same-theme polygon overlaps | 19 pairs | Three same-name school pairs; other overlaps need campus/building identity review |
| Repeated nonblank OSM names | 272 groups | Review aid only; common names can recur at different institutions |
| PAHO-to-OSM equal normalized health names | 67 pairs | Distances range from zero to 260.6 km; name equality alone cannot reconcile inventories |
| CNIGS-school-to-OSM equal normalized names | Three pairs | Distances approximately 7 m, 31 m and 1.2 km; candidates, not accepted matches |

No automatic merge, deletion or corrected unique-facility total is produced. Even same-name/coincident records can represent distinct services or institutions. Counts of pairs/groups above overlap and must not be added as a number of duplicate institutions. The [audit package](facilities-haiti-audit-20261127/README.md) provides a compact review summary and the archived full record/pair queue for resolution against authoritative identifiers.

## National and agency-source limitations

**PAHO/WHO:** 730 records; 250 lack geometry. Of 480 located records, 469 fall inside LSIB and 479 inside the CNIGS departmental union. Within LSIB, 36 coincident-coordinate groups contain 108 excess records relative to one record per coordinate; all groups contain different names, so collapsing them would conflate distinct reported institutions. Across the full source, 29 institution-code candidates are missing and three repeated-code groups contain five excess records. No current operational-status field is established.

**443 of 469 LSIB-located PAHO records have native department labels inconsistent with spatial assignment.** The source labels name only four departments, while coordinates occur across all ten. This may reflect erroneous labels, coordinates or earlier joins; it is not permission to overwrite labels using the geometry. Keep PAHO as a reconciliation source pending MSPP validation, rather than replacing OSM with it wholesale.

**CNIGS school project 29 (Sud):** 99 records, 11 missing geometries; 85 locations inside LSIB and all 88 located records inside the national departmental union/Sud. One coincident pair has different names and codes: retain both pending review.

**CNIGS school project 83 (Nippes):** five located records; three inside LSIB, all five inside the national union. Spatial assignment places three in Nippes and two in Ouest. Record this inconsistency with the project label; do not assume the five points form a reliable Nippes inventory. Both project layers remain partial and have unspecified reuse terms.

**MENFP:** the already acquired 4,122-row list covers four departments and has no coordinates. It remains useful for name/admin reconciliation; no locations were invented and its records were not added to mapped counts.

## What is ready, and what remains

Coverage diagnostics, source hashes, duplicate candidates and reproducible processing are saved. All selected OSM geometry passed basic validity checks; that does not establish positional or institution accuracy. No institution was silently removed, national inventory was concatenated, or source geometry repaired. The original source snapshot is 26 November, distinct from the newer road extract.

Before releasing deduplicated facility counts, reconcile candidate identities and geometry conventions with the intended inventory and current national master lists. Retain missing/unassessed coverage and source dates. Hazard exposure, capacity, people protected and service continuity have not been computed. No new infrastructure weights or severity bands are defined.

Power lines and buildings remain in scope with their selected provisional sources and national replacement gaps. KBA access awaits provider review; climate-hazard selection awaits Brayden. This audit does not activate T1/BIND records or expand the nine core variables.
