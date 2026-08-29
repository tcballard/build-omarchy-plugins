# Theme, layout, and monitors

## Theme tokens

Prefer semantic roles to literal colors and dimensions:

- `Color.foreground`, `Color.background`, `Color.accent`, `Color.urgent`;
- surface roles such as `Color.bar.*`, `Color.popups.*`, and `Color.menu.*`;
- `Style.space(px)`, `Style.spacing.*`, `Style.font.*`, and `Style.cornerRadius`;
- `Border.surfaceSpec(...)` plus `BorderSurface` for theme-aware borders.

For a bar widget, prefer the active bar's exposed foreground, urgent, and font
values when they exist, with semantic tokens as fallback.

## Orientation

Bar widgets must react to `vertical`. Use a compact icon, stacked short glyphs,
or a reduced label. Do not rotate text that remains hard to scan. Size through
implicit width/height and the bar's icon slot rather than fixed screen pixels.

## Monitor model

Assume a visual widget may exist once per monitor. Never start one poll timer or
remote command chain per visual instance when a shared service can own it.
Keep selection, hover, local focus, and the currently open popout local to the
visual instance. Keep fetched records, authentication state, and refresh timing
in one service.

For fullscreen windows, use `Variants` over `Quickshell.screens` only when every
screen should receive a surface. Otherwise bind the invocation to the selected
or focused screen and document that choice.
