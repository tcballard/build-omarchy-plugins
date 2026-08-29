import QtQuick
import Quickshell.Io

Item {
  id: root
  property string omarchyPath: ""
  property var shell: null
  property var manifest: null
  property int refreshCount: 0
  property date lastUpdated: new Date(0)

  function refresh() {
    root.refreshCount += 1
    root.lastUpdated = new Date()
  }

  IpcHandler {
    target: "{{PLUGIN_ID_QML}}"
    function refresh(): void { root.refresh() }
    function status(): string {
      return JSON.stringify({
        refreshCount: root.refreshCount,
        lastUpdated: root.lastUpdated.toISOString()
      })
    }
  }

  Timer {
    interval: 300000
    repeat: true
    running: true
    triggeredOnStart: true
    onTriggered: root.refresh()
  }
}
