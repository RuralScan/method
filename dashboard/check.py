"""Verify the generated edition before publication. Run against its edition directory."""

import json
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

import check_edition_evidence
import check_terrace


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = set()
        self.links = set()

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if "id" in attrs:
            self.targets.add(attrs["id"])
        if tag in {"a", "link", "script"}:
            href = attrs.get("href") or attrs.get("src")
            if href:
                self.links.add(href)


def check(directory):
    if not directory.is_dir():
        raise ValueError("Expected a built edition directory")
    check_terrace.check(str(directory.parent.parent))
    check_edition_evidence.check(directory)
    pages = {}
    for path in directory.glob("*.html"):
        parser = Links()
        parser.feed(path.read_text())
        pages[path.name] = parser
    counts = Counter(p.split("-", 1)[0] for p in pages)
    if counts["recipe"] != 6 or counts["row"] + 1 != 806 or counts["search"] != 229:
        raise ValueError(f"Edition inventory mismatch: {counts}")
    missing = []
    for page, info in pages.items():
        for href in info.links:
            url = urlsplit(href)
            if url.scheme or url.netloc:
                continue
            name = unquote(url.path) or page
            if name == "../../legacy.html":
                continue
            if (
                not (directory / name).is_file()
                or url.fragment
                and name in pages
                and name != "workbook.html"
                and unquote(url.fragment) not in pages[name].targets
            ):
                missing.append((page, href))
    if missing:
        raise ValueError(f"{len(missing)} broken references: {missing[:12]}")
    catalogue = json.loads((directory / "recipe-catalogue.json").read_text())
    status = json.loads((directory / "review-status.json").read_bytes())
    excluded = {
        "claim-" + eid + ".html"
        for eid, f in status["findings"].items()
        if f["excluded"]
    }
    if excluded - pages.keys():
        raise ValueError("Missing excluded-finding history")
    paths = {r["path"] for r in catalogue}
    if len(paths) != len(catalogue) or paths != {
        p for p in pages if p.startswith(("claim-", "source-"))
    }:
        raise ValueError("Evidence catalogue is incomplete")
    if {
        r["path"] for r in catalogue if "rejected (excluded)" in r["search"]
    } != excluded:
        raise ValueError("Excluded findings must be searchable and labelled")
    for eid, finding in status["findings"].items():
        card = "claim-" + eid + ".html"
        if finding["live_queue_available"] and not finding["live_batch"]:
            target = (
                "https://ciat.github.io/nbs_ruralscan/dashboard.html#review-evidence="
                + eid
            )
            if target not in pages[card].links:
                raise ValueError(f"Missing live CIAT queue link for {eid}")
    for table in ("t3", "t4", "t6"):
        lane = f"review-{table}.html"
        if lane not in pages["review.html"].links:
            raise ValueError(f"Review entry point is missing {table}")
    for key, record in status["rows"].items():
        table = record["table"].lower()
        path = f"row-{table}-{key}.html"
        if "review-details" not in pages[path].targets:
            raise ValueError(f"Missing review detail for {key}")
        if (
            record["provisional"]
            and "<strong>Provisional</strong>" not in (directory / path).read_text()
        ):
            raise ValueError(f"Missing provisional label for {key}")
    print(
        f"{len(pages):,} pages verified, including workbook, all analytical rows, search records and local anchors."
    )


if __name__ == "__main__":
    check(Path(sys.argv[1]))
