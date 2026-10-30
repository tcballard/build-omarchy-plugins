---
name: omarchy-plugin-test
description: Validate changed Omarchy 4 Quattro plugin behavior with manifest, path, advisory security, QML, fixture and live-shell checks. Use for development regression evidence; use release for version and asset readiness or publish for marketplace responses. Static checks do not certify security.
---

# Test an Omarchy plugin

Inspect the actual changed checkout, including relevant untracked files. Select checks for the changed behavior and complete required repository checks; a tooltip edit does not need a new state-machine suite.

Resolve `<skill-dir>` to this skill's directory:

```bash
python3 "<skill-dir>/scripts/validate_plugin.py" /absolute/path/to/plugin
python3 "<skill-dir>/scripts/validate_plugin.py" --json --security /absolute/path/to/plugin
```

The portable checker does not execute plugin code. Schema checks and advisory security diagnostics do not establish runtime correctness or certify safety. Reconcile differences with the installed `omarchy plugin validate <path>` and current marketplace contract.

Verify relevant layers: manifest/path; exact Qt/Quickshell imports; fixture/unit behavior; live discovery, enablement, visible interaction, IPC, reload and disablement; installation/update/removal for lifecycle changes. Include tray popout placement, language switching/RTL and Qt 6.12 palette lookup when affected.

For persistent-state fixes, use the [upgrade fixtures](references/upgrade-fixtures.md) against the production migration. For external text, use the optional [plain-text check](references/plain-text.md).

Load [test matrix](references/test-matrix.md) or [QML testing](references/qml-testing.md) as needed. For optional capability policies, baseline tools and disposable desktops, read [validation options](references/validation-options.md). For marketplace findings, read [review response](references/review-response.md). Companion tools are optional; do not install them just to satisfy a workflow.

Record source identity (commit plus relevant working changes, or fixture digest), commands, exit status, observed behavior and unrun checks. Missing Omarchy/display access leaves host checks unrun while portable work continues. Invalidate affected evidence after edits; do not repeatedly retry missing prerequisites or broaden testing after passing checks without a concrete reason.
