"""Build the methodology reference into a fresh output directory, then check it.

    uv run --with markdown python3 -B build/build.py --out site

Reads pinned Git objects only. Writes only under --out.
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
        results.append((name, bool(ok), detail))

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
            if target in ("site.css", "site.js", "reproduce.html"):
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

    leaks = []
    for name, html in core.PAGES.items():
        body = re.sub(r"<[^>]+>", " ", html).replace(
            chapters.ATTRIBUTION.replace("<code>", " ").replace("</code>", " "), ""
        )
        for m in NAMES.finditer(body):
            leaks.append(
                f"{name}: …{body[max(0, m.start() - 30) : m.end() + 20].strip()}…"
            )
    check(
        "No personal attribution on any page",
        not leaks,
        "; ".join(leaks[:6]) + (f" (+{len(leaks) - 6} more)" if len(leaks) > 6 else ""),
    )

    unbalanced = [
        n
        for n, h in core.PAGES.items()
        if len(re.findall(r"<div\b", h)) != h.count("</div>")
        or len(re.findall(r"<table\b", h)) != h.count("</table>")
    ]
    check("Page markup is balanced", not unbalanced, ", ".join(unbalanced[:5]))

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
    pages_text.build()

    results = run_checks()
    rows = [
        [core.esc(n), "Pass" if ok else "<strong>Fail</strong>", core.esc(d)]
        for n, ok, d in results
    ]
    body = (
        "<p>This reference is generated. Nothing on it is typed in by hand except the chapter text, and the "
        "chapter text cites the files it rests on. A build reads the release pin, reads every table and "
        "register from the pinned revision, renders the pages, and then runs the checks below. A failed "
        "check fails the build.</p>"
        '<h2 id="checks">Checks run on this build</h2>'
        + core.table(
            ["Check", "Result", "Detail"],
            rows,
            caption="Build checks and their results",
        )
        + '<h2 id="rebuild">Rebuild this reference</h2>'
        "<p>From the reference directory, with the method, evidence and producer repositories available locally:</p>"
        "<pre><code>uv run --with markdown python3 -B build/build.py --out site</code></pre>"
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
        lead="How this reference is built, the checks it must pass, and how to trace a value.",
        toc=[
            ("checks", "Checks run on this build"),
            ("rebuild", "Rebuild this reference"),
            ("release", "Rebuild the recipe release"),
            ("trace", "Trace any value"),
        ],
    )

    if out.exists():
        shutil.rmtree(out)
    out.mkdir(parents=True)
    (out / ".methodology-reference").write_text(core.RELEASE + "\n")
    for name, html in core.PAGES.items():
        (out / name).write_text(html)
    for asset in ("site.css", "site.js"):
        shutil.copy(HERE / asset, out / asset)

    words = sum(chapters.WORDS.values())
    print(
        f"{len(core.PAGES)} pages · {len(data.ROWS)} rows · {len(chapters.WORDS)} chapters · {words:,} words"
    )
    failed = [r for r in results if not r[1]]
    for name, ok, detail in results:
        print(
            ("PASS  " if ok else "FAIL  ")
            + name
            + (f" — {detail[:300]}" if detail and not ok else "")
        )
    if failed:
        raise SystemExit(f"{len(failed)} check(s) failed")


if __name__ == "__main__":
    main()
