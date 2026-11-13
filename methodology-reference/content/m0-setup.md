---
title: "M0: Setup and scope"
slug: m0-setup
summary: Shows how a scan is configured, how recipe and data readiness are checked before any analysis, and what the run configuration must record for a result to be reproducible.
sources:
  - methodology/modules/M0_setup.md
  - methodology/modules/M1_suitability.md
  - methodology/framework.md
  - methodology/T4_generation_method.md
  - methodology/T4_developer_contract.md
  - schema/spec.md
  - src/nbs_ruralscan/runtime/binding.py
  - AGENTS.md
  - method:handbook/implement-a-scan.md
---

## Question this module answers

M0 asks: what is being scanned (which NbS, over which geography, at what detail, under which climate scenario and risk lens), and is everything needed to run it actually available? [src: methodology/modules/M0_setup.md §2. Question answered]

M0 is the entry point. It turns a set of user choices into a validated, reproducible **run configuration**, surfaces the recipe (variables and rules) behind those choices, and runs an ingestion check on every required dataset before any analysis starts. [src: methodology/modules/M0_setup.md §1. Purpose]

M0 performs no analysis. It configures and validates. It also does not author recipe content: it reads T0, T4, T5 and T6 as they stand. [src: methodology/modules/M0_setup.md §2. Question answered]

The specification sheet is a draft (v0.1) authored to match the setup screen of an earlier wireframe. Its open questions (below) are unresolved at the pin. [src: methodology/modules/M0_setup.md] [src: methodology/modules/README.md §Index]

## Inputs

| Input | Source | Schema | Notes |
|---|---|---|---|
| NbS selection, one or more | user | `T0.nbs_id` | Each selected NbS gets its own opportunity space; the sub-practice variant is chosen per NbS. |
| Geographic scope | user | [[table:T7]] | Country or region, sub-national focus, and administrative level, using neutral codes (ADM0, ADM1, ADM2). |
| Resolution | user | run configuration | See the resolution note below. |
| Climate-risk mode | user | run configuration | Mode A (hazard × exposure, default) or Mode B (hazard × exposure × vulnerability). |
| Scenarios to compare | user | run configuration | `baseline` plus one or more future scenarios. |
| Recipe and datasets | T0, T1, T4, T5 | schema rows | For the recipe summary and data-readiness check. |

[src: methodology/modules/M0_setup.md §3. Inputs]

In practice the scoping brief also records the practice in [[table:T0]], the **suitability family** in [[table:FAM]] (because suitability is reasoned per family), the spatial context in [[table:T7]] and the inputs in [[table:T1]], and resolves dataset bindings for the AOI. The brief should retain the decision question, boundary source, grid, dates, the family's spatial product type and input versions. [src: method:handbook/implement-a-scan.md §3. Build the scoping brief]

**Resolution: the sources disagree on the default.** The M0 specification offers 5 km (default, fast), 1 km and 500 m. The M1 specification offers 10 km, 5 km, 1 km, 500 m and 100 m with 1 km as default, matching the framework's pre-processing ladder. [src: methodology/modules/M0_setup.md §3. Inputs] [src: methodology/modules/M1_suitability.md §3. Inputs] [src: methodology/framework.md §Spatial standardisation] Whatever is chosen, the resolution actually usable is bounded by the selected variables and by the family's product type (see step 3 and [[ch:m1-suitability]]).

## Method

M0 runs six sub-steps in order. [src: methodology/modules/M0_setup.md §6. Sub-steps]

### 1. Scope capture

Record the NbS and sub-practice, the AOI as T7 contexts, the administrative level (neutral ADM code, never a hardcoded "district" or "county"), the resolution, the climate mode and the scenarios. [src: methodology/modules/M0_setup.md §6. Sub-steps] [src: methodology/modules/M0_setup.md §8. Tests / acceptance criteria]

The AOI determines the set of T7 context identifiers (country, region, agro-ecological zone, farming system, hydrobasin) used later for dataset binding and for context overrides of response parameters. [src: schema/spec.md §BIND]

