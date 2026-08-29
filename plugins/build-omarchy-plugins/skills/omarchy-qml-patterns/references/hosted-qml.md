# Hosted QML contract

Omarchy runs one long-lived Quickshell process. A plugin entry point is loaded
inside that process and must not create another `ShellRoot`.

## Injected properties

The host conditionally assigns properties when they exist:

```qml
Item {
  property string omarchyPath: ""
  property var shell: null
  property var manifest: null
  property var pluginRegistry: null
  property var barWidgetRegistry: null
}
```

Use safe initial values in third-party components. Dynamic `Loader.source`
instantiates a component before the host's later assignment, so `required`
injected properties can make a valid-looking component fail at construction.

Bar widgets normally inherit `bar`, `settings`, `vertical`, `setting()`, and
related behavior from `BarWidget`. Full bar replacements also receive
`barConfig`.

## Imports

Use the shell-hosted module namespace:

```qml
import QtQuick
import Quickshell
import Quickshell.Io
import qs.Commons
import qs.Ui
```

`qs.Commons` contains theme and utility singletons. `qs.Ui` contains Omarchy
components such as `BarWidget`, `WidgetButton`, `Panel`, `BorderSurface`, and
keyboard/pointer helpers. These imports are available in the hosted shell and
are not evidence that the entry point can run as a standalone Quickshell app.

## Local JavaScript

Put pure parsing, sorting, and transition logic in imported `.js` modules when
that makes it testable without a live shell. Keep QML responsible for bindings,
lifecycle, and view composition.

Authoritative contract:
[docs/omarchy-shell.md](https://github.com/basecamp/omarchy/blob/quattro/docs/omarchy-shell.md).
