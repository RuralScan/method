"""Download the published data package for this edition and verify it.

    python3 build/fetch_package.py

This is the only step that uses the network. It follows the same route a new reader would:
the edition's catalogue names the package descriptor and its digest, and the descriptor names
each table and its digest. The build then reads the local copy offline and checks every digest
again, so a changed file fails the build.
"""

import hashlib
import json
import sys
import urllib.request
from pathlib import Path

sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).resolve().parent))

import core
import review_coverage


def get(url):
    request = urllib.request.Request(
        url, headers={"User-Agent": "methodology-reference-build"}
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        return response.read()


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def main():
    review_raw = get(review_coverage.URL)
    review_coverage.verified(review_raw)
    review_coverage.CACHE.parent.mkdir(parents=True, exist_ok=True)
    review_coverage.CACHE.write_bytes(review_raw)
    print(f"Verified review coverage at {review_coverage.PIN['revision']}")
    catalog = json.loads(get(core.EDITION_CATALOG_URL))
    listed = [
        d.get("sha256")
        for dataset in catalog.get("dataset", [])
        for d in dataset.get("distribution", [])
        if d.get("contentUrl") == core.PACKAGE_URL
    ]
    if listed != [core.PACKAGE_SHA256]:
        raise SystemExit(
            f"The edition catalogue lists {listed} for the package descriptor; "
            f"this reference expects {core.PACKAGE_SHA256}."
        )
    raw = get(core.PACKAGE_URL)
    if digest(raw) != core.PACKAGE_SHA256:
        raise SystemExit("The package descriptor does not match its catalogued digest.")
    out = core.PACKAGE_DIR
    out.mkdir(parents=True, exist_ok=True)
    (out / "datapackage.json").write_bytes(raw)
    (out / "catalog.json").write_text(json.dumps(catalog, indent=1) + "\n")
    for resource in json.loads(raw)["resources"]:
        table = get(core.PACKAGE_BASE + resource["path"])
        if "sha256:" + digest(table) != resource["hash"]:
            raise SystemExit(
                f"{resource['path']} does not match the digest in the descriptor."
            )
        (out / resource["path"]).write_bytes(table)
        print(f"verified  {resource['path']}  {len(table):,} bytes")
    print(f"Package {core.PACKAGE_EDITION} saved to {out}")


if __name__ == "__main__":
    main()
