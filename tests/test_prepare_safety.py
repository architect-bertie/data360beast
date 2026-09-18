"""Boundary and failure-path tests for portable prepare helpers; no live API calls."""
import contextlib
import copy
import io
import json
import os
import random
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from test_stl_prepare_helpers import bisect, builder_shape, ref_check, sample_full, fake_result
from test_ce_prepare_helpers import closure_mod, diagnostics
from stl_graph import validate_graph


class Clock:
    def __init__(self): self.now = 0
    def __call__(self): return self.now
    def sleep(self, seconds): self.now += seconds


class Api:
    """Synthetic transform resource with observable HTTP effects."""
    def __init__(self, status='ACTIVE'):
        self.current = None
        self.calls = []
        self.status = status
        self.create_error = None
        self.delete_error = False
        self.missing_identity = False
    def __call__(self, command):
        path, method = command[4], command[command.index('--method') + 1]
        body = None
        if '--body' in command:
            body = json.loads(Path(command[command.index('--body') + 1][1:]).read_text())
        self.calls.append((method, path, body))
        if path.endswith('-validation'): return fake_result(stdout='{"issues":[]}')
        if method == 'POST' and path.endswith('/data-transforms'):
            self.current = dict(body, id='created-id', status=self.status)
            if self.create_error: raise self.create_error
            return fake_result(stdout=json.dumps({} if self.missing_identity else {'id': 'created-id'}))
        if method == 'DELETE':
            if self.delete_error: raise RuntimeError('delete failed')
            self.current = None
            return fake_result(stdout='{}')
        if path.endswith('/actions/cancel'):
            self.current['lastRunStatus'] = 'CANCELED'
            return fake_result(stdout='{}')
        if path.endswith('/actions/refresh-status'): return fake_result(stdout='{}')
        if self.current is None:
            return fake_result(stdout='[{"errorCode":"ITEM_NOT_FOUND"}]', returncode=1)
        return fake_result(stdout=json.dumps(self.current))


