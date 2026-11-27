# Aqueduct: Haiti coverage and basin aggregation

Checked 27 November 2026. **Technical coverage confirmed; useful as coarse basin context, weak for differentiation within Haiti.** No runtime binding or new analytical rule is approved by this inspection.

## Result

The bounded [Earth Engine Aqueduct 4.0 annual baseline](https://developers.google.com/earth-engine/datasets/catalog/WRI_Aqueduct_Water_Risk_V4_baseline_annual) extract contains 54 candidate features. Exact clipping leaves 53 positive-area fragments: 42 valid fragments representing **only two distinct `pfaf_id` basins**, plus 11 nodata fragments. All source geometries passed validity checks. The [saved inspection](aqueduct-haiti-audit-20261127/inspection.json) records each native identifier, value, class and clipped area.

| Basin / coverage state | Native baseline stress ratio | Approved review class | Area within boundary, km² | Share of whole boundary |
|---|---:|---|---:|---:|
| 764001 (38 fragments) | 0.152043 (15.2043%) | Low | 26,319.523 | 97.0597% |
| 764002 (4 fragments) | 0.003536 (0.3536%) | Very little | 683.735 | 2.5214% |
| Source nodata | — | Not assessed | 62.550 | 0.2307% |
| Outside source coverage | — | Not assessed | 51.024 | 0.1882% |

Valid coverage totals **27,003.258 km² / 99.5812%**; unknown totals **113.574 km² / 0.4188%**. Among valid coverage alone, 97.4680% is Low and 2.5320% Very little. No Medium/High class occurs in this extract; that does not establish absence of local water scarcity.

Denominator is the pinned [LSIB diagnostic boundary](haiti-diagnostic-inputs-20261126/README.md), **27,116.832 km²**, not an official national area, population, cropland, NbS opportunity footprint or infrastructure exposure. EPSG:6933 areas and independent WGS84 ellipsoidal boundary area differ by less than 0.000002%. Boundary choice remains more consequential than that numerical difference.

## Basin aggregation to use

1. Select by spatial intersection and clip to the chosen footprint. Decode native category and special/nodata flags using the existing [approved water rules](2026-11-25-water-stress-four-classes.md); preserve `pfaf_id`, `aqid`, `string_id` and original values.
2. Check that fragments sharing a basin have identical stress values/categories before dissolving them. Both Haiti basins pass. WRI identifies the source basin geography as [HydroBASINS level 6](https://github.com/wri/Aqueduct40/blob/master/data_FAQ.md); administrative/intersection fragments are not independent hydrological observations.
3. Report **area in each class**, with both whole-footprint and assessed-area denominators, plus unknown area. For an NbS result, repeat the intersection with that NbS footprint; these country percentages cannot stand in for it.
4. Do not average polygon rows or basin ratios into a national stress category. Ratios are not additive. An area-weighted ratio describes land assigned to stress values, not national demand divided by supply or WRI's demand-weighted country summary.

The failure mode is material: the same extract yields 13.79% from an unweighted fragment mean, 7.78% from an equal-basin mean and 14.83% from a land-area-weighted mean. Those diagnostic numbers cross a class boundary solely because weights differ. None is adopted as a classifier.

## Coverage and interpretation limits

- Aqueduct is a historical baseline (target 2019 with smoothed historical inputs), not a 2026 measurement. Native basin support survives rasterization; a fine output grid would not add information.
- Native country labels do not match the chosen boundary perfectly: 34 positive-area features have HTI labels, seven DOM and twelve blank. DOM-labelled overlaps total 12.297 km²; blank-labelled overlaps total 205.832 km². Filtering only `gid_0=HTI` would omit geometric coverage. These are dataset-boundary differences, not a territorial finding.
- One GEE-selected candidate, `00050000000000002e3d`, has no local intersection and is excluded. Its geometry lies near 95.6°E, 80.1°N. The acquisition retains it for audit; the reason for its inclusion by the upstream spatial query was not established.
- Source fragments have no meaningful positive-area overlap after clipping. Nodata and uncovered coast/island margins remain unknown, never Very little. No geometry repair or interpolation was used.
- This baseline measures water demand relative to available supply. It is not drinking-water access, seasonal drought intensity, flood depth or infrastructure damage.

## Dataset-register and infrastructure hand-off

This is a research sidecar to the existing water-stress candidate. It records source asset/version metadata, exact subset and input hashes, native fields, grain and aggregation. It does not create accepted T1/BIND rows, binding-verification receipts or new runtime rules. A later context-specific binding must carry these limitations, preserve unknowns and allow a better national source.

Roads, facilities, power lines and buildings remain in [infrastructure scope](../infrastructure/README.md#approved-haiti-fallbacks-and-remaining-national-gaps), with the existing provisional fallbacks and national acquisition gaps. National datasets should replace global versions where suitable. Infrastructure exposure still needs Brayden's hazard selections and a hazard-specific overlay; Aqueduct water stress cannot supply that exposure calculation.

## Reproduction

See [audit instructions](aqueduct-haiti-audit-20261127/README.md). Acquisition is bounded and network-dependent; the retained native subset supports offline recalculation. The analytical class meanings are read from the existing contextual tables, not hardcoded in the spatial script. Neither a successful download nor this coverage check establishes scientific acceptance for every use.
