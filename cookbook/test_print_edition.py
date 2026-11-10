"""Compare the portable cookbook with the seven published Markdown pages."""

from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
import re
import unittest

from markdown_it import MarkdownIt

from build import EVIDENCE_REVISION
from print_edition import render_edition


HERE = Path(__file__).resolve().parent


class Document(HTMLParser):
    """Collect reader-visible tables, links and headings without assuming a layout."""

    def __init__(self, html):
        super().__init__()
        self.rows = []
        self.cell = None
        self.headings = []
        self.heading = None
        self.ids = []
        self.links = []
        self.tags = []
        self.text = []
        self.feed(html)
        self.close()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        self.tags.append((tag, attrs))
        if "id" in attrs:
            self.ids.append(attrs["id"])
        if tag == "a":
            self.links.append(attrs["href"])
        if tag == "tr":
            self.rows.append([])
        if tag in {"th", "td"}:
            self.cell = []
        if tag in {"h1", "h2", "h3"}:
            self.heading = []

    def handle_data(self, data):
        self.text.append(data)
        if self.cell is not None:
            self.cell.append(data)
        if self.heading is not None:
            self.heading.append(data)

    def handle_endtag(self, tag):
        if tag in {"th", "td"}:
            self.rows[-1].append(" ".join("".join(self.cell).split()))
            self.cell = None
        if tag in {"h1", "h2", "h3"}:
            self.headings.append((tag, "".join(self.heading).strip()))
            self.heading = None


class PrintEditionTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pages = {p.name: p.read_text() for p in HERE.glob("*.md")}
        markdown = MarkdownIt("commonmark").enable("table")
        cls.source = {
            name: Document(markdown.render(page)) for name, page in pages.items()
        }
        cls.table_css = (HERE.parent / "design" / "tables.css").read_text()
        cls.edition_css = "main { display: block; }"
        cls.html = render_edition(pages, cls.table_css, cls.edition_css)
        cls.edition = Document(cls.html)

    def test_each_chapter_preserves_table_cells_and_heading_order(self):
        names = ["README.md", *sorted(self.source.keys() - {"README.md"})]
        expected_rows = [row for name in names for row in self.source[name].rows]
        self.assertEqual(self.edition.rows, expected_rows)
        # Additional headings can label the always-visible family-ID lists.
        headings = iter(self.edition.headings)
        for name in names:
            for level, title in self.source[name].headings:
                self.assertIn(({"h1": "h2", "h2": "h3"}[level], title), headings)
        self.assertEqual(Counter(tag for tag, _ in self.edition.headings)["h1"], 1)

    def test_table_headings_identify_row_and_column_scopes(self):
        cells = [attrs for tag, attrs in self.edition.tags if tag == "th"]
        row_headers = sum(cell.get("scope") == "row" for cell in cells)
        data_rows = sum(tag == "tr" for tag, _ in self.edition.tags) - sum(
            tag == "thead" for tag, _ in self.edition.tags
        )
        self.assertEqual(row_headers, data_rows)
        self.assertTrue(all(cell.get("scope") in {"row", "col"} for cell in cells))
        labelled_tables = {
            attrs.get("data-ruralscan-table") for _, attrs in self.edition.tags
        }
        self.assertLessEqual({"T3", "T4", "T6", "T6E"}, labelled_tables)

    def test_navigation_and_pinned_references_survive_download(self):
        hrefs = set(self.edition.links)
        anchors = {href[1:] for href in hrefs if href.startswith("#")}
        self.assertLessEqual(anchors, set(self.edition.ids))
        self.assertEqual(len(self.edition.ids), len(set(self.edition.ids)))
        for name, doc in self.source.items():
            self.assertIn(
                "overview" if name == "README.md" else Path(name).stem, anchors
            )
            for href in doc.links:
                if href.startswith("https://"):
                    self.assertIn(href, hrefs)
                elif href.startswith("../handbook/"):
                    path = re.escape(href.removeprefix("../"))
                    pattern = rf"https://github\.com/RuralScan/method/blob/[0-9a-f]{{40}}/{path}"
                    self.assertTrue(
                        any(re.fullmatch(pattern, url) for url in hrefs), href
                    )
        self.assertTrue(all(href.startswith(("#", "https://")) for href in hrefs))

    def test_haiti_handoff_uses_the_same_workbook_in_both_editions(self):
        workbook = (
            f"https://github.com/RuralScan/evidence/blob/{EVIDENCE_REVISION}"
            "/publication/workbook/index.html"
        )
        for page in ("README.md", "agroforestry.md"):
            self.assertIn(workbook, self.source[page].links)
            self.assertIn("Trace the Haiti example", "".join(self.source[page].text))
        self.assertIn(workbook, self.edition.links)

    def test_family_identifiers_and_styles_are_available_offline(self):
        text = "".join(self.edition.text)
        sources = "".join("".join(doc.text) for doc in self.source.values())
        identifier = r"\b[a-z_]+__[a-z_]+\b"
        expected = Counter(re.findall(identifier, sources))
        self.assertTrue(expected)
        self.assertEqual(Counter(re.findall(identifier, text)), expected)
        self.assertIn(self.table_css.strip(), self.html)
        self.assertIn(self.edition_css, self.html)
        for tag, attrs in self.edition.tags:
            self.assertNotIn(tag, {"script", "link", "iframe"})
            if tag == "details":
                self.assertIn("open", attrs)
