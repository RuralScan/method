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

Pete approved the four [soil erosion classes](../research/2026-11-25-soil-erosion-global-classes.md), [water stress classes](../research/2026-11-25-water-stress-four-classes.md) and [food insecurity classes with coverage limits](../research/2026-11-25-food-insecurity-classes.md) on 25 November 2026. Their rationales record those approvals. Poverty cutoffs remain provisional. All six rows retain the release-workflow state `proposed` and `runtime_ready=false`: that state concerns the complete source/binding/release package, not whether these interpretations were approved. The existing package route still needs an accepted release adapter. Historical profiles and proposals remain preserved and do not override this table.

Food insecurity uses `binding.validation=requires_local_assessment`, with no inspected binding candidate. Its complete integer category vocabulary is checked against the declared domain. `preview_documented_category` is a review helper: it returns unknown by default and requires explicit available/applicable coverage flags and matching classification units. Those flags are caller assertions, not dataset verification. Unknown, fractional, out-of-vocabulary and unavailable values cannot become Very little. This is not a complete global binding.

Next variable: [crop production gap, four-class proposal](../research/2026-11-25-production-gap-classes.md). The published crop-yield bands do not automatically apply to livestock or mixed-system productivity.
