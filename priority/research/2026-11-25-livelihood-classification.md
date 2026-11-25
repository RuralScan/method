# Livelihood drought, water scarcity and carbon: research proposal

**25 November 2026. Research and routing proposal, not an accepted classification or verified dataset binding.** Responds to Pete's instruction to identify rural livelihood problems and their magnitude from literature. No scientific decision, source keep or calibration is inferred from merging this document.

## Drought: classify agricultural stress, retain magnitude and recurrence

Prefer a crop/pasture-season measure linked to production stress, accompanied by affected area and recurrence. Use meteorological SPI/SPEI as explanatory hazard information or fallback; event anomaly classes do not establish long-term livelihood-risk classes. Indicator choice must follow the sector and impact being investigated: no index is universally best. [WMO/GWP drought-indicator guidance](https://www.droughtmanagement.info/indices/)

FAO ASIS offers a concrete starting point. Its seasonal vegetation-health index weights crop sensitivity through the growing season. ASI measures the fraction of agricultural area under stress; Drought Intensity classifies regionally aggregated seasonal vegetation health. The native analytical unit for those summaries is GAUL level 2, even when displayed on a 1 km raster. These products indicate agricultural stress, not measured household income loss. [FAO FAQ, questions 2–3](https://www.fao.org/giews/earthobservation/faq.jsp)

The official Drought Intensity legend was inspected directly:

| Published seasonal wVHI band (%) | Provider class | Proposed RuralScan display class |
|---|---|---|
| <25 | Extreme | high |
| 25–35 | Severe | high |
| 35–38 | Moderate | medium |
| 38–42 | Mild | low |
| >42 | None | none |

Source: [FAO official intensity legend](https://www.fao.org/giews/earthobservation/country/imgs/MUVHI_legend.JPG). **The four-class compression is our proposal, not FAO's classification.** Retain the five native labels. Printed ranges do not settle endpoint equality; use verified provider category codes, or check the producer algorithm before adopting numerical cuts. The current scalar catalogue only supports thresholds/terciles, so this categorical mapping needs a separately reviewed adapter. Off-season, missing data, no season and no cropland are distinct states, not zero concern.

For long-term need, propose showing seasonal severity, percentage affected, and fraction of observed growing seasons affected over a declared period. Do not invent frequency-class cutoffs or add redundant severity/extent/frequency components independently into MCDA. Examine local yield/pasture anomalies and impact records before choosing the representative concern. FAO's historical frequency product provides explicit affected-area event definitions; it does not validate arbitrary RuralScan severity-frequency scoring. [FAO ASIS products](https://www.fao.org/giews/earthobservation/asis/index_1.jsp?lang=en)

Check crop-mask age, static phenology, irrigation and cloud effects. Separate cropped and pastoral systems where the selected product supports them. Missing or unsuitable coverage remains unknown. [FAO FAQ, questions 8–14](https://www.fao.org/giews/earthobservation/faq.jsp) Earth Engine access is offered by request; no access request was sent and no asset was verified. The access page also documents alternative delivery services. [FAO access](https://www.fao.org/giews/earthobservation/access.jsp)

**Analytical inference:** averaging locally standardized SPEI over its fitting baseline largely measures an anomaly around that baseline, not chronic livelihood stress. Likewise, same-baseline standardized event frequencies can be similar by construction. This motivates impact/season checks, not rejection of SPEI for event monitoring. JRC distinguishes meteorological anomalies, soil-water stress and integrated agricultural risk; its integrated agricultural risk product already includes exposure/vulnerability, so reusing it alongside those components needs an explicit double-counting audit. [JRC drought indicators](https://joint-research-centre.ec.europa.eu/european-and-global-drought-observatories/drought-indicators_en)

## Water: three related quantities, three different classifications

| Source and quantity | Published breakpoints | RuralScan consequence |
|---|---|---|
| Aqueduct 4.0: withdrawals relative to available renewable supply | 10, 20, 40, 80 percent; five native categories | Preserve native classes and sub-basin support; no accepted four-class collapse yet. |
| SDG 6.4.2: withdrawals divided by renewable resources after environmental-flow requirements | 25, 50, 75, 100 percent; none through critical | Thresholds cannot be transferred to Aqueduct. National values cannot differentiate hotspots within a country. |
| Mekonnen & Hoekstra: blue-water consumption relative to availability after environmental and upstream use allowances | ratios 1, 1.5, 2; low, moderate, significant, severe | Monthly ecological-budget pressure; different numerator and denominator from the other two. |

Sources: [WRI technical note](https://www.wri.org/research/aqueduct-40-updated-decision-relevant-global-water-risk-indicators), [UN/FAO indicator metadata, definition and calculation](https://unstats.un.org/sdgs/metadata/files/metadata-06-04-02.pdf), [Mekonnen & Hoekstra 2016, introduction and methods](https://pmc.ncbi.nlm.nih.gov/articles/PMC4758739/).

Aqueduct's annual measure is demand-weighted across months, not a ratio of annual totals. Its arid/low-use category indicates severe scarcity; 9999 is a scarcity sentinel, while -9999 is missing. Preserve that distinction before numeric conversion. The provider recommends treating arid/low-use areas alongside high-stress priorities. A “none” class cannot be inferred from low recorded demand. These measures do not directly quantify household access or crop losses. [WRI FAQ, Water Risk Interpretation and Water Stress](https://github.com/wri/Aqueduct40/blob/master/data_FAQ.md)

The blue-water study provides four literature-based bands, but its global product represents 1996–2005 at 30 arc-minute resolution. It is evidence for interpretation, not a current pilot binding. Its lowest band means demand stays within the modelled blue-water budget; calling it “none” must mean **no modelled budget exceedance**, never no water-related livelihood problem. Its published inequalities leave exact boundary equality unspecified. [Original study](https://pmc.ncbi.nlm.nih.gov/articles/PMC4758739/)

Proposed next binding comparison: retain seasonal water competition/availability and agricultural impact together; choose the product that represents the pilot's farming systems and water sources. Rainfed crop stress and irrigated blue-water competition are complementary, not interchangeable. Do not apply national SDG labels to finer Aqueduct pixels or disguise coarse source support through resampling. No arbitrary reducer or numerical cutoff is requested from Pete.

## IPLC: overlap and safeguard follow-up, no score

Current project references already place mapped overlap in M3 characterization, tenure/safeguard follow-up in M2b Project risk, and consultation/consent follow-up in M6 Next steps. See `methodology-reference/content/m3-characterisation.md`, `m2b-project-risk.md` and `m6-handoff.md`. Pete's direction makes the current sidecar unscored. This clarifies presentation without interpreting Indigenous or community presence as a benefit, disadvantage, risk severity or automatic exclusion. A missing LandMark polygon is unknown without completeness evidence. Existing FPIC language in reference chapters is a downstream safeguard prompt, not a newly determined legal conclusion in this research.

## Carbon: observed loss need versus practice-specific potential

For prioritization, propose a separately defined carbon-loss/degradation concern: observed forest conversion/degradation, wetland loss/drainage, and soil-carbon decline where credible time-series estimates exist. Report their periods, uncertainties and distinct units. Land-cover loss area alone does not quantify carbon emissions; a stock snapshot is not a loss rate. Keep the legacy potential identifier visible only for traceability until its successor definition and binding are accepted.

Naturebase can supply practice-specific modelled avoided emissions/removals, useful for descriptive opportunity-space characterization or Next steps. It does not substitute for observed loss. The **live Data catalogue**, not the shorter About list, was inspected on 25 November 2026. It contains 20 individual pathways:

| Group | Individual pathways, in plain language |
|---|---|
| Protection (7) | Avoided coastal-wetland impacts; forest conversion; grassland conversion; peatland impacts; shrubland conversion; forest woodfuel harvest; savanna woodfuel harvest |
| Restoration (4) | Coastal wetlands; grasslands; peatlands; reforestation |
| Management (9) | Climate-smart forestry; cropland agroforestry; peatland management; cropland soil carbon; grazing-land soil carbon; cropland emissions; grazing-land emissions; savanna agroforestry; savanna fire |

Actual scope matters: coastal layers cover mangroves/tidal marshes; savanna agroforestry covers silvopasture; cropland emissions include rice/nutrient management; the forestry layer covers reduced-impact logging. No dedicated water-harvesting or riparian-buffer pathway was found; no dedicated freshwater-mineral-wetland or seagrass layer was confirmed. Those are coverage findings, not proof of zero benefit. Raster units are tCO2e/ha/year; table units tCO2e/year. Catalogue licensing is CC BY-NC-SA 4.0. [Naturebase live data catalogue](https://app.naturebase.org/data)

**RuralScan crosswalk inference:** match cropland agroforestry and silvopasture only to corresponding families; match reforestation to eligible restoration settings; coastal/peat layers to matching wetland families. Broad family labels cannot establish equivalence. Practice-specific masks, counterfactuals, horizon and area denominator still require verification. Do not use the all-pathways total as any individual practice's effect.

Naturebase accounting uses a 1 km² conceptual pixel, recognizes fractional biome coverage and overlapping pathway estimates, and applies hierarchy rules to prevent double counting. Crop and wetland priorities constrain how totals are assembled. Independent pathway rasters therefore cannot simply be summed. [Accounting rules v1.0, pp. 5–8](https://naturebase-shared-docs.s3.amazonaws.com/NCS_Accounting_rules_narrative.pdf)

## What this work changes now

The profile/routing sidecar records IPLC as a descriptor and blocks scoring through the unresolved carbon-potential alias. The drought/water proposals above are reviewable scientific candidates, with known product limitations and explicit next binding checks. No source registration, human keep, threshold acceptance, runtime computation or published classification is created.

New research retrievals are recorded in `retrievals.json`; only successfully downloaded files have hashes. Web/legend/catalogue inspection is identified as such, not claimed to be an acquired archival source. The three successful downloads were copied byte-for-byte to the team-library mirror; relative paths and local read-back verification are recorded. Remote access and formal acquisition/title checks remain unconfirmed. Normal source acquisition, team access and human finding review must precede release use. Existing six-source preparation and eight preserved findings remain unchanged.
