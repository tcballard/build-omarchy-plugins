#!/usr/bin/env python3
"""Build deterministic release artifacts from one exact Git commit."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import stat
import subprocess
import sys
import tempfile
import zipfile
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from typing import Any, Callable, Iterable


FIXED_TIME = (2026, 8, 31, 0, 0, 0)
MAX_FILES = 4096
MAX_FILE_BYTES = 32 * 1024 * 1024
MAX_TREE_BYTES = 128 * 1024 * 1024
VERSION_RE = re.compile(r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)$")
SOURCE_SCHEMA = "https://github.com/tcballard/build-omarchy-plugins/schemas/source-manifest-v1.json"
RELEASE_SCHEMA = "https://github.com/tcballard/build-omarchy-plugins/schemas/release-manifest-v1.json"


class PackageError(ValueError):
    pass


@dataclass(frozen=True)
class Blob:
    path: PurePosixPath
    mode: str
    object_id: str
    data: bytes

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.data).hexdigest()


def _git(repo: Path, *arguments: str) -> bytes:
    result = subprocess.run(["git", "-C", str(repo), *arguments], capture_output=True, check=False)
    if result.returncode:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise PackageError(detail or f"git {' '.join(arguments)} failed")
    return result.stdout


def _safe_relative(raw: str) -> PurePosixPath:
    path = PurePosixPath(raw)
    if not raw or path.is_absolute() or "." in path.parts or ".." in path.parts:
        raise PackageError(f"unsafe source path: {raw!r}")
    return path


def load_tree(repo: Path, revision: str) -> tuple[str, str, dict[PurePosixPath, Blob]]:
    commit = _git(repo, "rev-parse", f"{revision}^{{commit}}").decode("ascii").strip()
    tree = _git(repo, "rev-parse", f"{commit}^{{tree}}").decode("ascii").strip()
    records = _git(repo, "ls-tree", "-rz", "-l", tree).split(b"\0")
    blobs: dict[PurePosixPath, Blob] = {}
    total = 0
    for record in records:
        if not record:
            continue
        try:
            header, raw_path = record.split(b"\t", 1)
            mode, kind, object_id, size_text = header.decode("ascii").split(" ", 3)
            path = _safe_relative(raw_path.decode("utf-8"))
            size = int(size_text)
        except (UnicodeDecodeError, ValueError) as error:
            raise PackageError(f"malformed Git tree entry: {error}") from error
        if kind != "blob" or mode == "120000":
            raise PackageError(f"release tree contains unsupported non-regular entry: {path}")
        if size > MAX_FILE_BYTES:
            raise PackageError(f"release file exceeds {MAX_FILE_BYTES} bytes: {path}")
        total += size
        if total > MAX_TREE_BYTES:
            raise PackageError(f"release tree exceeds {MAX_TREE_BYTES} bytes")
        if len(blobs) >= MAX_FILES:
            raise PackageError(f"release tree exceeds {MAX_FILES} files")
        data = _git(repo, "cat-file", "blob", object_id)
        if len(data) != size:
            raise PackageError(f"Git blob size mismatch: {path}")
        blobs[path] = Blob(path, mode, object_id, data)
    return commit, tree, blobs


def _json_blob(blob: Blob) -> dict[str, Any]:
    try:
        value = json.loads(blob.data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise PackageError(f"invalid JSON in {blob.path}: {error}") from error
    if not isinstance(value, dict):
        raise PackageError(f"expected JSON object in {blob.path}")
    return value


def _json_bytes(value: Any) -> bytes:
    return (json.dumps(value, indent=2, sort_keys=True, ensure_ascii=False) + "\n").encode("utf-8")


def _archive_bytes(entries: Iterable[tuple[Blob, PurePosixPath]]) -> tuple[bytes, int]:
    ordered = sorted(entries, key=lambda item: item[1].as_posix())
    names: set[str] = set()
    with tempfile.SpooledTemporaryFile(max_size=64 * 1024 * 1024) as handle:
        with zipfile.ZipFile(handle, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
            for blob, member in ordered:
                name = member.as_posix()
                _safe_relative(name)
                folded = name.casefold()
                if folded in names:
                    raise PackageError(f"case-insensitive archive collision: {name}")
                names.add(folded)
                info = zipfile.ZipInfo(name, FIXED_TIME)
                mode = 0o755 if blob.mode == "100755" else 0o644
                info.external_attr = (stat.S_IFREG | mode) << 16
                info.compress_type = zipfile.ZIP_DEFLATED
                info.create_system = 3
                archive.writestr(info, blob.data)
        handle.seek(0)
        return handle.read(), len(ordered)


def _selected(
    blobs: dict[PurePosixPath, Blob],
    predicate: Callable[[PurePosixPath], bool],
    mapper: Callable[[PurePosixPath], PurePosixPath],
) -> list[tuple[Blob, PurePosixPath]]:
    return [(blob, mapper(path)) for path, blob in blobs.items() if predicate(path)]


def _write(path: Path, data: bytes) -> None:
    temporary = path.with_name(f".{path.name}.tmp-{os.getpid()}")
    try:
        with temporary.open("xb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def _source_manifest(version: str, commit: str, tree: str, blobs: dict[PurePosixPath, Blob]) -> bytes:
    return _json_bytes({
        "$schema": SOURCE_SCHEMA,
        "schemaVersion": 1,
        "name": "build-omarchy-plugins",
        "version": version,
        "source": {
            "repository": "https://github.com/tcballard/build-omarchy-plugins",
            "commit": commit,
            "tree": tree,
        },
        "files": [
            {"path": path.as_posix(), "mode": blob.mode, "bytes": len(blob.data), "sha256": blob.sha256}
            for path, blob in sorted(blobs.items(), key=lambda item: item[0].as_posix())
        ],
    })


def _sbom(version: str, commit: str, blobs: dict[PurePosixPath, Blob]) -> bytes:
    created = datetime(2026, 8, 31, tzinfo=timezone.utc).isoformat().replace("+00:00", "Z")
    files = []
    relationships = [{"spdxElementId": "SPDXRef-DOCUMENT", "relationshipType": "DESCRIBES", "relatedSpdxElement": "SPDXRef-Package"}]
    for index, (path, blob) in enumerate(sorted(blobs.items(), key=lambda item: item[0].as_posix()), start=1):
        spdx_id = f"SPDXRef-File-{index}"
        files.append({
            "SPDXID": spdx_id,
            "fileName": f"./{path.as_posix()}",
            "checksums": [{"algorithm": "SHA256", "checksumValue": blob.sha256}],
        })
        relationships.append({"spdxElementId": "SPDXRef-Package", "relationshipType": "CONTAINS", "relatedSpdxElement": spdx_id})
    return _json_bytes({
        "spdxVersion": "SPDX-2.3",
        "dataLicense": "CC0-1.0",
        "SPDXID": "SPDXRef-DOCUMENT",
        "name": f"build-omarchy-plugins-{version}-source",
        "documentNamespace": f"https://github.com/tcballard/build-omarchy-plugins/spdx/{version}/{commit}",
        "creationInfo": {"created": created, "creators": ["Tool: build-omarchy-plugins/package_submission.py"]},
        "packages": [{
            "name": "build-omarchy-plugins",
            "SPDXID": "SPDXRef-Package",
            "versionInfo": version,
            "downloadLocation": f"git+https://github.com/tcballard/build-omarchy-plugins.git@{commit}",
            "filesAnalyzed": True,
            "licenseConcluded": "MIT",
            "licenseDeclared": "MIT",
            "copyrightText": "NOASSERTION",
        }],
        "files": files,
        "relationships": relationships,
    })


def build(repo: Path, output: Path, revision: str, require_clean: bool) -> dict[str, Any]:
    if require_clean and _git(repo, "status", "--porcelain=v1", "--untracked-files=all"):
        raise PackageError("--require-clean refused a dirty or untracked working tree")
    commit, tree, blobs = load_tree(repo, revision)
    try:
        version = blobs[PurePosixPath("VERSION")].data.decode("utf-8").strip()
        portable = _json_blob(blobs[PurePosixPath("plugin.json")])
        adapter = _json_blob(blobs[PurePosixPath("plugins/build-omarchy-plugins/.codex-plugin/plugin.json")])
    except KeyError as error:
        raise PackageError(f"release tree is missing required file: {error.args[0]}") from error
    if not VERSION_RE.fullmatch(version) or portable.get("version") != version or adapter.get("version") != version:
        raise PackageError("VERSION and both plugin manifests must contain the same strict semver")

    policy_names = {"README.md", "PORTABILITY.md", "LICENSE", "SECURITY.md", "PRIVACY.md", "TERMS.md", "SUPPORT.md"}
    portable_entries = _selected(
        blobs,
        lambda p: p == PurePosixPath("plugin.json") or p.parts[:1] == ("skills",) or p.as_posix() in policy_names,
        lambda p: PurePosixPath("build-omarchy-plugins") / p,
    )
    adapter_prefix = PurePosixPath("plugins/build-omarchy-plugins")
    adapter_entries = _selected(
        blobs,
        lambda p: p.parts[:2] == ("plugins", "build-omarchy-plugins"),
        lambda p: PurePosixPath("build-omarchy-plugins") / p.relative_to(adapter_prefix),
    )
    skills_prefix = PurePosixPath("plugins/build-omarchy-plugins/skills")
    skills_entries = _selected(
        blobs,
        lambda p: p.parts[:3] == ("plugins", "build-omarchy-plugins", "skills"),
        lambda p: PurePosixPath("skills") / p.relative_to(skills_prefix),
    )
    submission_entries = _selected(
        blobs,
        lambda p: (
            p.parts[:1] == ("submission",)
            or p.as_posix() in {"PRIVACY.md", "TERMS.md", "SUPPORT.md", "SECURITY.md"}
            or p.as_posix() in {
                "plugins/build-omarchy-plugins/assets/app-icon.png",
                "plugins/build-omarchy-plugins/assets/workflow.png",
            }
        ),
        lambda p: p,
    )
    archive_specs = (
        ("agent-plugin", f"build-omarchy-plugins-agent-plugin-{version}.zip", portable_entries),
        ("openai-plugin", f"build-omarchy-plugins-plugin-{version}.zip", adapter_entries),
        ("openai-skills", f"build-omarchy-plugins-skills-{version}.zip", skills_entries),
        ("submission", f"build-omarchy-plugins-submission-{version}.zip", submission_entries),
    )
    output.mkdir(parents=True, exist_ok=True)
    if output.is_symlink() or not output.is_dir():
        raise PackageError(f"output path is not a directory: {output}")
    artifacts = []
    for kind, name, entries in archive_specs:
        data, count = _archive_bytes(entries)
        _write(output / name, data)
        artifacts.append({"name": name, "kind": kind, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest(), "members": count})

    source_bytes = _source_manifest(version, commit, tree, blobs)
    sbom_bytes = _sbom(version, commit, blobs)
    _write(output / "SOURCE-MANIFEST.json", source_bytes)
    _write(output / "SBOM.spdx.json", sbom_bytes)
    documents = [
        {"name": "SOURCE-MANIFEST.json", "kind": "source-manifest", "bytes": len(source_bytes), "sha256": hashlib.sha256(source_bytes).hexdigest()},
        {"name": "SBOM.spdx.json", "kind": "spdx-sbom", "bytes": len(sbom_bytes), "sha256": hashlib.sha256(sbom_bytes).hexdigest()},
    ]
    release = {
        "$schema": RELEASE_SCHEMA,
        "schemaVersion": 1,
        "name": "build-omarchy-plugins",
        "version": version,
        "source": {"repository": "https://github.com/tcballard/build-omarchy-plugins", "commit": commit, "tree": tree},
        "artifacts": artifacts,
        "releaseDocuments": documents,
        "checksums": "SHA256SUMS",
    }
    release_bytes = _json_bytes(release)
    _write(output / "RELEASE-MANIFEST.json", release_bytes)
    subjects = [item["name"] for item in artifacts] + [item["name"] for item in documents] + ["RELEASE-MANIFEST.json"]
    sums = "".join(f"{hashlib.sha256((output / name).read_bytes()).hexdigest()}  {name}\n" for name in sorted(subjects))
    _write(output / "SHA256SUMS", sums.encode("ascii"))
    return {**release, "output": str(output), "files": sorted([*subjects, "SHA256SUMS"])}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--git-tree", default="HEAD", help="Commit or tag to package; must peel to a commit.")
    parser.add_argument("--require-clean", action="store_true")
    args = parser.parse_args(argv or sys.argv[1:])
    repo = Path(__file__).resolve().parent.parent
    output = (args.output_dir or repo / "dist").resolve(strict=False)
    try:
        report = build(repo, output, args.git_tree, args.require_clean)
    except (OSError, PackageError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
