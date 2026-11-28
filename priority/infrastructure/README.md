# Infrastructure exposure: retained Bank scoping request

25 November 2026. Active optional work alongside the nine core problems, not discarded with supplementary classifications. Pete reiterated the Bank requirement while limiting the problem menu to nine.

The project feedback log records the World Bank team and Pete's 9 November request to explore infrastructure exposure and optional prioritisation. Pete's later instruction that day restricts desk scoping to mapped exposure; potential protection benefits pass to feasibility. The current visual method implements this separation in [Stage 03, section 3.5](https://ciat.github.io/nbs_ruralscan/redesign/03-opportunity.html) and optional prioritisation in [Stage 05](https://ciat.github.io/nbs_ruralscan/redesign/05-hotspots.html). Its Haiti figures are illustrative, not data-backed results.

## National data should replace global fallbacks where suitable

26 November 2026, Pete: acquire and include national infrastructure datasets for country applications, including the Haiti examples. Seek the responsible ministries, utilities and national mapping agency at the start of an assessment. Use suitable national or local inventories to replace global versions through country/area-specific bindings; prefer spatial services where available. Global sources provide a provisional fallback, not an assumed complete national inventory.

Before replacement, check the actual observation date, geographic and asset-type coverage, coordinates/geometry, identifiers and duplicates, operating-status fields and permitted use. A government source may be old, partial or non-spatial; its institutional origin alone does not establish fitness. Replace only the geography/types it supports, retain provenance and fallback flags elsewhere, and reconcile overlaps instead of concatenating inventories. Record who holds any missing authoritative data and what must be acquired.

For every result, distinguish inventory coverage from hazard coverage. Report assessed and unassessed assets; absence from a map means not mapped, not absent on the ground. Power-line kilometres do not measure network capacity or reliability; building footprints do not establish occupancy, critical function or service capacity. The [Haiti national-source search and power/building checks](2026-11-26-haiti-national-infrastructure.md) records sources actually acquired, usable scope and remaining acquisition gaps.

## Minimum useful output where coverage permits

- Overlay mapped roads, schools and health facilities with available hazard footprints within the declared screening area.
- Report exposed and assessed road kilometres or facility counts, plus missing hazard coverage. Exposed assets are a subset of assessed assets; missing inventory is not zero assets.
- Keep asset identity, source date, hazard definition and inventory completeness visible. Overlap indicates exposure, not damage, service disruption, avoided loss or protection by a particular NbS.
- Offer an optional prioritisation input only after comparable coverage and its denominator are established. Retain the unweighted result alongside any weighted result. No weight or severity cutoff is set here.

Start with roads as the existing worked example; include schools and health facilities where suitable inventories exist. The visual method names Geofabrik/OpenStreetMap roads and country inventories (Haiti MSPP health facilities and CNIGS schools in its example). These are leads, not verified global coverage or adopted bindings. Pilot-country data determine what is possible.

The Phase 3, 4 & 5 methodology deliverable also identifies roads, power lines and buildings as critical-infrastructure interests, starting with flood exposure. Retain power lines and buildings as additional inventory candidates where coverage permits; the examples above are not an exhaustive asset list. Locator: team project `4_Outputs_&_Reporting/4_Reporting/4. Phase 3,4 & 5 reporting/NbS_RuralScan_Methodology_Deliverable_Phase 3,4 & 5.docx`, paragraph on assessing protection of critical infrastructure; original-byte SHA-256 `8db2a7ab536325ddce111dbd1f4b0e9782de9334e1f0a96475632528e8b7045b`. The later exposure-only instruction still governs the output.

The [flood-depth proposal](../research/2026-11-25-flood-hazard-classes.md) identifies a physical river-hazard candidate for this overlay. Its return period and coverage must be declared; river-flood maps cannot stand in for coastal or surface-water flooding. Brayden has been asked to confirm the hazard variables before a default is adopted.

The mock-up lists river flood, landslide and wildfire overlays. Check each source's actual meaning before use: susceptibility, current alerts, historical burn footprints and event hazard maps are not interchangeable. This optional overlay does not expand the nine-problem classification list. Keep it distinct from risk to the NbS investment itself.

Current status: provisional Haiti inventory sources selected on 26 November 2026 in the table below; no exposure computed or operational weighting adopted. Source selection does not establish runtime readiness. Source: retired producer `docs/redesign/FEEDBACK_LOG.md`, entries dated 2026-11-09, and current published Stages 03/05.

26 November follow-up: [roads binding inspection](2026-11-26-roads-binding.md) checks a real provider extract and records the remaining inventory/geometry and hazard choices. Schools, health facilities, power lines and buildings remain in scope where coverage permits. The parallel [KBA overlay](../conservation/README.md) does not replace this work.

[Health-facility and school follow-up](2026-11-26-facility-bindings.md): PAHO/WHO health Shapefile and OSM point/polygon fallback acquired and inspected; MENFP national school catalogue route identified. Source dates, operating-status gaps and inventory completeness remain explicit. Power-line and building candidates are now inspected in the [Haiti national-source follow-up](2026-11-26-haiti-national-infrastructure.md).


## Approved Haiti fallbacks and remaining national gaps

26 November 2026, Pete approved capturing the national-data gaps and using the best available fallbacks for now. The following are the selected provisional sources among those inspected. Use them for preparing the Haiti examples; retain the national acquisition needs alongside them. This is a source-selection decision, not a completed spatial analysis or an accepted executable BIND release.

| Asset | Selected provisional source | National data still needed / treatment of acquired sources | Required qualification |
|---|---|---|---|
| Roads | OpenStreetMap via the inspected Geofabrik Haiti-and-Dominican-Republic extract | CNIGS/MTPTC current network and codebook; retain acquired CNIGS 2019 network for comparison and replacement where coverage and currency are established | Clip to Haiti/AOI; retain road classes and snapshot date. OSM update date is not a survey date. Do not assume complete rural coverage or add both networks together |
| Schools | OpenStreetMap school points and polygons from the inspected Geofabrik extract | MENFP/CNIGS georeferenced master list with stable IDs; acquired MENFP list supports name/admin reconciliation, not facility locations; project point layers remain partial with unresolved reuse terms | Clip to Haiti/AOI, reconcile point/polygon duplicates, preserve unnamed schools and unknown operating status. Never manufacture locations from commune centroids |
| Health facilities | OpenStreetMap hospital/clinic/doctors points and polygons from the inspected Geofabrik extract | MSPP/SISNU dated, georeferenced master export with facility type and status; acquired PAHO/WHO file retained for reconciliation, with its coordinate/identity gaps | Clip to Haiti/AOI; retain facility types, deduplicate overlapping representations, qualify mapped coverage and unknown status/capacity |
| Power lines | Inspected Haiti OpenStreetMap power=line/minor_line/cable query | EDH/relevant network operators' transmission/distribution GIS, voltage, status, coverage and sharing conditions | Retain query and OSM snapshot; clip geometry to AOI. The 310 returned ways are mapping segments, not circuits; missing voltage/operator and unmapped networks remain unknown |
| Buildings | Google Open Buildings v3 polygons, Earth Engine asset GOOGLE/Research/open-buildings/v3/polygons | Current CNIGS/MTPTC/local-authority footprints for the target area; acquired Jérémie 2014–2017 inventory remains historical and local | Retain inference/version metadata and confidence field. Set and disclose the confidence-selection policy before footprint counts; no cutoff is approved here. Footprints do not identify use, occupants or service capacity |

Exact source routes, inspected bytes, dates and hashes are in the [national-source audit](2026-11-26-haiti-national-infrastructure.md), [roads inspection](2026-11-26-roads-binding.md) and [facility inspection](2026-11-26-facility-bindings.md). The five-building diagnostic verifies access only; it is not a Haiti completeness assessment. None of these source choices asserts complete national inventories. The nine core variables and optional infrastructure role are unchanged.

## How existing tables represent global and national data

No extra global/national column is needed. The [T1 and BIND specification](../../data-model/spec.md) already separates dataset coverage from its selection context:

| Question | Existing field / table | Haiti application |
|---|---|---|
| Where does the source cover? | T1.geographic_coverage | global for a global product; HTI for Haiti coverage. A country code alone does not promise complete coverage |
| What is its geographic support? | T1.grain_type, spatial_resolution_m or admin_level | Keep vectors, rasters and administrative summaries distinct; a national average is not a local map |
| Where should this variable use this source? | BIND.scope_type + scope_id, linked to T7.context_id | Global default, admin_country override for HTI, or a defined admin_region where a source is local |
| Which matching source wins? | BIND.preference_rank within scope precedence | More-specific scope first, then lower rank. Do not choose an older national source solely because its scope is more specific |
| Better national source not yet acquired? | BIND.status=requires_upload, blank dataset_id, fitness_note | Record the acquisition need; the specified resolution contract uses the global default with a visible substitution flag |
| What limits its use? | T1.time_period, version, license, limitations, preprocessing_notes; BIND.fitness_note | Record partial departments, missing coordinates, observation dates, use conditions and planned replacement |

BIND's specified precedence is admin_region > admin_country > hydrobasin > farming_system > aez > global. HTI is an example of the country context to register, not a claim that a Haiti row has already been created. The current runtime variable loader is not a verified consumer of these new infrastructure selections: automatic switching, coverage-mask mosaics and per-feature provenance still require explicit runtime implementation and validation. Existing columns can describe the choices; they do not automatically repair missing geometry or combine overlapping inventories. Preserve exact assessed footprints and source transitions in the run output. This decision does not silently alter the historical T1/BIND configuration tables.


26 November erosion follow-up: the [dataset comparison](../research/2026-11-26-erosion-dataset-alternatives.md#haiti-follow-up-actually-checked) identifies an acquired HaitiData local gully/bank-erosion line layer. Its partial geography, missing geometry and unspecified reuse terms are recorded. It is a possible local-context input for later assessment, not an approved replacement for the selected infrastructure hazard footprints or evidence of avoided damage. Existing roads, power, buildings, school and health-facility fallbacks remain in scope.

## Full Haiti road geometry follow-up — 27 November 2026

[Complete road inspection and national comparison](2026-11-27-haiti-road-geometry.md) now checks the dated OSM road layer, clips actual linework to Haiti, retains native-class lengths and inspects exact duplicates/IDs. CNIGS is processed separately. No hazard exposure, inventory completeness or automatic national replacement is claimed. Schools, health facilities, power lines and buildings remain active.

## School and health-facility coverage — 27 November 2026

[Haiti coverage and duplicate review](2026-11-27-haiti-facility-coverage.md) records OSM school/health features across all ten departments, boundary sensitivity and point/polygon identity candidates. PAHO missing locations and department disagreements prevent wholesale national replacement. No records merged or exposure computed; power lines/buildings and national master-list needs remain active.
