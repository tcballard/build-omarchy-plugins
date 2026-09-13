# Changelog

All notable changes to Build Omarchy Plugins are documented here.

## 0.3.2 — Unreleased

- Catch privilege-tool mentions in documentation before marketplace submission,
  including negated prose and real commands on the same line.
- Explain documentation-only capability warnings and distinguish compatibility,
  security review, maintainer approval and publication at the exact candidate SHA.
- Pin the marketplace security policy and synchronize portable/OpenAI guidance.
- Document skill workflows and evidence handoffs, including stale-candidate and
  marketplace-review behavioral cases; these cases are not recorded model runs.
- Align version metadata, installation examples and submission materials with v0.3.2.

## 0.3.1 — 2026-09-12

- Add native Claude Code packaging and adoption documentation.
- Incorporate marketplace reviewer evidence into targeted pre-submission guidance.
- Allow the release workflow to create a new annotated tag after exact-commit checks.
- Update marketplace submission categories and tag labels against a pinned upstream form.
- Add advisory checks and a reviewer-response evidence table for recurring findings.
- Require strict Claude manifest validation in CI alongside the cross-platform matrix.
- Align release metadata, installation examples and submission materials with v0.3.1.

## 0.3.0

- Review all twelve skills against OpenAI Astra and Anthropic Fable guidance.
- Preserve authorized task scope, settled decisions and evidence-backed progress.
- Make testing proportional, helper paths explicit and Workbench registration optional.
- Fix host-conformance text output and Codex ancestor/duplicate discovery.
- Add provider guidance, dated reviews and ten behavioral evaluation cases.

- Generate agent-neutral Workbench environment probes and a capability-gated validation workflow.
- Generate the schema-one Plugin Workbench project definition by default.
- Register `./tests/run` as an explicit, initially untrusted Workbench check.
- Pin and verify the upstream Workbench authoring contract.
- Document the separately versioned builder and local-lifecycle companion boundary.

## 0.2.3 — 2026-08-31

- Validate every GitHub Actions workflow with pinned actionlint and include
  workflow validation in the stable required CI gate.
- Repair draft-release recovery by inspecting unpublished drafts through the
  GitHub CLI instead of a REST tag endpoint that excludes draft releases.
- Retry newly created draft asset downloads with bounded backoff before the
  byte-for-byte release comparison, while preserving exact tag/main binding
  and owner-controlled publication.

## 0.2.2 — 2026-08-31

- Add transactional install, update, diff, recovery, and conservative uninstall
  with receipts, locks, symlink/hardlink defenses, and managed-file integrity.
- Add read-only discovery diagnostics for Codex, Cursor, Gemini CLI, Claude
  Code, and OpenCode, plus a deny-by-default OpenCode live-conformance probe.
- Build byte-reproducible archives from one exact Git tree with release/source
  manifests, SPDX 2.3 SBOM, and complete SHA-256 coverage.
- Add exact-tree secret, binary, symlink, QML capability, and trust-boundary
  scanning without presenting static findings as a security guarantee.
- Harden scaffolding and validation against duplicate JSON keys, oversized or
  special files, unsafe ancestors, dynamic QML behavior, and unpinned actions.
- Bind tagged release preflights to annotated local/remote tags, the remote
  default branch, historical reachability, downloaded assets, and checksums.
- Add PR-only contribution policy, immutable action pins, a Linux/macOS/Windows
  CI matrix, CodeQL, upstream-contract drift checks, and draft-only release
  automation with owner-controlled publication.
- Expand installation, removal, reviewer, submission, and release documentation
  while keeping provider and live-host claims evidence-bounded.

## 0.2.1 — 2026-08-30

- Add an explicit OpenCode installer target using its native project and global
  Agent Skills directories.
- Add OpenCode installation and idempotency coverage to the host matrix.
- Document that OpenCode can also discover the shared `.agents/skills` target.

## 0.2.0 — 2026-08-30

- Add a provider-neutral Agent Plugins 1.0.0 package at the repository root.
- Make the twelve canonical skills free of provider-specific metadata.
- Add safe project/user installers for shared Agent Skills, Codex, Cursor,
  Gemini CLI, Claude Code, and custom destinations.
- Preserve the existing OpenAI plugin as a thin adapter with deterministic
  source synchronisation and drift checks.
- Add offline portable-manifest validation, conflict/idempotency tests, and a
  deterministic Agent Plugin release archive.
- Document the exact portability, runtime, safety, and live-evaluation boundary.

## 0.1.0 — 2026-08-29

- Add twelve routed skills covering the complete Omarchy 4 Quattro plugin lifecycle.
- Add a repository generator for all six current shell plugin kinds.
- Add structural, path, symlink, QML, and advisory security validation.
- Add read-only diagnostics, deterministic demos, release preflight, and marketplace submission tooling.
- Add migration guidance for separating legacy machine integration from Quattro shell surfaces.
- Add repeatable tests, submission archives, artwork, policies, and reviewer materials.
