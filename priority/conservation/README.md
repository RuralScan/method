# Conservation importance: Key Biodiversity Area overlay

26 November 2026. Pete approved adding Key Biodiversity Areas (KBAs) as a separate conservation-importance overlay and suggested an ordinal proximity display: within = 3, very close = 2, close = 1, not close = 0. The overlay is approved in scope; numerical distance thresholds have not been selected. This supplements the nine visual-method problems without changing the biodiversity-loss classification or adding a default MCDA weight. [Infrastructure exposure](../infrastructure/README.md) remains active.

## Meaning and display

[IUCN defines KBAs](https://iucn.org/resources/conservation-tool/key-biodiversity-areas) as sites contributing significantly to the global persistence of biodiversity. They identify recognised importance, whereas the Biodiversity Intactness Index describes modelled ecological condition/depletion. Intact habitat can have high conservation importance. Protected-area designation is another distinct attribute; KBA membership alone is not a legal exclusion or proof of a permitted intervention.

Use the display name **Conservation importance — proximity to a mapped KBA**. Retain actual overlap and distance with the ordinal code. The codes express proximity, not measured biodiversity value, ecological connectivity, intervention benefit or likelihood of causing harm.

| Code | Display | Spatial rule |
|---|---|---|
| 3 | Within KBA | Location lies within a mapped KBA polygon, including its boundary |
| 2 | Very close | Outside a KBA; shortest distance to its polygon boundary is >0 and <= the near-distance setting |
| 1 | Close | Distance is > the near-distance setting and <= the outer-distance setting |
| 0 | Beyond selected distance | Distance is > the outer-distance setting, with valid source/search coverage |
| Missing | Not assessed | Source unavailable, coverage/search extent insufficient, or geometry invalid |

Require `0 < near_distance_m < outer_distance_m`, recorded with the context, rationale and source release. Neither setting has a silent numerical default. This captures Pete's proposed structure without inventing universal conservation thresholds. IBAT's [Proximity service](https://www.ibat-alliance.org/services), “Reports / PROXIMITY”, similarly allows user-specified buffers; this supports proximity screening, not any particular cutoffs or the 3/2/1/0 scores. The ordinal codes are a project decision convention and are not inserted into the priority evaluator's 0/0.33/0.66/1 classes.

Code 0 means beyond the selected buffer of mapped KBAs, **not no conservation importance**. Areas outside recognised KBAs can still matter nationally, locally or for connectivity; incomplete identification remains a limitation even where the database download itself is complete. Straight-line proximity does not establish ecological connection. Watershed pathways and species-specific connectivity require separate analysis.

## Spatial handling and useful outputs

- Compute polygon overlap and shortest metric/geodesic distance; never use distance to a KBA centroid. Include KBA sites beyond the project boundary, at least through the outer-distance setting, before classifying. If using only that buffered extract, distances beyond the search limit are censored, not exact global nearest-site distances.
- Preserve vector geometry for area intersections and calculate physical area appropriately. Report opportunity-space hectares and percentage within KBAs; optionally report area in each disjoint proximity class and the assessed/missing denominator. Do not classify an entire opportunity polygon as “within” because one corner overlaps.
- Dissolve overlapping KBA footprints for total area so overlap is not double-counted; retain individual source IDs for traceability. Pixel displays must state their spatial resolution and boundary assignment convention.
- Keep raw overlap/distance, KBA source ID(s), release date, acquisition/hash, classification settings and coverage caveats. Do not infer a site-level conservation score from pixel proximity.

## Dataset binding and access

Preferred source: the **World Database of Key Biodiversity Areas**, managed by BirdLife International for the KBA Partnership. [Official GIS request page](https://www.keybiodiversityareas.org/en/request-gis-data) routes non-commercial requests through its form and commercial access through IBAT. It states a normal 5–10 working-day processing period. [IBAT](https://www.ibat-alliance.org/services), “Access global spatial data”, offers GIS downloads and API access. A third-party public mirror is not a verified substitute for the authoritative edition and use conditions.

The [current KBA terms](https://www.keybiodiversityareas.org/en/terms-service), version 3.0 (July 2026), distinguish access/use from redistribution, including restrictions on geospatial outputs. Check the route and permission covering this funded project's team use and intended demonstrator outputs; do not assume that a nonprofit affiliation alone settles permitted use. No KBA request, paid subscription or new terms submission was made in this step.

Binding status: **source route identified; authorised polygon package, release/schema/geometry inspection and deployment permissions pending**. No new accepted BIND row, source evidence registration, distance calibration or runtime release is claimed. Once obtained, inspect actual polygon geometry, stable site IDs, status/coverage metadata and release date before naming fields in a binding. Never turn failed access into a zero-overlap result.

Reviewed provider pages and technical follow-up are preserved with the [roads binding inspection](../infrastructure/2026-11-26-roads-binding.md). Next binding work proceeds with roads while KBA access and distance settings remain explicit.
