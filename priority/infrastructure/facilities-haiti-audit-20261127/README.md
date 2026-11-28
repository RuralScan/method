# Haiti school and health-facility audit — 27 November 2026

Checks the already acquired 26 November OSM point/polygon inventory, PAHO/WHO health file and two CNIGS school-project layers. This is a coverage and duplicate-candidate inspection, not a current national census, deduplicated institution list or hazard-exposure calculation. `config.json` fixes the inspected classes and matching conventions; no analytical thresholds or runtime binding are introduced.

## Replay inputs

`inputs.json` gives the earlier facility and national-source archive locations and hashes. Extract the two OSM POI layers and PAHO ZIP from the facility archive into one directory, and `school_29.geojson` / `school_83.geojson` from the national archive into another. Use the exact archived OSM snapshot; its historical `latest` URL is mutable and differs from the newer road snapshot.

New departmental input and full record/pair review queue are in the team-library mirror at `0_Methodology_&_Frameworks/priority_classification/facilities_haiti_2026_11_27/reviewed_sources.zip`, SHA-256 `547d6b990a8e15a577d6f68bb9e492fbc1b70f8c1c4c3ee4db15b9adafffa729`. Member read-back hashes verified; remote SharePoint access not checked. Extract `departments.geojson` to a third input directory. `departments-acquisition.json` records the exact public WFS request, explicit EPSG:4326 output, returned count and source description; 10 returned features matched the declared total. The recorded CNIGS/IHSI source describes 2026 units; publication time is not a field-observation date.

From repository root, with Python, pyshp 2.3.1, Shapely 2.1.2 and pyproj 3.7.2:

```sh
uv run --with pyshp==2.3.1 --with shapely==2.1.2 --with pyproj==3.7.2 python priority/infrastructure/facilities-haiti-audit-20261127/analyze.py /path/to/facility-inputs /path/to/national-school-inputs /path/to/department-input priority/research/haiti-diagnostic-inputs-20261126/boundary.json /tmp/facility-replay
cmp priority/infrastructure/facilities-haiti-audit-20261127/inspection.json /tmp/facility-replay/inspection.json
python3 priority/infrastructure/verify_infrastructure.py
```

The script also writes `review_queue.json`; its hash must match `inspection.json`. Queue keys use source plus original one-based record position, and retain original source ID, name and class. They are review locators tied to pinned bytes, not permanent institution identifiers. The compact `review_summary.json` highlights the strongest exact-geometry/name and point-in-polygon/name candidates; the full archived queue provides the records needed to review them. Record names remain in their original encoding; matching keys are separate.

## Coverage and identity conventions

Primary country inclusion uses the same pinned LSIB fallback as the road audit: point covered by boundary, or polygon with positive-area intersection. National departmental-union counts are a **sensitivity comparison**, not a silent change to the country boundary. For department summaries, use source point or an interior representative point of the country-clipped polygon; retain unmatched/ambiguous assignments. An interior point for tabulation is not a substitute for the footprint in an exposure analysis. All 10 departmental geometries passed basic validity checks; this does not validate their positional accuracy or legal status.

Exact geometry groups, repeated source IDs/names, point-in-polygon pairs and positive polygon overlaps are separate flags. School and health themes are kept separate for cross-layer matching; hospital/clinic/doctors remain distinct native classes. Same normalized name, coordinate or footprint does not establish one institution. No records are deleted or merged, and no resulting institution count is asserted. A campus may contain several institutions, departments or buildings.

Cross-source name matches retain all same-theme candidates and distance to actual geometry, calculated in UTM zone 18N. No distance is used as an acceptance cutoff. Generic or repeated names can match distant institutions; name normalization is only a review aid. Broader fuzzy/address/near-coordinate matching was not undertaken, so absence from this queue does not establish uniqueness.

PAHO departmental disagreements compare its native `adm1_fr` against spatial assignment. Either coordinates or labels may be wrong. Do not overwrite them or present the spatial assignment as validated truth. Missing coordinates cannot be assigned to an administrative centroid. MENFP's acquired non-spatial list remains a name/admin reconciliation source, not an additional point inventory.

## Source conditions

- OSM: © [OpenStreetMap contributors](https://www.openstreetmap.org/copyright), ODbL 1.0; distributed by [Geofabrik](https://download.geofabrik.de/central-america/haiti-and-domrep.html). Counts and review summaries are RuralScan derivatives, not endorsed outputs.
- PAHO/WHO: [Haiti health sites](https://data.humdata.org/dataset/location-of-health-facilities-hospital-in-haiti), recorded catalogue period 2019–2023, CC BY label. Retain attribution and original damaged column names/labels. Current operation is unverified.
- CNIGS school layers [29](https://opendata.haitidata.org/catalogue/#/dataset/29), [83](https://opendata.haitidata.org/catalogue/#/dataset/83), and [CNIGS/IHSI departments 35](https://opendata.haitidata.org/catalogue/#/dataset/35): catalogue reuse terms `not_specified`; no blanket external redistribution/deployment permission inferred. Raw geometries remain outside Git.
- LSIB boundary: [shared diagnostic provenance](../../research/haiti-diagnostic-inputs-20261126/README.md), international fallback rather than country-endorsed boundaries.

The repository code licence does not relicense source datasets. Power lines and buildings remain active; KBA/provider permission and Brayden's hazard decisions are separate holds.
