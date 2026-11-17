# Rural Scan methodology and review workspace

[Open Methodology](https://ruralscan.github.io/method/) · [Open the evidence review queue](https://ruralscan.github.io/method/dashboard.html#review-queue).

The 17 November Methodology is the default home page, published at `reference/index.html`. The 10 November evidence dashboard overview is superseded and remains at `dashboard.html` and `legacy.html`. Its evidence review workspace remains active, with dedicated T3, T4, T6 and M2b queues, source previews, personal review history and submission controls.

Existing root bookmarks keep working: `/#review-evidence=…`, `/#review-priority=…`, table queues, source links and other dashboard fragments route to `dashboard.html` with their full query and fragment intact. Bare `/` and `/index.html` open Methodology. Review queue links are prominent in the Methodology header and version bar. No register or submission route changes with this navigation update.

Review records, evidence and submissions belong to [RuralScan/evidence](https://github.com/RuralScan/evidence). The queue loads that repository's current published register snapshot and displays its revision. CIAT supplies archived provenance and the pinned historical analytical dashboard; it is not a live submission destination. The archived analytical baseline remains [CIAT release `bec50bc0f9dc`](https://github.com/CIAT/nbs_ruralscan/tree/bec50bc0f9dc74b3d5ffafcf881571a8a8ec5c06/docs). `QUEUE_PIN` in `publish_editions.py` supplies the historical fallback and earlier-citation history, not the current register writer.

The menu groups Methodology under **Live**, the 10 November dashboard under **Superseded**, and seven design snapshots under **Earlier drafts**. The `reference/index.html` entry in `editions.json` has `default: true`; adding a draft does not change the default. The publication branch decorates navigation on the pinned reference pages so their menus match the published site. It does not change reference chapter content or approve candidate recipes.

A push to `gh-pages` builds and deploys the Pages artifact. Methodology content is maintained on `main`; the workflow pins its source. Since Methodology is the default, missing reference output, a not-for-publication marker, a noindex page or an unexpected navigation structure stops publication. A failed build leaves the existing deployed site in place. The publication names check remains required.

Checks: `python3 -m unittest discover -s tests -p 'test_*.py'` and `node --test tests/*.test.cjs`.

## Connect a local PDF library

In the review queue, open **PDF folder** beside the reviewer selector, then **Connect PDF folder**. Choose the synced SharePoint library or the local corpus cache. Subfolders are included. Opening a source preview finds its registered library path or source filename and displays the PDF at the cited page. Files remain on the device and are read only when opened; they are not submitted with reviews.

Chrome and Edge can keep the directory handle in this site's IndexedDB storage. After a restart they may require **Allow folder access**, which reconnects the remembered folder without selecting files again. Use **Refresh folder** after downloading new PDFs, **Change folder** to choose another location, and **Disconnect** to forget the handle and clear local previews. Other browsers use a folder selection for the current visit and say when reconnection after reload is required. OneDrive files must be available to read; make them available offline if a preview fails.

Optional setup hints are in `review/library-locations.json`, keyed by reviewer handle. `peetmate` has the confirmed synced library and corpus-cache paths. These path hints are public, as authorized, but are not browser permissions or proof of a reviewer's identity. A new device or browser still needs its own folder selection. Connections apply to this browser, independently of the selected reviewer. Only add someone else's machine path with their authorization.

Matching uses the registered path where possible and refuses ambiguous duplicate filenames. A local filename match is not a verified quotation or scientific approval. Published preview provenance checks and all submission decisions remain unchanged. The public site cannot open an arbitrary absolute path from Git: the browser grants access through its folder chooser. See [Chrome's folder-permission documentation](https://developer.chrome.com/blog/persistent-permissions-for-the-file-system-access-api).