### 2. Recipe resolution

For each NbS, resolve the recipe: T0 to its T4 suitability variables (per family) and its T5 priority variables, and compute variable counts before and after correlation clustering. [src: methodology/modules/M0_setup.md §6. Sub-steps] The post-clustering count is provisional at this stage, because clustering is run per AOI on standardised data in M1. [src: methodology/framework.md §Variable selection (two stages)]

Recipe resolution reads only what the schema holds. Nothing is hardcoded. [src: methodology/modules/M0_setup.md §8. Tests / acceptance criteria]

### 3. Data-readiness check

For every required dataset, report its hosting status: GEE catalogue, community-hosted, or pending upload. [src: methodology/modules/M0_setup.md §6. Sub-steps]

Dataset choice for a variable is context-resolved through [[table:BIND]]. For each variable the resolver collects bindings whose scope matches the AOI's contexts, picks the most specific scope, and breaks ties by lowest `preference_rank`:

```formula
admin_region > admin_country > hydrobasin > farming_system > aez > global
```

The ordering lists scope types from most to least specific; the most specific matching binding wins.

[src: schema/spec.md §BIND] [src: src/nbs_ruralscan/runtime/binding.py]

If the winning binding is `catalogued` or `community`, its dataset is used. If it is `requires_upload` (a better local dataset is known but not yet catalogued), the resolver falls back to the best fetchable binding, raises a needs-upload flag with a prompt for the user, and the substitution is recorded in the run configuration and the resolution audit. [src: schema/spec.md §BIND] [src: src/nbs_ruralscan/runtime/binding.py] [[ch:farming-systems-and-data]] describes the binding rules in full.

The same step applies a **resolution-honesty** check: it compares the coarsest required input with the chosen resolution and flags a run set finer than its data support. [src: methodology/modules/M0_setup.md §6. Sub-steps] [src: methodology/modules/M0_setup.md §8. Tests / acceptance criteria] It also seeds the resolution audit table that M1 to M4 append to. [src: methodology/modules/M0_setup.md §4. Outputs]

Two resolution limits apply, and M0 is where they first become visible. The first is the variable limit: each canonical variable carries `min_meaningful_resolution_m`, and the run's maximum coarseness is set by the most resolution-sensitive selected variable. The second is the footprint limit set by the family's `spatial_product_type`. [src: methodology/T4_generation_method.md §2.4 Per-variable resolution validity]

### 4. Ingestion validation

Confirm that each dataset is reachable or has an upload path. Hard-block the run on any required dataset that is unreachable and has no upload path. [src: methodology/modules/M0_setup.md §6. Sub-steps]

The distinction matters. A `requires_upload` binding does not block the run when a catalogued fallback exists; it produces a flag. An unreachable required dataset with no route blocks it. [src: src/nbs_ruralscan/runtime/binding.py] [src: methodology/modules/M0_setup.md §4. Outputs]

### 5. Variable-configuration surfaces

Expose two configuration surfaces for inspection: suitability variables (feeding M1) and priority or hotspot variables (feeding M3 and M4). Technical controls (cluster representatives, response curves, weights) are marked as technical-mode actions. [src: methodology/modules/M0_setup.md §6. Sub-steps] All Variable Cards for the selected NbS are surfaced read-only; editing them is a technical action. [src: methodology/modules/M0_setup.md §7. Variable Cards consumed]

Configuration choices made here do not change the evidence. In particular, a numeric suitability response requires an explicit selection of a response option with a recorded applicability note and decision reference; it is not chosen automatically, and selecting it does not make the spatial run ready. [src: methodology/T4_developer_contract.md §Selections, corrections and rebuilds]

### 6. Emit the run configuration

Write the run configuration, recording NbS, AOI, resolution, scenarios, mode, recipe and schema versions, dataset versions and date. [src: methodology/modules/M0_setup.md §6. Sub-steps]

