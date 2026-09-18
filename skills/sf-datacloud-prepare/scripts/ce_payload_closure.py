#!/usr/bin/env python3
"""Build/check a static Python import closure without importing code or calling an org.

Supports flat modules and static packages. Dynamic imports and package resources
are not certified. The destination must be empty or owned by this helper.
"""
from __future__ import annotations

import argparse
import ast
import filecmp
import json
import os
import shutil
import sys
import tempfile
import uuid
from pathlib import Path

MARKER = '.beast-closure.json'


def local_imports(path: Path, known: set[str]) -> set[str]:
    """Legacy flat-module inspection; the closure resolver below handles packages."""
    found = set()
    for node in ast.walk(ast.parse(path.read_text())):
        if isinstance(node, ast.Import):
            found.update(alias.name.split('.')[0] for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                found.add(node.module.split('.')[0])
            if node.level:
                found.update(alias.name.split('.')[0] for alias in node.names)
    return found & known


def _inventory(source):
    modules = {}
    for path in sorted(source.rglob('*')):
        if path.is_symlink():
            raise ValueError(f'symlinks are unsupported in source: {path}')
        if path.is_file() and path.suffix == '.py':
            rel = path.relative_to(source)
            parts = list(rel.with_suffix('').parts)
            if parts[-1] == '__init__':
                parts.pop()
            name = '.'.join(parts)
            if name in modules:
                raise ValueError(f'ambiguous package/module: {name}')
            modules[name] = path
    return modules


def closure(roots, source, payload, package_name=None):
    source, payload = Path(source), Path(payload)
    if source.is_symlink() or payload.is_symlink():
        raise ValueError('source and payload roots must not be symlinks')
    source, payload = source.resolve(), payload.resolve()
    if not source.is_dir() or not payload.is_dir():
        raise ValueError('source and payload must be existing directories')
    package_name = package_name or source.name
    if not package_name.isidentifier():
        raise ValueError('package name must be one Python identifier')
    modules = _inventory(source)
    local_tops = {name.split('.')[0] for name in modules if name}
    seen, pending = set(), []

    def add(name, required=True):
        if name in modules:
            if name not in seen:
                seen.add(name)
                pending.append((name, modules[name]))
        elif not any(n.startswith(name + '.') for n in modules):
            if required:
                raise ValueError(f'unresolved local import: {package_name}.{name}')
            return False
        # Package initializers execute when a submodule is imported.
        parts = name.split('.') if name else []
        for index in range(len(parts)):
            parent = '.'.join(parts[:index])
            if parent in modules and parent not in seen:
                seen.add(parent)
                pending.append((parent, modules[parent]))
        return True

    def classify(name):
        if name == package_name:
            return '', True
        if name.startswith(package_name + '.'):
            return name[len(package_name) + 1:], True
        return name, name.split('.')[0] in local_tops

    def scan(module_name, path, root=False):
        tree = ast.parse(path.read_text(), filename=str(path))
        dynamic_names = {'__import__', 'import_module'}
        for item in ast.walk(tree):
            if isinstance(item, ast.ImportFrom) and item.module == 'importlib':
                dynamic_names.update(a.asname or a.name for a in item.names if a.name == 'import_module')
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                function = node.func
                if ((isinstance(function, ast.Name) and function.id in dynamic_names) or
                    (isinstance(function, ast.Attribute) and function.attr in {'import_module', '__import__', 'exec_module'})):
                    raise ValueError(f'unsupported dynamic import in {path}')
            if isinstance(node, ast.Import):
                for alias in node.names:
                    name, local = classify(alias.name)
                    if local:
                        add(name)
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    if root:
                        raise ValueError(f'relative imports in payload roots need a declared package: {path}')
                    package = module_name.split('.') if path.name == '__init__.py' else module_name.split('.')[:-1]
                    if node.level - 1 > len(package):
                        raise ValueError(f'relative import escapes source package: {path}')
                    if node.level > 1:
                        package = package[:-(node.level - 1)]
                    base = '.'.join(package + ([node.module] if node.module else []))
                    local = True
                else:
                    base, local = classify(node.module or '')
                if not local:
                    continue
                if base:
                    add(base)
                elif '' in modules:
                    add('')
                for alias in node.names:
                    if alias.name == '*':
                        raise ValueError(f'wildcard local import unsupported: {path}')
                    candidate = '.'.join(part for part in (base, alias.name) if part)
                    if candidate in modules or any(n.startswith(candidate + '.') for n in modules):
                        add(candidate)
                    elif not node.module:
                        raise ValueError(f'unresolved relative module: {candidate}')
                    elif base not in modules:
                        # A namespace package has no initializer that could
                        # export this as a symbol. It must resolve to a module.
                        raise ValueError(f'unresolved package import: {candidate}')
                    # from module import value may refer to a symbol, not a file.
    for root in roots:
        if not root or not all(part.isidentifier() for part in root.split('.')):
            raise ValueError('roots must be module names, not filesystem paths')
        path = payload.joinpath(*root.split('.')).with_suffix('.py')
        if not path.resolve().is_relative_to(payload) or path.is_symlink():
            raise ValueError('root escapes payload')
        scan(root, path, root=True)
    while pending:
        name, path = pending.pop()
        scan(name, path)
    return sorted(modules[name] for name in seen)


def validate_paths(source, payload, destination):
    source, payload, destination = map(Path, (source, payload, destination))
    if any(path.is_symlink() for path in (source, payload, destination)):
        raise ValueError('source, payload and destination must not be symlinks')
    src, pay, dest = source.resolve(), payload.resolve(), destination.resolve()
    # A dedicated child of payload is allowed; payload itself or any input ancestor is not.
    if src.is_relative_to(dest) or dest.is_relative_to(src) or pay.is_relative_to(dest):
        raise ValueError('closure destination overlaps source or contains payload inputs')
    lexical = Path(os.path.abspath(destination))
    lexical_payload = Path(os.path.abspath(payload))
    if lexical.is_relative_to(lexical_payload) and not dest.is_relative_to(pay):
        raise ValueError('destination symlink escapes payload')
    cursor = lexical
    while cursor != lexical_payload and cursor != cursor.parent:
        # macOS exposes these OS-owned root aliases. A user symlink with the
        # same basename elsewhere does not receive an exemption.
        if cursor.is_symlink() and cursor not in {Path('/tmp'), Path('/var')}:
            raise ValueError('destination contains a symlink component')
        cursor = cursor.parent
    if destination.exists() and not destination.is_dir():
        raise ValueError('closure destination must be a directory')
    if destination.exists() and any(p.is_symlink() for p in destination.rglob('*')):
        raise ValueError('generated directory contains a symlink')
    return src, pay, dest


def _owned_destination(destination):
    if not destination.exists() or not any(destination.iterdir()):
        return
    marker = destination / MARKER
    try:
        record = json.loads(marker.read_text())
        files = record['files']
        if (record['format'] != 'beast-python-closure/v1' or not isinstance(files, list)
                or not all(isinstance(name, str) for name in files)):
            raise ValueError()
    except (OSError, ValueError, KeyError, TypeError) as exc:
        raise ValueError('refusing to replace nonempty, unowned closure directory') from exc
    actual = {str(p.relative_to(destination)) for p in destination.rglob('*') if p.is_file()}
    if actual - set(files) - {MARKER}:
        raise ValueError('generated directory contains unowned files')
    owned_dirs = {str(parent) for name in files for parent in Path(name).parents if str(parent) != '.'}
    actual_dirs = {str(p.relative_to(destination)) for p in destination.rglob('*') if p.is_dir()}
    if actual_dirs - owned_dirs:
        raise ValueError('generated directory contains unowned directories')


def write(roots, source, payload, closure_dir, package_name=None):
    source, payload, destination = validate_paths(source, payload, closure_dir)
    package_name = package_name or destination.name
    modules = closure(roots, source, payload, package_name)
    _owned_destination(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    staged = Path(tempfile.mkdtemp(prefix='.beast-closure-', dir=destination.parent))
    backup = destination.with_name(f'.{destination.name}.backup-{uuid.uuid4().hex}')
    moved = False
    try:
        for module in modules:
            relative = module.relative_to(source)
            target = staged / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(module, target)
        record = {'format': 'beast-python-closure/v1', 'package': package_name,
                  'files': [str(p.relative_to(source)) for p in modules]}
        (staged / MARKER).write_text(json.dumps(record, indent=2) + '\n')
        # Recheck after staging; never replace newly introduced unowned files.
        _owned_destination(destination)
        if destination.exists():
            os.replace(destination, backup)
            moved = True
        try:
            os.replace(staged, destination)
        except BaseException:
            if moved:
                os.replace(backup, destination)
            raise
        if moved:
            shutil.rmtree(backup)
    finally:
        if staged.exists():
            shutil.rmtree(staged)


def drift(roots, source, payload, closure_dir, package_name=None):
    source, payload, destination = validate_paths(source, payload, closure_dir)
    modules = closure(roots, source, payload, package_name or destination.name)
    expected = {str(p.relative_to(source)): p for p in modules}
    actual = ({str(p.relative_to(destination)) for p in destination.rglob('*')
               if p.is_file() and p.name != MARKER} if destination.is_dir() else set())
    problems = [f'missing from payload: {name}' for name in sorted(expected.keys() - actual)]
    problems += [f'unreachable in payload: {name}' for name in sorted(actual - expected.keys())]
    for name in sorted(expected.keys() & actual):
        if not filecmp.cmp(expected[name], destination / name, shallow=False):
            problems.append(f'differs from source: {name}')
    if not destination.is_dir():
        problems.append('closure directory is missing')
    return problems


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, required=True)
    parser.add_argument('--payload', type=Path, required=True)
    parser.add_argument('--closure-dir', type=Path, required=True)
    parser.add_argument('--roots', nargs='+', required=True)
    parser.add_argument('--package-name', help='generated package namespace; defaults to closure directory name')
    parser.add_argument('--check', action='store_true', help='read-only drift check')
    args = parser.parse_args()
    params = (args.roots, args.source, args.payload, args.closure_dir, args.package_name)
    if args.check:
        problems = drift(*params)
        for problem in problems:
            print(problem)
        if not problems:
            print('static Python closure matches source; dynamic imports/resources are not certified')
        return int(bool(problems))
    write(*params)
    print(f'wrote generated static Python closure: {args.closure_dir}')
    return 0


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (ValueError, OSError, SyntaxError) as exc:
        print(str(exc), file=sys.stderr)
        sys.exit(2)
