import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from html.parser import HTMLParser

from publish_discovery import publish, BASE


class Links(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.describedby = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'link' and attrs.get('rel') == 'describedby':
            self.describedby.append(attrs['href'])


class Discovery(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.site = Path(self.tmp.name)
        (self.site / 'reference/data').mkdir(parents=True)
        for name in ('index.html', 'reference/index.html', 'dashboard.html'):
            (self.site / name).write_text('<html><head></head><body>Keep existing finding routes</body></html>')
        (self.site / 'reference/version.json').write_text(json.dumps({'version': '0.26.0'}))
        (self.site / 'dashboard-build.json').write_text(json.dumps({'revision': 'a'*40, 'review_release': '1.0.0'}))
        self.workflow = self.site / 'workflow.yml'
        self.workflow.write_text('ref: ' + 'b'*40 + '\n          path: reference-src\n')
        self.coverage = {
            'source': {'revision': 'c'*40}, 'definitions': {'retained': 'kept + pending + held'},
            'counts': 'data/review-coverage.json', 'csv': 'data/review-coverage.csv',
            'findings': 'data/review-findings.json',
        }
        self.assets = {'reviewCoverage': self.coverage,
                       'package': {'edition': 'historical', 'fieldGuide': 'data-guide.html'},
                       'accessRights': 'Public access; licence unconfirmed.', 'citation': 'Historical edition citation'}
        (self.site / 'reference/data/assets.json').write_text(json.dumps(self.assets))
        for name in ('counts', 'csv', 'findings'):
            (self.site / 'reference' / self.coverage[name]).write_text('fixture-' + name)
        (self.site / 'catalog.json').write_text('{"historical":true}')

    def test_fresh_client_discovers_versions_data_and_writer_without_javascript(self):
        catalog_before = (self.site / 'catalog.json').read_bytes()
        m = publish(self.site, self.workflow)
        self.assertEqual(Links((self.site / 'index.html').read_text()).describedby, [BASE+'discovery.json'])
        discovered = json.loads((self.site / 'discovery.json').read_text())
        self.assertEqual(discovered, m)
        self.assertEqual(m['methodology']['version'], '0.26.0')
        self.assertEqual(m['methodology']['sourceRevision'], 'b'*40)
        self.assertEqual(m['reviewCoverage']['source']['revision'], 'c'*40)
        self.assertEqual(m['reviewWorkspace']['sourceRevision'], 'a'*40)
        self.assertEqual(m['reviewWorkspace']['liveDecisionAuthority'], 'RuralScan/evidence')
        self.assertEqual(m['historicalEvidence']['package']['edition'], 'historical')
        self.assertEqual(m['historicalEvidence']['package']['fieldGuide'], BASE+'reference/data-guide.html')
        for a in [m['methodology']['assets']] + m['reviewCoverage']['distributions']:
            raw = (self.site / a['url'].removeprefix(BASE)).read_bytes()
            self.assertEqual(a['bytes'], len(raw))
            self.assertEqual(a['sha256'], hashlib.sha256(raw).hexdigest())
        self.assertEqual(catalog_before, (self.site / 'catalog.json').read_bytes())
        self.assertEqual(m['reuse']['dataLicenceStatus'], 'awaiting confirmation')
        self.assertNotIn('license', m)
        self.assertNotIn('version', m['runtime'])
        self.assertIn('discovery.json', (self.site / 'llms.txt').read_text())

    def test_repeat_publication_does_not_duplicate_links_or_change_routes(self):
        publish(self.site, self.workflow)
        before = (self.site / 'discovery.json').read_bytes()
        publish(self.site, self.workflow)
        self.assertEqual(before, (self.site / 'discovery.json').read_bytes())
        for name in ('index.html', 'reference/index.html', 'dashboard.html'):
            html = (self.site / name).read_text()
            self.assertEqual(len(Links(html).describedby), 1)
            self.assertIn('Keep existing finding routes', html)

    def test_missing_asset_or_unpinned_reference_blocks_publication(self):
        (self.site / 'reference' / self.coverage['csv']).unlink()
        with self.assertRaises(FileNotFoundError):
            publish(self.site, self.workflow)
        self.workflow.write_text('ref: main\npath: reference-src\n')
        with self.assertRaisesRegex(ValueError, 'immutable reference'):
            publish(self.site, self.workflow)


if __name__ == '__main__':
    unittest.main()
