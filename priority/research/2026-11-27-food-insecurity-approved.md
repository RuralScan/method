# Approved acute food-insecurity classes

Decision date: 27 November 2026. Pete: “ok approved, capture those four food insecurity classes and limitations, retain the Phase 5 flag, then proceed to the next remaining dataset binding. Keep infrastructure in scope while we wait for Brayden.”

This approves the interpretation proposed in [the IPC/ENSSAN acquisition note](2026-11-27-ipc-enssan-acquisition-and-classes.md). The [approved crosswalk](food-insecurity-approval-20261127/classes.csv) records the decision separately from the frozen acquisition/proposal snapshot; historical records are not rewritten.

| Native IPC acute **area** phase | Approved display | Ordinal code | Mandatory flag |
|---|---|---:|---|
| 1 — Minimal | Very little | 0 | — |
| 2 — Stressed | Low | 1 | — |
| 3 — Crisis | Medium | 2 | — |
| 4 — Emergency | High | 3 | — |
| 5 — Famine | High | 3 | `critical_phase_5=true` |

Always retain the native phase and label. Display Medium with **Crisis** and High with its native Emergency/Famine label. The Phase 5 flag is mandatory alongside the four-class result, not discarded after classification. Preserve the source's separate `risk_of_famine`, assistance and confidence fields; risk of famine and household Phase 5 population are not equivalent to an area classified Phase 5. These are ordinal codes, not probabilities or percentages and not a new IPC standard.

Missing phase, insufficient evidence, unanalysed area, unavailable footprint or inapplicable period remains **Not assessed** with no score. Only an applicable published Phase 1 can yield Very little. Current and projected assessments remain separate. Global use means reuse of an applicable published acute assessment where available, not complete global coverage or extrapolation from Haiti.

## Retained limitations and adoption boundary

- The current Haiti source covers 1 September 2026–28 February 2027. It records 30 assessment areas after deduplicating 35 map representations. Duplicate representations must not multiply population. Two polygons fail validity checks; eight areas have only point geometry. Overlap and exact footprint handling remain unresolved; do not invent buffers or release complete area totals.
- Acute severity reflects current need, including conflict, prices, displacement and assistance. It does not quantify the component an NbS investment can remedy or replace longer-term chronic food insecurity.
- ENSSAN Table 41 is household severe-FIES prevalence, not an IPC phase. Keep its percentages as separate qualified context. The Ouest/metropolitan partition, camps, weights, uncertainty and sample-count discrepancy remain documented; the IPC crosswalk cannot classify those percentages.
- Retain IPC attribution and CC BY-NC-SA 3.0 IGO conditions. Approval of class meaning does not broaden source permissions.

The approval record pins the earlier proposal and source inspection. It does **not** assert an accepted T1/BIND adapter or runtime release. The existing contextual bundle's chronic IPC row remains a distinct, explicitly chronic configuration; it must not be fed acute phases. The approved acute crosswalk is now available for a deliberate source/context configuration once its adapter and geometry holds are resolved. This preserves both earlier chronic work and the new acute decision without silently changing units or accepting incomplete coverage.

Next technical binding check: [BII Haiti coverage and depletion conversion](2026-11-27-bii-haiti-binding.md). The combined Biodiversity score remains Not assessed until both BII and KBA inputs are valid. [Infrastructure](../infrastructure/README.md) remains active with national replacement needs; hazard selection awaits Brayden.
