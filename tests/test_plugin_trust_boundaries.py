from __future__ import annotations

import json
import os
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
VALIDATOR = REPO / "skills/omarchy-plugin-test/scripts/validate_plugin.py"
GENERATOR = REPO / "skills/omarchy-plugin-scaffold/scripts/new_plugin.py"


def manifest(entry: str = "Panel.qml") -> dict[str, object]:
    return {
        "schemaVersion": 1,
        "id": "io.github.example.fixture",
        "name": "Fixture",
        "version": "1.0.0",
        "author": "Fixture",
        "description": "Fixture plugin.",
        "license": "MIT",
        "kinds": ["panel"],
        "entryPoints": {"panel": entry},
    }


def write_plugin(root: Path, entry: str = "Panel.qml") -> None:
    root.mkdir()
    (root / "manifest.json").write_text(json.dumps(manifest(entry)), encoding="utf-8")
    (root / "Panel.qml").write_text("import QtQuick\nItem { function open(x) {} function close() {} }\n", encoding="utf-8")


def validate(root: Path, *arguments: str, timeout: int = 10) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(VALIDATOR), "--json", *arguments, str(root)],
        cwd=REPO,
        text=True,
        capture_output=True,
        check=False,
        timeout=timeout,
    )


class PluginTrustBoundaryTests(unittest.TestCase):
    def test_duplicate_manifest_keys_and_oversized_manifest_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "plugin"
            write_plugin(root)
            text = json.dumps(manifest())
            (root / "manifest.json").write_text(text[:-1] + ',"id":"io.github.example.shadow"}', encoding="utf-8")
            duplicate = validate(root)
            self.assertEqual(1, duplicate.returncode, duplicate.stdout + duplicate.stderr)
            self.assertIn("duplicate JSON key", json.loads(duplicate.stdout)["errors"][0]["message"])

            (root / "manifest.json").write_bytes(b" " * (1024 * 1024 + 1))
            oversized = validate(root)
            self.assertEqual(1, oversized.returncode)
            codes = {item["code"] for item in json.loads(oversized.stdout)["errors"]}
            self.assertIn("manifest-json", codes)

    def test_symlinked_ancestor_is_rejected_before_outside_qml_is_scanned(self) -> None:
        if os.name == "nt":
            self.skipTest("symlink creation is not generally available on Windows CI")
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            outside = base / "outside"
            outside.mkdir()
            (outside / "Evil.qml").write_text(
                "import QtQuick\nItem { function open(x) {} function close() {} XMLHttpRequest {} }\n",
                encoding="utf-8",
            )
            root = base / "plugin"
            write_plugin(root, "linked/Evil.qml")
            (root / "linked").symlink_to(outside, target_is_directory=True)
            result = validate(root, "--security")
            payload = json.loads(result.stdout)
            self.assertEqual(1, result.returncode)
            self.assertIn("symlink", {item["code"] for item in payload["errors"]})
            self.assertEqual([], payload["security"]["capabilities"])

    def test_fifo_is_rejected_without_blocking(self) -> None:
        if not hasattr(os, "mkfifo"):
            self.skipTest("FIFO unavailable")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "plugin"
            write_plugin(root)
            os.mkfifo(root / "trap")
            result = validate(root, timeout=5)
            self.assertEqual(1, result.returncode, result.stdout + result.stderr)
            self.assertIn("special-file", {item["code"] for item in json.loads(result.stdout)["errors"]})

    def test_qml_dynamic_code_network_and_process_are_review_capabilities(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary) / "plugin"
            write_plugin(root)
            (root / "Panel.qml").write_text(
                "import QtQuick\nItem { function open(x) { eval(x); var y = new XMLHttpRequest() } function close() {} Process {} }\n",
                encoding="utf-8",
            )
            result = validate(root, "--security")
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            codes = {item["code"] for item in json.loads(result.stdout)["security"]["capabilities"]}
            self.assertTrue({"qml-dynamic-code", "qml-network", "qml-process"}.issubset(codes))

    def test_generator_rejects_symlink_destination_and_pins_generated_actions(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            base = Path(temporary)
            victim = base / "victim"
            victim.mkdir()
            if os.name != "nt":
                linked = base / "linked"
                linked.symlink_to(victim, target_is_directory=True)
                refused = subprocess.run(
                    [sys.executable, str(GENERATOR), "--id", "io.github.example.fixture", "--name", "Fixture", "--kind", "panel", "--output", str(linked), "--no-git"],
                    cwd=REPO, text=True, capture_output=True, check=False,
                )
                self.assertEqual(2, refused.returncode)
                self.assertTrue(victim.is_dir())

            output = base / "generated"
            generated = subprocess.run(
                [sys.executable, str(GENERATOR), "--id", "io.github.example.fixture", "--name", "Fixture", "--kind", "panel", "--output", str(output), "--no-git"],
                cwd=REPO, text=True, capture_output=True, check=False,
            )
            self.assertEqual(0, generated.returncode, generated.stdout + generated.stderr)
            workflow = (output / ".github/workflows/test.yml").read_text(encoding="utf-8")
            refs = re.findall(r"uses:\s+[^@]+@([0-9a-f]{40})", workflow)
            self.assertEqual(2, len(refs))
            self.assertIn("encoded.length > 16384", (output / "Panel.qml").read_text(encoding="utf-8"))
            portable = subprocess.run([str(output / "tests/run")], cwd=output, text=True, capture_output=True, check=False, timeout=10)
            self.assertEqual(0, portable.returncode, portable.stdout + portable.stderr)


if __name__ == "__main__":
    unittest.main()
