"""Compose the versioned review component into the dashboard host at publication time."""
import argparse
from datetime import date
from hashlib import sha256
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
FRAGMENTS = ('workspace', 'gap-dialog', 'submission-dialogs')


def runtime_files(root=ROOT):
    """Only component runtime content determines its release, not the dashboard or data."""
    return {str(p.relative_to(root)): sha256(p.read_bytes()).hexdigest()
            for p in sorted(root.rglob('*')) if p.is_file()
            and p.suffix in {'.js', '.css', '.html', '.json'} and p.name != 'release.json'}


def content_hash(files):
    return sha256(json.dumps(files, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def read_release(root=ROOT):
    release = json.loads((root / 'release.json').read_text())
    if not re.fullmatch(r'\d+\.\d+\.\d+', release['version']):
        raise ValueError('Review release must use major.minor.patch')
    date.fromisoformat(release['date'])
    if not release['notes'] or not all(isinstance(note, str) and note.strip() for note in release['notes']):
        raise ValueError('Review release needs change notes')
    files = runtime_files(root)
    if release['files'] != files or release['content_sha256'] != content_hash(files):
        raise ValueError('Review component changed without a matching release. Stamp a new version before publication.')
    return release


def stamp(version, released, notes, root=ROOT):
    if not re.fullmatch(r'\d+\.\d+\.\d+', version):
        raise ValueError('Review release must use major.minor.patch')
    date.fromisoformat(released)
    if not notes or any(not note.strip() for note in notes):
        raise ValueError('Review release needs change notes')
    prior_path = root / 'release.json'
    history = []
    if prior_path.exists():
        prior = json.loads(prior_path.read_text())
        if tuple(map(int, version.split('.'))) <= tuple(map(int, prior['version'].split('.'))):
            raise ValueError('New review version must be greater than the previous version')
        history = [{key: prior[key] for key in ('version', 'date', 'notes', 'content_sha256')}, *prior.get('history', [])]
    files = runtime_files(root)
    release = dict(version=version, date=released, notes=notes, files=files,
                   content_sha256=content_hash(files), history=history)
    prior_path.write_text(json.dumps(release, indent=2) + '\n')
    return release


def compose(html, root=ROOT):
    """Require exactly one slot each; never silently publish a partial review UI."""
    release = read_release(root)
    public = {k: v for k, v in release.items() if k != 'files'}
    fragments = {key: (root / (key + '.html')).read_text() for key in FRAGMENTS}
    fragments['release'] = '<script type="application/json" id="review-component-release">' + json.dumps(public).replace('<', r'\u003c') + '</script>'
    fragments['build-label'] = '<div id="review-build" class="review-release-history" aria-label="Review component and evidence version"></div>'
    for name, value in fragments.items():
        marker = '<!-- REVIEW:' + name + ' -->'
        if html.count(marker) != 1:
            raise ValueError('Expected one review component slot: ' + name)
        html = html.replace(marker, value, 1)
    # Cache identity follows component content, independent of dashboard and evidence revisions.
    def asset(match):
        attr, path = match.groups()
        name = path.split('?', 1)[0].removeprefix('review/')
        if name not in release['files']:
            raise ValueError('Unversioned review asset: ' + name)
        return attr + '="review/' + name + '?v=' + release['files'][name][:16] + '"'
    html = re.sub(r'(src|href)="(review/[^"?]+\.(?:js|css)(?:\?[^\"]*)?)"', asset, html)
    return html


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest='command', required=True)
    commands.add_parser('check')
    release = commands.add_parser('stamp')
    release.add_argument('--version', required=True)
    release.add_argument('--date', default=date.today().isoformat())
    release.add_argument('--note', action='append', required=True)
    build = commands.add_parser('compose')
    build.add_argument('source', type=Path)
    build.add_argument('output', type=Path)
    args = parser.parse_args()
    if args.command == 'stamp':
        result = stamp(args.version, args.date, args.note)
        print('Review v' + result['version'] + ' · ' + result['content_sha256'][:12])
    elif args.command == 'check':
        result = read_release()
        print('Review v' + result['version'] + ': content verified')
    else:
        args.output.write_text(compose(args.source.read_text()))


if __name__ == '__main__':
    main()
