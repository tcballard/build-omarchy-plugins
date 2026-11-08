# Motion and reduced motion

Reviewed 8 November 2026 against [Omarchy's motion contract](https://github.com/omacom/omarchy/blob/d9cc361cddf5d75dcb880de3c7fb8b5542ae6e39/agents/skills/motion.md).
Check the installed host's `qs.Commons.Style` and `qs.Ui` before adopting these
APIs. The bundle's broad Omarchy version range does not imply every older host
provides them; retain an instant presentation or declare a tested minimum.

Prefer `KeyboardPanel`, `PopupCard` and `Button` for their existing motion.
Do not stack a second open/close animation onto a host component. Custom motion
should explain placement, confirm input or prevent a distracting jump.

- Use `Style.duration(ms)` for every animation duration. It returns zero when
  animations are disabled through `omarchy toggle animations`.
- Stop looping animations with `running: active && !Style.reduceMotion`.
  Zero duration alone can leave an infinite loop spinning the CPU.
- Use `Style.easeOut` with `Easing.Bezier` for movement and entrances, or
  `Easing.OutCubic` for a plain fade. Avoid ease-in, bounce and overshoot;
  use linear easing only for constant motion.
- Keep transitions below 300 ms, with shorter exits: about 180 ms in and
  120 ms out. Start scale around 0.95–0.97, never zero.
- Frequently invoked transient pickers and OSDs should appear immediately.
  Panels where the user stays can use the host's normal motion for both keys
  and pointer input.

```qml
import QtQuick
import qs.Commons

NumberAnimation {
    target: spinner
    property: "rotation"
    from: 0
    to: 360
    duration: Style.duration(1000)
    loops: Animation.Infinite
    running: spinner.visible && !Style.reduceMotion
    easing.type: Easing.Linear
}
```

The spinner is constant motion, not a UI entrance; the sub-300 ms rule applies
to transitions. Ensure its parent supplies `spinner` and a useful static state.

Test animations enabled and disabled, including switching off during a loop,
rapid open/close/reopen, late content, keyboard dismissal and pointer hit areas.
Scaling a visual must not shrink its clickable boundary; sizing content to its
final height and clipping avoids reflow on every frame. Inspect motion frame by
frame on the target host. Source review and portable checks do not establish
smooth motion, focus behaviour or idle CPU usage.
