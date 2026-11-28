# Haiti food insecurity: official IPC acquisition, ENSSAN tables and four-class proposal

**Subsequent decision, 27 November 2026:** Pete [approved these four classes and limitations with the Phase 5 flag](2026-11-27-food-insecurity-approved.md). The original proposal/acquisition snapshot below is preserved; runtime and geometry holds remain.

27 November 2026. **The current official IPC spatial export and population workbook are acquired. ENSSAN's published geographic prevalence table is extracted and visually checked.** Access is no longer the main hold for these products; interpretation, geometry and geographic matching remain explicit. Four display classes below are **proposed**, not activated or accepted.

## Acquired products and verified identity

| Product | Acquired content | Time and geographic support |
|---|---|---|
| [Official IPC Haiti analysis](https://www.ipcinfo.org/ipc-country-analysis/details-map/en/c/1165467/?iso3=HTI), released 28 October 2026 | GeoJSON from the public map's **Download GeoJSON** control; 35 features representing 30 unique assessment areas | Current period **1 Sep 2026–28 Feb 2027**. 22 polygon/multipolygon features and 13 point features; eight assessment areas have point-only representation. |
| IPC **Download Excel** workbook | Population Table and Analysis Overview sheets; 30 leaf areas plus departmental/national aggregates | Current period above and **1 Mar–30 Jun 2027 projection**, kept separate. Native analysis ID `87143457`; analysis date 5 Oct 2026. |
| [CNSA ENSSAN 2025](https://www.cnsahaiti.org/Web/Etudes/2025/Rapport%20ENSSAN%202025_vf.pdf), Table 41 | 12 geographic groups × 2022–2025: 46 reported severe-FIES percentages and two explicit missing cells | Printed p.121 / PDF p.122; nine department names, Reste Ouest, Zone métropolitaine and Camps de déplacés. Published aggregate household prevalence, not raw household records. |
| ENSSAN supporting material | Table 39 national comparator and Table 1 sampling-frame extraction; saved page renders | Table 39: printed p.116 / PDF p.117. Table 1: printed p.23 / PDF p.24. These support definition and geography checks. |

Official map route: [Haiti public analysis map](https://map.ipcinfo.org/public/?anl_id=ht-2026-10-05&nofocus=y&period=C&table=true). No API-key application, contact details, email or explicit terms-acceptance form was required. Downloaded originals, hashes, extraction outputs and notices are preserved in the team archive referenced by the [audit](ipc-enssan-audit-20261127/README.md).

## Four proposed classes

Use the **published IPC acute area phase**, not the percentage of households in a phase, as the classification input. This is a RuralScan display crosswalk to fit four requested classes; IPC itself retains five phases.

| RuralScan display | Score | Published IPC acute area phase | Rationale |
|---|---:|---|---|
| Very little | 0 | 1 — Minimal | Lowest published acute severity. Does not mean every household is food secure. |
| Low | 1 | 2 — Stressed | Preserves the next published severity distinction. |
| Medium | 2 | 3 — Crisis | Preserves the crisis threshold. Always show **Crisis** beside the project label; “Medium” does not reduce humanitarian urgency. |
| High | 3 | 4 — Emergency; 5 — Famine | Combines the two highest phases for the four-class display. Preserve native phase and an explicit **Phase 5 critical flag**, never hide it within generic High. |

The [IPC Technical Manual v3.1](https://www.ipcinfo.org/fileadmin/user_upload/ipcinfo/manual/IPC_Technical_Manual_3_Final.pdf), printed pp.29 and 34–35, supplies the five severity distinctions. Combining Phases 4–5 is our proposal, not an IPC-recommended four-band standard. Source-phase mapping and interpretation also follow its mapping guidance (printed p.78): retain native labels and separate unavailable evidence. No new prevalence cutoffs are invented. Keep an original five-phase IPC view available; label any four-class view as **RuralScan reclassification of IPC acute area phase**, without implying IPC endorsement.

Not analysed, insufficient evidence, absent geometry, missing phase and out-of-period data remain **Not assessed**, not score zero. Preserve confidence, humanitarian-assistance and risk-of-famine fields; an area risk-of-famine flag is distinct from an observed Phase 5 classification. Household Phase 5 population also differs from an area classified Famine. Never combine current and projected periods into one assessment.

The acquired current dataset has **20 unique areas in Phase 3 and ten in Phase 4**. The proposal would therefore show Medium/Crisis and High/Emergency in this Haiti release. It should not manufacture Low/Very little areas to fill every class. The [proposal CSV](ipc-enssan-audit-20261127/four_class_proposal.csv) is research-only and is not consumed by the accepted rule bundle.

## IPC limitations and checks

- **Duplicate representations:** five area IDs repeat across polygon/point or multiple point features. Naively summing all features gives 11,959,463 people. Deduplicating consistent area IDs gives **11,224,797**, including **5,943,469 in Phase 3+**, exactly matching the official workbook. All 30 leaf-area phases, population counts and dates match. Never add departmental/national aggregate rows to leaf rows.
- **Points are not footprints:** eight areas, accounting for 2,664,521 analysed people, have only point representation. Do not buffer these into invented areas, assign a whole municipality automatically, or add point populations to overlapping polygons without the source's area accounting.
- **Geometry:** Ouest HT07+HT03 and Nippes HT01 have self-intersections. Among valid polygons alone, the pinned LSIB boundary overlap is 85.65%, with 11.60 km² of polygon overlap. This deliberately incomplete diagnostic excludes invalid polygons and unbuffered points; **it is not full IPC coverage**. No repair, rasterization or class-area totals are released. A separate exploratory repair was not adopted.
- **Dates:** the browser's month labels displayed Aug/Feb starts, whereas exported ISO dates and the published report agree on Sep/Mar. Use the verified ISO dates and retain this discrepancy. Although GeoJSON metadata lists two available periods, all 35 exported features carry only the current period; do not claim projected geometry was acquired from that metadata.
- **Meaning:** acute food insecurity responds to conflict, prices, displacement and assistance as well as agriculture/climate. It indicates current need, not the share of that need an NbS intervention can remedy. Refresh or explicitly retain a historical reference date after expiry; no stale-to-current fallback.
- **Conditions:** IPC results and derived IPC data retain [CC BY-NC-SA 3.0 IGO](https://www.ipcinfo.org/ipcinfo-website/privacy-policy/) attribution/share-alike/non-commercial conditions. This research acquisition does not establish permission for every later project use.

## ENSSAN use and geographic limitations

Table 41 supplies usable **reported geographic context**, now saved as a [CSV transcription](ipc-enssan-audit-20261127/enssan_geographic_prevalence.csv), not a provider-issued CSV. All 2025 rows are populated; missing camp values in 2022/2023 remain blank. Nine department-name rows are candidates for admin1 matching. Reste Ouest and Zone métropolitaine need exact complementary definitions; camps are a population group, not an additional department. No polygon join is performed.

Keep severe-FIES household prevalence separate from IPC area phase. Table 41 lacks four class shares, confidence intervals and geographic weights; it cannot reconstruct a national total or justify four area-prevalence bands. National Table 39 is retained as a comparator. The report gives 6,550 sampled households in its narrative versus 6,500 in Table 1; retain the discrepancy rather than silently reconcile it. The sampling frame and 2026 IPC assessment names are not proven interchangeable. Figure 11 is not digitized into estimates.

Next national acquisition targets are provider-issued weighted geographic tables, uncertainty, recall/scoring definitions and matching boundary IDs/polygons—especially the Ouest split and camp population universe. No outreach has been sent. Until those are verified, use the published table as qualified context; do not apply the IPC crosswalk to its percentages.

## Register and next step

This supersedes the earlier **public polygon access hold**, not scientific/runtime acceptance. Add source identity, actual native support, dates, licence, duplicates, geometry and uncertainty to any later T1/BIND proposal. Existing chronic IPC rules and accepted bindings remain unchanged pending a decision on the acute four-class proposal. No new opportunity variable is introduced.

[Infrastructure remains in scope](../infrastructure/README.md#approved-haiti-fallbacks-and-remaining-national-gaps): roads, facilities, power and buildings retain provisional fallbacks, coverage caveats and national-replacement needs. Climate-hazard selection remains pending Brayden. Food-insecurity geometry and scores cannot substitute for physical infrastructure exposure.
