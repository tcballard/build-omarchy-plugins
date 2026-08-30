#!/usr/bin/env python3
"""Install portable Omarchy Agent Skills for a supported host or custom directory."""

from __future__ import annotations

import argparse
import filecmp
import json
import shutil
import stat
import sys
import tempfile
from pathlib import Path


TARGET_PATHS = {
    "agents": (Path(".agents/skills"), Path(".agents/skills")),
    "codex": (Path(".agents/skills"), Path(".agents/skills")),
    "cursor": (Path(".cursor/skills"), Path(".cursor/skills")),
    "gemini": (Path(".gemini/skills"), Path(".gemini/skills")),
    "claude": (Path(".claude/skills"), Path(".claude/skills")),
}
IGNORED_NAMES = {"__pycache__", ".DS_Store"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}


def ignored(path: Path) -> bool:
    return any(part in IGNORED_NAMES for part in path.parts) or path.suffix in IGNORED_SUFFIXES


def files(root: Path) -> dict[Path, Path]:
    result: dict[Path, Path] = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if ignored(relative):
            continue
        if path.is_symlink():
            raise ValueError(f"refusing skill containing symlink: {relative}")
        if path.is_file():
            result[relative] = path
    return result


def same_tree(source: Path, destination: Path) -> bool:
    if not destination.is_dir() or destination.is_symlink():
        return False
    source_files = files(source)
    destination_files = files(destination)
    if set(source_files) != set(destination_files):
        return False
    for relative, left in source_files.items():
        right = destination_files[relative]
        if not filecmp.cmp(left, right, shallow=False):
            return False
        if bool(left.stat().st_mode & stat.S_IXUSR) != bool(right.stat().st_mode & stat.S_IXUSR):
            return False
    return True


def copy_tree(source: Path, destination: Path) -> None:
    for relative, path in files(source).items():
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)


def replace_tree(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    temporary = Path(tempfile.mkdtemp(prefix=f".{destination.name}-", dir=destination.parent))
    backup = destination.parent / f".{destination.name}.backup"
    try:
        copy_tree(source, temporary)
        if backup.exists():
            raise RuntimeError(f"refusing to overwrite stale backup: {backup}")
        if destination.exists() or destination.is_symlink():
            destination.rename(backup)
        temporary.rename(destination)
        if backup.is_symlink() or backup.is_file():
            backup.unlink()
        elif backup.exists():
            shutil.rmtree(backup)
    except Exception:
        if destination.exists() and backup.exists():
            if destination.is_dir() and not destination.is_symlink():
                shutil.rmtree(destination)
            else:
                destination.unlink()
            backup.rename(destination)
        elif backup.exists() and not destination.exists():
            backup.rename(destination)
        if temporary.exists():
            shutil.rmtree(temporary)
        raise


def resolve_destination(args: argparse.Namespace) -> Path:
    if args.destination:
        return args.destination.expanduser().resolve(strict=False)
    if args.target == "generic":
        raise ValueError("--destination is required for --target generic")
    project_path, user_path = TARGET_PATHS[args.target]
    base = Path.cwd() if args.scope == "project" else Path.home()
    return (base / (project_path if args.scope == "project" else user_path)).resolve(strict=False)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=[*TARGET_PATHS, "generic"], default="agents")
    parser.add_argument("--scope", choices=("project", "user"), default="project")
    parser.add_argument("--destination", type=Path)
    parser.add_argument("--skill", action="append", default=[], help="Install only this skill; repeatable")
    parser.add_argument("--force", action="store_true", help="Replace conflicting copies of selected skills")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv or sys.argv[1:])

    repo = Path(__file__).resolve().parent.parent
    source_root = repo / "skills"
    available = {path.name: path for path in source_root.iterdir() if path.is_dir() and (path / "SKILL.md").is_file()}
    selected_names = args.skill or sorted(available)
    unknown = sorted(set(selected_names) - set(available))
    try:
        destination = resolve_destination(args)
        if unknown:
            raise ValueError(f"unknown skill: {', '.join(unknown)}")
        conflicts: list[str] = []
        unchanged: list[str] = []
        pending: list[str] = []
        for name in selected_names:
            target = destination / name
            if target.exists() or target.is_symlink():
                if same_tree(available[name], target):
                    unchanged.append(name)
                elif not args.force:
                    conflicts.append(name)
                else:
                    pending.append(name)
            else:
                pending.append(name)
        if conflicts:
            raise ValueError(
                "conflicting skill directories (use --force to replace only these named skills): "
                + ", ".join(conflicts)
            )
        installed: list[str] = []
        if not args.dry_run:
            destination.mkdir(parents=True, exist_ok=True)
            for name in pending:
                replace_tree(available[name], destination / name)
                installed.append(name)
        payload = {
            "ok": True,
            "target": args.target,
            "scope": args.scope,
            "destination": str(destination),
            "installed": installed,
            "would_install": pending if args.dry_run else [],
            "unchanged": unchanged,
        }
    except (OSError, ValueError, RuntimeError) as error:
        payload = {"ok": False, "error": str(error)}

    if args.as_json:
        print(json.dumps(payload, indent=2))
    elif not payload["ok"]:
        print(f"error: {payload['error']}", file=sys.stderr)
    else:
        verb = "Would install" if args.dry_run else "Installed"
        count = len(payload["would_install"] if args.dry_run else payload["installed"])
        print(f"{verb} {count} skills in {payload['destination']} ({len(payload['unchanged'])} unchanged).")
    return 0 if payload["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
