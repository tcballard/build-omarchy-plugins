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

## Scoped host interfaces

Reviewed against Quattro commit `cce8b1c971df64a7610b818ff8819e4bea04584a`
(17 October 2026). Check the target host before assuming these APIs exist on
an older installation.

The injected names above do not grant third-party code the trusted host objects.
Ordinary plugins receive capability-scoped facades for their own service and
lifecycle. Configuration, registry and scalar bar snapshots are detached:
mutating them does not update host state. Use the supported scoped operations
instead of treating these values as writable shell configuration.

Built-in clones have narrow source-specific compatibility; menus receive an
application-library facade. Full replacement bars receive detached bar config
and widget-catalog snapshots, limited non-authentication service proxies and
lifecycle control over configured non-authentication UI plugins. Do not infer
arbitrary cross-plugin service access from built-in examples. Authentication
capabilities come from trusted first-party manifests; declaring them in a
third-party manifest does not grant them.

These facades are API boundaries, not a QML sandbox. Visual plugins share the
host scene and can traverse ordinary parent objects; plugins retain user-level
file and process access. Do not use scene traversal to work around the scoped
API, or keep sensitive state in the scene on the assumption it is isolated.

## Imports

Use the shell-hosted module namespace:

```qml
import QtQuick
import Quickshell
import Quickshell.Io
import qs.Commons
import qs.Commons as Commons
import qs.Ui
```

Use `Commons.Color.*` for palette references on Qt 6.12; its QtQuick `Color` type shadows unqualified access. Keep the unqualified import for `Style`, `Util` and `Border`.

`qs.Commons` contains theme and utility singletons. `qs.Ui` contains Omarchy
components such as `BarWidget`, `WidgetButton`, `Panel`, `BorderSurface`, and
keyboard/pointer helpers. These imports are available in the hosted shell and
are not evidence that the entry point can run as a standalone Quickshell app.

## Local JavaScript

Put pure parsing, sorting, and transition logic in imported `.js` modules when
that makes it testable without a live shell. Keep QML responsible for bindings,
lifecycle, and view composition.

Authoritative contract:
[docs/omarchy-shell.md](https://github.com/omacom/omarchy/blob/cce8b1c971df64a7610b818ff8819e4bea04584a/docs/omarchy-shell.md).