For an implementation, the handbook asks for more than this minimum: the AOI and its boundary source, dataset versions, transformations, grid, input pins and output hashes, kept together with the output manifest and map legends. For each number in a brief, retain its unit, denominator and coverage. [src: method:handbook/start-here.md §Read the status before implementation] [src: method:handbook/implement-a-scan.md §3. Build the scoping brief]

## Outputs

| Output | Format | Consumer |
|---|---|---|
| Run configuration | JSON | every downstream module |
| Data-readiness report | JSON or CSV | readiness badges (GEE catalogue, community, pending upload) |
| Resolution-audit seed | CSV | appended by M1 to M4 |
| Ingestion status | JSON | blocks the run if a required dataset is unreachable and not uploadable |

[src: methodology/modules/M0_setup.md §4. Outputs]

Every analytical module reads the run configuration. M1 and M3 read the variable lists; M2 and M2b read the mode and scenarios. [src: methodology/modules/M0_setup.md §5. Dependencies]

### Acceptance criteria

The specification lists these tests: [src: methodology/modules/M0_setup.md §8. Tests / acceptance criteria]

- a valid run configuration capturing all choices with schema and dataset versions;
- every required dataset classified as catalogue, community or upload;
- the run blocked when a required dataset is unreachable and has no upload path;
- neutral administrative terminology throughout;
- the resolution-honesty flag firing when the chosen resolution is finer than the coarsest required input;
- recipe and datasets read from the schema, with nothing hardcoded.

None of these is recorded as passed at the pin; they are the specification's acceptance tests.

## Worked illustration

The published first-pass runtime check reads a supplied run configuration and scoring package and prints the outstanding holds before any map is made. For the agroforestry planted-silvoarable example it reports scoring package 0.1.5 and outstanding choices about the AOI boundary and its source, transfer of evidence to the target country, soil inputs and legal exclusions. [src: method:handbook/implement-a-scan.md §1. Check the inputs before making a map]

The example shows the M0 principle at work. A country code can resolve a data binding; it cannot establish that a response observed elsewhere transfers to that country. Target country (for binding) and evidence country (for applicability) are different filters, and M0 records the first without implying the second. [src: method:handbook/implement-a-scan.md §1. Check the inputs before making a map] [src: methodology/T4_developer_contract.md §Target country and evidence country are different filters]

## Assumptions and limits

- **Readiness is not validity.** M0 checks that data can be reached and that versions are recorded. It does not check that a dataset measures the variable the response requires, that units and depths match, or that a response transfers to the AOI. Those checks fall to M1 configuration and, ultimately, to feasibility work. [src: methodology/T4_developer_contract.md §Reproducible chain]
- **Unresolved design questions.** The specification leaves open whether a multi-NbS session produces one configuration per NbS or one configuration with an NbS list; whether pending-upload datasets are supplied manually or through a guided ingestion step; and whether the default administrative level is ADM2 or set by recipe and AOI. [src: methodology/modules/M0_setup.md §11. Open questions]
- **Default resolution is inconsistent between specifications** (5 km in M0, 1 km in M1). A run must state its resolution explicitly.
- **Global fallbacks can hide local better data.** When a `requires_upload` binding falls back to a global default, the run proceeds; the flag must be carried into outputs and the hand-off, not dropped.
- **Sensitive variables are flagged, not resolved.** Variables marked `context_sensitivity = high` (population, poverty, production statistics) should be confirmed against a country-endorsed source during feasibility. M0 does not perform that confirmation. [src: methodology/T4_generation_method.md §2.6]

## Where this is configured

- Practices: [[table:T0]]; families and product types: [[table:FAM]].
- Datasets and access routes: [[table:T1]]; context-specific dataset choice and upload flags: [[table:BIND]].
- Geographic, administrative and farming-system contexts: [[table:T7]].
- Variable resolution limits and sensitivity flags: [[table:VONT]].
- Suitability and priority variables surfaced for configuration: [[table:T4]], [[table:T5]]; approved run policies: [[table:T4_RUN]].
