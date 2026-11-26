"""Publish discovery links without changing editions, licensing or review authority."""
import hashlib
import json
import re
from pathlib import Path

BASE = "https://ruralscan.github.io/method/"
LINK = '<link rel="describedby" type="application/json" href="' + BASE + 'discovery.json">'


def publish(site, workflow):
    site = Path(site)
    versions = json.loads((site / 'reference/version.json').read_text())
    assets = json.loads((site / 'reference/data/assets.json').read_text())
    build = json.loads((site / 'dashboard-build.json').read_text())
    refs = re.findall(r'ref: ([0-9a-f]{40})\s+path: reference-src', Path(workflow).read_text())
    if len(refs) != 1:
        raise ValueError('Expected one immutable reference checkout revision')
    coverage = assets['reviewCoverage']

    def asset(path, media):
        raw = (site / path).read_bytes()
        return {'url': BASE + path, 'mediaType': media, 'bytes': len(raw),
                'sha256': hashlib.sha256(raw).hexdigest()}

    manifest = {
        'format': 'ruralscan.discovery.v1',
        'id': BASE + 'discovery.json',
        'publicationRevision': build['revision'],
        'description': 'Entry points for independently versioned methodology, evidence, review and runtime. '
                       'Current URLs may change; use the stated revisions and checksums when citing a snapshot.',
        'methodology': {
            'url': BASE + 'reference/index.html', 'version': versions['version'],
            'sourceRepository': 'RuralScan/method', 'sourceRevision': refs[0],
            'setupGuide': BASE + 'reference/ch-system-setup.html',
            'assets': asset('reference/data/assets.json', 'application/json'),
            'agentGuide': BASE + 'reference/llms.txt',
        },
        'historicalEvidence': {
            'catalogue': BASE + 'catalog.json',
            'package': {**assets['package'], 'fieldGuide': BASE + 'reference/' + assets['package']['fieldGuide']},
            'meaning': 'Pinned historical analytical edition. Not the live register or a new scientific acceptance.',
            'accessRights': assets['accessRights'],
            'citation': assets['citation'],
        },
        'reviewCoverage': {
            'source': coverage['source'],
            'meaning': 'Pinned finding coverage and official review status; separate from the historical recipe edition. '
                       'Independent-study counts and scientific acceptance are not inferred.',
            'accessRights': assets['accessRights'],
            'browse': BASE + 'reference/evidence-findings.html',
            'distributions': [asset('reference/' + coverage[key], media) for key, media in (
                ('counts', 'application/json'), ('csv', 'text/csv'), ('findings', 'application/json'))],
            'definitions': coverage['definitions'],
        },
        'reviewWorkspace': {
            'url': BASE + 'dashboard.html#review-queue',
            'sourceRepository': 'RuralScan/method', 'sourceRevision': build['revision'],
            'componentVersion': build['review_release'],
            'documentation': 'https://github.com/RuralScan/method/blob/' + build['revision'] + '/review/README.md',
            'liveDecisionAuthority': 'RuralScan/evidence',
        },
        'officialRegisters': {
            'repository': 'https://github.com/RuralScan/evidence',
            'currentQueue': 'https://raw.githubusercontent.com/RuralScan/evidence/main/publication/review-queue.json',
            'currentManifest': 'https://raw.githubusercontent.com/RuralScan/evidence/main/registers/manifest.json',
            'submissions': 'https://github.com/RuralScan/evidence/blob/main/workflows/submissions/README.md',
            'meaning': 'Moving operational pointers. Read their revision before joining or citing. CIAT is historical provenance, not a live writer.',
        },
        'runtime': {
            'repository': 'https://github.com/RuralScan/runtime',
            'meaning': 'Separately maintained software. This index does not pin or approve a runtime release.',
        },
        'reuse': {
            'dataLicenceStatus': 'awaiting confirmation',
            'archiveStatus': 'not selected',
            'meaning': 'Public access is not a reuse licence. Software licences do not grant rights to quoted publications or third-party source material.',
        },
    }
    (site / 'discovery.json').write_text(json.dumps(manifest, indent=2) + '\n')
    (site / 'llms.txt').write_text(
        '# Rural NbS Scan\n\n'
        'Scoping methodology, evidence records and human review. Start with discovery.json.\n\n'
        + '\n'.join(f'- [{label}]({BASE + path})' for label, path in (
            ('Machine-readable discovery and versions', 'discovery.json'),
            ('Methodology and setup', 'reference/ch-system-setup.html'),
            ('Methodology data and field definitions', 'reference/llms.txt'),
            ('Historical evidence catalogue', 'catalog.json'),
            ('Current review workspace', 'dashboard.html#review-queue'))) + '\n\n'
        'RuralScan/evidence owns live decisions and registers; CIAT records are historical. '
        'Review coverage, historical analytical tables and runtime have separate revisions. '
        'Extracted-data reuse licence and durable archive remain unconfirmed.\n'
    )
    for name in ('index.html', 'reference/index.html', 'dashboard.html'):
        path = site / name
        text = path.read_text()
        if '</head>' not in text:
            raise ValueError(f'Missing discovery insertion point: {name}')
        if LINK not in text:
            path.write_text(text.replace('</head>', LINK + '</head>', 1))
    return manifest
