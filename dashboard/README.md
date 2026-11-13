# Build and check the methodology dashboard

The public dashboard starts with the bench-terrace decision. Methods includes the AI workflow, new-practice and search-update procedures, review actions and the feedback loop. The public build reads pinned Git objects and method definitions. Live CIAT registration, review and the country pilot use their own entry points.

From the method checkout, use Python 3.10 or later, Git, the RuralScan/evidence clone and a CIAT/nbs_ruralscan clone containing the producer and progress commits. Run in a fresh output directory.

```sh
python3 -B dashboard/build.py --out /tmp/ruralscan-site \
  --evidence /path/to/evidence --ciat /path/to/nbs_ruralscan
python3 -B dashboard/check.py /tmp/ruralscan-site/editions/*
python3 -m http.server --directory /tmp/ruralscan-site
```

[Open Review](https://ruralscan.github.io/method/review.html) from the dashboard header. Review links the published T3/T6 ratings and T4 calibrations to applied finding decisions. The builder verifies the review-status manifest, producer revision, candidate release ID and workbook digest before rendering. Each live review link belongs to CIAT. A historical setter replay identifies which findings can change a headline rating at the candidate pin. The separate live batch can use a later scientific revision.

The publisher adds the top version selector after all editions pass their build checks. Set a display label and ISO date for each edition entry. The selector preserves a matching page and falls back to the selected edition’s overview when needed.

The last command serves the new pages locally. The publishing branch adds the previous dashboard, its libraries and its pinned records at the site root for historical deep links. Every new build has an edition directory. The site root opens the current overview and resolves saved hashes. Each claim, source, synthesis row and search event can be reached by following native links without the optional search catalogue.

To release a new edition, verify the paired method definitions and cookbook with the pinned evidence release checker. Update source pins, reader-facing examples and the expected edition inventory together. Run the historical terrace replay, verify the full candidate rebuild, run the link checks and exercise the keyboard, history and search-retry journeys. Commit the reviewed dashboard source. On the gh-pages branch append the edition ID and source revisions to editions.json. Its workflow rebuilds each listed edition, checks local references and publishes only after those checks pass. Preserve earlier list entries for shared URLs.
