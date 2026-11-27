"""Verify the bounded carbon/Naturebase handover without network or raster dependencies."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest_entries(record):
    if isinstance(record.get('files'), list):
        return {item['file']: item['sha256'] for item in record['files']}
    return record


def main():
    directories = sorted(ROOT.glob('*audit-20261126'))
    assert len(directories) == 8, 'Review the bounded audit inventory if adding a new inspection'
    inputs = ROOT / 'haiti-diagnostic-inputs-20261126'
    checked = 0
    for directory in [*directories, inputs]:
        manifest = json.loads((directory / 'manifest.json').read_text())
        for name, expected in manifest_entries(manifest).items():
            assert digest(directory / name) == expected, str(directory / name)
            checked += 1
        verifier = directory / 'verify_audit.py'
        if verifier.exists():
            subprocess.run([sys.executable, str(verifier)], check=True)
    points = json.loads((inputs / 'stratified_points.geojson').read_text())['features']
    assert len(points) == len({point['id'] for point in points}) == 1440
    classes = {point['properties']['landcover'] for point in points}
    assert len(classes) == 9
    assert all(sum(point['properties']['landcover'] == cls for point in points) == 160 for cls in classes)
    carbon = json.loads((ROOT / 'carbon-loss-audit-20261126/manifest.json').read_text())
    assert digest(inputs / 'boundary.json') == carbon['original_boundary_snapshot_sha256']
    soil = json.loads((ROOT / 'crop-soil-components-audit-20261126/soil_raster_checks.json').read_text())
    assert digest(inputs / 'boundary.json') == soil['boundary_sha256']
    assert digest(inputs / 'stratified_points.geojson') == soil['points_sha256']
    # Probe compilation checks syntax only; it does not run downloaded code or fetch data.
    for directory in directories:
        for script in directory.glob('*.py'):
            compile(script.read_text(), str(script), 'exec')
    documents = [ROOT / 'README.md', ROOT / 'THIRD_PARTY_NOTICES.md',
                 ROOT / '2026-11-26-handover-brayden-diego.md', inputs / 'README.md',
                 *ROOT.glob('2026-11-26-naturebase-*.md'),
                 ROOT / '2026-11-26-carbon-loss-followup.md',
                 ROOT / '2026-11-26-carbon-loss-classes.md',
                 ROOT / '2026-11-26-crop-soil-components.md',
                 *(directory / 'README.md' for directory in directories)]
    links = 0
    for document in documents:
        for target in re.findall(r'\]\(([^)]+)\)', document.read_text()):
            if '://' in target or target.startswith(('#', 'mailto:')):
                continue
            path = target.split('#')[0]
            assert (document.parent / path).exists(), (str(document), target)
            links += 1
    print(f'PASS: {len(directories)} audits; {checked} hashes; shared 1,440-point inputs; '
          f'probe syntax; {links} local links. No scientific acceptance or runtime activation inferred.')


if __name__ == '__main__':
    main()
