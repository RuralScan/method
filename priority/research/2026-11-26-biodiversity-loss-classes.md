# Biodiversity loss: approved four-class interpretation; binding pending

26 November 2026. Pete requested biodiversity review while climate-hazard confirmation is pending, retaining infrastructure. Following presentation of this four-class proposal and its limitations, Pete replied “ok next?”. This records acceptance of the displayed interpretation. A current dataset binding and runtime release remain pending; that response does not verify a raster or approve a new dataset edition.

## Measure and proposed classes

Use the abundance-based Biodiversity Intactness Index (BII) to represent **biodiversity depletion relative to a minimally disturbed reference**. The [Natural History Museum explanation](https://www.nhm.ac.uk/our-science/services/data/biodiversity-intactness-index.html), sections “About the Biodiversity Intactness Index” and “How does the Biodiversity Intactness Index work?”, describes a model combining abundance and compositional similarity. A single BII map describes condition relative to that reference; it does not measure recent annual loss, the percentage of species extinct, or species richness alone.

The approved BII input describes “Modelled depletion relative to an undisturbed reference”. Greater depletion means greater concern for this input. Pete subsequently requested one [Biodiversity priority layer combining BII and KBA proximity](../conservation/README.md); that combined presentation replaces the loss-only menu label while retaining these BII classes unchanged.

| RuralScan display | BII remaining (%) | Depletion score, 100 − BII |
|---|---:|---:|
| None / very little — display as **Very little** | 90–100 | 0–10 |
| Low | 80 to below 90 | Above 10 to 20 |
| Medium | 60 to below 80 | Above 20 to 40 |
| High | Below 60 | Above 40 |

These intervals describe a valid percentage-scale input within 0–100. Exact equality assignments are explicit RuralScan conventions: BII 90 → Very little, 80 → Low, 60 → Medium. In depletion units, 10/20/40 are upper-inclusive, compatible with the contextual table's existing numeric convention. No new endpoint convention or schema extension is needed; a reviewed rule row and verified binding are still required. Missing remains unknown; do not silently clip unexpected values, infer validity from colour, or turn uncovered cells into Very little.

## Published basis and strength of rationale

[UNEP (2021), *GEO-6 for Youth*, printed page 22, Figure 1.5](https://www.unccd.int/sites/default/files/library/1677_G4Y.pdf#page=46), reproduces a **global** BII map attributed to Newbold et al. (2016). Its legend has five bands: below 60%, 60–80%, 80–90%, 90–95%, and above 95%. The proposed crosswalk preserves the first three bands and combines the two most-intact bands. Four concern labels and endpoint equality are RuralScan choices; UNEP does not publish these four loss-severity labels.

NHM identifies 90% as a proposed planetary-boundary reference. That provides a rationale for distinguishing comparatively intact areas, but does not establish a universally safe pixel-level cutoff or literal absence of loss. The 60% and 80% breaks are published **map-display bands**, not demonstrated universal ecological tipping points. This is a transparent published-band convention for scoping, not a claim that all three boundaries have equivalent ecological validation. The global legend avoids calibrating classes from a UK or US distribution.

Alternative screened: *State of Nature 2016*, printed pages 70–71, Figure 46, also displays BII, but uses more bands in a UK view. Its global-model explanation is useful background; it is not the selected classification legend. Equal-width or income-group terciles have not been calculated or substituted.

## Scope and binding limitations

- This measures terrestrial biodiversity condition. It is not a marine or freshwater biodiversity assessment, a threat forecast, or a direct estimate of ecosystem-service loss.
- A low depletion class can contain highly valuable intact habitat. It must not imply low conservation importance or permission to convert that habitat. KBA proximity and protected-area constraints retain their separate meanings. The subsequent combined-priority proposal combines ordinal decision classes, not raw BII with binary designation as if they measured the same quantity.
- BII is modelled from biodiversity observations and mapped pressures. Inspect uncertainty and local ecological relevance; maps are screening evidence, not site surveys or predictions of recovery from a particular NbS.
- The legacy `bii_nhm_global` pointer references the 2016 publication. Its circa-2005 layer must not be labelled current-year loss. *State of Nature 2016*, page 71, explicitly describes the 2005 pressure inputs. Prefer an appropriate newer edition if available and compatible, after confirming its reference state, native resolution, units, valid domain, masks, coverage and access conditions. Do not subtract different model editions to invent a trend.
- The global class convention does not require World Bank income groups. Country/biome adjustments remain possible where better local evidence supports them; record and justify any override.

No current raster has been sampled or selected in this review. Existing profile and T5 routing remain held; interpretation approval does not turn an old dataset pointer into an inspected binding. Once the input is selected and its transformation verified, the contextual row can record `method=thresholds`, depletion units, `direction=higher_is_more_concern`, cutoffs 10/20/40, the exact BII-to-depletion transformation, source/version, rationale and limitations. The table's binding currently permits positive scale only, so do not encode `100 − BII` as a silently accepted negative scale or invent a derived input asset. No core rule is activated by this approval record.

Climate hazards remain pending Brayden's reply. The Bank's [infrastructure exposure work](../infrastructure/README.md) stays active alongside the nine problems; this biodiversity proposal does not change that scope or add another problem variable.

## Source preservation

The global legend was visually checked on the original PDF (PDF page 46; printed page 22). Source bytes and locators are in the team-library mirror: `0_Methodology_&_Frameworks/priority_classification/biodiversity_loss_2026_11_26/reviewed_sources.zip`, SHA-256 `f4749c9ac11afc4a5539a912b8b17c754b6517e18992e3cb707061ad5585b8bc`.

| Member | SHA-256 |
|---|---|
| `geo4youth.pdf` | `ccfd8b38ddfc9b1df0e243d5fdb6eac9d381a68862f4dc4b61a73b6ef7b42bd3` |
| `nhm_bii.html` | `9baa9cc37626bd66ba67be981a4d97a370d9ff50d7686fc546107a9cea3ac0a6` |
| `state-of-nature-2016.pdf` | `b80b567977950229623a72f95126531509ac64dd2e06681c8475b8cb3494e510` |

Archive members were read back and verified. Remote SharePoint access was not checked. This is technical proposal provenance, not formal SRC/EV registration or scientific acceptance. Historical profiles and approvals are preserved.


## Next binding inspection: NHM v2.1.1 limited release

26 November 2026 follow-up after selecting provisional Haiti infrastructure sources. The [producer catalogue](https://data.nhm.ac.uk/dataset/bii-developed-by-nhm-v2-1-1-limited-release), resource [c4c281c4-befa-4e1b-a162-ba2f25e5ae82](https://data.nhm.ac.uk/dataset/bii-developed-by-nhm-v2-1-1-limited-release/resource/c4c281c4-befa-4e1b-a162-ba2f25e5ae82), identifies **v2.1.1 (Open Access, Limited Release)**, updated 9 October 2024, as a newer candidate than the legacy Newbold 2016 pointer. The resource catalogue reports a ZIP of 45,890,222 bytes. Catalogue temporal extent is 2000–2020, but this is explicitly a temporally limited release: it does not establish which years are in the ZIP. The producer directs requests for the complete annual series, finer resolution and commercial use to its Biodiversity Futures Lab.

The advertised licence is **CC-BY-NC-SA 4.0**. It must not inherit the old T1 entry's CC-BY-4.0 label. Catalogue access succeeded in the browser after initial command-line requests returned HTTP 403. The download panel offers a no-notification option; this was selected, with no email/personal details entered. **Start was not submitted:** the producer states that downloading records agreement to the terms. Exact download approval is still needed under the browser's action-time agreement rule. No contact message was sent.

This advances source identity and acquisition-route inspection, not raster verification. File contents, native resolution, actual year selection, units, valid range, mask and Haiti coverage remain unverified. The separate NHM explanatory page illustrates a 2020 map at 0.25 degrees; that caption is not evidence of the ZIP's native grid. No raster bytes/hash or class results are claimed. Do not activate the old pointer merely because the newer candidate is awaiting acquisition, and do not apply the approved percentage bands to unknown units. After acquisition, verify these properties and the explicit BII-to-depletion transform before proposing an executable binding. The approved maximum-with-KBA rule and nine-variable scope remain unchanged.
