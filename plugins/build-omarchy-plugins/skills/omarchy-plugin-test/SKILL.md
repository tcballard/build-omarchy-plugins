---
name: omarchy-plugin-test
description: Validate and test an Omarchy 4 Quattro plugin. Use for manifest and path checks, advisory security linting, QML syntax or unit tests, fixture tests, live-shell smoke tests, and release evidence; not as a claim of security certification.
---

# Test Omarchy Plugins

Select evidence for the changed behavior and complete required repository
checks. A failed prerequisite blocks dependent checks, not independent useful
work. Resolve `<skill-dir>` to the directory containing this loaded `SKILL.md`.
Keep permanent tests consistent with the repository's conventions. Temporary
probes can establish evidence without becoming new maintained test suites.

## Portable static validation

```bash
python3 "<skill-dir>/scripts/validate_plugin.py" /absolute/path/to/plugin
python3 "<skill-dir>/scripts/validate_plugin.py" --json --security /absolute/path/to/plugin
```

The validator mirrors Omarchy's documented schema, entry-point, reserved-ID,
and symlink checks and adds quality and advisory security diagnostics. It never
executes plugin code. Its security report is not the marketplace's authoritative
baseline and is not proof that a plugin is safe.

## Test layers

These layers are a selection guide for development and the basis of release
evidence, not a mandatory sequence for every edit. For a manifest path repair,
reproduce the failure and validate the corrected mapping. For async or lifecycle
changes, exercise state transitions and cleanup. Pure copy edits do not need new
state-machine tests. Full release work uses the release skill when available.

1. Run the portable validator.
2. On Omarchy, run `omarchy plugin validate <path>` and reconcile any contract
   difference in favor of the installed Omarchy version.
3. Parse or lint QML with the exact Qt/Quickshell imports available to the
   target version.
4. Unit-test pure JavaScript and service state machines with fictional data.
5. Run live-shell smoke tests for discovery, enablement, visible behavior, IPC,
   reload, disablement, and restoration.
6. Exercise installation from a fresh Git checkout and removal without residue.

Read [references/test-matrix.md](references/test-matrix.md) for relevant states
and [references/qml-testing.md](references/qml-testing.md) when building QtTest
stubs or CI.

Record exact commands, target Omarchy revision, fixtures, exit status, and known
limitations. A screenshot is product evidence, not a substitute for state and
lifecycle assertions.

If Omarchy, Qt imports, or a display are unavailable, finish portable work and
identify the exact unrun host check. Do not invent passing evidence, weaken a
release gate, or repeatedly retry a missing environment. After selected checks
pass, repeat or broaden only for a new change, failure, or unresolved risk.

## Inputs and completion

Inspect the exact checkout and requested behavior, including staged, unstaged
and untracked files relevant to the change. Check inherited evidence against
that source before reusing it.

Report which behaviors passed, failed or remain unrun, with commands and
source identity: commit plus relevant working-tree changes, or a fixture
digest outside Git. Changes after a check invalidate evidence for affected
behavior. Carry these results into demo or release work when requested; a
clean HEAD diff does not establish that working-tree changes were tested.
