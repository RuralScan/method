# Naturebase savanna agroforestry / silvopasture — binding inspection

26 November 2026. Technical inspection authorised by Pete. **Sample checked; scientifically accepted = false; runtime ready = false.** No analytical rules, four-class cutoffs, suitability masks or binding registry rows changed.

## Finding and Haiti disposition

Naturebase's silvopasture pathway matches additional trees in grazing systems conceptually, but the inspected release provides **no positive mapped opportunity in Haiti**. Every native raster cell centre inside the checked Haiti boundary stores zero; all Haitian administrative mitigation and footprint fields contain `NA`. Keep it as a global research comparator, **held for Haiti quantitative comparison**. Do not interpret those outputs as evidence that Haiti lacks feasible silvopasture or carbon benefit.

This layer estimates intervention-specific mitigation potential. It cannot fill the carbon-loss concern or justify its high/medium/low/none classes.

## Verified binding facts

| Field | Result |
|---|---|
| Producer | [Naturebase Savanna-based Agroforestry, pathway 11](https://app.naturebase.org/data/nb/11), citation dated 15 April 2025, Silvopasture v3 |
| Acquired package | [grs_sba_total.zip](https://naturebase-shared-docs.s3.amazonaws.com/Data-download/grs_sba_total.zip), 186,649,911 bytes; server last-modified 19 November 2026; full archive CRC check passed |
| Hosted raster | Catalogue's `https://action-mapper.s3.amazonaws.com/naturebase_cog/grs_sba_total.tif` returns HTTP 404; ZIP fallback works |
| Actual raster | `grs_sba_tco2eha.tif`, band 1, Float32; EPSG:4326; 40,076 × 14,140; 0.00898315284119522° cells, nominally 1 km |
| Decode | Scale 1; offset 0; nodata −3.4028234663852886e38; zero is stored, including offshore. Band unit tag absent; producer raster-specific documentation gives tCO₂e/ha/year |
| Carbon pools | Combined aboveground biomass, belowground biomass and soil organic carbon. Only one total raster; no separate pool, uncertainty, eligibility or fractional-area raster supplied in package |
| Time | Modelled annual potential, not observed annual change. Producer describes 2015 tree cover, grazing extent from Chapman et al. (2020), and soil accumulation continuing to accounting horizon 2035. Publication year is not automatically grazing-map observation year |
| Contents | One raster, administrative CSVs for levels 0–2, administrative geodatabase and README |
| Metadata defects | README names `grs_sba_total.tif`, unlike actual member; its CRS text contains `WHA83`, while raster header is EPSG:4326. Use inspected header |

Package SHA-256: `04ea543a41cc4329bb567eaff7db91101100c2b17eb689903b44af6b263f856f`.
Raster SHA-256: `2d9fd91b4fa69bfe12f2fc681c9a50bdb363cb4985ee21acb62fd7140d29e0ec`.
Catalogue-level CC BY-NC-SA 4.0 condition recorded in the [preceding crosswalk](2026-11-26-naturebase-nbs-crosswalk.md) remains applicable to intended-use review; download access does not establish unrestricted reuse.

## Haiti observations and integrity checks

| Check | Observation |
|---|---|
| Native cell centres inside USDOS/LSIB_SIMPLE/2017 Haiti | 28,815 valid cells; all zero; no nodata or positive values |
| WorldCover 2021 stratified diagnostics | 1,440 points, 160 in each of nine classes; all zero. These occupy 1,292 distinct Naturebase cells |
| Grassland and shrubland strata | 0/160 positive in each. WorldCover grass/shrub classes do not independently establish managed pasture |
| Producer administrative tables | Haiti national row, all 10 department rows and all 42 level-2 rows have `NA` for mitigation and pathway hectares; preserve missingness |
| Positive control outside Haiti | Raster value 1.690944 at approximately −6.75084°, 58.27820° verifies that the global file is not uniformly zero; not ecological validation of that pixel |
| Geographic inclusion | Checked window fully contains the supplied Haiti boundary bounding box; cell-centre inclusion, not all-touched rasterisation |

These checks establish access and actual stored values, not accuracy, pasture completeness or absence of local opportunity. Zero-filled raster and `NA` tables provide no defensible numeric Haiti benefit estimate. Do not coerce table `NA` to zero, divide missing mitigation by missing footprint, or assign “none/very little” solely from this product. No area-weighted national statistic is inferred from stratified samples.

## Method interpretation and remaining holds

**Family match.** Closest to `agroforestry__silvopastoral`, specifically additional trees in managed grazing land with limited existing tree cover. Producer averages silvopasture, hedgerow and parkland fluxes within climate zones and uses broader biome/geographic fallbacks. The total cannot distinguish planted silvopasture from tree-retention management, species, livestock systems or planting arrangements. Mixed crop–livestock systems need explicit crop/grazing allocation. A generic grassland class does not authorise planting in naturally open ecosystems.

**Area weighting.** Producer applies possible additional tree-cover percentage and the non-cropland fraction of the nominal 1 km² accounting cell. See [accounting rules](https://naturebase-shared-docs.s3.amazonaws.com/NCS_Accounting_rules_narrative.pdf), section I(c), PDF page 6. Values are already weighted opportunities, not coefficients per hectare planted. Do not multiply directly by RuralScan planted hectares or apply the non-cropland fraction again. Cropland and grazing pathway totals cannot both be assigned to the same physical intervention. README also warns that its raster-footprint hectare estimates can overestimate implementation extent; geographic raster cells are not uniformly 100 ha.

**Unresolved producer inconsistency.** Both current catalogue and package Methods describe a conservative forest-suitability/historically forested filter. Their caveats also state that the unmasked maximum silvopasture extent was used. These may describe different processing stages, but supplied material does not resolve that interpretation. Preserve the discrepancy; do not attribute Haiti's all-zero result to either filter or claim a verified ecological exclusion. Intermediate pasture, tree-cover, filter and fractional-allocation layers or producer clarification would be needed to diagnose the cause. No message sent.

**Upstream science is not the same raster.** The [2024 source paper](https://link.springer.com/article/10.1186/s13021-024-00268-y) used expert-derived tree-cover opportunities, natural-regrowth biomass rates and root-to-shoot ratios; Naturebase v3 describes different flux inputs and includes soil carbon. The paper cautions against afforestation of naturally open grasslands. Its Methods also use an older grazing tree-cover baseline than the current Naturebase narrative. Do not silently transplant its dates, rates or uncertainty into v3. Its [producer repository](https://github.com/Catalytic-Science-for-NCS/Trees_in_Agriculture) links a [GEE grazing-land script](https://code.earthengine.google.com/3c27e1a6360bdcf0133ad04c625c0669); link verified, script not executed. This is a follow-up lead for intermediate inputs, not a verified equivalent hosted Naturebase product.

## Recorded outcome and next step

Resolved: ZIP acquisition, integrity, raster identity/decode, combined pool definition, actual Haiti raster/table results and global positive control. Still held: useful Haiti applicability, producer extent discrepancy, exact implementation denominator, family-specific transfer, uncertainty and working cloud raster. No accepted quantitative Haiti binding proposed.

Subsequent [reforestation inspection](2026-11-26-naturebase-reforestation-binding.md) is complete; its area/additionality and transfer holds remain explicit. [Infrastructure work remains active](../infrastructure/README.md), including Haiti national-data replacements and qualified roads, schools, health, power-line and building fallbacks.

[Reproducible audit](naturebase-savanna-audit-20261126/README.md) preserves metadata, hashes, all sample observations and Haiti table rows.
