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

## Service access and retained instances

On the reviewed Quattro host, ordinary third-party entry points may resolve
only their own service through the injected facade. The trusted built-in bar
preserves that integration for service-backed third-party widgets. A replacement
bar gives hosted widgets a service-less entry facade; its ability to render a
widget is not evidence that the widget can reach its service. Handle unavailable
service state explicitly and test the selected bar. Do not retrieve another
plugin's service or traverse scene objects to bypass this boundary.

A manifest with `keepLoaded: true` retains its service across plugin hot-reload.
The retained instance is not replaced: service code changes take effect on a
shell restart. Test edit reload and restart separately; do not start another
poller to compensate for a retained instance. Arrange any restart with the user,
particularly when session-lock services are involved.

Source: [Quattro shell contract, reviewed 29 September 2026](https://github.com/omacom/omarchy/blob/e332dc975d5f635294c497ebb54feb98dc3d89eb/docs/omarchy-shell.md).
These restrictions are host-version dependent; record the actual tested commit.

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
