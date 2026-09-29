# Bar widget contract

Minimal hosted shape:

```qml
import QtQuick
import qs.Commons
import qs.Ui

BarWidget {
  id: root
  moduleName: "io.github.owner.example"

  implicitWidth: button.implicitWidth
  implicitHeight: button.implicitHeight

  WidgetButton {
    id: button
    anchors.fill: parent
    bar: root.bar
    text: root.vertical ? "" : "Example"
    tooltipText: "Example status"
    onPressed: function(mouseButton) { root.activate(mouseButton) }
  }
}
```

## Popout contract

When the widget owns a private panel, expose the panel's state and lifecycle on
the root so the bar can coordinate popouts:

```qml
readonly property bool opened: panelLoader.item
  ? panelLoader.item.opened === true : false

function open() { if (panelLoader.item) panelLoader.item.open() }
function close() { if (panelLoader.item) panelLoader.item.close() }
```

Inject `bar`, `settings`, anchor item, and host widget into the loaded panel
whenever the relevant source property changes. Use the current first-party
clock or a maintained community plugin as the local pattern rather than copying
an old Waybar module.

## Multi-monitor service lookup

A combined `service` + `bar-widget` plugin should resolve the singleton hosted
by the shell and provide an inert local fallback until it appears. Keep a
binding to the service map or registry revision so the lookup recomputes after
service creation.

## Pointer behavior

Use the `WidgetButton` press callback's button argument. Make left-click the
primary action, reserve right/middle click for predictable secondary behavior,
and document it in the tooltip and README.

## Service-backed widgets under replacement bars

Quattro's [reviewed 29 September contract](https://github.com/omacom/omarchy/blob/e332dc975d5f635294c497ebb54feb98dc3d89eb/docs/omarchy-shell.md)
gives widgets hosted by a third-party replacement bar a service-less entry
facade. Full own-service integration is retained under the trusted built-in bar.
Rendering a widget under a replacement bar does not prove its data integration
works. Handle an unavailable service explicitly, avoid duplicate pollers, and
record which bar was tested. Do not bypass the facade through scene traversal.
