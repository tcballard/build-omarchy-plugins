#!/usr/bin/env python3
"""Preflight a public Omarchy plugin release without publishing it."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from pathlib import PurePosixPath


MAX_JSON_BYTES = 4 * 1024 * 1024
SEMVER = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?"
    r"(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
TAG = re.compile(r"^v((?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?(?:\+[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?)$")


@dataclass
class Item:
    level: str
    code: str
    message: str
    detail: str = ""


def run(command: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(command, cwd=cwd, text=True, capture_output=True, check=False)


def validator_path() -> Path:
    return Path(__file__).resolve().parents[2] / "omarchy-plugin-test" / "scripts" / "validate_plugin.py"


def normalize_remote(value: str) -> str:
    value = value.strip()
    match = re.fullmatch(r"git@github\.com:([^/]+)/(.+?)(?:\.git)?", value)
    if match:
        return f"https://github.com/{match.group(1)}/{match.group(2)}"
    if value.startswith("https://github.com/"):
        return value.removesuffix(".git").rstrip("/")
    return value


def strict_json_object(text: str) -> dict[str, object]:
    def pairs(values: list[tuple[str, object]]) -> dict[str, object]:
        result: dict[str, object] = {}
        for key, value in values:
            if key in result:
                raise ValueError(f"duplicate JSON key: {key}")
            result[key] = value
        return result

    try:
        value = json.loads(text, object_pairs_hook=pairs)
    except json.JSONDecodeError as error:
        raise ValueError(str(error)) from error
    if not isinstance(value, dict):
        raise ValueError("top-level JSON value must be an object")
    return value


def strict_object(path: Path) -> dict[str, object]:
    if path.stat().st_size > MAX_JSON_BYTES:
        raise ValueError(f"JSON exceeds {MAX_JSON_BYTES} bytes")
    try:
        return strict_json_object(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as error:
        raise ValueError(str(error)) from error


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def safe_asset_name(value: object) -> str | None:
    if not isinstance(value, str) or not value or PurePosixPath(value).name != value:
        return None
    if value in {".", ".."} or "\\" in value or "\x00" in value:
        return None
    return value


def validate_release_directory(
    directory: Path,
    expected_source: dict[str, str],
    version: str,
    add: object,
) -> None:
    emit = add  # keep the call sites compact while retaining the nested reporter
    documents: dict[str, dict[str, object]] = {}
    for name in ("RELEASE-MANIFEST.json", "SOURCE-MANIFEST.json", "SBOM.spdx.json"):
        path = directory / name
        try:
            documents[name] = strict_object(path)
        except (OSError, ValueError) as error:
            emit("error", "release-json", f"{name} is missing or invalid.", str(error))
    if len(documents) != 3:
        return

    release = documents["RELEASE-MANIFEST.json"]
    source = documents["SOURCE-MANIFEST.json"]
    sbom = documents["SBOM.spdx.json"]
    for name, document in (("release", release), ("source", source)):
        if document.get("schemaVersion") != 1 or document.get("version") != version or document.get("source") != expected_source:
            emit("error", f"{name}-identity", f"{name.title()} manifest does not bind the selected version, repository, commit, and tree.")
    packages = sbom.get("packages")
    if sbom.get("spdxVersion") != "SPDX-2.3" or not isinstance(packages, list) or len(packages) != 1:
        emit("error", "sbom-structure", "SBOM must be one SPDX 2.3 package document.")
    else:
        package = packages[0]
        if not isinstance(package, dict) or package.get("versionInfo") != version or not str(package.get("downloadLocation", "")).endswith("@" + expected_source["commit"]):
            emit("error", "sbom-identity", "SBOM package does not bind the selected version and commit.")

    listed: dict[str, str] = {}
    for group in (release.get("artifacts"), release.get("releaseDocuments")):
        if not isinstance(group, list):
            emit("error", "release-files", "Release manifest artifact lists must be arrays.")
            continue
        for entry in group:
            if not isinstance(entry, dict) or safe_asset_name(entry.get("name")) is None:
                emit("error", "release-file-name", "Release manifest contains an unsafe asset name.")
                continue
            name = str(entry["name"])
            if name in listed:
                emit("error", "release-file-duplicate", "Release manifest repeats an asset name.", name)
                continue
            path = directory / name
            if not path.is_file() or path.is_symlink():
                emit("error", "release-file-missing", "Release asset is missing or not a regular file.", name)
                continue
            digest = sha256(path)
            if entry.get("bytes") != path.stat().st_size or entry.get("sha256") != digest:
                emit("error", "release-file-integrity", "Release asset size or digest does not match its manifest.", name)
            listed[name] = digest
    release_digest = sha256(directory / "RELEASE-MANIFEST.json")
    listed["RELEASE-MANIFEST.json"] = release_digest

    sums_path = directory / "SHA256SUMS"
    sums: dict[str, str] = {}
    try:
        for line in sums_path.read_text(encoding="ascii").splitlines():
            match = re.fullmatch(r"([0-9a-f]{64})  ([^\r\n]+)", line)
            if not match or safe_asset_name(match.group(2)) is None or match.group(2) in sums:
                raise ValueError("malformed, unsafe, or duplicate checksum entry")
            sums[match.group(2)] = match.group(1)
    except (OSError, UnicodeError, ValueError) as error:
        emit("error", "checksums-format", "SHA256SUMS is missing or invalid.", str(error))
        return
    if sums != listed:
        emit("error", "checksums-coverage", "SHA256SUMS must exactly cover every manifested release file.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("plugin_dir", type=Path)
    parser.add_argument("--json", action="store_true", dest="as_json")
    parser.add_argument("--allow-dirty", action="store_true")
    parser.add_argument("--tag", help="Verify an existing annotated vX.Y.Z release tag.")
    parser.add_argument("--published", action="store_true", help="Verify a historical published tag; requires --tag and --release-dir.")
    parser.add_argument("--release-dir", type=Path, help="Verify release manifests, SBOM, assets, and checksums in this directory.")
    args = parser.parse_args(argv or sys.argv[1:])
    root = args.plugin_dir.expanduser().resolve(strict=False)
    items: list[Item] = []

    def add(level: str, code: str, message: str, detail: str = "") -> None:
        items.append(Item(level, code, message, detail))

    if args.published and (not args.tag or args.release_dir is None):
        add("error", "published-arguments", "--published requires both --tag and --release-dir.")

    validator = validator_path()
    if not validator.is_file():
        add("error", "validator-missing", "Bundled Omarchy validator is missing.", str(validator))
    elif root.is_dir():
        result = run([sys.executable, str(validator), "--json", "--security", "--publish", "--strict", str(root)], root)
        try:
            payload = json.loads(result.stdout)
            for error in payload.get("errors", []):
                add("error", error["code"], error["message"], error.get("path", ""))
            for warning in payload.get("warnings", []):
                add("warning", warning["code"], warning["message"], warning.get("path", ""))
            security = payload.get("security", {})
            for finding in security.get("findings", []):
                add("error", finding["code"], finding["message"], finding.get("path", ""))
            for capability in security.get("capabilities", []):
                add("warning", capability["code"], capability["message"], capability.get("path", ""))
        except json.JSONDecodeError:
            add("error", "validator-output", "Bundled validator returned unreadable output.", result.stderr.strip())

    if not root.is_dir():
        add("error", "plugin-directory", "Plugin directory does not exist.", str(root))
    else:
        git = run(["git", "rev-parse", "--show-toplevel"], root)
        if git.returncode != 0:
            add("error", "git-repository", "Plugin must be in a Git repository.", git.stderr.strip())
        else:
            top = Path(git.stdout.strip()).resolve()
            if top != root:
                add("warning", "repository-root", "Plugin directory is not the Git repository root.", str(top))
            status = run(["git", "status", "--porcelain"], root)
            if status.stdout.strip() and not args.allow_dirty:
                add("error", "dirty-tree", "Git working tree is not clean.", status.stdout.strip()[:2000])
            head = run(["git", "rev-parse", "HEAD"], root)
            candidate = head.stdout.strip()
            if head.returncode == 0 and re.fullmatch(r"[0-9a-f]{40}\n?", head.stdout):
                add("info", "release-sha", "Release candidate full SHA.", head.stdout.strip())
            else:
                add("error", "release-sha", "Could not resolve a full release SHA.", head.stderr.strip())
            normalized = ""
            remote = run(["git", "remote", "get-url", "origin"], root)
            if remote.returncode != 0:
                add("error", "origin-missing", "A public GitHub origin is required for marketplace release.")
            else:
                normalized = normalize_remote(remote.stdout)
                if not re.fullmatch(r"https://github\.com/[^/]+/[^/]+", normalized):
                    add("error", "origin-github", "Origin is not a GitHub repository root URL.", normalized)
                else:
                    add("info", "origin", "Release repository.", normalized)

            manifest_version = ""
            manifest_path = root / "manifest.json"
            try:
                manifest = strict_object(manifest_path)
                manifest_version = manifest.get("version", "") if isinstance(manifest.get("version"), str) else ""
                if not SEMVER.fullmatch(manifest_version):
                    add("error", "manifest-version", "manifest.json must contain a strict semantic version.")
            except (OSError, ValueError) as error:
                add("error", "manifest-json", "manifest.json is missing or invalid.", str(error))

            if args.tag:
                tag_match = TAG.fullmatch(args.tag)
                if not tag_match:
                    add("error", "tag-format", "Release tag must be vX.Y.Z semantic version form.", args.tag)
                tag_type = run(["git", "cat-file", "-t", f"refs/tags/{args.tag}"], root)
                peeled = run(["git", "rev-parse", f"refs/tags/{args.tag}^{{commit}}"], root)
                tag_object = run(["git", "rev-parse", f"refs/tags/{args.tag}"], root)
                if tag_type.stdout.strip() != "tag" or peeled.returncode or tag_object.returncode:
                    add("error", "tag-annotated", "Release tag must exist locally as an annotated tag.")
                else:
                    candidate = peeled.stdout.strip()
                    remote_tag = run(["git", "ls-remote", "origin", f"refs/tags/{args.tag}", f"refs/tags/{args.tag}^{{}}"], root)
                    remote_values = dict(
                        reversed(line.split("\t", 1)) for line in remote_tag.stdout.splitlines() if "\t" in line
                    ) if remote_tag.returncode == 0 else {}
                    if remote_values.get(f"refs/tags/{args.tag}") != tag_object.stdout.strip() or remote_values.get(f"refs/tags/{args.tag}^{{}}") != candidate:
                        add("error", "remote-tag", "Remote annotated tag does not exactly match the local tag object and commit.")
                    remote_head = run(["git", "ls-remote", "--symref", "origin", "HEAD"], root)
                    remote_head_sha = ""
                    remote_head_ref = ""
                    for line in remote_head.stdout.splitlines():
                        if line.startswith("ref: ") and line.endswith("\tHEAD"):
                            remote_head_ref = line[5:].split("\t", 1)[0]
                        elif line.endswith("\tHEAD"):
                            remote_head_sha = line.split("\t", 1)[0]
                    if remote_head.returncode or not re.fullmatch(r"refs/heads/[^\s]+", remote_head_ref) or not re.fullmatch(r"[0-9a-f]{40}", remote_head_sha):
                        add("error", "remote-head", "Could not bind the release to the remote default branch.")
                    if args.published:
                        remote_object = run(["git", "cat-file", "-e", f"{remote_head_sha}^{{commit}}"], root)
                        reachable = run(["git", "merge-base", "--is-ancestor", candidate, remote_head_sha], root) if remote_object.returncode == 0 else remote_object
                        if remote_head_sha and reachable.returncode != 0:
                            add("error", "published-reachability", "Published tag commit is not reachable from the remote default-branch history available locally.")
                    elif candidate != head.stdout.strip():
                        add("error", "tag-head", "Unpublished release tag must identify the current HEAD exactly.")
                    elif remote_head_sha and candidate != remote_head_sha:
                        add("error", "tag-remote-head", "Unpublished release tag must identify the remote default-branch HEAD exactly.")

                    relative_manifest = (root.relative_to(top) / "manifest.json").as_posix()
                    tagged_manifest = run(["git", "show", f"{candidate}:{relative_manifest}"], root)
                    try:
                        selected = strict_json_object(tagged_manifest.stdout) if tagged_manifest.returncode == 0 else {}
                        selected_version = selected.get("version", "")
                        if not isinstance(selected_version, str) or not SEMVER.fullmatch(selected_version):
                            raise ValueError("tagged manifest has no strict semantic version")
                        manifest_version = selected_version
                    except ValueError as error:
                        add("error", "tag-manifest", "Could not read a valid manifest from the tagged commit.", str(error))
                    if tag_match and tag_match.group(1) != manifest_version:
                        add("error", "tag-version", "Release tag and tagged manifest version differ.")

            tree = run(["git", "rev-parse", f"{candidate}^{{tree}}"], root)
            if args.release_dir is not None and re.fullmatch(r"[0-9a-f]{40}", candidate) and tree.returncode == 0:
                release_dir = args.release_dir.expanduser().resolve(strict=False)
                expected = {"repository": normalized, "commit": candidate, "tree": tree.stdout.strip()}
                if not release_dir.is_dir() or release_dir.is_symlink():
                    add("error", "release-directory", "Release directory is missing or unsafe.", str(release_dir))
                elif manifest_version:
                    validate_release_directory(release_dir, expected, manifest_version, add)

        tests = root / "tests" / "run"
        if not tests.is_file():
            add("error", "tests-run", "tests/run is required for reproducible portable checks.")
        elif not os.access(tests, os.X_OK):
            add("error", "tests-executable", "tests/run must be executable.")
        workflow = root / ".github" / "workflows"
        if not workflow.is_dir() or not any(workflow.glob("*.yml")) and not any(workflow.glob("*.yaml")):
            add("warning", "ci-missing", "No GitHub Actions workflow was found.")
        preview = [path for path in root.iterdir() if path.name.lower() in {"preview.png", "preview.jpg", "preview.jpeg", "preview.webp", "preview.avif"}]
        if not preview:
            add("warning", "preview-missing", "Visual plugins should include a current root marketplace preview.")

    ok = not any(item.level == "error" for item in items)
    result_payload = {
        "plugin_dir": str(root),
        "ok": ok,
        "items": [asdict(item) for item in items],
        "mutated": False,
        "disclaimer": "Static checks are evidence, not a security audit or compatibility guarantee.",
    }
    if args.as_json:
        print(json.dumps(result_payload, indent=2, sort_keys=True))
    else:
        for item in items:
            detail = f" — {item.detail}" if item.detail else ""
            print(f"{item.level.upper()} {item.code}: {item.message}{detail}")
        print("READY" if ok else "NOT READY")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
