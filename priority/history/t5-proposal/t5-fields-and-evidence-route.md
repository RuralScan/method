# T5 classification fields and cross-cutting evidence route

Status: proposed extension, 25 November 2026. This specification precedes the bounded literature review. It builds on merged method PR #100 and evidence PR #99; their scientific proposals remain unaccepted. Schema tracking: [issue #103](https://github.com/RuralScan/method/issues/103).

## T5 additions and storage

Add the following logical fields through a one-to-one CSV extension, `priority/T5_classification_refs.csv`. Its key is the existing `T5.variable_id`. Preserve the historical T5 CSV, its 19 IDs, four descriptor roles and all review history. The extension has a separate frozen manifest, `priority/t5-structure.json`; it does not silently widen the compiler configuration release. A future accepted T5 view joins the historical presentation fields to this extension. It must not inherit historical normalization or default weights.

| Field | Type and rule | Storage purpose |
|---|---|---|
| `variable_id` | Existing unique T5 ID; exactly one row per historical ID | Stable crosswalk |
| `mcda_role` | `priority` or `descriptor`; preserve historical role until an explicit decision | Eligibility, not a weight |
| `concern_id` | Stable proposed shared concern ID | Prevent aliases entering the same run twice; shared concern does not imply equivalent quantities |
| `profile_ref` | Versioned JSON path, required | Quantity, units, time/space/context and dataset-binding audit, including unresolved choices |
| `proposed_rule_ref` | Versioned proposal path or empty | Review candidate only; never an execution default |
| `accepted_rule_ref` | Empty until an immutable accepted release reference exists | Exact `{repository,revision,path,sha256,classification_id,version}` in an accepted profile/release, not a mutable branch |
| `classification_status` | `held` or `descriptor` for this batch | Author assessment; human disposition is separately derived from decisions |

The profile stores `quantity`, `unit`, `temporal_statistic`, `spatial_support`, `context`, `binding_candidates`, `binding_status`, `uncertainty`, `missing`, and `blockers`. A binding candidate names the real BIND ID and T1 dataset, with current record hashes. An unresolved binding stays unresolved; an ID alone is not verification. Context includes geography, period, scenario and purpose. Future accepted profiles additionally require exact asset/band, quantity derivation, scale/offset, domain, NoData/status handling and support. Do not duplicate threshold prose in T5 rows.

`priority/proposals/<classification_id>-<version>.json` remains the owner of class definitions. The existing v1 proposal already carries quantity/unit, direction, three numeric thresholds or two tercile cuts, upper-inclusive endpoints, domain/conversion, context, spatial support, missing=unknown, source references, rationale, alternatives, blockers and decision identity. Structured source findings and explicit interpretation records supplement it without editing immutable v0.1.0 proposals. Each class mapping states the source finding, provider class, proposed decision class and justification. Terciles additionally require the reference population, geography/mask, period, exclusions, sample/hash, n, quantile algorithm, realized cuts and ties policy. No lowest-tercile 'none'. Uncertainty describes source error, transfer limitations and interpretation uncertainty separately.

## Evidence ownership and proposed extension

Existing EV intake requires practice/family and a suitability/effect role. It cannot safely represent practice-neutral calibration. Reserved `priority_need` and `climate_risk` labels are not an implemented route. Use a separate cross-cutting candidate bundle and schema under `workflows/priority_classification/`; propose a dedicated register manifest at `registers/cross_cutting/manifest.json`. The manifest names prospective canonical stores; those files are not created, and activation is explicitly disabled. No NbS, family or T4/effect lane is fabricated.

- **Source record (XCS):** stable source-version ID; title/publisher/URL/DOI; authoritative identity-verification record; original artefact hash, format and team acquisition path. A genuine existing SRC can be reused by immutable ID and record digest; otherwise XCS owns practice-neutral identity. These are candidate IDs until reviewed registration, not assertions that SRC/EV already contains them.
- **Finding record (XCE):** stable ID/version; source-version reference; exact passage/table/page/section; concise source-reported statement and structured values/units; geographic, temporal and population scope; uncertainty and transfer limits. No method scores or scientific approval. Findings have independent append-only keep/drop/query review events against exact content hashes. Drop is reversible quarantine, not deletion.
- **Search record (XSRCH):** query/provider/date, scope, returned/screened/included counts, inclusion decisions and stop rule. This separate log does not stamp the practice/family progress ledger or claim exhaustive coverage.
- **Interpretation:** method owns proposed source-class → decision-class mapping, alternatives and rationale. Evidence owns what the source actually reports. Source acceptance cannot approve that mapping.

