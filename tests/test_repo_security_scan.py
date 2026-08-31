from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
SCANNER = REPO / "scripts/security_scan.py"


def git(root: Path, *arguments: str) -> None:
    subprocess.run(["git", "-C", str(root), *arguments], check=True, capture_output=True)


def run_scan(root: Path, tree: str = "HEAD") -> tuple[int, dict[str, object]]:
    result = subprocess.run(
        [sys.executable, str(SCANNER), "--repo", str(root), "--git-tree", tree, "--json"],
        text=True,
        capture_output=True,
        check=False,
    )
    return result.returncode, json.loads(result.stdout)


class RepositorySecurityScanTests(unittest.TestCase):
    def make_repo(self) -> tuple[tempfile.TemporaryDirectory[str], Path]:
        temporary = tempfile.TemporaryDirectory()
        root = Path(temporary.name)
        git(root, "init", "-q")
        git(root, "config", "user.name", "Fixture")
        git(root, "config", "user.email", "fixture@example.invalid")
        return temporary, root

    def test_exact_committed_tree_ignores_uncommitted_workspace_content(self) -> None:
        temporary, root = self.make_repo()
        with temporary:
            (root / "safe.txt").write_text("safe\n", encoding="utf-8")
            git(root, "add", "safe.txt")
            git(root, "commit", "-qm", "safe")
            (root / ".env").write_text("github_pat_" + "A" * 40, encoding="utf-8")
            code, report = run_scan(root)
            self.assertEqual(0, code)
            self.assertTrue(report["ok"])
            self.assertEqual(1, report["files"])

    def test_secret_and_credential_filename_block_without_echoing_value(self) -> None:
        temporary, root = self.make_repo()
        with temporary:
            secret = "ghp_" + "S" * 36
            (root / ".env").write_text(secret, encoding="utf-8")
            git(root, "add", ".env")
            git(root, "commit", "-qm", "unsafe")
            code, report = run_scan(root)
            self.assertEqual(1, code)
            self.assertFalse(report["ok"])
            self.assertNotIn(secret, json.dumps(report))
            self.assertEqual({"credential-filename", "github-token"}, {item["code"] for item in report["findings"]})

    def test_symlink_and_unapproved_binary_fail_closed(self) -> None:
        temporary, root = self.make_repo()
        with temporary:
            (root / "payload.bin").write_bytes(b"\x00\x01")
            (root / "link").symlink_to("payload.bin")
            git(root, "add", "payload.bin", "link")
            git(root, "commit", "-qm", "unsafe")
            code, report = run_scan(root)
            self.assertEqual(1, code)
            self.assertIn("unsupported non-regular Git entry", report["error"])

    def test_capabilities_are_review_signals_not_false_safety_failures(self) -> None:
        temporary, root = self.make_repo()
        with temporary:
            script = root / "runner.py"
            script.write_text("import subprocess\nsubprocess.run(['true'])\n", encoding="utf-8")
            script.chmod(0o755)
            git(root, "add", "runner.py")
            git(root, "commit", "-qm", "capability")
            code, report = run_scan(root)
            self.assertEqual(0, code)
            self.assertTrue(report["ok"])
            self.assertEqual({"process-execution", "executable"}, {item["code"] for item in report["findings"]})


if __name__ == "__main__":
    unittest.main()
