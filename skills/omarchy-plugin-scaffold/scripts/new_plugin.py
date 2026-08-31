#!/usr/bin/env python3
"""Generate a standalone Omarchy 4 Quattro shell-plugin repository."""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
import xml.sax.saxutils
from pathlib import Path


KINDS = {
    "bar-widget": ("barWidget", "BarWidget.qml"),
    "panel": ("panel", "Panel.qml"),
    "overlay": ("overlay", "Overlay.qml"),
    "menu": ("menu", "Menu.qml"),
    "service": ("service", "Service.qml"),
    "bar": ("bar", "Bar.qml"),
}
ID_PATTERN = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)


def system_root_alias(path: Path, metadata: os.stat_result) -> bool:
    """Allow immutable root-owned aliases such as macOS /var -> private/var."""
    return path.parent == Path(path.anchor) and getattr(metadata, "st_uid", -1) == 0


def same_directory(path_metadata: os.stat_result, current: os.stat_result) -> bool:
    if os.name == "nt":
        return stat.S_ISDIR(current.st_mode) and current.st_mtime_ns == path_metadata.st_mtime_ns
    return (current.st_dev, current.st_ino) == (path_metadata.st_dev, path_metadata.st_ino)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--id", required=True, dest="plugin_id")
    parser.add_argument("--name", required=True)
    parser.add_argument("--kind", action="append", required=True, choices=tuple(KINDS))
    parser.add_argument("--author", default="Plugin author")
    parser.add_argument("--description", default="A native Omarchy Quattro shell plugin.")
    parser.add_argument("--version", default="0.1.0")
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--default-section", choices=("left", "center", "right"), default="right")
    parser.add_argument("--allow-multiple", action="store_true")
    parser.add_argument("--no-git", action="store_true")
    return parser.parse_args(argv)


def validate_args(args: argparse.Namespace) -> None:
    if not ID_PATTERN.fullmatch(args.plugin_id) or ".." in args.plugin_id:
        raise ValueError("--id must be lowercase and contain only letters, digits, '.', '_', or '-'")
    if args.plugin_id.startswith("omarchy."):
        raise ValueError("--id may not use the reserved omarchy.* namespace")
    if "." not in args.plugin_id:
        raise ValueError("--id must be globally namespaced, for example io.github.owner.name")
    for flag, value in (("--name", args.name), ("--author", args.author), ("--description", args.description)):
        if not value.strip():
            raise ValueError(f"{flag} may not be empty")
        if any(character in value for character in ("\n", "\r", "\x00")):
            raise ValueError(f"{flag} must be one line without NUL characters")
    if not SEMVER.fullmatch(args.version):
        raise ValueError("--version must be semantic, for example 0.1.0")
    if len(args.kind) != len(set(args.kind)):
        raise ValueError("--kind values may not be repeated")
    if args.allow_multiple and "bar-widget" not in args.kind:
        raise ValueError("--allow-multiple requires --kind bar-widget")
    output = Path(os.path.abspath(args.output.expanduser()))
    current = Path(output.anchor)
    for part in output.parts[1:]:
        current /= part
        try:
            metadata = current.lstat()
        except FileNotFoundError:
            break
        if stat.S_ISLNK(metadata.st_mode) and not system_root_alias(current, metadata):
            raise ValueError(f"destination path may not traverse a symlink: {current}")
    if output.exists() and (output.is_symlink() or not output.is_dir() or any(output.iterdir())):
        raise ValueError(f"destination must not exist or must be empty: {output}")


def template_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "assets" / "templates"


def render(name: str, values: dict[str, str]) -> str:
    path = template_dir() / name
    text = path.read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    unresolved = re.findall(r"\{\{[A-Z0-9_]+\}\}", text)
    if unresolved:
        raise RuntimeError(f"unresolved template values in {name}: {', '.join(unresolved)}")
    return text


def inferred_repository(plugin_id: str, output_name: str) -> str:
    parts = plugin_id.split(".")
    if len(parts) >= 4 and parts[0:2] == ["io", "github"]:
        return f"https://github.com/{parts[2]}/{output_name}"
    return "https://github.com/OWNER/REPOSITORY"


def write_text(root: Path, relative: str, text: str, executable: bool = False) -> None:
    path = root / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    data = text.replace("\r\n", "\n").encode("utf-8")
    descriptor = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0), 0o755 if executable else 0o644)
    try:
        offset = 0
        while offset < len(data):
            written = os.write(descriptor, data[offset:])
            if written <= 0:
                raise OSError("short write")
            offset += written
        os.fsync(descriptor)
    finally:
        os.close(descriptor)


