---
name: omarchy-qml-patterns
description: Apply shared hosted-QML patterns to Omarchy 4 Quattro plugin code, including theme tokens, layout, process execution and local state. Use alongside the relevant bar, panel or service skill for implementation; use theme skills for shared palette or shell.toml styling.
---

# Write hosted Omarchy QML

Inspect the installed host and closest working component. Use its contract rather than assuming the pinned examples fit every version.

- Use hosted `Item`/UI entry points, never a second `ShellRoot` or Quickshell process. Give late-injected host properties safe defaults rather than `required` declarations.
- Use `qs.Ui` components and semantic tokens. Import `qs.Commons as Commons` and qualify `Commons.Color.*`: Qt 6.12 adds a conflicting `Color` type. Keep the unqualified import too when using `Style`, `Util` or `Border`.
- Keep hover/selection/open state per visual instance; share polling and remote state through a service where needed.
- Set `Text.PlainText` for external text at every sink, including tooltips and nested delegates. Bound external data before displaying or saving it.
- Launch commands with argument arrays. If a shell is necessary, quote external values with `Util.shellQuote`. Keep secrets out of display properties, logs and environment dumps.
- Keep repeated network/process/storage policy in a narrow adapter with explicit errors and tests for its actual production path.

Load only relevant references: [host injection and facades](references/hosted-qml.md), [theme/orientation/monitors](references/theme-and-layout.md), [plugin translations](references/translations.md), [process and state](references/process-and-state.md), or [external-data review boundaries](references/reviewer-boundaries.md).

For a theme problem, fix the consumer or shared theme source that owns it. Verify affected behavior with fixtures and required repository checks; report Qt imports and live lifecycle as unrun unless observed on the target host.
