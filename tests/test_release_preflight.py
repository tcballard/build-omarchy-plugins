from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent
SCRIPT = REPO / "skills/omarchy-plugin-release/scripts/release_preflight.py"
GENERATOR = REPO / "skills/omarchy-plugin-scaffold/scripts/new_plugin.py"

SPEC = importlib.util.spec_from_file_location("release_preflight", SCRIPT)
assert SPEC and SPEC.loader
PREFLIGHT = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = PREFLIGHT
SPEC.loader.exec_module(PREFLIGHT)


def run(command: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


class ReleasePreflightTests(unittest.TestCase):
    def fixture(self, parent: Path) -> Path:
        root = parent / "fixture"
        generated = run([
            sys.executable, str(GENERATOR), "--id", "io.github.example.fixture",
            "--name", "Fixture", "--kind", "bar-widget", "--version", "0.1.0",
            "--output", str(root),
        ])
        self.assertEqual(0, generated.returncode, generated.stdout + generated.stderr)
        for command in (
            ["git", "config", "user.name", "Fixture"],
            ["git", "config", "user.email", "fixture@example.invalid"],
            ["git", "add", "."],
            ["git", "commit", "-m", "fixture"],
        ):
            result = run(command, root)
            self.assertEqual(0, result.returncode, result.stderr)
        return root

    def release_directory(self, root: Path, source: dict[str, str]) -> Path:
        directory = root / "release"
        directory.mkdir()
        artifact = directory / "fixture.zip"
        artifact.write_bytes(b"deterministic fixture\n")
        source_document = {
            "schemaVersion": 1, "version": "0.1.0", "source": source, "files": [],
        }
        sbom = {
            "spdxVersion": "SPDX-2.3",
            "packages": [{"versionInfo": "0.1.0", "downloadLocation": "git+https://example.invalid/repo.git@" + source["commit"]}],
        }
        write_json(directory / "SOURCE-MANIFEST.json", source_document)
        write_json(directory / "SBOM.spdx.json", sbom)
        release = {
            "schemaVersion": 1,
            "version": "0.1.0",
            "source": source,
            "artifacts": [{"name": artifact.name, "bytes": artifact.stat().st_size, "sha256": digest(artifact)}],
            "releaseDocuments": [
                {"name": name, "bytes": (directory / name).stat().st_size, "sha256": digest(directory / name)}
                for name in ("SOURCE-MANIFEST.json", "SBOM.spdx.json")
            ],
        }
        write_json(directory / "RELEASE-MANIFEST.json", release)
        names = ("RELEASE-MANIFEST.json", "SBOM.spdx.json", "SOURCE-MANIFEST.json", "fixture.zip")
        (directory / "SHA256SUMS").write_text(
            "".join(f"{digest(directory / name)}  {name}\n" for name in names), encoding="ascii",
        )
        return directory

    def test_strict_json_rejects_duplicate_keys(self) -> None:
        with self.assertRaisesRegex(ValueError, "duplicate JSON key: version"):
            PREFLIGHT.strict_json_object('{"version":"0.1.0","version":"9.9.9"}')

    def test_release_directory_binds_identity_and_exact_checksum_coverage(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            source = {"repository": "https://github.com/example/fixture", "commit": "a" * 40, "tree": "b" * 40}
            directory = self.release_directory(root, source)
            items: list[tuple[str, str]] = []

            def add(level: str, code: str, _message: str, _detail: str = "") -> None:
                items.append((level, code))

            PREFLIGHT.validate_release_directory(directory, source, "0.1.0", add)
            self.assertEqual([], [item for item in items if item[0] == "error"])

            with (directory / "SHA256SUMS").open("a", encoding="ascii") as handle:
                handle.write(f"{'0' * 64}  fixture.zip\n")
            items.clear()
            PREFLIGHT.validate_release_directory(directory, source, "0.1.0", add)
            self.assertIn(("error", "checksums-format"), items)

            source_document = json.loads((directory / "SOURCE-MANIFEST.json").read_text(encoding="utf-8"))
            source_document["source"]["commit"] = "c" * 40
            write_json(directory / "SOURCE-MANIFEST.json", source_document)
            items.clear()
            PREFLIGHT.validate_release_directory(directory, source, "0.1.0", add)
            self.assertIn(("error", "source-identity"), items)

    def test_lightweight_tag_and_unbound_published_mode_fail_closed(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self.fixture(Path(temporary))
            self.assertEqual(0, run(["git", "tag", "v0.1.0"], root).returncode)
            result = run([sys.executable, str(SCRIPT), "--json", "--tag", "v0.1.0", str(root)], root)
            payload = json.loads(result.stdout)
            self.assertNotEqual(0, result.returncode)
            self.assertIn("tag-annotated", {item["code"] for item in payload["items"]})

            published = run([sys.executable, str(SCRIPT), "--json", "--published", str(root)], root)
            self.assertIn("published-arguments", {item["code"] for item in json.loads(published.stdout)["items"]})

    def test_published_historical_tag_requires_reachability_not_head_equality(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = self.fixture(Path(temporary))
            self.assertEqual(0, run(["git", "tag", "-a", "v0.1.0", "-m", "release"], root).returncode)
            (root / "README.md").write_text("post-release history\n", encoding="utf-8")
            self.assertEqual(0, run(["git", "add", "README.md"], root).returncode)
            self.assertEqual(0, run(["git", "commit", "-m", "after release"], root).returncode)
            commit = run(["git", "rev-parse", "v0.1.0^{}"], root).stdout.strip()
            tree = run(["git", "rev-parse", f"{commit}^{{tree}}"], root).stdout.strip()
            directory = self.release_directory(root, {"repository": "", "commit": commit, "tree": tree})
            result = run([
                sys.executable, str(SCRIPT), "--json", "--published", "--tag", "v0.1.0",
                "--release-dir", str(directory), str(root),
            ], root)
            codes = {item["code"] for item in json.loads(result.stdout)["items"]}
            self.assertNotIn("tag-head", codes)
            self.assertNotIn("published-reachability", codes)
            self.assertIn("origin-missing", codes)
            self.assertIn("remote-tag", codes)


if __name__ == "__main__":
    unittest.main()