def build_manifest(args: argparse.Namespace) -> dict[str, object]:
    entry_points = {KINDS[kind][0]: KINDS[kind][1] for kind in args.kind}
    manifest: dict[str, object] = {
        "schemaVersion": 1,
        "id": args.plugin_id,
        "name": args.name.strip(),
        "version": args.version,
        "author": args.author.strip(),
        "license": "MIT",
        "description": args.description.strip(),
        "kinds": args.kind,
        "entryPoints": entry_points,
    }
    if "bar-widget" in args.kind:
        manifest["barWidget"] = {
            "displayName": args.name.strip(),
            "description": args.description.strip(),
            "category": "Other",
            "allowMultiple": args.allow_multiple,
            "defaultSection": args.default_section,
            "defaults": {},
            "schema": [],
        }
    return manifest


def populate(root: Path, args: argparse.Namespace) -> None:
    repository = inferred_repository(args.plugin_id, args.output.name)
    namespace = re.sub(r"[^a-z0-9-]", "-", args.plugin_id.replace(".", "-"))
    short = "".join(word[0].upper() for word in re.findall(r"[A-Za-z0-9]+", args.name))[:3] or "O"
    values = {
        "PLUGIN_ID": args.plugin_id,
        "PLUGIN_ID_QML": json.dumps(args.plugin_id, ensure_ascii=False)[1:-1],
        "PLUGIN_NAME": args.name.strip(),
        "PLUGIN_NAME_QML": json.dumps(args.name.strip(), ensure_ascii=False)[1:-1],
        "PLUGIN_NAME_XML": xml.sax.saxutils.escape(args.name.strip()),
        "DESCRIPTION": args.description.strip(),
        "DESCRIPTION_XML": xml.sax.saxutils.escape(args.description.strip()),
        "AUTHOR": args.author.strip(),
        "YEAR": "2026",
        "REPOSITORY_URL": repository,
        "NAMESPACE": namespace,
        "NAMESPACE_QML": json.dumps(namespace, ensure_ascii=False)[1:-1],
        "SHORT_LABEL": short,
        "SHORT_LABEL_QML": json.dumps(short, ensure_ascii=False)[1:-1],
        "KINDS": ", ".join(args.kind),
    }
    write_text(root, "manifest.json", json.dumps(build_manifest(args), indent=2, ensure_ascii=False) + "\n")
    for kind in args.kind:
        _, filename = KINDS[kind]
        write_text(root, filename, render(filename + ".tpl", values))
    for source, destination, executable in (
        ("README.md.tpl", "README.md", False),
        ("LICENSE.tpl", "LICENSE", False),
        ("preview.svg.tpl", "preview.svg", False),
        ("validate_manifest.py.tpl", "scripts/validate_manifest.py", True),
        ("tests-run.tpl", "tests/run", True),
        ("demo-run.tpl", "demo/run", True),
        ("fixture.json.tpl", "demo/fixtures/example.json", False),
        ("test.yml.tpl", ".github/workflows/test.yml", False),
        ("gitignore.tpl", ".gitignore", False),
    ):
        write_text(root, destination, render(source, values), executable)


def initialize_git(root: Path) -> None:
    subprocess.run(["git", "init", "--initial-branch=main", str(root)], check=True, stdout=subprocess.DEVNULL)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    try:
        validate_args(args)
    except ValueError as error:
        print(f"new_plugin.py: {error}", file=sys.stderr)
        return 2

    output = Path(os.path.abspath(args.output.expanduser()))
    output.parent.mkdir(parents=True, exist_ok=True)
    original = output.lstat() if output.exists() else None
    try:
        with tempfile.TemporaryDirectory(prefix=f".{output.name}.stage-", dir=output.parent) as temporary:
            stage = Path(temporary) / output.name
            stage.mkdir()
            populate(stage, args)
            if original is not None:
                current = output.lstat()
                if not same_directory(original, current) or output.is_symlink():
                    raise RuntimeError("destination changed during generation")
                output.rmdir()
            elif output.exists() or output.is_symlink():
                raise RuntimeError("destination appeared during generation")
            stage.rename(output)
        if not args.no_git:
            initialize_git(output)
    except (OSError, RuntimeError, subprocess.CalledProcessError) as error:
        print(f"new_plugin.py: generation failed: {error}", file=sys.stderr)
        return 1

    print(json.dumps({
        "plugin_dir": str(output),
        "id": args.plugin_id,
        "kinds": args.kind,
        "manifest": str(output / "manifest.json"),
        "next": [str(output / "tests" / "run"), f"omarchy plugin validate {output}"],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
