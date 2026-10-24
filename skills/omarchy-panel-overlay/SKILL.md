---
name: omarchy-panel-overlay
description: Build or refactor Omarchy Quattro panel, overlay, or menu entry points. Use for summon/hide lifecycle, payloads, layer-shell windows, focus, dismissal, positioning, keyboard navigation, or multi-monitor presentation.
---

# Build an Omarchy panel, overlay or menu

Preserve the existing surface, payload and monitor contract for a targeted change. Choose `panel` for compact floating content, `overlay` for fullscreen transient UI, or `menu` for navigable actions. Read [lifecycle and windows](references/lifecycle-and-windows.md) before adding an entry point.

- Expose `open(payloadJson)`, `close()` and truthful `opened` state. Parse payloads defensively; repeated open must update/focus rather than duplicate windows.
- Release temporary requests, timers and exclusive focus on Escape, outside click, action completion and host hide. Hidden windows must not steal focus.
- Use overlay layer/exclusion behavior only where required. Choose the focused monitor or all monitors deliberately.
- Provide keyboard navigation and visible dismissal. Keep hit regions within the card and prevent backdrop click-through.
- Use host UI components, semantic theme tokens and plugin-owned translations. Keep slow work off the visible open path when a service already owns it.

Verify changed open, repeated-open, dismissal, focus and monitor behavior. Record unobserved host checks without treating stubs as live window evidence.
