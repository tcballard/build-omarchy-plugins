#!/usr/bin/env python3
"""Collect bounded host evidence without confusing self-reported hooks with verification."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
import uuid
from pathlib import Path
from typing import Any

from doctor_agent_skills import HOSTS, inspect
from install_agent_skills import inventory, snapshot_tree


MAX_OUTPUT = 2 * 1024 * 1024
TIMEOUT = 300
PROBE_SKILL = "omarchy-plugin-design"
PROBE_TITLE = "Omarchy Plugin Design"


def git_attribution(source: Path) -> dict[str, Any]:
    command = ["git", "-C", str(source), "rev-parse", "--show-toplevel", "HEAD", "HEAD^{tree}"]
    result = subprocess.run(command, text=True, capture_output=True, check=False, timeout=10)
    if result.returncode != 0:
        return {"stable": False, "reason": "source is not in a Git commit"}
    root, commit, tree = result.stdout.splitlines()[:3]
    relative = os.path.relpath(source, root)
    dirty = subprocess.run(
        ["git", "-C", root, "status", "--porcelain=v1", "--untracked-files=all", "--", relative],
        text=True, capture_output=True, check=False, timeout=10,
    )
    stable = dirty.returncode == 0 and not dirty.stdout.strip()
    return {
        "stable": stable,
        "repository": root,
        "commit": commit,
        "tree": tree,
        "sourcePath": relative,
        "reason": None if stable else "source path has uncommitted or untracked content",
    }


def bounded_run(command: list[str], cwd: Path, environment: dict[str, str] | None = None, timeout: int = TIMEOUT) -> dict[str, Any]:
    try:
        result = subprocess.run(
            command,
            cwd=cwd,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=timeout,
        )
        stdout, stderr = result.stdout[:MAX_OUTPUT], result.stderr[:MAX_OUTPUT]
        return {
            "exitCode": result.returncode,
            "stdoutSha256": hashlib.sha256(stdout).hexdigest(),
            "stderrSha256": hashlib.sha256(stderr).hexdigest(),
            "stdoutTruncated": len(result.stdout) > MAX_OUTPUT,
            "stderrTruncated": len(result.stderr) > MAX_OUTPUT,
            "_stdout": stdout,
        }
    except (OSError, subprocess.TimeoutExpired) as error:
        return {"exitCode": None, "error": str(error), "_stdout": b""}


def walk_json(value: Any):
    yield value
    if isinstance(value, dict):
        for child in value.values():
            yield from walk_json(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_json(child)


def parse_opencode(stdout: bytes, nonce: str) -> dict[str, Any]:
    events: list[Any] = []
    parse_errors = 0
    for line in stdout.decode("utf-8", "replace").splitlines():
        if not line.strip():
            continue
        try:
            events.append(json.loads(line))
        except json.JSONDecodeError:
            parse_errors += 1
    skill_call = False
    for event in events:
        for value in walk_json(event):
            if not isinstance(value, dict):
                continue
            tool = value.get("tool") or value.get("toolName") or value.get("name")
            arguments = value.get("args") or value.get("arguments") or value.get("input")
            if tool == "skill" and isinstance(arguments, dict) and arguments.get("name") == PROBE_SKILL:
                skill_call = True
    rendered = json.dumps(events, sort_keys=True)
    return {
        "jsonEvents": len(events),
        "parseErrors": parse_errors,
        "skillToolObserved": skill_call,
        "nonceObserved": nonce in rendered,
        "skillTitleObserved": PROBE_TITLE in rendered,
        "passed": bool(events and not parse_errors and skill_call and nonce in rendered and PROBE_TITLE in rendered),
    }


def opencode_probe(executable: str, cwd: Path, home: Path, model: str | None, timeout: int) -> dict[str, Any]:
    nonce = uuid.uuid4().hex
    permission = {"*": "deny", "read": "allow", "glob": "allow", "grep": "allow", "skill": "allow"}
    config = {
        "$schema": "https://opencode.ai/config.json",
        "plugin": [],
        "share": "disabled",
        "autoupdate": False,
        "lsp": False,
        "mcp": {},
        "instructions": [],
        "permission": permission,
        "agent": {
            "omarchy-host-conformance": {
                "description": "Read-only Agent Skills conformance probe",
                "mode": "primary",
                "permission": permission,
                "prompt": "Use only read, glob, grep, and skill. Never modify files, run shell commands, use the network, delegate, or ask questions.",
            }
        },
    }
    prompt = (
        f"Call the skill tool with name {PROBE_SKILL}. After loading it, return one JSON object containing "
        f'nonce "{nonce}" and title "{PROBE_TITLE}". Do not infer the title without loading the skill.'
    )
    command = [executable, "--pure", "run", "--format", "json", "--agent", "omarchy-host-conformance"]
    if model:
        command.extend(["--model", model])
    command.append(prompt)
    with tempfile.TemporaryDirectory(prefix="omarchy-conformance-") as temporary:
        config_home = Path(temporary) / "config"
        cache_home = Path(temporary) / "cache"
        for path in (config_home, cache_home):
            path.mkdir()
        environment = {
            "PATH": os.environ.get("PATH", ""),
            "HOME": str(home),
            "LANG": os.environ.get("LANG", "C.UTF-8"),
            "XDG_CONFIG_HOME": str(config_home),
            # Preserve OpenCode's normal home-backed authentication store.
            "XDG_DATA_HOME": os.environ.get("XDG_DATA_HOME", str(home / ".local/share")),
            "XDG_CACHE_HOME": str(cache_home),
            "OPENCODE_CONFIG_CONTENT": json.dumps(config, separators=(",", ":")),
            "OPENCODE_DISABLE_CLAUDE_CODE_PROMPT": "1",
            "OPENCODE_DISABLE_AUTOSHARE": "1",
            "OPENCODE_DISABLE_LSP_DOWNLOAD": "1",
            "OPENCODE_DISABLE_DEFAULT_PLUGINS": "1",
        }
        # Authentication is intentionally left to OpenCode's normal home-backed store.
        result = bounded_run(command, cwd, environment, timeout)
    parsed = parse_opencode(result.pop("_stdout"), nonce)
    parsed["passed"] = bool(
        parsed["passed"]
        and result.get("exitCode") == 0
        and not result.get("stdoutTruncated")
        and not result.get("stderrTruncated")
    )
    return {
        "kind": "builtin-opencode-readonly",
        "trust": "host-observed",
        "command": ["opencode", "--pure", "run", "--format", "json", "--agent", "omarchy-host-conformance"],
        "model": model,
        "policy": {"default": "deny", "allowed": ["read", "glob", "grep", "skill"], "plugins": False, "lsp": False, "sharing": False},
        **result,
        **parsed,
    }


def operator_evidence(label: str, command: str, cwd: Path, timeout: int) -> dict[str, Any]:
    result = bounded_run(shlex.split(command), cwd, timeout=timeout)
    result.pop("_stdout", None)
    return {
        "kind": label,
        "trust": "operator-controlled-self-report",
        "eligibleForVerification": False,
        **result,
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", choices=HOSTS, required=True)
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parent.parent / "skills")
    parser.add_argument("--cwd", type=Path, default=Path.cwd())
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument("--invoke", action="store_true", help="Run the built-in, constrained host probe when supported.")
    parser.add_argument("--opencode", help="OpenCode executable; defaults to PATH lookup.")
    parser.add_argument("--model", help="Explicit provider/model identifier for built-in host evidence.")
    parser.add_argument("--custom-command", action="append", default=[])
    parser.add_argument("--eval-hook", action="append", default=[])
    parser.add_argument("--timeout", type=int, default=TIMEOUT)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    source, cwd, home = map(lambda item: Path(os.path.abspath(item.expanduser())), (args.source, args.cwd, args.home))
    try:
        discovery = inspect(args.host, source, cwd, home, args.repo_root)
        attribution = git_attribution(source)
        source_digest = inventory(snapshot_tree(source))["digest"]
        evidence: list[dict[str, Any]] = []
        builtin: dict[str, Any] | None = None
        if args.invoke:
            if args.host != "opencode":
                raise ValueError("a built-in live probe is currently available only for OpenCode")
            executable = args.opencode or shutil.which("opencode")
            if not executable:
                raise ValueError("OpenCode was not found; install it or pass --opencode")
            builtin = opencode_probe(executable, cwd, home, args.model, args.timeout)
            evidence.append(builtin)
        evidence.extend(operator_evidence("custom-host-command", item, cwd, args.timeout) for item in args.custom_command)
        evidence.extend(operator_evidence("custom-eval-hook", item, cwd, args.timeout) for item in args.eval_hook)
        host_verified = bool(
            builtin
            and builtin["passed"]
            and discovery["discoveryReady"]
            and attribution["stable"]
        )
        provider_verified = bool(host_verified and args.model)
        payload = {
            "schemaVersion": 1,
            "host": args.host,
            "sourceDigest": source_digest,
            "sourceAttribution": attribution,
            "discovery": discovery,
            "evidence": evidence,
            "hostVerified": host_verified,
            "providerVerified": provider_verified,
            "provider": args.model if provider_verified else None,
            "claim": (
                "Built-in discovery and invocation evidence verified for the exact clean Git source."
                if host_verified else
                "No verified live-host claim. Custom commands and eval hooks are retained only as operator-controlled self-report."
            ),
        }
    except (OSError, ValueError, subprocess.SubprocessError) as error:
        payload = {"schemaVersion": 1, "host": args.host, "error": str(error), "hostVerified": False, "providerVerified": False}
    print(json.dumps(payload, indent=2, sort_keys=True) if args.json else payload.get("claim", f"error: {payload['error']}"))
    return 2 if "error" in payload else 0


if __name__ == "__main__":
    raise SystemExit(main())
