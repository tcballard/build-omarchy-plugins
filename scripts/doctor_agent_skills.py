#!/usr/bin/env python3
"""Inspect supported host discovery locations without claiming a live host run."""

from __future__ import annotations

import argparse
import json
import os
import stat
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from install_agent_skills import inventory, snapshot_tree


HOSTS = ("codex", "opencode", "cursor", "claude", "gemini")
COMPATIBILITY_SOURCES = {
    "codex": "https://learn.chatgpt.com/docs/customization/overview",
    "opencode": "https://opencode.ai/docs/skills/",
    "cursor": "https://cursor.com/docs/skills",
    "claude": "https://code.claude.com/docs/en/skills",
    "gemini": "https://geminicli.com/docs/cli/skills/",
}


@dataclass(frozen=True)
class Root:
    path: str
    scope: str
    kind: str
    rank: int | None
    recursive: bool = False
    activation: str = "startup"


def absolute(path: Path) -> Path:
    return Path(os.path.abspath(path.expanduser()))


def repository_root(cwd: Path, explicit: Path | None) -> Path:
    if explicit is not None:
        return absolute(explicit)
    current = absolute(cwd)
    for candidate in (current, *current.parents):
        marker = candidate / ".git"
        if marker.is_dir() or marker.is_file():
            return candidate
    return current


def ancestors(cwd: Path, root: Path) -> list[Path]:
    cwd, root = absolute(cwd), absolute(root)
    try:
        cwd.relative_to(root)
    except ValueError:
        return [cwd]
    result: list[Path] = []
    current = cwd
    while True:
        result.append(current)
        if current == root:
            return result
        current = current.parent


def nested_roots(repo: Path, families: tuple[str, ...]) -> list[Path]:
    result: list[Path] = []
    for current, directories, _files in os.walk(repo, followlinks=False):
        directories[:] = sorted(name for name in directories if name not in {".git", "node_modules", "dist", "build"})
        base = Path(current)
        for family in families:
            candidate = base / family / "skills"
            if candidate.is_dir() and not candidate.is_symlink():
                result.append(candidate)
        # Do not traverse into skill payloads merely to rediscover nested roots.
        if base.parent.name in families and base.name == "skills":
            directories[:] = []
    return sorted(set(result), key=lambda item: str(item))


def roots_for(host: str, cwd: Path, home: Path, repo: Path) -> tuple[list[Root], list[str]]:
    roots: list[Root] = []
    blind_spots: list[str] = []
    chain = ancestors(cwd, repo)
    if host == "codex":
        roots = [
            Root(str(repo / ".agents/skills"), "project", "agents", 200),
            Root(str(home / ".agents/skills"), "user", "agents", 100),
        ]
        blind_spots.append("admin or product-managed skills are not represented by a portable filesystem contract")
    elif host == "opencode":
        rank = 300
        for directory in chain:
            for family in (".opencode", ".claude", ".agents"):
                roots.append(Root(str(directory / family / "skills"), "project", family[1:], rank))
                rank -= 1
        roots.extend([
            Root(str(home / ".config/opencode/skills"), "user", "opencode", 100),
            Root(str(home / ".claude/skills"), "user", "claude", 99),
            Root(str(home / ".agents/skills"), "user", "agents", 98),
        ])
        blind_spots.append("OpenCode documents discovery locations but not duplicate-name precedence; duplicates are ambiguous")
    elif host == "cursor":
        for path in nested_roots(repo, (".cursor", ".agents")):
            roots.append(Root(str(path), "project", path.parent.name[1:], None, True, "path-scoped"))
        roots.extend([
            Root(str(repo / ".claude/skills"), "project", "claude-compat", None),
            Root(str(repo / ".codex/skills"), "project", "codex-compat", None),
            Root(str(home / ".agents/skills"), "user", "agents", None),
            Root(str(home / ".cursor/skills"), "user", "cursor", None),
            Root(str(home / ".claude/skills"), "user", "claude-compat", None),
            Root(str(home / ".codex/skills"), "user", "codex-compat", None),
        ])
        blind_spots.append("Cursor does not document duplicate-name precedence across skill roots; duplicates are ambiguous")
    elif host == "claude":
        for index, directory in enumerate(chain):
            roots.append(Root(str(directory / ".claude/skills"), "project", "claude", 100 - index))
        roots.append(Root(str(home / ".claude/skills"), "personal", "claude", 200))
        for path in nested_roots(cwd, (".claude",)):
            if str(path) not in {item.path for item in roots}:
                roots.append(Root(str(path), "nested", "claude", None, True, "on-file-access"))
        blind_spots.extend([
            "enterprise managed skills override personal and project skills but their platform-specific root is not inferred",
            "plugin, --add-dir, and claude.ai synced sources require live host configuration to enumerate completely",
        ])
    else:  # gemini
        roots = [
            Root(str(repo / ".gemini/skills"), "workspace", "gemini", 300),
            Root(str(repo / ".agents/skills"), "workspace", "agents", 301),
            Root(str(home / ".gemini/skills"), "user", "gemini", 200),
            Root(str(home / ".agents/skills"), "user", "agents", 201),
        ]
        blind_spots.append("built-in and extension skills require live Gemini CLI configuration to enumerate")
    deduplicated = {item.path: item for item in roots}
    return list(deduplicated.values()), blind_spots


