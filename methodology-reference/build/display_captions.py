"""Number and audit native table/figure captions on each methodology page."""

from html import escape, unescape
from html.parser import HTMLParser
import re


def plain(value):
    return re.sub(r"\s+", " ", unescape(re.sub(r"<[^>]+>", "", value))).strip()


def number_displays(body, title):
    """Page-local sequences; preserve authored captions and describe uncaptained tables."""
    for kind, caption_tag, label in (("table", "caption", "Table"), ("figure", "figcaption", "Figure")):
        counter = 0
        source = body

        def render(match):
            nonlocal counter
            counter += 1
            block = match.group(0)
            cap = re.search(rf"<{caption_tag}\b[^>]*>(.*?)</{caption_tag}>", block, re.S)
            if cap:
                description = re.sub(rf"^{label}\s+\d+(?:\.\d+)*[.:]?\s+", "", cap.group(1)).strip()
            elif kind == "table":
                headings = re.findall(r"<h[2-6]\b[^>]*>(.*?)</h[2-6]>", source[:match.start()], re.S)
                topic = plain(headings[-1]) if headings else title
                headers = [plain(h) for h in re.findall(r"<th\b[^>]*>(.*?)</th>", block, re.S)]
                description = escape(topic + (": " + ", ".join(headers[:3]) if headers else ""))
            else:
                raise ValueError(f"Figure without a descriptive caption on {title}")
            if not plain(description):
                raise ValueError(f"Empty {kind} caption on {title}")
            caption = f"<{caption_tag}>{label} {counter}. {description}</{caption_tag}>"
            if cap:
                return block[:cap.start()] + caption + block[cap.end():]
            opening = re.match(r"<table\b[^>]*>", block)
            return block[:opening.end()] + caption + block[opening.end():]

        body = re.sub(rf"<{kind}\b[^>]*>.*?</{kind}>", render, source, flags=re.S)
    return body


class CaptionAudit(HTMLParser):
    def __init__(self):
        super().__init__()
        self.stack = []
        self.errors = []
        self.counts = {"table": 0, "figure": 0}

    def handle_starttag(self, tag, attrs):
        if tag in self.counts:
            self.counts[tag] += 1
            self.stack.append(dict(kind=tag, number=self.counts[tag], captions=[], reading=False))
        elif self.stack and tag == {"table": "caption", "figure": "figcaption"}[self.stack[-1]["kind"]]:
            self.stack[-1]["captions"].append("")
            self.stack[-1]["reading"] = True

    def handle_data(self, data):
        if self.stack and self.stack[-1]["reading"]:
            self.stack[-1]["captions"][-1] += data

    def handle_endtag(self, tag):
        if not self.stack:
            return
        current = self.stack[-1]
        if tag in ("caption", "figcaption"):
            current["reading"] = False
        elif tag == current["kind"]:
            self.stack.pop()
            prefix = f"{tag.title()} {current['number']}. "
            captions = current["captions"]
            if len(captions) != 1 or not captions[0].startswith(prefix) or not captions[0][len(prefix):].strip():
                self.errors.append(f"{tag} {current['number']}: expected one numbered, descriptive caption")


def audit(html):
    parser = CaptionAudit()
    parser.feed(html)
    if parser.stack:
        parser.errors.append("Unclosed table or figure")
    return parser.errors
