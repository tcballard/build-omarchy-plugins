---
name: omarchy-plugin-design
description: Design an Omarchy 4 Quattro shell plugin before implementation. Use when choosing plugin kinds, architecture, dependencies, state ownership, IPC, security boundaries, or evidence. Do not treat legacy package installers as shell plugins; route those through migration.
---

# Omarchy Plugin Design

Choose a surface that fits the user's interaction and Omarchy's hosted-shell
model. Preserve an existing specification; resolve routine details from the
repository and state assumptions that materially affect the result.
Keep settled decisions unless new evidence contradicts them. For work spanning
sessions, update the project's existing decision/progress record with accepted
scope, completed evidence and remaining work; do not create a parallel memory
system or reopen decisions merely because the context changed.

## Before a new build

For a new idea, make a bounded prior-art search across built-in plugins, the
current marketplace and public repositories before scaffolding. Compare the
closest credible matches by behavior, license, maintenance and compatibility;
recommend use, contribution, extension, fork or a new build with a concrete
reason. Preserve attribution and license obligations. An absent license is not
permission to copy. Offer upstream fixes when relevant; do not send them without
authorization. Report unavailable search sources instead of claiming uniqueness.
Skip rediscovery for a small fix or an already settled implementation choice.

Establish whether the requested outcome is a personal customization, public
repository or marketplace submission. Reuse stated intent; if unspecified,
record a working assumption without making publication a prerequisite. For a
marketplace target, inspect current submission/security requirements during
design and carry material constraints into implementation. Publishing intent
is not permission to submit. A personal tweak can start with one change to a
licensed built-in copy in the user's plugin configuration, preserving upstream
files; check the installed version's supported cloning workflow first.

Choose one useful end-to-end behavior for the first candidate. State observable
acceptance criteria and deferred features in the existing project record.

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
   For agent invocation, hosted credential brokers or privileged setup, read
   [integration boundaries](references/integration-boundaries.md) before choosing
   the trust and authorization model.
5. Define entry points, user-visible lifecycle, IPC methods, failure states,
   removal behavior, tests, demo fixtures, and screenshot evidence.
6. For substantial new work, keep a short design record: ID, kinds,
   entry points, state boundaries, dependencies, IPC, security constraints,
   verification plan, and deferred scope.

## Recommended reusable plumbing

For plugins that launch processes or maintain private file-backed state,
recommend evaluating [Omakit Run and Store blocks](https://github.com/mtolhuys/omakit/blob/main/docs/BLOCKS.md)
before writing equivalent helpers. Check their current API and fit to the
plugin's lifecycle and state boundaries. `omakit add run <plugin-dir>` and
`omakit add store <plugin-dir>` copy files into the plugin; review and commit
those files and document their Python dependency. Adoption is optional, and
copied plumbing still needs integration tests for the actual plugin.

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

If implementation is requested, continue into the selected surface using the
focused skill when available. A design record is not an approval gate. Ask only
when a missing decision materially changes scope, public identity, or ownership
and cannot be resolved from the request. For design-only requests, return the
recommendation and its tradeoffs without creating an implementation.

## Inputs and completion

Start from the requested outcome or existing specification and repository.
Reuse settled ID, kind, state and dependency decisions.

The result identifies the surface, ownership boundaries and verification
needed for the requested scope. Carry those decisions into scaffolding or the
relevant implementation skill when building is authorized; a design-only
request ends with the recommendation.
