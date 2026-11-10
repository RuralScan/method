# Understand Rural Scan

Rural Scan turns a question about rural investment into a transparent set of spatial opportunities, risks and priorities. A recipe defines the nature-based solution being considered; versioned analytical tables describe how data and evidence enter the analysis.

For an executable first pass, open the Haiti notebook, inspect its holds, and use the module checklist to prepare a scoping brief. [Implement a rural scan](implement-a-scan.md)

## Follow the seven modules

| Module | Question |
|---|---|
| M0 — Setup and scope | Where are we working, which practices matter, and what decision should the scan support? |
| M1 — Opportunity space | Where do biophysical conditions, existing systems and hard exclusions allow the practice to be considered? |
| M2 — Rural climate risk | Which climate hazards affect livelihoods in that landscape? |
| M3 — Characterisation | Which people, production systems and other priorities overlap the opportunity space? |
| M4 — Priority hotspots | How do explicit, adjustable priorities change the areas worth investigating? |
| M5 — NbS scorecard | What benefits and trade-offs does the evidence support, with what limitations? |
| M6 — Implementation hand-off | What needs local validation, feasibility work or additional information before investment? |

The M2b addendum screens risk to the proposed investment, including asset hazards and operational barriers. It is a filter or flag, kept distinct from M2's livelihood-risk lens; the two are never added together.

## Follow a rule back to evidence

Trace a bench-terrace rainfall claim through its family, input dataset, evidence and scoring decision. [Read a suitability recipe](read-a-suitability-recipe.md)

A source is discovered, screened, acquired and catalogued. An extraction records a claim with its location and context. Review checks that extraction. Compilation combines eligible claims under explicit policies into candidate analytical tables. A separate acceptance decision produces a versioned release for runtime.

An approved extraction is not automatically a transferable threshold or an executable rule. Species/crop claims, operational barriers and source-specific assumptions retain their scopes. Missing information remains unknown; it must not become a default zero or an invented threshold.

Suitability is reasoned by families of sub-practices sharing a limiting factor. Linear or point practices are not reported as if every suitable pixel were implemented area. Recipe guidance must explain product type, spatial scale, host-system requirements, datasets, missing-data behavior and transfer assumptions.

## Read the status before implementation

Start with the [six-practice recipe selector](../cookbook/README.md). Choose the intervention you are considering, then identify its suitability family and the spatial output that family supports. Each guide distinguishes rows assigned to one family from rows recorded for the whole practice. For example, planting mangroves and restoring tidal exchange share a coastal family. Its candidate recipe contains hazard responses, scorecard effects and economic profiles. It has zero compiled suitability mappings. [Mangrove recipe guide](../cookbook/mangrove_restoration.md)

Use an accepted analytical manifest and compatible runtime version for an implementation. Record the AOI, dataset versions, transformations, grid, input pins and output hashes. Worked examples must distinguish exploratory reproduction from runs satisfying all required gates and spatial semantics.

See the [pinned source map and unresolved-reference index](../data-model/baseline.md) for the exact baseline, file hashes and preserved holds.
