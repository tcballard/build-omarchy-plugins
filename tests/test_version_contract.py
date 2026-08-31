from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
CHECK = REPO / "scripts/check_versions.py"


class VersionContractTests(unittest.TestCase):
    def test_repository_version_surfaces_agree(self) -> None:
        result = subprocess.run(
            [sys.executable, str(CHECK), str(REPO), "--tag", "v0.2.2"],
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)

    def test_mismatch_and_wrong_tag_fail(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "plugins/build-omarchy-plugins/.codex-plugin").mkdir(parents=True)
            (root / "submission").mkdir()
            (root / "VERSION").write_text("0.2.2\n", encoding="utf-8")
            (root / "plugin.json").write_text(json.dumps({"version": "0.2.1"}), encoding="utf-8")
            (root / "plugins/build-omarchy-plugins/.codex-plugin/plugin.json").write_text(
                json.dumps({"version": "0.2.2"}), encoding="utf-8"
            )
            (root / "submission/evals.json").write_text(json.dumps({"version": "0.2.2"}), encoding="utf-8")
            for relative in (
                "CHANGELOG.md", "submission/README.md",
                "submission/portal-field-map.md", "submission/release-notes.md",
            ):
                (root / relative).write_text("0.2.2\n", encoding="utf-8")
            result = subprocess.run(
                [sys.executable, str(CHECK), str(root), "--tag", "v0.2.1"],
                text=True,
                capture_output=True,
                check=False,
            )
            self.assertEqual(1, result.returncode)
            self.assertIn("plugin.json version must equal 0.2.2", result.stderr)
            self.assertIn("tag must be v0.2.2", result.stderr)


if __name__ == "__main__":
    unittest.main()
