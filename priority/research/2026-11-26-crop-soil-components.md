# Cropland soil-carbon components: separation and Haiti applicability

26 November 2026. Research candidates only; no BIND activation, accepted effect, class boundary or carbon-loss rule.

**Separate no-till, higher-input, joint and biochar candidates have now been checked for Haiti.** User approved Soils Revealed v3 CC BY 4.0 acceptance and the three downloads on 26 November 2026. All three full global originals were acquired and match the publisher's MD5 checksums. Earlier native Haiti windows for inputs and joint management, acquired with HTTP range requests, were independently reproduced from the full files: identical masks, statistics and all 1,440 sampled values. All three soil scenarios share the same Haiti mask. **The joint scenario is 6.08–10.65% larger than the sum of the separate gains at every readable Haiti cell.** This verifies non-additivity within Soils Revealed, not a decomposition or reconciliation of Naturebase's combined Haiti estimate. Published Earth Engine paths remain inaccessible to the current caller.

## Component table

| Component | Separate source and meaning | Haiti evidence and current status | Appropriate use |
|---|---|---|---|
| Minimum disturbance / no-till | Soils Revealed `scenario_crop_MG_dSOC_Y20.tif`, file 4202144: change from business as usual to no-till | **80,187 positive native Haiti cells**, 368,805 masked; **49/160 cropland sample points positive**, 111 masked. Producer MD5 matches. Local residue-placement research supports process relevance, not a national effect rate. | Candidate comparator only where no-till is the proposed change and current tillage is established. Not a generic effect for all reduced tillage, contouring or water harvesting. |
| Higher organic inputs | `scenario_crop.I_dSOC_Y20.tif`, file 4202142: higher inputs without manure, consistent with cover crops and other greater residue return | **80,187 positive native Haiti cells**, 368,805 masked; **49/160 cropland sample points positive**, 111 masked. No isolated mulching, compost or specific cover-crop map established. | A broad input-management scenario. Do not label its full gain as mulch-only or manure/compost treatment response. |
| Both management and inputs | `scenario_crop.MGI_dSOC_Y20.tif`, file 4202145: combined no-till and higher inputs | Same native support and sample coverage as the individual scenarios. Joint gains exceed their sum throughout readable Haiti support | Use the documented joint scenario if both interventions match. The checked joint values do not equal the sum of the single scenarios; do not add the joint scenario to either single scenario. |
| Biochar, constrained | `bc_100_constrained.tif`, file 7354742: annual residue-derived biochar carbon remaining after 100 years, allowing for sustainable harvesting and livestock competition | **281 positive native Haiti cells**, 48 masked; **149/160 cropland sample points positive**, 11 masked | Separate coarse resource-potential comparator; not an accepted RuralScan practice or an investment estimate. Current local residue uses and production systems still required. |
| Biochar, technical upper scenario | `bc_100_tech.tif`, file 7354744: same persistence calculation using all generated residues | **314 positive native Haiti cells**, 15 masked; **156/160 cropland sample points positive**, 4 masked | Upper scenario for comparison, not feasible supply. No constrained value exceeds its technical counterpart where both are readable. |

