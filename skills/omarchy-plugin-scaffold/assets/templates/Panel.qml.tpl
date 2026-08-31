import QtQuick
import Quickshell
import Quickshell.Wayland
import qs.Commons
import qs.Ui

Item {
  id: root
  property string omarchyPath: ""
  property var shell: null
  property var manifest: null
  property bool opened: false
  property string detail: "Ready"

  function open(payloadJson) {
    var payload = ({})
    var encoded = String(payloadJson || "{}")
    if (encoded.length > 16384) encoded = "{}"
    try { payload = JSON.parse(encoded) || ({}) }
    catch (error) { payload = ({}) }
    root.detail = String(payload.detail || "Ready").slice(0, 256)
    root.opened = true
  }

  function close() { root.opened = false }

  PanelWindow {
    visible: root.opened
    anchors { top: true; right: true }
    margins { top: Style.gapsOut; right: Style.gapsOut }
    implicitWidth: Style.space(360)
    implicitHeight: Style.space(180)
    color: "transparent"
    WlrLayershell.namespace: "{{NAMESPACE_QML}}"
    WlrLayershell.layer: WlrLayer.Top
    WlrLayershell.keyboardFocus: root.opened ? WlrKeyboardFocus.OnDemand : WlrKeyboardFocus.None
    exclusionMode: ExclusionMode.Ignore

    BorderSurface {
      anchors.fill: parent
      color: Color.popups.background
      radius: Style.cornerRadius
      borderSpec: Border.surfaceSpec("popups", "border", Color.popups.border, 1)
      padding: Style.spacing.panelPadding

      Column {
        spacing: Style.spacing.md
        Text { text: "{{PLUGIN_NAME_QML}}"; color: Color.popups.text; font.pixelSize: Style.font.title }
        Text { text: root.detail; color: Color.popups.text; font.pixelSize: Style.font.body }
      }
    }
  }
}
