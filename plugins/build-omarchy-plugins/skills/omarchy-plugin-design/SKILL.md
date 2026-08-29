---
name: omarchy-plugin-design
description: Design an Omarchy 4 Quattro shell plugin before implementation. Use when choosing plugin kinds, architecture, dependencies, state ownership, IPC, security boundaries, or evidence. Do not treat legacy package installers as shell plugins; route those through migration.
---

# Omarchy Plugin Design

Design the smallest complete plugin that fits Omarchy's hosted-shell model.

## Workflow

1. Inspect an existing repository and `manifest.json` before proposing a new
   structure. For a new project, read
   [references/kind-selection.md](references/kind-selection.md).
2. Decide the permanent namespaced plugin ID and one or more supported kinds.
   Never use the reserved `omarchy.*` namespace for third-party code.
3. Identify state ownership:
   - per widget instance and monitor;
   - process-wide singleton service;
   - durable user configuration stored inline in `shell.json`; or
   - external application state owned outside `omarchy-shell`.
4. Name every external command, package, credential source, network endpoint,
   and privileged operation. Prefer an existing authenticated CLI over reading
   or copying its credentials.
5. Define entry points, user-visible lifecycle, IPC methods, failure states,
   removal behavior, tests, demo fixtures, and screenshot evidence.
6. Produce a short design record before substantial implementation: ID, kinds,
   entry points, state boundaries, dependencies, IPC, security constraints,
   verification plan, and deferred scope.

## Invariants

- A third-party shell plugin is a Git repository with `manifest.json` at its
  root; Omarchy does not run install hooks or grant `sudo` during plugin add.
- Entry points are hosted QML `Item`s, never independent `ShellRoot`s or a
  second Quickshell process.
- Plugins execute unsandboxed inside the user's long-running shell. Keep the
  dependency and process surface explicit and reviewable.
- Prefer one end-to-end vertical slice with deterministic fixtures over a broad
  collection of unverified surfaces.
- Preserve distinct unavailable, unauthenticated, unsupported, offline, empty,
  and failed states; do not silently collapse them into generic fallback data.

Use the focused implementation skill for the selected surface after the design
record is agreed.
