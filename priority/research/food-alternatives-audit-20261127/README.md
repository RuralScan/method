# Newer Haiti food-source audit

See [comparison and recommendation](../2026-11-27-food-insecurity-alternatives-haiti.md). These records check access, dates, grain and geometry; they do not approve replacements for chronic IPC classes.

`acquisition.json` pins downloaded originals, exact source URLs and the team-library archive. `inspection.json` records native FEWS scenario properties, coverage and overlap, plus the latest non-null WDI observation and its metadata. `manifest.json` pins repository audit files. ENSSAN page/figure locators and methodological limits are in the comparison note. Large source files remain outside Git; no household microdata were acquired.

Reproduce from the method repository root after extracting the team archive into a new scratch folder:

```sh
uv run --with shapely==2.1.2 --with pyproj==3.7.2 python priority/research/food-alternatives-audit-20261127/analyze.py /absolute/path/to/extracted_sources /tmp/food-alternatives-recheck.json
cmp priority/research/food-alternatives-audit-20261127/inspection.json /tmp/food-alternatives-recheck.json
```

The probe requires exact original bytes and the shared pinned Haiti boundary; it fails on hash drift. Coverage uses clipped geometry unions separately for each scenario. It reports cross-phase overlaps without silently removing them, and does not produce class-area totals or a runtime raster. The `1e-3 km²` accounting tolerance is numerical, not an analytical cutoff. Forecasts remain distinct from the current-situation assessment.

Sources and conditions:

- **Famine Early Warning Systems Network (FEWS NET), Haiti October 2026 acute food-insecurity classifications**, downloaded from the [Data Warehouse](https://fdw.fews.net/api/ipcphasemap/country/HT/2026-10-01.geojson); interpretation accompanies the [October outlook](https://fews.net/latin-america-and-caribbean/haiti/food-security-outlook/october-2026). The same endpoint pattern was found in the official June 2026 download page; October reporting dates were verified in the response. Follow the [use and attribution policy](https://help.fews.net/fdp/data-and-information-use-and-attribution-policy): retain source acknowledgement in onward sharing, do not imply endorsement, and respect any third-party restrictions. API accessibility alone is not a blanket licence for every upstream input.
- **Coordination Nationale de la Sécurité Alimentaire (CNSA), ENSSAN 2025**, original PDF retained for team research with its source URL; no new redistribution licence asserted. Public Git contains our short review, not the report or household data.
- **FAO via World Bank World Development Indicators**, `SN.ITK.MSFI.ZS`, downloaded national observations and metadata; the [indicator page](https://data.worldbank.org/indicator/SN.ITK.MSFI.ZS?locations=HT) identifies CC BY 4.0. Retain FAO/WDI attribution. Catalogue metadata and other snapshots retain their original source conditions.

The team OneDrive mirror was read back and hashed. Remote SharePoint availability was not independently verified. No SRC/EV or accepted T1/BIND row is created by archiving these research inputs.
