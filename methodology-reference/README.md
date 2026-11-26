# Rural NbS Scan methodology

Published as “Methodology”. The folder name and the address (`reference/`) keep the earlier word so existing links hold.

A static, generated reference for technical readers: the scan method, the evidence methods, the data
model, six practices with every compiled row, the evidence base, and edition checks. Review build; it
is not published to Pages.

- `content/` authored chapters and the chapter contract. Each chapter cites the pinned files it rests on.
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

### Review coverage in sections 5 and 6

`review-coverage-pin.json` pins the official RuralScan/evidence review queue by full revision and
SHA-256. `fetch_package.py` downloads it beside the historical recipe package; the offline build
checks its digest again. To refresh coverage, update that pin and the methodology version, then
rebuild and run the checks. This does not change the historical recipe edition or any review decisions.

Both sections use `build/review_coverage.py`: reviewed and kept / total retained, with pending,
held and rejected states visible. The denominator is kept + pending + held. Each scope uses unique
finding IDs, and broader or earlier-scope pointers are not added to child totals. All collected T3/T6
effects include uncited findings; the queue's T3 and T6 membership lists are labelled as cited subsets.

Source counts use distinct `source_id` values within exactly the same scope, lane and
relationship. `sources_retained` counts works reporting at least one kept, pending or held
finding; `sources_registered` also includes works with rejected-only findings. A source can
span several practices, lanes or review states, so their source counts must not be added.
The finding browser counts sources after applying every filter, including search, across
all matching pages. A source count does not imply source-wide approval or independent studies.
Duplicate publications under different source IDs require identity review; counts do not merge them by citation text.
Study/data/judgement origins require the separate synthesis audit; coverage leaves their
independence unassessed. Counts never select effect direction or assign synthesis weights.

The count links open a read-only, paginated finding browser. Every finding links to its live review
card, which may be newer than the pinned count. JSON and CSV coverage exports carry definitions and
source metadata, and are listed in `data/assets.json` and `llms.txt`.

    python3 -B -m unittest discover -s build -p test_review_coverage.py
    node build/test_review_coverage.cjs site

The tests reconcile official EV and review-log status, queue membership, practice totals, pending
findings with no compiled mapping, deduplication, broader context and earlier-scope retention. The
JavaScript test checks every generated scope/lane/relationship count against the browser selector.

## Version numbers

The methodology carries one version number, written major.minor.patch. It is kept in `VERSION.json` with its
date and status, and nowhere else: the build stamps it on every page, writes it to `version.json` beside the
pages, and the site reads its menu label from that file.

Raise the number in every pull request that changes a page:

| Part | Raise it when | Example |
|---|---|---|
| Major | The method works differently, so results could change | 1.0.0 to 2.0.0 |
| Minor | A chapter or section is added or rewritten | 0.8.0 to 0.9.0 |
| Patch | Wording, corrections or layout | 0.8.0 to 0.8.1 |

Versions before 1.0.0 are drafts (`"status": "draft"`). Version 1.0.0 is the first release
(`"status": "released"`).

Each version needs an entry at the top of `CHANGELOG.md`, headed `## [0.8.1] - 2026-11-20`, with one bullet per
change in plain words. The change history on "About versions and changes" and the release notes are made from it. Write for a reader of
the pages: no names, no pull request or issue numbers.

Three things hold this in place. The build fails if the top changelog entry is not the version in
`VERSION.json`. The pull request check fails if a file under `build/` or `content/` changed and the number did
not go up. When a new number reaches `main`, the "Methodology release" workflow tags it (`v0.8.1`) and
publishes the changelog entry as release notes.

The evidence base has its own number, written year.month.release. It stands for one release pin in the
evidence repository. `VERSION.json` lists each number beside its full release identifier, and the build stops
if the current pin has no number. When the pin moves to a new release, add a line for it there.

    python3 build/versioning.py version
    python3 build/versioning.py notes
    python3 build/versioning.py check-bump origin/main

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

The site root opens the current methodology; existing review and finding links continue to open the review workspace. Every page of this reference carries the
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

The published **System and setup** section gives a short operating entry point, repository map and human-review gates. It links detailed workflows rather than duplicating them.

Two older chapters on operating the evidence base are kept in `content/unpublished/` and are not built: `continue-with-ai.md` and `rulesets-and-learning.md`. See the note in that folder for how to publish one again.

The review page describes the evidence repository's operating procedures at `EVIDENCE_OPERATING` in `build/core.py`; the build fails unless the evidence checkout is at exactly that revision, so the text and its links cannot drift apart. To move it, check out the newer evidence revision, re-read the review page against the submissions guides, then change the constant. Citations written
`[src: retired:<path>]` open the producer repository at the revision where its evidence records became read-only.

## Evidence chapter ownership

The opening evidence chapter owns shared provenance, record meanings, classification and source appraisal.
Discovery, acquisition, extraction and review own their respective procedures. The common synthesis chapter
follows review and owns compatibility, dependence, weighting concepts and sensitivity guidance. The T4,
T3/T6 and T6E chapters own their numerical algorithms and table-specific gates. New guidance belongs in
these chapters; do not add a parallel registry dictionary or repeat numerical policies in a general guide.
The former `ch-evidence-registry.html` and `ch-combining-t4-evidence.html` addresses redirect to the
consolidated chapters so existing links remain usable.

## Pending override review

`build/override_review.py` reads the authoritative override CSV and its generated candidate JSON at `EVIDENCE_OPERATING`. It verifies exact committed bytes and calls that revision's official validator and reference evaluator. The shared `override-review.js` view appears in the override chapter and the published dashboard. The output `data/t4-overrides.json` is a pinned review snapshot, never an accepted mapping stream. Non-pending or active candidates fail this publication path; their later publication requires an explicit lifecycle integration. No acceptance or activation control is provided.

Run `python3 -m unittest discover -s build -p test_override_review.py` and `node --test build/test_override_review.cjs` in addition to the full build.
