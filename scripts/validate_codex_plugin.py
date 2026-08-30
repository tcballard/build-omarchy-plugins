#!/usr/bin/env python3
"""Offline preflight for the OpenAI plugin distribution adapter."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path, PurePosixPath


SEMVER = re.compile(r"^\d+\.\d+\.\d+(?:-[0-9A-Za-z.-]+)?(?:\+[0-9A-Za-z.-]+)?$")


def resolve_inside(root: Path, value: str) -> Path | None:
    if not isinstance(value, str) or not value.startswith("./"):
        return None
    posix = PurePosixPath(value)
    if ".." in posix.parts:
        return None
    path = (root / value).resolve(strict=False)
    try:
        path.relative_to(root.resolve())
    except ValueError:
        return None
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plugin_dir", type=Path)
    args = parser.parse_args(argv or sys.argv[1:])
    root = args.plugin_dir.resolve()
    manifest_path = root / ".codex-plugin" / "plugin.json"
    errors: list[str] = []
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"ERROR: invalid plugin manifest: {error}", file=sys.stderr)
        return 1
    if not isinstance(manifest, dict):
        errors.append("plugin manifest must be an object")
        manifest = {}
    if manifest.get("name") != root.name:
        errors.append("manifest name must match plugin directory")
    if not isinstance(manifest.get("version"), str) or not SEMVER.fullmatch(manifest["version"]):
        errors.append("manifest version must be strict semver")
    for key in ("name", "description"):
        if not isinstance(manifest.get(key), str) or not manifest[key].strip():
            errors.append(f"manifest {key} must be non-empty")
    if not isinstance(manifest.get("author"), dict) or not manifest["author"].get("name"):
        errors.append("manifest author.name is required")
    interface = manifest.get("interface")
    if not isinstance(interface, dict):
        errors.append("manifest interface object is required")
        interface = {}
    for key in ("displayName", "shortDescription", "longDescription", "developerName", "category"):
        if not isinstance(interface.get(key), str) or not interface[key].strip():
            errors.append(f"interface.{key} is required")
    prompts = interface.get("defaultPrompt")
    if not isinstance(prompts, list) or not 1 <= len(prompts) <= 3 or any(not isinstance(item, str) or len(item) > 128 for item in prompts):
        errors.append("interface.defaultPrompt must contain 1-3 strings of at most 128 characters")
    for url_key in ("websiteURL", "privacyPolicyURL", "termsOfServiceURL"):
        if not isinstance(interface.get(url_key), str) or not interface[url_key].startswith("https://"):
            errors.append(f"interface.{url_key} must be an absolute HTTPS URL")
    for asset_key in ("composerIcon", "logo"):
        path = resolve_inside(root, interface.get(asset_key, ""))
        if path is None or not path.is_file():
            errors.append(f"interface.{asset_key} must point to an existing in-plugin asset")
    screenshots = interface.get("screenshots", [])
    if not isinstance(screenshots, list):
        errors.append("interface.screenshots must be an array")
    else:
        for item in screenshots:
            path = resolve_inside(root, item)
            if path is None or path.suffix.lower() != ".png" or not path.is_file():
                errors.append(f"invalid screenshot asset: {item}")
    skills = resolve_inside(root, manifest.get("skills", ""))
    if skills is None or not skills.is_dir():
        errors.append("manifest skills path must point to the bundled skills directory")
    if "mcpServers" in manifest or "apps" in manifest:
        errors.append("skills-only plugin must not declare absent MCP or app companions")
    for path in root.rglob("*"):
        if path.is_symlink():
            errors.append(f"symlink not allowed in plugin archive: {path.relative_to(root)}")
        if path.is_file() and "[TODO:" in path.read_text(encoding="utf-8", errors="ignore"):
            errors.append(f"unfinished scaffold placeholder: {path.relative_to(root)}")
    for error in errors:
        print(f"ERROR: {error}", file=sys.stderr)
    if errors:
        return 1
    print(f"VALID: {manifest['name']} {manifest['version']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
