"""Regression cases for PR #12; all org responses are synthetic."""
import contextlib
import copy
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from test_stl_prepare_helpers import bisect, builder_shape, ref_check, sample_full
from test_ce_prepare_helpers import closure_mod, diagnostics


class ReviewRegressions(unittest.TestCase):
    def test_r1_collision_never_deletes_existing_transform(self):
        client = bisect.ConnectClient('fake', '66.0')
        with patch.object(client, 'get', return_value={'id': 'existing'}), \
             patch.object(client, 'drop') as drop, \
             patch.object(client, 'validate', side_effect=RuntimeError('invalid')):
            with self.assertRaises(RuntimeError):
                client.activate({'name': 'probe'}, 1)
            drop.assert_not_called()

    def test_r2_output_cut_is_rejected(self):
        with self.assertRaises(ValueError):
            bisect.build_probe(sample_full(), 'O', 'probe', 'SCRATCH__dll', 'Key__c')

    def test_r3_overlapping_destination_preserves_inputs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            src, payload = root / 'src', root / 'payload'
            src.mkdir(); payload.mkdir()
            entry = payload / 'entrypoint.py'
            entry.write_text('import a\n')
            (src / 'a.py').write_text('x = 1\n')
            try:
                closure_mod.write(['entrypoint'], src, payload, payload)
            except (ValueError, FileNotFoundError):
                pass
            self.assertEqual(entry.read_text(), 'import a\n')

    def test_r4_activation_failure_returns_and_cleans(self):
        client = bisect.ConnectClient('fake', '66.0')
        with patch.object(client, 'activate', return_value=('ERROR', 1)), \
             patch.object(client, 'cleanup') as cleanup:
            result = bisect.execute_probe(client, {'name': 'probe'}, 'activation', 1)
            self.assertEqual(result, 'ERROR')
            cleanup.assert_called_once_with('probe')

    def test_r5_reversed_json_order_preserves_graph(self):
        nodes = sample_full()['definition']['nodes']
        nodes['F']['parameters']['fields'].append({'name': 'Y', 'formulaExpression': 'A'})
        rewritten = builder_shape.expand_formula_nodes(dict(reversed(list(nodes.items()))))
        for node in rewritten.values():
            for source in node.get('sources', []):
                self.assertIn(source, rewritten)

    def test_r6_qualified_import_includes_required_module(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); src = root / 'src'; payload = root / 'payload'
            src.mkdir(); payload.mkdir()
            (src / 'a.py').write_text('x = 1\n')
            (payload / 'entrypoint.py').write_text('from closure.a import x\n')
            self.assertEqual([p.name for p in closure_mod.closure(
                ['entrypoint'], src, payload, package_name='closure')], ['a.py'])

    def test_r7_missing_quoted_column_is_reported(self):
        body = sample_full()
        body['definition']['nodes']['F']['parameters']['fields'][0]['formulaExpression'] = '"MISSING"'
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'body.json'; path.write_text(json.dumps(body))
            self.assertTrue(any(row[2] == 'MISSING' for row in ref_check.unresolved(path)))

    def test_r8_logs_are_scoped_and_ordered(self):
        sql = diagnostics.build_logs_query('my_transform', limit=5)
        self.assertIn('"ProcessDefinitionName__c" = \'my_transform\'', sql)
        self.assertIn('ORDER BY "Timestamp__c" DESC', sql)
        self.assertNotIn('SELECT *', sql)


if __name__ == '__main__':
    unittest.main()
