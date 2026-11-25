"""Check the built section 5/6 reader paths without changing evidence semantics.

Run after build.py: python test_practice_navigation.py <built-site>
"""
import csv
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
from urllib.parse import urlsplit, parse_qs


class Document(HTMLParser):
    def __init__(self, source):
        super().__init__()
        self.ids = {}
        self.links = []
        self.details = []
        self.feed(source)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "details":
            self.details.append("open" in attrs)
        if "id" in attrs:
            assert attrs["id"] not in self.ids, f'Duplicate anchor: {attrs["id"]}'
            self.ids[attrs["id"]] = tuple(self.details)
        if tag == "a":
            self.links.append(attrs.get("href", ""))

    def handle_endtag(self, tag):
        if tag == "details":
            self.details.pop()


def check(site):
    register = Path(__file__).resolve().parents[2] / "data-model/configuration/FAM_family_registry.csv"
    definitions = list(csv.DictReader(register.open()))
    counts = json.loads((site / "data/review-coverage.json").read_text())["rows"]
    landing = Document((site / "practices.html").read_text())
    assert landing.ids["rows"] == (False,), "Historical output totals must start collapsed"
    for practice in sorted({r["nbs_id"] for r in definitions}):
        name = f"practice-{practice}.html"
        html = (site / name).read_text()
        doc = Document(html)
        for anchor in ("definition-and-boundary", "current-families", "review-coverage"):
            assert doc.ids[anchor] == (), (practice, anchor, "core content hidden")
        for anchor in ("historical-rows", "registry", "families", "T4", "T3", "T6", "T6E", "chapter-sources"):
            assert doc.ids[anchor] == (False,), (practice, anchor, "history lost or expanded by default")
        assert f"evidence-practice-{practice}.html" in doc.links
        for row in definitions:
            if row["nbs_id"] == practice:
                assert "definition-" + row["subpractice_id"] in doc.ids
                assert row["suitability_family_id"] in html
        evidence_name = f"evidence-practice-{practice}.html"
        evidence_html = (site / evidence_name).read_text()
        evidence = Document(evidence_html)
        assert name in evidence.links
        assert name + "#historical-rows" in evidence.links
        for state in ("reviewed_kept", "awaiting", "held", "rejected"):
            assert any(parse_qs(urlsplit(h).query).get("state") == [state] for h in evidence.links), (practice, state)
        assert any('relation=broader' in h for h in evidence.links), practice
        row = next(r for r in counts if r["node"] == "practice:" + practice and r["lane"] == "all" and r["relation"] == "included")
        label = f'{row["reviewed_kept"]:,} / {row["retained_total"]:,}'
        assert label in html and label in evidence_html, (practice, label)
        # All local definition/history/finding entry links resolve, including every row detail.
        for current_name, document in [(name, doc), (evidence_name, evidence)]:
            for href in document.links:
                url = urlsplit(href)
                if url.scheme or url.netloc or not (url.path.endswith('.html') or not url.path):
                    continue
                target = site / (url.path or current_name)
                assert target.is_file(), href
                if url.fragment:
                    assert url.fragment in Document(target.read_text()).ids, href
    print("PASS: six practice/evidence paths; current definitions; matching totals; pending, held and broader links; historical anchors and row links")


if __name__ == "__main__":
    check(Path(sys.argv[1]))
