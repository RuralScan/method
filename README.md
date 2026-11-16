# Rural Scan dashboard

[Open the dashboard](https://ruralscan.github.io/method/).

This branch publishes the existing static evidence dashboard on GitHub Pages. The November 10 analytical dashboard uses [CIAT release `bec50bc0f9dc`](https://github.com/CIAT/nbs_ruralscan/tree/bec50bc0f9dc74b3d5ffafcf881571a8a8ec5c06/docs). The queues use a separate CIAT revision, linked above the reviewer picker. To refresh their evidence, sources, and decision history, update `QUEUE_PIN` in `publish_editions.py` and rebuild. The build traces earlier T3/T6 recipe citations so personal history includes findings removed from ratings. Live review runs in the CIAT checkout.

The November 10 evidence dashboard opens at the root and at <code>dashboard.html</code>. Its original QA/QC queue has dedicated [T3 hazard](https://ruralscan.github.io/method/#review-t3) and [T4 suitability](https://ruralscan.github.io/method/#review-t4) views. The selector opens later design drafts at their pinned edition URLs. Adding a draft to <code>editions.json</code> keeps the live design selected.

A push to `gh-pages` builds and deploys the Pages artifact. The methodology and cookbook are maintained on `main`.

The version menu groups the evidence dashboard under **Live**, the methodology reference under **Under review**, and the seven snapshots under **Earlier drafts**, newest first. In `editions.json`, snapshot records have an `edition` ID. The reference record supplies its site-relative `href`, `group`, `label` and `date`. The Pages workflow pins the reference source and includes its menu entry only when the reference builds with the names list and passes its publication checks.
