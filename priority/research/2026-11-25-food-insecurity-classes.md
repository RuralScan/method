# Food insecurity: approved chronic-level interpretation

25 November 2026. Four-class interpretation and coverage limitations approved by Pete; not yet bound to a selected local area dataset.

Approval: “ok approved, capture those four food insecurity classes and the rationale, noting the coverage limitations, then proceed to the next variable”. This approves the displayed mapping and its conditional coverage, not a claim of current global data availability.

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

Where no suitable chronic analysis exists, retain the variable as unavailable until an appropriate local or alternative dataset and its own classification are specified. Do not treat national FIES prevalence, acute IPC phases, poverty or a rasterized national average as interchangeable observations. Reviewing these four labels does not require a new seasonal-fit analysis.

The approved mapping, rationale and limits now live in [rules.csv](../classifications/rules.csv), linked from T5. Binding status is explicitly `requires_local_assessment`: the catalogue URL is a discovery pointer, not an acquired dataset, and the exact field is pending selection. Review previews remain unknown unless coverage is explicitly available and applicable; they do not validate those assertions or create IPC assessments. Runtime release remains separate. Next proposal: [crop production gap](2026-11-25-production-gap-classes.md).

Source artefacts archived in the team-library mirror under `0_Methodology_&_Frameworks/priority_classification/food_insecurity_2026_11_25/classification_sources.zip`; SHA-256 `fac4d44954270906de1a2fce7c7b58513c64f083f74fb21892161645b9e005f1`. All members were read back byte-for-byte. Remote team access was not checked.

27 November binding follow-up: [Haiti national-source inspection](2026-11-27-food-insecurity-haiti-binding.md) acquired the October 2015 CNSA chronic bulletin. Its catalogue validity ends in October 2020; matching polygons and a current applicable assessment remain unverified. Keep current Haiti coverage Not assessed. Newer acute releases do not inherit this chronic mapping. Infrastructure remains in scope.