Soil scenario files are listed in [Soils Revealed v3](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/HA17D3); biochar files in [Biochar from crop residues v1](https://dataverse.harvard.edu/dataset.xhtml?persistentId=doi:10.7910/DVN/Y6NGFM). These exact file names matter: input and combined filenames use a dot after `crop`, while management-only uses an underscore. The UI/GEE scenario keys use underscores throughout.

## Units, support and non-additivity

**Soils Revealed:** 20-year SOC stock change, Mg C/ha, 0–30 cm. The application describes 2018–2038 scenarios and nominal 250 m support. Its [producer application documentation](https://github.com/Vizzuality/soils-revealed/blob/9eb9e12a434d997edaacd52f935d0d5fe9a819d7/components/map/constants.js) assumes immediate adoption across eligible land and does not model local feasibility or existing adoption. These are potential changes, not observed annual sequestration. The original no-till header and remote original input/joint headers verify the same approximately 250 m grid: EPSG:4326, 0.002276188° steps, Float32, 60,934 × 158,159 cells, nodata approximately −3.4 × 10^38. Preserve this nodata mask; do not fill it with zero. The upstream stock-change convention differs from Naturebase's annualised, fraction-weighted product.

**Coverage warning:** each soil scenario has readable values at only 49 of 160 diagnostic WorldCover cropland locations. Masks agree exactly across 448,992 native Haiti cell centres: 80,187 positive values and 368,805 missing, with no valid zero or negative values. Source support and independently mapped cropland do not coincide. Some positive cells also intersect points labelled built-up, tree cover or water by WorldCover, consistent with a different/coarser source land-use footprint. These are not evidence for applying cropland management to those land uses. Reconcile an appropriate observed cropland mask and baseline before local transfer. This is a point diagnostic, not an area-based completeness estimate; a missing value does not show that no-till is inapplicable or has zero benefit.

The native Haiti diagnostics below describe model outputs on their valid source footprint, **not locally calibrated treatment effects or national area-weighted benefit estimates**. Units are Mg C/ha over 20 years. No resampling or nodata-to-zero conversion was used.

| Soil scenario | Minimum | Median | Maximum | Valid cells |
|---|---:|---:|---:|---:|
| No-till | 1.780 | 3.886 | 6.801 | 80,187 |
| Higher inputs | 0.992 | 3.648 | 6.384 | 80,187 |
| Joint no-till + inputs | 2.940 | 8.337 | 14.589 | 80,187 |

The pixelwise joint-minus-sum difference is 0.169–1.404 Mg C/ha over 20 years (median 0.803). All 80,187 common valid cells exceed the sum by more than 0.00001 Mg C/ha; that tolerance is a floating-point diagnostic, not an analytical class boundary. The joint/sum ratio is 1.060835–1.106524. Use the joint layer where both changes match the proposed intervention, rather than synthesising it by addition. This model interaction is not field proof of the same incremental gain in Haiti.

**Biochar:** downloaded TIFFs are Float32, EPSG:4326, 4,320 × 2,160 cells with 0.083333° steps (approximately 5 arc minutes, roughly 9 km in Haiti). README units are **Mg C/year/pixel**, not Mg C/ha. The 100-year label describes persistence of annual biochar production: **do not divide by 100 to create an annual rate**. Nodata is NaN; masked cells remain unknown. The 1,440 WorldCover-stratified samples collapse to 340 distinct biochar cells and are not an area-weighted national sample.

The Haiti cell-centre diagnostic uses 329 grid cells under `USDOS/LSIB_SIMPLE/2017`. It sums to 368,297.60 Mg C/year for technical potential and 174,233.56 Mg C/year for constrained potential, over their different valid supports. **These are boundary-convention diagnostics, not authoritative national totals**: coarse cells can straddle borders and coastlines. No conversion into project benefits or subtraction from Naturebase's national estimate is justified.

The biochar study uses approximately 2010 MapSPAM production and a 5-arc-minute resource model. Its constrained scenario allows for harvesting sustainability and livestock use; it is not a complete local feasibility or life-cycle model. Upstream crop inventory covers 42 categories, while the paper describes a 34-crop subset selected for residue assessment. Do not call it every Haitian crop or current-year production. [Karan and colleagues, methods §§2.1–2.4](https://onlinelibrary.wiley.com/doi/full/10.1111/gcbb.13102)

The same residues can contribute to soil cover, livestock feed or biochar feedstock. These uses compete. Do not sum independent maximum scenarios, count the same residue carbon twice, or calculate a biochar residual as Naturebase total minus unrelated soil scenarios. No exact version/processing equivalence between these upstream files and Naturebase's bundled release has been demonstrated.

## Haiti applicability

Local relevance is supported, but national calibration remains absent:

- A Central Plateau field study followed maize, bean and cover-crop residue decomposition during 2013. Surface residues decomposed more slowly than buried residues. This supports distinguishing residue type and placement; a short litterbag study does not validate a 20-year SOC stock increment or national no-till benefit. [Lynch and colleagues, 2016](https://link.springer.com/article/10.1186/s40064-016-2651-1)
- A historical International Biochar Initiative project profile describes sugarcane-bagasse conversion and soil-amendment trials in northern Haiti, alongside cooking-charcoal production. This demonstrates a locally relevant pathway, not present national capacity or measured durable removal. **Charcoal burned for cooking is not biochar stored in soil.** [Carbon Roots International profile](https://biochar-international.org/carbon-roots-international/)

For local application, establish current tillage and residue practices, the proposed change, crop/residue supply, competing uses, and the actual fate of produced char. Global baseline assumptions cannot substitute for those observations. Soil-process evidence does not automatically define a suitability threshold, and a positive resource cell does not establish a feasible production site.

## Status and next action

1. Keep separate management, input, joint and biochar entries in research context. Retain the combined Naturebase raster only as the previously qualified comparator.
2. **CC BY 4.0** acceptance and all three Soils Revealed downloads were approved on 26 November 2026. The repository's “custom terms” label resolves to that licence. Biochar is **CC0 1.0**. No name/email was submitted.
3. Haiti coverage, masks and the joint-versus-sum comparison are verified from native original-file windows. Full-original MD5 verification passed for all three files, and full-file results reproduce the native subset results exactly. Native subset and global-file checksums are recorded separately. Country applicability still requires an observed cropland footprint, current management and residue-use data; no scientific acceptance or runtime activation follows automatically.
4. Keep infrastructure in scope under the [infrastructure record](../infrastructure/README.md): roads, power lines, buildings, schools and health facilities, with global fallback limitations and preference for national replacements. Road access or nearby buildings alone do not demonstrate biochar-processing capacity. No new infrastructure or hazard score is introduced.

Audit: [source metadata, probes and verification](crop-soil-components-audit-20261126/README.md). No email sent, formal evidence extraction performed, or production schema changed.
