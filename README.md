# Rural Scan methodology and review workspace

[Open Methodology](https://ruralscan.github.io/method/) · [Open the evidence review queue](https://ruralscan.github.io/method/dashboard.html#review-queue).

The 17 November Methodology is the default home page, published at `reference/index.html`. The 10 November evidence dashboard overview is superseded and remains at `dashboard.html` and `legacy.html`. Its evidence review workspace remains active, with dedicated T3, T4, T6 and M2b queues, source previews, personal review history and submission controls.

Existing root bookmarks keep working: `/#review-evidence=…`, `/#review-priority=…`, table queues, source links and other dashboard fragments route to `dashboard.html` with their full query and fragment intact. Bare `/` and `/index.html` open Methodology. Review queue links are prominent in the Methodology header and version bar. No register or submission route changes with this navigation update.

Review records, evidence and submissions belong to [RuralScan/evidence](https://github.com/RuralScan/evidence). The queue loads that repository's current published register snapshot and displays its revision. CIAT supplies archived provenance and the pinned historical analytical dashboard; it is not a live submission destination. The archived analytical baseline remains [CIAT release `bec50bc0f9dc`](https://github.com/CIAT/nbs_ruralscan/tree/bec50bc0f9dc74b3d5ffafcf881571a8a8ec5c06/docs). `QUEUE_PIN` in `publish_editions.py` supplies the historical fallback and earlier-citation history, not the current register writer.

The menu groups Methodology under **Live**, the 10 November dashboard under **Superseded**, and seven design snapshots under **Earlier drafts**. The `reference/index.html` entry in `editions.json` has `default: true`; adding a draft does not change the default. The publication branch decorates navigation on the pinned reference pages so their menus match the published site. It does not change reference chapter content or approve candidate recipes.

A push to `gh-pages` builds and deploys the Pages artifact. Methodology content is maintained on `main`; the workflow pins its source. Since Methodology is the default, missing reference output, a not-for-publication marker, a noindex page or an unexpected navigation structure stops publication. A failed build leaves the existing deployed site in place. The publication names check remains required.

Checks: `python3 -m unittest discover -s tests -p 'test_*.py'` and `node --test tests/*.test.cjs`.
