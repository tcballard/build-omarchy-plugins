# Reviewer notes

## Product boundary

Build Omarchy Plugins is a skills-only developer tool. It helps a coding agent
work on repositories that target the Omarchy 4 Quattro shell plugin contract.
It is not an Omarchy runtime plugin and it does not install software on the
reviewer's machine.

## Architecture

- Twelve narrowly routed skills live below `skills/`.
- Six executable Python utilities use only the Python standard library.
- Templates generate each current Omarchy kind: `bar-widget`, `panel`,
  `overlay`, `menu`, `service`, and `bar`.
- The structural validator runs without Omarchy, Quickshell, network access, or
  elevated privileges.
- Live-shell verification is explicitly conditional on the host having the
  relevant Omarchy tooling.

## External actions and approvals

- Repository generation writes only to the destination selected by the user and
  refuses a non-empty destination.
- Diagnostic tools are read-only.
- Marketplace preparation emits a draft; it never opens an issue by itself.
- Publishing, pushing, enabling an Omarchy plugin, installing packages, and
  changing system configuration remain owner-controlled actions.
- The skills warn that third-party Omarchy QML runs unsandboxed inside the shell
  process and that static analysis cannot establish trust.

## Data and privacy

The plugin has no service, account, analytics, network integration, MCP server,
or app connector. It processes repository content supplied in the conversation
or workspace. Generated files remain in that workspace unless the user directs
an external action. See `PRIVACY.md` for the published policy.

## Reproduction

Use Python 3.11 or newer and run `./scripts/test`. The suite validates all skill
routes, generates all six current plugin kinds, rejects traversal and symlinks,
checks a known unsafe download-to-shell fixture, exercises the marketplace body
generator and release preflight, and proves the archives are deterministic.
