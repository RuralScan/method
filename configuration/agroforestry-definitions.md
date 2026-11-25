# Agroforestry definitions and linear-family transition

Scientific decision: `agroforestry_family_definitions`. This branch proposes the
decision and its definition release; it becomes official through review and merge.
Evidence adoption is a separate protected PR. This release does not migrate
findings, transfer human approvals, regenerate scientific outputs or change runtime.

## Definitions

The [FAM register](../data-model/configuration/FAM_family_registry.csv) retains all
existing subpractice IDs. It separates establishment, system composition, location
and purpose instead of using those concepts interchangeably.

- **Planted trees in grazed pasture** (`planted_silvopasture`) means deliberately
  managed planted trees with forage and grazing livestock on the same land unit.
  In this catalogue, a separately identified crop component beyond forage belongs
  under **Trees with crops and livestock** (`agrosilvopasture`). Crops elsewhere on
  a farm, or fruit harvested from the trees, do not alone establish that component.
  Crop and livestock use can be simultaneous or a documented seasonal rotation.
  Both retain `agroforestry__silvopastoral`. The historical grassland-only gate
  cannot establish eligibility for every mixed crop–livestock system. A new
  accepted proposal must state the observed host system, timing and applicable
  constraints. The planted ID does not silently expand to unmanaged woodland
  grazing or to a new existing-tree silvopasture pathway.
- **Alley cropping** has woody rows and crop alleys; **Dispersed trees with annual
  crops** is the narrower display definition of `tree_intercropping`. Preserve
  broad source terminology when reviewing older findings. Both remain in the
  planted-silvoarable family; boundary planting moves out of that family.
- **Farmer-managed natural regeneration** and **assisted natural regeneration on
  farmland** remain related management variants in the regeneration family.
  **Parkland tree retention** describes keeping existing farm trees; recruitment
  is a renewal pathway, not a requirement inferred for every retained tree.
  An accepted mapping must state whether it addresses retention or recruitment.
- **Homegardens** remain qualitative-only; livestock may be present but do not
  automatically turn a small homestead garden into an area suitability surface.
  The existing cross-family tag remains evidence metadata, not an intervention.
  Missing family attribution is not evidence that a finding applies to all families.
- Soft tenure, access, finance and extension conditions belong in the operational
  risk and implementation stream. They are not structural exclusions. Hard legal
  exclusions remain structural masks.

FAO distinguishes trees with forage/livestock from systems also containing crops
and recognizes temporal combinations: [combined production systems, §4.2–4.3](https://www.fao.org/4/t0122e/t0122e04.htm).
Its [examples of agroforestry systems](https://www.fao.org/agroforestry/about-agroforestry/faqs/)
also illustrate overlapping location and function labels. The exact catalogue
boundaries here are project decisions, not a claim that one universal taxonomy
makes all source terminology mutually exclusive.

## Linear families

| Stable subpractice ID | New family ID | Placement logic |
|---|---|---|
| `planted_boundary_cropland` | `agroforestry__boundary_planting` | Cultivated-field boundary and host context; no wind or runoff function inferred from location |
| `windbreaks_shelterbelts` | `agroforestry__wind_shelter` | Wind-protection function and suitable orientation/placement; internal and field-edge positions are possible |
| `contour_vegetative_buffers` | `agroforestry__contour_buffers` | Woody buffers positioned with respect to contours and runoff pathways; no field-boundary requirement |

All three use `applicability_zone`. A candidate zone, a physical planting footprint
and an area receiving protection are distinct quantities. Never report every
eligible pixel as planted area; use documented geometry and locally supported
widths for footprint estimates. No universal width or numeric suitability rule is
introduced by these definitions.

A boundary windbreak has a location and a function. It is one installation, not
two counted interventions. Inspect which claim a finding supports; do not duplicate
an evidence ID or its review history to express multiple functions. If a consumer
cannot express multiple applicability relationships, retain that limitation and
the original attribution until a reviewed representation is available.

The [NRCS windbreak standard, definition and placement criteria](https://www.nrcs.usda.gov/sites/default/files/2022-10/Windbreak-Shelterbelt_Establishment_380_NHCP_CPS_2021.pdf)
supports distinguishing protective function from boundary location. Its numerical
design criteria are not adopted here. The split is a project inference: wind,
boundary and contour/runoff placement need different limiting-variable logic;
sharing a linear shape is insufficient for one scientific family. “Linear
plantings” may be a display group, not a pooled suitability surface.

## Historical attribution and evidence adoption

The [machine-readable transition](family-transitions/agroforestry-2026-11-24.json)
pins the previous method revision and FAM digest, retains all 13 previous
agroforestry definitions, and records the three changed memberships. It is a
review crosswalk, not an executable register migration.

`agroforestry__linear_boundary` is retired from new family assignments. Its old
windbreak and contour definitions remain resolvable through the transition and
the pinned edition. It is not an alias for either successor. The retained
`agroforestry__planted_silvoarable` ID no longer includes boundary planting in new
definitions, but older findings retain their recorded attribution until reviewed.

EV and SRCH do not identify subpractices directly. Neither an old family ID nor a
new definition is sufficient to allocate an existing finding to a successor.
Migration requires source/locator inspection, an explicit before/after record,
the governing method revision and rationale. Preserve evidence IDs, source links,
original quotations, prior review events and receipt history. Reopen changed
scientific scope through the supported review route; do not treat an old approval
as approval of a new interpretation. Leave unresolved records visible with their
original attribution. Do not duplicate search protocols into successor families.

The legacy `cross_family` value, when qualified by `nbs_id=agroforestry`, denotes
`agroforestry__cross_family`; it is unrelated to the linear split. Preserve reader
compatibility before any spelling-only normalization. No aliases are rewritten by
this release.

Before adopting this release in evidence, its consumers must support legacy
family resolution and pending scope review. The current pin/build route alone
does not implement that migration. A separate evidence PR must prove that old
findings, review logs, search scope and historical outputs remain readable before
changing the method pin. New AI proposals must use the revised definitions and
fresh input hashes; human acceptance precedes packaging. Historical T4 gates and
T3/T6 ratings remain historical. No automatic re-rating follows a FAM edit.

## Acceptance cases

| Case | Required result |
|---|---|
| Planted trees with managed grazed pasture | Livestock family; no crop component invented |
| Trees, crops and seasonal livestock use of the same unit | Agrosilvopasture; observed crop/grazing timing; do not rely solely on a grassland gate |
| Live fence with no wind-protection evidence | Boundary-placement family; no inferred wind benefit |
| Internal windbreak | Wind-shelter family; field-edge geometry not mandatory |
| Boundary windbreak | Wind function plus boundary location; one feature and deduplicated evidence |
| Woody contour strip within a field | Contour family; runoff/terrain placement rather than wind or boundary logic |
| Existing F1 or legacy-linear finding without specific scope | Retain original attribution pending source review; no automatic successor |
| Historical linear-family edition | Resolve its original definitions and records without changing IDs or approvals |
| General agroforestry finding with no demonstrated family coverage | Preserve uncertainty; do not broadcast to every family |

Definition and crosswalk checks run with `python3 -m unittest discover -s
configuration` and `python3 configuration/release.py check --base <previous-method-sha>`.
They validate this method release; they do not claim that an evidence migration,
new spatial model or human scientific review has occurred.
