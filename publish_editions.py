"""Rebuild every shared dashboard edition, then leave the latest at the site root."""
import json
from pathlib import Path
import re
import subprocess
import sys
from tempfile import TemporaryDirectory


def git(repo, *args):
    subprocess.run(["git", "-C", str(repo), *args], check=True)


def repository(parent, name, remote):
    repo = parent / name
    repo.mkdir()
    git(repo, "init", "--quiet")
    git(repo, "remote", "add", "origin", "https://github.com/" + remote + ".git")
    git(repo, "config", "remote.origin.promisor", "true")
    git(repo, "config", "remote.origin.partialclonefilter", "blob:none")
    return repo


def fetch(repo, revision):
    if not re.fullmatch("[0-9a-f]{40}", revision):
        raise ValueError(f"Expected full commit: {revision}")
    exists = subprocess.run(["git", "-C", str(repo), "cat-file", "-e", revision + "^{commit}"],
                            stderr=subprocess.DEVNULL).returncode == 0
    if not exists:
        git(repo, "fetch", "--no-tags", "--depth=1", "--filter=blob:none", "origin", revision)


def main():
    site = Path("site").resolve()
    ciat = Path("producer").resolve()
    with TemporaryDirectory() as tmp:
        method = repository(Path(tmp), "method", "RuralScan/method")
        evidence = repository(Path(tmp), "evidence", "RuralScan/evidence")
        for edition in json.loads(Path("editions.json").read_text()):
            fetch(method, edition["method"])
            git(method, "checkout", "--quiet", "--detach", edition["method"])
            fetch(evidence, edition["evidence"])
            fetch(ciat, edition["producer"])
            fetch(ciat, edition["progress"])
            target = site / "editions" / edition["edition"]
            if target.exists():
                raise ValueError(f"Repeated edition: {target}")
            subprocess.run([sys.executable, "-B", str(method/"dashboard/build.py"),
                            "--out", str(site), "--evidence", str(evidence), "--ciat", str(ciat)], check=True)
            subprocess.run([sys.executable, "-B", str(method/"dashboard/check.py"), str(target)], check=True)


if __name__ == "__main__":
    main()
