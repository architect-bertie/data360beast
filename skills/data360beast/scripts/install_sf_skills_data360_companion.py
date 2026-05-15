#!/usr/bin/env python3
"""Install the Salesforce sf-skills Data 360 companion subset.

The installer fetches selected skill directories from forcedotcom/sf-skills and
installs only the Data 360-relevant companion skills. It never writes into the
VS Code Agentforce Vibes extension package or a local node_modules package.
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
import tempfile
import urllib.request
import zipfile
from pathlib import Path

REPO = "forcedotcom/sf-skills"
ARCHIVE_URL = "https://github.com/forcedotcom/sf-skills/archive/{ref}.zip"
DEFAULT_REF = "main"

COMPANION_SKILLS = [
    "orchestrating-datacloud",
    "connecting-datacloud",
    "preparing-datacloud",
    "harmonizing-datacloud",
    "segmenting-datacloud",
    "activating-datacloud",
    "retrieving-datacloud",
    "getting-datacloud-schema",
    "developing-datacloud-code-extension",
]

FORBIDDEN_DEST_MARKERS = [
    "salesforce.salesforcedx-agentforce-vibes-2",
    "npm-afv-skills/node_modules",
    "node_modules/@salesforce/afv-skills",
]


def default_dest() -> Path:
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        return Path(codex_home).expanduser() / "skills"
    return Path.home() / ".codex" / "skills"


def reject_forbidden_dest(dest: Path) -> None:
    text = str(dest.expanduser().resolve())
    for marker in FORBIDDEN_DEST_MARKERS:
        if marker in text:
            raise SystemExit(
                "Refusing to install into a vendor-managed VS Code Vibes or "
                f"node_modules package path: {dest}"
            )


def fetch_archive(ref: str, tmpdir: Path) -> Path:
    url = ARCHIVE_URL.format(ref=ref)
    archive = tmpdir / "sf-skills.zip"
    try:
        urllib.request.urlretrieve(url, archive)
    except Exception as exc:  # pragma: no cover - network error text only
        raise SystemExit(f"Failed to download {url}: {exc}") from exc
    return archive


def extract_archive(archive: Path, tmpdir: Path) -> Path:
    extract_root = tmpdir / "extract"
    with zipfile.ZipFile(archive) as zf:
        zf.extractall(extract_root)
    roots = [p for p in extract_root.iterdir() if p.is_dir()]
    if len(roots) != 1:
        raise SystemExit("Unexpected sf-skills archive layout")
    return roots[0]


def validate_source(root: Path) -> None:
    missing = [
        skill for skill in COMPANION_SKILLS
        if not (root / "skills" / skill / "SKILL.md").is_file()
    ]
    if missing:
        raise SystemExit("Archive missing expected companion skills: " + ", ".join(missing))


def install_skills(root: Path, dest: Path, force: bool, dry_run: bool) -> int:
    existing = [skill for skill in COMPANION_SKILLS if (dest / skill).exists()]
    if existing and not force:
        print(
            "Refusing to overwrite existing skills without --force: "
            + ", ".join(existing),
            file=sys.stderr,
        )
        return 1

    if dry_run:
        for skill in COMPANION_SKILLS:
            state = "exists" if (dest / skill).exists() else "new"
            print(f"DRY RUN: would install {skill} -> {dest / skill} ({state})")
        return 0

    dest.mkdir(parents=True, exist_ok=True)
    for skill in COMPANION_SKILLS:
        source = root / "skills" / skill
        target = dest / skill
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target)
        print(f"Installed {skill} -> {target}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dest", type=Path, default=default_dest(), help="Skill install destination")
    parser.add_argument("--ref", default=DEFAULT_REF, help="forcedotcom/sf-skills ref to install")
    parser.add_argument("--dry-run", action="store_true", help="Validate upstream and print planned installs")
    parser.add_argument("--force", action="store_true", help="Overwrite existing installed companion skills")
    parser.add_argument("--list", action="store_true", help="List the approved companion skills and exit")
    args = parser.parse_args()

    if args.list:
        for skill in COMPANION_SKILLS:
            print(skill)
        return 0

    dest = args.dest.expanduser()
    reject_forbidden_dest(dest)

    print(f"Source: https://github.com/{REPO}/tree/{args.ref}/skills")
    print(f"Destination: {dest}")
    print(f"Scope: {len(COMPANION_SKILLS)} Data 360 companion skills")

    with tempfile.TemporaryDirectory(prefix="data360beast-sf-skills-") as raw_tmp:
        tmpdir = Path(raw_tmp)
        archive = fetch_archive(args.ref, tmpdir)
        root = extract_archive(archive, tmpdir)
        validate_source(root)
        return install_skills(root, dest, args.force, args.dry_run)


if __name__ == "__main__":
    raise SystemExit(main())
