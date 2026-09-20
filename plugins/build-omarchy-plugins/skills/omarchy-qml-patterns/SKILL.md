---
name: omarchy-qml-patterns
description: Build or refactor QML hosted inside the Omarchy 4 Quattro shell, including plugin theme-token bindings, responsive layout, process execution and state. Use for QML implementation; global palette or shell.toml styling belongs to theme skills, and standalone Quickshell apps are outside this skill.
---

# Omarchy QML Patterns

For colour or spacing requests, identify the owner before editing. Fix a plugin's literal values or incorrect token bindings in its QML. Change shared palette values or shell TOML through omarchy-theme-palette or omarchy-theme-shell when available. For mixed tasks, keep the QML consumer and theme source changes scoped to their respective files; do not create a plugin merely to recolour the desktop.

Work inside Omarchy's existing shell process and preserve local repository
conventions.

## Core rules

- Entry points are QML `Item`s or Omarchy UI base components, never
  `ShellRoot`. Do not launch a second Quickshell instance.
- Declare host-injected properties with safe initial values for third-party
  entry points. The host assigns `omarchyPath`, `shell`, `manifest`, and the
  relevant registries after loading; `required` properties can fail before
  late injection on dynamically loaded components.
- Use `qs.Commons` tokens and `qs.Ui` components instead of copying first-party
  colors, dimensions, controls, or popup chrome.
- Treat one visual widget per monitor as normal. Keep shared polling and remote
  state in a service; keep hover, selection, and open state local to the visual
  instance.
- Run processes with argument arrays. Avoid `bash -c`; when a shell is truly
  required, quote every external value with Omarchy's `Util.shellQuote` and
  explain the boundary.
- Never put access tokens, complete environment dumps, or credential-bearing
  command output in QML properties that may be logged or displayed.

Read [references/hosted-qml.md](references/hosted-qml.md) for injected-property
and component patterns. Read
[references/theme-and-layout.md](references/theme-and-layout.md) for theme,
orientation, and monitor behavior. Read
[references/process-and-state.md](references/process-and-state.md) when QML
launches commands or owns asynchronous state.

For external data, automatic execution or mutable state, consult
[reviewer boundaries](references/reviewer-boundaries.md) for concrete failure
paths and relevant adversarial checks from marketplace reviews.

## Work from concrete examples

Start from the closest local working component and the examples in
[hosted QML](references/hosted-qml.md) and
[process/state](references/process-and-state.md). Read the code and its checks
before adapting it. Preserve the proven boundary, then verify the changed
behavior with a fixture: stale completion after reload, repeated refresh,
malformed output, or disablement while a helper is running, as applicable.
For supervised processes or private storage, evaluate Omakit's Run/Store
examples against the current API instead of inventing another helper.

Record which example/revision was used and what its tests actually establish.
Scaffold/static checks establish structure; only observed host checks establish
Qt imports and shell lifecycle. Do not call copied code tested merely because
its source project has a green badge.

## Verification

For a new data-driven surface, exercise loading, empty, success, partial failure,
authentication-required, and retry behavior when those states exist. For a
targeted change, verify the affected state or interaction with fictional
fixtures. Run required repository checks and relevant QML tests; record live
shell behavior only when observed on Omarchy. Do not block a portable patch on
an unavailable display or treat stubs as proof of host integration.

## Inputs and completion

Apply these patterns to the requested change in the actual hosted entry point
or shared component, using the existing surface and state decisions.

Leave a focused patch and evidence for the affected behavior. Carry changed
components and unavailable host checks back to the surface workflow or
testing; using a documented pattern by itself is not verification.
