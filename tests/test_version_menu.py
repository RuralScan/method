"""Exercise both publication outcomes on the live dashboard and a nested draft."""
import json
from pathlib import Path
import re
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import publish_editions as publish


class VersionMenuTest(unittest.TestCase):
    def test_reference_is_listed_only_when_published(self):
        catalog = json.loads(Path(publish.__file__).with_name("editions.json").read_text())
        editions = [row for row in catalog if "edition" in row]
        reference = next(row for row in catalog if row.get("href") == "reference/index.html")
        shell = ('<html><head></head><body><header></header><div id="tab-qaqc">'
                 '<a href="#review-t3">T3</a><a href="#review-t4">T4</a></div></body></html>')
        for available in (True, False):
            with self.subTest(available=available), TemporaryDirectory() as tmp:
                site = Path(tmp)
                (site / "legacy.html").write_bytes(Path(publish.__file__).with_name("dashboard.html").read_bytes())
                data = site / "data" / publish.LIVE_PIN[:12]
                data.mkdir(parents=True)
                (data / "dashboard_data.json").write_text('{"progress_overview":{"sources":[]},"recipes":{}}')
                for edition in editions:
                    directory = site / "editions" / edition["edition"]
                    directory.mkdir(parents=True)
                    (directory / "index.html").write_text(shell)
                (directory / "review-status.json").write_text('{"findings":{}}')
                if available:
                    entry = site / reference["href"]
                    entry.parent.mkdir()
                    entry.write_text("reference")
                    (entry.parent / "help.html").write_text("help")
                with patch.object(publish, "live_rating_reviews", return_value={}), \
                     patch.object(publish, "publish_review_queue", return_value="queue.json"):
                    publish.add_version_selectors(site, editions, None, reference)

                for page in [site / "index.html", directory / "index.html"]:
                    html = page.read_text()
                    menu = html.split('<select id="dashboard-version"', 1)[1].split(">", 1)[1].split("</select>", 1)[0]
                    groups = dict(re.findall(r'<optgroup label="([^"]+)">(.*?)</optgroup>', menu))
                    expected = ["Live", "Under review", "Earlier drafts"] if available else ["Live", "Earlier drafts"]
                    self.assertEqual(list(groups), expected)
                    self.assertEqual(re.findall(r'data-edition="([^"]+)"', groups["Earlier drafts"]),
                                     [edition["edition"] for edition in reversed(editions)])
                    self.assertEqual(menu.count(" selected"), 1)
                    if page.parent == site:
                        self.assertIn(" selected", groups["Live"])
                        bar = html.split('aria-label="Dashboard version and tools">', 1)[1].split("</div>", 1)[0]
                        controls = ['>Version</label>', 'id="dashboard-version-note"', 'id="theme-toggle"',
                                    'id="rv-toggle"', 'What changed? · history and feedback']
                        self.assertEqual(sorted(controls, key=bar.index), controls)
                        help_url = "reference/help.html" if available else "https://ciat.github.io/nbs_ruralscan/redesign/help.html"
                        self.assertIn(f'href="{help_url}">Help / Contact / Team</a>', html)
                    else:
                        self.assertIn(f'data-edition="{editions[-1]["edition"]}" selected', groups["Earlier drafts"])
                    if available:
                        href = reference["href"] if page.parent == site else "../../" + reference["href"]
                        label = "Methodology · 17 Nov 2026"
                        self.assertEqual(groups["Under review"], f'<option value="{href}">{label}</option>')
                        self.assertIn(f'<a href="{href}">{label}</a>', html)
                    else:
                        self.assertNotIn(reference["href"], html)
