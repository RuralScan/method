# House style

The methodology reference looks like the live evidence dashboard. That is the house style. It is not a matter of taste for whoever edits the reference next: read this file before changing `build/site.css` or the page template in `build/core.py`.

## The rule

1. **The live dashboard is the source.** Colours, fonts, corner radii, card shadow and the dark default come from `dashboard.html` on the site branch, at the site revision pinned as `SITE_REV` in `build/core.py`.
2. **Copy, do not reinterpret.** The house tokens in `build/site.css` keep the dashboard's own names (`--bg-primary`, `--accent-emerald`, `--font-outfit` and the rest) and its exact values, in two marked blocks: dark and light.
3. **The build enforces it.** The check "House style: colours, fonts, radii and the dark default match the live dashboard at the pinned site revision" compares every house token, the font link and the dark default with the dashboard at `SITE_REV`. A drifted value fails the build.
4. **If the dashboard's style changes,** it changes there first. Move `SITE_REV`, let the check name what differs, and copy the new values across. Never change a house token here on its own.
5. **A new look for the reference is a decision, not an edit.** It needs approval, and this file and the check change in the same pull request.

## What the house style is

| Element | Style |
|---|---|
| Default theme | Dark, as the dashboard opens. A toggle in the header switches to light; the choice is remembered on the device. |
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
| Brand | The open-book mark in emerald, then "Rural NbS Scan" in Outfit 22px bold |
| Version bar | The dashboard's dark green bar, same wording pattern |
| Page width | 1400px |

## Where the reference differs, on purpose

These are the only departures. Each has a reason; do not add to the list without approval.

- **Secondary text uses `--text-secondary`, not `--text-muted`.** The reference is long-form reading, and the dashboard's muted grey is too faint for running text on the dark background.
- **Light-theme links and filled buttons use a darker emerald (`--accent-strong`, `#047857`).** The dashboard's light emerald does not reach the contrast needed for body-size text on white.
- **Body text is 16px.** The dashboard is a dense tool; the reference is read at length.
- **Table colour chips (T0 to T7) keep the project's table colours.** They are a separate, fixed scheme shared with the data-model diagrams.
- **Print is always light.**
- **The theme choice is remembered.** The dashboard's toggle is not.

## Fonts

Inter and Outfit load from Google Fonts with the same link the dashboard uses. If they do not load, the page falls back to the system sans-serif and still reads fully.

## Checking a change by eye

Open the reference and the live dashboard side by side in the same theme. Header, tabs, a card and a table should look like parts of one site. View the reference in both themes and at phone width before opening a pull request.
