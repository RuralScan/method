# Contextual classification table

T5 keeps one row per variable. Its new `classification_set_ref` links to `rules.csv#<rule_set_id>`; the rule set holds context-specific rows. This extension is tracked under [method issue #103](https://github.com/RuralScan/method/issues/103), with columns frozen in `columns.json` and the T5 manifest. It does not reshape the historical T5 table.

| File | Purpose |
|---|---|
| `rules.csv` | Measure binding, context, boundaries, class meanings, rationale and version |
| `country_groups.csv` | 218 economies and their pinned FY2027 World Bank income groups and regions |
| `reference_samples.csv` | 1,609 observed subnational area records used to reproduce poverty terciles |
| `sources.csv` | Source URLs, original-byte hashes and locators; technical provenance, not formal evidence acceptance |
| `rules.json` | Generated typed bundle; never edit directly |

## Poverty

Measure: population share below $3/day in 2021 PPP, GSAP Fall 2026, estimates aligned to 2024. The source fraction is multiplied by 100. Global reference distributions are calculated separately within FY2027 income tiers, with equal weight per published area record. They are not population-weighted or equally weighted by country. National-only observations are excluded. See the [calibration and source archive](../research/2026-11-25-poverty-context-calibration.md).

| Income tier | Areas | Low upper bound (%) | Medium upper bound (%) |
|---|---:|---:|---:|
| Low (LIC) | 339 | 40.86 | 67.17 |
| Lower-middle (LMC) | 525 | 5.92 | 39.49 |
| Upper-middle (UMC) | 745 | 0.22 | 4.27 |

Displayed bounds are rounded; CSV stores full precision. Values above the second bound are high. These are relative classes within each tier, not comparable absolute severity labels. Poverty needs contextual review before application. Regional or national alternatives need an explicit rationale and versioned record. There is no high-income default. Zero estimates remain low; no separate none/very-little band is justified. Missing or invalid values remain unknown. Estimates cover all population, not rural households alone.

## Selection and checks

Review selection precedence is explicit country > region > income tier > global. Country membership must match the pinned vintage; unsupported contexts and ambiguous selectors fail. No country or regional overrides are currently supplied. The global soil erosion rule does not depend on income membership. Contextual rule sets and singular rule references cannot coexist on one T5 row.

```sh
python3 priority/context_rules.py generate
python3 priority/context_rules.py check
python3 priority/t5_refs.py
python3 -m unittest discover -s priority -p test_context_rules.py -v
```

The generator verifies fields, source references, domains, sample membership, fixed quantile reproduction and T5 linkage. Numeric boundaries are upper-inclusive. Manifest v2 adds a `category_map` JSON column for provider-category crosswalks; numeric rows use `{}`. Water stress uses native categories and the existing inspected binding's raw-value guards. Its preview requires raw value and category together, retaining original inputs and special states. Missing raw values take precedence over category flags. The generated bundle embeds the matched binding candidate, so any change to its decode contract makes the bundle stale. These previews are not spatial processing adapters. Source hashes identify reviewed bytes but do not claim fresh network retrieval on every check.

Pete approved the four [soil erosion classes](../research/2026-11-25-soil-erosion-global-classes.md), [water stress classes](../research/2026-11-25-water-stress-four-classes.md), [food insecurity classes with coverage limits](../research/2026-11-25-food-insecurity-classes.md) and [crop production gap classes with crop/spatial limits](../research/2026-11-25-production-gap-classes.md) on 25 November 2026. Their rationales record those approvals. Poverty cutoffs remain provisional. All nine rows retain the release-workflow state `proposed` and `runtime_ready=false`: that state concerns the complete source/binding/release package, not whether these interpretations were approved. The existing package route still needs an accepted release adapter. Historical profiles and proposals remain preserved and do not override this table.

Food insecurity uses `binding.validation=requires_local_assessment`, with no inspected binding candidate. Its complete integer category vocabulary is checked against the declared domain. `preview_documented_category` is a review helper: it returns unknown by default and requires explicit available/applicable coverage flags and matching classification units. Those flags are caller assertions, not dataset verification. Unknown, fractional, out-of-vocabulary and unavailable values cannot become Very little. This is not a complete global binding.

Crop production gap uses documentation-only thresholds: Very little 0–20%, Low >20–40%, Medium >40–60%, High >60–100%. Its catalogue URL is a discovery pointer, not a selected data asset. Scalar previews check a supplied percentage only; they do not derive yield gaps or verify crop eligibility, benchmark compatibility or spatial coverage. Livestock and mixed-system productivity need separate metrics.

Pete approved the [agricultural dependency approach and limitations](../research/2026-11-25-agricultural-dependency-classes.md) on 25 November 2026: local Low/Medium/High terciles with no None/Very little cutoff. `requires_local_data` records an uncalibrated tercile approach using the existing columns. Cutoffs, reference sample and category map must be empty; every scalar preview returns unknown. Local source, reference population, period, weighting and distinct observations must be checked before a separate calibrated rule is supplied. National ILO values remain qualified context, not local hotspot scores.

Pete approved the [gender inequity approach and limitations](../research/2026-11-25-gender-inequity-classes.md) on 25 November 2026: national GII Low/Medium/High terciles across one pooled global LIC/LMC/UMC reference set, equal weight per economy, no None/Very little cutoff. `requires_reference_calibration` preserves blank cutoffs and no reference sample; every preview stays unknown. Select one UNDP release and common year, pin income-group membership and eligible economies before calibration. National context only; local hotspot differentiation needs a separate subnational measure.

Next priority variable: [catchment water yield, interpretation review](../research/2026-11-25-catchment-water-yield-classes.md). Intervening T5 rows are descriptors, not priority classes.
