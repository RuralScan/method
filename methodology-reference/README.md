# Rural NbS Scan methodology reference

A static, generated reference for technical readers: the scan method, the evidence methods, the data
model, six practices with every compiled row, the evidence base, and edition checks. Review build; it
is not published to Pages.

- `content/` authored chapters (27) and the chapter contract. Each chapter cites the pinned files it rests on.
- `build/` the generator. It reads the release pin, the recipe tables and registers at the pinned producer
  revision, the method cookbook names and the published readiness columns. Nothing analytical is typed in.
- `site/` the built pages (generated, not committed).

## Build and check

Needs Python 3.10 or later, `uv`, and local clones of this repository, RuralScan/evidence, RuralScan/runtime
and the producer repository. By default the build looks for them as sibling folders; set
`RURALSCAN_EVIDENCE`, `RURALSCAN_RUNTIME`, `RURALSCAN_CIAT` or `RURALSCAN_METHOD` to point elsewhere.

Before the first build, copy `build/people.example.txt` to `build/people.local.txt` and list the personal
names that appear in recorded review notes. The build removes them from public pages and fails if any remain.

    uv run --with markdown python3 -B build/build.py --out site
    python3 -m http.server 8137 --directory site

The build takes its edition from the evidence release pin. It fails if row counts differ from the counts the
release states, a link or anchor is broken, a chapter directive does not resolve, markup is unbalanced, or a
personal attribution reaches a page.

## Editing chapters

Chapters follow `content/CONTRACT.md`: every rule and formula carries a citation to the pinned file that
states it, rule tables are rendered from the pinned files rather than retyped, and anything the method does
not specify is marked as not specified.
