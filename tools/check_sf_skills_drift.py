#!/usr/bin/env python3
"""Check the approved Salesforce sf-skills Data 360 companion subset.

The checker reads only the nine skills named by the Beast contract, keeps the
upstream bodies in a temporary directory, and emits public-safe metadata. It
never vendors upstream content into this repository.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import tempfile
import urllib.request
import zipfile
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs" / "data360" / "sf-skills-data360-companion.json"
REPO = "forcedotcom/sf-skills"
ARCHIVE = "https://github.com/forcedotcom/sf-skills/archive/{ref}.zip"


def load_contract() -> dict:
    return json.loads(CONTRACT.read_text(encoding="utf-8"))


def approved_names(contract: dict) -> list[str]:
    return [item["upstreamName"] for item in contract.get("companionSkills", [])]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def classify(paths: list[str], changed_text: str) -> list[str]:
    value = " ".join(paths) + " " + changed_text
    categories: list[str] = []
    patterns = {
        "install": r"package\.json|install|destination|archive|manifest",
        "routing": r"phase|route|when to use|scope|workflow",
        "command behavior": r"sf data360|command|subcommand|flag|argument|--[a-z-]+",
        "templates": r"template|payload|example|request|response",
        "readiness": r"readiness|preflight|permission|auth|credential|status|health",
        "gotchas": r"gotcha|troubleshoot|error|warning|limitation|caveat",
    }
    for category, pattern in patterns.items():
        if re.search(pattern, value, re.IGNORECASE):
            categories.append(category)
    return categories or ["content"]


def fetch_archive(ref: str, destination: Path) -> Path:
    archive = destination / "sf-skills.zip"
    request = urllib.request.Request(
        ARCHIVE.format(ref=ref),
        headers={"User-Agent": "data360beast-docs-watch"},
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        archive.write_bytes(response.read())
    return archive


def fetch_ref_metadata(ref: str) -> dict:
    result = subprocess.run(
        ["git", "ls-remote", f"https://github.com/{REPO}.git", f"refs/heads/{ref}"],
        text=True,
        capture_output=True,
        timeout=60,
        check=False,
    )
    if result.returncode or not result.stdout.strip():
        raise RuntimeError(f"could not resolve upstream ref {ref}: {result.stderr.strip()}")
    return {"sha": result.stdout.split()[0], "date": None}


def inspect_upstream(ref: str, contract: dict) -> dict:
    names = approved_names(contract)
    with tempfile.TemporaryDirectory(prefix="data360beast-sf-skills-watch-") as raw:
        root = Path(raw)
        archive = fetch_archive(ref, root)
        with zipfile.ZipFile(archive) as zipped:
            zipped.extractall(root / "extract")
        package_roots = [item for item in (root / "extract").iterdir() if item.is_dir()]
        if len(package_roots) != 1:
            raise RuntimeError("unexpected sf-skills archive layout")
        source_root = package_roots[0]
        files: dict[str, dict[str, object]] = {}
        missing: list[str] = []
        for name in names:
            skill_root = source_root / "skills" / name
            skill_file = skill_root / "SKILL.md"
            if not skill_file.is_file():
                missing.append(name)
                continue
            for path in sorted(skill_root.rglob("*")):
                if path.is_file():
                    rel = path.relative_to(source_root).as_posix()
                    files[rel] = {
                        "sha256": sha256(path),
                        "bytes": path.stat().st_size,
                    }
        if missing:
            raise RuntimeError("upstream archive missing approved skills: " + ", ".join(missing))

        package = {}
        package_path = source_root / "package.json"
        if package_path.is_file():
            package = json.loads(package_path.read_text(encoding="utf-8"))
        metadata = fetch_ref_metadata(ref)
        return {
            "repository": f"https://github.com/{REPO}",
            "ref": ref,
            "commit": metadata.get("sha"),
            "date": metadata.get("date"),
            "packageName": package.get("name"),
            "packageVersion": package.get("version"),
            "skills": names,
            "files": files,
        }


def compare(observed: dict, contract: dict) -> dict:
    upstream = contract.get("upstream", {})
    old_files = contract.get("observedFiles", {})
    changed = sorted(
        set(old_files) | set(observed["files"])
        - {key for key in set(old_files) & set(observed["files"])
           if old_files[key].get("sha256") == observed["files"][key].get("sha256")}
    )
    # The expression above is intentionally normalized below for readability
    # and to avoid treating unchanged files as drift.
    changed = sorted(
        key for key in set(old_files) | set(observed["files"])
        if old_files.get(key, {}).get("sha256") != observed["files"].get(key, {}).get("sha256")
    )
    changed_text = " ".join(changed)
    categories = classify(changed, changed_text)
    package_changed = (
        upstream.get("packageName") != observed.get("packageName")
        or upstream.get("observedPackageVersion") != observed.get("packageVersion")
    )
    if package_changed and "install" not in categories:
        categories.insert(0, "install")
    return {
        "changed": bool(changed or package_changed),
        "changedFiles": changed,
        "categories": categories if (changed or package_changed) else [],
        "packageChanged": package_changed,
        "observed": observed,
        "previous": {
            "ref": upstream.get("observedRef"),
            "packageVersion": upstream.get("observedPackageVersion"),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", default="main")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    contract = load_contract()
    observed = inspect_upstream(args.ref, contract)
    result = compare(observed, contract)
    result["approvedSkills"] = approved_names(contract)
    result["source"] = f"https://github.com/{REPO}/tree/{args.ref}/skills"
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
