#!/usr/bin/env python3
"""Read-only diagnostics for an Omarchy Quattro shell plugin."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


@dataclass
class Check:
    status: str
    code: str
    message: str
    detail: str = ""


def run(command: list[str], timeout: float = 8.0) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, text=True, capture_output=True, timeout=timeout, check=False)


def validator_path() -> Path:
    skills_dir = Path(__file__).resolve().parents[2]
    return skills_dir / "omarchy-plugin-test" / "scripts" / "validate_plugin.py"


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plugin_dir", type=Path)
    parser.add_argument("--live", action="store_true", help="Probe the running Omarchy shell and discovery state.")
    parser.add_argument("--json", action="store_true", dest="as_json")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    root = args.plugin_dir.expanduser().resolve(strict=False)
    checks: list[Check] = []

    if root.is_dir():
        checks.append(Check("pass", "plugin-directory", "Plugin directory exists.", str(root)))
    else:
        checks.append(Check("fail", "plugin-directory", "Plugin directory does not exist.", str(root)))

    manifest: dict[str, Any] | None = None
    manifest_path = root / "manifest.json"
    if manifest_path.is_file():
        try:
            value = json.loads(manifest_path.read_text(encoding="utf-8"))
            manifest = value if isinstance(value, dict) else None
            if manifest is None:
                raise ValueError("root value is not an object")
            checks.append(Check("pass", "manifest-json", "manifest.json is valid JSON."))
        except (OSError, UnicodeDecodeError, json.JSONDecodeError, ValueError) as error:
            checks.append(Check("fail", "manifest-json", "manifest.json could not be parsed.", str(error)))
    else:
        checks.append(Check("fail", "manifest-json", "Root manifest.json is missing."))

    portable = validator_path()
    if portable.is_file() and root.is_dir():
        result = run([sys.executable, str(portable), "--json", str(root)])
        try:
            payload = json.loads(result.stdout)
            checks.append(Check(
                "pass" if result.returncode == 0 else "fail",
                "portable-validation",
                "Portable manifest validation passed." if result.returncode == 0 else "Portable manifest validation failed.",
                json.dumps(payload.get("errors", []), ensure_ascii=False),
            ))
        except json.JSONDecodeError:
            checks.append(Check("fail", "portable-validation", "Portable validator returned unreadable output.", result.stderr.strip()))
    else:
        checks.append(Check("warn", "portable-validation", "Bundled portable validator was not found."))

    required_commands = ("git", "jq", "omarchy", "omarchy-shell", "quickshell")
    for command in required_commands:
        location = shutil.which(command)
        status = "pass" if location else ("warn" if command in {"git", "jq"} else "skip")
        checks.append(Check(status, f"command-{command}", f"Command '{command}' {'is available' if location else 'is not available'}.", location or ""))

    if shutil.which("omarchy") and root.is_dir():
        result = run(["omarchy", "plugin", "validate", str(root)])
        checks.append(Check(
            "pass" if result.returncode == 0 else "fail",
            "official-validation",
            "Installed Omarchy validation passed." if result.returncode == 0 else "Installed Omarchy validation failed.",
            (result.stderr or result.stdout).strip()[-2000:],
        ))
    else:
        checks.append(Check("skip", "official-validation", "Installed Omarchy validator is unavailable."))

    plugin_id = str(manifest.get("id", "")) if manifest else ""
    if plugin_id:
        installed = Path(os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config"))) / "omarchy" / "plugins" / plugin_id
        if installed.exists() or installed.is_symlink():
            kind = "symlink" if installed.is_symlink() else ("git checkout" if (installed / ".git").is_dir() else "directory")
            checks.append(Check("pass", "installed-path", f"Plugin is present in the user plugin directory as a {kind}.", str(installed)))
        else:
            checks.append(Check("skip", "installed-path", "Plugin is not installed in the user plugin directory.", str(installed)))

    if args.live:
        if not shutil.which("omarchy-shell"):
            checks.append(Check("fail", "shell-ping", "--live requested but omarchy-shell is unavailable."))
        else:
            ping = run(["omarchy-shell", "shell", "ping"], timeout=3.0)
            checks.append(Check(
                "pass" if ping.returncode == 0 else "fail",
                "shell-ping",
                "Running shell answered ping." if ping.returncode == 0 else "Running shell did not answer ping.",
                (ping.stderr or ping.stdout).strip(),
            ))
            if plugin_id and shutil.which("omarchy"):
                listed = run(["omarchy", "plugin", "list", "--json"])
                found = False
                detail = (listed.stderr or listed.stdout).strip()
                if listed.returncode == 0:
                    try:
                        entries = json.loads(listed.stdout)
                        entry = next((item for item in entries if str(item.get("id", "")) == plugin_id), None)
                        found = entry is not None
                        detail = json.dumps(entry, ensure_ascii=False) if entry else ""
                    except (json.JSONDecodeError, TypeError):
                        pass
                checks.append(Check(
                    "pass" if found else "fail",
                    "plugin-discovery",
                    "Running shell discovered the plugin." if found else "Running shell did not report the plugin.",
                    detail[-2000:],
                ))

    result = {
        "plugin_dir": str(root),
        "plugin_id": plugin_id,
        "live": args.live,
        "mutated": False,
        "checks": [asdict(check) for check in checks],
        "ok": not any(check.status == "fail" for check in checks),
    }
    if args.as_json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        for check in checks:
            detail = f" — {check.detail}" if check.detail else ""
            print(f"{check.status.upper():4} {check.code}: {check.message}{detail}")
        print("No configuration or process state was changed.")
    return 0 if result["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
