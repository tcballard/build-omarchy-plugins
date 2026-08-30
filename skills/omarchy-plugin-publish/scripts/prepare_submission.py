#!/usr/bin/env python3
"""Prepare, but never submit, an Omarchy community marketplace issue."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


CATEGORIES = {
    "Appearance", "Desktop", "Developer Tools", "Hardware", "Productivity",
    "System", "Widgets", "Other",
}
TAGS = {
    "ai", "bar", "games", "hyprland", "launcher", "media",
    "power-management", "quickshell", "security", "system", "workspaces",
}


def git_repository(root: Path) -> str:
    result = subprocess.run(
        ["git", "remote", "get-url", "origin"], cwd=root, text=True,
        capture_output=True, check=False,
    )
    if result.returncode != 0:
        return ""
    value = result.stdout.strip()
    ssh = re.fullmatch(r"git@github\.com:([^/]+)/(.+?)(?:\.git)?", value)
    if ssh:
        return f"https://github.com/{ssh.group(1)}/{ssh.group(2)}"
    if value.startswith("https://github.com/"):
        return value.removesuffix(".git").rstrip("/")
    return ""


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--plugin-dir", required=True, type=Path)
    parser.add_argument("--repository")
    parser.add_argument("--category", required=True, choices=sorted(CATEGORIES))
    parser.add_argument("--tag", action="append", required=True)
    parser.add_argument("--suggested-tag", default="_No response_")
    parser.add_argument("--maintainer-notes", default="_No response_")
    parser.add_argument("--output", type=Path, help="Write the issue body to this path.")
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    root = args.plugin_dir.expanduser().resolve(strict=True)
    manifest_path = root / "manifest.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as error:
        print(f"prepare_submission.py: invalid manifest: {error}", file=sys.stderr)
        return 2
    name = manifest.get("name")
    plugin_id = manifest.get("id")
    if not isinstance(name, str) or not name.strip() or not isinstance(plugin_id, str) or not plugin_id:
        print("prepare_submission.py: manifest name and id must be non-empty strings", file=sys.stderr)
        return 2
    if len(args.tag) < 1 or len(args.tag) > 3 or len(args.tag) != len(set(args.tag)):
        print("prepare_submission.py: choose one to three unique tags", file=sys.stderr)
        return 2
    invalid_tags = sorted(set(args.tag) - TAGS)
    if invalid_tags:
        print(f"prepare_submission.py: invalid tags: {', '.join(invalid_tags)}", file=sys.stderr)
        return 2
    repository = (args.repository or git_repository(root)).removesuffix(".git").rstrip("/")
    if not re.fullmatch(r"https://github\.com/[^/]+/[^/]+", repository):
        print("prepare_submission.py: provide a GitHub repository root URL", file=sys.stderr)
        return 2

    title = f"[Plugin]: {name.strip()}"
    body = f"""### Repository URL

{repository}

### Category

{args.category}

### Tags

{', '.join(args.tag)}

### Suggest a missing tag

{args.suggested_tag}

### Maintainer notes

{args.maintainer_notes}

### Submission checklist

- [x] The repository is public and contains installation and removal instructions.
- [x] I have documented the plugin license and any external dependencies.
- [x] I confirm that I own or have permission to submit this plugin and its preview assets.
- [x] The plugin does not overwrite user configuration without explicit consent.
- [x] I understand that approval is for listing and is not a security review.
"""
    if args.output:
        args.output.expanduser().resolve(strict=False).parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(body, encoding="utf-8", newline="\n")
    result = {
        "title": title,
        "body": body,
        "plugin_id": plugin_id,
        "repository": repository,
        "submitted": False,
        "requires_owner_approval": True,
    }
    if args.as_json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(title)
        print()
        print(body, end="")
        if args.output:
            print(f"\nBody written to {args.output}", file=sys.stderr)
        print("\nNot submitted. Show this exact title and body to the owner for explicit approval.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
