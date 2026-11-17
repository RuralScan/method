"""Promotion keeps the reference, active review workspace and old links distinct."""
import json
from pathlib import Path
import re
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import publish_editions as publish


REFERENCE = '''<html><head></head><body><header><a class="review-entry" href="https://ruralscan.github.io/method/dashboard.html#review-queue">Review queue</a></header>
<select id="dashboard-version" aria-describedby="dashboard-version-note"><option>Old menu</option></select>
<span id="dashboard-version-note"><b>Under review</b> Draft for approval</span>
<a class="vb-live" href="https://ruralscan.github.io/method/dashboard.html#overview">Live dashboard</a>
<noscript>Old links</noscript><main><h1>Methodology</h1><p>Draft recipe edition; candidate, not released.</p></main></body></html>'''


class VersionMenuTest(unittest.TestCase):
    def prepare(self, site, available=True):
        catalog = json.loads(Path(publish.__file__).with_name("editions.json").read_text())
        editions = [row for row in catalog if "edition" in row]
        reference = next(row for row in catalog if row.get("href") == "reference/index.html")
        (site / "legacy.html").write_bytes(Path(publish.__file__).with_name("dashboard.html").read_bytes())
        data = site / "data" / publish.LIVE_PIN[:12]
        data.mkdir(parents=True)
        (data / "dashboard_data.json").write_text('{"progress_overview":{"sources":[]},"recipes":{}}')
        for edition in editions:
            directory = site / "editions" / edition["edition"]
            directory.mkdir(parents=True)
            for name in ('index.html', 'review.html', 'claim-finding.html', 'source-paper.html'):
                (directory / name).write_text('<html><head></head><body><header></header><main>Unchanged content</main></body></html>')
        (directory / "review-status.json").write_text('{"findings":{}}')
        if available:
            entry = site / reference["href"]
            entry.parent.mkdir()
            for name in ('index.html', 'help.html', 'row-t4-finding.html'):
                (entry.parent / name).write_text(REFERENCE)
        return editions, reference

    def publish(self, site, editions, reference):
        with patch.object(publish, "live_rating_reviews", return_value={}), \
             patch.object(publish, "publish_review_queue", return_value="queue.json"):
            publish.add_version_selectors(site, editions, None, reference)

    def test_methodology_is_default_and_review_workspace_keeps_old_routes(self):
        with TemporaryDirectory() as tmp:
            site=Path(tmp);editions,reference=self.prepare(site)
            self.publish(site,editions,reference)
            self.assertEqual((site/'index.html').read_bytes(),Path(publish.__file__).with_name('index.html').read_bytes())
            self.assertIn('reference/index.html',(site/'index.html').read_text())
            self.assertTrue((site/'home-route.js').is_file())
            self.assertIn('dashboard.html#review-queue',(site/'review.html').read_text())
            for page in [site/'dashboard.html',site/'legacy.html',site/'reference/index.html',site/'reference/row-t4-finding.html',site/'editions'/editions[-1]['edition']/'review.html']:
                html=page.read_text()
                menu=html.split('<select id="dashboard-version"',1)[1].split('>',1)[1].split('</select>',1)[0]
                groups=dict(re.findall(r'<optgroup label="([^"]+)">(.*?)</optgroup>',menu))
                self.assertEqual(list(groups),['Live','Superseded','Earlier drafts'])
                self.assertIn('Methodology · 17 Nov 2026',groups['Live'])
                self.assertIn('Evidence dashboard · 10 Nov 2026',groups['Superseded'])
                self.assertIn('legacy.html#',groups['Superseded'])
                self.assertNotIn('dashboard.html',groups['Superseded'])
                self.assertEqual(menu.count(' selected'),1)
                if page.parent==site:
                    if page.name=='dashboard.html':
                        self.assertIn(' selected',groups['Live'])
                        self.assertNotIn('aria-label="Superseded dashboard"',html)
                        self.assertNotIn('Current review workspace',html)
                        self.assertNotIn('Methodology home</a>',html)
                        self.assertIn('id="dashboard-version-note" hidden></span>',html)
                    else:
                        self.assertIn(' selected',groups['Superseded'])
                        self.assertIn('aria-label="Superseded dashboard"',html)
                        self.assertIn('href="dashboard.html#review-queue">Open the current review queue',html)
                    self.assertIn('id="legacy-version-routes"',html)
                    self.assertIn('name="ciat-review-snapshot" content="queue.json"',html)
                    self.assertIn('id="vf-scope"',html)
                    self.assertIn('src="dashboard-tables.js?',html)
                    self.assertIn('id="review-table-description"',html)
                    self.assertNotIn('aria-label="Review findings by table"',html)
                    bar=html.split('aria-label="Dashboard version and tools">',1)[1].split('</div>',1)[0]
                    controls=['>Version</label>','id="dashboard-version-note"','id="theme-toggle"','id="rv-toggle"','What changed? · history and feedback']
                    self.assertEqual(sorted(controls,key=bar.index),controls)
                elif page.parent.name=='reference':
                    self.assertIn(' selected',groups['Live'])
                    self.assertIn('href="../dashboard.html#review-queue">Review queue</a>',html)
                    self.assertIn('Current methodology',html)
                    self.assertNotIn('Under review',html)
                    self.assertIn('<main><h1>Methodology</h1><p>Draft recipe edition; candidate, not released.</p></main>',html)
                else:
                    self.assertIn(f'data-edition="{editions[-1]["edition"]}" selected',groups['Earlier drafts'])
                    self.assertIn('../../dashboard.html#review-queue',html)

    def test_without_promotion_original_dashboard_remains_default(self):
        with TemporaryDirectory() as tmp:
            site=Path(tmp);editions,_=self.prepare(site,available=False)
            self.publish(site,editions,None)
            self.assertEqual((site/'index.html').read_bytes(),(site/'dashboard.html').read_bytes())
            for name in ('index.html','dashboard.html','legacy.html'):
                html=(site/name).read_text()
                self.assertIn(' selected>Evidence dashboard · 10 Nov 2026</option>',html)
                self.assertNotIn('aria-label="Superseded dashboard"',html)

    def test_missing_or_unlisted_default_stops_publication(self):
        for problem in ('missing','private','noindex'):
            with self.subTest(problem=problem),TemporaryDirectory() as tmp:
                site=Path(tmp);editions,reference=self.prepare(site,problem!='missing')
                if problem=='private':(site/'reference/NOT-FOR-PUBLICATION.txt').write_text('Blocked')
                if problem=='noindex':
                    path=site/'reference/help.html';path.write_text(path.read_text().replace('</head>','<meta name="robots" content="noindex"></head>'))
                with self.assertRaisesRegex(ValueError,'Default Methodology'):
                    self.publish(site,editions,reference)
                self.assertFalse((site/'index.html').exists())

    def test_reference_markup_changes_cannot_silently_leave_stale_navigation(self):
        with TemporaryDirectory() as tmp:
            site=Path(tmp);editions,reference=self.prepare(site)
            (site/'reference/help.html').write_text('<html><head></head><body>Missing menu</body></html>')
            with self.assertRaisesRegex(ValueError,'shared navigation'):
                self.publish(site,editions,reference)