class RunnerSafety(unittest.TestCase):
    def client(self, api):
        clock = Clock()
        return bisect.ConnectClient('fake', '66.0', runner=api, execute=True,
                                    invocation='test-invocation', clock=clock, sleep=clock.sleep)
    def body(self):
        return bisect.build_probe(sample_full(), 'F', 'ScratchProbe', 'SCRATCH__dll', 'Key__c')
    def test_existing_name_refused_without_any_write(self):
        api = Api(); api.current = {'id': 'foreign'}
        with self.assertRaises(RuntimeError): self.client(api).activate(self.body(), 1)
        self.assertTrue(all(method == 'GET' for method, _, _ in api.calls))
    def test_activation_failure_cleans_and_returns(self):
        api = Api('ERROR'); client = self.client(api)
        self.assertEqual(bisect.execute_probe(client, self.body(), 'activation', 1), 'ERROR')
        self.assertIsNone(api.current)
    def test_timeout_is_inconclusive_and_cleans(self):
        api = Api('PENDING'); client = self.client(api)
        with self.assertRaises(bisect.Inconclusive):
            bisect.execute_probe(client, self.body(), 'activation', 1)
        self.assertIsNone(api.current)
    def test_ambiguous_creation_never_deletes(self):
        for missing in (True, False):
            api = Api(); api.missing_identity = missing
            if not missing: api.create_error = TimeoutError('connection lost')
            stderr = io.StringIO()
            with contextlib.redirect_stderr(stderr), self.assertRaises((RuntimeError, TimeoutError)):
                bisect.execute_probe(self.client(api), self.body(), 'activation', 1)
            self.assertIn('UNRESOLVED CLEANUP', stderr.getvalue())
            self.assertFalse(any(method == 'DELETE' for method, _, _ in api.calls))
    def test_interrupt_preserves_original_exception_and_cleans(self):
        api = Api(); client = self.client(api)
        with patch.object(client, 'run', side_effect=KeyboardInterrupt), self.assertRaises(KeyboardInterrupt):
            bisect.execute_probe(client, self.body(), 'run', 1)
        self.assertIsNone(api.current)
    def test_cleanup_failure_does_not_replace_original(self):
        api = Api(); api.delete_error = True; client = self.client(api)
        stderr = io.StringIO()
        with patch.object(client, 'run', side_effect=ValueError('original')), \
             contextlib.redirect_stderr(stderr), self.assertRaisesRegex(ValueError, 'original'):
            bisect.execute_probe(client, self.body(), 'run', 1)
        self.assertIn('UNRESOLVED CLEANUP', stderr.getvalue())
    def test_ownership_mismatch_blocks_cancel_and_delete(self):
        api = Api(); client = self.client(api); body = self.body()
        client.activate(body, 1)
        api.current['id'] = 'replacement'
        api.calls.clear()
        with self.assertRaises(RuntimeError): client.cleanup(body['name'])
        self.assertTrue(all(method == 'GET' for method, _, _ in api.calls))
    def test_running_owned_probe_is_cancelled_before_delete(self):
        api = Api(); client = self.client(api); body = self.body()
        client.activate(body, 1)
        client.owned[body['name']]['run_started'] = True
        api.current['lastRunStatus'] = 'IN_PROGRESS'
        client.cleanup(body['name'])
        paths = [path for method, path, _ in api.calls if method != 'GET']
        self.assertTrue(any(path.endswith('/actions/cancel') for path in paths))
        self.assertIsNone(api.current)
    def test_no_mutations_without_execute(self):
        api = Api(); client = bisect.ConnectClient('fake', '66.0', runner=api)
        with self.assertRaises(RuntimeError): client.activate(self.body(), 1)
        self.assertEqual(api.calls, [])
    def test_invalid_response_does_not_mean_missing(self):
        for response in ('not json', '', 'null'):
            client = bisect.ConnectClient('fake', '66.0', runner=lambda _: fake_result(stdout=response))
            with self.assertRaises(RuntimeError): client.get('Probe')
    def test_preview_and_denied_execution_never_spawn(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'body.json'; path.write_text(json.dumps(sample_full()))
            args = ['bisect', str(path), '--org', 'fake', '--scratch-dlo', 'SCRATCH__dll', '--cuts', 'L', 'F']
            with patch.object(bisect.subprocess, 'run') as run, contextlib.redirect_stdout(io.StringIO()):
                with patch('sys.argv', args): self.assertEqual(bisect.main(), 0)
                with patch('sys.argv', args + ['--execute']), contextlib.redirect_stderr(io.StringIO()), self.assertRaises(SystemExit):
                    bisect.main()
                run.assert_not_called()
    def test_name_uniqueness_and_length(self):
        names = {bisect.probe_name('DTTMPBISECT', 1, token) for token in ('abc123', 'xyz987')}
        self.assertEqual(len(names), 2)
        self.assertTrue(all(len(name) <= 32 for name in names))
        with self.assertRaises(ValueError): bisect.probe_name('X' * 31, 1, 'token')
    def test_all_write_boundaries_are_checked(self):
        for cut, scratch in (('O', 'SCRATCH__dll'), ('F', 'PROD__dll')):
            with self.assertRaises(ValueError): bisect.build_probe(sample_full(), cut, 'probe', scratch, 'Key__c')
        body = sample_full(); body['definition']['nodes']['F']['action'] = 'unknownWriter'
        with self.assertRaises(ValueError): bisect.build_probe(body, 'F', 'probe', 'SCRATCH__dll', 'Key__c')


class ClosureSafety(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        root = Path(self.tmp.name)
        self.source, self.payload = root / 'src', root / 'payload'
        self.dest = self.payload / 'closure'
        self.source.mkdir(); self.payload.mkdir()
        (self.source / 'a.py').write_text('x = 1\n')
        (self.payload / 'entry.py').write_text('from closure.a import x\n')
    def write(self): closure_mod.write(['entry'], self.source, self.payload, self.dest)
    def test_check_is_read_only_and_reports_missing_module(self):
        before = sorted(str(p) for p in Path(self.tmp.name).rglob('*'))
        problems = closure_mod.drift(['entry'], self.source, self.payload, self.dest)
        self.assertIn('missing from payload: a.py', problems)
        self.assertEqual(before, sorted(str(p) for p in Path(self.tmp.name).rglob('*')))
    def test_unowned_destination_is_preserved(self):
        self.dest.mkdir(); note = self.dest / 'precious.txt'; note.write_text('keep')
        with self.assertRaises(ValueError): self.write()
        self.assertEqual(note.read_text(), 'keep')
    def test_overlap_and_symlink_escape_are_refused(self):
        for dest in (self.source, self.source / 'child', self.payload, self.payload.parent):
            with self.assertRaises(ValueError): closure_mod.write(['entry'], self.source, self.payload, dest)
        self.dest.symlink_to(self.source, target_is_directory=True)
        with self.assertRaises(ValueError): self.write()
        self.assertTrue((self.source / 'a.py').exists())
    def test_syntax_or_copy_failure_preserves_previous_payload(self):
        self.write(); original = (self.dest / 'a.py').read_text()
        (self.source / 'a.py').write_text('this is invalid python !!!')
        with self.assertRaises(SyntaxError): self.write()
        self.assertEqual((self.dest / 'a.py').read_text(), original)
        (self.source / 'a.py').write_text('x = 2\n')
        with patch.object(closure_mod.shutil, 'copy2', side_effect=OSError('copy failed')), self.assertRaises(OSError): self.write()
        self.assertEqual((self.dest / 'a.py').read_text(), original)
    def test_replacement_failure_rolls_back(self):
        self.write(); original = (self.dest / 'a.py').read_text()
        (self.source / 'a.py').write_text('x = 2\n')
        replace = os.replace
        def fail_install(source, destination):
            if Path(source).name.startswith('.beast-closure-'): raise OSError('install failed')
            return replace(source, destination)
        with patch.object(closure_mod.os, 'replace', side_effect=fail_install), self.assertRaises(OSError): self.write()
        self.assertEqual((self.dest / 'a.py').read_text(), original)
    def test_nested_packages_and_initializer_dependencies(self):
        (self.source / 'sub').mkdir()
        (self.source / '__init__.py').write_text('from . import a\n')
        (self.source / 'sub' / '__init__.py').write_text('')
        (self.source / 'sub' / 'b.py').write_text('from .. import a\nvalue = a.x\n')
        (self.payload / 'entry.py').write_text('from closure.sub.b import value\n')
        self.write()
        self.assertTrue((self.dest / 'a.py').is_file())
        self.assertTrue((self.dest / '__init__.py').is_file())
        self.assertTrue((self.dest / 'sub' / '__init__.py').is_file())
        self.assertTrue((self.dest / 'sub' / 'b.py').is_file())
    def test_dynamic_and_unresolved_imports_fail(self):
        for code in ('from closure.missing import x', 'import importlib\nimportlib.import_module("closure.a")',
                     'from importlib import import_module as load\nload("closure.a")'):
            (self.payload / 'entry.py').write_text(code)
            with self.assertRaises(ValueError): self.write()
            self.assertFalse(self.dest.exists())
    def test_owned_directory_with_new_unowned_file_is_not_replaced(self):
        self.write(); note = self.dest / 'extra.txt'; note.write_text('keep')
        with self.assertRaises(ValueError): self.write()
        self.assertEqual(note.read_text(), 'keep')


class GraphSafety(unittest.TestCase):
    def test_permutations_and_collisions_preserve_all_edges(self):
        nodes = sample_full()['definition']['nodes']
        nodes['F']['parameters']['fields'].append({'name': 'Y', 'formulaExpression': 'A'})
        nodes['F_1'] = {'action': 'filter', 'parameters': {}, 'sources': ['L']}
        for seed in range(10):
            keys = list(nodes); random.Random(seed).shuffle(keys)
            result = builder_shape.expand_formula_nodes({key: nodes[key] for key in keys})
            validate_graph(result)
            self.assertEqual(result['F_1'], nodes['F_1'])
    def test_cycles_and_missing_sources_fail_without_rewriting(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'body.json'
            for source in ('O', 'missing'):
                body = sample_full(); body['definition']['nodes']['L']['sources'] = [source]
                path.write_text(json.dumps(body)); before = path.read_bytes()
                with self.assertRaises(ValueError): builder_shape._split_file(str(path))
                self.assertEqual(before, path.read_bytes())
    def test_properties_and_final_schema_are_preserved(self):
        nodes = sample_full()['definition']['nodes']; node = nodes['F']
        node['parameters']['expressionType'] = 'SQL'; node['customProperty'] = 'keep'
        node['schema'] = {'slice': {'mode': 'DROP', 'fields': ['A']}}
        node['parameters']['fields'].append({'name': 'Y', 'formulaExpression': 'A'})
        result = builder_shape.expand_formula_nodes(nodes)
        tail = result['O']['sources'][0]
        self.assertEqual(result[tail]['schema'], node['schema'])
        self.assertEqual(result[tail]['customProperty'], 'keep')
    def test_tokenizer_handles_literals_comments_and_escaped_quotes(self):
        refs = ref_check.references('concat(\'not a column\', "A", "odd""name", "r"."B") /* ignored */')
        self.assertEqual([ref for ref, _ in refs], ['A', 'odd"name', 'r.B'])
    def test_drop_removes_columns_and_unknown_shape_is_inconclusive(self):
        nodes = sample_full()['definition']['nodes']
        nodes['L']['schema'] = {'slice': {'mode': 'DROP', 'fields': ['A']}}
        self.assertEqual(ref_check.node_columns(nodes)('L'), set())
        nodes['L']['schema']['slice']['mode'] = 'UNSUPPORTED'
        with self.assertRaises(ref_check.UnsupportedShape): ref_check.node_columns(nodes)('L')
    def test_unknown_upstream_action_is_not_certified(self):
        nodes = sample_full()['definition']['nodes']; nodes['L']['action'] = 'mystery'
        with self.assertRaises(ref_check.UnsupportedShape): ref_check.node_columns(nodes)('F')


class DiagnosticSafety(unittest.TestCase):
    def test_structured_filters_escape_sql_and_order(self):
        sql = diagnostics.build_logs_query("transform' OR '1'='1", execution_id="run'1", since='2026-09-01T00:00:00Z')
        self.assertIn("'transform'' OR ''1''=''1'", sql)
        self.assertIn("'run''1'", sql)
        self.assertIn('ORDER BY "Timestamp__c" DESC', sql)
        for bad in ('no-timezone', '2026-01-01T00:00:00'):
            with self.assertRaises(ValueError): diagnostics.build_logs_query('t', since=bad)
    def test_pagination_is_bounded_and_scoped(self):
        client = unittest.mock.Mock()
        client.request.side_effect = [
            {'data': [[1]], 'done': False, 'nextBatchId': 'page/2'},
            {'data': [[2]], 'done': True}]
        result = diagnostics.fetch_logs(client, '/base', 'scoped sql', 5, data_space='space one')
        self.assertEqual(result['data'], [[1], [2]])
        self.assertTrue(result['paginationComplete'])
        self.assertIn('page%2F2?dataspace=space%20one', client.request.call_args.args[0])
    def test_row_cap_and_missing_cursor_are_incomplete(self):
        for page in ({'data': [[1], [2]], 'done': True}, {'data': [], 'done': False}):
            client = unittest.mock.Mock(); client.request.return_value = page
            result = diagnostics.fetch_logs(client, '/base', 'sql', 1)
            self.assertTrue(result['truncated'])
            self.assertEqual(client.request.call_count, 1)
    def test_delayed_logs_poll_to_bounded_completion(self):
        clock = Clock(); client = unittest.mock.Mock()
        client.request.side_effect = [
            {'histories': [{'status': 'IN_PROGRESS'}]}, {'data': [], 'done': True},
            {'histories': [{'status': 'SUCCESS'}]}, {'data': [['log']], 'done': True}]
        report = diagnostics.collect(client, '66.0', 'transform', execution_id='run',
            wait_seconds=30, clock=clock, sleep=clock.sleep)
        self.assertTrue(report['complete']); self.assertEqual(clock.now, 15)
        self.assertEqual(report['correlation']['scope'], 'execution')
        self.assertFalse(report['correlation']['historyExecutionMatched'])
    def test_snapshot_does_not_claim_running_history_is_terminal(self):
        client = unittest.mock.Mock()
        client.request.side_effect = [{'histories': [{'status': 'IN_PROGRESS'}]}, {'data': [], 'done': True}]
        report = diagnostics.collect(client, '66.0', 'transform')
        self.assertFalse(report['runTerminal']); self.assertFalse(report['complete'])
        self.assertEqual(report['correlation']['scope'], 'transform')
    def test_missing_schema_never_falls_back_to_unscoped_query(self):
        client = unittest.mock.Mock()
        client.request.side_effect = [{'histories': []}, RuntimeError('unknown field')]
        report = diagnostics.collect(client, '66.0', 'transform')
        self.assertFalse(report['complete']); self.assertTrue(report['errors'])
        self.assertEqual(client.request.call_count, 2)
    def test_empty_logs_timeout_is_explicit(self):
        clock = Clock(); client = unittest.mock.Mock()
        client.request.side_effect = lambda path, *a: ({'histories': [{'status': 'FAILURE'}]} if 'run-history' in path else {'data': [], 'done': True})
        report = diagnostics.collect(client, '66.0', 'transform', wait_seconds=20,
                                     clock=clock, sleep=clock.sleep)
        self.assertTrue(report['timedOut']); self.assertEqual(clock.now, 20)
        self.assertFalse(report['complete'])


if __name__ == '__main__': unittest.main()
