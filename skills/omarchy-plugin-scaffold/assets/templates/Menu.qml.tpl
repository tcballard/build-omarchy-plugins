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
  property int selectedIndex: 0
  property var options: ["First action", "Second action", "Close"]

  function open(payloadJson) {
    var payload = ({})
    try { payload = JSON.parse(payloadJson || "{}") || ({}) }
    catch (error) { payload = ({}) }
    if (Array.isArray(payload.options) && payload.options.length) root.options = payload.options.slice(0, 20)
    root.selectedIndex = 0
    root.opened = true
  }

  function close() { root.opened = false }

  PanelWindow {
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
      width: Math.min(parent.width - Style.space(48), Style.space(420))
      height: Math.min(parent.height - Style.space(48), list.contentHeight + Style.space(80))
      anchors.centerIn: parent
      color: Color.menu.background
      radius: Style.cornerRadius
      borderSpec: Border.surfaceSpec("menu", "border", Color.menu.border, 1)
      padding: Style.spacing.panelPadding

      MouseArea { anchors.fill: parent; onClicked: {} }
      ListView {
        id: list
        anchors.fill: parent
        model: root.options
        currentIndex: root.selectedIndex
        focus: root.opened
        Keys.onEscapePressed: root.close()
        Keys.onReturnPressed: if (currentIndex === count - 1) root.close()
        delegate: Text {
          required property string modelData
          width: list.width
          height: Style.space(42)
          verticalAlignment: Text.AlignVCenter
          text: modelData
          color: index === list.currentIndex ? Color.menu.selectedText : Color.menu.text
        }
      }
    }
  }
}
