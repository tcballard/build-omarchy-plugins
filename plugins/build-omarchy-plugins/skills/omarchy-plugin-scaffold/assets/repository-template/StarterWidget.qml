import QtQuick
import qs.Commons
import qs.Ui

BarWidget {
  id: root
  moduleName: "io.github.tcballard.plugin_starter"
  property bool active: false
  implicitWidth: button.implicitWidth
  implicitHeight: button.implicitHeight

  WidgetButton {
    id: button
    anchors.fill: parent
    bar: root.bar
    text: root.active ? "●" : "○"
    tooltipText: root.active ? "Starter is active" : "Activate starter"
    onPressed: function(mouseButton) {
      if (mouseButton === Qt.LeftButton) root.active = !root.active
    }
  }
}
