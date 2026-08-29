#!/usr/bin/env python3
import json
import re
import sys
from pathlib import Path, PurePosixPath

ROOT = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
MANIFEST = ROOT / "manifest.json"
KINDS = {"bar": "bar", "bar-widget": "barWidget", "menu": "menu", "overlay": "overlay", "panel": "panel", "service": "service"}

def fail(message):
    print(f"validate_manifest.py: {message}", file=sys.stderr)
    raise SystemExit(1)

try:
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
except Exception as error:
    fail(f"invalid manifest.json: {error}")

if not isinstance(manifest, dict): fail("manifest must be an object")
if type(manifest.get("schemaVersion")) is not int or manifest["schemaVersion"] != 1: fail("schemaVersion must be the number 1")
for field in ("id", "name", "version", "kinds", "entryPoints"):
    if field not in manifest: fail(f"missing field {field}")
plugin_id = manifest["id"]
if not isinstance(plugin_id, str) or not re.fullmatch(r"[a-z0-9][a-z0-9._-]*", plugin_id) or ".." in plugin_id: fail("invalid plugin id")
if plugin_id.startswith("omarchy."): fail("reserved omarchy.* id")
if not isinstance(manifest["kinds"], list) or not manifest["kinds"]: fail("kinds must be non-empty")
if not isinstance(manifest["entryPoints"], dict): fail("entryPoints must be an object")
for kind in manifest["kinds"]:
    if kind not in KINDS: fail(f"unsupported kind {kind}")
    key = KINDS[kind]
    if key not in manifest["entryPoints"]: fail(f"{kind} requires entryPoints.{key}")
for key, value in manifest["entryPoints"].items():
    if not isinstance(value, str) or not value or "\n" in value: fail(f"unsafe entry point {key}")
    path = PurePosixPath(value)
    if path.is_absolute() or ".." in path.parts or value != path.as_posix(): fail(f"unsafe entry point {value}")
    if not (ROOT / value).is_file(): fail(f"missing entry point {value}")
for path in ROOT.rglob("*"):
    if ".git" in path.parts: continue
    if path.is_symlink(): fail(f"symlink not allowed: {path.relative_to(ROOT)}")
print(f"VALID: {ROOT}")
