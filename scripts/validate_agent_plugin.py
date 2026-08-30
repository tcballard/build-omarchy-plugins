#!/usr/bin/env python3
"""Validate the provider-neutral Agent Plugin package without network access."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


SCHEMA = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
ALLOWED_FIELDS = {
    "$schema", "name", "version", "description", "author", "homepage",
    "repository", "license", "keywords", "extensions",
}
NAME_PATTERN = re.compile(r"^[a-z0-9](?:[a-z0-9.-]{0,62}[a-z0-9])?$")
SEMVER_PATTERN = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


def load_manifest(path: Path) -> tuple[dict[str, object] | None, list[str]]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None, ["missing root plugin.json"]
    except (OSError, json.JSONDecodeError) as error:
        return None, [f"cannot read plugin.json: {error}"]
    if not isinstance(value, dict):
        return None, ["plugin.json must contain a JSON object"]
    return value, []


def validate_manifest(manifest: dict[str, object]) -> list[str]:
    errors: list[str] = []
    unknown = sorted(set(manifest) - ALLOWED_FIELDS)
    if unknown:
        errors.append(f"unsupported plugin.json fields: {', '.join(unknown)}")
    if manifest.get("$schema") != SCHEMA:
        errors.append(f"$schema must be {SCHEMA}")
    name = manifest.get("name")
    if not isinstance(name, str) or not NAME_PATTERN.fullmatch(name) or "--" in name or ".." in name:
        errors.append("name must be 1-64 lowercase letters, digits, hyphens, or periods without doubled separators")
    version = manifest.get("version")
    if version is not None and (not isinstance(version, str) or not SEMVER_PATTERN.fullmatch(version)):
        errors.append("version must be semantic when present")
    for field in ("description", "homepage", "repository", "license"):
        value = manifest.get(field)
        if value is not None and not isinstance(value, str):
            errors.append(f"{field} must be a string")
    author = manifest.get("author")
    if author is not None:
        if not isinstance(author, dict):
            errors.append("author must be an object")
        else:
            unknown_author = sorted(set(author) - {"name", "email", "url"})
            if unknown_author:
                errors.append(f"unsupported author fields: {', '.join(unknown_author)}")
            if any(not isinstance(value, str) for value in author.values()):
                errors.append("author values must be strings")
    keywords = manifest.get("keywords")
    if keywords is not None and (
        not isinstance(keywords, list) or any(not isinstance(item, str) for item in keywords)
    ):
        errors.append("keywords must be an array of strings")
    extensions = manifest.get("extensions")
    if extensions is not None and not isinstance(extensions, dict):
        errors.append("extensions must be an object")
    return errors


def validate_tree(root: Path) -> list[str]:
    errors: list[str] = []
    skills = root / "skills"
    if not skills.is_dir():
        return ["missing root skills directory"]
    skill_dirs = sorted(path for path in skills.iterdir() if path.is_dir())
    if not skill_dirs:
        errors.append("skills directory must contain at least one skill")
    for path in root.rglob("*"):
        if path.is_symlink():
            errors.append(f"portable package must not contain symlink: {path.relative_to(root)}")
    for metadata in skills.glob("*/agents/openai.yaml"):
        errors.append(
            "portable skills must keep OpenAI metadata in the OpenAI adapter: "
            f"{metadata.relative_to(root)}"
        )
    for skill in skill_dirs:
        if not (skill / "SKILL.md").is_file():
            errors.append(f"skill directory is missing SKILL.md: {skill.name}")
    return errors


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", nargs="?", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv or sys.argv[1:])
    root = (args.root or Path(__file__).resolve().parent.parent).expanduser().resolve(strict=False)
    manifest, errors = load_manifest(root / "plugin.json")
    if manifest is not None:
        errors.extend(validate_manifest(manifest))
    errors.extend(validate_tree(root))

    validator = root / "scripts" / "validate_skills.py"
    if not errors and validator.is_file():
        result = subprocess.run(
            [sys.executable, str(validator), str(root / "skills")],
            cwd=root,
            text=True,
            capture_output=True,
            check=False,
        )
        if result.returncode:
            errors.append((result.stdout + result.stderr).strip() or "skill validation failed")

    payload = {
        "ok": not errors,
        "root": str(root),
        "schema": manifest.get("$schema") if manifest else None,
        "name": manifest.get("name") if manifest else None,
        "version": manifest.get("version") if manifest else None,
        "skills": len([path for path in (root / "skills").glob("*") if path.is_dir()]),
        "errors": errors,
    }
    if args.as_json:
        print(json.dumps(payload, indent=2))
    elif errors:
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
    else:
        print(f"Valid Agent Plugin: {payload['name']} {payload['version']} ({payload['skills']} skills)")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
