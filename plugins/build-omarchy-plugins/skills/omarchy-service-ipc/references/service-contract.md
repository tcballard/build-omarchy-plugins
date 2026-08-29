# Hosted service and IPC contract

## Service entry point

```qml
import QtQuick
import Quickshell.Io

Item {
  id: root
  property var shell: null
  property var manifest: null
  property bool refreshing: false
  property string lastError: ""

  function refresh() {
    if (refreshing) return
    refreshing = true
    lastError = ""
    statusProcess.running = true
  }

  IpcHandler {
    target: "io.github.owner.example"
    function refresh(): void { root.refresh() }
    function status(): string {
      return JSON.stringify({ refreshing: root.refreshing,
        error: root.lastError !== "" })
    }
  }
}
```

The service is mounted once while its third-party plugin is enabled. A visual
entry point may be created many times, so resolve this singleton rather than
starting duplicate pollers.

## Stable IPC

- Use the exact plugin ID as the target unless compatibility requires a stable
  older name.
- Keep method names domain-oriented and few in number.
- Return `ok`, a bounded scalar, or a documented small JSON object.
- Never return access tokens, full environment variables, raw auth responses,
  or unbounded third-party payloads.
- Changing an existing method's meaning or result shape is an API change even
  when QML callers live in the same repository.

The host `shell` target owns discovery and lifecycle methods such as `summon`,
`hide`, `toggle`, `rescanPlugins`, `setPluginEnabled`, and `listPlugins`.
