"""Proof IDs are unique evidence identities, not row counters."""
import importlib.util
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('proof_reference_validator', ROOT / 'tools/validate_docs_watch.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class ProofReferences(unittest.TestCase):
    def test_missing_reference_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); (root / 'skills').mkdir(); (root / 'docs').mkdir()
            (root / 'skills' / 'SKILL.md').write_text('See BEAST-PROOF-999')
            issues = []
            with patch.object(validator, 'ROOT', root):
                validator.validate_proof_references(issues, {'BEAST-PROOF-001'})
            self.assertTrue(any('BEAST-PROOF-999' in issue for issue in issues))
    def test_reserved_id_is_not_actual_skill_evidence(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); (root / 'skills').mkdir(); (root / 'docs').mkdir()
            (root / 'docs' / 'proof-ledger.md').write_text('Reserved BEAST-PROOF-019')
            (root / 'skills' / 'SKILL.md').write_text('Tested BEAST-PROOF-019')
            issues = []
            with patch.object(validator, 'ROOT', root): validator.validate_proof_references(issues, set())
            self.assertEqual(len(issues), 1)
            self.assertIn('skills/SKILL.md', issues[0])
    def test_duplicate_or_reused_reserved_ids_are_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); (root / 'docs').mkdir()
            header = '| ' + ' | '.join(validator.PROOF_HEADERS) + ' |\n'
            row = '| `BEAST-PROOF-019` | source | unrelated evidence | prepare | default | response | caveat | tested | none | candidate |\n'
            (root / 'docs' / 'proof-ledger.md').write_text('## Current Evidence\n' + header + '|---|\n' + row + row)
            issues = []
            with patch.object(validator, 'ROOT', root): validator.validate_proof_ledger(issues, {'prepare'})
            self.assertTrue(any('duplicate proof' in issue for issue in issues))
            self.assertTrue(any('reserved for different' in issue for issue in issues))
    def test_lifecycle_entry_can_land_in_reserved_slot(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp); (root / 'docs').mkdir()
            header = '| ' + ' | '.join(validator.PROOF_HEADERS) + ' |\n'
            row = '| `BEAST-PROOF-019` | source | ' + validator.PROOF_RESERVATIONS['BEAST-PROOF-019'] + ' | develop-package | default | response | caveat | tested | none | promoted |\n'
            (root / 'docs' / 'proof-ledger.md').write_text('## Current Evidence\n' + header + '|---|\n' + row)
            issues = []
            with patch.object(validator, 'ROOT', root): validator.validate_proof_ledger(issues, {'develop-package'})
            self.assertEqual(issues, [])


if __name__ == '__main__': unittest.main()
