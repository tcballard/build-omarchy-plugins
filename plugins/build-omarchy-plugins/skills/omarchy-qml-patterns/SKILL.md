---
name: omarchy-qml-patterns
description: Build or refactor QML hosted inside the Omarchy 4 Quattro shell. Use for injected properties, Omarchy components, theme tokens, responsive layout, process execution, state, or multi-monitor behavior; not for standalone Quickshell applications.
---

# Omarchy QML Patterns

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

## Verification

Build the smallest state-complete surface first. Exercise loading, empty,
success, partial failure, authentication-required, and retry behavior with
fictional fixtures. Then run static validation, QML tests where available, and
a live-shell smoke test on Omarchy.
