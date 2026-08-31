from __future__ import annotations

import json
import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
INSTALLER = REPO / "scripts/install_agent_skills.py"


def run(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(INSTALLER), *arguments, "--json"],
        cwd=REPO,
        text=True,
        capture_output=True,
        check=False,
    )


class InstallerLifecycleTests(unittest.TestCase):
    def test_dry_run_receipt_update_diff_and_conservative_uninstall(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "skills"
            dry = run("--target", "generic", "--destination", str(destination), "--skill", "omarchy-plugin-design", "--dry-run")
            self.assertEqual(0, dry.returncode, dry.stdout + dry.stderr)
            self.assertFalse(destination.exists())
            self.assertFalse(any(destination.parent.glob("*.lock")))

            installed = run("--target", "generic", "--destination", str(destination), "--skill", "omarchy-plugin-design")
            self.assertEqual(0, installed.returncode, installed.stdout + installed.stderr)
            receipt = destination / ".build-omarchy-plugins-receipt.json"
            self.assertTrue(receipt.is_file())
            payload = json.loads(receipt.read_text(encoding="utf-8"))
            self.assertEqual("0.2.2", payload["source"]["version"])
            self.assertEqual(["omarchy-plugin-design"], sorted(payload["skills"]))

            skill_file = destination / "omarchy-plugin-design/SKILL.md"
            skill_file.write_text("local modification\n", encoding="utf-8")
            refused = run("--target", "generic", "--destination", str(destination), "--update")
            self.assertEqual(2, refused.returncode)
            diffed = run("--target", "generic", "--destination", str(destination), "--update", "--diff")
            self.assertEqual(0, diffed.returncode, diffed.stdout + diffed.stderr)
            diff_payload = json.loads(diffed.stdout)
            self.assertEqual(["omarchy-plugin-design"], diff_payload["wouldChange"])
            self.assertEqual(["SKILL.md"], diff_payload["diff"]["omarchy-plugin-design"]["changed"])
            self.assertEqual("local modification\n", skill_file.read_text(encoding="utf-8"))
            forced = run("--target", "generic", "--destination", str(destination), "--update", "--force")
            self.assertEqual(0, forced.returncode, forced.stdout + forced.stderr)
            self.assertNotEqual("local modification\n", skill_file.read_text(encoding="utf-8"))

            unrelated = destination / "third-party"
            unrelated.mkdir()
            (unrelated / "SKILL.md").write_text("third party\n", encoding="utf-8")
            removed = run("--target", "generic", "--destination", str(destination), "--uninstall")
            self.assertEqual(0, removed.returncode, removed.stdout + removed.stderr)
            self.assertFalse((destination / "omarchy-plugin-design").exists())
            self.assertTrue((unrelated / "SKILL.md").is_file())
            self.assertFalse(receipt.exists())

    def test_source_and_destination_symlinks_are_rejected(self) -> None:
        if os.name == "nt":
            self.skipTest("symlink creation is not generally available on Windows CI")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            real = root / "real"
            real.mkdir()
            link = root / "link"
            link.symlink_to(real, target_is_directory=True)
            result = run("--target", "generic", "--destination", str(link / "skills"), "--skill", "omarchy-plugin-design")
            self.assertEqual(2, result.returncode)
            self.assertIn("symlink", json.loads(result.stdout)["error"])

    def test_hardlinked_lock_is_rejected_without_clobbering_peer(self) -> None:
        if os.name == "nt":
            self.skipTest("hard-link semantics are exercised on POSIX CI")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            destination = root / "skills"
            victim = root / "victim"
            victim.write_bytes(b"preserve me\n")
            lock = root / ".skills.build-omarchy-plugins.lock"
            os.link(victim, lock)
            result = run("--target", "generic", "--destination", str(destination), "--skill", "omarchy-plugin-design")
            self.assertEqual(2, result.returncode)
            self.assertEqual(b"preserve me\n", victim.read_bytes())
            self.assertEqual(b"preserve me\n", lock.read_bytes())

    def test_multi_skill_install_is_idempotent(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "skills"
            first = run("--target", "generic", "--destination", str(destination))
            self.assertEqual(0, first.returncode, first.stdout + first.stderr)
            self.assertEqual(12, len(json.loads(first.stdout)["installed"]))
            second = run("--target", "generic", "--destination", str(destination))
            self.assertEqual(0, second.returncode, second.stdout + second.stderr)
            self.assertEqual(12, len(json.loads(second.stdout)["unchanged"]))


if __name__ == "__main__":
    unittest.main()
