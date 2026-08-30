#!/usr/bin/env python3
"""Create deterministic portable, OpenAI, and reviewer-material archives."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import stat
import subprocess
import sys
import zipfile
from pathlib import Path
from typing import Iterable


FIXED_TIME = (2026, 8, 30, 0, 0, 0)
EXCLUDED_PARTS = {".git", "__pycache__", ".pytest_cache", ".ruff_cache", "dist"}


def files_under(root: Path) -> Iterable[Path]:
    for path in sorted(root.rglob("*")):
        if not path.is_file() or path.is_symlink():
            continue
        if any(part in EXCLUDED_PARTS for part in path.parts):
            continue
        if path.name in {".DS_Store"} or path.suffix in {".pyc", ".pyo"}:
            continue
        yield path


def add_file(archive: zipfile.ZipFile, source: Path, name: str) -> None:
    data = source.read_bytes()
    info = zipfile.ZipInfo(name, FIXED_TIME)
    mode = 0o755 if os.access(source, os.X_OK) else 0o644
    info.external_attr = (stat.S_IFREG | mode) << 16
    info.compress_type = zipfile.ZIP_DEFLATED
    info.create_system = 3
    archive.writestr(info, data)


def make_archive(destination: Path, mappings: Iterable[tuple[Path, str]]) -> None:
    with zipfile.ZipFile(destination, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for source, name in sorted(mappings, key=lambda item: item[1]):
            add_file(archive, source, name)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path)
    args = parser.parse_args(argv or sys.argv[1:])
    repo = Path(__file__).resolve().parent.parent
    plugin = repo / "plugins" / "build-omarchy-plugins"
    portable_manifest = json.loads((repo / "plugin.json").read_text(encoding="utf-8"))
    openai_manifest = json.loads((plugin / ".codex-plugin" / "plugin.json").read_text(encoding="utf-8"))
    version = portable_manifest["version"]
    if openai_manifest.get("version") != version:
        print("portable and OpenAI plugin versions must match", file=sys.stderr)
        return 1
    output = (args.output_dir or repo / "dist").expanduser().resolve(strict=False)
    output.mkdir(parents=True, exist_ok=True)

    validations = [
        [sys.executable, str(repo / "scripts" / "validate_agent_plugin.py"), str(repo)],
        [sys.executable, str(repo / "scripts" / "sync_openai_adapter.py"), "--check"],
        [sys.executable, str(repo / "scripts" / "validate_codex_plugin.py"), str(plugin)],
        [
            sys.executable,
            str(repo / "scripts" / "validate_skills.py"),
            "--require-openai-metadata",
            str(plugin / "skills"),
        ],
    ]
    for command in validations:
        result = subprocess.run(command, cwd=repo, text=True, capture_output=True, check=False)
        if result.returncode:
            print(result.stdout, end="", file=sys.stderr)
            print(result.stderr, end="", file=sys.stderr)
            return result.returncode

    portable_archive = output / f"build-omarchy-plugins-agent-plugin-{version}.zip"
    plugin_archive = output / f"build-omarchy-plugins-plugin-{version}.zip"
    skills_archive = output / f"build-omarchy-plugins-skills-{version}.zip"
    reviewer_archive = output / f"build-omarchy-plugins-submission-{version}.zip"

    portable_mappings = [(repo / "plugin.json", "build-omarchy-plugins/plugin.json")]
    portable_mappings.extend(
        (path, f"build-omarchy-plugins/skills/{path.relative_to(repo / 'skills').as_posix()}")
        for path in files_under(repo / "skills")
    )
    portable_mappings.extend(
        (repo / name, f"build-omarchy-plugins/{name}")
        for name in (
            "README.md", "PORTABILITY.md", "LICENSE", "SECURITY.md",
            "PRIVACY.md", "TERMS.md", "SUPPORT.md",
        )
    )
    make_archive(portable_archive, portable_mappings)
    make_archive(plugin_archive, ((path, f"build-omarchy-plugins/{path.relative_to(plugin).as_posix()}") for path in files_under(plugin)))
    skills_root = plugin / "skills"
    make_archive(skills_archive, ((path, f"skills/{path.relative_to(skills_root).as_posix()}") for path in files_under(skills_root)))

    reviewer_files = [path for path in files_under(repo / "submission")]
    reviewer_files += [repo / name for name in ("PRIVACY.md", "TERMS.md", "SUPPORT.md", "SECURITY.md")]
    reviewer_files += [plugin / "assets" / name for name in ("app-icon.png", "workflow.png")]
    make_archive(reviewer_archive, (
        (path, path.relative_to(repo).as_posix() if repo in path.parents else path.name)
        for path in reviewer_files if path.is_file()
    ))

    archives = [portable_archive, plugin_archive, skills_archive, reviewer_archive]
    sums = output / "SHA256SUMS"
    sums.write_text("".join(f"{sha256(path)}  {path.name}\n" for path in archives), encoding="utf-8", newline="\n")
    print(json.dumps({
        "version": version,
        "artifacts": [{"path": str(path), "sha256": sha256(path), "bytes": path.stat().st_size} for path in archives],
        "checksums": str(sums),
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
