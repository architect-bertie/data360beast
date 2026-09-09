#!/usr/bin/env python3
"""Check a code-extension payload ships exactly the modules its entrypoint imports.

`script deploy --package-dir ./payload` ships everything under `payload/` and
nothing outside it, so any pipeline module the entrypoint imports must physically
live inside the payload. `script scan` then walks the WHOLE package directory
(not just the entrypoint) and writes every discovered third-party import into
`requirements.txt`, unpinned -- so a module that sits in the payload but is never
imported still drags its own dependencies into the packed venv (see
BEAST-PROOF-031). The fix is to copy in only the modules the entrypoint
transitively imports: its import closure.

This computes that closure by AST (no module imports dynamically, so the walk is
exact) and reports drift between the authoritative source tree and the copy that
ships in the payload. It parses `.py` files and calls no org.

Usage:
    ce_payload_closure.py --source <pkg> --payload <dir> --closure-dir <dir> \\
        --roots entrypoint adapter                # rebuild the payload copy
    ce_payload_closure.py ... --check             # CI: fail on drift, do not write
"""
from __future__ import annotations

import argparse
import ast
import filecmp
import shutil
import sys
import tempfile
from pathlib import Path


def local_imports(path: Path, known: set[str]) -> set[str]:
    """The modules `path` imports that resolve to a module in `known`.

    Covers `import x`, `from x import y`, and the `from . import x` a flat
    package falls back to; only names present in `known` are returned.
    """
    found: set[str] = set()
    for node in ast.walk(ast.parse(path.read_text())):
        if isinstance(node, ast.Import):
            found.update(alias.name.split(".")[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                found.add(node.module.split(".")[0])
            if node.level:
                found.update(alias.name.split(".")[0] for alias in node.names)
    return found & known


def closure(roots: list[str], source: Path, payload: Path) -> list[Path]:
    """The source modules the roots transitively import, in a stable order.

    Roots are the hand-written entrypoint modules under `payload`; every module
    reached from them lives under `source`.
    """
    known = {p.stem for p in source.glob("*.py")}
    seen: set[str] = set()
    stack = [
        name
        for root in roots
        for name in local_imports(payload / f"{root}.py", known)
    ]
    while stack:
        name = stack.pop()
        if name in seen:
            continue
        seen.add(name)
        stack.extend(local_imports(source / f"{name}.py", known) - seen)
    return sorted(source / f"{name}.py" for name in seen)


def write(roots: list[str], source: Path, payload: Path, closure_dir: Path) -> None:
    """Materialize the payload copy: exactly the closure, nothing else."""
    if closure_dir.exists():
        shutil.rmtree(closure_dir)
    closure_dir.mkdir(parents=True)
    for module in closure(roots, source, payload):
        shutil.copy2(module, closure_dir / module.name)


def drift(roots: list[str], source: Path, payload: Path, closure_dir: Path) -> list[str]:
    """Name every file that differs between the committed copy and a fresh build."""
    with tempfile.TemporaryDirectory() as tmp:
        fresh = Path(tmp) / "closure"
        write(roots, source, payload, fresh)

        problems: list[str] = []
        expected = {p.name for p in fresh.glob("*.py")}
        actual = (
            {p.name for p in closure_dir.glob("*.py")}
            if closure_dir.is_dir()
            else set()
        )
        problems += [f"missing from payload: {n}" for n in sorted(expected - actual)]
        problems += [f"unreachable in payload: {n}" for n in sorted(actual - expected)]
        for name in sorted(expected & actual):
            if not filecmp.cmp(fresh / name, closure_dir / name, shallow=False):
                problems.append(f"differs from source: {name}")
        return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, required=True,
                        help="authoritative package dir the closure is drawn from")
    parser.add_argument("--payload", type=Path, required=True,
                        help="dir holding the hand-written root modules")
    parser.add_argument("--closure-dir", type=Path, required=True,
                        help="dir the payload copy of the closure lives in")
    parser.add_argument("--roots", nargs="+", required=True,
                        help="root module stems under --payload (e.g. entrypoint)")
    parser.add_argument("--check", action="store_true",
                        help="verify the payload copy matches source; do not write")
    args = parser.parse_args()

    if args.check:
        problems = drift(args.roots, args.source, args.payload, args.closure_dir)
        if problems:
            print("code-ext payload is out of date; rerun without --check")
            for problem in problems:
                print(f"  {problem}")
            return 1
        print(f"payload matches source ({len(closure(args.roots, args.source, args.payload))} modules)")
        return 0

    write(args.roots, args.source, args.payload, args.closure_dir)
    print(f"wrote {args.closure_dir}: {len(closure(args.roots, args.source, args.payload))} modules")
    return 0


if __name__ == "__main__":
    sys.exit(main())
