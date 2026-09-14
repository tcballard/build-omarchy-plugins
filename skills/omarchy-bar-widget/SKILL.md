---
name: omarchy-bar-widget
description: Build or refactor an Omarchy Quattro bar-widget implementation, including settings, orientation, popouts, instances and shared services. Use for widget QML or behaviour; global bar styling belongs to theme skills, and replacing the entire bar is outside this skill.
---

# Omarchy Bar Widget

Inspect the existing widget and requested effect before editing. For global bar colours, spacing or theme-owned surface tokens, use omarchy-theme-shell when available. For one widget that ignores the active theme, fix its QML token consumption with omarchy-qml-patterns. A mixed styling and behaviour request may need both workflows; avoid changing global theme values to mask a widget defect.

Use Omarchy's `BarWidget` and `WidgetButton` primitives so placement,
orientation, theme, tooltips, and popout behavior remain coherent with the
active bar.

For an existing widget, preserve its API and settings unless the request changes
them. Apply the relevant contract below; a label or tooltip correction does not
require redesigning state ownership or adding a service.

## Workflow

1. Confirm `manifest.json` declares `bar-widget` and maps
   `entryPoints.barWidget` to the real QML file.
2. Set `moduleName` to the exact plugin ID. Use `root.bar` for bar-owned actions
   and `root.settings` / `setting(key, fallback)` for inline configuration.
3. Design both horizontal and vertical forms. A vertical bar should not merely
   rotate a long horizontal label.
4. Keep one visual instance's transient state local. Put shared polling,
   authentication probes, and cross-monitor data in a `service` entry point.
5. If the widget opens a panel, expose `opened`, `open()`, and `close()` on the
   widget root and keep its anchor and settings injection synchronized.
6. Validate pointer, keyboard, tooltip, empty, error, and retry behavior.

Read [references/widget-contract.md](references/widget-contract.md) for the QML
shape. Read [references/settings-schema.md](references/settings-schema.md) when
adding `barWidget.defaults` or `barWidget.schema`.

## Manifest decisions

- `allowMultiple` is `false` unless independent concurrent instances are
  genuinely useful and state is selector-safe.
- `defaultSection` is one of `left`, `center`, or `right` and is only a default;
  users remain free to move the widget.
- Put user settings directly on the `shell.json` entry. Do not invent a nested
  `config` object or a parallel settings file for ordinary widget options.

## Inputs and completion

Use the target checkout, manifest and requested interaction, retaining agreed
settings and state ownership.

Leave the requested widget behavior implemented in the mapped entry point,
with evidence for the affected orientation, settings or interaction paths.
Pass the changed files and any unobserved host behavior to testing; broader
release or demo work follows only when requested.
