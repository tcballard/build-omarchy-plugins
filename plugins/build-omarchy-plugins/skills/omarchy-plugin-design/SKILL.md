---
name: omarchy-plugin-design
description: Design an Omarchy 4 Quattro shell plugin before implementation. Use when choosing plugin kinds, architecture, dependencies, state ownership, IPC, security boundaries, or evidence. Do not treat legacy package installers as shell plugins; route those through migration.
---

# Design an Omarchy plugin

Read the installed Omarchy skill's `plugins.md` and the target host's commands before choosing an API. Use this bundle as deeper engineering guidance; preserve the installed system's contract. For the Agents-panel entry point and personal tweaks, see [host workflow](references/host-workflow.md).

1. Inspect the existing plugin and preserve settled identity, scope and state decisions. For a new idea, check built-ins, marketplace and public prior art; compare behavior, licence and maintenance before building.
2. Choose personal customization, public project or marketplace intent. Default to the requested local outcome; publication is a separate action. Clone a built-in for a small customization rather than scaffolding a replacement.
3. Choose the smallest useful surface and observable acceptance criteria. Read [kind selection](references/kind-selection.md) when choosing kinds. Use a permanent namespaced ID outside `omarchy.*`.
4. Assign transient state to each visual instance, shared polling to a service, ordinary settings to `shell.json`, and application data/credentials to their external owner.
5. Identify commands, packages, network, credentials, privileged setup and removal behavior. Read [integration boundaries](references/integration-boundaries.md) for agent, broker or privileged integrations; [adapter contracts](references/abstraction-contracts.md) for repeated process/network/storage operations.

Plugins have a root `manifest.json`, hosted QML entry points and user-level unsandboxed execution. Plugin add does not run installation hooks. Keep external setup explicit.

For design-only work, return the recommendation and tradeoffs. For a build, continue to implementation and relevant checks. Record decisions in the project's existing record only when continuity needs it; no prescribed planner, agent tools or handoff format is required.
