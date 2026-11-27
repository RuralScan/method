# Official IPC and ENSSAN acquisition audit

Read the [findings and class proposal](../2026-11-27-ipc-enssan-acquisition-and-classes.md). This folder contains research observations and a proposed crosswalk, not accepted method configuration.

- `acquisition.json`: original source/archive hashes, download route and boundary hash.
- `inspection.json`: unique-area reconciliation against the IPC Excel workbook, periods, native geometry limitations and ENSSAN extraction checks.
- `four_class_proposal.csv`: five native acute phases mapped to four proposed display classes. Status stays `proposed`; no runtime reader consumes this file.
- `enssan_geographic_prevalence.csv`: Table 41 transcription, 48 geography-year cells including two missing values. `join_status` identifies department-name candidates, custom boundaries and a population group. No spatial join is claimed.
- `enssan_national_prevalence.csv`: Table 39 comparator, not extra geographic observations.
- `manifest.json`: hashes of retained audit files.

## Replay

Extract the team archive named in `acquisition.json` into a new scratch folder. From the method repository root:

```sh
uv run --with shapely==2.1.2 --with pyproj==3.7.2 --with openpyxl==3.1.5 python priority/research/ipc-enssan-audit-20261127/analyze.py /absolute/path/to/extracted_sources /tmp/ipc-enssan-recheck.json
cmp priority/research/ipc-enssan-audit-20261127/inspection.json /tmp/ipc-enssan-recheck.json
```

The script checks original hashes, compares repeated area IDs before deduplication, matches native counts/phases/dates to Excel leaf rows, and reports invalid geometries without repairing them. Coverage is explicitly restricted to valid polygons; points are not buffered. It checks every Table 41 CSV cell against the preserved PDF extraction. The table was also inspected visually on PDF page 122. The extract is not a replacement for provider-issued weighted estimates and geography definitions.

For fresh IPC acquisition, open the [official analysis](https://map.ipcinfo.org/public/?anl_id=ht-2026-10-05&nofocus=y&period=C&table=true), wait for its analysis to load, and use **Download GeoJSON** and **Download Excel** in Details. Verify `analysis_id=87143457`, country HT, acute condition A, and feature-level ISO dates. Export timestamps change hashes on a later download; retain new bytes separately. Metadata listing two periods is not evidence that both occur in the features. No API access key or account was required for this public download.

ENSSAN original: [CNSA report](https://www.cnsahaiti.org/Web/Etudes/2025/Rapport%20ENSSAN%202025_vf.pdf), SHA256 `ad0157ddd13b0d527db844e2189b2da82e39102073071b40cc4db34e5d9be6e9`. Tables 1/39/41 were extracted with pdfplumber; the archive includes the exact raw cell grids and page renders used for checks. Table 1 has merged/overlapping text: its raw extraction is retained, but no clean stratum-label crosswalk is asserted. Figures were not converted into invented numeric tables.

## Attribution and conditions

**IPC, CC BY-NC-SA 3.0 IGO, analysis released 28-10-2026, accessed 27-11-2026**, [IPC source](https://www.ipcinfo.org/ipc-country-analysis/details-map/en/c/1165467/?iso3=HTI). Original IPC exports and derived IPC values in `inspection.json` retain [these conditions](https://www.ipcinfo.org/ipcinfo-website/privacy-policy/), rather than the repository code licence. Deduplication, diagnostics and the four-class display proposal are project modifications; no IPC endorsement is claimed.

**CNSA, ENSSAN 2025**, Tables 39 and 41, with page locators above. No blanket redistribution licence is asserted for the report. The public repository contains limited tabular research transcriptions and findings; the source PDF remains in the team library. Original source conditions continue to apply. No household microdata were obtained.

Team-mirror archive bytes were read back and verified; remote SharePoint access was not independently checked. No SRC/EV registration, accepted T1/BIND row, scientific approval or runtime readiness follows from acquisition alone.
