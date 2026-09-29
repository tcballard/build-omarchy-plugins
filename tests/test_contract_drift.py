from __future__ import annotations

import contextlib
import hashlib
import importlib.util
import io
import json
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location('check_contracts', Path(__file__).resolve().parents[1] / 'scripts/check_contracts.py')
CHECK = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(CHECK)


class ContractDriftTests(unittest.TestCase):
    def run_check(self, head, contents, *, text=False):
        entry = dict(name='Fixture', repository='https://github.com/example/fixture',
                     trackedRef='refs/heads/main', pinnedCommit='a' * 40,
                     path='contract.md', sha256=hashlib.sha256(b'contract\n').hexdigest(),
                     assumptions=['Fixture contract'])
        with tempfile.TemporaryDirectory() as directory:
            ledger = Path(directory) / 'ledger.json'
            ledger.write_text(json.dumps(dict(schemaVersion=1, reviewedAt='2026-09-29', contracts=[entry])))
            before = ledger.read_bytes()
            output = io.StringIO()
            with patch.object(CHECK, 'remote_head', return_value=head), patch.object(CHECK, 'fetch', side_effect=contents) as fetch, contextlib.redirect_stdout(output):
                args = ['--ledger', str(ledger), '--check-heads']
                if not text:
                    args.append('--json')
                status = CHECK.main(args)
            self.assertEqual(before, ledger.read_bytes(), 'Monitoring must not update reviewed pins')
            return status, output.getvalue() if text else json.loads(output.getvalue()), fetch.call_args_list

    def test_unchanged_head_verifies_pinned_bytes_once(self):
        status, payload, calls = self.run_check('a' * 40, [b'contract\n'])
        self.assertEqual(status, 0)
        self.assertEqual(payload['headsMoved'], [])
        self.assertTrue(payload['contracts'][0]['contentVerified'])
        self.assertEqual(len(calls), 1)

    def test_new_commit_with_identical_document_is_informational(self):
        status, payload, calls = self.run_check('b' * 40, [b'contract\n', b'contract\n'])
        self.assertEqual(status, 0)
        self.assertEqual(payload['headsMoved'], ['Fixture'])
        self.assertEqual(payload['drifted'], [])
        self.assertIn('/' + 'b' * 40 + '/contract.md', calls[1].args[0])
        status, output, _ = self.run_check('b' * 40, [b'contract\n', b'contract\n'], text=True)
        self.assertIn('contract bytes unchanged: Fixture', output)

    def test_changed_content_fails_and_reports_digest(self):
        status, payload, _ = self.run_check('b' * 40, [b'contract\n', b'changed\n'])
        self.assertEqual(status, 1)
        self.assertEqual(payload['drifted'], ['Fixture'])
        self.assertEqual(payload['contracts'][0]['headSha256'], hashlib.sha256(b'changed\n').hexdigest())

    def test_missing_head_document_and_network_errors_fail_closed(self):
        for error in [urllib.error.HTTPError('https://example.invalid', 404, 'Missing', {}, None), urllib.error.URLError('unavailable')]:
            with self.subTest(error=error):
                status, payload, _ = self.run_check('b' * 40, [b'contract\n', error])
                self.assertEqual(status, 1)
                self.assertFalse(payload['ok'])
                self.assertIn('error', payload)

    def test_corrupt_pin_fails_before_head_content_is_read(self):
        status, payload, calls = self.run_check('b' * 40, [b'wrong pin\n'])
        self.assertEqual(status, 1)
        self.assertIn('pinned content digest mismatch', payload['error'])
        self.assertEqual(len(calls), 1)
