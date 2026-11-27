# Aqueduct Haiti inspection

Source: World Resources Institute, Aqueduct 4.0 annual baseline, GEE asset `WRI/Aqueduct_Water_Risk/V4/baseline_annual`. Retrieved 27 November 2026; asset update timestamp is preserved in `metadata.json`. Attribution and conditions: [GEE catalogue](https://developers.google.com/earth-engine/datasets/catalog/WRI_Aqueduct_Water_Risk_V4_baseline_annual) permits use/distribution with WRI attribution requested. This bounded field/feature selection and derived diagnostics are our modifications, not a WRI-certified product.

`haiti_intersecting_native.geojson.gz` losslessly preserves full native geometries and selected native fields for all 54 upstream spatial-query candidates. Gzip keeps the 52,505-line coordinate snapshot out of the textual review diff. `analyze.py` performs exact local clipping, validity checks, basin consistency checks, union-area accounting and classification through the existing table reader. Its `1e-3 km²` assertion tolerance concerns numerical bookkeeping only; it is not a minimum feature size or analytical cutoff.

From the method repository root:

```sh
uv run --with shapely==2.1.2 --with pyproj==3.7.2 python priority/research/aqueduct-haiti-audit-20261127/analyze.py /tmp/aqueduct-haiti-recheck.json
cmp priority/research/aqueduct-haiti-audit-20261127/inspection.json /tmp/aqueduct-haiti-recheck.json
```

The checked-in boundary lives in `../haiti-diagnostic-inputs-20261126/boundary.json`. `inspection.json` pins its hash, the uncompressed subset bytes and both existing classification/binding CSV inputs. `manifest.json` pins the retained files, including the compressed subset. No accepted rule or binding is generated.

For a fresh network acquisition, copy `acquire.py` into a **new scratch directory**, then run it with an absolute path to the pinned boundary and an authenticated Earth Engine environment (`uv run --with earthengine-api python /path/to/scratch/acquire.py /absolute/path/to/boundary.json`). It writes uncompressed GeoJSON adjacent to itself; do not run against the frozen audit folder. Credentials are not stored. Asset updates or serialization changes may change bytes: retain new output separately and compare native values/geometries before revising this snapshot.

See [interpretation and aggregation](../2026-11-27-aqueduct-haiti-coverage.md). These are country-boundary diagnostics, not opportunity-space or infrastructure-exposure results.
