# Rural Scan methodology and review workspace

[Open Methodology](https://ruralscan.github.io/method/) · [Open the evidence review queue](https://ruralscan.github.io/method/dashboard.html#review-queue).

The Methodology is the default home page, published at `reference/index.html`. Its version number and date are written by its own build (`reference/version.json`) and read from there for the version menu; they are not typed on this branch. Its active review workspace is at `dashboard.html`, with dedicated T3, T4, T6 and M2b queues, source previews, personal review history and submission controls. Each selects its own entry in the live version menu. The old `legacy.html` address forwards to the current dashboard, preserving the requested view.

Existing root bookmarks keep working: `/#review-evidence=…`, `/#review-priority=…`, table queues, source links and other dashboard fragments route to `dashboard.html` with their full query and fragment intact. Bare `/` and `/index.html` open Methodology. Review queue links are prominent in the Methodology header and version bar. No register or submission route changes with this navigation update.

Review records, evidence and submissions belong to [RuralScan/evidence](https://github.com/RuralScan/evidence). The queue loads that repository's current published register snapshot and displays its revision. CIAT supplies archived provenance and the pinned historical analytical dashboard; it is not a live submission destination. The archived analytical baseline remains [CIAT release `bec50bc0f9dc`](https://github.com/CIAT/nbs_ruralscan/tree/bec50bc0f9dc74b3d5ffafcf881571a8a8ec5c06/docs). `QUEUE_PIN` in `publish_editions.py` supplies the historical fallback and earlier-citation history, not the current register writer.

The menu lists two entries under **Live**, the Methodology and the evidence dashboard (each selected on its own pages), and seven design snapshots under **Earlier drafts**. There is one dashboard: `legacy.html`, the old address of its superseded overview, forwards to `dashboard.html` and keeps the view asked for. Every page carries a browser-tab symbol: an open book for the Methodology and earlier drafts, three bars for the dashboard. The `reference/index.html` entry in `editions.json` has `default: true`; adding a draft does not change the default. The publication branch decorates navigation on the pinned reference pages so their menus match the published site. It does not change reference chapter content or approve candidate recipes.

A push to `gh-pages` builds and deploys the Pages artifact. Methodology content is maintained on `main`; the workflow pins its source. Since Methodology is the default, missing reference output, a not-for-publication marker, a noindex page or an unexpected navigation structure stops publication. A failed build leaves the existing deployed site in place. The publication names check remains required.

Tab 3 of the workspace, **Evidence**, shows every retained finding in plain words: five questions, each viewable as how much evidence there is or as what it says, with a search across all findings and a download of the whole evidence base. `dashboard-evidence.js` builds it in the browser from the registers the review queue already loads from RuralScan/evidence, so it follows the evidence repository without a rebuild. It combines nothing: a source is counted once per topic, and ranges are shown as reported. The three earlier analysis views (suitability relationships, the T4 explorer, hazard ratings) are no longer in the navigation; `#relationships`, `#evidence-explorer`, `#hazard-ratings` and `#t4/…` links still open them.

Checks: `python3 -m unittest discover -s tests -p 'test_*.py'` and `node --test tests/*.test.cjs`.

## Review findings

Choose your GitHub reviewer name, then use the left Filters sidebar for practice, evidence type (T3, T4, T6 or M2b), search and review-status filters. The review navigation and sidebar stay visible as findings scroll. On taller desktop screens, practice, family, evidence type and search also stay pinned while you scroll the remaining sidebar filters. On small screens, expand Filters above the queue. To review, Waiting for answers and My reviewed remain above the findings. Record status, origin and reviewer filters open a custom view; each count shows the number of findings that selection will display. Access and search round also respect the selected queue or custom filters. Compare the extracted values and quotation with **View source preview**, then use **Keep**, **Drop** or **Query** directly on the card. Drop requires a reason; Query requires a question. Open previews sit beside the finding on wider screens. Request history and extraction checks remain available under expandable details.

Decisions save immediately on this device, appear under **My reviewed**, and remain editable until submitted. **Submit all my decisions** at either end of the queue opens the batch summary and its RuralScan/evidence submission link; each revision has its own CSV download. After submission, confirming a verified GitHub receipt clears only the matching drafts. Undo or batch removal clears an unsubmitted draft without changing recorded reviews. Reviewer, finding and original register revision stay attached to each decision, including older saved batches. A T3/T6 finding shared by both views has one saved decision.

Keyboard controls: **j** / **↓** next finding, **↑** previous, **k** Keep, **d** Drop, **q** Query. Drop still requires a reason; Query focuses the question field when empty. Shortcuts are ignored while typing.

## Read a source

Use **Open source** on the finding card to read the paper in SharePoint or on its original website. SharePoint may ask you to sign in with your team account. No local folder, path, sync or helper service is required for this route. If access is missing, request it from the library maintainer.

### Optional: PDFs inside the dashboard

Open **Optional: PDFs inside the dashboard**, then **Connect PDF folder**, only if you want to view local PDFs inline. The recommended synced-library location remains available here for the configured reviewer; browsing to any suitable PDF folder is supported. Subfolders are included. Files remain on the device and are read only when opened; they are not submitted with reviews.

Chrome and Edge can keep the directory handle in this site's IndexedDB storage. After a restart they may require **Reconnect PDF folder**. Use **Refresh folder** after downloading new PDFs, **Change folder** to choose another location, and **Disconnect** to forget the handle and clear local previews. Other browsers use a folder selection for the current visit and say when reconnection after reload is required. OneDrive files must be available to read for local previews.

Optional setup hints are in `review/library-locations.json`, keyed by reviewer handle. `peetmate` has the confirmed synced-library path. These path hints are public, as authorized, but are not browser permissions or proof of a reviewer's identity. Connections apply to this browser, independently of the selected reviewer. Only add someone else's machine path with their authorization.

Matching uses the registered path where possible and refuses ambiguous duplicate filenames. A local filename match is not a verified quotation or scientific approval. Published preview provenance checks and all submission decisions remain unchanged. The public site cannot open an arbitrary absolute path from Git: the browser grants access through its folder chooser. See [Chrome's folder-permission documentation](https://developer.chrome.com/blog/persistent-permissions-for-the-file-system-access-api).

## Review component releases

The review workspace is maintained under [`review/`](review/README.md), with its own version, content hashes and release notes. Its header shows the Review version and the official evidence revision. It remains at the existing dashboard address, shares the site navigation and is published by the existing Pages workflow. See the component guide for its host contract, release command and compatibility checks.
