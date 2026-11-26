# Poverty classes calibrated to comparable economies

25 November 2026. Provisional contextual calibration, not an accepted runtime rule.

**Subsequent direction approved by Pete:** use global references separately within World Bank income tiers; regional or national adaptation requires documented justification. The pooled low/lower-middle reference below records the initial comparison and is no longer the recommended default. Approval of this reference design does not constitute exact-content acceptance of the numerical rules.

Table representation: one poverty variable in T5 now links through `classification_set_ref` to three [CSV classification records](../classifications/README.md), one for each income tier. Each carries the same variable/concern identity and measure, plus context, cutoffs and reference-sample provenance. The review selector uses pinned FY2027 country membership, with no cross-tier fallback. This implements the table extension; scientific acceptance and runtime activation remain separate.

Poverty must be contextualized to the setting. US poverty-area thresholds are excluded from this calibration. Published, applicable classifications remain preferred. This interim analysis uses the distribution of World Bank poverty estimates within comparable economies because no transferable published four-class headcount scheme was established in the preceding search.

## Initial reference and classes

Interpret “medium to lower income” as **low- and lower-middle-income economies** for the initial reference, and retain upper-middle-income economies as a comparison. This keeps the cohort choice visible and reversible.

Measure: percentage of the population below **$3.00 per person per day, 2021 PPP**, representing extreme monetary poverty. Reference: **2024 lined-up estimates**, World Bank GSAP Fall 2026 edition, grouped using **FY2027 income classifications**. This is a current peer-group comparison applied to 2024 poverty estimates, not a reconstruction of 2024 country income classifications.

| Provisional class | Poverty headcount (%) |
|---|---:|
| Low within the reference group | 0 to 19.11333333333333 |
| Medium within the reference group | >19.11333333333333 to 50.63 |
| High within the reference group | >50.63 to 100 |
| None / very little | No justified separate band established |
| Unknown | Missing or invalid input |

Display the cutoffs as **19.1% and 50.6%**, while calculation retains the generated full-precision values. For example, 10% is low, 30% medium and 60% high under this reference. These labels indicate relative incidence; “low” does not imply negligible hardship.

The reference contains **864 subnational representative areas in 62 economies**, equally weighted by area record. Linear-interpolated one-third and two-thirds quantiles each yield 288 areas per class. Rates of zero remain in the distribution: the workbook stores rounded estimates, which cannot establish true absence of poverty. There is no invented positive “very little” ceiling.

## Why the setting matters

All rows below use the same $3.00 measure and reference year; only the income-group membership changes. Cutoffs shown rounded for reading.

| Comparison set | Economies | Areas | Low/medium cutoff (%) | Medium/high cutoff (%) |
|---|---:|---:|---:|---:|
| Low income | 19 | 339 | 40.86 | 67.17 |
| Lower-middle income | 43 | 525 | 5.92 | 39.49 |
| Upper-middle income | 43 | 745 | 0.22 | 4.27 |
| **Low + lower-middle income: initial reference** | **62** | **864** | **19.11** | **50.63** |
| All low- and middle-income economies | 105 | 1,609 | 2.10 | 26.07 |

A class computed within one peer group is not an absolute severity equivalent to that class in another. The primary reference gives equal weight to each source area, so countries with more areas contribute more observations. It estimates the distribution across available areas, not across equally weighted countries or people. No population weighting was possible from the supplied table.

Changing the poverty line also changes the question. For the same 864-area initial reference, the **$4.20/day** series gives cuts of **40.203333333333326% and 73.38000000000001%**. This is a separate, broader poverty measure associated with lower-middle-income settings, not a rescaling of the $3.00 indicator. Retain it as a comparison; do not mix lines within one reference distribution.

## Source selection and checks

