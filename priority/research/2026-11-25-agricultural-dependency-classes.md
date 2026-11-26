# Agricultural dependency: measure and classification review

25 November 2026. Next variable after approved crop production gap. No new classes approved, calibrated or linked from T5 in this pass.

The existing profile defines this as agricultural employment share. World Bank indicator `SL.AGR.EMPL.ZS` reports annual agriculture employment as a percentage of total employment, sourced from ILO modelled estimates. Agriculture includes hunting, forestry and fishing. This is an employment measure, not household income dependence. The metadata cautions that imputed observations should not be used for country comparisons or rankings, and notes survey coverage and comparability limitations. [World Bank metadata: Long definition; Statistical concept and methodology; Limitations and exceptions](https://databank.worldbank.org/metadataglossary/world-development-indicators/series/SL.AGR.EMPL.ZS).

The current candidate has national (admin0) support. Retain national values as qualified context; they cannot differentiate hotspots within a country. Rasterizing national values does not fix this. An admin1-or-finer census or labour-force survey is needed for local differentiation, with consistent employment definitions, coverage and period.

A bounded search found no transferable published four-band standard for this exact metric. World Development Report 2008's agriculture-based / transforming / urbanized typology uses agriculture's contribution to growth and the rural share of poverty; it is not a set of employment-share thresholds. Do not repurpose those categories. [Official overview, Figure 2 and accompanying text](https://documents.worldbank.org/curated/en/873611468174885835/pdf/414560ENGLISH018082137297501PUBLIC1.pdf).

## Proposed approach for discussion

Use contextual Low / Medium / High terciles of comparable observed subnational employment shares within the selected country. This is a RuralScan distribution-based convention, not an ILO severity standard. Keep raw percentages visible. Do not invent a None / Very little boundary; zero estimates do not establish absence of agricultural livelihoods. Missing observations remain unknown.

Before calculating cuts, select the local source and reference population, pin period, document weighting and check sufficient distinct observations. Country-specific relative classes do not imply equal absolute dependency across countries. Do not pool imputed national estimates to create a global or World Bank income-tier ranking. No numeric cutoffs or reference sample are claimed here. If no suitable subnational data are available, retain the national contextual value and leave local classification unavailable.

## Search record

Primary-source search on 25 November 2026 covered ILO employment definitions, World Bank indicator metadata and WDR 2008's country typology, plus FAO-oriented searches. Queries included:

- `site.ilo.org employment agriculture share high medium low classification threshold`
- `site.worldbank.org SL.AGR.EMPL.ZS metadata agriculture hunting forestry fishing`
- `site.fao.org "agricultural dependence" "classification"`
- `"agricultural employment" "thresholds" "dependency"`
- `site.worldbank.org "agriculture-based" "transforming" "rural poverty" "2008"`

This is a bounded classification review, not an exhaustive literature search or formal source registration. No dataset acquired and no release decision recorded.
