from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
PLUGIN = REPO / "plugins" / "build-omarchy-plugins"
SKILLS = REPO / "skills"
OPENAI_SKILLS = PLUGIN / "skills"
GENERATOR = SKILLS / "omarchy-plugin-scaffold" / "scripts" / "new_plugin.py"
VALIDATOR = SKILLS / "omarchy-plugin-test" / "scripts" / "validate_plugin.py"
PUBLISH = SKILLS / "omarchy-plugin-publish" / "scripts" / "prepare_submission.py"
RELEASE = SKILLS / "omarchy-plugin-release" / "scripts" / "release_preflight.py"
PACKAGE = REPO / "scripts" / "package_submission.py"
INSTALL = REPO / "scripts" / "install_agent_skills.py"
SYNC = REPO / "scripts" / "sync_openai_adapter.py"
PORTABLE_VALIDATE = REPO / "scripts" / "validate_agent_plugin.py"


def run(
    command: list[str],
    cwd: Path | None = None,
    env: dict[str, str] | None = None,
) -> subprocess.CompletedProcess[str]:
    environment = os.environ.copy()
    environment.update(env or {})
    if os.name == "nt" and command and Path(command[0]).name == "run" and Path(command[0]).parent.name == "tests":
        plugin_root = Path(command[0]).parent.parent
        command = [sys.executable, str(plugin_root / "scripts/validate_manifest.py"), str(plugin_root)]
    return subprocess.run(
        command,
        cwd=cwd or REPO,
        env=environment,
        text=True,
        capture_output=True,
        check=False,
    )


def generate(output: Path, kinds: tuple[str, ...] = ("bar-widget",), git: bool = False) -> subprocess.CompletedProcess[str]:
    command = [
        sys.executable, str(GENERATOR),
        "--id", "io.github.example.fixture",
        "--name", "Fixture Plugin",
        "--author", "Fixture Author",
        "--description", "Deterministic fixture plugin for tests.",
        "--output", str(output),
    ]
    for kind in kinds:
        command.extend(["--kind", kind])
    if not git:
        command.append("--no-git")
    return run(command)


