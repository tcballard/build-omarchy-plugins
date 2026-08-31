# Reviewer notes

## Product boundary

Build Omarchy Plugins is a skills-only, provider-neutral developer tool. It
helps a coding agent work on repositories that target the Omarchy 4 Quattro
shell plugin contract.
It is not an Omarchy runtime plugin and it does not install software on the
reviewer's machine.

## Architecture

- Twelve narrowly routed skills live in a canonical Agent Skills tree, with an
  OpenAI adapter generated from the same source.
- Executable Python utilities use only the Python standard library.
- The installer targets the shared `.agents/skills` convention as well as the
  native Codex, Cursor, Gemini CLI, Claude Code, and OpenCode skill directories.
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
- Skill installation, update, and removal are receipt-backed transactions;
  locally modified managed files stop update/removal unless the user explicitly
  inspects and forces the named operation.
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

Use Python 3.11 or newer and run `./scripts/test`. The suite validates the
portable package and OpenAI adapter, checks adapter synchronization, tests all
host installation layouts and managed lifecycle behavior, validates every skill
route, generates all six current plugin kinds, rejects traversal, special files,
unsafe ancestors, duplicate JSON keys, and unreviewed binaries, checks a known
unsafe download-to-shell fixture, exercises marketplace and exact-provenance
release preflights, and proves archives are deterministic.

The repository CI repeats this on Python 3.11–3.13 across Linux, macOS, and
Windows. Live Omarchy shell runs and live model-provider behavior are not
claimed by that portable matrix; `PORTABILITY.md` describes the narrower
evidence boundary and optional OpenCode probe.
