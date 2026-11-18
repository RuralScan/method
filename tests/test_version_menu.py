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


# What the methodology build writes beside its pages. The site takes its menu label from this.
VERSION = {"name": "Methodology", "version": "0.8.0", "date": "2026-11-18", "status": "draft"}


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
            (entry.parent / 'version.json').write_text(json.dumps(VERSION))
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
            for page in [site/'dashboard.html',site/'reference/index.html',site/'reference/row-t4-finding.html',site/'editions'/editions[-1]['edition']/'review.html']:
                html=page.read_text()
                menu=html.split('<select id="dashboard-version"',1)[1].split('>',1)[1].split('</select>',1)[0]
                groups=dict(re.findall(r'<optgroup label="([^"]+)">(.*?)</optgroup>',menu))
                self.assertEqual(list(groups),['Live','Earlier drafts'])
                self.assertNotIn('legacy.html',menu)
                self.assertNotIn('10 Nov 2026',menu)
                self.assertEqual(menu.count('Evidence dashboard'),1)
                self.assertIn('>Methodology v0.8.0 · 18 Nov 2026</option>',groups['Live'])
                self.assertIn('v0.7.0 · Human review queues and finding cards · 13 Nov 2026',groups['Earlier drafts'])
                self.assertIn('v0.1.0 · Methodology draft · 11 Nov 2026',groups['Earlier drafts'])
                self.assertEqual(menu.count(' selected'),1)
                self.assertIn('>Evidence dashboard · current',groups['Live'])
                chosen=re.search(r'<option[^>]* selected[^>]*>(.*?)</option>',menu)[1]
                if page.parent==site:
                    self.assertEqual(chosen,'Evidence dashboard · current')
                    self.assertIn('<option value="dashboard.html" selected>',groups['Live'])
                    self.assertNotIn('aria-label="Superseded dashboard"',html)
                    self.assertNotIn('Current review workspace',html)
                    self.assertNotIn('Methodology home</a>',html)
                    self.assertIn('id="dashboard-version-note" hidden></span>',html)
                    self.assertIn('id="legacy-version-routes"',html)
                    self.assertIn('name="ciat-review-snapshot" content="queue.json"',html)
                    self.assertIn('id="vf-scope"',html)
                    self.assertIn('src="dashboard-tables.js?',html)
                    self.assertIn('id="review-table-description"',html)
                    self.assertNotIn('aria-label="Review findings by table"',html)
                    header=html.split('<header class="app-header">',1)[1].split('</header>',1)[0]
                    self.assertIn('aria-label="Dashboard version and tools"',header)
                    self.assertIn('id="dashboard-version"',header)
                    bar=html.split('aria-label="Dashboard version and tools">',1)[1].split('</div>',1)[0]
                    controls=['>Version</label>','id="dashboard-version-note"','id="theme-toggle"','id="rv-toggle"','What changed? · history and feedback']
                    self.assertEqual(sorted(controls,key=bar.index),controls)
                elif page.parent.name=='reference':
                    self.assertEqual(chosen,'Methodology v0.8.0 · 18 Nov 2026')
                    route='review-t4' if page.name.startswith('row-t4-') else 'overview'
                    self.assertIn(f'<option value="../dashboard.html#{route}">Evidence dashboard · current</option>',groups['Live'])
                    self.assertIn(publish.tab_icon('methodology'),html)
                    self.assertIn('href="../dashboard.html#review-queue">Review queue</a>',html)
                    self.assertIn('<span id="dashboard-version-note">Current draft</span>',html)
                    self.assertNotIn('Under review',html)
                    self.assertIn('<main><h1>Methodology</h1><p>Draft recipe edition; candidate, not released.</p></main>',html)
                else:
                    self.assertIn(publish.tab_icon('methodology'),html)
                    self.assertIn(f'data-edition="{editions[-1]["edition"]}" selected',groups['Earlier drafts'])
                    self.assertIn('<option value="../../dashboard.html#',groups['Live'])
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

    def test_every_kind_of_page_has_a_tab_symbol_and_the_two_products_differ(self):
        self.assertNotEqual(publish.tab_icon('dashboard'),publish.tab_icon('methodology'))
        here=Path(publish.__file__).parent
        self.assertEqual((here/'dashboard.html').read_text().count(publish.tab_icon('dashboard')),1)
        self.assertEqual((here/'index.html').read_text().count(publish.tab_icon('methodology')),1)
        with TemporaryDirectory() as tmp:
            site=Path(tmp);editions,reference=self.prepare(site)
            self.publish(site,editions,reference)
            for page in site.rglob('*.html'):
                if page.name=='review.html' and page.parent==site:continue  # a redirect with no content of its own
                self.assertEqual(page.read_text().count('rel="icon"'),1,page)
            for name in ('dashboard.html','legacy.html'):
                self.assertIn(publish.tab_icon('dashboard'),(site/name).read_text())

    def test_old_address_of_the_superseded_overview_forwards_to_the_dashboard(self):
        with TemporaryDirectory() as tmp:
            site=Path(tmp);editions,reference=self.prepare(site)
            self.publish(site,editions,reference)
            html=(site/'legacy.html').read_text()
            self.assertIn('location.replace("dashboard.html" + location.search + location.hash)',html)
            self.assertIn('<a href="dashboard.html">Open the evidence dashboard</a>',html)
            self.assertNotIn('id="tab-qaqc"',html)
            for page in site.rglob('*.html'):
                self.assertNotIn('legacy.html',page.read_text(),page)

    def test_version_comes_from_the_methodology_build_and_is_never_retyped(self):
        catalog=json.loads(Path(publish.__file__).with_name('editions.json').read_text())
        reference=next(row for row in catalog if row.get('href')=='reference/index.html')
        self.assertNotIn('date',reference)
        self.assertNotIn('version',reference)
        numbers=[row['version'] for row in catalog if 'edition' in row]
        self.assertEqual(numbers,[f'0.{n}.0' for n in range(1,len(numbers)+1)])
        for source in ('publish_editions.py','index.html'):
            self.assertIsNone(re.search(r'Methodology · \d|Methodology v\d',Path(publish.__file__).with_name(source).read_text()),source)
        with TemporaryDirectory() as tmp:
            site=Path(tmp);editions,reference=self.prepare(site)
            (site/'reference/version.json').write_text(json.dumps({**VERSION,'version':'1.2.0','date':'2027-01-05','status':'released'}))
            self.publish(site,editions,reference)
            html=(site/'reference/index.html').read_text()
            self.assertIn(' selected>Methodology v1.2.0 · 05 Jan 2027</option>',html)
            self.assertIn('<span id="dashboard-version-note">Current release</span>',html)

    def test_methodology_without_a_stated_version_stops_publication(self):
        for problem in ('missing','unreadable','no number','bad status'):
            with self.subTest(problem=problem),TemporaryDirectory() as tmp:
                site=Path(tmp);editions,reference=self.prepare(site)
                path=site/'reference/version.json'
                if problem=='missing':path.unlink()
                if problem=='unreadable':path.write_text('not json')
                if problem=='no number':path.write_text(json.dumps({**VERSION,'version':'18 Nov'}))
                if problem=='bad status':path.write_text(json.dumps({**VERSION,'status':'final'}))
                with self.assertRaisesRegex(ValueError,'states no version'):
                    self.publish(site,editions,reference)
                self.assertFalse((site/'index.html').exists())

    def test_reference_markup_changes_cannot_silently_leave_stale_navigation(self):
        with TemporaryDirectory() as tmp:
            site=Path(tmp);editions,reference=self.prepare(site)
            (site/'reference/help.html').write_text('<html><head></head><body>Missing menu</body></html>')
            with self.assertRaisesRegex(ValueError,'shared navigation'):
                self.publish(site,editions,reference)
