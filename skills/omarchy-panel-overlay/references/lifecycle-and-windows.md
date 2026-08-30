# Lifecycle and layer-shell windows

## Entry-point lifecycle

```qml
Item {
  id: root
  property bool opened: false

  function open(payloadJson) {
    var payload = ({})
    try { payload = JSON.parse(payloadJson || "{}") || ({}) }
    catch (error) { payload = ({}) }
    root.opened = true
  }

  function close() {
    root.opened = false
  }
}
```

The host routes `summon`, `hide`, and `toggle` through those methods. A panel,
overlay, or menu that claims a kind but omits its entry point or lifecycle will
install yet fail only at runtime; treat that as a preflight error.

## Overlay window

A fullscreen overlay commonly uses a `PanelWindow` anchored on all four edges:

```qml
PanelWindow {
  visible: root.opened
  anchors { top: true; bottom: true; left: true; right: true }
  color: "transparent"
  WlrLayershell.namespace: "io-github-owner-example"
  WlrLayershell.layer: WlrLayer.Overlay
  WlrLayershell.keyboardFocus: root.opened
    ? WlrKeyboardFocus.Exclusive : WlrKeyboardFocus.None
  exclusionMode: ExclusionMode.Ignore
}
```

Add a scrim, an outside-click dismissal target, a non-propagating card hit
region, and Escape handling. Do not keep exclusive keyboard focus when hidden.

## Panel base

For a bar-aligned popout, prefer the Omarchy `Panel` or `KeyboardPanel` base.
Pass the active bar and anchor item rather than recreating monitor and bar-edge
geometry.

## Payloads

Treat payload JSON as untrusted input. Validate fields, cap sizes, ignore unknown
keys, and never turn a payload string directly into a shell command or file
path. Define what a repeated `open()` does while already visible.
