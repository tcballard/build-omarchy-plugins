#!/usr/bin/env python3
"""Check an Omarchy plugin demo harness without running or mutating it."""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


PREVIEWS = {"preview.png", "preview.jpg", "preview.jpeg", "preview.webp", "preview.avif"}
SENSITIVE = re.compile(r"(?:access[_-]?token|api[_-]?key|client[_-]?secret|password)\s*[=:]\s*[\"']?[^\s\"']+", re.IGNORECASE)


@dataclass
class Item:
    level: str
    code: str
    message: str
    path: str = ""


def relative(root: Path, path: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return str(path)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plugin_dir", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv or sys.argv[1:])
    root = args.plugin_dir.expanduser().resolve(strict=False)
    items: list[Item] = []

    def add(level: str, code: str, message: str, path: Path | None = None) -> None:
        items.append(Item(level, code, message, relative(root, path) if path else ""))

    runner = root / "demo" / "run"
    fixtures = root / "demo" / "fixtures"
    if not runner.is_file():
        add("error", "runner-missing", "demo/run is missing.", runner)
    else:
        text = runner.read_text(encoding="utf-8", errors="replace")
        if not os.access(runner, os.X_OK):
            add("error", "runner-executable", "demo/run is not executable.", runner)
        if "set -euo pipefail" not in text:
            add("warning", "strict-shell", "Shell demo should enable set -euo pipefail.", runner)
        live_markers = ("omarchy-shell", "omarchy-restart-shell", "quickshell", "hyprctl")
        if any(marker in text for marker in live_markers):
            required = {
                "trap": "Install cleanup traps before live-shell mutation.",
                "mktemp": "Use a collision-resistant temporary directory.",
                "cleanup": "Define a cleanup path.",
                "backup": "Preserve configuration/plugin state before replacement.",
            }
            for marker, message in required.items():
                if marker not in text.lower():
                    add("error", f"live-{marker}", message, runner)
            if "sleep 10" in text or "sleep 30" in text:
                add("warning", "fixed-wait", "Prefer a machine-readable readiness probe to long fixed sleeps.", runner)
            if "rm -rf" in text:
                add("warning", "recursive-delete", "Review every recursive deletion target in the demo cleanup.", runner)
        else:
            add("warning", "fixture-only", "Demo validates fixtures but does not yet prove a reversible live-shell screenshot path.", runner)

    if not fixtures.is_dir():
        add("error", "fixtures-missing", "demo/fixtures is missing.", fixtures)
    else:
        fixture_files = [path for path in fixtures.rglob("*") if path.is_file()]
        if not fixture_files:
            add("error", "fixtures-empty", "No committed fictional fixture exists.", fixtures)
        for path in fixture_files:
            data = path.read_text(encoding="utf-8", errors="replace")
            if SENSITIVE.search(data):
                add("error", "fixture-secret", "Fixture appears to contain a credential-like value.", path)
            if path.suffix.lower() == ".json":
                try:
                    json.loads(data)
                except json.JSONDecodeError as error:
                    add("error", "fixture-json", f"Fixture JSON is invalid: {error}", path)

    previews = [path for path in root.iterdir() if path.is_file() and path.name.lower() in PREVIEWS] if root.is_dir() else []
    if not previews:
        add("warning", "preview-missing", "No supported root marketplace preview image is present.")
    if len(previews) > 1:
        add("error", "preview-count", "Marketplace input should contain at most one root preview.", previews[1])
    for path in previews:
        if path.stat().st_size > 50 * 1024 * 1024:
            add("error", "preview-size", "Preview exceeds 50 MB.", path)

    result = {
        "plugin_dir": str(root),
        "ok": not any(item.level == "error" for item in items),
        "items": [asdict(item) for item in items],
        "mutated": False,
    }
    if args.as_json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        for item in items:
            location = f" ({item.path})" if item.path else ""
            print(f"{item.level.upper()} {item.code}: {item.message}{location}")
        print("PASS" if result["ok"] else "FAIL")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
