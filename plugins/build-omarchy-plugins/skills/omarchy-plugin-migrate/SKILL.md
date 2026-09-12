---
name: omarchy-plugin-migrate
description: Migrate an older installer-style Omarchy integration or standalone Quickshell surface to Omarchy 4 Quattro. Use to separate machine setup, daemon, credentials, and shell UI while preserving safe install, upgrade, and removal behavior.
---

# Migrate Omarchy Plugins

Begin by classifying every existing responsibility. Read
[references/migration-map.md](references/migration-map.md).

Preserve the requested behavior and packaging boundaries. The two layers below
describe ownership, not a requirement for two repositories or a rewrite. Adapt
the current layout when it already separates them; prepare portable changes even
if privileged installation or live lifecycle verification must happen later.

## Two-layer model

- **Shell layer:** root `manifest.json`, hosted QML, bar/panel/overlay/menu,
  process-wide QML service, theme integration, and shell IPC.
- **Machine integration layer:** packages, compiled binaries, systemd units,
  privileged helpers, durable application data, and credentials.

Quattro's `omarchy plugin add` clones files, validates the manifest, and changes
enabled state. It does not run installation hooks or request `sudo`. Do not hide
machine integration in QML or claim that a shell plugin can provision it.

## Migration workflow

1. Inventory files written, packages installed, processes started, credentials
   accessed, config modified, and removal behavior in the current integration.
2. Move only the visual and shell-lifecycle surface into hosted QML. Replace a
   standalone `ShellRoot` with the appropriate entry-point `Item`.
3. Keep an independently supervised daemon or CLI independent. Let QML probe it
   and present explicit missing, unsupported, unauthenticated, offline, and
   ready states.
4. Use the external program's credential store. Do not migrate secrets into
   `shell.json` or QML persistence.
5. Replace implicit install hooks with documented explicit prerequisites or a
   separately reviewed package distribution path.
6. Prove upgrade and removal for both layers. Removing the shell plugin must not
   unexpectedly delete user data or unrelated packages.

For a Wayfinder-style integration, the router daemon remains the portable core;
the Quattro repository becomes a thin control surface and status client rather
than the router, supervisor, or credential store.

## Inputs and completion

Use the current integration, requested migration scope and existing
installation/removal contract. Preserve agreed repository and machine-layer
boundaries.

For planning, return the responsibility mapping and affected lifecycle checks.
For implementation, also leave the scoped patch and evidence for the migrated
surface, retained helper and removal boundaries. Pass the actual changed
checkout and unrun host checks into testing; do not regenerate an established
plugin.
