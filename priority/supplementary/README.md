# Saved supplementary work

Pete restricted the active classification review to the nine visual-method problems on 25 November 2026. These records remain saved, with their previous approvals and limitations intact. They do not expand the core menu. No historical evidence or T5 ID is deleted.

| Saved work | Decision retained |
|---|---|
| [Crop production gap](2026-11-25-production-gap-classes.md) | Approved four crop-only bands; spatial binding pending |
| [Agricultural dependency](2026-11-25-agricultural-dependency-classes.md) | Approved local terciles; local data required; no None cutoff |
| [Gender inequity](2026-11-25-gender-inequity-classes.md) | Approved national-context terciles; calibration pending; no None cutoff |
| [Catchment water yield](2026-11-25-catchment-water-yield-classes.md) | Interpretation proposal only; no classification or role change approved |

The three approved approaches reside in `priority/classifications/supplementary_rules.csv`; generated JSON keeps them under `supplementary_rules`. Default review selection excludes them. Their T5 references point explicitly to the supplementary file. Shared source and country registries remain shared to avoid duplicate provenance.


Crop production gap uses documentation-only thresholds: Very little 0–20%, Low >20–40%, Medium >40–60%, High >60–100%. Its catalogue URL is a discovery pointer, not a selected data asset. Scalar previews check a supplied percentage only; they do not derive yield gaps or verify crop eligibility, benchmark compatibility or spatial coverage. Livestock and mixed-system productivity need separate metrics.

Pete approved the [agricultural dependency approach and limitations](2026-11-25-agricultural-dependency-classes.md) on 25 November 2026: local Low/Medium/High terciles with no None/Very little cutoff. `requires_local_data` records an uncalibrated tercile approach using the existing columns. Cutoffs, reference sample and category map must be empty; every scalar preview returns unknown. Local source, reference population, period, weighting and distinct observations must be checked before a separate calibrated rule is supplied. National ILO values remain qualified context, not local hotspot scores.

Pete approved the [gender inequity approach and limitations](2026-11-25-gender-inequity-classes.md) on 25 November 2026: national GII Low/Medium/High terciles across one pooled global LIC/LMC/UMC reference set, equal weight per economy, no None/Very little cutoff. `requires_reference_calibration` preserves blank cutoffs and no reference sample; every preview stays unknown. Select one UNDP release and common year, pin income-group membership and eligible economies before calibration. National context only; local hotspot differentiation needs a separate subnational measure.

Previously proposed next variable (now outside core scope): [catchment water yield, interpretation review](2026-11-25-catchment-water-yield-classes.md). Intervening T5 rows are descriptors, not priority classes.
