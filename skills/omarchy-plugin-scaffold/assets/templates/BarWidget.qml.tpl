import QtQuick
import qs.Commons
import qs.Ui

BarWidget {
  id: root
  moduleName: "{{PLUGIN_ID_QML}}"

  property bool active: false
  readonly property string label: root.active ? "{{SHORT_LABEL_QML}} · on" : "{{SHORT_LABEL_QML}}"

  implicitWidth: button.implicitWidth
  implicitHeight: button.implicitHeight

  WidgetButton {
    id: button
    anchors.fill: parent
    bar: root.bar
    text: root.vertical ? (root.active ? "●" : "○") : root.label
    tooltipText: root.active ? "{{PLUGIN_NAME_QML}} is active" : "Activate {{PLUGIN_NAME_QML}}"

    onPressed: function(mouseButton) {
      if (mouseButton === Qt.LeftButton) root.active = !root.active
    }
  }
}
