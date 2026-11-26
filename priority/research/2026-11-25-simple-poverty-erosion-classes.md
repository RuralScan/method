# Poverty and soil erosion: four-class draft

25 November 2026. Proposed display cutoffs for Opportunity Space variables. These are review proposals, not accepted classifications. No pilot country or season is required to review them.

**Poverty update:** the numerical draft below was withdrawn. Following the instruction to contextualize poverty and calibrate to lower-income settings, see the [computed low- and middle-income reference](2026-11-25-poverty-context-calibration.md). US thresholds remain excluded from that calibration; the earlier screening is retained as history.

**Soil erosion update:** the European 1/2/10 draft below is superseded by the [global GloSEM classification proposal](2026-11-25-soil-erosion-global-classes.md), using published 1/3/5 boundaries and combining higher bands. Everything below records the earlier screening, not the current proposal.

| Variable and raw measure | None / very little | Low | Medium | High |
|---|---:|---:|---:|---:|
| Poverty: population below the selected poverty line (%) | Withdrawn pending rationale | Withdrawn pending rationale | Withdrawn pending rationale | Withdrawn pending rationale |
| Soil erosion: modelled annual soil loss by water (tonnes/ha/year) | 0–1 | >1–2 | >2–10 | >10 |

All upper endpoints are inclusive. Missing, nonfinite and negative values are unknown; poverty above 100% is invalid. The first class means **very little**, not proof of absence or harmlessness. Existing ordinal scores remain 0, 0.33, 0.66 and 1.

## Poverty

Candidate dataset: [World Bank Global Subnational Poverty Atlas (GSAP)](https://datacatalog.worldbank.org/search/dataset/0042041/global-subnational-poverty-atlas-gsap), September 2026 vintage, using the share below $3.00/person/day in 2021 purchasing-power-parity dollars. The catalogue describes administrative-level-1 estimates aligned to common reference years. The [World Bank indicator definition](https://data.worldbank.org/indicator/SI.POV.DDAY) establishes the poverty measure, not these severity classes.

**Correction following Pete's challenge: the proposed 5%, 20% and 40% breaks are withdrawn.** They were convenient display choices, with no empirical or published severity rationale. Describing them as one in twenty, one in five and two in five explains the percentages but does not justify the boundaries. They must not be implemented or represented as evidence-backed defaults.

The [World Bank's poverty measurement explanation](https://www.worldbank.org/ext/en/topic/poverty/measuring-poverty) grounds monetary poverty lines in national poverty lines and purchasing-power comparisons. Those lines determine who is counted as poor; they do not establish 5/20/40 percent regional severity bands. The bounded search did not establish a transferable four-class headcount standard.

**Pete's direction, 25 November 2026:** pursue published classifications first. Distribution-based alternatives may use geographic regions, World Bank country income/status groups, or another justified grouping of economies; a global reference population is not mandatory. These are permitted comparison approaches, not approval of numerical thresholds.

If a distribution-based alternative is needed, classify positive poverty rates into lower, middle and upper thirds within the declared comparison group. This provides a reproducible rationale for *relative* low/medium/high poverty incidence, not absolute severity. Use the same indicator, poverty line, units and reference year within a comparison. Record the country-group definition and vintage, included subnational observations, exclusions and weighting; keep ties together and freeze resulting cutoffs for that reference. A regional or income-group class must be labelled as such: “high within lower-middle-income economies,” for example. Classes computed from different groups are not interchangeable absolute severities. No numerical quantiles have been calculated or accepted.

Do not label the lowest third “none.” A none category could be reserved for a valid unrounded zero estimate, described as “no poverty estimated at this line,” not proof that no poor people exist. A positive “very little” ceiling requires its own evidence or an explicit policy choice; it cannot be recovered merely by splitting the distribution. Missing observations remain unknown.

### Published-classification screening

Sources checked on 25 November 2026; this is a bounded research note, not formal source registration or acceptance.

| Published source and locator | Thresholds and rationale | Relevance to the current binding |
|---|---|---|
| [USDA ERS, Poverty Area Measures: Background and Uses](https://ers.usda.gov/data-products/poverty-area-measures/background-and-uses), “High and Extreme Poverty” | High poverty starts at 20%; extreme concentration starts at 40%. ERS links these thresholds to neighbourhood effects and correspondence with multidimensional area hardship. | A substantive published rationale, but based on the US Official Poverty Measure and US areas. This does not establish the same effects or cutoffs for international-line poverty in rural low- and middle-income economies. Retain as a transfer-limited comparator, not the global default. |
| [US Census, Areas With Concentrated Poverty: 2006–2010](https://www.census.gov/library/publications/2011/acs/acsbr10-17.html), Introduction | Four published categories: below 13.8%; 13.8–19.9%; 20–39.9%; at least 40%. | Demonstrates an actual published four-band classification. The lowest band is not “none/very little,” and the US measure/context differs. Do not relabel these categories or copy 13.8 into GSAP. |
| [World Bank WDI, Poverty and Inequality](https://datatopics.worldbank.org/world-development-indicators/themes/poverty-and-inequality.html), poverty measurement discussion | Below 3% is the global extreme-poverty policy target; zero is the SDG eradication goal. | Relevant policy benchmark, not a four-class regional severity standard. Do not combine this global target with US 20/40 thresholds to manufacture a purportedly published international scale. |

Outcome: published thresholds with explanations have been found, but this pass has not established a complete four-class scheme transferable to the selected international-line GSAP measure. Original 5/20/40 proposal remains withdrawn. Published map legend breaks alone are insufficient evidence of severity; the source must explain the meaning or basis, and any adaptation must be identified.

GSAP represents subnational population poverty, not automatically rural-only poverty. Until a rural-specific series is bound, display “Poverty” with “subnational population estimate” in its description. Rural masking does not convert a regional all-population headcount into a rural household estimate. Use one stated reference year and poverty line; do not mix national poverty lines with this international-line default. Actual download fields and units still need verification before a runtime binding is claimed.

## Soil erosion

Candidate quantity: the annual soil-loss output from [JRC GloSEM](https://esdac.jrc.ec.europa.eu/themes/global-soil-erosion), not SoilGrids properties or the rainfall-erosivity factor alone.

Classification basis: [JRC, *Soil threats in Europe*, Table 14.1, printed page 177](https://esdac.jrc.ec.europa.eu/public_path/shared_folder/doc_pub/EUR27607.pdf#page=177). The table reports low 1–2, moderate 3–10 and high >10 tonnes/ha/year. Our continuous-value adaptation fills the printed 2–3 gap by assigning >2–10 to medium, adds 0–1 as very little, and assigns equality at 1 to very little. These changes are explicit RuralScan proposals. The source is European; using these bands as global scoping defaults is a transfer proposal, not a globally validated soil-loss tolerance standard.

The [older global GloSEM download](https://esdac.jrc.ec.europa.eu/content/global-soil-erosion) is a 25 km resampling for 2001/2012; the original 250 m model resolution must not be claimed for that distributed file. Newer 100 m GloSEM 1.3 targets croplands. Exact edition and coverage remain a dataset-selection task, separate from reviewing these cutoffs. The measure covers modelled water erosion, not wind erosion, all gully processes or measured NbS benefits.

## Scope correction

Proceed variable by variable with dataset, measure, four classes and a short source note. Pilot coverage, seasonal fit and tile alignment belong to later application checks; they do not block these classification proposals. Historical binding investigations remain useful technical records but do not set the scope of this classification pass.
