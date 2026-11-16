"""Report what has moved since this reference was last checked against it.

The reference reads three things at fixed revisions: the evidence repository's operating
procedures, the published site, and the producer repository. It also links to open plans for
routes that are not built. Any of these can move while the text stands still. This script
compares each pin with the current head and each linked plan with its current state.

It reports and never fails, unless --strict is given. It needs only Python and network access:
no checkouts, no build. Set GH_TOKEN or GITHUB_TOKEN to avoid the anonymous rate limit.

    python3 build/staleness.py            # print the report
    python3 build/staleness.py --strict   # exit 1 if anything is stale
"""

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
API = "https://api.github.com/repos/"
PLAN = re.compile(r"https://github\.com/([\w.-]+/[\w.-]+)/(issues|pull)/(\d+)")


def constant(name):
    found = re.search(
        rf'^{name} = "([0-9a-f]{{40}})"',
        (ROOT / "build/core.py").read_text(),
        re.MULTILINE,
    )
    if not found:
        raise SystemExit(f"{name} is not a full revision in build/core.py")
    return found.group(1)


def api(path):
    request = urllib.request.Request(
        API + path, headers={"Accept": "application/vnd.github+json"}
    )
    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if token:
        request.add_header("Authorization", f"Bearer {token}")
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def pin(label, repo, branch, pinned, action):
    """One line for a pinned revision: current, behind by N commits, or not on the branch."""
    try:
        compared = api(f"{repo}/compare/{pinned}...{branch}")
    except urllib.error.HTTPError as error:
        return (
            None,
            f"{label}: could not compare with {repo} {branch} (HTTP {error.code}).",
        )
    except (urllib.error.URLError, TimeoutError) as error:
        return None, f"{label}: could not reach GitHub ({error})."
    behind, ahead = compared["ahead_by"], compared["behind_by"]
    head = compared["commits"][-1]["sha"] if compared["commits"] else pinned
    if ahead:
        return True, (
            f"{label}: pinned revision {pinned[:8]} is not on {repo} {branch}. Check the pin."
        )
    if not behind:
        return False, f"{label}: current ({pinned[:8]} is the head of {repo} {branch})."
    files = sorted({f["filename"] for f in compared.get("files", [])})
    shown = ", ".join(files[:6]) + (
        f" and {len(files) - 6} more" if len(files) > 6 else ""
    )
    return True, (
        f"{label}: {behind} commit{'s' if behind != 1 else ''} behind {repo} {branch} "
        f"(pinned {pinned[:8]}, head {head[:8]}). Changed: {shown or 'no files listed'}. {action}"
    )


def plans():
    """Every issue or pull request linked from the chapters and the page builders."""
    found = {}
    for path in sorted((ROOT / "content").glob("*.md")) + sorted(
        (ROOT / "build").glob("pages_*.py")
    ):
        for repo, kind, number in PLAN.findall(path.read_text()):
            found.setdefault((repo, int(number)), set()).add(path.name)
    return found


def plan(repo, number, files):
    where = ", ".join(sorted(files))
    try:
        state = api(f"{repo}/issues/{number}")["state"]
    except urllib.error.HTTPError as error:
        return (
            None,
            f"Linked plan {repo} {number} ({where}): could not read its state (HTTP {error.code}).",
        )
    except (urllib.error.URLError, TimeoutError) as error:
        return (
            None,
            f"Linked plan {repo} {number} ({where}): could not reach GitHub ({error}).",
        )
    if state == "open":
        return False, f"Linked plan {repo} {number} ({where}): still open."
    return True, (
        f"Linked plan {repo} {number} ({where}): now {state}. The text that calls it planned "
        "is probably out of date. Re-read it against the repository and remove the link."
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    parser.add_argument(
        "--strict", action="store_true", help="exit 1 if anything is stale"
    )
    args = parser.parse_args()

    results = [
        pin(
            "Operating procedures",
            "RuralScan/evidence",
            "main",
            constant("EVIDENCE_OPERATING"),
            "Re-read content/continue-with-ai.md and the review page against the changed guides, "
            "then move EVIDENCE_OPERATING.",
        ),
        pin(
            "Published site",
            "RuralScan/method",
            "gh-pages",
            constant("SITE_REV"),
            "Re-read the review page and the overview against the changed dashboard files, "
            "then move SITE_REV.",
        ),
        pin(
            "Producer read-only marker",
            "CIAT/nbs_ruralscan",
            "main",
            constant("CIAT_RETIRED"),
            "Informational: the producer still changes outside its evidence records. Check only "
            "that .ciat-evidence-readonly is still present.",
        ),
    ]
    results += [
        plan(repo, number, files) for (repo, number), files in sorted(plans().items())
    ]

    stale = [text for state, text in results if state]
    unknown = [text for state, text in results if state is None]
    current = [text for state, text in results if state is False]
    lines = ["## Methodology reference: what has moved", ""]
    for title, group in (
        ("Stale", stale),
        ("Could not check", unknown),
        ("Current", current),
    ):
        if group:
            lines += [f"**{title}**", ""] + [f"- {text}" for text in group] + [""]
    report = "\n".join(lines)
    print(report)
    summary = os.environ.get("GITHUB_STEP_SUMMARY")
    if summary:
        with open(summary, "a") as handle:
            handle.write(report + "\n")
    if os.environ.get("GITHUB_ACTIONS"):
        for text in stale + unknown:
            print(f"::warning title=Methodology reference pin::{text}")
    return 1 if args.strict and stale else 0


if __name__ == "__main__":
    sys.exit(main())
