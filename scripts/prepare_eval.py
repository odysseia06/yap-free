"""Prepare isolated text fixtures. This module never runs a model or host CLI."""

import argparse
import hashlib
import json
from pathlib import Path, PureWindowsPath
import stat
import sys


ENTRIES = {'core': 'SKILL.md', **{
    name: f'skills/yap-free-{name}/SKILL.md' for name in ('ui', 'cli', 'docs', 'ai')
}}
PACKAGE_DIRS = ('references', 'skills', '.claude-plugin')
EXCLUDED_NAMES = {'.git', 'eval', 'evals', '.aws', '.ssh', '.codex', 'credentials', 'secrets'}
RESERVED_NAMES = {'con', 'prn', 'aux', 'nul', 'conin$', 'conout$',
                  *(f'{prefix}{number}' for prefix in ('com', 'lpt') for number in '123456789¹²³')}


def _safe_parts(value):
    """Reject paths that could escape or alias another path on Windows."""
    if not isinstance(value, str) or not value or PureWindowsPath(value).drive:
        raise ValueError(f'Unsafe relative path: {value!r}')
    parts = value.replace('\\', '/').split('/')
    for part in parts:
        if (not part or part in ('.', '..') or part.endswith(('.', ' '))
                or any(ord(char) < 32 or char in '<>:"|?*' for char in part)
                or part.split('.')[0].casefold() in RESERVED_NAMES):
            raise ValueError(f'Unsafe relative path: {value!r}')
    return parts


def _claim_path(parts, names):
    for index in range(1, len(parts) + 1):
        path = '/'.join(parts[:index])
        key = path.casefold()
        kind = 'file' if index == len(parts) else 'directory'
        if key in names and (names[key] != (path, kind) or kind == 'file'):
            raise ValueError(f'Colliding path: {path}')
        names[key] = (path, kind)


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'Duplicate JSON key: {key}')
        result[key] = value
    return result


def _read_cases(cases_file):
    cases = json.loads(cases_file.read_text(encoding='utf-8'), object_pairs_hook=_unique_object)
    if not isinstance(cases, list):
        raise ValueError('Cases must be a JSON array')
    ids = set()
    validated = []
    for case in cases:
        fields = {'id', 'mode', 'entry', 'turns', 'files', 'oracle'}
        if not isinstance(case, dict) or set(case) != fields:
            raise ValueError('Each case must contain exactly id, mode, entry, turns, files, oracle')
        parts = _safe_parts(case['id'])
        if len(parts) != 1 or case['id'].casefold() in ids:
            raise ValueError(f'Case ID must be a unique safe path segment: {case["id"]!r}')
        ids.add(case['id'].casefold())
        if (case['mode'] not in ('generate', 'audit', 'fix')
                or not isinstance(case['entry'], str) or case['entry'] not in ENTRIES):
            raise ValueError('Invalid mode or entry')
        if not isinstance(case['turns'], list) or not case['turns'] or not all(isinstance(turn, str) for turn in case['turns']):
            raise ValueError('turns must be a nonempty array of strings')
        oracle = case['oracle']
        if (not isinstance(oracle, dict) or set(oracle) != {'preserve', 'change', 'forbidden'}
                or not all(isinstance(items, list) and all(isinstance(item, str) for item in items) for items in oracle.values())):
            raise ValueError('oracle must contain preserve, change, forbidden string arrays')
        if not isinstance(case['files'], dict):
            raise ValueError('files must map relative paths to UTF-8 text')
        names, files = {}, {}
        for relative, content in case['files'].items():
            parts = _safe_parts(relative)
            _claim_path(parts, names)
            if not isinstance(content, str):
                raise ValueError(f'Fixture is not text: {relative}')
            files['/'.join(parts)] = content.encode('utf-8')
        validated.append((case['id'], case['entry'], case['turns'], files))
    return validated


def _package_files(package_root):
    files, names = {}, {}

    def collect(path, relative):
        info = path.lstat()
        if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT:
            raise ValueError(f'Package links/reparse points are not allowed: {relative}')
        parts = _safe_parts(relative)
        name = parts[-1].casefold()
        if name in EXCLUDED_NAMES or name == '.env' or name.startswith('.env.'):
            raise ValueError(f'Excluded package content: {relative}')
        if path.is_dir():
            for child in sorted(path.iterdir()):
                collect(child, f'{relative}/{child.name}')
        elif path.is_file():
            _claim_path(parts, names)
            files[relative] = path.read_bytes()
        else:
            raise ValueError(f'Package content is not a regular file: {relative}')

    collect(package_root / 'SKILL.md', 'SKILL.md')
    for directory in PACKAGE_DIRS:
        path = package_root / directory
        if path.exists() or path.is_symlink():
            collect(path, directory)
    return files


def _write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('xb') as handle:
        handle.write(data)


def prepare(cases_file: Path, package_root: Path, out: Path, variant: str) -> list[Path]:
    """Validate inputs before creating a new batch; return prepared case paths."""
    if variant not in ('legacy', 'candidate', 'none'):
        raise ValueError('variant must be legacy, candidate or none')
    out = Path(out).absolute()
    package_root = Path(package_root).absolute()
    if out.exists() or out.is_symlink():
        raise FileExistsError(f'Output already exists: {out}')
    if variant != 'none' and (out.resolve() == package_root.resolve() or package_root.resolve() in out.resolve().parents):
        raise ValueError('Output must be outside the package root')
    cases = _read_cases(Path(cases_file))
    package = {} if variant == 'none' else _package_files(package_root)
    for _, entry, _, _ in cases:
        selected = 'SKILL.md' if variant == 'legacy' else ENTRIES[entry]
        if variant != 'none' and selected not in package:
            raise ValueError(f'Selected skill is missing: {selected}')
    out.mkdir(parents=True, exist_ok=False)
    paths = []
    for case_id, entry, raw_turns, files in cases:
        case_out = out / case_id
        (case_out / 'workspace').mkdir(parents=True)
        (case_out / 'outputs').mkdir()
        for relative, data in files.items():
            _write(case_out / 'workspace' / relative, data)
        turns = list(raw_turns)
        if variant != 'none':
            (case_out / 'plugin').mkdir()
            for relative, data in package.items():
                _write(case_out / 'plugin' / relative, data)
            selected = 'SKILL.md' if variant == 'legacy' else ENTRIES[entry]
            skill = (case_out / 'plugin' / selected).resolve()
            turns[0] = f'Read and explicitly use the skill at "{skill}" for this task.\n\n{turns[0]}'
        before = {relative: hashlib.sha256(data).hexdigest() for relative, data in files.items()}
        _write(case_out / 'before.json', (json.dumps(before, indent=2) + '\n').encode('utf-8'))
        _write(case_out / 'turns.json', (json.dumps(turns, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
        _write(case_out / 'prompt.txt', turns[0].encode('utf-8'))
        paths.append(case_out)
    return paths


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--cases', type=Path, required=True)
    parser.add_argument('--package', type=Path, required=True)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--variant', choices=('legacy', 'candidate', 'none'), required=True)
    args = parser.parse_args()
    try:
        paths = prepare(args.cases, args.package, args.out, args.variant)
    except (ValueError, OSError, TypeError) as error:
        print(f'Preparation failed: {error}', file=sys.stderr)
        return 1
    for path in paths:
        print(path)
    return 0


if __name__ == '__main__':
    sys.exit(main())
