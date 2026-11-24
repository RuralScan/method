# CRITIC assessment for T2/T5 priority weighting

**Conclusion:** keep explicit user weights as the default. Offer CRITIC as a diagnostic comparison only. It does not settle semantic duplication, scientific calibration or the intended policy priorities. These are controlled calculations, not pilot validation.

## Method and published check

CRITIC measures each criterion’s variation and its conflict with the others. With consistently oriented, min–max scaled criteria, `C_j = sd_j × sum_k(1 − r_jk)` and `w_j = C_j / sum(C)`. The implementation reproduces the original eight-alternative, three-criterion example: profitability **0.202**, market share **0.481**, productivity **0.317**, within **0.001** of the reported weights. Population rather than sample standard deviations cancel under the common sample size.

Source: Diakoulaki, Mavrotas and Papayannakis (1995), [Determining objective weights in multiple criteria problems: The CRITIC method](https://doi.org/10.1016/0305-0548(94)00059-H), equations 2–6 and Tables 2–3; [original paper copy](https://reformship.github.io/pages/1capacity/1model/11evaluation/Determining%20objective%20weights%20in%20multiple%20criteria%20problems%20The%20CRITIC%20method.pdf).

## Controlled tests

The synthetic raw columns are `a=[0,1,2,3,4,5]`, `b=[0,1,2,3,4,50]`, `c=[1,0,1,0,1,0]`. All are oriented with increasing concern. The illustrative classification is 0 at zero, 0.33 through 2, 0.66 through 4, then 1. It is not a real indicator calibration.

| Test | Weight a | Weight b | Weight c | Result |
|---|---:|---:|---:|---|
| Raw, min–max | 0.2137 | 0.2461 | 0.5403 | Baseline diagnostic |
| First four locations only | 0.2135 | 0.2135 | 0.5729 | Area/reference sample changes weights |
| Classified, fixed 0–1 scale | 0.3294 | 0.3294 | 0.3412 | Discretisation changes variation and correlation |
| Classified, then min–max | 0.1946 | 0.1946 | 0.6108 | Rescaling class scores changes meaning again |
| Add exact copy of a | 0.1415 | 0.1904 | 0.5267 | Copy gets another 0.1415; block total 0.2830 |
| Add constant column | 0.2137 | 0.2461 | 0.5403 | Constant omitted from correlation, assigned zero |

An opposing pair receives 0.5/0.5. Identical nonconstant criteria yield no identifiable weights; the implementation reports this instead of inventing equal weights. Complete-case sampling is explicit, with excluded observations and sample size reported. All-constant inputs also have no identifiable weights.

## Implications for the method

- CRITIC is not invariant to adding a duplicate in general. Shared concern IDs and explicit representative selection are still needed. High correlation can also occur between genuinely distinct policy concerns.
- Variation and conflict describe the chosen data sample, not stakeholder importance. Area, period, missingness, scaling and class boundaries can change the result.
- A constant concern may still deserve a user weight even though it cannot distinguish locations. Its diagnostic CRITIC weight is not a rule to erase it from the user’s priorities.
- Problem classes are ordinal conventions. The user-weighted mean is an explicit compensatory scoring rule, not a prediction of benefit or a measured cardinal utility. Sensitivity to those conventions needs inspection.
- Keep one representative per shared concern. Inspect remaining correlations; explain retained correlated concerns and test alternatives. No silent hybrid AHP/entropy/CRITIC correction.

## Reproduce and limits

In the companion RuralScan/runtime change, run:

```sh
uv run pytest -q tests/test_priority.py
uv run python scripts/assess_critic.py
uv run python -m nbs_runtime.priority config/priority/illustration.json --output /tmp/priority-example.json
```

`tests/test_priority.py` contains the published-example regression. `scripts/assess_critic.py` produces all diagnostic matrices and weights above. The illustration gives scores **0.8325** and **0.745**, leaves incomplete cells unknown and excludes cells outside the opportunity mask. Exact source revisions are recorded in the corresponding PRs and runtime’s packaged method pin.

This supports an implementation decision, not the scientific calibration of any real variable. Before a pilot, provide reviewed cutoffs or a justified reference population, align the datasets, check geographic support and missingness, and compare rankings under alternative user weights and retained representatives. The existing T4 notebook is unchanged.