- [World Bank GSAP catalogue](https://datacatalog.worldbank.org/search/dataset/0042041/global-subnational-poverty-atlas-gsap), [source workbook](https://datacatalogfiles.worldbank.org/ddh-published/0042041/DR0052555/AM26%20-%20GSAP%20data.xlsx): sheet `Data 2024`, fields `poor300_ln` and `poor420_ln`; dictionary specifies fractions 0–1 multiplied by 100 for percentages. Stable observation identity uses the source `geo_code`.
- [World Bank country groups](https://datahelpdesk.worldbank.org/knowledgebase/articles/906519-world-bank-country-and-lending-groups), [classification workbook](https://ddh-openapi.worldbank.org/resources/DR0095333/download): `List of economies`, join `Code` to GSAP `code`. The workbook's notes explicitly identify FY2027. Income groups were read from the file, not inferred from poverty values.
- The GSAP sheet contains 1,977 observations from 172 economies. National-only records are excluded before spatial calibration. In the initial reference, Honduras, Nicaragua, South Sudan, Syria and Venezuela have national-only rows; Afghanistan, Eritrea, Cambodia, North Korea and Somalia have no source rows. No missing values are imputed.
- All 864 selected poverty rates are valid fractions and their source geographic IDs are unique. Survey years range from 2009 to 2024, although all estimates are aligned to 2024; the largest survey-vintage gap is 15 years. They are lined-up estimates, not 864 observations collected in 2024.
- There are 29 reported zero estimates. There are also 107 missing newer geometry IDs; original `geo_code` remains present and unique. The statistical calibration does not claim that a spatial boundary join has been verified.
- Source areas are representative survey geographies with mixed administrative arrangements, not uniform pixels. These are all-population estimates, not rural-only rates.
- Quantiles use the existing method's `(n-1)*q` linear interpolation. An independent `statistics.quantiles(..., n=3, method='inclusive')` calculation agrees to numerical precision. Class counts reconcile, ties remain together, and no source workbook was modified.

## Reproduction

The companion `poverty-calibration-20261125/` directory contains the calculation script, generated results and the initial reference sample. Run with the two downloaded source files:

```sh
python3 calibrate.py --source GSAP_AM26.xlsx --groups WB_income_groups.xlsx --sheet 'Data 2024' --field poor300_ln --field poor420_ln --cohort 'low=Low income' --cohort 'lower_middle=Lower middle income' --cohort 'upper_middle=Upper middle income' --cohort 'low_lower_middle=Low income|Lower middle income' --cohort 'all_low_middle=Low income|Lower middle income|Upper middle income' --output calibration.json
```

Dependencies: Python, openpyxl for read-only source access. No analytical rule is installed in runtime by this script.

The complete source and calculation bundle is retained in the team-library mirror under `0_Methodology_&_Frameworks/priority_classification/poverty_calibration_2026_11_25/original_sources_and_calibration.zip`. All 14 archive members were read back and verified byte-for-byte against the local originals. Archive SHA-256: `cb148f8b9cd5878892299f0c76eee5901ed3e4a66b927f32aa3631751c99c22d`. Use the archived originals for reproduction: the separately copied XLSX files changed bytes after placement in the sync folder. Remote team access has not been independently checked.

Source workbook SHA-256: `a4b47f19b3cac0d9a3604bdb174de1a6f2b56908e3afbb143e68f8a139330671`.

Income-group workbook SHA-256: `f164422e0c9868d12775727c88fc5fc4242512acc4006cc501fbcc5792c96b5d`.

Initial reference sample SHA-256 (canonical JSON, without trailing newline): `09cc6eb43a6572edf5d469c775fb290ef2a813642d0db5cb15fbc45ffda79c7b`.

Validation: the methodology preview rendered the updated chapter, resolved its citations and internal links, and passed the content/version checks. The full build reports one existing environment mismatch: the available evidence checkout is `eed6178c`, while the methodology describes operating revision `77a6c6d8`. The personal-attribution check was not run because its names list was not supplied. This local preview is not a publication artifact.
