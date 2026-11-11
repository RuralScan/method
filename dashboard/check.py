"""Verify the generated edition before publication. Run against its edition directory."""

import json
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


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
    if {r["path"] for r in catalogue} != {
        p for p in pages if p.startswith(("claim-", "source-"))
    }:
        raise ValueError("Evidence catalogue is incomplete")
    print(
        f"{len(pages):,} pages verified, including workbook, all analytical rows, search records and local anchors."
    )


if __name__ == "__main__":
    check(Path(sys.argv[1]))
