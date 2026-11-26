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

Current status: requirement and output specification retained; no pilot asset inventory selected, no new exposure computed, no operational weighting adopted. Source: retired producer `docs/redesign/FEEDBACK_LOG.md`, entries dated 2026-11-09, and current published Stages 03/05.

26 November follow-up: [roads binding inspection](2026-11-26-roads-binding.md) checks a real provider extract and records the remaining inventory/geometry and hazard choices. Schools, health facilities, power lines and buildings remain in scope where coverage permits. The parallel [KBA overlay](../conservation/README.md) does not replace this work.

[Health-facility and school follow-up](2026-11-26-facility-bindings.md): PAHO/WHO health Shapefile and OSM point/polygon fallback acquired and inspected; MENFP national school catalogue route identified. Source dates, operating-status gaps and inventory completeness remain explicit. Power-line and building candidates are now inspected in the [Haiti national-source follow-up](2026-11-26-haiti-national-infrastructure.md).
