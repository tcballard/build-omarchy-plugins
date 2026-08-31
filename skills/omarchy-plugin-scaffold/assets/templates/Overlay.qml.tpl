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

  function open(payloadJson) {
    var encoded = String(payloadJson || "{}")
    if (encoded.length <= 16384) {
      try { JSON.parse(encoded) } catch (error) {}
    }
    root.opened = true
  }

  function close() { root.opened = false }

  PanelWindow {
    id: window
    visible: root.opened
    anchors { top: true; bottom: true; left: true; right: true }
    color: "transparent"
    WlrLayershell.namespace: "{{NAMESPACE_QML}}"
    WlrLayershell.layer: WlrLayer.Overlay
    WlrLayershell.keyboardFocus: root.opened ? WlrKeyboardFocus.Exclusive : WlrKeyboardFocus.None
    exclusionMode: ExclusionMode.Ignore

    Rectangle { anchors.fill: parent; color: Color.menu.scrim }
    MouseArea { anchors.fill: parent; onClicked: root.close() }

    BorderSurface {
      id: card
      width: Math.min(parent.width - Style.space(48), Style.space(520))
      height: Style.space(240)
      anchors.centerIn: parent
      color: Color.menu.background
      radius: Style.cornerRadius
      borderSpec: Border.surfaceSpec("menu", "border", Color.menu.border, 1)
      padding: Style.spacing.panelPadding

      MouseArea { anchors.fill: parent; onClicked: {} }
      Item {
        anchors.fill: parent
        focus: root.opened
        Keys.onEscapePressed: root.close()
        Text { anchors.centerIn: parent; text: "{{PLUGIN_NAME_QML}}"; color: Color.menu.text; font.pixelSize: Style.font.title }
      }
    }
  }
}
