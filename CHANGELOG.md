# Changelog

All notable changes to Build Omarchy Plugins are documented here.

## 0.2.2 — 2026-08-31

- Harden release construction, installation lifecycle, host diagnostics,
  repository governance, and submission evidence without overstating live-host
  or provider verification.

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
