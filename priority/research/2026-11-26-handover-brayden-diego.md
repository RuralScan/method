# Dataset and carbon research handover — Brayden and Diego

Status at 26 November 2026. Prepared for review; this document does not assign work or record either colleague's agreement.

The World Bank-funded Rural Nature-based Solutions Scan is an early investment-scoping method. This work identifies usable datasets, checks what their values mean in Haiti, and records what must be resolved before an executable binding or classification is accepted. It does not establish site feasibility, measured project benefits or infrastructure protection.

## Progress across the workstream

| Area | Completed / agreed | Remaining decision or limitation |
|---|---|---|
| Scope and classification tables | Exactly nine visual-method problems; contextual rule extension recorded. Extra-variable work saved separately. Poverty grouping by World Bank income tier approved as an approach; soil erosion, water stress and chronic food insecurity class interpretations recorded | Poverty numerical cutoffs remain provisional. Interpretation approval is distinct from a complete accepted source/binding/release package; current rules are not runtime-ready |
| Climate hazards | Drought boundaries checked; river-flood depth proposal documented; hazard-versus-impact distinction retained | Brayden's indicator confirmation remains outstanding in the recorded alignment note. Confirm drought measure, flood hazard type/return period and heat indicator before adopting defaults |
| Biodiversity | BII 2020 acquired and inspected; approximately 10 km support accepted for interim coarse context. Maximum of BII depletion and KBA proximity approved, with 1.5/5 km KBA bands | KBA polygon access/inspection, explicit BII depletion transform and executable binding/release remain open |
| Erosion | Original cropland erosion raster extracted and checked. Alternative RUSLE and mEPM routes investigated; approved mEPM request submitted | Cropland-only coverage remains explicit. Option 2 lacks verified geographic metadata; mEPM provider approval and Haiti pixels remain pending. No alternative silently replaces the current source |
| Infrastructure | Provisional Haiti roads, schools, health facilities, power lines and buildings sources selected; national-source gaps documented | Acquire suitable CNIGS/MTPTC, MENFP, MSPP and EDH/operator inventories where available. Inventory coverage, operating status and deduplication need attention. No hazard exposure or protection benefit has been computed |
| Carbon loss | Soil-carbon and woody-biomass change candidates checked across 1,440 Haiti diagnostic locations in nine WorldCover classes | Pool/time alignment, change uncertainty and four-class rationale unresolved. Root and other missing pools are not zero. Naturebase mitigation potential cannot substitute for observed carbon loss |
| Naturebase comparison | Family-level crosswalk and initial pathway inspection sequence completed; originals/subsets, native decoding, Haiti support, administrative outputs and limitations retained | These are technically inspected research candidates, not scientifically accepted or executable bindings. Follow-up below identifies the specific blockers |

Sources of current status: [classification table](../classifications/README.md), [hazard alignment](2026-11-25-climate-hazard-alignment.md), [biodiversity](2026-11-26-biodiversity-loss-classes.md), [conservation](../conservation/README.md), [erosion alternatives](2026-11-26-erosion-options-haiti.md), [infrastructure](../infrastructure/README.md), [carbon findings](2026-11-26-carbon-loss-followup.md).

## Carbon / Naturebase results now available

| Candidate | Haiti result | Appropriate interim use / remaining hold |
|---|---|---|
| OpenLandMap soil-carbon change + CTrees woody biomass | Readable numerical support across multiple land-cover classes; scaling and period/pool meanings checked | Complementary context for the single carbon concern. No total ecosystem-carbon loss classes, root-complete accounting or aggregation rule adopted |
| Cropland agroforestry | Positive Haiti support, but sparse | Matching-family mitigation comparator only; eligible-area denominator and local transfer still unresolved |
| Savanna agroforestry | Checked Haiti raster values zero; administrative results `NA` | Hold quantitative Haiti use. This does not demonstrate that silvopasture is infeasible or has no benefits |
| Reforestation | Positive Haiti potential; documented above- and belowground biomass basis | Natural-regrowth comparator. Soil-carbon pool listing remains unsubstantiated; area fractions, administrative reconciliation and local eligibility remain open |
| Coastal restoration | Positive Haiti potential; combined mangrove/tidal-marsh output | Keep combined context. Mangrove split unavailable; embedded area field unusable. Separate mangrove national-table lead acquired, but spatial component validation remains |
| Peat restoration and management | Both checked Haiti pathway rasters zero and tables `NA`; independent peat sources intersect Haiti | Zero opportunity output is not absence of peat. Drainage source has no valid Haiti cells; verify substrate, drainage and eligible area before quantitative use |
| Combined cropland soil-carbon pathway | Positive Naturebase Haiti values | Cannot assign bundled tillage/input/biochar benefit to mulching, conservation tillage or water harvesting alone |
| Separate soil scenarios | All three Soils Revealed originals acquired; publisher MD5 checks passed. Same 80,187 positive Haiti cells, but only 49/160 diagnostic cropland sample locations readable | Approximately 250 m, 0–30 cm, modelled stock change over 20 years. Joint scenario exceeds separate gains summed by 6.08–10.65%; use it directly for a matching combined practice. Local baseline and source-mask mismatch remain material |
| Biochar | Separate technical and constrained rasters acquired; positive Haiti support | Coarse residue-resource context. Units are Mg C/year/pixel, not per hectare; 100 years describes persistence. Residues compete with soil cover/feed uses. No independent-maxima summation or reconciliation with the Naturebase bundle established |

The [research index](README.md) links each report and its compact audit. Statistics are diagnostic model outputs, not field validation or national area-weighted treatment effects. Missing values remain unknown.

## Proposed follow-up for discussion

**Brayden — climate hazards and infrastructure:** confirm the intended physical hazard indicators, flood hazard type and return period, and heat measure. Then identify which hazard footprints support the optional infrastructure exposure overlay. Keep livelihood exposure separate from risk to the NbS investment; overlap with a hazard does not estimate damage avoided or protection benefits. Recorded Teams request remains pending; no new message is sent by this handover.

**Diego — data/runtime integration review, if this is the agreed team allocation:** use the inspected files, masks, scale factors, units and hashes to assess adapter effort. Preserve native support and source dates; derive scale-dependent quantities before aggregation; distinguish unknown coverage from valid zero. Resolve global/national source selection through existing T1/BIND/T7 context fields, with visible fallback provenance. Take only explicitly reviewed packages through scientific acceptance and release; this PR does not activate those bindings.

**Shared scientific decisions:** choose the defensible carbon-loss interpretation before calibrating classes; reconcile pool/time scope and change uncertainty. For mitigation comparisons, resolve pathway fractions and component overlap before multiplying by implementation hectares or combining benefits. Prioritise Haitian cropland management/residue baselines, peat drainage and coastal restoration geometry where these control applicability.

## Handover package and housekeeping

This PR packages the carbon/Naturebase follow-up reports, eight compact audit directories, shared exact Haiti boundary/sample inputs, source-specific notices and current crosslinks. Earlier classification, biodiversity, erosion and infrastructure decisions are linked as context; they are not newly approved here.

Global binaries, incomplete duplicate transfers and browser screenshots remain outside Git. Audit manifests retain source hashes and acquisition distinctions: full archives versus selected members, originals versus native Haiti subsets, and successful reads versus failed hosted routes. No accepted T1/BIND, T3/T4/T6 rule or runtime release is changed.

Offline verification: run `python3 priority/research/verify_research.py`. Reported repository/CI validation is included in the PR description. Replaying remote probes requires their documented dependencies and source access; use a scratch directory to preserve the inspected record.
