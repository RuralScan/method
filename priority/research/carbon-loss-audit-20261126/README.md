# Carbon candidate inspection audit — 26 November 2026

Read the [findings and binding status](../2026-11-26-carbon-loss-followup.md).

This directory preserves technical observations, not accepted classifications. No source data beyond small point/window samples are included. `observations.json` has 1,440 unique locations, the 2021 land-cover label, and raw values from five native-grid image reads. `soil_uncertainty_all.json` has six native raster reads at 20 deliberately spatially spread points. `summary.json` retains descriptive calculations, including quantities deliberately not interpreted as significance tests.

`*_metadata.json` and `probe_index.json` pin inspected GEE asset identities and properties. `manifest.json` hashes retained files and identifies the original boundary snapshot by checksum. The original boundary and verbose raw response files remain in the task's private research directory; the compact observations preserve every sampled location and raw band value needed for the reported calculations.

Offline integrity and arithmetic check:

```sh
python3 priority/research/carbon-loss-audit-20261126/verify_audit.py
```

Reproduce remote observations **in a copy of this directory**, preserving the audited files:

```sh
uv run --with earthengine-api python probe_haiti.py
uv run --with rasterio python probe_soil_uncertainty.py
python summarize.py
python build_observations.py
```

Earth Engine initialization uses an already authorized local configuration. No credentials are included. The probe reuses recorded coordinates if `observations.json` exists; otherwise it generates the seeded, land-cover-stratified sample. Neither script exports global imagery or creates remote assets. The soil probe uses three concurrent native HTTP range readers. Source rasters are externally hosted and may change: compare new metadata and samples with the preserved audit rather than replacing the records silently.

Important limitations:

- A numerical value is access/coverage evidence, not ecological validity or measured carbon loss.
- Class allocation is equal, not area-weighted. Do not aggregate class percentages into a national estimate.
- Native carbon cells can include other cover types; 2021 labels do not establish historical land use.
- SOC period estimates and annual AGB images have different time support.
- Marginal uncertainty ranges do not supply cross-time covariance or calibrated change intervals.
- Research scripts contain explicit inspection parameters and arithmetic; they are not runtime analytical rules and are not imported by the pipeline.

Housekeeping update: exact point and boundary inputs are now included in [the shared diagnostic input archive](../haiti-diagnostic-inputs-20261126/README.md). Original input hashes are unchanged. Use those files in the scratch layout described above; laptop-only input access is no longer required. [Third-party terms](../THIRD_PARTY_NOTICES.md) remain attached to retained source-derived values.
