# Release notes — 0.3.0

Prepares the provider-neutral skills for Astra, Claude Fable and other frontier
models. The
same twelve skills install into shared Agent Skills paths or native Codex,
Cursor, Gemini CLI, Claude Code, and OpenCode locations without calling a model
API.

This candidate revises task completion, scope, approval reuse, focused edits,
verification and progress reporting. It fixes host-conformance text output and
Codex skill discovery, and adds ten behavioral cases. No live Fable execution or
model-specific performance improvement is claimed.

It retains transactional managed updates and removal, read-only host
discovery diagnostics, a deny-by-default OpenCode conformance probe,
deterministic exact-tree archives, source and release manifests, an SPDX 2.3
SBOM, SHA-256 coverage, stricter scaffold and QML trust-boundary checks, and
tag/asset provenance verification. CI covers Linux, macOS, and Windows;
release automation can prepare a verified draft but cannot publish it. The
release path validates every workflow with pinned actionlint, inspects
unpublished drafts through the supported GitHub CLI surface, and retries initial
asset downloads before comparing the uploaded release byte-for-byte.

Live Omarchy and model-provider compatibility remains explicitly evidence
bounded. Static validation and filesystem discovery are not described as a
security audit or a successful host invocation.
