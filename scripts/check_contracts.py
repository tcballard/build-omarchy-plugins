#!/usr/bin/env python3
"""Validate pinned upstream contracts and optionally report upstream drift."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


COMMIT = re.compile(r"^[0-9a-f]{40}$")
DIGEST = re.compile(r"^[0-9a-f]{64}$")
ENTRY_KEYS = {"name", "repository", "trackedRef", "pinnedCommit", "path", "sha256", "assumptions"}
OPTIONAL_ENTRY_KEYS = {"vendoredPath"}


def unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"), object_pairs_hook=unique_object)
    if not isinstance(value, dict) or set(value) != {"schemaVersion", "reviewedAt", "contracts"}:
        raise ValueError("contract ledger has unexpected top-level fields")
    if value["schemaVersion"] != 1 or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value["reviewedAt"]):
        raise ValueError("contract ledger version or review date is invalid")
    if not isinstance(value["contracts"], list) or not value["contracts"]:
        raise ValueError("contract ledger must contain entries")
    names: set[str] = set()
    for entry in value["contracts"]:
        if (
            not isinstance(entry, dict)
            or not ENTRY_KEYS.issubset(entry)
            or not set(entry).issubset(ENTRY_KEYS | OPTIONAL_ENTRY_KEYS)
        ):
            raise ValueError("contract entry has unexpected fields")
        if not isinstance(entry["name"], str) or not entry["name"] or entry["name"] in names:
            raise ValueError("contract names must be unique non-empty strings")
        names.add(entry["name"])
        if not re.fullmatch(r"https://github\.com/[^/]+/[^/]+", entry["repository"]):
            raise ValueError(f"invalid GitHub repository for {entry['name']}")
        if not isinstance(entry["trackedRef"], str) or not entry["trackedRef"]:
            raise ValueError(f"invalid tracked ref for {entry['name']}")
        if not COMMIT.fullmatch(entry["pinnedCommit"]) or not DIGEST.fullmatch(entry["sha256"]):
            raise ValueError(f"invalid immutable pin for {entry['name']}")
        if not isinstance(entry["path"], str) or entry["path"].startswith("/") or ".." in Path(entry["path"]).parts:
            raise ValueError(f"invalid contract path for {entry['name']}")
        if "vendoredPath" in entry and (
            not isinstance(entry["vendoredPath"], str)
            or entry["vendoredPath"].startswith("/")
            or ".." in Path(entry["vendoredPath"]).parts
        ):
            raise ValueError(f"invalid vendored contract path for {entry['name']}")
        if not isinstance(entry["assumptions"], list) or not entry["assumptions"] or not all(isinstance(item, str) and item for item in entry["assumptions"]):
            raise ValueError(f"missing assumptions for {entry['name']}")
    return value


def pinned_url(entry: dict[str, Any]) -> str:
    repository = entry["repository"].removeprefix("https://github.com/")
    return f"https://raw.githubusercontent.com/{repository}/{entry['pinnedCommit']}/{entry['path']}"


def fetch(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "build-omarchy-plugins-contract-check/1"})
    with urllib.request.urlopen(request, timeout=30) as response:
        data = response.read(16 * 1024 * 1024 + 1)
    if len(data) > 16 * 1024 * 1024:
        raise ValueError(f"contract exceeds download limit: {url}")
    return data


def remote_head(entry: dict[str, Any]) -> str:
    result = subprocess.run(
        ["git", "ls-remote", entry["repository"] + ".git", entry["trackedRef"]],
        text=True, capture_output=True, check=False, timeout=60,
    )
    if result.returncode != 0 or not result.stdout.strip():
        raise ValueError(f"cannot resolve {entry['name']} {entry['trackedRef']}: {result.stderr.strip()}")
    value = result.stdout.split()[0]
    if not COMMIT.fullmatch(value):
        raise ValueError(f"upstream returned an invalid commit for {entry['name']}")
    return value


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, default=Path(__file__).resolve().parent.parent / "contracts/upstream-contracts.json")
    parser.add_argument("--online", action="store_true", help="Fetch each exact pinned document and verify its digest.")
    parser.add_argument("--check-heads", action="store_true", help="Fail when a tracked upstream ref has moved beyond the reviewed pin.")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        ledger = load(args.ledger)
        results = []
        for entry in ledger["contracts"]:
            item = {"name": entry["name"], "pinValid": True, "contentVerified": False, "vendoredVerified": False, "head": None, "drifted": False}
            if "vendoredPath" in entry:
                vendored = args.ledger.resolve().parent.parent / entry["vendoredPath"]
                actual = hashlib.sha256(vendored.read_bytes()).hexdigest()
                if actual != entry["sha256"]:
                    raise ValueError(f"vendored content digest mismatch for {entry['name']}")
                item["vendoredVerified"] = True
            if args.online:
                actual = hashlib.sha256(fetch(pinned_url(entry))).hexdigest()
                if actual != entry["sha256"]:
                    raise ValueError(f"pinned content digest mismatch for {entry['name']}")
                item["contentVerified"] = True
            if args.check_heads:
                item["head"] = remote_head(entry)
                item["drifted"] = item["head"] != entry["pinnedCommit"]
            results.append(item)
        drifted = [item["name"] for item in results if item["drifted"]]
        payload = {"ok": not drifted, "reviewedAt": ledger["reviewedAt"], "contracts": results, "drifted": drifted}
    except (OSError, ValueError, json.JSONDecodeError, urllib.error.URLError, subprocess.SubprocessError) as error:
        payload = {"ok": False, "error": str(error)}
    print(json.dumps(payload, indent=2, sort_keys=True) if args.json else ("Contracts verified." if payload["ok"] else f"Contract check failed: {payload.get('error') or ', '.join(payload['drifted'])}"))
    return 0 if payload["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
