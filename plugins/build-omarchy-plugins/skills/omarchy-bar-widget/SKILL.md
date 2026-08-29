---
name: omarchy-bar-widget
description: Build or refactor an Omarchy Quattro bar widget, including settings, vertical layouts, optional popout panels, multiple instances, and shared services. Use when `kinds` includes `bar-widget`; not for replacing the entire bar.
---

# Omarchy Bar Widget

Use Omarchy's `BarWidget` and `WidgetButton` primitives so placement,
orientation, theme, tooltips, and popout behavior remain coherent with the
active bar.

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