def skill_directories(root: Root) -> list[Path]:
    path = Path(root.path)
    if not path.exists() and not path.is_symlink():
        return []
    metadata = path.lstat()
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise ValueError(f"unsafe skill root: {path}")
    if root.recursive:
        return sorted({item.parent for item in path.rglob("SKILL.md") if item.is_file() and not item.is_symlink()})
    return sorted(item for item in path.iterdir() if item.is_dir() and not item.is_symlink() and (item / "SKILL.md").is_file())


def inspect(host: str, source: Path, cwd: Path, home: Path, repo: Path | None = None) -> dict[str, Any]:
    source = absolute(source)
    cwd, home = absolute(cwd), absolute(home)
    repo = repository_root(cwd, repo)
    expected = {path.name: inventory(snapshot_tree(path)) for path in sorted(source.iterdir()) if path.is_dir()}
    roots, blind_spots = roots_for(host, cwd, home, repo)
    found: list[dict[str, Any]] = []
    errors: list[str] = []
    for root in roots:
        try:
            candidates = skill_directories(root)
        except (OSError, ValueError) as error:
            errors.append(str(error))
            continue
        for candidate in candidates:
            name = candidate.name
            try:
                actual = inventory(snapshot_tree(candidate))
                exact = name in expected and actual == expected[name]
                digest = actual["digest"]
            except (OSError, ValueError) as error:
                errors.append(f"{candidate}: {error}")
                exact, digest = False, None
            found.append({**asdict(root), "skill": name, "skillPath": str(candidate), "digest": digest, "exactSourceCopy": exact})

    by_name: dict[str, list[dict[str, Any]]] = {}
    for item in found:
        by_name.setdefault(item["skill"], []).append(item)
    resolution: dict[str, dict[str, Any]] = {}
    for name, candidates in sorted(by_name.items()):
        ranked = [item for item in candidates if item["rank"] is not None and item["activation"] == "startup"]
        ambiguous = len(candidates) > 1 and (host in {"opencode", "cursor"} or not ranked)
        selected = None if ambiguous else max(ranked or candidates, key=lambda item: item["rank"] or 0)
        resolution[name] = {
            "ambiguous": ambiguous,
            "candidatePaths": [item["skillPath"] for item in candidates],
            "selectedPath": selected["skillPath"] if selected else None,
            "exactSourceCopy": bool(selected and selected["exactSourceCopy"]),
        }

    expected_names = sorted(expected)
    exact = [name for name in expected_names if resolution.get(name, {}).get("exactSourceCopy")]
    ambiguous = [name for name in expected_names if resolution.get(name, {}).get("ambiguous")]
    return {
        "schemaVersion": 1,
        "host": host,
        "cwd": str(cwd),
        "repositoryRoot": str(repo),
        "source": str(source),
        "documentation": COMPATIBILITY_SOURCES[host],
        "roots": [asdict(item) | {"exists": Path(item.path).is_dir()} for item in roots],
        "skills": found,
        "resolution": resolution,
        "summary": {
            "expected": len(expected_names),
            "exactEffectiveCopies": len(exact),
            "missingOrDifferent": sorted(set(expected_names) - set(exact)),
            "ambiguous": ambiguous,
        },
        "blindSpots": blind_spots,
        "errors": errors,
        "discoveryReady": len(exact) == len(expected_names) and not ambiguous and not errors,
        "hostVerified": False,
        "providerVerified": False,
        "claim": "Filesystem discovery evidence only; a live host invocation has not been verified.",
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--host", choices=HOSTS, required=True)
    parser.add_argument("--source", type=Path, default=Path(__file__).resolve().parent.parent / "skills")
    parser.add_argument("--cwd", type=Path, default=Path.cwd())
    parser.add_argument("--home", type=Path, default=Path.home())
    parser.add_argument("--repo-root", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)
    try:
        payload = inspect(args.host, args.source, args.cwd, args.home, args.repo_root)
    except (OSError, ValueError) as error:
        payload = {"schemaVersion": 1, "host": args.host, "error": str(error), "hostVerified": False, "providerVerified": False}
    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    elif "error" in payload:
        print(f"error: {payload['error']}", file=sys.stderr)
    else:
        summary = payload["summary"]
        print(f"{args.host}: {summary['exactEffectiveCopies']}/{summary['expected']} exact effective copies")
        print(payload["claim"])
    return 2 if "error" in payload or payload.get("errors") else 0


if __name__ == "__main__":
    raise SystemExit(main())
