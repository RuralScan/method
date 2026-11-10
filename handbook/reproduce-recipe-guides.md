# Reproduce the family recipe guides

The cookbook combines the method’s practice and family definitions with the analytical rows in one candidate release. Each practice page links to the evidence workbench at the revision used for the build. Choose the practice page directly to read the guide. [Open the cookbook](../cookbook/README.md)

## Read or print all six guides

Open `cookbook/rural-scan-cookbook.html` from your checkout in a browser. On GitHub, open the file and select **Download raw file**, then open the saved HTML. The practice links work offline. Follow the evidence and handbook links when connected.

Use the browser’s **Print** command to print on A4 or US Letter, or choose **Save as PDF**. Use the default scale and turn off browser headers and footers. Each practice starts on a new page. The family IDs and release identifier appear in the printed document.

## Check a published guide

From the root of the method repository, use Git, uv and Python 3.12. This command rebuilds the candidate in temporary storage and compares the resulting seven Markdown pages and standalone print edition with this checkout. The first run downloads pinned software and Git inputs.

```sh
uv run --python 3.12 --locked --script cookbook/build.py
```

For an offline check, use local clones containing the pinned commits and their objects, with the locked Python environment already in the uv cache:

```sh
uv run --offline --python 3.12 --locked --script cookbook/build.py --offline \
  --evidence-repo /path/to/evidence --ciat-repo /path/to/nbs_ruralscan \
  --method-repo /path/to/method
```

To inspect regenerated pages separately, append `--out /path/to/new-directory`. A successful run reports the candidate release ID, six practices, 28 families, 56 family-register entries and 806 analytical rows. Three register entries capture cross-family context. The build reads the pinned evidence checker and the candidate’s method lock. It validates the release members, method definition files and all six T0 identities before grouping analytical rows. A changed pin, missing family, mismatch in readiness counts or stale published page stops the check. [Pinned evidence release](https://github.com/RuralScan/evidence/blob/950f91ea29cea43a5a1a7928bddaef7758965cc7/workflows/recipe_release/pin.json)

## How rows are counted

T3, T4, T6 and T6E each carry an analytical row ID. A row with a family ID is counted once under its practice and that family. A row without a family ID appears once in the practice-wide count, even if it carries a geographic or farming-system condition. Several subpractices can share one family. Multiplying a family’s row count by its number of subpractices would overstate coverage.

The T4 readiness counts come from the candidate’s readiness report, restricted to compiled mapping IDs. One mapping can have functions available and a function selected, so these counts overlap. Extra reference-only entries in that report do not increase the mappings count. The original analytical records retain the context, units, evidence IDs and limitations. [Evidence recipe index](https://github.com/RuralScan/evidence/blob/950f91ea29cea43a5a1a7928bddaef7758965cc7/publication/recipes/README.md)

## Refresh a guide

When a new candidate is available, update the evidence revision in the builder and use its pinned method and producer revisions. Generate the Markdown and HTML together in a new directory. Review changes to family membership, spatial product types, scope counts and readiness alongside the practice-specific text before replacing the checked-in pages. Run the default check again. Candidate compilation, evidence review and runtime adoption have separate release histories.
