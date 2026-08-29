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
SKILLS = PLUGIN / "skills"
GENERATOR = SKILLS / "omarchy-plugin-scaffold" / "scripts" / "new_plugin.py"
VALIDATOR = SKILLS / "omarchy-plugin-test" / "scripts" / "validate_plugin.py"
PUBLISH = SKILLS / "omarchy-plugin-publish" / "scripts" / "prepare_submission.py"
RELEASE = SKILLS / "omarchy-plugin-release" / "scripts" / "release_preflight.py"
PACKAGE = REPO / "scripts" / "package_submission.py"


def run(command: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd or REPO, text=True, capture_output=True, check=False)


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
    def test_plugin_has_twelve_valid_skill_routes(self) -> None:
        skills = sorted(path for path in SKILLS.iterdir() if path.is_dir())
        self.assertEqual(12, len(skills))
        result = run([sys.executable, str(REPO / "scripts" / "validate_skills.py"), str(SKILLS)])
        self.assertEqual(0, result.returncode, result.stderr)

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


if __name__ == "__main__":
    unittest.main()
