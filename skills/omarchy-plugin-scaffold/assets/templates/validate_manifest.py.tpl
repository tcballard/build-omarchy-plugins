#!/usr/bin/env python3
import json
import os
import re
import stat
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(os.path.abspath(Path(sys.argv[1] if len(sys.argv) > 1 else ".").expanduser()))
MANIFEST = ROOT / "manifest.json"
KINDS = {"bar": "bar", "bar-widget": "barWidget", "menu": "menu", "overlay": "overlay", "panel": "panel", "service": "service"}
MAX_MANIFEST = 1024 * 1024
MAX_FILE = 64 * 1024 * 1024
MAX_TREE = 512 * 1024 * 1024
MAX_FILES = 20000

def fail(message):
    print(f"validate_manifest.py: {message}", file=sys.stderr)
    raise SystemExit(1)

def duplicates(pairs):
    result = {}
    for key, value in pairs:
        if key in result: fail(f"duplicate JSON key: {key}")
        result[key] = value
    return result

def regular_bytes(path, limit):
    try:
        before = path.lstat()
    except OSError as error:
        fail(f"cannot inspect regular file {path}: {error}")
    if not stat.S_ISREG(before.st_mode) or stat.S_ISLNK(before.st_mode) or before.st_size > limit:
        fail(f"unsafe or oversized regular file: {path.relative_to(ROOT)}")
    descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
    try:
        opened = os.fstat(descriptor)
        if (opened.st_dev, opened.st_ino) != (before.st_dev, before.st_ino): fail("file changed during validation")
        chunks, remaining = [], opened.st_size
        while remaining:
            chunk = os.read(descriptor, min(remaining, 1024 * 1024))
            if not chunk: fail("file changed during validation")
            chunks.append(chunk)
            remaining -= len(chunk)
        return b"".join(chunks)
    finally:
        os.close(descriptor)

current = Path(ROOT.anchor)
for part in ROOT.parts[1:]:
    current /= part
    if current.is_symlink(): fail(f"plugin path traverses symlink: {current}")
if not ROOT.is_dir(): fail("plugin root is not a directory")

count = total = 0
for directory, dirnames, filenames in os.walk(ROOT, topdown=True, followlinks=False):
    base = Path(directory)
    safe_dirs = []
    for name in sorted(dirnames):
        path = base / name
        metadata = path.lstat()
        if stat.S_ISLNK(metadata.st_mode): fail(f"symlink not allowed: {path.relative_to(ROOT)}")
        if not stat.S_ISDIR(metadata.st_mode): fail(f"special entry not allowed: {path.relative_to(ROOT)}")
        if name != ".git": safe_dirs.append(name)
    dirnames[:] = safe_dirs
    for name in sorted(filenames):
        path = base / name
        metadata = path.lstat()
        if stat.S_ISLNK(metadata.st_mode): fail(f"symlink not allowed: {path.relative_to(ROOT)}")
        if not stat.S_ISREG(metadata.st_mode): fail(f"special entry not allowed: {path.relative_to(ROOT)}")
        if metadata.st_size > MAX_FILE: fail(f"file too large: {path.relative_to(ROOT)}")
        count += 1
        total += metadata.st_size
        if count > MAX_FILES or total > MAX_TREE: fail("plugin tree exceeds safety limits")

try:
    manifest = json.loads(regular_bytes(MANIFEST, MAX_MANIFEST).decode("utf-8"), object_pairs_hook=duplicates)
except (OSError, UnicodeDecodeError, json.JSONDecodeError, RecursionError, ValueError) as error:
    fail(f"invalid manifest.json: {error}")

if not isinstance(manifest, dict): fail("manifest must be an object")
if type(manifest.get("schemaVersion")) is not int or manifest["schemaVersion"] != 1: fail("schemaVersion must be the number 1")
for field in ("id", "name", "version", "kinds", "entryPoints"):
    if field not in manifest: fail(f"missing field {field}")
plugin_id = manifest["id"]
if not isinstance(plugin_id, str) or not re.fullmatch(r"[a-z0-9][a-z0-9._-]*", plugin_id) or ".." in plugin_id: fail("invalid plugin id")
if plugin_id.startswith("omarchy."): fail("reserved omarchy.* id")
if not isinstance(manifest["kinds"], list) or not manifest["kinds"]: fail("kinds must be non-empty")
if len(manifest["kinds"]) != len(set(manifest["kinds"])): fail("duplicate kinds")
if not isinstance(manifest["entryPoints"], dict): fail("entryPoints must be an object")
for kind in manifest["kinds"]:
    if kind not in KINDS: fail(f"unsupported kind {kind}")
    key = KINDS[kind]
    if key not in manifest["entryPoints"]: fail(f"{kind} requires entryPoints.{key}")
for key, value in manifest["entryPoints"].items():
    if not isinstance(value, str) or not value or "\n" in value or "\r" in value or "\x00" in value or "\\" in value: fail(f"unsafe entry point {key}")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or value != path.as_posix(): fail(f"unsafe entry point {value}")
    regular_bytes(ROOT / value, MAX_FILE)
print(f"VALID: {ROOT}")
