# /// script
# requires-python = ">=3.12"
# dependencies = ["markdown-it-py==4.0.0", "numpy==2.4.6", "requests==2.34.2"]
# ///

"""Rebuild the family guides from pinned definitions and a verified candidate release."""

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
EVIDENCE_REVISION = "8ef5b58f5245481548ff04834c8601745d9a49f6"
EVIDENCE_URL = "https://github.com/RuralScan/evidence.git"


def evidence_tools(root, local):
    """Import the release checker from its pinned Git tree, including for a dirty local clone."""
    checkout = root / "workbench"
    subprocess.run(["git", "init", "--quiet", str(checkout)], check=True)
    origin = str(local.resolve(strict=True)) if local else EVIDENCE_URL
    for args in (
        ["fetch", "--quiet", "--no-tags", "--depth=1", origin, EVIDENCE_REVISION],
        ["checkout", "--quiet", "--detach", EVIDENCE_REVISION],
    ):
        subprocess.run(["git", *args], cwd=checkout, check=True)
    directory = checkout / "workflows" / "recipe_release"
    sys.path.insert(0, str(directory))
    import check as checker

    return checker, json.loads((directory / "pin.json").read_bytes())


def check_pages(folder, rendered):
    existing = {f.name for f in folder.iterdir() if f.suffix in {".md", ".html"}}
    if existing != rendered.keys():
        changed = sorted(existing ^ rendered.keys())
        raise ValueError("Cookbook page inventory differs: " + ", ".join(changed))
    for name, content in rendered.items():
        if (folder / name).read_bytes() != content.encode("utf-8"):
            raise ValueError(f"Cookbook page differs: {name}")


def build(root, args):
    from families import family_profiles
    from pages import pages
    from print_edition import render_edition

    checker, pin = evidence_tools(root, args.evidence_repo)
    source = root / "producer"
    store = root / "release"
    checker.snapshot(
        source,
        checker.REPOSITORY,
        pin["source_revision"],
        [
            "/src/",
            "/schema/",
            "/pipeline/t4_audit/agroforestry/importance_2026-10-21/source_weight_trees.csv",
        ],
        args.ciat_repo,
    )
    summary = checker.verify(source, store, pin, build=True)
    from nbs_ruralscan.runtime.schema_loader import load_recipe_release

    release = load_recipe_release(store, pin["release_id"])
    model, manifest = checker.load_definitions(
        root / "method", pin["method"], args.method_repo
    )
    provenance = json.loads(release.read_bytes("provenance.json"))
    if manifest["structure_version"] != provenance["schema_version"]:
        raise ValueError("Candidate and method structure versions differ")
    profiles = family_profiles(model, release)
    for practice, profile in profiles.items():
        audited = summary["practices"][practice]
        if profile["totals"] != {
            key: audited[key] for key in ("T3", "T4", "T6", "T6E")
        }:
            raise ValueError(
                f"Family and practice counts disagree with the candidate for {practice}"
            )
        families = profile["families"].values()
        for field, key in (
            ("with_options", "T4 with options"),
            ("selected", "T4 with selected function"),
            ("spatially_validated", "Spatially validated T4"),
        ):
            if sum(f[field] for f in families) != audited[key]:
                raise ValueError(
                    f"Family readiness differs from the candidate for {practice}: {key}"
                )
    rendered = pages(profiles, pin, EVIDENCE_REVISION, manifest["source_revision"])
    markdown_pages = len(rendered)
    edition_name = "rural-scan-cookbook.html"
    rendered[edition_name] = render_edition(
        rendered,
        (HERE.parent / "design" / "tables.css").read_text(encoding="utf-8"),
        (HERE / "edition.css").read_text(encoding="utf-8"),
    )
    if args.out:
        checker.write_index(args.out, rendered)
    else:
        check_pages(HERE, rendered)
    print(
        json.dumps(
            {
                "release_id": release.release_id,
                "practices": len(profiles),
                "families": sum(len(p["families"]) for p in profiles.values()),
                "family_register_entries": sum(
                    len(f["variants"])
                    for p in profiles.values()
                    for f in p["families"].values()
                ),
                "analytical_rows": sum(
                    summary["totals"][k] for k in ("T3", "T4", "T6", "T6E")
                ),
                "pages": markdown_pages,
                "print_edition": edition_name,
            },
            indent=2,
        )
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--out",
        type=Path,
        help="Write to a new directory. Default checks the published pages.",
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="Use local clones and disable network Git transfers.",
    )
    for name in ("evidence", "ciat", "method"):
        parser.add_argument(
            f"--{name}-repo",
            type=Path,
            help=f"Use pinned Git objects from a local {name} clone.",
        )
    args = parser.parse_args()
    if args.offline and not (
        args.evidence_repo and args.ciat_repo and args.method_repo
    ):
        parser.error(
            "--offline requires --evidence-repo, --ciat-repo and --method-repo"
        )
    if args.offline:
        os.environ["GIT_ALLOW_PROTOCOL"] = "file"
    os.environ["GIT_NO_REPLACE_OBJECTS"] = "1"
    # Git hooks and CI can set these to the parent project's paths. Each checkout
    # here must use its own tree and objects.
    for var in (
        "GIT_DIR",
        "GIT_COMMON_DIR",
        "GIT_WORK_TREE",
        "GIT_INDEX_FILE",
        "GIT_OBJECT_DIRECTORY",
        "GIT_ALTERNATE_OBJECT_DIRECTORIES",
    ):
        os.environ.pop(var, None)
    with TemporaryDirectory(prefix="ruralscan-cookbook-") as temp:
        build(Path(temp), args)


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, subprocess.CalledProcessError) as exc:
        sys.exit(f"Cookbook build stopped: {exc}")
