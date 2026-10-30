"""Behavioral tests for local fixture preparation; no model evaluation."""

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from scripts.prepare_eval import prepare


class PrepareEvalTests(unittest.TestCase):
    def setUp(self):
        # Stay inside the writable checkout; clean up each isolated test root.
        self.temp = tempfile.TemporaryDirectory(
            prefix='yap-free-eval-test-', dir=Path(__file__).resolve().parent)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.package = self.root / 'package'
        for name, text in {
            'SKILL.md': 'root skill', 'references/core.md': 'shared rules',
            'skills/yap-free-ui/SKILL.md': 'ui skill', '.claude-plugin/plugin.json': '{}',
            'README.md': 'not an instruction', '.git/config': 'PRIVATE_GIT',
            '.env': 'PRIVATE_SECRET', 'evals/cases.json': 'PRIVATE_ORACLE',
            'user-files/private.txt': 'PRIVATE_USER',
        }.items():
            path = self.package / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding='utf-8')
        self.cases = self.root / 'cases.json'
        self.out = self.root / 'batch'
        self.case = {
            'id': 'example', 'mode': 'fix', 'entry': 'ui',
            'turns': ['Fix the screen.', 'Keep the error details.'],
            'files': {'src/screen.txt': 'hello\n'},
            'oracle': {'preserve': ['ORACLE_PRESERVE'], 'change': ['ORACLE_CHANGE'],
                       'forbidden': ['ORACLE_FORBIDDEN']},
        }

    def run_prepare(self, cases=None, variant='candidate'):
        self.cases.write_text(json.dumps([self.case] if cases is None else cases), encoding='utf-8')
        return prepare(self.cases, self.package, self.out, variant)

    def test_no_oracle_leak(self):
        paths = self.run_prepare()
        self.assertEqual(paths, [self.out / 'example'])
        case = paths[0]
        copied = {p.relative_to(case / 'plugin').as_posix() for p in (case / 'plugin').rglob('*') if p.is_file()}
        self.assertEqual(copied, {'SKILL.md', 'references/core.md', 'skills/yap-free-ui/SKILL.md', '.claude-plugin/plugin.json'})
        for path in case.rglob('*'):
            if path.is_file():
                content = path.read_text(encoding='utf-8')
                for marker in ['ORACLE_PRESERVE', 'ORACLE_CHANGE', 'ORACLE_FORBIDDEN', 'PRIVATE_']:
                    self.assertNotIn(marker, content)
        self.assertEqual((case / 'workspace/src/screen.txt').read_bytes(), b'hello\n')
        self.assertEqual(json.loads((case / 'before.json').read_text()), {
            'src/screen.txt': '5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03'})
        self.assertEqual(list((case / 'outputs').iterdir()), [])

    def test_reject_traversal_and_absolute_fixture(self):
        for name in ['../outside.txt', '/absolute.txt', 'C:/absolute.txt', r'C:\absolute.txt',
                     r'..\outside.txt', r'\\server\share\x', 'x/../escape', 'C:drive.txt',
                     'x:stream', 'CON', 'file.', 'file ', 'x//y']:
            with self.subTest(name=name):
                self.case['files'] = {name: 'unsafe'}
                with self.assertRaises(ValueError):
                    self.run_prepare()
                self.assertFalse(self.out.exists())

    def test_refuse_existing_output(self):
        self.out.mkdir()
        marker = self.out / 'keep.txt'
        marker.write_text('unchanged', encoding='utf-8')
        with self.assertRaises((ValueError, FileExistsError)):
            self.run_prepare()
        self.assertEqual(marker.read_text(), 'unchanged')
        self.assertEqual(list(self.out.iterdir()), [marker])

    def test_first_turn_only_and_selected_entry(self):
        case = self.run_prepare()[0]
        turns = json.loads((case / 'turns.json').read_text())
        self.assertIn(str((case / 'plugin/skills/yap-free-ui/SKILL.md').resolve()), turns[0])
        self.assertTrue(turns[0].endswith(self.case['turns'][0]))
        self.assertEqual(turns[1:], self.case['turns'][1:])
        self.assertEqual((case / 'prompt.txt').read_text(), turns[0])

    def test_legacy_uses_root_skill(self):
        case = self.run_prepare(variant='legacy')[0]
        prompt = (case / 'prompt.txt').read_text()
        self.assertIn(str((case / 'plugin/SKILL.md').resolve()), prompt)
        self.assertNotIn(str((case / 'plugin/skills/yap-free-ui/SKILL.md').resolve()), prompt)

    def test_none_has_raw_turns_and_no_plugin(self):
        case = self.run_prepare(variant='none')[0]
        self.assertFalse((case / 'plugin').exists())
        self.assertEqual(json.loads((case / 'turns.json').read_text()), self.case['turns'])
        self.assertEqual((case / 'prompt.txt').read_text(), self.case['turns'][0])

    def test_case_ids_and_fixture_collisions_are_rejected(self):
        for files in [{'A.txt': 'one', 'a.txt': 'two'}, {'A/x': 'one', 'a/y': 'two'},
                      {'a': 'one', 'a/b': 'two'}]:
            with self.subTest(files=files):
                self.case['files'] = files
                with self.assertRaises(ValueError):
                    self.run_prepare()
                self.assertFalse(self.out.exists())
        for case_id in ['../escape', 'a/b', 'NUL', 'trailing.', '']:
            with self.subTest(case_id=case_id):
                self.case['id'] = case_id
                with self.assertRaises(ValueError):
                    self.run_prepare()
        second = copy.deepcopy(self.case)
        self.case['id'], second['id'] = 'EXAMPLE', 'example'
        self.case['files'], second['files'] = {}, {}
        with self.assertRaises(ValueError):
            self.run_prepare([self.case, second])

    def test_invalid_schema_is_rejected_before_output(self):
        for field, value in [('mode', 'edit'), ('entry', 'web'), ('entry', []), ('turns', []),
                             ('turns', [1]), ('files', {'x': 1}), ('oracle', {}),
                             ('oracle', {'preserve': [], 'change': [], 'forbidden': [1]})]:
            with self.subTest(field=field, value=value):
                case = copy.deepcopy(self.case)
                case[field] = value
                with self.assertRaises(ValueError):
                    self.run_prepare([case])
                self.assertFalse(self.out.exists())
        with self.assertRaises(ValueError):
            self.run_prepare({'cases': [self.case]})

    def test_symlink_package_content_is_rejected(self):
        outside = self.root / 'external-secret.txt'
        outside.write_text('EXTERNAL_SECRET', encoding='utf-8')
        try:
            (self.package / 'references/link.md').symlink_to(outside)
        except OSError as error:
            self.skipTest(f'Host cannot create symlinks: {error}')
        with self.assertRaises(ValueError):
            self.run_prepare()
        self.assertFalse(self.out.exists())

    def test_core_candidate_uses_root_skill(self):
        self.case['entry'] = 'core'
        case = self.run_prepare()[0]
        self.assertIn(str((case / 'plugin/SKILL.md').resolve()), (case / 'prompt.txt').read_text())

    def test_duplicate_json_keys_are_rejected(self):
        self.cases.write_text('[{"id": "one", "id": "two"}]', encoding='utf-8')
        with self.assertRaises(ValueError):
            prepare(self.cases, self.package, self.out, 'none')
        self.assertFalse(self.out.exists())

    def test_nested_excluded_package_content_is_rejected(self):
        secret = self.package / 'references/.env'
        secret.write_text('PRIVATE_SECRET', encoding='utf-8')
        with self.assertRaises(ValueError):
            self.run_prepare()
        self.assertFalse(self.out.exists())

    def test_missing_selected_entry_is_rejected(self):
        self.case['entry'] = 'cli'
        with self.assertRaises(ValueError):
            self.run_prepare()
        self.assertFalse(self.out.exists())

    def test_cli_success_and_failure(self):
        self.cases.write_text(json.dumps([self.case]), encoding='utf-8')
        command = [sys.executable, '-B', str(Path(__file__).resolve().parents[1] / 'scripts/prepare_eval.py'),
                   '--cases', str(self.cases), '--package', str(self.package),
                   '--out', str(self.out), '--variant', 'none']
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), str(self.out / 'example'))
        failed = subprocess.run(command, capture_output=True, text=True)
        self.assertNotEqual(failed.returncode, 0)
        self.assertTrue(failed.stderr.strip())


if __name__ == '__main__':
    unittest.main()
