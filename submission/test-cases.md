# Routing test cases

The first five cases should activate one or more bundled skills. The last five
should not activate the plugin because they are unrelated or ask only for
general operating-system use.

## Positive cases

### P1 — New bar widget

- Prompt: `Create an Omarchy 4 bar widget that shows my current focus session and opens a detail panel when clicked.`
- Expected routes: `omarchy-plugin-design`, `omarchy-plugin-scaffold`, `omarchy-bar-widget`.
- Expected behavior: chooses `bar-widget` plus panel/service entry points, generates a root manifest and QML, uses host-injected properties, and runs structural validation.
- Expected result shape: a repository tree, concise architecture note, validation result, and remaining live-shell check.
- Fixture data: an empty writable directory; use fictional 25-minute focus sessions and no external service.

### P2 — Manifest failure

- Prompt: `My Omarchy plugin appears in the plugin list but fails validation after I renamed Panel.qml. Diagnose it.`
- Expected routes: `omarchy-plugin-debug`, `omarchy-plugin-test`.
- Expected behavior: inspects `manifest.json` and repository-relative entry points before changing code; identifies a missing or mismatched panel path and verifies the correction.
- Expected result shape: observed evidence, root cause, minimal patch, and before/after validator output.
- Fixture data: generate a panel scaffold, rename `Panel.qml` to `Details.qml`, and leave `entryPoints.panel` unchanged.

### P3 — Shared service and IPC

- Prompt: `Add one process-wide weather service to this Quattro plugin and expose a refresh action over IPC without logging the API token.`
- Expected routes: `omarchy-service-ipc`, `omarchy-qml-patterns`, `omarchy-plugin-test`.
- Expected behavior: separates secret handling from observable state, avoids per-monitor duplicate workers, defines a stable command contract, and adds failure-path tests.
- Expected result shape: service QML, IPC contract table, redacted test evidence, and explicit host-dependent checks.
- Fixture data: a generated service scaffold and fictional environment variable `WEATHER_DEMO_TOKEN`; no credential or network call is required.

### P4 — Legacy migration

- Prompt: `Migrate my old Omarchy installer plugin: keep its required systemd helper, but move its visible status and controls into the Quattro shell.`
- Expected routes: `omarchy-plugin-migrate`, `omarchy-plugin-design`.
- Expected behavior: does not claim Quattro supports install hooks; splits machine integration from shell UI and documents independent install, rollback, and trust boundaries.
- Expected result shape: responsibility map, two-repository target layout, staged migration plan, and independent rollback steps.
- Fixture data: describe a legacy `install.sh`, `demo-helper.service`, and a status script that prints `ready`; no privileged operation should run.

### P5 — Release and community submission

- Prompt: `Preflight this Omarchy plugin release and prepare the exact community marketplace submission, but do not publish anything yet.`
- Expected routes: `omarchy-plugin-release`, `omarchy-plugin-publish`, `omarchy-plugin-demo`.
- Expected behavior: verifies clean/reproducible evidence, prepares metadata in the marketplace template's order, and holds external publication for owner approval.
- Expected result shape: pass/fail preflight, exact issue title/body, preview evidence, and an explicit `submitted: false` state.
- Fixture data: a committed generated bar-widget repository with an `origin` URL, root README, MIT license, and fictional preview.

## Negative cases

### N1 — Ordinary Arch package install

- Prompt: `How do I install PostgreSQL on Arch Linux?`
- Expected fallback: answer with ordinary Arch guidance; do not scaffold or inspect an Omarchy manifest.
- Why not: package installation is unrelated to authoring an Omarchy shell plugin.

### N2 — GNOME extension

- Prompt: `Write a GNOME Shell extension that changes the overview animation.`
- Expected fallback: use a GNOME-specific development workflow.
- Why not: GNOME Shell extensions do not use Omarchy's manifest or hosted QML contract.

### N3 — User configuration

- Prompt: `Help me change the wallpaper in Omarchy.`
- Expected fallback: provide Omarchy usage guidance; activate a build skill only if the user later requests a reusable Quattro surface.
- Why not: changing one setting is not plugin development.

### N4 — Generic QML application

- Prompt: `Build a standalone Qt Quick calculator for Windows.`
- Expected fallback: use a general Qt/QML application workflow.
- Why not: a standalone Windows app does not run inside `omarchy-shell`.

### N5 — Plugin installation only

- Prompt: `Enable an existing Omarchy plugin I already downloaded.`
- Expected fallback: answer as an Omarchy usage/support request without scaffolding or publication workflows.
- Why not: enabling reviewed code is an end-user operation, not authoring, testing, migrating, or publishing a plugin.
