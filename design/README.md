# Use the Rural Scan table colours

Use the analytical table ID and a short title together wherever a figure, recipe or notebook refers to the data model. The colour pair identifies the table family. Give review state, confidence and suitability scores their own explicit labels. [Data model](../data-model/spec.md)

| ID | Label for a reader |
|---|---|
| T0 | Practice definition |
| T1 | Input datasets |
| T2 | Climate risk formulation |
| T3 | Responses to hazards by farming system |
| T4 | Suitability mappings |
| T5 | Opportunity-space indicators |
| T6 | Practice scorecard |
| T7 | Geographic context |

The shared stylesheet supplies the eight original table colours and the evidence-register colour. Use the register style with the actual register ID, such as SRC or EV. Use the parent table colour for a subdivision and retain its full ID, such as T6E for economic profiles. [Shared stylesheet](tables.css) · [Original schema diagram and colour definitions](https://github.com/CIAT/nbs_ruralscan/blob/157a26c2729c05cccf2b1d9374a63e28c97acac6/docs/erd.html#L32-L43)

## Label a figure

For the terrace example, label the steps **SRC · Terrace manual**, **EV · Rainfall observation, PDF p. 129** and **T4 · Bench terraces, annual precipitation**. Caption the decision in words. The reported 200–600 mm/year describes where the benches were observed. The compiled row retains the observation and leaves the numerical score unassigned. [Worked terrace example](../handbook/read-a-suitability-recipe.md)

Import the stylesheet into your document and apply a table ID to a label. Use normal-weight body copy outside the label. The text and border remain legible when background printing is turned off.

```html
<link rel="stylesheet" href="design/tables.css">
<span data-ruralscan-table="T4">T4 · Suitability mappings</span>
```

For plotted series, place the table ID and unit in the legend or direct labels. Distinguish overlapping series by line style or marker shape. For maps, label scored, excluded and unknown areas separately and include the spatial resolution. A caption for counts should identify the release, counted unit and whether categories overlap.
