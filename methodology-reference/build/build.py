"""Build the methodology into a fresh output directory, then check it.

    uv run --with markdown --with duckdb --with pandas python3 -B build/build.py --out site

Reads pinned Git objects and the verified local copy of the published data package.
Writes only under --out.
"""

import argparse
import re
import shutil
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

import chapters
import core
import data
import pages_data
import pages_evidence
import pages_model
import pages_practices
import pages_text

HERE = Path(__file__).resolve().parent
# Personal attributions must not reach public pages. Published authors in citations are fine.
NAMES = core._PERSON


def counts_md():
    """Totals stated by the release, read from its counts file (not hardcoded here)."""
    text = (core.EVIDENCE / "workflows/recipe_release/counts.md").read_text()
    stated = {}
    for line in text.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 8 and cells[1].isdigit():
            stated[cells[0]] = [int(c) for c in cells[1:]]
    total = int(re.search(r"(\d+) analytical rows", text).group(1))
    return stated, total


def run_checks():
    results = []

    def check(name, ok, detail=""):
        # ok is None when a check could not be run; that is reported, never counted as a pass.
        results.append((name, None if ok is None else bool(ok), detail))

    stated, total = counts_md()
    check(
        "Row total equals the release count",
        len(data.ROWS) == total,
        f"{len(data.ROWS)} rows; release states {total}",
    )
    order = ["T3", "T4", "T6", "T6E"]
    bad = []
    for p in core.PRACTICE_IDS:
        name = core.words(p)
        mine = [data.ROW_COUNTS[(p, t)] for t in order]
        theirs = stated.get(
            name, stated.get(name.replace(" conservation", " conservation"))
        )
        if theirs is None or mine != theirs[:4]:
            bad.append(f"{p}: built {mine}, release {theirs}")
    check(
        "Rows by practice and table equal the release counts",
        not bad,
        "; ".join(bad) or "six practices by four tables",
    )
    s = pages_text.t4_status()
    tot = stated.get("Total", [0] * 7)
    check(
        "Readiness totals equal the release counts",
        [s["options"], s["selected"], s["validated"]] == tot[4:7],
        f"options {s['options']}, selected {s['selected']}, validated {s['validated']}; release {tot[4:7]}",
    )
    check(
        "Every suitability mapping has a published function role",
        all(data.readiness(r) for r in data.ROWS if r["table"] == "T4"),
    )
    missing = [i for i in data.ROWS_BY_EV if i not in data.EV_BY_ID]
    check(
        "Every finding cited by a row exists in the evidence register",
        not missing,
        f"{len(data.ROWS_BY_EV)} cited findings",
    )
    dropped = [
        i
        for i in data.ROWS_BY_EV
        if i in data.EV_BY_ID and not data.retained(data.EV_BY_ID[i])
    ]
    check(
        "No row cites a dropped finding",
        not dropped,
        f"{len(dropped)} dropped findings cited",
    )
    orphan = [
        u["evidence_id"] for u in data.EV if u.get("source_id") not in data.SRC_BY_ID
    ]
    check(
        "Every finding names a registered source",
        not orphan,
        f"{len(orphan)} findings without a registered source",
    )
    check(
        "One detail page for every row",
        sum(1 for f in core.PAGES if f.startswith("row-")) == len(data.ROWS),
    )
    check(
        "Authored chapters are complete and their directives resolve",
        not chapters.PROBLEMS,
        "; ".join(chapters.PROBLEMS[:6]),
    )

    ids = {
        name: set(re.findall(r'\sid="([^"]+)"', html))
        for name, html in core.PAGES.items()
    }
    broken = []
    for name, html in core.PAGES.items():
        for href in set(re.findall(r'href="([^"]+)"', html)):
            if re.match(r"^[a-z]+:", href) or href.startswith("//"):
                continue
            target, _, frag = href.partition("#")
            target = target or name
            if (
                target in ("site.css", "site.js", "reproduce.html")
                or target in core.FILES
                or target in core.ASSETS
            ):
                continue
            if target not in core.PAGES:
                broken.append(f"{name} -> {href}")
            elif frag and frag not in ids[target]:
                broken.append(f"{name} -> {href} (anchor)")
    check(
        "Every internal link and anchor resolves",
        not broken,
        "; ".join(broken[:8])
        + (f" (+{len(broken) - 8} more)" if len(broken) > 8 else ""),
    )

    # The help page is the one page that names people: the project contacts and team, read from the
    # visual methodology. Every other page is checked.
    leaks = []
    for name, html in core.PAGES.items():
        if name == "help.html":
            continue
        body = re.sub(r"<[^>]+>", " ", html).replace(
            chapters.ATTRIBUTION.replace("<code>", " ").replace("</code>", " "), ""
        )
        for m in NAMES.finditer(body):
            leaks.append(
                f"{name}: …{body[max(0, m.start() - 30) : m.end() + 20].strip()}…"
            )
    check(
        "No personal attribution on any page",
        (not leaks) if core.PEOPLE_SUPPLIED else None,
        "; ".join(leaks[:6]) + (f" (+{len(leaks) - 6} more)" if len(leaks) > 6 else "")
        if core.PEOPLE_SUPPLIED
        else "The names list was not supplied, so recorded notes were not scrubbed. Do not publish this build.",
    )

    unbalanced = [
        n
        for n, h in core.PAGES.items()
        if len(re.findall(r"<div\b", h)) != h.count("</div>")
        or len(re.findall(r"<table\b", h)) != h.count("</table>")
    ]
    check("Page markup is balanced", not unbalanced, ", ".join(unbalanced[:5]))

    # The top bar is the same on every page, and the same set of controls as the visual methodology's.
    parts = (
        'id="dashboard-version"',
        'id="theme-toggle"',
        'class="vb-changes vb-hist" href="changes.html"',
        'src="review-mode.js"',
        'href="help.html"',
    )
    logo = f'src="{core.LOGO}"'
    bad = [
        n
        for n, h in core.PAGES.items()
        if not all(p in h for p in parts) or (logo in h) != core.SHOW_PROGRAMME_LOGO
    ]
    named = (
        "mailto:" in core.PAGES["help.html"] and 'id="team"' in core.PAGES["help.html"]
    )
    if not named:
        bad.append("help.html has no contacts or team")
    tool = core.FILES["review-mode.js"]
    stale = [
        w
        for w in ("nbs_v2_review", "CIAT/nbs_ruralscan", "v2 pages", "ENSO")
        if w in tool
    ]
    check(
        "Shared top bar on every page: version menu, theme switch, review tool, help and change history; programme logo as switched; contacts on the help page",
        not bad and not stale and len(core.ASSETS[core.LOGO]) > 1000,
        ", ".join(bad[:5] + stale),
    )

    # House style: every house token in the stylesheet equals the live dashboard's at the pinned site revision.
    def declared(block):
        return {
            k: " ".join(v.split())
            for k, v in re.findall(r"(--[a-z-]+):\s*([^;]+);", block)
        }

    sheet = (core.ROOT / "build/site.css").read_text()
    dash = core._site("dashboard.html")
    drift = []
    for mode, opener in (("dark", ":root {"), ("light", '[data-theme="light"] {')):
        ours = declared(
            sheet.split(f"/* house tokens: {mode}")[1].split("/* end house tokens */")[
                0
            ]
        )
        theirs = declared(dash.split(opener, 1)[1].split("}", 1)[0])
        drift += [
            f"{mode} {k}: {v} here, {theirs.get(k, 'absent')} on the dashboard"
            for k, v in ours.items()
            if theirs.get(k) != v
        ]
        if len(ours) < 13:
            drift.append(f"{mode}: only {len(ours)} house tokens declared")
    fonts = re.search(r'href="(https://fonts\.googleapis\.com/css2[^"]+)"', dash)
    if not fonts or fonts.group(1).replace("&amp;", "&") != core.FONTS:
        drift.append("font link differs from the dashboard's")
    if '<body data-theme="dark"' not in dash:
        drift.append("the dashboard no longer opens in its dark theme")
    check(
        "House style: colours, fonts, radii and the dark default match the live dashboard at the pinned site revision",
        not drift,
        "; ".join(drift[:6]),
    )

    wrong = [
        n
        for n, h in core.PAGES.items()
        if re.search(
            r"reviewed calibration|awaiting calibration|(?<!sub-)practice variant",
            h,
            re.IGNORECASE,
        )
    ]
    check(
        "Held and unrecorded calibration is never described as reviewed or pending",
        not wrong,
        ", ".join(wrong[:5]),
    )

    # The version menu matches the deployed dashboard's: three groups, and this methodology once, selected.
    grouped = re.compile(r'<optgroup label="([^"]+)">(.*?)</optgroup>')
    option = re.compile(r"<option value=\"([^\"]*)\"( selected)?>([^<]*)</option>")
    drafts = [(url, "", label) for url, label in core.SITE_DRAFTS]
    bad = []
    for name, html in core.PAGES.items():
        menu = html.split('<select id="dashboard-version"', 1)[1].split("</select>", 1)[
            0
        ]
        groups = [(g, option.findall(items)) for g, items in grouped.findall(menu)]
        total = sum(len(items) for _, items in groups)
        ok = (
            [g for g, _ in groups]
            == [core.LIVE_GROUP, core.REFERENCE_GROUP, core.DRAFTS_GROUP]
            and total == len(core.SITE_DRAFTS) + 2 == len(option.findall(menu))
            and len(groups[0][1]) == 1
            and groups[0][1][0][0].startswith(core.SITE_URL + "dashboard.html#")
            and groups[0][1][0][1] == ""
            and groups[0][1][0][2].startswith(core.LIVE_LABEL)
            and groups[1][1]
            == [(core.REFERENCE_URL, " selected", core.REFERENCE_LABEL)]
            and groups[2][1] == drafts
        )
        if not ok:
            bad.append(name)
    check(
        "Version menu on every page: Live, Under review and Earlier drafts as the deployed dashboard lists them, "
        "with this methodology once and selected",
        not bad,
        ", ".join(bad[:5]),
    )

    tag = '<meta name="robots" content="noindex">'
    bad = [n for n, h in core.PAGES.items() if (tag in h) == core.LISTED]
    check(
        "Every page asks search engines not to index it while the reference is unlisted"
        if not core.LISTED
        else "No page carries a no-index tag now that the reference is listed",
        not bad,
        ", ".join(bad[:5]),
    )

    queue = f'href="{core.live("review-queue")}"'
    tables = [f'href="{core.live(anchor)}"' for _, anchor, _ in core.REVIEW_QUEUES]
    bad = [n for n, h in core.PAGES.items() if queue not in h]
    bad += [
        n
        for n in ("index.html", "review.html")
        if not all(link in core.PAGES[n] for link in tables)
    ]
    check(
        "Review queue is reachable from every page, and the T3, T4 and T6 queues from the overview",
        not bad,
        ", ".join(bad[:5]),
    )

    kinds = ("Finding review", "Archived finding review", "Rating decision")
    review = core.PAGES["review.html"]
    check(
        "Finding reviews, archived finding reviews and rating decisions are listed separately",
        all(f"<strong>{k}</strong>" in review for k in kinds),
    )

    start = core.PAGES["evidence-base.html"].split('id="walkthrough"')[1]
    first = re.search(r'<ol>\s*<li>.*?<a href="([^"]+)"', start, re.DOTALL)
    check(
        "The worked example sits in the evidence base part and starts with the terrace slope finding in the live dashboard",
        first
        and first.group(1) == core.live("review-evidence=" + pages_data.SLOPE_FINDING)
        and 'id="walkthrough"' not in core.PAGES["index.html"],
        first.group(1) if first else "no first step",
    )

    numbers = re.findall(
        r'<h2 id="[^"]+"><span class="secno">([\d.]+)</span>', core.PAGES["index.html"]
    )
    listed = re.findall(
        r'<li><a href="#[^"]+"><span class="n">([\d.]+)</span>',
        core.PAGES["index.html"].split('class="side"')[1].split("</nav>")[0],
    )
    check(
        "Overview sections are numbered from their order, 1.1 onward, and listed in the side bar",
        len(numbers) >= 5
        and numbers == [f"1.{i}" for i in range(1, len(numbers) + 1)]
        and listed == numbers,
        f"{numbers} / {listed}",
    )

    # The retired name, split so that a search for it does not find this line.
    OLD_NAME = "methodology " + "reference|this " + "reference"

    bad = sorted(
        n for n, h in core.PAGES.items() if re.search(OLD_NAME, h, re.IGNORECASE)
    )
    check(
        "Pages call this the methodology, in the version menu as well as the text",
        not bad,
        f"{len(bad)} pages: " + ", ".join(bad[:5]),
    )
    for name, ok, detail in pages_data.CHECKS:
        check(name, ok, detail)
    check(
        "The evidence checkout is the revision whose operating procedures are described",
        core.EVIDENCE_REV == core.EVIDENCE_OPERATING,
        f"checkout {core.EVIDENCE_REV[:8]}; described {core.EVIDENCE_OPERATING[:8]}",
    )
    return results


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()
    out = args.out.resolve()
    if (
        out.exists()
        and any(out.iterdir())
        and not (out / ".methodology-reference").exists()
    ):
        raise SystemExit(f"{out} is not empty and was not created by this build")

    chapters.titles()
    pages_practices.build()
    pages_model.build()
    pages_evidence.build()
    pages_data.build()
    pages_text.build()

    results = run_checks()
    rows = [
        [
            core.esc(n),
            "Not run" if ok is None else "Pass" if ok else "<strong>Fail</strong>",
            core.esc(d),
        ]
        for n, ok, d in results
    ]
    body = (
        "<p>This methodology is generated. Nothing on it is typed in by hand except the chapter text, and the "
        "chapter text cites the files it rests on. A build reads the release pin, reads every table and "
        "register from the pinned revision, renders the pages, and then runs the checks below. A failed "
        "check fails the build.</p>"
        '<h2 id="checks">Checks run on this build</h2>'
        + core.table(
            ["Check", "Result", "Detail"],
            rows,
            caption="Build checks and their results",
        )
        + '<h2 id="rebuild">Rebuild this methodology</h2>'
        "<p>From the reference directory, with the method, evidence and producer repositories available locally:</p>"
        "<pre><code>python3 build/fetch_package.py\n"
        "uv run --with markdown --with duckdb --with pandas python3 -B build/build.py --out site</code></pre>"
        "<p>The first command downloads the published data package once and verifies it. The build then reads that copy, "
        "checks every checksum again and runs the query recipes against it. DuckDB and pandas are needed only for those recipes.</p>"
        "<p>The build takes its edition from the release pin, not from constants in the build code. To move "
        "to a new edition, update the pin and rebuild; the row totals are then checked against the counts "
        "the release states.</p>"
        '<h2 id="release">Rebuild the recipe release</h2>'
        f"<p>The recipe tables are a content-addressed release built from the producer revision. The procedure and its "
        f"checker are in the evidence workflows: {core.link(core.EVIDENCE_URL + 'workflows/recipe_release/README.md', 'recipe release guide')}. "
        f"A complete worked replay of one decision is kept as an example: "
        f"{core.link(core.EVIDENCE_URL + 'examples/terrace-rainfall/README.md', 'terrace rainfall example')}.</p>"
        '<h2 id="trace">Trace any value</h2><ol>'
        "<li>Open the row under its practice. The row page shows its fields, status and signals.</li>"
        "<li>Each cited finding links to its source page and locator.</li>"
        "<li>The source page lists every finding taken from that source and every row that cites them.</li>"
        "<li>The finding's verbatim quote is in the evidence register at the pinned revision, where an automated check compares it with the cached source text.</li></ol>"
    )
    core.page(
        "reproduce.html",
        "editions.html",
        "Reproduce and check",
        body,
        crumbs=[("editions.html", "Editions and checks"), ("", "Reproduce and check")],
        lead="How this methodology is built, the checks it must pass, and how to trace a value.",
        toc=[
            ("checks", "Checks run on this build"),
            ("rebuild", "Rebuild this methodology"),
            ("release", "Rebuild the recipe release"),
            ("trace", "Trace any value"),
        ],
    )

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    (out / ".methodology-reference").write_text(core.RELEASE + "\n")
    if not core.PEOPLE_SUPPLIED:
        (out / "NOT-FOR-PUBLICATION.txt").write_text(
            "Built without the names list: recorded review notes are not scrubbed.\n"
        )
    for name, html in core.PAGES.items():
        (out / name).write_text(html)
    for asset in ("site.css", "site.js"):
        shutil.copy(HERE / asset, out / asset)
    for name, text in core.FILES.items():
        (out / name).parent.mkdir(parents=True, exist_ok=True)
        (out / name).write_text(text)
    for name, blob in core.ASSETS.items():
        (out / name).parent.mkdir(parents=True, exist_ok=True)
        (out / name).write_bytes(blob)

    words = sum(chapters.WORDS.values())
    print(
        f"{len(core.PAGES)} pages · {len(data.ROWS)} rows · {len(chapters.WORDS)} chapters · {words:,} words"
    )
    failed = [r for r in results if r[1] is False]
    for name, ok, detail in results:
        print(
            ("SKIP  " if ok is None else "PASS  " if ok else "FAIL  ")
            + name
            + (f" — {detail[:300]}" if detail and not ok else "")
        )
    if failed:
        raise SystemExit(f"{len(failed)} check(s) failed")


if __name__ == "__main__":
    main()
