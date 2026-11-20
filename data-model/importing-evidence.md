# Importing an evidence edition

Pin a full RuralScan/evidence commit and retain stable evidence and source IDs. The
[method pin](https://github.com/RuralScan/evidence/blob/e835eb6e7ed711a80e4593c0e9d66f9fbd3911b8/configuration/method-pin.json)
records the definitions used by that edition. VONT, FAM, BIND, XW and BANDS are authored
in method and mirrored into evidence. Evidence CI verifies those bytes against the
selected method release; equality with a later method `main` is not required.

## Retention is separate from review

`review_state = dropped` is a soft deletion: retain the row for audit and restoration,
but exclude it from synthesis. Blank `review_state` means retained. It does not establish
human approval, extraction validity or suitability for a particular analysis.
`reviewer_ok`, review history and the intended analytical lane remain separate checks.

For an importer that needs explicit status, derive a new field without changing the
register. Validate the known states rather than silently treating a new state as active:

```python
import csv

with open("EV_evidence_register.csv", encoding="utf-8", newline="") as stream:
    records = list(csv.DictReader(stream))
for row in records:
    state = row["review_state"]
    if state not in {"", "dropped"}:
        raise ValueError(f"Unknown review_state: {state!r}")
    row["is_retained"] = state == ""
retained = [row for row in records if row["is_retained"]]
```

At evidence revision `e835eb6e7ed711a80e4593c0e9d66f9fbd3911b8`, the 6,839 records comprise
5,252 retained rows and 1,587 dropped rows. These are edition-specific counts, not
approval counts or a permanent validation constraint.

## Knowledge basis and legacy spelling

Use `knowledge_basis` for current scientific-basis filtering and `extraction_format`
for prose/table/figure/code presentation. Keep `claim_basis` for historical compiler
reproduction. See the [classification contract](evidence-classification.json) and
[compatibility procedure](https://github.com/RuralScan/evidence/blob/e835eb6e7ed711a80e4593c0e9d66f9fbd3911b8/workflows/extraction/classification.md).

The same edition contains 28 retained rows with legacy `claim_basis = primary_measurement`.
Their `knowledge_basis` is `unknown`; they are not part of the 2,311 records tagged
`primary_measured` in the legacy field. Preserve and flag those 28 rows for source review.
Do not silently infer that an invalid spelling establishes measured knowledge.

This is not a harmless replacement for compiler reproduction: the
[pinned weighting convention](../methodology-reference/content/effect-synthesis.md#step-4-weight-each-unit)
gives unlisted legacy bases a factor of 0.5 and `primary_measured` a factor of 1.0.
Changing the value can therefore change synthesis weights and outputs. A correction
needs source verification, the existing correction/review trail and a candidate rebuild.
New intake already rejects this spelling because `claim_basis` must match a known
`knowledge_basis`. The import guidance does not reclassify claims or approve new weights.

## Runtime provenance

Use [RuralScan/runtime](https://github.com/RuralScan/runtime) for the executable
implementation. `runtime-fork-backup` is a separate fork, not the runtime linked by the
method workflow. Runtime's `upstream/PIN.json` records its historical CIAT package;
the pinned files are bundled in `upstream/` and checked locally by
`python scripts/sync_upstream.py --check`. CIAT/nbs_ruralscan was publicly readable
on 20 November 2026; a pin there is provenance, not a current authoring destination.
Method definitions, evidence records and runtime code now have separate repositories.
