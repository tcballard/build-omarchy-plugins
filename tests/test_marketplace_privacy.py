import hashlib
import importlib.util
import io
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
CHECK = ROOT / "skills/omarchy-plugin-test/scripts/check_plain_text.py"
READER = ROOT / "skills/omarchy-service-ipc/assets/private-request/read_request.py"


def module(path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


class PlainTextTests(unittest.TestCase):
    def test_each_text_type_requires_its_own_format(self):
        scan = module(CHECK).scan
        for kind in ("Text", "Label", "TextEdit", "TextArea", "Controls.Label"):
            with self.subTest(kind=kind):
                self.assertTrue(scan(f'{kind} {{ text: remote; Text {{ textFormat: Text.PlainText }} }}'))
                self.assertFalse(scan(f'{kind} {{ text: remote; textFormat: Text.PlainText }}'))
                self.assertTrue(scan(f'{kind} {{ textFormat: trusted ? Text.PlainText : Text.RichText }}'))
                self.assertTrue(scan(f'{kind} {{ textFormat: Text.PlainText + 1 }}'))

    def test_comments_and_strings_cannot_satisfy_policy(self):
        scan = module(CHECK).scan
        for body in ('// textFormat: Text.PlainText\ntext: remote',
                     '/* textFormat: Text.PlainText */ text: remote',
                     'text: "textFormat: Text.PlainText } Text {"'):
            self.assertTrue(scan("Text { " + body + " }"))
        self.assertFalse(scan('Item { property string s: "Text { ToolTip.text: x }" }'))
        self.assertFalse(scan('Text { textFormat:\nQQ.Text.PlainText\ntext: "{}" }'))

    def test_tooltip_content_must_be_its_own_plain_text_object(self):
        scan = module(CHECK).scan
        for source in ('Item { ToolTip.text: remote }', 'Item { onClicked: ToolTip.show(remote) }',
                       'ToolTip { text: remote }',
                       'ToolTip { Item { contentItem: Text { textFormat: Text.PlainText } } }',
                       'ToolTip { contentItem: Label { text: remote } }'):
            with self.subTest(source=source):
                self.assertTrue(scan(source))
        self.assertFalse(scan('ToolTip { contentItem: Controls.Label\n{ textFormat: Text.PlainText } }'))

    def test_cli_exceptions_are_named_reviewable_and_fail_when_stale(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            path = root / "About.qml"
            path.write_text('Text { id: credits; textFormat: Text.RichText; text: "<b>Licence</b>" }')
            command = [sys.executable, str(CHECK), str(root)]
            run = lambda *args: subprocess.run(command + list(args), capture_output=True, text=True)
            self.assertEqual(run().returncode, 1)
            allowed = ("--allow-rich-text", "About.qml:credits=Bundled licence only")
            self.assertEqual(run(*allowed).returncode, 0)
            self.assertIn("Bundled licence only", run(*allowed).stdout)
            path.write_text('Item { Text { id: credits } Text { id: credits } }')
            self.assertIn("Ambiguous exception", run(*allowed).stderr)
            path.write_text(path.read_text() + '\nText { id: other; text: remote }')
            self.assertEqual(run(*allowed).returncode, 1)
            path.write_text('Text { id: credits; textFormat: Text.PlainText }')
            self.assertIn("Unused exception", run(*allowed).stderr)
            path.write_bytes(b"\xff")
            self.assertEqual(run().returncode, 1)

    def test_malformed_source_is_rejected(self):
        scan = module(CHECK).scan
        for source in ('Text {', 'Text { text: "unterminated }'):
            with self.subTest(source=source), self.assertRaises(ValueError):
                scan(source)

    def test_cli_refuses_unscanned_symlink_directories(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "plugin"
            root.mkdir()
            (root / "Safe.qml").write_text('Text { textFormat: Text.PlainText }')
            outside = Path(temporary) / "outside"
            outside.mkdir()
            (outside / "Unsafe.qml").write_text('Text { text: remote }')
            try:
                alias = Path(temporary) / "alias"
                alias.symlink_to(root, target_is_directory=True)
                (root / "nested").mkdir()
                (root / "nested/Safe.qml").write_text('Text { textFormat: Text.PlainText }')
                accepted = subprocess.run([sys.executable, str(CHECK), str(alias / "nested")],
                                          capture_output=True, text=True)
                self.assertEqual(accepted.returncode, 0, accepted.stderr)
                (root / "linked").symlink_to(outside, target_is_directory=True)
            except OSError:
                self.skipTest("Symlink creation unavailable")
            result = subprocess.run([sys.executable, str(CHECK), str(root)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 1)
            self.assertIn("Symlinks are not checked", result.stderr)


class PrivateRequestTests(unittest.TestCase):
    def test_real_stdin_preserves_private_unicode_without_echoing(self):
        text = 'Private meeting العربية 🦅 <img src="https://example.invalid/pixel">'
        payload = json.dumps({"text": text}, ensure_ascii=False).encode()
        script = (
            "import hashlib, sys; from read_request import read_request; "
            "value = read_request(sys.stdin.buffer); "
            "print(hashlib.sha256(value.encode()).hexdigest())"
        )
        result = subprocess.run([sys.executable, "-c", script], cwd=READER.parent,
                                input=payload, capture_output=True, timeout=5)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.decode().strip(), hashlib.sha256(text.encode()).hexdigest())
        self.assertEqual(result.stderr, b"")
        self.assertNotIn(text, " ".join(result.args))

    def test_receiver_bounds_bytes_and_rejects_without_payload_in_errors(self):
        reader = module(READER)
        for payload in (b"private invalid json", b'{"text": 12}', b'[]',
                        b'{"text":"private","command":"run"}', b'{"text":"\\u0000"}',
                        b'{"text":"\\ud800"}', b"\xff", b"[" * 2000 + b"]" * 2000,
                        b"x" * (reader.MAX_BYTES + 1)):
            with self.subTest(payload=payload[:50]), self.assertRaises(ValueError) as caught:
                reader.read_request(io.BytesIO(payload))
            self.assertNotIn("private", str(caught.exception))
        value = "x" * (reader.MAX_BYTES - len(b'{"text":""}'))
        self.assertEqual(reader.read_request(io.BytesIO(b'{"text":"' + value.encode() + b'"}')), value)


if __name__ == "__main__":
    unittest.main()