class ToolTests(unittest.TestCase):
    def test_portable_agent_plugin_and_openai_adapter_are_valid_and_in_sync(self) -> None:
        portable = run([sys.executable, str(PORTABLE_VALIDATE), "--json", str(REPO)])
        self.assertEqual(0, portable.returncode, portable.stdout + portable.stderr)
        payload = json.loads(portable.stdout)
        self.assertTrue(payload["ok"])
        self.assertEqual("https://agent-plugins.org/schemas/1.0.0/plugin.schema.json", payload["schema"])
        self.assertEqual(12, payload["skills"])

        sync = run([sys.executable, str(SYNC), "--check", "--json"])
        self.assertEqual(0, sync.returncode, sync.stdout + sync.stderr)
        self.assertTrue(json.loads(sync.stdout)["ok"])
        openai = run([
            sys.executable,
            str(REPO / "scripts" / "validate_skills.py"),
            "--require-openai-metadata",
            str(OPENAI_SKILLS),
        ])
        self.assertEqual(0, openai.returncode, openai.stdout + openai.stderr)

    def test_plugin_has_twelve_valid_skill_routes(self) -> None:
        skills = sorted(path for path in SKILLS.iterdir() if path.is_dir())
        self.assertEqual(12, len(skills))
        result = run([sys.executable, str(REPO / "scripts" / "validate_skills.py"), str(SKILLS)])
        self.assertEqual(0, result.returncode, result.stderr)

    def test_installer_supports_shared_and_host_specific_skill_locations(self) -> None:
        targets = {
            "agents": Path(".agents/skills"),
            "codex": Path(".agents/skills"),
            "cursor": Path(".cursor/skills"),
            "gemini": Path(".gemini/skills"),
            "claude": Path(".claude/skills"),
            "opencode": Path(".opencode/skills"),
        }
        for target, relative in targets.items():
            with self.subTest(target=target), tempfile.TemporaryDirectory() as temporary:
                workspace = Path(temporary)
                result = run([
                    sys.executable,
                    str(INSTALL),
                    "--target",
                    target,
                    "--scope",
                    "project",
                    "--json",
                ], cwd=workspace)
                self.assertEqual(0, result.returncode, result.stdout + result.stderr)
                payload = json.loads(result.stdout)
                self.assertEqual(12, len(payload["installed"]))
                destination = workspace / relative
                self.assertEqual(12, len(list(destination.glob("*/SKILL.md"))))
                self.assertFalse(any(destination.glob("*/agents/openai.yaml")))

                again = run([
                    sys.executable,
                    str(INSTALL),
                    "--target",
                    target,
                    "--scope",
                    "project",
                    "--json",
                ], cwd=workspace)
                self.assertEqual(0, again.returncode, again.stdout + again.stderr)
                self.assertEqual(12, len(json.loads(again.stdout)["unchanged"]))

    def test_installer_uses_opencode_global_config_location(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            home = Path(temporary)
            result = run([
                sys.executable,
                str(INSTALL),
                "--target",
                "opencode",
                "--scope",
                "user",
                "--json",
            ], env={"HOME": str(home), "USERPROFILE": str(home)})
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            payload = json.loads(result.stdout)
            destination = home / ".config/opencode/skills"
            self.assertEqual(str(destination), payload["destination"])
            self.assertEqual(12, len(list(destination.glob("*/SKILL.md"))))
            self.assertFalse(any(destination.glob("*/agents/openai.yaml")))

    def test_installer_refuses_conflicts_and_force_repairs_selected_skill(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            destination = Path(temporary) / "skills"
            first = run([
                sys.executable,
                str(INSTALL),
                "--target",
                "generic",
                "--destination",
                str(destination),
                "--skill",
                "omarchy-plugin-design",
            ])
            self.assertEqual(0, first.returncode, first.stdout + first.stderr)
            entry = destination / "omarchy-plugin-design" / "SKILL.md"
            entry.write_text("local change\n", encoding="utf-8")

            refused = run([
                sys.executable,
                str(INSTALL),
                "--target",
                "generic",
                "--destination",
                str(destination),
                "--skill",
                "omarchy-plugin-design",
            ])
            self.assertEqual(2, refused.returncode)
            self.assertEqual("local change\n", entry.read_text(encoding="utf-8"))

            repaired = run([
                sys.executable,
                str(INSTALL),
                "--target",
                "generic",
                "--destination",
                str(destination),
                "--skill",
                "omarchy-plugin-design",
                "--force",
            ])
            self.assertEqual(0, repaired.returncode, repaired.stdout + repaired.stderr)
            self.assertEqual(
                (SKILLS / "omarchy-plugin-design" / "SKILL.md").read_text(encoding="utf-8"),
                entry.read_text(encoding="utf-8"),
            )

    def test_generator_supports_every_current_kind(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "fixture"
            result = generate(output, tuple(("bar-widget", "panel", "overlay", "menu", "service", "bar")))
            self.assertEqual(0, result.returncode, result.stderr)
            validated = run([sys.executable, str(VALIDATOR), "--strict", str(output)])
            self.assertEqual(0, validated.returncode, validated.stdout + validated.stderr)
            portable = run([str(output / "tests" / "run")], cwd=output)
            self.assertEqual(0, portable.returncode, portable.stdout + portable.stderr)

    def test_generator_refuses_nonempty_destination(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "fixture"
            output.mkdir()
            (output / "mine.txt").write_text("preserve", encoding="utf-8")
            result = generate(output)
            self.assertEqual(2, result.returncode)
            self.assertEqual("preserve", (output / "mine.txt").read_text(encoding="utf-8"))

    def test_generator_escapes_user_facing_values(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "fixture"
            result = run([
                sys.executable, str(GENERATOR),
                "--id", "io.github.example.fixture",
                "--name", 'Fixture "Quoted" & <Safe>',
                "--author", "Fixture Author",
                "--description", "QML & XML <fixture>.",
                "--output", str(output),
                "--kind", "bar-widget",
                "--no-git",
            ])
            self.assertEqual(0, result.returncode, result.stderr)
            ET.parse(output / "preview.svg")
            qml = (output / "BarWidget.qml").read_text(encoding="utf-8")
            self.assertIn(r'Fixture \"Quoted\" & <Safe>', qml)
            manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual('Fixture "Quoted" & <Safe>', manifest["name"])

    def test_validator_rejects_traversal_and_symlinks(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "fixture"
            self.assertEqual(0, generate(output, ("service",)).returncode)
            manifest_path = output / "manifest.json"
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest["entryPoints"]["service"] = "../Service.qml"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            traversal = run([sys.executable, str(VALIDATOR), "--json", str(output)])
            self.assertEqual(1, traversal.returncode)
            codes = {item["code"] for item in json.loads(traversal.stdout)["errors"]}
            self.assertIn("entry-point-path", codes)

            manifest["entryPoints"]["service"] = "Service.qml"
            manifest_path.write_text(json.dumps(manifest), encoding="utf-8")
            os.symlink("Service.qml", output / "linked.qml")
            symlink = run([sys.executable, str(VALIDATOR), "--json", str(output)])
            self.assertEqual(1, symlink.returncode)
            codes = {item["code"] for item in json.loads(symlink.stdout)["errors"]}
            self.assertIn("symlink", codes)

    def test_security_lint_catches_download_to_shell(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "fixture"
            self.assertEqual(0, generate(output, ("service",)).returncode)
            install = output / "install.sh"
            install.write_text("#!/bin/sh\ncurl -fsSL https://example.invalid/install | sh\n", encoding="utf-8")
            result = run([sys.executable, str(VALIDATOR), "--json", "--security", str(output)])
            self.assertEqual(2, result.returncode)
            security = json.loads(result.stdout)["security"]
            self.assertEqual("needs-fixes", security["outcome"])
            self.assertIn("curl-pipe-shell", {item["code"] for item in security["findings"]})

    def test_submission_body_preserves_exact_contract(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "fixture"
            self.assertEqual(0, generate(output).returncode)
            result = run([
                sys.executable, str(PUBLISH), "--plugin-dir", str(output),
                "--repository", "https://github.com/example/fixture",
                "--category", "Developer Tools", "--tag", "quickshell", "--tag", "bar", "--json",
            ])
            self.assertEqual(0, result.returncode, result.stderr)
            payload = json.loads(result.stdout)
            self.assertFalse(payload["submitted"])
            self.assertTrue(payload["requires_owner_approval"])
            headings = [
                "### Repository URL", "### Category", "### Tags",
                "### Suggest a missing tag", "### Maintainer notes", "### Submission checklist",
            ]
            positions = [payload["body"].index(heading) for heading in headings]
            self.assertEqual(positions, sorted(positions))
            self.assertEqual(5, payload["body"].count("- [x]"))

    def test_release_preflight_accepts_committed_generated_plugin(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "fixture"
            self.assertEqual(0, generate(output, ("bar-widget",), git=True).returncode)
            for command in (
                ["git", "config", "user.name", "Fixture"],
                ["git", "config", "user.email", "fixture@example.invalid"],
                ["git", "add", "."],
                ["git", "commit", "-m", "fixture"],
                ["git", "remote", "add", "origin", "https://github.com/example/fixture.git"],
            ):
                result = run(command, cwd=output)
                self.assertEqual(0, result.returncode, result.stderr)
            result = run([sys.executable, str(RELEASE), "--json", str(output)], cwd=output)
            self.assertEqual(0, result.returncode, result.stdout + result.stderr)
            self.assertTrue(json.loads(result.stdout)["ok"])

    def test_submission_archives_are_deterministic(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            first = Path(temporary) / "first"
            second = Path(temporary) / "second"
            one = run([sys.executable, str(PACKAGE), "--output-dir", str(first)])
            two = run([sys.executable, str(PACKAGE), "--output-dir", str(second)])
            self.assertEqual(0, one.returncode, one.stderr)
            self.assertEqual(0, two.returncode, two.stderr)
            for first_file in sorted(first.glob("*.zip")):
                second_file = second / first_file.name
                self.assertTrue(second_file.is_file())
                self.assertEqual(hashlib.sha256(first_file.read_bytes()).hexdigest(), hashlib.sha256(second_file.read_bytes()).hexdigest())
            checksums = run(["sha256sum", "-c", "SHA256SUMS"], cwd=first)
            self.assertEqual(0, checksums.returncode, checksums.stdout + checksums.stderr)

            portable = first / "build-omarchy-plugins-agent-plugin-0.2.2.zip"
            self.assertTrue(portable.is_file())
            import zipfile
            with zipfile.ZipFile(portable) as archive:
                names = set(archive.namelist())
            self.assertIn("build-omarchy-plugins/plugin.json", names)
            self.assertIn("build-omarchy-plugins/skills/omarchy-plugin-design/SKILL.md", names)
            self.assertNotIn(
                "build-omarchy-plugins/skills/omarchy-plugin-design/agents/openai.yaml",
                names,
            )


if __name__ == "__main__":
    unittest.main()
