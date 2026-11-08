# Host contract refresh, 8 November 2026

Reviewed Quattro at `d9cc361cddf5d75dcb880de3c7fb8b5542ae6e39`
against the previous `cce8b1c971df64a7610b818ff8819e4bea04584a` pin.
Reviewed marketplace contract files at
`bc49ed6ee941da0cab2796da4a0e0e878b5c5642` against
`3e38844761e5a4045243fd1c9ca272e4c6b61c12`.
The ledger records exact source paths and SHA-256 digests.

## Changes applied

- Shell/plugin guidance adds shared motion tokens and host component motion.
  The motion reference includes reduced-motion loop stopping, interruption and
  late-content acceptance, with installed-host availability made explicit.
- Shell development guidance now describes the supervised launcher. Debugging
  uses bounded journal logs and the supported restart path, preserving lock
  protection and distinguishing plugin watching from Quickshell file watching.
- PluginRegistry fixes multi-kind enablement/clone revert and ignores Python
  bytecode writes. Debugging covers these symptoms and requires actual host
  version checks. No plugin-side workaround for a host bug is generated.
- The Agents panel changed extensively, but its Plugin starter still requests
  the built-in guide through `omarchy-agent-prompt`; bundle loading is unchanged.
  Indicators multiselect settings and the six pinned marketplace files are
  byte-identical to the previous pins. No new submission requirements are inferred.
- Workbench is no longer recommended or generated, following the owner's
  deprecation direction. Both generators retain standalone checks. The full
  starter applies integration version 3 to generated files, blueprint, receipt
  and checker; its immutable upstream snapshot and lock remain intact.

## Evidence boundary

The reviewed Omarchy and marketplace bytes were read from exact Git commits and
checked against the ledger digests; vendored copies match. The Agent Skills and
Codex discovery pins are unchanged and are outside this host refresh. This is
not a review of every marketplace implementation file or every upstream API.

Portable validation covers both generators, generated-project checks, clone and
reinitialization, adapter parity, packaging and existing regressions. The Qt
rendering fixture is optional. Live Omarchy motion, CPU usage, lock recovery,
notification recovery and multi-kind enable/revert remain unrun here. Newer
Quattro APIs do not retroactively establish compatibility on older installations.
Versions remain at the published v0.10.0 baseline; this PR prepares source changes,
not a tagged release or an update to separately installed personal skills.

## Executed checks

`./scripts/test` passed: 90 Python cases (89 passed; optional PySide6 fixture
skipped), six Node cases, both adapter validations and deterministic packaging.
An independent text-only skill exercise identified the reduced-motion loop,
keepLoaded retention and multi-kind enablement diagnosis, checked host-version
uncertainty and proposed no unauthorized restart. This does not close the live
acceptance scenarios above.
