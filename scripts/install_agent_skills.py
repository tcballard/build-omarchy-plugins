#!/usr/bin/env python3
"""Install, update, inspect, and remove portable Omarchy Agent Skills safely."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import sys
import time
import uuid
from contextlib import AbstractContextManager
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Mapping


TARGET_PATHS = {
    "agents": (Path(".agents/skills"), Path(".agents/skills")),
    "codex": (Path(".agents/skills"), Path(".agents/skills")),
    "cursor": (Path(".cursor/skills"), Path(".cursor/skills")),
    "gemini": (Path(".gemini/skills"), Path(".gemini/skills")),
    "claude": (Path(".claude/skills"), Path(".claude/skills")),
    "opencode": (Path(".opencode/skills"), Path(".config/opencode/skills")),
}
MANAGER = "build-omarchy-plugins"
REPOSITORY = "https://github.com/tcballard/build-omarchy-plugins"
RECEIPT_NAME = f".{MANAGER}-receipt.json"
RECEIPT_SCHEMA = 1
TRANSACTION_SCHEMA = 1
MAX_FILE_BYTES = 32 * 1024 * 1024
MAX_TREE_BYTES = 128 * 1024 * 1024
MAX_TREE_FILES = 4096
MAX_RECEIPT_BYTES = 2 * 1024 * 1024
IGNORED_NAMES = {"__pycache__", ".DS_Store"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}


@dataclass(frozen=True)
class FileSnapshot:
    data: bytes
    mode: int


def _ignored(path: PurePosixPath) -> bool:
    return any(part in IGNORED_NAMES for part in path.parts) or path.suffix in IGNORED_SUFFIXES


def _absolute(path: Path) -> Path:
    return Path(os.path.abspath(path.expanduser()))


def _reject_symlink_components(path: Path, label: str) -> None:
    absolute = _absolute(path)
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current /= part
        try:
            metadata = current.lstat()
        except FileNotFoundError:
            break
        if stat.S_ISLNK(metadata.st_mode):
            raise ValueError(f"refusing {label} reached through symlink: {current}")


def _require_directory(path: Path, label: str) -> None:
    metadata = path.lstat()
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise ValueError(f"{label} is not a private directory: {path}")


def snapshot_tree(root: Path) -> dict[PurePosixPath, FileSnapshot]:
    _reject_symlink_components(root, "tree")
    _require_directory(root, "tree root")
    result: dict[PurePosixPath, FileSnapshot] = {}
    total = 0

    def visit(directory: Path, relative: PurePosixPath) -> None:
        nonlocal total
        if len(relative.parts) > 64:
            raise ValueError(f"tree exceeds 64-directory depth: {root}")
        entries = sorted(os.scandir(directory), key=lambda item: item.name)
        for entry in entries:
            child = relative / entry.name
            if _ignored(child):
                continue
            metadata = entry.stat(follow_symlinks=False)
            if stat.S_ISLNK(metadata.st_mode):
                raise ValueError(f"refusing tree containing symlink: {child}")
            if stat.S_ISDIR(metadata.st_mode):
                visit(Path(entry.path), child)
                continue
            if not stat.S_ISREG(metadata.st_mode):
                raise ValueError(f"refusing non-regular tree entry: {child}")
            if metadata.st_size > MAX_FILE_BYTES:
                raise ValueError(f"file exceeds {MAX_FILE_BYTES} byte limit: {child}")
            total += metadata.st_size
            if total > MAX_TREE_BYTES or len(result) >= MAX_TREE_FILES:
                raise ValueError(f"tree exceeds installer safety limits: {root}")
            flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
            descriptor = os.open(entry.path, flags)
            try:
                opened = os.fstat(descriptor)
                if not stat.S_ISREG(opened.st_mode) or (opened.st_dev, opened.st_ino) != (metadata.st_dev, metadata.st_ino):
                    raise ValueError(f"file changed during snapshot: {child}")
                data = b""
                while len(data) < opened.st_size:
                    chunk = os.read(descriptor, min(1024 * 1024, opened.st_size - len(data)))
                    if not chunk:
                        raise ValueError(f"file changed during snapshot: {child}")
                    data += chunk
                if os.read(descriptor, 1) or os.fstat(descriptor).st_size != opened.st_size:
                    raise ValueError(f"file changed during snapshot: {child}")
            finally:
                os.close(descriptor)
            result[child] = FileSnapshot(data, 0o755 if opened.st_mode & 0o111 else 0o644)

    visit(root, PurePosixPath())
    return result


def inventory(snapshot: Mapping[PurePosixPath, FileSnapshot]) -> dict[str, Any]:
    files = [
        {
            "path": path.as_posix(),
            "mode": f"{value.mode:04o}",
            "bytes": len(value.data),
            "sha256": hashlib.sha256(value.data).hexdigest(),
        }
        for path, value in sorted(snapshot.items(), key=lambda item: item[0].as_posix())
    ]
    encoded = json.dumps(files, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return {"digest": hashlib.sha256(encoded).hexdigest(), "files": files}


def _inventory_valid(value: Any) -> bool:
    if not isinstance(value, dict) or set(value) != {"digest", "files"} or not isinstance(value["files"], list):
        return False
    encoded = json.dumps(value["files"], sort_keys=True, separators=(",", ":")).encode("utf-8")
    return value.get("digest") == hashlib.sha256(encoded).hexdigest()


def _write_all(descriptor: int, data: bytes) -> None:
    offset = 0
    while offset < len(data):
        written = os.write(descriptor, data[offset:])
        if written <= 0:
            raise OSError("short write")
        offset += written


def _fsync_directory(path: Path) -> None:
    if os.name == "nt":
        return
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def _atomic_write(path: Path, data: bytes, mode: int = 0o600) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.tmp-{uuid.uuid4().hex}")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0)
    descriptor = os.open(temporary, flags, mode)
    try:
        _write_all(descriptor, data)
        os.fsync(descriptor)
    finally:
        os.close(descriptor)
    try:
        os.replace(temporary, path)
        _fsync_directory(path.parent)
    finally:
        if temporary.exists():
            temporary.unlink()


def _write_json(path: Path, value: Any) -> None:
    _atomic_write(path, (json.dumps(value, indent=2, sort_keys=True) + "\n").encode("utf-8"))


def _read_regular(path: Path, maximum: int) -> bytes:
    metadata = path.lstat()
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode) or metadata.st_size > maximum:
        raise ValueError(f"refusing unsafe or oversized file: {path}")
    flags = os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
    descriptor = os.open(path, flags)
    try:
        opened = os.fstat(descriptor)
        if (opened.st_dev, opened.st_ino) != (metadata.st_dev, metadata.st_ino):
            raise ValueError(f"file changed before read: {path}")
        data = b""
        while len(data) < opened.st_size:
            chunk = os.read(descriptor, opened.st_size - len(data))
            if not chunk:
                raise ValueError(f"file changed during read: {path}")
            data += chunk
        return data
    finally:
        os.close(descriptor)


def load_receipt(destination: Path) -> dict[str, Any] | None:
    path = destination / RECEIPT_NAME
    if not path.exists() and not path.is_symlink():
        return None
    try:
        value = json.loads(_read_regular(path, MAX_RECEIPT_BYTES).decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"invalid installer receipt: {error}") from error
    if not isinstance(value, dict) or set(value) != {"schemaVersion", "manager", "source", "skills"}:
        raise ValueError("unsupported or malformed installer receipt")
    if value["schemaVersion"] != RECEIPT_SCHEMA or value["manager"] != MANAGER:
        raise ValueError("unsupported installer receipt")
    if not isinstance(value["skills"], dict) or not all(_inventory_valid(item) for item in value["skills"].values()):
        raise ValueError("invalid skill inventories in receipt")
    return value


def make_receipt(version: str, skills: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "schemaVersion": RECEIPT_SCHEMA,
        "manager": MANAGER,
        "source": {"repository": REPOSITORY, "version": version},
        "skills": dict(sorted(skills.items())),
    }


def _write_snapshot(snapshot: Mapping[PurePosixPath, FileSnapshot], root: Path) -> None:
    root.mkdir(parents=True, mode=0o700)
    for relative, value in sorted(snapshot.items(), key=lambda item: item[0].as_posix()):
        target = root / relative.as_posix()
        target.parent.mkdir(parents=True, exist_ok=True)
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_BINARY", 0)
        descriptor = os.open(target, flags, value.mode)
        try:
            _write_all(descriptor, value.data)
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
        os.chmod(target, value.mode)
    for directory in sorted((item for item in root.rglob("*") if item.is_dir()), reverse=True):
        _fsync_directory(directory)
    _fsync_directory(root)


def _remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink()
    elif path.exists():
        _require_directory(path, "transaction path")
        shutil.rmtree(path)


def _lock_windows(descriptor: int, unlock: bool = False) -> None:
    import msvcrt

    os.lseek(descriptor, 0, os.SEEK_SET)
    msvcrt.locking(descriptor, msvcrt.LK_UNLCK if unlock else msvcrt.LK_LOCK, 1)


class DestinationLock(AbstractContextManager["DestinationLock"]):
    def __init__(self, destination: Path) -> None:
        self.path = destination.parent / f".{destination.name}.{MANAGER}.lock"
        self.descriptor: int | None = None

    def _private(self) -> bool:
        assert self.descriptor is not None
        opened = os.fstat(self.descriptor)
        try:
            published = self.path.lstat()
        except FileNotFoundError:
            return False
        return (
            stat.S_ISREG(opened.st_mode)
            and opened.st_nlink == 1
            and stat.S_ISREG(published.st_mode)
            and not stat.S_ISLNK(published.st_mode)
            and published.st_nlink == 1
            and (opened.st_dev, opened.st_ino) == (published.st_dev, published.st_ino)
        )

    def __enter__(self) -> "DestinationLock":
        try:
            existing = self.path.lstat()
        except FileNotFoundError:
            existing = None
        if existing is not None and (not stat.S_ISREG(existing.st_mode) or stat.S_ISLNK(existing.st_mode) or existing.st_nlink != 1):
            raise ValueError(f"installer lock is not a private regular file: {self.path}")
        flags = os.O_RDWR | os.O_CREAT | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0)
        self.descriptor = os.open(self.path, flags, 0o600)
        if not self._private():
            os.close(self.descriptor)
            self.descriptor = None
            raise ValueError(f"installer lock is not a private regular file: {self.path}")
        if os.name == "nt":
            if os.fstat(self.descriptor).st_size == 0:
                _write_all(self.descriptor, b"\0")
                os.fsync(self.descriptor)
            _lock_windows(self.descriptor)
        else:
            import fcntl

            fcntl.flock(self.descriptor, fcntl.LOCK_EX)
        if not self._private():
            self.__exit__()
            raise ValueError(f"installer lock changed while acquiring it: {self.path}")
        payload = json.dumps({"pid": os.getpid(), "started": int(time.time())}, sort_keys=True).encode("utf-8")
        os.ftruncate(self.descriptor, 0)
        os.lseek(self.descriptor, 0, os.SEEK_SET)
        _write_all(self.descriptor, payload)
        os.fsync(self.descriptor)
        return self

    def __exit__(self, *exc: object) -> None:
        if self.descriptor is None:
            return
        try:
            if self._private():
                os.ftruncate(self.descriptor, 0)
                os.lseek(self.descriptor, 0, os.SEEK_SET)
                _write_all(self.descriptor, b"{}\n")
                os.fsync(self.descriptor)
        finally:
            if os.name == "nt":
                _lock_windows(self.descriptor, unlock=True)
            else:
                import fcntl

                fcntl.flock(self.descriptor, fcntl.LOCK_UN)
            os.close(self.descriptor)
            self.descriptor = None


def _transaction_prefix(destination: Path) -> str:
    return f".{destination.name}.{MANAGER}.txn-"


def _rollback(transaction: Path, destination: Path, journal: Mapping[str, Any]) -> None:
    backup = transaction / "backup"
    for name in reversed(sorted(journal["actions"])):
        target = destination / name
        original = backup / name
        _remove_path(target)
        if original.exists() or original.is_symlink():
            snapshot_tree(original)
            original.rename(target)
    receipt = destination / RECEIPT_NAME
    receipt_backup = transaction / "receipt-backup.json"
    if journal["receiptOriginal"]:
        _atomic_write(receipt, _read_regular(receipt_backup, MAX_RECEIPT_BYTES))
    elif receipt.exists() or receipt.is_symlink():
        _remove_path(receipt)
    _fsync_directory(destination)


def recover_transactions(destination: Path) -> list[str]:
    recovered: list[str] = []
    prefix = _transaction_prefix(destination)
    for transaction in sorted(destination.parent.glob(prefix + "*")):
        _require_directory(transaction, "transaction")
        journal_path = transaction / "journal.json"
        try:
            journal = json.loads(_read_regular(journal_path, MAX_RECEIPT_BYTES).decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise ValueError(f"cannot recover malformed transaction {transaction}: {error}") from error
        if (
            not isinstance(journal, dict)
            or journal.get("schemaVersion") != TRANSACTION_SCHEMA
            or journal.get("destination") != str(destination)
            or journal.get("phase") not in {"prepared", "committing", "complete"}
            or not isinstance(journal.get("actions"), dict)
        ):
            raise ValueError(f"cannot recover unsupported transaction: {transaction}")
        if journal["phase"] == "committing":
            destination.mkdir(parents=True, exist_ok=True)
            _rollback(transaction, destination, journal)
        shutil.rmtree(transaction)
        _fsync_directory(destination.parent)
        recovered.append(transaction.name)
    return recovered


def apply_transaction(
    destination: Path,
    actions: Mapping[str, str],
    sources: Mapping[str, Mapping[PurePosixPath, FileSnapshot]],
    receipt: dict[str, Any] | None,
) -> None:
    transaction = destination.parent / f"{_transaction_prefix(destination)}{uuid.uuid4().hex}"
    transaction.mkdir(mode=0o700)
    staged, backup = transaction / "staged", transaction / "backup"
    staged.mkdir()
    backup.mkdir()
    for name, action in sorted(actions.items()):
        if action == "install":
            _write_snapshot(sources[name], staged / name)
    receipt_path = destination / RECEIPT_NAME
    receipt_original = receipt_path.exists() or receipt_path.is_symlink()
    if receipt_original:
        _atomic_write(transaction / "receipt-backup.json", _read_regular(receipt_path, MAX_RECEIPT_BYTES))
    journal = {
        "schemaVersion": TRANSACTION_SCHEMA,
        "destination": str(destination),
        "phase": "prepared",
        "actions": dict(sorted(actions.items())),
        "receiptOriginal": receipt_original,
    }
    _write_json(transaction / "journal.json", journal)
    _fsync_directory(transaction)
    destination.mkdir(parents=True, exist_ok=True)
    try:
        journal["phase"] = "committing"
        _write_json(transaction / "journal.json", journal)
        for name, action in sorted(actions.items()):
            target = destination / name
            original = backup / name
            if target.exists() or target.is_symlink():
                _require_directory(target, "installed skill")
                target.rename(original)
            if action == "install":
                (staged / name).rename(target)
            _fsync_directory(destination)
        if receipt is None:
            if receipt_path.exists() or receipt_path.is_symlink():
                _remove_path(receipt_path)
        else:
            _write_json(receipt_path, receipt)
        _fsync_directory(destination)
        journal["phase"] = "complete"
        _write_json(transaction / "journal.json", journal)
        shutil.rmtree(transaction)
        _fsync_directory(destination.parent)
    except Exception:
        _rollback(transaction, destination, journal)
        raise


def resolve_destination(args: argparse.Namespace) -> Path:
    if args.destination:
        return _absolute(args.destination)
    if args.target == "generic":
        raise ValueError("--destination is required for --target generic")
    project, user = TARGET_PATHS[args.target]
    base = Path.cwd() if args.scope == "project" else Path.home()
    return _absolute(base / (project if args.scope == "project" else user))


def _current_inventory(destination: Path, name: str) -> dict[str, Any] | None:
    target = destination / name
    if not target.exists() and not target.is_symlink():
        return None
    return inventory(snapshot_tree(target))


def _diff(before: dict[str, Any] | None, after: dict[str, Any] | None) -> dict[str, list[str]]:
    old = {item["path"]: item for item in before["files"]} if before else {}
    new = {item["path"]: item for item in after["files"]} if after else {}
    return {
        "added": sorted(set(new) - set(old)),
        "removed": sorted(set(old) - set(new)),
        "changed": sorted(path for path in set(old) & set(new) if old[path] != new[path]),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", choices=[*TARGET_PATHS, "generic"], default="agents")
    parser.add_argument("--scope", choices=("project", "user"), default="project")
    parser.add_argument("--destination", type=Path)
    parser.add_argument("--skill", action="append", default=[])
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--diff", action="store_true", dest="show_diff")
    operation = parser.add_mutually_exclusive_group()
    operation.add_argument("--update", action="store_true")
    operation.add_argument("--uninstall", action="store_true")
    parser.add_argument("--json", action="store_true", dest="as_json")
    args = parser.parse_args(argv or sys.argv[1:])

    repo = Path(__file__).resolve().parent.parent
    try:
        version = (repo / "VERSION").read_text(encoding="utf-8").strip()
        source_root = repo / "skills"
        available = {
            path.name: snapshot_tree(path)
            for path in sorted(source_root.iterdir())
            if path.is_dir() and (path / "SKILL.md").is_file()
        }
        destination = resolve_destination(args)
        _reject_symlink_components(destination, "destination")
        if destination.exists() or destination.is_symlink():
            _require_directory(destination, "destination")
        existing_receipt = load_receipt(destination) if destination.exists() else None
        if args.update or args.uninstall:
            if existing_receipt is None:
                raise ValueError("no managed receipt exists for update or uninstall")
            selected = args.skill or sorted(existing_receipt["skills"])
        else:
            selected = args.skill or sorted(available)
        unknown = sorted(set(selected) - (set(existing_receipt["skills"]) if args.uninstall and existing_receipt else set(available)))
        if unknown:
            raise ValueError(f"unknown or unmanaged skill: {', '.join(unknown)}")

        actions: dict[str, str] = {}
        unchanged: list[str] = []
        differences: dict[str, Any] = {}
        observed: dict[str, dict[str, Any] | None] = {}
        desired_skills = dict(existing_receipt["skills"]) if existing_receipt else {}
        for name in selected:
            current = _current_inventory(destination, name)
            observed[name] = current
            managed = existing_receipt["skills"].get(name) if existing_receipt else None
            if (args.update or args.uninstall) and current != managed and not (args.force or args.show_diff):
                raise ValueError(f"locally modified or missing managed skill (use --force after --diff): {name}")
            desired = None if args.uninstall else inventory(available[name])
            differences[name] = _diff(current, desired)
            if args.uninstall:
                actions[name] = "uninstall"
                desired_skills.pop(name, None)
            elif current == desired:
                unchanged.append(name)
                desired_skills[name] = desired
            elif current is not None and not (args.force or args.update):
                raise ValueError(f"conflicting skill directory (use --force to replace only this skill): {name}")
            else:
                actions[name] = "install"
                desired_skills[name] = desired
        desired_receipt = make_receipt(version, desired_skills) if desired_skills else None

        recovered: list[str] = []
        if actions and not args.dry_run and not args.show_diff:
            destination.parent.mkdir(parents=True, exist_ok=True)
            _reject_symlink_components(destination.parent, "destination parent")
            with DestinationLock(destination):
                recovered = recover_transactions(destination)
                if recovered:
                    raise RuntimeError("recovered an interrupted transaction; rerun to apply against the recovered state")
                locked_receipt = load_receipt(destination) if destination.exists() else None
                if locked_receipt != existing_receipt or any(
                    _current_inventory(destination, name) != before for name, before in observed.items()
                ):
                    raise RuntimeError("destination changed concurrently; rerun the operation")
                apply_transaction(destination, actions, available, desired_receipt)
        payload = {
            "ok": True,
            "operation": "uninstall" if args.uninstall else "update" if args.update else "install",
            "target": args.target,
            "scope": args.scope,
            "destination": str(destination),
            "changed": sorted(actions),
            "unchanged": sorted(unchanged),
            "wouldChange": sorted(actions) if args.dry_run or args.show_diff else [],
            "diff": differences if args.show_diff else None,
            "receipt": str(destination / RECEIPT_NAME) if desired_receipt else None,
            "recovered": recovered,
        }
        # Backward-compatible install result fields.
        payload["installed"] = sorted(actions) if not args.uninstall and not args.dry_run and not args.show_diff else []
        payload["would_install"] = sorted(actions) if not args.uninstall and (args.dry_run or args.show_diff) else []
    except (OSError, ValueError, RuntimeError) as error:
        payload = {"ok": False, "error": str(error)}

    if args.as_json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    elif not payload["ok"]:
        print(f"error: {payload['error']}", file=sys.stderr)
    else:
        print(f"{payload['operation'].title()}: {len(payload['changed'])} changed, {len(payload['unchanged'])} unchanged in {payload['destination']}")
    return 0 if payload["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
