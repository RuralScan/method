# House style

The methodology looks like the live evidence dashboard. That is the house style. It is not a matter of taste for whoever edits the reference next: read this file before changing `build/site.css` or the page template in `build/core.py`.

## The rule

1. **The live dashboard is the source.** Colours, fonts, corner radii, card shadow and the dark default come from `dashboard.html` on the site branch, at the site revision pinned as `SITE_REV` in `build/core.py`.
2. **Copy, do not reinterpret.** The house tokens in `build/site.css` keep the dashboard's own names (`--bg-primary`, `--accent-emerald`, `--font-outfit` and the rest) and its exact values, in two marked blocks: dark and light.
3. **The build enforces it.** The check "House style: colours, fonts, radii and the dark default match the live dashboard at the pinned site revision" compares every house token, the font link and the dark default with the dashboard at `SITE_REV`. A drifted value fails the build.
4. **If the dashboard's style changes,** it changes there first. Move `SITE_REV`, let the check name what differs, and copy the new values across. Never change a house token here on its own.
5. **A new look for the reference is a decision, not an edit.** It needs approval, and this file and the check change in the same pull request.

## What the house style is

| Element | Style |
|---|---|
| Default theme | Dark, as the dashboard opens. The theme button in the top bar switches to light; the choice is remembered on the device. |
| Page background | `--bg-primary` |
| Header, cards, tables, panels | `--bg-secondary`, 1px `--border-color` border |
| Table headers, code, soft fills | `--bg-tertiary` |
| Body text | Inter, `--text-primary` |
| Secondary text | `--text-secondary` |
| Headings, brand, tab labels, big numbers, buttons | Outfit, weights 600 to 800 |
| Primary accent: links, active tab, bars, filled buttons | Emerald (`--accent-emerald`) |
| Second accent: focus ring, step labels | Sky (`--accent-sky`) |
| On hold | Amber (`--accent-amber`) |
| Warning | Rose (`--accent-rose`) |
| Cards and stat tiles | 12px radius (`--radius-lg`), `--card-shadow` |
| Tables, buttons, tab pills | 8px radius (`--radius-md`) |
| Section tabs | Pills. The active tab has the card background, emerald text, a border and the card shadow. |
| Table headers | Outfit 12px, upper case, 0.03em letter-spacing |
| Brand | The NBS Invest programme logo, unmodified and linked to the programme page, then the open-book mark in emerald and "Rural NbS Scan" in Outfit 22px bold. The logo is 68px high. |
| Top bar | Shared with the visual methodology. See the next section. |
| Page width | 1400px |

## Two looks, one frame

This was decided, not left open:

- **The visual methodology keeps its own look** (light, editorial). It is a mock-up for discussion and is not restyled.
- **The live dashboard and this reference share the dashboard's look** (dark by default), as set out above.
- **All three share the frame:** the top bar, the review tool, the programme logo and the help link.

Do not restyle the reference toward the visual methodology, or the reverse, to "finish" the alignment. Only the frame is shared.

## The top bar is shared with the visual methodology

Every product a reviewer moves between should carry the same controls in the same order, so nobody has to relearn them. The model is the visual methodology's version bar.

| Position | Control | Rule |
|---|---|---|
| 1 | **Version** label and menu | Three groups, as on the live dashboard: Live, Under review, Earlier drafts. Built from the site's edition catalogue. This reference appears once, selected. |
| 2 | Note | An "Under review" marker and one short line saying what this version is. |
| 3 | **Dark theme / Light theme** button | Same moon and sun icons and wording as the visual methodology. |
| 4 | **Review** button | Switches on the review tool. Reads "Review on" while active. |
| 5 | **What changed? · history and feedback** | Opens `changes.html`. |
| 6 | Live dashboard | Link back to the live evidence dashboard. |

Below the bar, the header carries the programme logo, the brand, the edition line, **Help / Contact / Team** and the Review queue button.

**The review tool is the visual methodology's own.** The build reads `review-mode.js` and `review-mode.css` from the visual methodology at the revision pinned as `VISUAL_REV` in `build/core.py` and changes only the storage keys, the page targets, the page names and the issue address. Do not write a second feedback tool and do not edit the generated files; change the substitutions. The build fails if a substitution no longer matches.

**The logo is read from the same revision,** with its source note written beside it (`assets/nbs-invest-logo.source.txt`). It is shown unmodified, to identify the programme context. It is the NBS Invest programme mark, not a World Bank corporate logo. Its use on this site awaits confirmation from the programme; `SHOW_PROGRAMME_LOGO` in `build/core.py` removes it from every page if needed.

**Help page.** `help.html` covers finding your way, giving feedback, contact, team and the programme. The contact, team and programme sections are read from the visual methodology's help page at `VISUAL_REV`, so the names have one home and this repository carries none. It is the only page that names people.

The check "Shared top bar on every page" enforces all of this.

## Where the reference differs, on purpose

These are the only departures. Each has a reason; do not add to the list without approval.

- **Secondary text uses `--text-secondary`, not `--text-muted`.** The reference is long-form reading, and the dashboard's muted grey is too faint for running text on the dark background.
- **Light-theme links and filled buttons use a darker emerald (`--accent-strong`, `#047857`).** The dashboard's light emerald does not reach the contrast needed for body-size text on white.
- **Body text is 16px.** The dashboard is a dense tool; the reference is read at length.
- **Table colour chips (T0 to T7) keep the project's table colours.** They are a separate, fixed scheme shared with the data-model diagrams.
- **Print is always light.**
- **The theme choice is remembered.** The dashboard's toggle is not.

## Name and overview

- **The public name is "Methodology".** Pages do not call it a "reference". The folder and the address keep the old word so links do not break. A check fails on the old name anywhere on a page, including the version menu, whose labels come from the site's edition catalogue.
- **The overview is a story, not a dashboard of counts.** It runs in this order: the problem, what the method does about it, who it is for, how it works (one figure), the working tool, how it was built, what it covers, what is settled, where the detail is. Counts of practices and evidence belong in the Practices part.
- **One figure shows the whole method:** how evidence becomes rules (AI-supported, checked by people), then the seven stages that apply them. Do not add a second method figure to the overview.
- **Overview sections are numbered from their order** (1.1, 1.2 ...) by the build, and listed at the top of the page. Do not type section numbers.
- **Boxes carry a tooltip.** Tabs, figure steps and count tiles each have one more line of detail on hover.

## Fonts

Inter and Outfit load from Google Fonts with the same link the dashboard uses. If they do not load, the page falls back to the system sans-serif and still reads fully.

## Checking a change by eye

Open the reference and the live dashboard side by side in the same theme. Header, tabs, a card and a table should look like parts of one site. View the reference in both themes and at phone width before opening a pull request.
