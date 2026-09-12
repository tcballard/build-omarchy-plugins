---
name: omarchy-panel-overlay
description: Build or refactor Omarchy Quattro panel, overlay, or menu entry points. Use for summon/hide lifecycle, payloads, layer-shell windows, focus, dismissal, positioning, keyboard navigation, or multi-monitor presentation.
---

# Omarchy Panels, Overlays, and Menus

Match the surface to the interaction:

- `panel`: compact persistent or summoned floating content, often bar-attached;
- `overlay`: fullscreen modal or transient shell surface; and
- `menu`: summoned navigable action or selection surface.

Read [references/lifecycle-and-windows.md](references/lifecycle-and-windows.md)
before implementing a new entry point.

For a targeted fix, inspect the existing lifecycle and change the affected path;
do not add new windows or switch kinds merely to match an example.

## Required lifecycle

- Expose `open(payloadJson)` and `close()` on every panel, overlay, and menu
  entry point. Parse payload JSON defensively and default to `{}`.
- Track a truthful `opened` state. Opening twice should update or focus the
  active surface rather than duplicate hidden windows.
- Release temporary requests, timers, and exclusive keyboard focus on every
  close path, including Escape, outside click, completed action, and host hide.
- Use `WlrLayer.Overlay` and `ExclusionMode.Ignore` only for genuine overlays.
  Avoid stealing keyboard focus while not visible.
- Use one window per screen only when the interaction requires it. Decide
  explicitly whether an invocation belongs on the focused monitor or all
  monitors.

## Interaction quality

Provide keyboard navigation and a visible dismissal path for modal surfaces.
Keep pointer hit regions inside the intended card, prevent backdrop clicks from
passing through, and preserve reduced motion and theme tokens where supported.
Do not perform slow process or network work on the visible open path when a
service can preload it.

## Inputs and completion

Use the target checkout, selected kind and requested open/close interaction,
including any existing payload and monitor contract.

Leave the mapped surface implementing the requested behavior and identify
evidence for affected open, repeated-open and dismissal paths. Carry remaining
focus or monitor checks into testing; portable checks alone do not establish
live window behavior.
