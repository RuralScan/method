"""Promotion keeps the reference, active review workspace and old links distinct."""
import json
from pathlib import Path
import re
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import publish_editions as publish


REFERENCE = '''<html><head></head><body><header><a class="review-entry" href="https://ruralscan.github.io/method/dashboard.html#review-queue">Review queue</a><nav class="tabs" aria-label="Sections"><div class="wrap"><a href="index.html" aria-current="page"><span class="n">1</span> Overview</a><a href="method.html"><span class="n">2</span> Method</a><a href="evidence-methods.html"><span class="n">3</span> Evidence methods</a></div></nav></header>
<select id="dashboard-version" aria-describedby="dashboard-version-note"><option>Old menu</option></select>
<span id="dashboard-version-note"><b>Under review</b> Draft for approval</span>
<a class="vb-live" href="https://ruralscan.github.io/method/dashboard.html#overview">Live dashboard</a>
<noscript>Old links</noscript><main><h1>Methodology</h1><p>Draft recipe edition; candidate, not released.</p></main></body></html>'''


# What the methodology build writes beside its pages. The site takes its menu label from this.
DASHBOARD_REV = "a" * 40

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
            for name in ('index.html', 'method.html', 'evidence-methods.html', 'help.html', 'row-t4-finding.html'):
                (entry.parent / name).write_text(REFERENCE)
            (entry.parent / 'version.json').write_text(json.dumps(VERSION))
        return editions, reference

    def publish(self, site, editions, reference):
        with patch.object(publish, "dashboard_revision", return_value=DASHBOARD_REV), \
             patch.object(publish, "live_rating_reviews", return_value={}), \
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
                self.assertEqual(list(groups),['Current version','Earlier drafts'])
                self.assertNotIn('legacy.html',menu)
                self.assertNotIn('10 Nov 2026',menu)
                self.assertEqual(menu.count('Evidence dashboard'),0)
                self.assertEqual(groups['Current version'].count('<option '),1)
                self.assertIn('>Methodology v0.8.0 · 18 Nov 2026</option>',groups['Current version'])
                self.assertIn('v0.7.0 · Human review queues and finding cards · 13 Nov 2026',groups['Earlier drafts'])
                self.assertIn('v0.1.0 · Methodology draft · 11 Nov 2026',groups['Earlier drafts'])
                self.assertEqual(menu.count(' selected'),1)
                chosen=re.search(r'<option[^>]* selected[^>]*>(.*?)</option>',menu)[1]
                if page.parent==site:
                    self.assertEqual(chosen,'Methodology v0.8.0 · 18 Nov 2026')
                    self.assertIn('<option value="dashboard.html" selected data-current-workspace>',groups['Current version'])
                    self.assertNotIn('aria-label="Superseded dashboard"',html)
                    self.assertNotIn('Current review workspace',html)
                    self.assertIn('https://github.com/RuralScan/method/tree/' + DASHBOARD_REV, html)
                    history=html.split('id="dashboard-history"',1)[1].split('</section>',1)[0]
                    self.assertIn('id="review-build"',history)
                    self.assertIn('id="snapshot-history"',history)
                    self.assertIn('All dashboard changes',history)
                    self.assertIn('Feedback and reported issues',history)
                    self.assertIn('is the home of this site',history)
                    self.assertNotIn('id="review-build"',html.split('<div class="header-actions">',1)[1].split('</header>',1)[0])
                    build=json.loads((site/'dashboard-build.json').read_text())
                    self.assertEqual(build['revision'],DASHBOARD_REV)
                    self.assertEqual(build['overview_snapshot'],publish.LIVE_PIN)
                    self.assertNotIn('Methodology home</a>',html)
                    self.assertIn('id="dashboard-version-note" hidden></span>',html)
                    self.assertIn('id="legacy-version-routes"',html)
                    self.assertIn('name="ciat-review-snapshot" content="queue.json"',html)
                    self.assertIn('id="vf-scope"',html)
                    self.assertIn('src="dashboard-tables.js?',html)
                    self.assertIn('id="review-table-description"',html)
                    self.assertNotIn('aria-label="Review findings by table"',html)
                    header=html.split('<header class="app-header">',1)[1].split('</header>',1)[0]
                    self.assertNotIn('nbs-invest-logo.jpg', header)
                    self.assertNotIn('alliance-logo.png', header)
                    footer = html.split('<footer', 1)[1].split('</footer>', 1)[0]
                    self.assertIn('assets/nbs-invest-logo.jpg', footer)
                    self.assertIn('assets/alliance-logo.png', footer)
                    self.assertIn('aria-label="Dashboard version and tools"',header)
                    self.assertIn('id="dashboard-version"',header)
                    bar=html.split('aria-label="Dashboard version and tools">',1)[1].split('</div>',1)[0]
                    controls=['>Version</label>','id="dashboard-version-note"','id="theme-toggle"','id="rv-toggle"','What changed? · history and feedback']
                    self.assertEqual(sorted(controls,key=bar.index),controls)
                    nav=header.split('aria-label="Methodology sections">',1)[1].split('</nav>',1)[0]
                    self.assertIn('id="btn-methods" href="reference/method.html"><span class="n">2</span> Method</a>',nav)
                    self.assertNotIn('aria-current=',nav)
                    self.assertIn('class="methodology-home project-brand" href="reference/index.html"',header)
                    self.assertIn('src="reference/assets/nbs-rural-scan-tagline.png"',header)
                    brand = re.search(r'<h1\b[^>]*id="app-title"[^>]*>(.*?)</h1>',header,re.S)[1]
                    self.assertNotIn('<svg',brand)
                    self.assertIn('alt="NBS Rural Scan',brand)
                    tools=html.split('aria-label="Evidence workspace tools">',1)[1].split('</nav>',1)[0]
                    self.assertNotIn('Methods',tools)
                    self.assertNotIn('Overview',tools)
                    self.assertIn('id="btn-qaqc">Evidence review</button>',tools)
                    self.assertIn('id="tab-qaqc" class="tab-content active"',html)
                    self.assertIn('<script src="home-route.js?v=2"></script>',html)
                    self.assertIn('<body data-methodology-workspace',html)
                elif page.parent.name=='reference':
                    self.assertEqual(chosen,'Methodology v0.8.0 · 18 Nov 2026')
                    self.assertIn('<option value="../reference/index.html" selected>',groups['Current version'])
                    self.assertIn(publish.tab_icon('methodology'),html)
                    self.assertEqual(html.split('<main', 1)[0].count('>Review queue</a>'), 1)
                    self.assertNotIn('class="vb-live"', html)
                    self.assertIn('href="../dashboard.html#review-queue">Review queue</a>',html)
                    self.assertIn('<span id="dashboard-version-note">Current draft</span>',html)
                    self.assertNotIn('Under review',html)
                    self.assertIn('<main><h1>Methodology</h1><p>Draft recipe edition; candidate, not released.</p></main>',html)
                else:
                    self.assertIn(publish.tab_icon('methodology'),html)
                    self.assertIn(f'data-edition="{editions[-1]["edition"]}" selected',groups['Earlier drafts'])
                    self.assertIn('<option value="../../dashboard.html#',groups['Current version'])
                    self.assertIn('../../dashboard.html#review-queue',html)

    def test_reference_without_legacy_queue_link_publishes(self):
        with TemporaryDirectory() as tmp:
            site = Path(tmp)
            editions, reference = self.prepare(site)
            for page in (site / 'reference').glob('*.html'):
                page.write_text(re.sub(r'<a class="vb-live".*?</a>', '', page.read_text()))
            self.publish(site, editions, reference)
            for page in (site / 'reference').glob('*.html'):
                header = page.read_text().split('<main', 1)[0]
                self.assertEqual(header.count('>Review queue</a>'), 1, page)
            dashboard = (site / 'dashboard.html').read_text()
            self.assertIn('<span>Comment on this page</span>', dashboard)
            self.assertNotIn('<span>Review</span>', dashboard)

    def test_without_promotion_original_dashboard_remains_default(self):
        with TemporaryDirectory() as tmp:
            site=Path(tmp);editions,_=self.prepare(site,available=False)
            self.publish(site,editions,None)
            self.assertEqual((site/'index.html').read_bytes(),(site/'dashboard.html').read_bytes())
            for name in ('index.html','dashboard.html','legacy.html'):
                html=(site/name).read_text()
                self.assertIn(' selected>Evidence dashboard · 10 Nov 2026</option>',html)
                self.assertNotIn('aria-label="Superseded dashboard"',html)

    def test_missing_or_broken_methodology_navigation_stops_publication(self):
        for problem in ('missing navigation', 'missing method page'):
            with self.subTest(problem=problem),TemporaryDirectory() as tmp:
                site=Path(tmp);editions,reference=self.prepare(site)
                if problem=='missing navigation':
                    path=site/'reference/index.html'
                    path.write_text(re.sub(r'<nav.*?</nav>','',path.read_text(),flags=re.S))
                else:
                    (site/'reference/method.html').unlink()
                with self.assertRaisesRegex(ValueError,'Methodology'):
                    self.publish(site,editions,reference)
                self.assertFalse((site/'index.html').exists())

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

    def test_pages_have_tab_symbols_and_workspace_is_distinguishable(self):
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

    def test_finding_browser_noscript_download_help_survives_publication(self):
        fallback = '<noscript><p>Use the downloadable finding IDs and statuses without JavaScript.</p></noscript>'
        with TemporaryDirectory() as tmp:
            site=Path(tmp);editions,reference=self.prepare(site)
            page=site/'reference/evidence-findings.html'
            page.write_text(REFERENCE.replace('</main>',fallback+'</main>'))
            self.publish(site,editions,reference)
            html=page.read_text()
            self.assertEqual(html.count(fallback),1)
            self.assertIn('Current version',html.split('<main>',1)[0])
            self.assertIn('Current version',html.split('<noscript>',1)[1].split('</noscript>',1)[0])

    def test_content_fallback_cannot_replace_missing_navigation_fallback(self):
        with TemporaryDirectory() as tmp:
            site=Path(tmp);editions,reference=self.prepare(site)
            page=site/'reference/evidence-findings.html'
            content=REFERENCE.replace('<noscript>Old links</noscript>','')
            page.write_text(content.replace('</main>','<noscript>Finding downloads</noscript></main>'))
            with self.assertRaisesRegex(ValueError,'Expected one shared navigation element'):
                self.publish(site,editions,reference)

    def test_reference_markup_changes_cannot_silently_leave_stale_navigation(self):
        with TemporaryDirectory() as tmp:
            site=Path(tmp);editions,reference=self.prepare(site)
            (site/'reference/help.html').write_text('<html><head></head><body>Missing menu</body></html>')
            with self.assertRaisesRegex(ValueError,'shared navigation'):
                self.publish(site,editions,reference)
