import QtQuick
import Quickshell
import Quickshell.Wayland
import qs.Commons

Item {
  id: root
  property string omarchyPath: ""
  property var shell: null
  property var manifest: null
  property var pluginRegistry: null
  property var barWidgetRegistry: null
  property var barConfig: ({})

  Variants {
    model: Quickshell.screens

    delegate: Component {
      PanelWindow {
        required property var modelData
        screen: modelData
        anchors { top: true; left: true; right: true }
        implicitHeight: Style.bar.sizeHorizontal
        color: Color.bar.background
        WlrLayershell.namespace: "{{NAMESPACE_QML}}"
        WlrLayershell.layer: WlrLayer.Top
        WlrLayershell.keyboardFocus: WlrKeyboardFocus.None
        exclusionMode: ExclusionMode.Auto

        Text {
          anchors.centerIn: parent
          text: "{{PLUGIN_NAME_QML}}"
          color: Color.bar.text
          font.pixelSize: Style.font.body
        }
      }
    }
  }
}
