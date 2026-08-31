#!/usr/bin/env python3
"""Scan one exact Git tree for secrets and unsafe repository payloads."""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path, PurePosixPath
from typing import Any


MAX_FILES = 4096
MAX_FILE_BYTES = 32 * 1024 * 1024
MAX_TREE_BYTES = 128 * 1024 * 1024
TEXT_PREFIX_BYTES = 2 * 1024 * 1024
ALLOWED_BINARY_SUFFIXES = {".png"}
CREDENTIAL_NAMES = {
    ".env", ".npmrc", ".pypirc", "credentials", "credentials.json",
    "id_rsa", "id_ed25519", "service-account.json",
}
SECRET_PATTERNS = (
    ("private-key", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("github-token", re.compile(r"\b(?:gh[opusr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{30,})\b")),
    ("aws-access-key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("openai-key", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{24,}\b")),
    ("slack-token", re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{20,}\b")),
)
CAPABILITY_PATTERNS = (
    ("process-execution", re.compile(r"\b(?:subprocess\.|os\.system\(|QProcess\b|Process\s*\{)")),
    ("network-access", re.compile(r"\b(?:curl|wget|urllib|requests\.|fetch\s*\()")),
    ("recursive-delete", re.compile(r"\b(?:rm\s+-[A-Za-z]*r|shutil\.rmtree\s*\()")),
)


class ScanError(ValueError):
    pass


def _git(repo: Path, *arguments: str, input_bytes: bytes | None = None) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(repo), *arguments],
        input=input_bytes,
        capture_output=True,
        check=False,
    )
    if result.returncode:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise ScanError(detail or f"git {' '.join(arguments)} failed")
    return result.stdout


def _safe_path(raw: str) -> PurePosixPath:
    path = PurePosixPath(raw)
    if not raw or path.is_absolute() or ".." in path.parts or "." in path.parts:
        raise ScanError(f"unsafe Git path: {raw!r}")
    return path


def _entries(repo: Path, tree: str) -> list[dict[str, Any]]:
    raw = _git(repo, "ls-tree", "-rz", "-l", tree)
    entries: list[dict[str, Any]] = []
    total = 0
    for record in raw.split(b"\0"):
        if not record:
            continue
        try:
            header, name = record.split(b"\t", 1)
            mode, kind, object_id, size = header.decode("ascii").split(" ", 3)
            path = _safe_path(name.decode("utf-8"))
        except (ValueError, UnicodeDecodeError) as error:
            raise ScanError(f"malformed Git tree entry: {error}") from error
        if kind != "blob" or mode == "120000":
            raise ScanError(f"unsupported non-regular Git entry: {path}")
        try:
            length = int(size)
        except ValueError as error:
            raise ScanError(f"missing blob size for {path}") from error
        if length > MAX_FILE_BYTES:
            raise ScanError(f"file exceeds {MAX_FILE_BYTES} byte limit: {path}")
        total += length
        if total > MAX_TREE_BYTES:
            raise ScanError(f"tree exceeds {MAX_TREE_BYTES} byte limit")
        entries.append({"path": path, "mode": mode, "object": object_id, "size": length})
        if len(entries) > MAX_FILES:
            raise ScanError(f"tree exceeds {MAX_FILES} file limit")
    return entries


def scan(repo: Path, tree: str) -> dict[str, Any]:
    resolved = _git(repo, "rev-parse", f"{tree}^{{tree}}").decode("ascii").strip()
    findings: list[dict[str, Any]] = []
    entries = _entries(repo, resolved)
    for entry in entries:
        path: PurePosixPath = entry["path"]
        lower_name = path.name.lower()
        if lower_name in CREDENTIAL_NAMES or lower_name.endswith((".pem", ".key", ".p12", ".pfx")):
            findings.append({"severity": "error", "code": "credential-filename", "path": str(path)})
        data = _git(repo, "cat-file", "blob", entry["object"])
        if len(data) != entry["size"]:
            raise ScanError(f"blob size changed while reading: {path}")
        prefix = data[:TEXT_PREFIX_BYTES]
        try:
            text = prefix.decode("utf-8")
            binary = "\0" in text
        except UnicodeDecodeError:
            text = ""
            binary = True
        if binary:
            if path.suffix.lower() not in ALLOWED_BINARY_SUFFIXES:
                findings.append({"severity": "error", "code": "unapproved-binary", "path": str(path)})
            continue
        for code, pattern in SECRET_PATTERNS:
            if pattern.search(text):
                findings.append({"severity": "error", "code": code, "path": str(path)})
        for code, pattern in CAPABILITY_PATTERNS:
            if pattern.search(text):
                findings.append({"severity": "review", "code": code, "path": str(path)})
        if entry["mode"] == "100755":
            findings.append({"severity": "review", "code": "executable", "path": str(path)})
    errors = sum(item["severity"] == "error" for item in findings)
    return {
        "schemaVersion": 1,
        "tree": resolved,
        "files": len(entries),
        "bytes": sum(entry["size"] for entry in entries),
        "ok": errors == 0,
        "errors": errors,
        "reviewSignals": sum(item["severity"] == "review" for item in findings),
        "findings": findings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo", type=Path, default=Path(__file__).resolve().parent.parent)
    parser.add_argument("--git-tree", default="HEAD")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    try:
        report = scan(args.repo.resolve(), args.git_tree)
    except (OSError, ScanError) as error:
        report = {"schemaVersion": 1, "ok": False, "errors": 1, "error": str(error), "findings": []}
    if args.json:
        print(json.dumps(report, indent=2))
    elif report["ok"]:
        print(f"Security scan passed for {report['tree']} ({report['reviewSignals']} review signals).")
    else:
        print(f"Security scan failed: {report.get('error') or str(report['errors']) + ' blocking finding(s)' }", file=sys.stderr)
    return 0 if report["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
