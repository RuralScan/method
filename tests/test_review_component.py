"""Release isolation, complete composition and fail-closed publication."""
from html.parser import HTMLParser
from pathlib import Path
import re
import shutil
from tempfile import TemporaryDirectory
import unittest

from review import build

HOST = build.ROOT.parent / 'dashboard.html'
NEXT_VERSION = '.'.join([*build.read_release()['version'].split('.')[:2], str(int(build.read_release()['version'].split('.')[2]) + 1)])


class Tags(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.tags = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        self.tags.append((tag, dict(attrs)))


class ReviewComponentTest(unittest.TestCase):
    def test_complete_host_contains_one_component_and_real_versioned_assets(self):
        html = build.compose(HOST.read_text())
        tags = Tags(html).tags
        for id in ['tab-qaqc', 'vf-sidebar', 'vf-cards', 'finding-submission', 'review-batch', 'gap-modal', 'review-build', 'review-component-release']:
            self.assertEqual(sum(attrs.get('id') == id for _, attrs in tags), 1, id)
        self.assertNotIn('<!-- REVIEW:', html)
        self.assertNotIn('function renderVfWorklist', html)
        assets = [attrs.get('src', '') for tag, attrs in tags if tag == 'script']
        assets += [attrs.get('href', '') for tag, attrs in tags if tag == 'link']
        release = build.read_release()
        for asset in [x for x in assets if x.startswith('review/') and re.search(r'\.(js|css)(\?|$)', x)]:
            name, query = asset.removeprefix('review/').split('?')
            self.assertEqual(query, 'v=' + release['files'][name][:16])
            self.assertTrue((build.ROOT / name).is_file())
        self.assertLess(html.index('src="review/workspace.js'), html.index('src="dashboard-shell.js'))
        self.assertLess(html.index('id="review-batch"'), html.index('src="review/submission.js'))

    def test_missing_or_duplicate_slot_refuses_publication(self):
        host = HOST.read_text()
        for kind in ['workspace', 'release', 'build-label', 'gap-dialog', 'submission-dialogs']:
            marker = '<!-- REVIEW:' + kind + ' -->'
            for changed in [host.replace(marker, ''), host + marker]:
                with self.subTest(kind=kind), self.assertRaisesRegex(ValueError, 'Expected one review component slot'):
                    build.compose(changed)

    def test_dashboard_changes_do_not_change_review_release_or_asset_urls(self):
        host = HOST.read_text()
        original = build.compose(host)
        changed = build.compose(host.replace('Evidence for rural nature-based solutions', 'Changed dashboard subtitle'))
        pattern = r'<script type="application/json" id="review-component-release">(.*?)</script>'
        self.assertEqual(re.search(pattern, original)[1], re.search(pattern, changed)[1])
        self.assertEqual(re.findall(r'review/[^"?]+\?v=[0-9a-f]+', original), re.findall(r'review/[^"?]+\?v=[0-9a-f]+', changed))

    def test_changed_component_requires_new_release_and_retains_history(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp) / 'review'
            shutil.copytree(build.ROOT, root)
            old = build.read_release(root)
            path = root / 'workspace.css'
            path.write_text(path.read_text() + '\n/* changed component */\n')
            with self.assertRaisesRegex(ValueError, 'changed without a matching release'):
                build.compose(HOST.read_text(), root)
            with self.assertRaisesRegex(ValueError, 'must be greater'):
                build.stamp(old['version'], old['date'], ['Fix'], root)
            new = build.stamp(NEXT_VERSION, old['date'], ['Compatible fix'], root)
            self.assertNotEqual(new['content_sha256'], old['content_sha256'])
            self.assertEqual(new['history'][0]['version'], old['version'])
            self.assertEqual(new['history'][0]['notes'], old['notes'])
            self.assertEqual(build.read_release(root), new)
            self.assertIn('"version": "' + NEXT_VERSION + '"', build.compose(HOST.read_text(), root))

    def test_added_or_removed_runtime_file_requires_release(self):
        for change in ['add', 'remove']:
            with TemporaryDirectory() as tmp:
                root = Path(tmp) / 'review'
                shutil.copytree(build.ROOT, root)
                if change == 'add':
                    (root / 'new.js').write_text('// new code')
                else:
                    (root / 'vote-drafts.js').unlink()
                with self.assertRaisesRegex(ValueError, 'changed without a matching release'):
                    build.read_release(root)

    def test_script_like_release_notes_are_escaped(self):
        with TemporaryDirectory() as tmp:
            root = Path(tmp) / 'review'
            shutil.copytree(build.ROOT, root)
            build.stamp(NEXT_VERSION, '2026-11-19', ['</script><script>alert(1)</script>'], root)
            html = build.compose(HOST.read_text(), root)
            self.assertNotIn('</script><script>alert(1)', html)
            self.assertIn(r'\u003c/script>', html)
