# Shared Haiti diagnostic inputs — 26 November 2026

Exact boundary and point inputs used in the linked carbon/Naturebase audits. `manifest.json` pins original bytes; no coordinates or geometry were changed during publication.

- `boundary.json`: Earth Engine `USDOS/LSIB_SIMPLE/2017`, filtered to Haiti. International fallback, not a country-endorsed boundary or marine jurisdiction. [Provider and public-domain terms](https://developers.google.com/earth-engine/datasets/catalog/USDOS_LSIB_SIMPLE_2017).
- `stratified_points.geojson`: 1,440 diagnostic locations, 160 per each of nine WorldCover 2021 classes; sampling at 100 m in UTM 18N. These are generated sample locations, not household, farm or survey records. Equal stratum allocation is not a national area-weighted sample. Derived from ESA WorldCover 2021 v200, CC BY 4.0; [source and attribution](https://developers.google.com/earth-engine/datasets/catalog/ESA_WorldCover_v200).

Native source rasters were sampled without interpreting missing values as zero. Cell-centre inclusion is the default country convention; coastal all-touched results are labelled sensitivity checks. Pass these two files to the probe scripts. For the soil-component scripts, copy this directory beside the scratch audit directory, preserving its name. For the original carbon-loss scripts, copy the input files into their scratch directory before running them. Run probes in scratch directories to preserve recorded audit bytes.
