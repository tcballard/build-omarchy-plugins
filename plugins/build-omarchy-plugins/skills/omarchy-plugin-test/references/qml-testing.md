# QML and state-machine testing

Use three complementary levels.

## Pure JavaScript

Move parsing, sorting, filtering, version comparison, and setup-plan selection
into imported `.js` modules. Exercise them with Node's built-in test runner when
they do not depend on QML objects.

## QtTest

Use `qmltestrunner` for service state transitions and component lifecycle. In
CI, install Qt 6 QML/Quick/Test modules and provide narrow Quickshell stubs only
for the exact types exercised. Stubs should expose process completion manually;
they must never invoke real commands.

Representative runner environment:

```bash
QT_QPA_PLATFORM=offscreen \
QT_QUICK_BACKEND=software \
qmltestrunner -input tests/qml -import tests/qml/imports -o -,txt
```

The maintained
[Basecamp Omarchy plugin](https://github.com/basecamp/omarchy-basecamp-plugin)
is a useful current example of fixture CLIs, Quickshell process stubs, Node
tests, and QtTest service transitions.

## Live shell

QtTest cannot prove layer-shell geometry, host injection, actual Omarchy imports,
multi-monitor anchoring, bar placement, or IPC registration. Exercise those on
the target Omarchy revision after portable tests pass.
