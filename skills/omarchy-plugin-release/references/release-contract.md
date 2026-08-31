# Release contract

## Required repository surface

- one root `manifest.json` and matching entry points;
- root README with requirements, install, use, update, and removal;
- root license and third-party dependency/license notes;
- current root preview for visual plugins;
- automated portable tests and current live-shell evidence;
- public issue/support route and security reporting instructions.

## Pre-tag sequence

1. Select the intended source boundary and update the manifest version.
2. Update release notes and compatibility claims.
3. Run static, unit, fixture, live-shell, install, update, and removal evidence.
4. Merge release-only changes and require green CI.
5. Record the final full SHA and confirm the tree is clean.
6. Create an immutable annotated tag at that SHA.
7. Publish release notes that describe only the tested boundary.

Before publication, run the preflight with `--tag`. Run it again against the
downloaded draft assets with `--tag --release-dir`; never validate only the
local upload directory. For an already-published historical tag, use
`--published` so the commit must remain reachable from the current remote
default-branch history but is not incorrectly required to equal its HEAD.

Do not move a published tag or retarget marketplace evidence to a different
commit. If the boundary changes, produce a new version and rerun the relevant
evidence.

## Compatibility statement

State the tested Omarchy version or full source SHA, plugin SHA, hardware/display
scope, and anything not tested. Quattro's plugin contract is evolving; avoid
unbounded claims such as “works on all Omarchy versions.”

## Security language

Marketplace baseline and local lint results are deterministic limited scans.
Describe their outcome as evidence for an exact commit and retain the required
“not a security audit” boundary.
