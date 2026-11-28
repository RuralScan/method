# BII Haiti native-cell audit

Read [findings](../2026-11-27-bii-haiti-binding.md). The script reads the original 2020 raster, constructs native cell footprints, clips them to the pinned boundary, preserves nodata, and applies the previously approved depletion transformation/classes from local data files. Class areas are BII-only research diagnostics; combined biodiversity and runtime readiness remain held.

Original source: Trustees of the Natural History Museum, London (2024), BII v2.1.1 limited release, CC BY-NC-SA 4.0. [Catalogue](https://data.nhm.ac.uk/dataset/bii-developed-by-nhm-v2-1-1-limited-release). Derived source values and diagnostic summaries retain those conditions and attribution; they are not relicensed by the repository code licence. No endorsement or permission for every downstream use is asserted.

Original acquisition archive, already downloaded with Pete's approval:
`0_Methodology_&_Frameworks/priority_classification/bii_binding_2026_11_26/reviewed_sources.zip`

Archive SHA256: `57e742d788a8bfb0d6e28f7da2d8b2014df5f038691da2f25832d7f01ed7f2af`. Its `nhm_download.zip` contains the nested source package. Extract `bii-2020_v2-1-1.tif` into a scratch directory; the probe verifies its exact hash against `contract.json`. The acquired README confirms percentage units and five-arc-minute support. Remote team access has not been independently checked.

From the method repository root:

```sh
uv run --with rasterio==1.5.2 --with shapely==2.1.2 --with pyproj==3.7.2 python priority/research/bii-haiti-audit-20261127/probe.py /absolute/path/to/bii-2020_v2-1-1.tif /tmp/bii-haiti-recheck.json
cmp priority/research/bii-haiti-audit-20261127/inspection.json /tmp/bii-haiti-recheck.json
```

`inspection.json` retains native row/column, raw BII, depletion, class and clipped area for every intersecting cell. `contract.json` and `classes.csv` are bounded research configuration, not additions to the frozen runtime schema. `manifest.json` pins the files. Area accounting tolerance of 0.001 km² is numerical bookkeeping, not a minimum feature-area cutoff. The script includes equality/domain/missing-value checks and exact source/boundary hashes. No global raster is added to Git.
