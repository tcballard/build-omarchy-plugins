#!/usr/bin/env python3
"""Portable Omarchy Quattro plugin validator and advisory security linter.

The structural checks mirror the public Omarchy v4 schema and CLI behavior
verified on 2026-08-29. The security checks deliberately cover only documented,
deterministic patterns and are not a security audit or marketplace result.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import stat
import sys
from dataclasses import asdict, dataclass
from pathlib import Path, PurePosixPath
from typing import Any, Iterable


SUPPORTED_KINDS = {
    "bar": "bar",
    "bar-widget": "barWidget",
    "menu": "menu",
    "overlay": "overlay",
    "panel": "panel",
    "service": "service",
}
HOST_INJECTED_PROPERTIES = {
    "omarchyPath",
    "shell",
    "manifest",
    "pluginRegistry",
    "barWidgetRegistry",
    "barConfig",
}
SEMVER = re.compile(
    r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
PLUGIN_ID = re.compile(r"^[a-z0-9][a-z0-9._-]*$")
TEXT_SUFFIXES = {
    ".bash", ".c", ".cc", ".cfg", ".conf", ".cpp", ".css", ".go",
    ".h", ".hpp", ".ini", ".java", ".js", ".json", ".jsonc", ".md",
    ".py", ".qml", ".rs", ".service", ".sh", ".toml", ".txt", ".xml",
    ".yaml", ".yml",
}
PREVIEW_NAMES = {"preview.png", "preview.jpg", "preview.jpeg", "preview.webp", "preview.avif"}
MAX_MANIFEST_BYTES = 1024 * 1024
MAX_TEXT_BYTES = 2 * 1024 * 1024
MAX_FILE_BYTES = 64 * 1024 * 1024
MAX_TREE_BYTES = 512 * 1024 * 1024
MAX_TREE_FILES = 20_000
MAX_TREE_DEPTH = 64


@dataclass(frozen=True)
class Diagnostic:
    level: str
    code: str
    message: str
    path: str = ""


class Report:
    def __init__(self, root: Path) -> None:
        self.root = root
        self.diagnostics: list[Diagnostic] = []
        self.findings: list[Diagnostic] = []
        self.capabilities: list[Diagnostic] = []
        self._seen: set[tuple[str, str, str]] = set()

    def add(self, level: str, code: str, message: str, path: Path | str = "") -> None:
        relative = relative_path(self.root, path)
        key = (level, code, relative)
        if key in self._seen:
            return
        self._seen.add(key)
        self.diagnostics.append(Diagnostic(level, code, message, relative))

    def finding(self, code: str, message: str, path: Path | str = "") -> None:
        relative = relative_path(self.root, path)
        key = ("finding", code, relative)
        if key in self._seen:
            return
        self._seen.add(key)
        self.findings.append(Diagnostic("finding", code, message, relative))

    def capability(self, code: str, message: str, path: Path | str = "") -> None:
        relative = relative_path(self.root, path)
        key = ("capability", code, relative)
        if key in self._seen:
            return
        self._seen.add(key)
        self.capabilities.append(Diagnostic("capability", code, message, relative))

    @property
    def errors(self) -> list[Diagnostic]:
        return [item for item in self.diagnostics if item.level == "error"]

    @property
    def warnings(self) -> list[Diagnostic]:
        return [item for item in self.diagnostics if item.level == "warning"]

    @property
    def security_outcome(self) -> str:
        if self.findings:
            return "needs-fixes"
        if self.capabilities:
            return "review-required"
        return "passed"

    def result(self, security: bool) -> dict[str, Any]:
        return {
            "root": str(self.root),
            "valid": not self.errors,
            "errors": [asdict(item) for item in self.errors],
            "warnings": [asdict(item) for item in self.warnings],
            "security": {
                "scanned": security,
                "outcome": self.security_outcome if security else "not-run",
                "findings": [asdict(item) for item in self.findings],
                "capabilities": [asdict(item) for item in self.capabilities],
                "disclaimer": (
                    "Advisory deterministic checks only; not a security audit, "
                    "certification, warranty, endorsement, or marketplace result."
                ),
            },
        }


def relative_path(root: Path, value: Path | str) -> str:
    if not value:
        return ""
    path = Path(value)
    try:
        return Path(os.path.abspath(path)).relative_to(Path(os.path.abspath(root))).as_posix()
    except ValueError:
        return str(path)


def is_plain_object(value: Any) -> bool:
    return isinstance(value, dict)


def system_root_alias(path: Path, metadata: os.stat_result) -> bool:
    """Allow immutable root-owned aliases such as macOS /var -> private/var."""
    return path.parent == Path(path.anchor) and getattr(metadata, "st_uid", -1) == 0


def same_open_file(path_metadata: os.stat_result, opened: os.stat_result) -> bool:
    if not stat.S_ISREG(opened.st_mode):
        return False
    if os.name == "nt":
        return opened.st_size == path_metadata.st_size and opened.st_mtime_ns == path_metadata.st_mtime_ns
    return (opened.st_dev, opened.st_ino) == (path_metadata.st_dev, path_metadata.st_ino)


def path_has_symlink(path: Path) -> Path | None:
    absolute = Path(os.path.abspath(path))
    current = Path(absolute.anchor)
    for part in absolute.parts[1:]:
        current /= part
        try:
            metadata = current.lstat()
        except FileNotFoundError:
            return None
        if stat.S_ISLNK(metadata.st_mode) and not system_root_alias(current, metadata):
            return current
    return None


def safe_entry_point(value: Any) -> bool:
    if not isinstance(value, str) or not value or any(character in value for character in ("\n", "\r", "\x00", "\\")):
        return False
    posix = PurePosixPath(value)
    if posix.is_absolute() or ".." in posix.parts:
        return False
    return value == posix.as_posix()


def iter_files(root: Path) -> Iterable[Path]:
    for directory, dirnames, filenames in os.walk(root, followlinks=False):
        dirnames[:] = [name for name in dirnames if name != ".git"]
        base = Path(directory)
        for name in filenames:
            yield base / name


def read_regular(path: Path, limit: int) -> bytes | None:
    try:
        before = path.lstat()
        if not stat.S_ISREG(before.st_mode) or stat.S_ISLNK(before.st_mode) or before.st_size > limit:
            return None
        descriptor = os.open(path, os.O_RDONLY | getattr(os, "O_BINARY", 0) | getattr(os, "O_NOFOLLOW", 0))
        try:
            opened = os.fstat(descriptor)
            if not same_open_file(before, opened):
                return None
            chunks: list[bytes] = []
            remaining = opened.st_size
            while remaining:
                chunk = os.read(descriptor, min(remaining, 1024 * 1024))
                if not chunk:
                    return None
                chunks.append(chunk)
                remaining -= len(chunk)
            if os.read(descriptor, 1) or os.fstat(descriptor).st_size != opened.st_size:
                return None
            return b"".join(chunks)
        finally:
            os.close(descriptor)
    except OSError:
        return None


def read_text(path: Path, limit: int = MAX_TEXT_BYTES) -> str | None:
    data = read_regular(path, limit)
    if data is None:
        return None
    if b"\x00" in data:
        return None
    try:
        return data.decode("utf-8")
    except UnicodeDecodeError:
        return None


def reject_duplicate_keys(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON key: {key}")
        result[key] = value
    return result


def load_manifest(root: Path, report: Report) -> dict[str, Any] | None:
    manifest_path = root / "manifest.json"
    if not manifest_path.is_file():
        report.add("error", "manifest-missing", "Root manifest.json is required.", manifest_path)
        return None
    if manifest_path.is_symlink():
        report.add("error", "manifest-symlink", "manifest.json may not be a symlink.", manifest_path)
        return None
    try:
        data = read_regular(manifest_path, MAX_MANIFEST_BYTES)
        if data is None:
            raise ValueError(f"manifest must be a regular file no larger than {MAX_MANIFEST_BYTES} bytes")
        value = json.loads(data.decode("utf-8"), object_pairs_hook=reject_duplicate_keys)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, RecursionError, ValueError) as error:
        report.add("error", "manifest-json", f"manifest.json is not valid UTF-8 JSON: {error}", manifest_path)
        return None
    if not is_plain_object(value):
        report.add("error", "manifest-object", "manifest.json must contain one JSON object.", manifest_path)
        return None
    return value


def validate_manifest(root: Path, manifest: dict[str, Any], report: Report, strict: bool) -> None:
    manifest_path = root / "manifest.json"
    if type(manifest.get("schemaVersion")) is not int or manifest.get("schemaVersion") != 1:
        report.add("error", "schema-version", "schemaVersion must be the JSON number 1.", manifest_path)

    for key in ("id", "name", "version", "kinds", "entryPoints"):
        if key not in manifest:
            report.add("error", "required-field", f"Missing required manifest field '{key}'.", manifest_path)

    for key in ("id", "name", "version"):
        value = manifest.get(key)
        if not isinstance(value, str) or not value.strip():
            report.add("error", f"{key}-value", f"Manifest field '{key}' must be a non-empty string.", manifest_path)

    plugin_id = manifest.get("id", "")
    if isinstance(plugin_id, str):
        if not PLUGIN_ID.fullmatch(plugin_id) or ".." in plugin_id:
            report.add(
                "error", "plugin-id",
                "Plugin id must be lowercase and contain only letters, digits, '.', '_', or '-'.",
                manifest_path,
            )
        if plugin_id.startswith("omarchy."):
            report.add("error", "reserved-id", "Third-party plugins may not use the reserved omarchy.* namespace.", manifest_path)
        if "." not in plugin_id:
            report.add("warning", "unnamespaced-id", "Use a globally namespaced plugin id such as io.github.owner.name.", manifest_path)

    version = manifest.get("version", "")
    if isinstance(version, str) and version and not SEMVER.fullmatch(version):
        report.add("error" if strict else "warning", "version-semver", "Use a semantic version such as 1.0.0.", manifest_path)

    for optional in ("author", "description", "license"):
        if not isinstance(manifest.get(optional), str) or not str(manifest.get(optional, "")).strip():
            report.add("warning", f"{optional}-missing", f"Publishable plugins should declare '{optional}'.", manifest_path)

    kinds = manifest.get("kinds")
    if not isinstance(kinds, list) or not kinds:
        report.add("error", "kinds", "'kinds' must be a non-empty array.", manifest_path)
        kinds = []
    elif any(not isinstance(item, str) or not item for item in kinds):
        report.add("error", "kind-type", "Every kind must be a non-empty string.", manifest_path)
        kinds = [item for item in kinds if isinstance(item, str) and item]

    if len(kinds) != len(set(kinds)):
        report.add("error", "duplicate-kind", "Manifest kinds must not contain duplicates.", manifest_path)
    for kind in kinds:
        if kind not in SUPPORTED_KINDS:
            report.add("error", "unsupported-kind", f"Unsupported plugin kind '{kind}'.", manifest_path)

    entry_points = manifest.get("entryPoints")
    if not is_plain_object(entry_points):
        report.add("error", "entry-points-object", "'entryPoints' must be an object.", manifest_path)
        entry_points = {}

    for kind in kinds:
        expected = SUPPORTED_KINDS.get(kind)
        if expected and expected not in entry_points:
            report.add("error", "entry-point-required", f"Kind '{kind}' requires entryPoints.{expected}.", manifest_path)

    for key, value in entry_points.items():
        if not safe_entry_point(value):
            report.add("error", "entry-point-path", f"Entry point '{key}' must be a safe relative path without '..'.", manifest_path)
            continue
        target = root / value
        if not target.is_file():
            report.add("error", "entry-point-missing", f"Entry point '{value}' does not exist as a regular file.", target)
            continue
        if target.is_symlink():
            report.add("error", "entry-point-symlink", f"Entry point '{value}' may not be a symlink.", target)
        check_qml_entry_point(target, kinds, key, report)

    widget = manifest.get("barWidget")
    if "bar-widget" in kinds:
        if not is_plain_object(widget):
            report.add("warning", "bar-widget-metadata", "A bar widget should declare a barWidget metadata object.", manifest_path)
        else:
            validate_bar_widget(widget, report, manifest_path, strict)
    elif widget is not None:
        report.add("warning", "unused-bar-widget-metadata", "barWidget metadata is present without the bar-widget kind.", manifest_path)

    keep_loaded = manifest.get("keepLoaded")
    if keep_loaded is not None and type(keep_loaded) is not bool:
        report.add("error", "keep-loaded-type", "keepLoaded must be a JSON boolean.", manifest_path)


def validate_bar_widget(widget: dict[str, Any], report: Report, path: Path, strict: bool) -> None:
    section = widget.get("defaultSection")
    if section is not None and section not in {"left", "center", "right"}:
        report.add("error", "default-section", "barWidget.defaultSection must be left, center, or right.", path)
    allow_multiple = widget.get("allowMultiple")
    if allow_multiple is not None and type(allow_multiple) is not bool:
        report.add("error", "allow-multiple-type", "barWidget.allowMultiple must be a JSON boolean.", path)
    defaults = widget.get("defaults")
    if defaults is not None and not is_plain_object(defaults):
        report.add("error", "defaults-object", "barWidget.defaults must be an object.", path)
    schema = widget.get("schema")
    if schema is not None:
        if not isinstance(schema, list):
            report.add("error", "settings-schema", "barWidget.schema must be an array.", path)
        else:
            keys: set[str] = set()
            for index, field in enumerate(schema):
                if not is_plain_object(field):
                    report.add("error", "settings-field", f"barWidget.schema[{index}] must be an object.", path)
                    continue
                key = field.get("key")
                field_type = field.get("type")
                label = field.get("label")
                if not isinstance(key, str) or not key:
                    report.add("error", "settings-key", f"barWidget.schema[{index}].key must be non-empty.", path)
                elif key in keys:
                    report.add("error", "settings-key-duplicate", f"Duplicate settings key '{key}'.", path)
                else:
                    keys.add(key)
                if field_type not in {"boolean", "enum", "integer", "path", "string"}:
                    report.add("error" if strict else "warning", "settings-type", f"Unrecognized current settings type '{field_type}'.", path)
                if not isinstance(label, str) or not label:
                    report.add("warning", "settings-label", f"barWidget.schema[{index}] should have a readable label.", path)
                if field_type == "enum" and not isinstance(field.get("options"), list):
                    report.add("error", "settings-options", f"Enum setting '{key}' requires an options array.", path)
                if is_plain_object(defaults) and isinstance(key, str) and key not in defaults and "defaultValue" not in field:
                    report.add("warning", "settings-default", f"Setting '{key}' has no declared default.", path)


def check_qml_entry_point(path: Path, kinds: list[str], key: str, report: Report) -> None:
    if path.suffix.lower() != ".qml":
        report.add("warning", "entry-point-extension", "Omarchy entry points are normally QML files.", path)
        return
    text = read_text(path)
    if text is None:
        report.add("warning", "qml-unreadable", "Could not read QML entry point for static quality checks.", path)
        return
    if re.search(r"\bShellRoot\s*\{", text):
        report.add("error", "standalone-shell-root", "Plugin entry points must be hosted Items, not ShellRoot.", path)
    if key in {"panel", "overlay", "menu"}:
        for method in ("open", "close"):
            if not re.search(rf"\bfunction\s+{method}\s*\(", text):
                report.add("error", f"lifecycle-{method}", f"{key} entry point must expose function {method}().", path)
    for match in re.finditer(r"\brequired\s+property\s+\w+\s+(\w+)", text):
        if match.group(1) in HOST_INJECTED_PROPERTIES:
            report.add(
                "warning", "required-injected-property",
                f"Host-injected property '{match.group(1)}' is required before late Loader injection; use a safe default in third-party QML.",
                path,
            )
    if re.search(r"command\s*:\s*\[\s*[\"'](?:ba)?sh[\"']\s*,\s*[\"']-c[\"']", text):
        report.add("warning", "qml-shell-command", "Prefer a Process argument array over bash/sh -c.", path)


def validate_tree(root: Path, report: Report) -> bool:
    trusted = True
    files = 0
    total = 0

    def visit(directory: Path, depth: int) -> None:
        nonlocal trusted, files, total
        if depth > MAX_TREE_DEPTH:
            report.add("error", "tree-depth", f"Plugin tree exceeds {MAX_TREE_DEPTH} levels.", directory)
            trusted = False
            return
        try:
            entries = sorted(os.scandir(directory), key=lambda item: item.name)
        except OSError as error:
            report.add("error", "tree-read", f"Cannot inspect plugin directory: {error}", directory)
            trusted = False
            return
        for entry in entries:
            path = Path(entry.path)
            try:
                metadata = entry.stat(follow_symlinks=False)
            except OSError as error:
                report.add("error", "tree-stat", f"Cannot inspect plugin entry: {error}", path)
                trusted = False
                continue
            if stat.S_ISLNK(metadata.st_mode):
                report.add("error", "symlink", "Symlinks are not allowed anywhere inside an Omarchy plugin.", path)
                trusted = False
                continue
            if entry.name == ".git" and stat.S_ISDIR(metadata.st_mode):
                continue
            if stat.S_ISDIR(metadata.st_mode):
                visit(path, depth + 1)
                continue
            if not stat.S_ISREG(metadata.st_mode):
                report.add("error", "special-file", "Only regular files and directories are allowed in a plugin.", path)
                trusted = False
                continue
            files += 1
            total += metadata.st_size
            if metadata.st_size > MAX_FILE_BYTES:
                report.add("error", "file-size", f"File exceeds {MAX_FILE_BYTES} bytes.", path)
                trusted = False
            if files > MAX_TREE_FILES or total > MAX_TREE_BYTES:
                report.add("error", "tree-size", "Plugin tree exceeds validator safety limits.", path)
                trusted = False
                return

    visit(root, 0)
    return trusted


def validate_publish_surface(root: Path, report: Report, strict: bool) -> None:
    readme = next((root / name for name in ("README.md", "README", "readme.md") if (root / name).is_file()), None)
    if not readme:
        report.add("warning" if not strict else "error", "readme-missing", "A root README is required for marketplace submission.")
    else:
        text = read_text(readme) or ""
        if "omarchy plugin add" not in text:
            report.add("warning" if not strict else "error", "install-docs", "README should include the standard omarchy plugin add command.", readme)
        if "omarchy plugin remove" not in text:
            report.add("warning" if not strict else "error", "remove-docs", "README should include the standard omarchy plugin remove command.", readme)
    if not any((root / name).is_file() for name in ("LICENSE", "LICENSE.md", "COPYING")):
        report.add("warning" if not strict else "error", "license-file", "A root license file is required for marketplace submission.")
    previews = [path for path in root.iterdir() if path.is_file() and path.name.lower() in PREVIEW_NAMES]
    if len(previews) > 1:
        report.add("error", "preview-count", "Use at most one supported root preview image.", previews[1])
    for preview in previews:
        if preview.stat().st_size > 50 * 1024 * 1024:
            report.add("error", "preview-size", "Preview exceeds the current 50 MB marketplace limit.", preview)


def scan_security(root: Path, report: Report) -> None:
    for path in iter_files(root):
        data = read_regular(path, MAX_FILE_BYTES)
        if data is None:
            continue
        mode = path.lstat().st_mode

        prefix = data[:4]
        if prefix.startswith(b"\x7fELF") or prefix.startswith(b"MZ") or prefix in {
            b"\xfe\xed\xfa\xce", b"\xfe\xed\xfa\xcf", b"\xce\xfa\xed\xfe", b"\xcf\xfa\xed\xfe",
        }:
            report.capability("bundled-executable-binary", "Bundled executable binary requires manual review.", path)

        name = path.name.lower()
        if re.search(r"(?:^|[-_.])(install|installer|setup|uninstall)(?:$|[-_.])", name):
            report.capability("installer", "Installer/setup/uninstall surface requires manual review.", path)

        if path.suffix.lower() not in TEXT_SUFFIXES and not stat.S_ISREG(mode):
            continue
        text = read_text(path)
        if text is None:
            continue
        lower = text.lower()

        if re.search(r"\b(?:curl|wget)\b[^\n]{0,500}(?:\||&&|;)\s*(?:sudo\s+|pkexec\s+)?(?:/\S*/)?(?:ba)?sh\b", text, re.IGNORECASE):
            report.finding("curl-pipe-shell", "Downloaded content is passed directly to a shell.", path)

        for line in text.splitlines():
            line_lower = line.lower()
            if "cargo install" in line_lower and "--git" in line_lower:
                rev = re.search(r"--rev(?:=|\s+)([0-9a-fA-F]{40})(?:\s|$)", line)
                if not rev:
                    report.finding("cargo-git-unpinned", "cargo install --git is not pinned to a full 40-character revision.", path)

        has_external_git = bool(re.search(r"\bgit\s+clone\s+(?:--\s+)?(?:https?|ssh|git@)", text, re.IGNORECASE))
        has_build_or_exec = bool(re.search(r"\b(?:cargo\s+(?:build|install)|go\s+build|cmake\b|make\b|npm\s+(?:install|ci)|pnpm\s+install|yarn\s+install|\.\/\S+)", text, re.IGNORECASE))
        has_full_checkout = bool(re.search(r"\bgit\s+(?:-C\s+\S+\s+)?checkout\s+--detach\s+[0-9a-fA-F]{40}\b", text))
        if has_external_git and has_build_or_exec:
            report.capability("remote-build", "External source is cloned and built or executed.", path)
            if not has_full_checkout:
                report.finding("remote-git-execution-unpinned", "External Git source is built or executed without a detached full-commit checkout.", path)

        if re.search(r"\b(?:pacman|yay|paru|apt(?:-get)?|dnf|zypper|brew|npm|pipx?)\s+(?:install|add|-S)\b", text, re.IGNORECASE):
            report.capability("package-manager", "Package-manager installation behavior requires review.", path)

        privilege_lines = [
            line for line in text.splitlines()
            if re.search(r"\b(?:sudo|pkexec)\b", line, re.IGNORECASE)
            and not re.search(r"\b(?:no|not|without|does not|doesn't|never)\b[^\n]{0,30}\b(?:sudo|pkexec)\b", line, re.IGNORECASE)
        ]
        if privilege_lines:
            report.capability("privilege", "Non-negated sudo or pkexec behavior requires review.", path)

        if re.search(r"\bNOPASSWD\s*:\s*(?:ALL|.*\b(?:bash|sh|zsh|fish|python\d*|perl|ruby)\b|.*\b(?:kill|systemctl|rm|cp|mv)\b.*\*)", text, re.IGNORECASE):
            report.finding("sudoers-dangerous-passwordless-command", "Broad or interpreter-capable NOPASSWD sudoers rule detected.", path)

        if re.search(r"/tmp/[^\s\"']*\.pid\b", text) and re.search(r"\b(?:sudo|pkexec)\b[^\n]{0,200}\b(?:kill|systemctl)\b", text, re.IGNORECASE):
            report.finding("privileged-process-control-from-shared-temp", "Privileged process control consumes predictable /tmp PID state.", path)

        if path.suffix == ".service" or re.search(r"\b(?:systemctl|systemd-run)\b", text):
            report.capability("service-management", "System service-management behavior requires review.", path)

        if "sudoers" in lower or "/etc/sudoers" in lower:
            report.capability("sudoers-modification", "Sudoers policy behavior requires complete manual review.", path)

        if path.suffix.lower() == ".qml":
            if re.search(r"\b(?:eval|Function|Qt\.createQmlObject)\s*\(", text):
                report.capability("qml-dynamic-code", "Dynamic QML/JavaScript code construction requires manual review.", path)
            if re.search(r"\b(?:XMLHttpRequest|WebSocket)\b", text):
                report.capability("qml-network", "QML network access requires manual review.", path)
            if re.search(r"\bProcess\s*\{", text):
                report.capability("qml-process", "QML process execution requires manual review.", path)


def print_text(result: dict[str, Any]) -> None:
    for key in ("errors", "warnings"):
        for item in result[key]:
            location = f" ({item['path']})" if item["path"] else ""
            print(f"{item['level'].upper()} {item['code']}: {item['message']}{location}")
    security = result["security"]
    if security["scanned"]:
        for key in ("findings", "capabilities"):
            for item in security[key]:
                location = f" ({item['path']})" if item["path"] else ""
                print(f"{item['level'].upper()} {item['code']}: {item['message']}{location}")
        print(f"SECURITY {security['outcome']}: {security['disclaimer']}")
    status = "VALID" if result["valid"] else "INVALID"
    print(f"{status}: {result['root']}")


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plugin_dir", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--security", action="store_true", help="Run advisory deterministic security checks.")
    parser.add_argument("--strict", action="store_true", help="Promote publish-surface and compatibility warnings to errors where defined.")
    parser.add_argument("--publish", action="store_true", help="Check root README, license, install/remove docs, and preview limits.")
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv or sys.argv[1:])
    root = Path(os.path.abspath(args.plugin_dir.expanduser()))
    report = Report(root)
    linked = path_has_symlink(root)
    if linked is not None:
        report.add("error", "plugin-directory-symlink", "Plugin path may not traverse a symlink.", linked)
    elif not root.is_dir() or root.is_symlink():
        report.add("error", "plugin-directory", "Plugin directory does not exist or is not a directory.", root)
    else:
        trusted = validate_tree(root, report)
        if trusted:
            manifest = load_manifest(root, report)
            if manifest is not None:
                validate_manifest(root, manifest, report, args.strict)
            if args.publish:
                validate_publish_surface(root, report, args.strict)
            if args.security:
                scan_security(root, report)
    result = report.result(args.security)
    if args.as_json:
        print(json.dumps(result, indent=2, sort_keys=True))
    else:
        print_text(result)
    if report.errors:
        return 1
    if args.security and report.findings:
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
