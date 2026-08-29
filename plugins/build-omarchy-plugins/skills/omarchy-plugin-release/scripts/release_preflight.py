#!/usr/bin/env python3
"""Preflight a public Omarchy plugin release without publishing it."""

from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class Item:
    level: str
    code: str
    message: str
    detail: str = ""


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)


def validator_path() -> Path:
    return Path(__file__).resolve().parents[2] / "omarchy-plugin-test" / "scripts" / "validate_plugin.py"


def normalize_remote(value: str) -> str:
    value = value.strip()
    match = re.fullmatch(r"git@github\.com:([^/]+)/(.+?)(?:\.git)?", value)
    if match:
        return f"https://github.com/{match.group(1)}/{match.group(2)}"
    if value.startswith("https://github.com/"):
        return value.removesuffix(".git").rstrip("/")
    return value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plugin_dir", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--allow-dirty", action="store_true")
    args = parser.parse_args(argv or sys.argv[1:])
    root = args.plugin_dir.expanduser().resolve(strict=False)
    items: list[Item] = []

    def add(level: str, code: str, message: str, detail: str = "") -> None:
        items.append(Item(level, code, message, detail))

    validator = validator_path()
    if not validator.is_file():
        add("error", "validator-missing", "Bundled Omarchy validator is missing.", str(validator))
    elif root.is_dir():
        result = run([sys.executable, str(validator), "--json", "--security", "--publish", "--strict", str(root)], root)
        try:
            payload = json.loads(result.stdout)
            for error in payload.get("errors", []):
                add("error", error["code"], error["message"], error.get("path", ""))
            for warning in payload.get("warnings", []):
                add("warning", warning["code"], warning["message"], warning.get("path", ""))
            security = payload.get("security", {})
            for finding in security.get("findings", []):
                add("error", finding["code"], finding["message"], finding.get("path", ""))
            for capability in security.get("capabilities", []):
                add("warning", capability["code"], capability["message"], capability.get("path", ""))
        except json.JSONDecodeError:
            add("error", "validator-output", "Bundled validator returned unreadable output.", result.stderr.strip())

    if not root.is_dir():
        add("error", "plugin-directory", "Plugin directory does not exist.", str(root))
    else:
        git = run(["git", "rev-parse", "--show-toplevel"], root)
        if git.returncode != 0:
            add("error", "git-repository", "Plugin must be in a Git repository.", git.stderr.strip())
        else:
            top = Path(git.stdout.strip()).resolve()
            if top != root:
                add("warning", "repository-root", "Plugin directory is not the Git repository root.", str(top))
            status = run(["git", "status", "--porcelain"], root)
            if status.stdout.strip() and not args.allow_dirty:
                add("error", "dirty-tree", "Git working tree is not clean.", status.stdout.strip()[:2000])
            head = run(["git", "rev-parse", "HEAD"], root)
            if head.returncode == 0 and re.fullmatch(r"[0-9a-f]{40}\n?", head.stdout):
                add("info", "release-sha", "Release candidate full SHA.", head.stdout.strip())
            else:
                add("error", "release-sha", "Could not resolve a full release SHA.", head.stderr.strip())
            remote = run(["git", "remote", "get-url", "origin"], root)
            if remote.returncode != 0:
                add("error", "origin-missing", "A public GitHub origin is required for marketplace release.")
            else:
                normalized = normalize_remote(remote.stdout)
                if not re.fullmatch(r"https://github\.com/[^/]+/[^/]+", normalized):
                    add("error", "origin-github", "Origin is not a GitHub repository root URL.", normalized)
                else:
                    add("info", "origin", "Release repository.", normalized)

        tests = root / "tests" / "run"
        if not tests.is_file():
            add("error", "tests-run", "tests/run is required for reproducible portable checks.")
        elif not os.access(tests, os.X_OK):
            add("error", "tests-executable", "tests/run must be executable.")
        workflow = root / ".github" / "workflows"
        if not workflow.is_dir() or not any(workflow.glob("*.yml")) and not any(workflow.glob("*.yaml")):
            add("warning", "ci-missing", "No GitHub Actions workflow was found.")
        preview = [path for path in root.iterdir() if path.name.lower() in {"preview.png", "preview.jpg", "preview.jpeg", "preview.webp", "preview.avif"}]
        if not preview:
            add("warning", "preview-missing", "Visual plugins should include a current root marketplace preview.")

    ok = not any(item.level == "error" for item in items)
    result_payload = {
        "plugin_dir": str(root),
        "ok": ok,
        "items": [asdict(item) for item in items],
        "mutated": False,
        "disclaimer": "Static checks are evidence, not a security audit or compatibility guarantee.",
    }
    if args.as_json:
        print(json.dumps(result_payload, indent=2, sort_keys=True))
    else:
        for item in items:
            detail = f" — {item.detail}" if item.detail else ""
            print(f"{item.level.upper()} {item.code}: {item.message}{detail}")
        print("READY" if ok else "NOT READY")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
