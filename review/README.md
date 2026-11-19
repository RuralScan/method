# Review workspace component

The review workspace has its own version and release notes in `release.json`. Its current host remains `dashboard.html`; all finding and queue addresses stay the same. The component shares the dashboard's theme and navigation, and is assembled in the same Pages deployment. A review release does not change the Methodology version or the evidence revision.

## Files and host contract

- `workspace.html`, `gap-dialog.html`, `submission-dialogs.html`: markup inserted into named `REVIEW:` slots by `build.py`.
- `workspace.js`: snapshot loading, filters, finding cards, historical decisions, and the `ReviewWorkspace` lifecycle. Existing global card callbacks remain available for compatibility.
- `workspace.css`: review-specific styling, including the sticky sidebar and source preview layout.
- `priority.js`: review sets, finding routes and applied-correction panels. The existing `DashboardPriority` API is unchanged.
- The other scripts in this directory retain source previews, local PDF connections, browser drafts, public receipt creation and priority updates.

The host provides `reviewData`, `setDashboardSnapshots`, `familyDisplayName`, `DashboardTables`, `DashboardShell`, shared theme variables and measured navigation heights. It calls `ReviewWorkspace.mount()` after the DOM exists, `start()` after data loads, `onTab(tabId)` on navigation and `updateBuild()` after a snapshot refresh. The component is a classic script so old inline card actions and integrations keep working; it is not yet a standalone application.

`publish_editions.py` composes the component before decorating the dashboard. There is one markup/controller source. The generated dashboard loads hashed component assets; missing fragments or unstamped changes fail the build. The Review version in **What changed? · history and feedback** follows component content. The same history panel identifies the whole dashboard by its publishing commit, separately from the older overview data snapshot. Evidence links use the full RuralScan/evidence SHA actually loaded, separately from the historical dashboard data version.

## Change and release

1. Edit the files under `review/`. Keep existing IDs, callbacks, URL fragments and browser-storage keys compatible unless a migration is explicitly provided.
2. Stamp a new version once the change is ready:

   ```sh
   python3 -m review.build stamp --version 1.0.1 --note 'Describe the reviewer-visible change.'
   ```

   Use a patch for compatible fixes, a minor version for compatible additions and a major version for breaking changes. The command preserves earlier release notes and refuses reused or older version numbers.
3. Run the checks:

   ```sh
   python3 -m review.build check
   node --test tests/*.test.cjs
   python3 -m unittest discover -s tests -p 'test_*.py'
   ```

4. Open a PR targeting `gh-pages`. The **Review component checks** workflow runs the same tests. After approval and merge, the existing **Publish dashboard** workflow deploys it. No separate publication, evidence migration or submission route is required.

For a prepared local site with its normal snapshot metadata, compose the dashboard before serving it:

```sh
python3 -m review.build compose dashboard.html /path/to/prepared-site/dashboard.html
```

Copy `review/` and the existing host assets beside that output. The source dashboard contains build slots and must not be served directly. The full Pages build supplies version menus and pinned snapshot metadata as before.

## Compatibility checks

Test T3, T4, T6 and M2b; direct finding links; both reviewer histories; filter counts; applied-correction notes; source previews; remembered PDF folders; old saved drafts; and batch preview across lanes. Use synthetic findings for votes and never submit test decisions. Reverting a UI release must retain browser drafts and the official evidence history. RuralScan/evidence remains the source of records and the destination for review receipts.

## Review shortcuts and filters

The original CIAT shortcuts set the same axes displayed in the sidebar. All T3, T4, T6 and M2b queues use one predicate for findings and prospective counts. Changing a sidebar control refines the current selection; it does not switch to another queue mode. Practice, family, source, access, search, discovery round and selected review task remain in effect when choosing a shortcut.

- **To review:** active findings with no current decision by the selected reviewer. Other reviewers may have reviewed them. A reopened decision no longer counts as reviewed.
- **AI-flagged / AI-passed:** To review restricted by the AI verification origin.
- **2nd opinion:** active findings reviewed by others but not by the selected reviewer.
- **Kept / Queried:** the selected reviewer's current Keep / Query calls on active findings.
- **Dropped:** the selected reviewer's Drop calls, including saved drafts on records that have not yet been excluded. The sidebar's Record status distinguishes active records from dropped history.
- **My reviewed:** the reviewer's current calls across active and dropped findings. Archived finding reviews and rating decisions appear separately when their available metadata supports the selected scope; they do not inflate counts for refined EV filters.
- **Answers ready / Conflicts:** explicit follow-up presets, including previously reviewed findings. The Follow-up sidebar filter also provides waiting questions, requested rechecks and status reconciliation. Gaps and Stats retain their existing buttons.

An active task never overrides Reviewed by me. Use **Show requested rechecks** within a selected task to include earlier decisions explicitly. Task status changes preserve sidebar selections. Direct finding links still open the selected record, including decided and dropped findings; choosing a shortcut returns to the scoped queue.
