#!/usr/bin/env python3
"""Check or refresh the OpenAI plugin's vendored copy of the portable skills."""

from __future__ import annotations

import argparse
import filecmp
import json
import os
import shutil
import stat
import sys
import tempfile
from pathlib import Path


IGNORED_NAMES = {"__pycache__", ".DS_Store"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}


def is_ignored(path: Path) -> bool:
    return any(part in IGNORED_NAMES for part in path.parts) or path.suffix in IGNORED_SUFFIXES


def portable_files(root: Path) -> dict[Path, Path]:
    files: dict[Path, Path] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if is_ignored(relative):
            continue
        if path.is_symlink():
            raise ValueError(f"skill package contains a symlink: {relative}")
        if path.is_file():
            files[relative] = path
    return files


def adapter_core_files(root: Path) -> dict[Path, Path]:
    files = portable_files(root)
    return {
        relative: path
        for relative, path in files.items()
        if not (len(relative.parts) >= 3 and relative.parts[1:] == ("agents", "openai.yaml"))
    }


def compare(source: Path, destination: Path) -> list[str]:
    source_files = portable_files(source)
    destination_files = adapter_core_files(destination)
    problems: list[str] = []
    for relative in sorted(set(source_files) - set(destination_files)):
        problems.append(f"missing from OpenAI adapter: {relative}")
    for relative in sorted(set(destination_files) - set(source_files)):
        problems.append(f"unexpected OpenAI adapter file: {relative}")
    for relative in sorted(set(source_files) & set(destination_files)):
        left = source_files[relative]
        right = destination_files[relative]
        if not filecmp.cmp(left, right, shallow=False):
            problems.append(f"content differs: {relative}")
        left_exec = bool(left.stat().st_mode & stat.S_IXUSR)
        right_exec = bool(right.stat().st_mode & stat.S_IXUSR)
        if left_exec != right_exec:
            problems.append(f"executable mode differs: {relative}")
    return problems


def copy_portable_tree(source: Path, destination: Path, adapter: Path) -> None:
    for relative, path in portable_files(source).items():
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
    for metadata in sorted(adapter.glob("*/agents/openai.yaml")):
        relative = metadata.relative_to(adapter)
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(metadata, target)


def write_adapter(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{destination.name}-", dir=destination.parent))
    backup = destination.parent / f".{destination.name}.backup"
    try:
        copy_portable_tree(source, temporary, destination)
        if backup.exists():
            raise RuntimeError(f"refusing to overwrite stale backup: {backup}")
        if destination.exists():
            destination.rename(backup)
        temporary.rename(destination)
        if backup.exists():
            shutil.rmtree(backup)
    except Exception:
        if destination.exists() and backup.exists():
            shutil.rmtree(destination)
            backup.rename(destination)
        elif backup.exists() and not destination.exists():
            backup.rename(destination)
        if temporary.exists():
            shutil.rmtree(temporary)
        raise


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--write", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv or sys.argv[1:])
    repo = Path(__file__).resolve().parent.parent
    source = repo / "skills"
    destination = repo / "plugins" / "build-omarchy-plugins" / "skills"

    try:
        if args.write:
            write_adapter(source, destination)
        problems = compare(source, destination)
    except (OSError, ValueError, RuntimeError) as error:
        problems = [str(error)]

    payload = {
        "ok": not problems,
        "source": str(source),
        "destination": str(destination),
        "problems": problems,
    }
    if args.as_json:
        print(json.dumps(payload, indent=2))
    elif problems:
        for problem in problems:
            print(f"error: {problem}", file=sys.stderr)
    else:
        action = "refreshed" if args.write else "matches"
        print(f"OpenAI adapter {action} the portable skill source.")
    return 0 if not problems else 1


if __name__ == "__main__":
    raise SystemExit(main())
