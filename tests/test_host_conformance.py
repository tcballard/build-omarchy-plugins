from __future__ import annotations

import importlib.util
import json
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
DOCTOR = REPO / "scripts/doctor_agent_skills.py"
CONFORMANCE = REPO / "scripts/host_conformance.py"


def run(script: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(script), *arguments, "--json"],
        cwd=REPO,
        text=True,
        capture_output=True,
        check=False,
    )


def skill(root: Path, name: str = "fixture-skill", body: str = "# Fixture\n") -> Path:
    target = root / name
    target.mkdir(parents=True)
    (target / "SKILL.md").write_text(
        f"---\nname: {name}\ndescription: Fixture skill for conformance tests.\n---\n\n{body}",
        encoding="utf-8",
    )
    return target


def copy_skill(source: Path, root: Path) -> None:
    shutil.copytree(source, root / source.name)


class HostConformanceTests(unittest.TestCase):
    def test_opencode_walks_to_worktree_and_rejects_duplicate_claims(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".git").mkdir()
            source_root = root / "source"
            source = skill(source_root)
            cwd = root / "apps/web"
            cwd.mkdir(parents=True)
            copy_skill(source, root / ".agents/skills")
            one = run(DOCTOR, "--host", "opencode", "--source", str(source_root), "--cwd", str(cwd), "--home", str(root / "home"))
            self.assertEqual(0, one.returncode, one.stdout + one.stderr)
            payload = json.loads(one.stdout)
            self.assertTrue(payload["discoveryReady"])
            roots = {item["path"] for item in payload["roots"]}
            self.assertIn(str(cwd / ".opencode/skills"), roots)
            self.assertIn(str(root / ".agents/skills"), roots)

            copy_skill(source, cwd / ".opencode/skills")
            duplicate = run(DOCTOR, "--host", "opencode", "--source", str(source_root), "--cwd", str(cwd), "--home", str(root / "home"))
            payload = json.loads(duplicate.stdout)
            self.assertFalse(payload["discoveryReady"])
            self.assertEqual(["fixture-skill"], payload["summary"]["ambiguous"])

    def test_gemini_precedence_and_cursor_recursive_discovery(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".git").mkdir()
            source_root = root / "source"
            source = skill(source_root)
            copy_skill(source, root / ".gemini/skills")
            alias = root / ".agents/skills"
            changed = skill(alias, body="# Different\n")
            gemini = run(DOCTOR, "--host", "gemini", "--source", str(source_root), "--cwd", str(root), "--home", str(root / "home"))
            payload = json.loads(gemini.stdout)
            self.assertEqual(str(changed), payload["resolution"]["fixture-skill"]["selectedPath"])
            self.assertFalse(payload["resolution"]["fixture-skill"]["exactSourceCopy"])

            nested = root / "packages/widget/.cursor/skills"
            copy_skill(source, nested)
            cursor = run(DOCTOR, "--host", "cursor", "--source", str(source_root), "--cwd", str(root), "--home", str(root / "empty-home"))
            payload = json.loads(cursor.stdout)
            paths = {item["skillPath"] for item in payload["skills"]}
            self.assertIn(str(nested / "fixture-skill"), paths)

    def test_claude_reports_uninspectable_sources_and_documented_personal_precedence(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / ".git").mkdir()
            source_root = root / "source"
            source = skill(source_root)
            copy_skill(source, root / ".claude/skills")
            personal = root / "home/.claude/skills"
            copy_skill(source, personal)
            result = run(DOCTOR, "--host", "claude", "--source", str(source_root), "--cwd", str(root), "--home", str(root / "home"))
            payload = json.loads(result.stdout)
            self.assertEqual(str(personal / "fixture-skill"), payload["resolution"]["fixture-skill"]["selectedPath"])
            self.assertTrue(any("enterprise" in item for item in payload["blindSpots"]))
            self.assertFalse(payload["hostVerified"])

    def test_custom_commands_and_eval_hooks_cannot_promote_verification(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source_root = root / "skills"
            skill(source_root)
            result = run(
                CONFORMANCE,
                "--host", "codex",
                "--source", str(source_root),
                "--cwd", str(root),
                "--home", str(root / "home"),
                "--custom-command", f'{sys.executable} -c "print(1)"',
                "--eval-hook", f'{sys.executable} -c "print(2)"',
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertFalse(payload["hostVerified"])
            self.assertFalse(payload["providerVerified"])
            self.assertEqual({"operator-controlled-self-report"}, {item["trust"] for item in payload["evidence"]})
            self.assertTrue(all(not item["eligibleForVerification"] for item in payload["evidence"]))

    def test_builtin_opencode_probe_requires_tool_event_clean_source_and_readonly_policy(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.name", "Fixture"], check=True)
            subprocess.run(["git", "-C", str(root), "config", "user.email", "fixture@example.test"], check=True)
            source_root = root / "skills"
            source = skill(source_root, "omarchy-plugin-design", "# Omarchy Plugin Design\n")
            subprocess.run(["git", "-C", str(root), "add", "skills"], check=True)
            subprocess.run(["git", "-C", str(root), "commit", "-qm", "fixture"], check=True)
            copy_skill(source, root / ".agents/skills")
            executable = root / "opencode"
            executable.write_text(
                "#!/usr/bin/env python3\n"
                "import json, os, re, sys\n"
                "cfg=json.loads(os.environ['OPENCODE_CONFIG_CONTENT'])\n"
                "assert cfg['permission']['*']=='deny' and cfg['permission']['skill']=='allow'\n"
                "nonce=re.search(r'nonce \\\"([0-9a-f]+)\\\"', sys.argv[-1]).group(1)\n"
                "print(json.dumps({'type':'tool','tool':'skill','args':{'name':'omarchy-plugin-design'}}))\n"
                "print(json.dumps({'type':'text','text':json.dumps({'nonce':nonce,'title':'Omarchy Plugin Design'})}))\n",
                encoding="utf-8",
            )
            executable.chmod(0o755)
            result = run(
                CONFORMANCE,
                "--host", "opencode",
                "--source", str(source_root),
                "--cwd", str(root),
                "--home", str(root / "home"),
                "--repo-root", str(root),
                "--invoke",
                "--opencode", str(executable),
                "--model", "fixture/model",
            )
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            self.assertTrue(payload["hostVerified"], payload)
            self.assertTrue(payload["providerVerified"])
            self.assertTrue(payload["sourceAttribution"]["stable"])
            self.assertEqual(["read", "glob", "grep", "skill"], payload["evidence"][0]["policy"]["allowed"])

            executable.write_text(executable.read_text(encoding="utf-8") + "raise SystemExit(1)\n", encoding="utf-8")
            failed = run(
                CONFORMANCE,
                "--host", "opencode",
                "--source", str(source_root),
                "--cwd", str(root),
                "--home", str(root / "home"),
                "--repo-root", str(root),
                "--invoke",
                "--opencode", str(executable),
                "--model", "fixture/model",
            )
            failed_payload = json.loads(failed.stdout)
            self.assertFalse(failed_payload["hostVerified"])
            self.assertFalse(failed_payload["providerVerified"])


if __name__ == "__main__":
    unittest.main()
