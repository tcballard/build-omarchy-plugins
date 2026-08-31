from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path, PurePosixPath


REPO = Path(__file__).resolve().parent.parent
PACKAGER = REPO / "scripts/package_submission.py"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


class ReleaseArtifactTests(unittest.TestCase):
    def build(self, output: Path) -> dict[str, object]:
        result = subprocess.run(
            [sys.executable, str(PACKAGER), "--output-dir", str(output), "--git-tree", "HEAD"],
            cwd=REPO,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, result.returncode, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_two_builds_are_byte_identical_and_archives_are_safe(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            first, second = root / "first", root / "second"
            report = self.build(first)
            second_report = self.build(second)
            self.assertEqual(report["source"], second_report["source"])
            self.assertEqual(report["files"], second_report["files"])
            for name in report["files"]:
                self.assertEqual(sha256(first / name), sha256(second / name), name)
            for archive_path in first.glob("*.zip"):
                with zipfile.ZipFile(archive_path) as archive:
                    names = archive.namelist()
                    self.assertEqual(len(names), len({name.casefold() for name in names}))
                    for info in archive.infolist():
                        path = PurePosixPath(info.filename)
                        self.assertFalse(path.is_absolute())
                        self.assertNotIn("..", path.parts)
                        self.assertNotEqual(0o120000, (info.external_attr >> 16) & 0o170000)

    def test_manifests_and_checksums_bind_the_exact_commit(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            output = Path(temporary) / "dist"
            report = self.build(output)
            commit = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=REPO, text=True, capture_output=True, check=True
            ).stdout.strip()
            manifest = json.loads((output / "RELEASE-MANIFEST.json").read_text(encoding="utf-8"))
            source = json.loads((output / "SOURCE-MANIFEST.json").read_text(encoding="utf-8"))
            sbom = json.loads((output / "SBOM.spdx.json").read_text(encoding="utf-8"))
            self.assertEqual(commit, manifest["source"]["commit"])
            self.assertEqual(commit, source["source"]["commit"])
            self.assertEqual("SPDX-2.3", sbom["spdxVersion"])
            self.assertTrue(sbom["packages"][0]["downloadLocation"].endswith("@" + commit))
            expected = {}
            for line in (output / "SHA256SUMS").read_text(encoding="ascii").splitlines():
                digest, name = line.split("  ", 1)
                expected[name] = digest
            self.assertEqual(7, len(expected))
            for name, digest in expected.items():
                self.assertEqual(digest, sha256(output / name))
            self.assertEqual(8, len(report["files"]))

    def test_require_clean_rejects_ambient_changes(self) -> None:
        destination = REPO / "dist-test-never-created"
        result = subprocess.run(
            [sys.executable, str(PACKAGER), "--output-dir", str(destination), "--require-clean"],
            cwd=REPO,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(1, result.returncode)
        self.assertIn("dirty or untracked", result.stderr)
        self.assertFalse(destination.exists())


if __name__ == "__main__":
    unittest.main()
