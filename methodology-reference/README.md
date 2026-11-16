# Rural NbS Scan methodology reference

A static, generated reference for technical readers: the scan method, the evidence methods, the data
model, six practices with every compiled row, the evidence base, and edition checks. Review build; it
is not published to Pages.

- `content/` authored chapters (28) and the chapter contract. Each chapter cites the pinned files it rests on.
- `build/` the generator. It reads the release pin, the recipe tables and registers at the pinned producer
  revision, the method cookbook names and the published readiness columns. Nothing analytical is typed in.
- `site/` the built pages (generated, not committed).

## Build and check

Needs Python 3.10 or later, `uv`, and local clones of this repository, RuralScan/evidence, RuralScan/runtime
and the producer repository. By default the build looks for them as sibling folders; set
`RURALSCAN_EVIDENCE`, `RURALSCAN_RUNTIME`, `RURALSCAN_CIAT` or `RURALSCAN_METHOD` to point elsewhere.

Before the first build, copy `build/people.example.txt` to `build/people.local.txt` and list the personal
names that appear in recorded review notes. The build removes them from public pages and fails if any remain.

    python3 build/fetch_package.py
    uv run --with markdown --with duckdb --with pandas python3 -B build/build.py --out site
    python3 -m http.server 8137 --directory site

The build also reads the published site branch of this repository at one fixed revision (`SITE_REV` in
`build/core.py`) for the live dashboard's label, its producer revisions, the data package edition and the list of drafts. Run
`git fetch origin gh-pages` once so that revision is available locally.

## Listed, and marked as under review

The reference is approved for the site's version list, so `LISTED` in `build/core.py` is `True` and pages carry
no no-index tag. A build check enforces whichever state `LISTED` declares. The top bar marks every page
"Under review" until the edition is released. Adding the entry to the site's version menu is done on the site
branch.

## People and the programme logo

The help page (`help.html`) is the one page that names people: the project contacts and team. They are read at
build time from the visual methodology's help page at the pinned revision, so this repository holds no names
and the two pages cannot disagree. The names check skips that page and no other.

The NBS Invest logo is shown on every page while `SHOW_PROGRAMME_LOGO` in `build/core.py` is `True`. Its use on
this site awaits confirmation from the programme. Set it to `False` to remove the logo everywhere.

## Pins, and knowing when they have moved

The reference reads other repositories at fixed revisions, all set in `build/core.py`: the scientific edition
(the producer revision in the evidence repository's release pin), `EVIDENCE_OPERATING` (current operating
procedures), `SITE_REV` (the published site) and `CIAT_RETIRED` (where the producer's evidence records became
read-only). Those repositories change several times a day. To see what has moved, and whether a plan that a
chapter links to as "not built yet" has since closed:

    python3 build/staleness.py

It needs only Python and network access, reports and does not fail (`--strict` makes it fail), and names the
changed files and what to re-read before moving a pin. Move one pin per pull request.

## Continuous integration

`.github/workflows/methodology-reference.yml` runs on pull requests and pushes that change this folder, and once
a day. It runs the report above, then builds the reference on a clean machine at the pinned revisions and runs
every build check. It publishes nothing. The names list is not in the repository: set it as the repository secret
`REFERENCE_PEOPLE` (the contents of `people.local.txt`). Without the secret the build still runs, with
`RURALSCAN_PEOPLE_OPTIONAL=1`: the personal-attribution check is reported as not run, and the output carries a
`NOT-FOR-PUBLICATION.txt` marker because recorded notes were not scrubbed. Never publish such a build.

`.github/workflows/change-areas.yml` notes when one pull request to `main` changes more than one top-level folder.
Several sessions work in this repository at once, each in its own folder; the note makes an overlap visible
before merge. It never fails.

## The data package

`build/fetch_package.py` is the only build step that uses the network. It downloads the published data package for the
edition (ten CSV tables and their description) into `.cache/`, starting from the edition catalogue and checking every
checksum. The build reads that copy offline, checks the checksums again, and runs every query recipe shown on the
"Query the data" page against it (DuckDB and pandas are needed only for this; the R recipe runs when `Rscript` is
installed). The package is linked, never copied into the built site.

The build takes its edition from the evidence release pin. It fails if row counts differ from the counts the
release states, a link or anchor is broken, a chapter directive does not resolve, markup is unbalanced, or a
personal attribution reaches a page.

## How it sits beside the live dashboard

The live evidence dashboard stays the default view of the site. Every page of this reference carries the
site's version menu in the live dashboard's three groups (Live, Under review, Earlier drafts), built from the
site's edition catalogue at the pinned site revision, with this reference listed once and selected, and
a Review queue link to the live queues. The overview starts with one finding followed end to end, opening
in the live dashboard. Finding decisions are submitted from the live dashboard to the evidence repository and
recorded there once applied; the producer repository keeps its earlier records read-only. This reference links to
the queues and does not copy or re-implement them. `review.html` explains how finding reviews, archived
finding reviews and rating decisions are kept apart, and which revision or repository each product reads.

## House style

The reference looks like the live evidence dashboard: same colours, fonts, corner radii, dark default and
header. This is a rule, not a preference. `STYLE.md` records it, and the build fails if a colour, font or
radius in `build/site.css` differs from the dashboard at the pinned site revision. Read `STYLE.md` before
changing the stylesheet or the page template.

The top bar is shared with the visual methodology: version menu, theme button, review tool, change history,
programme logo and help link. The review tool and the logo are read from the visual methodology at a pinned
revision at build time, so the products use one feedback tool, not three.

## Editing chapters

Chapters follow `content/CONTRACT.md`: every rule and formula carries a citation to the pinned file that
states it, rule tables are rendered from the pinned files rather than retyped, and anything the method does
not specify is marked as not specified.

## Data access and continuing the work

The Evidence base section is built for getting the data out: `evidence-base.html` lists every download with its
address, size and checksum, `data-guide.html` renders the field definitions and joins from the published package,
and `data-queries.html` holds query recipes in SQL, Python and R with the results of running them at build time.
The build also writes two files for programs: `llms.txt` (a plain-text guide for language-model agents) and
`data/assets.json` (every downloadable file with address, revision, row count and checksum).

`content/continue-with-ai.md` describes how to set up and run the agent-plus-human system that extends the evidence
base: where the instruction files live, the operating loop, the checks, the human approval points, where each kind
of record is written today and which routes are still planned. It works from two revisions. The scientific edition
is the producer revision in the evidence repository's release pin. The operating procedures are the evidence
repository at `EVIDENCE_OPERATING` in `build/core.py`; the build fails unless the evidence checkout is at exactly
that revision, so the chapter's text and its links cannot drift apart. To move it, check out the newer evidence
revision, re-read the chapter against the submissions guides, then change the constant. Citations written
`[src: retired:<path>]` open the producer repository at the revision where its evidence records became read-only.
