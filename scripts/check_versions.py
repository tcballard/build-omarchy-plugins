#!/usr/bin/env python3
"""Require every release-facing version surface to match VERSION."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


SEMVER = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")


def check(repo: Path, tag: str | None = None) -> list[str]:
    errors: list[str] = []
    try:
        version = (repo / "VERSION").read_text(encoding="utf-8").strip()
    except OSError as error:
        return [f"cannot read VERSION: {error}"]
    if not SEMVER.fullmatch(version):
        errors.append("VERSION must contain one strict semantic version")

    json_surfaces = (
        (repo / "plugin.json", "version"),
        (repo / "plugins/build-omarchy-plugins/.codex-plugin/plugin.json", "version"),
        (repo / "submission/evals.json", "version"),
    )
    for path, field in json_surfaces:
        try:
            value = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as error:
            errors.append(f"cannot read {path.relative_to(repo)}: {error}")
            continue
        if not isinstance(value, dict) or value.get(field) != version:
            errors.append(f"{path.relative_to(repo)} {field} must equal {version}")

    text_surfaces = (
        repo / "CHANGELOG.md",
        repo / "submission/README.md",
        repo / "submission/portal-field-map.md",
        repo / "submission/release-notes.md",
    )
    for path in text_surfaces:
        try:
            text = path.read_text(encoding="utf-8")
        except OSError as error:
            errors.append(f"cannot read {path.relative_to(repo)}: {error}")
            continue
        if version not in text:
            errors.append(f"{path.relative_to(repo)} does not name {version}")

    if tag is not None and tag != f"v{version}":
        errors.append(f"tag must be v{version}, got {tag}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("repo", nargs="?", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--tag")
    args = parser.parse_args()
    errors = check(args.repo.resolve(), args.tag)
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"Version surfaces agree: {(args.repo / 'VERSION').read_text(encoding='utf-8').strip()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
