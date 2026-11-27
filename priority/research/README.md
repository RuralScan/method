# Dataset research and Haiti inspections

Start with the [Brayden/Diego handover](2026-11-26-handover-brayden-diego.md) for current progress, holds and proposed next actions. These reports support technical review; successful access is not scientific acceptance or runtime readiness. [Nine core problems](../visual-scope.md) and [optional infrastructure exposure](../infrastructure/README.md) remain the scope.

| Research question | Current report | Reproducible observations |
|---|---|---|
| Official IPC polygons, ENSSAN geographic tables and four acute classes? | [Acquisition, proposal and limitations](2026-11-27-ipc-enssan-acquisition-and-classes.md) | [30-area reconciliation and geographic table audit](ipc-enssan-audit-20261127/README.md) |
| Aqueduct Haiti coverage and basin aggregation? | [Two-basin inspection and aggregation guidance](2026-11-27-aqueduct-haiti-coverage.md) | [Pinned vectors and offline probe](aqueduct-haiti-audit-20261127/README.md) |
| Newer national/global Haiti food-insecurity sources? | [Seven-source comparison and recommendation](2026-11-27-food-insecurity-alternatives-haiti.md) | [Acquisition hashes, FEWS geometry and WDI checks](food-alternatives-audit-20261127/README.md) |
| Current Haiti chronic food-insecurity binding? | [National source and remaining hold](2026-11-27-food-insecurity-haiti-binding.md) | [Inspection](food-binding-audit-20261127/inspection.json), [acquisition hashes](food-binding-audit-20261127/acquisition.json) |
| Carbon change beyond forests | [Soil, woody biomass and remaining pools](2026-11-26-carbon-loss-followup.md) | [Carbon audit](carbon-loss-audit-20261126/README.md) |
| Which RuralScan families match Naturebase? | [Crosswalk and completed sequence](2026-11-26-naturebase-nbs-crosswalk.md) | Exact family/source revisions recorded in report |
| Cropland agroforestry | [Haiti inspection](2026-11-26-naturebase-cropland-binding.md) | [Audit](naturebase-cropland-audit-20261126/README.md) |
| Savanna agroforestry | [Haiti inspection](2026-11-26-naturebase-savanna-binding.md) | [Audit](naturebase-savanna-audit-20261126/README.md) |
| Reforestation | [Haiti inspection](2026-11-26-naturebase-reforestation-binding.md) | [Audit](naturebase-reforestation-audit-20261126/README.md) |
| Coastal restoration / mangroves | [Haiti inspection](2026-11-26-naturebase-coastal-binding.md) | [Audit](naturebase-coastal-audit-20261126/README.md) |
| Peat restoration and management | [Haiti inspection](2026-11-26-naturebase-peat-bindings.md) | [Audit](naturebase-peat-audit-20261126/README.md) |
| Combined cropland soil-carbon pathway | [Haiti inspection](2026-11-26-naturebase-crop-soil-binding.md) | [Audit](naturebase-crop-soil-audit-20261126/README.md) |
| Separate no-till, inputs, joint and biochar scenarios | [Component comparison](2026-11-26-crop-soil-components.md) | [Audit](crop-soil-components-audit-20261126/README.md) |

[Shared Haiti diagnostic inputs](haiti-diagnostic-inputs-20261126/README.md) preserve exact point and boundary bytes. [Third-party notices](THIRD_PARTY_NOTICES.md) distinguish data conditions from code licences. Global rasters/ZIPs and browser screenshots remain outside Git. Earlier research notes remain available; historical proposals are not erased or silently promoted.

Run `python3 priority/research/verify_research.py` to check audit manifests, shared-input integrity, sample counts, saved scientific diagnostics and local report links without downloading data. Acquisition and probe commands in each audit README are separate network-dependent replays, not CI requirements.

Run `python3 priority/research/verify_haiti_bindings.py` for the three 27 November Aqueduct/food snapshots. Their audit READMEs give replay commands with pinned dependencies; food-source replays use archived original files.
