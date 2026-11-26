# Soil erosion: published global bands

25 November 2026. Four-class interpretation approved by Pete in this chat; dataset verification and runtime release remain separate.

Approval: “ok approved, keep those four soil erosion classes and capture the rationale, then proceed to the next variable”. This follows the displayed 0–1 / >1–3 / >3–5 / >5 tonnes/ha/year mapping and the explanation of the source bands. It approves these class definitions, not an uninspected raster or a runtime release.

Use modelled annual soil loss by water, in tonnes/ha/year. [Borrelli et al. (2017), Figure 1a and Results, “Global perspective on soil erosion”](https://www.nature.com/articles/s41467-017-02142-7) apply seven bands globally: 0–1, 1–3, 3–5, 5–10, 10–20, 20–50 and >50. The first three correspond to very low, low and moderate erosion. RuralScan retains those boundaries and combines the four higher bands.

| Display class | Soil loss (tonnes/ha/year) |
|---|---:|
| Very little | 0–1 |
| Low | >1–3 |
| Medium | >3–5 |
| High | >5 |

Upper-inclusive endpoints and the four-class collapse are explicit RuralScan conventions. The internal `none` score code displays **Very little**, not zero erosion or a soil-specific safe-loss guarantee. Missing, negative and nonfinite values remain unknown. The measure is modelled water erosion, not all erosion processes or an estimated NbS benefit.

This replaces the earlier European 1/2/10 transfer proposal. Its basis is a published global application, not a newly inferred global tolerance standard. The figure was visually inspected alongside the article text.

Rationale: retain the source's first three bands, rename very low to Very little and moderate to Medium, and combine its high and higher bands into High. The article labels 5–10 as high and separately uses 10 tonnes/ha/year as a generic tolerable-erosion benchmark. Therefore 5 is the published start of the high class, not a claim that every soil tolerates losses up to 5 or 10. The bands originate in the European Soil Bureau classification, which this paper applies globally; global application is not universal validation of safe-loss limits. This preserves a published basis while providing the four classes requested for scoping.

Candidate dataset: [JRC GloSEM, 2012 output](https://esdac.jrc.ec.europa.eu/content/global-soil-erosion). The distributed global raster is resampled to **25 km**; original 250 m model resolution must not be claimed for that file. Newer 100 m cropland coverage must not be silently treated as a forest/rangeland layer. No raster was acquired or field-verified in this classification pass: binding status is `documentation_only`. Resolution and coverage remain application constraints, not prerequisites for reviewing class definitions.

The rule and approval rationale are captured in [rules.csv](../classifications/rules.csv), linked from the single T5 soil erosion row. Source locators and snapshot hashes are in [sources.csv](../classifications/sources.csv). Source registration and the protected runtime-release decision remain outstanding; this does not negate Pete's approval of the four-class interpretation.

Reviewed article, catalogue and figure snapshots are archived in the team-library mirror under `0_Methodology_&_Frameworks/priority_classification/soil_erosion_2026_11_25/reviewed_web_sources.zip`. All three members were verified byte-for-byte after writing. Archive SHA-256: `8796ab582cf57c2da06953bab8941278f2872f4ea1f4cac51c48bec437d437e3`. Remote team access has not been independently checked.
