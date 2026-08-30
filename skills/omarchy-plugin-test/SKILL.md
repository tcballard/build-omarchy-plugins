---
name: omarchy-plugin-test
description: Validate and test an Omarchy 4 Quattro plugin. Use for manifest and path checks, advisory security linting, QML syntax or unit tests, fixture tests, live-shell smoke tests, and release evidence; not as a claim of security certification.
---

# Test Omarchy Plugins

Use layered evidence and stop at the first failed prerequisite.

## Portable static validation

```bash
python3 scripts/validate_plugin.py /absolute/path/to/plugin
python3 scripts/validate_plugin.py --json --security /absolute/path/to/plugin
```

The validator mirrors Omarchy's documented schema, entry-point, reserved-ID,
and symlink checks and adds quality and advisory security diagnostics. It never
executes plugin code. Its security report is not the marketplace's authoritative
baseline and is not proof that a plugin is safe.

## Test layers

1. Run the portable validator.
2. On Omarchy, run `omarchy plugin validate <path>` and reconcile any contract
   difference in favor of the installed Omarchy version.
3. Parse or lint QML with the exact Qt/Quickshell imports available to the
   target version.
4. Unit-test pure JavaScript and service state machines with fictional data.
5. Run live-shell smoke tests for discovery, enablement, visible behavior, IPC,
   reload, disablement, and restoration.
6. Exercise installation from a fresh Git checkout and removal without residue.

Read [references/test-matrix.md](references/test-matrix.md) for required states
and [references/qml-testing.md](references/qml-testing.md) when building QtTest
stubs or CI.

Record exact commands, target Omarchy revision, fixtures, exit status, and known
limitations. A screenshot is product evidence, not a substitute for state and
lifecycle assertions.
