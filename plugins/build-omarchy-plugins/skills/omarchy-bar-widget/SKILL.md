---
name: omarchy-bar-widget
description: Build or refactor an Omarchy Quattro bar-widget implementation, including settings, orientation, popouts, instances and shared services. Use for widget QML or behaviour; global bar styling belongs to theme skills, and replacing the entire bar is outside this skill.
---

# Build an Omarchy bar widget

Inspect the existing manifest, widget and installed host. Use `BarWidget` and `WidgetButton`; preserve settings and behavior outside the requested change.

- Map `entryPoints.barWidget` to the real file and set `moduleName` to the plugin ID.
- Use `root.bar`, `root.settings` and `setting(key, fallback)`. Store ordinary options inline in `shell.json`, not in a nested `config` or separate settings file.
- Support horizontal and vertical bars. Keep selection, hover and open state per instance; share polling and cross-monitor data through a service only when needed.
- For a popout, expose `opened`, `open()` and `close()` and preserve anchor/settings injection. Check placement from the tray drawer as well as bar edges.
- Set `allowMultiple` only when independent concurrent instances make sense.
- Current Quattro accepts `left`, `centerBegin`, `center`, `centerEnd`, `right`, `tray` as `defaultSection`. Automatic placement maps `center` to `centerEnd`; use the side sections to sit beside the clock without shifting it. Check older hosts before relying on new sections.

Read [widget contract](references/widget-contract.md) for QML shape and [settings schema](references/settings-schema.md) when adding options. Use QML patterns for theme, translations and shared implementation; change global theme tokens through the theme workflow.

Verify affected pointer, keyboard, orientation, placement and failure paths. Report which live-host checks were observed and which remain unrun; portable validation alone does not prove popup geometry.
