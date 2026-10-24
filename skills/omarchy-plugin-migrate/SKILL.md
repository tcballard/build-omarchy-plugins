---
name: omarchy-plugin-migrate
description: Migrate an older installer-style Omarchy integration or standalone Quickshell surface to Omarchy 4 Quattro. Use to separate machine setup, daemon, credentials, and shell UI while preserving safe install, upgrade, and removal behavior.
---

# Migrate an Omarchy integration

Read [migration map](references/migration-map.md). Inventory current writes, packages, processes, credentials, configuration and removal behavior before moving code. Preserve requested repository boundaries; separating responsibilities does not require two repositories or a rewrite.

- Move visual/shell lifecycle behavior into hosted QML with a root manifest and `Item` entry points; replace standalone `ShellRoot` surfaces.
- Keep CLI/daemon supervision, privileged helpers, packages, durable app data and credentials with their external owner. Probe missing, unsupported, unauthenticated, offline and ready states explicitly.
- `omarchy plugin add` clones/validates files and changes enabled state; it runs no installation hooks or sudo setup. Document explicit prerequisites or a separate package path.
- Use the external program's credential store. Do not move secrets into QML or `shell.json`.
- Verify upgrade/removal for each layer. Removing the shell plugin must not unexpectedly delete user data or unrelated packages.

For a plan, return responsibility mapping and lifecycle checks without implementation. For an authorized migration, patch the existing integration and test affected boundaries; report unavailable live/privileged checks while completing independent portable work.
