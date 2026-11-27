# Haiti food insecurity: historical source verified, current binding held

27 November 2026. The next non-climate binding check covers the already approved IPC **chronic** food-insecurity interpretation. No classification, accepted dataset binding or runtime release changes here. The nine core variables and optional infrastructure scope remain unchanged.

## Result

Keep current Haiti chronic food insecurity **Not assessed / requires local assessment**. The national source located and acquired is from October 2015; the IPC catalogue ends its validity on 31 October 2020. Newer acute analyses cannot be passed through the chronic four-level crosswalk. This resolves the source-identification question, not the current-data hold.

| Check | Finding | Binding consequence |
|---|---|---|
| National source | CNSA's [chronic catalogue](https://www.cnsahaiti.org/ipc-chronique/) links the [October 2015 bulletin](https://www.cnsahaiti.org/Web/Bulletin_IPC/2014/Rapport%20IPC_chronique_version%20finale.pdf). Original PDF acquired and hashed | National provenance verified; the `/2014/` URL directory does not make this a 2014 assessment |
| Temporal applicability | [IPC analysis 459668](https://www.ipcinfo.org/ipc-country-analysis/details-map/en/c/459668/?iso3=HTI) lists 1 October 2015–31 October 2020. Bulletin page 3 permits up to five years unless major structural change occurs | Historical context only; no current applicability established |
| Native coverage | Bulletin page 1 footnote: 15 defined livelihood-based areas, two unassessed; page 4 has 13 area rows. Page 3 identifies missing areas and warns about finer-scale variation | Country scope does not mean complete coverage or department-level support. No missing-to-zero conversion |
| Spatial implementation | Acquired PDF provides narrative and population table, not a verified polygon package with join fields | Exact geometry, stable area IDs, published area-level field and missing-value encoding remain unverified; do not invent field names or join by approximate department names |
| Current alternative | [IPC analysis 1165467](https://www.ipcinfo.org/ipc-country-analysis/details-map/en/c/1165467/?iso3=HTI), released 28 October 2026, covers acute conditions September 2026–February 2027 and a March–June 2027 projection | Useful alternative lead, but a different measure. No automatic replacement, mixing of current/projected periods or approved acute-to-four-class mapping |
| Hosted access | [IPC API documentation](https://www.ipcinfo.org/ipc-country-analysis/api/) describes acute data, with chronic data listed for future addition. Public map has a Chronic mode, but no Haiti polygon download was verified in this check | Do not equate map display or API availability with an acquired chronic binding. No API key request submitted |

The existing interpretation remains IPC chronic levels **1 → Very little, 2 → Low, 3 → Medium, 4 → High**. These are published area classes, not household percentages. Minimal does not mean no food insecurity. Reusing this mapping still requires an applicable assessment and its exact geographic support.

## Fit with T1, BIND and the classification table

The classification table already records `requires_local_assessment`. Preserve it. A future T1 record needs the actual dataset/version, native analysis-area support, validity period, licence and coverage caveats. A Haiti-specific BIND record would select that source for `admin_country=HTI`; it cannot make an expired assessment current. Partial areas must retain an explicit assessment mask.

No historical T1/BIND rows or the evidence-pinned fourteen-candidate catalogue are modified. This inspection is a research sidecar, not a source-register promotion or a binding-verification receipt.

To release a current binding, acquire an updated applicable chronic assessment from CNSA/IPC, its matching polygons and codebook. If an acute source or another national food-security measure is preferred instead, review its definition and class mapping explicitly first. No outreach has been sent.

## Acquisition, limitations and next work

[Inspection record](food-binding-audit-20261127/inspection.json) records metadata, URLs, access outcomes and holds. [Acquisition receipt](food-binding-audit-20261127/acquisition.json) pins the PDF, national catalogue snapshot and browser observation. The source archive was copied to the team-library mirror and read back; remote team access was not verified. Direct IPC HTML requests returned 403; official indexed pages supplied catalogue/API metadata. Searches of IPC and CNSA found no newer chronic release; this is a bounded finding, not proof none exists.

[IPC terms](https://www.ipcinfo.org/ipcinfo-website/privacy-policy/), section I.C, specify CC BY-NC-SA 3.0 IGO for IPC results and require source/licence/update-date attribution. The research inspection does not establish permission for every later deployment. Original materials retain their source terms, not the repository's MIT licence.

Next non-climate binding check: Aqueduct water-stress coverage and basin aggregation for Haiti, against its existing approved category mapping. [Infrastructure](../infrastructure/README.md) remains active: roads, schools, health facilities, power lines and buildings keep their provisional sources and national replacement needs. Food-security classes are not physical hazard footprints for infrastructure exposure. Climate indicator selection remains pending Brayden's confirmation.