Candidate validation, reviewability and registration eligibility are separate checks. PDF sources cannot register without a verified identity and team-library accession; local cache paths are not team access. Websites require a saved hashed snapshot and precise locator. Dataset downloads are not introduced by this route: only documentation is reviewed. No actual binding is marked verified from documentation alone.

## Exact trace and review gates

For water stress, the existing `wri_aqueduct40_2023` packet identifies the WRI technical note and page 11. A candidate XCS identifies those exact PDF bytes; candidate XCE findings preserve demand/supply definition, annual aggregation, basin support and the five provider bands separately. A second source/finding identifies the Earth Engine catalogue's `bws_raw`, category and score fields. Neither establishes four RuralScan classes.

`source (SRC reused or XCS) → XCE finding → source-review event → method interpretation → versioned classification proposal → exact human decision → immutable accepted release → T5.accepted_rule_ref`.

The concrete candidate trace is `xcs_wri_aqueduct40_2023@0.1.0` → `xce_aqueduct_quantity_support@0.1.0` and `xce_aqueduct_provider_bands@0.1.0` (printed page 11), supplemented by `xcs_aqueduct_gee_catalogue@0.1.0` → `xce_aqueduct_catalogue_fields@0.1.0` (Table Schema), then `aqueduct_bws@0.1.0` → the `water_stress` T5 extension row. The batch is pinned to evidence revision `7a134a578209b9eb1c51319f8c6d18dc78f7ebda`; its file SHA-256 is `4378a7a01456c690f43a49e323c97436daa3a24ef06abc0dfda081c2d2e6e23d`. Individual finding digests are in the interpretation record. Source review, human classification decision and accepted release are all absent, so `accepted_rule_ref` is empty.

Each arrow requires a full revision and content digest. The existing `aqueduct_bws-0.1.0` proposal remains held with null cuts. A later successor may propose a mapping, but acceptance must name its complete canonical hash and context hash through the existing method decision register and protected human PR. Before release, verify reviewed source receipts, binding/context fitness, no unresolved blockers, and the approved storage route. A keep finding vote, a merged infrastructure PR or passing CI alone is insufficient.

This batch creates no human decisions or accepted releases. The executable candidate route must reject claimed acceptance, fabricated source IDs, stale packet hashes and descriptor scoring. Production activation and immutable publication remain a separate protected change after the cross-cutting schema is approved. Historical source packets and proposal versions remain readable and unchanged.

## Compatibility

The shared priority scoring contract v1.0.0 remains byte-identical: thresholds default, explicit terciles alternative, scores 0/0.33/0.66/1, unknown missing, user weights, shared concerns counted once and CRITIC diagnostic only. M2b stays separate. Binary IPLC and carbon stock/potential cannot be forced into existing monotonic thresholds. Descriptors carry no proposed/accepted scoring rule. This extension introduces no runtime evaluator, T2 migration or compiler-pin change. Runtime issue #12 remains the integration reference.

## First bounded batch and implemented checks

The proposed T5 extension is populated for all 19 IDs, with versioned profiles and four references to existing held rule proposals. Six primary documentation sources support eight unreviewed findings across four T5 variables in [evidence PR #101](https://github.com/RuralScan/evidence/pull/101). [Structured interpretations](interpretations/t5-first-batch-0.1.0.json) distinguish source categories, proposed semantic mapping, examples and unresolved decisions. [Pinned evidence](t5-evidence.lock.json) identifies exact candidate bytes; these are not canonical XCS/XCE records yet.

The five original rule proposals are immutable and unchanged. These interpretation supplements do not amend their hashes or approvals. Any accepted successor must embed the selected interpretation, canonical reviewed evidence references, binding and context in its own full proposal hash. The current supplement cannot activate a rule.

Run `python3 priority/t5_refs.py`, `python3 priority/t5_review.py --evidence-repo /path/to/evidence`, and `python3 -m unittest discover -s priority`. Candidate intake, source identity replay and staging are implemented in evidence. Authenticated canonical registration, shared accessions, accepted-release publication and runtime adoption remain explicit future gates; no success is claimed for them.
