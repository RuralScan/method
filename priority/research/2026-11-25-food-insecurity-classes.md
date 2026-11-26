# Food insecurity: published chronic levels for review

25 November 2026. Proposed interpretation for `food_insecurity`; not yet approved or bound to a downloaded area dataset.

Use an existing published **IPC Chronic Food Insecurity area classification**, where available and applicable. Its four levels map directly to the requested labels:

| Published IPC chronic level | RuralScan display class |
|---|---|
| 1 — Minimal (area classification) | Very little |
| 2 — Mild | Low |
| 3 — Moderate | Medium |
| 4 — Severe | High |

The [IPC reference table, Protocol 2.2](https://www.ipcinfo.org/ipc-manual-interactive/ipc-chronic-food-insecurity-protocols/function-2-classify-severity-and-identify-key-drivers/protocol-22-compare-evidence-against-the-ipc-chronic-food-insecurity-reference-table/en/) supplies these four severity levels. It combines evidence about food consumption quality and quantity, nutrition and contributing factors. RuralScan would reuse the published result, not run its own IPC classification or invent percentage thresholds. Renaming the labels is our display convention; preserve original IPC level and name.

Rationale for selecting the chronic measure: [IPC Protocol 2.3](https://www.ipcinfo.org/ipc-manual-interactive/ipc-chronic-food-insecurity-protocols/function-2-classify-severity-and-identify-key-drivers/protocol-23-adhere-to-analytical-parameters/en/) explicitly targets medium- and long-term programming and persistent food insecurity. That makes it a suitable candidate for this rural investment-scoping variable. Acute IPC phases describe a different condition and must not silently substitute for chronic levels. An area class is also not a percentage of food-insecure households or a household-level diagnosis. Minimal does not mean every household is food secure.

Coverage is the practical limitation. The [IPC chronic catalogue](https://www.ipcinfo.org/ipcinfo-website/ipc-overview-and-classification-system/ipc-chronic-food-insecurity-classification/en/) contains country-specific analyses with different validity periods; no continuous, current global dataset is established here. Each binding must identify the published analysis, area boundaries, assessment/validity period and exact level field. Preserve the native area support. Outside assessed coverage, missing, invalid and inapplicable historical records remain unknown, never Very little.

Where no suitable chronic analysis exists, retain the variable as unavailable until an appropriate local or alternative dataset and its own classification are specified. Do not treat national FIES prevalence, acute IPC phases, poverty or a rasterized national average as interchangeable observations. This is a source-backed classification proposal, not a completed global data binding. Reviewing these four labels does not require a new seasonal-fit analysis.
