# Work with Omarchy's built-in creation flow

Reviewed against Quattro `cce8b1c971df64a7610b818ff8819e4bea04584a` on 17 October 2026. These are development-branch capabilities; inspect the installed host before using them.

## Agents panel

The Agents panel's Plugin starter passes this prompt to `omarchy-agent-prompt`, which launches the configured default coding agent:

> Make me a new Omarchy shell plugin. Ask me what I'd like it to do, then build it following the Omarchy skill's plugin guide and enable it.

This selects the built-in `omarchy` skill's `plugins.md`, not this bundle. The bundle is an optional engineering companion. It does not require a particular model, terminal, planner, connector or worker topology. Native skill discovery depends on the agent host; plain file reads also work.

Read `$OMARCHY_PATH/default/agents/skills/omarchy/plugins.md` when available. Otherwise inspect the installed skill location or the exact target host source. Use `omarchy commands` and `omarchy plugin --help` to discover available commands. A missing built-in guide does not prevent portable implementation; record the host contract still needing verification.

A user can follow the starter with:

> Also use the installed Build Omarchy Plugins skills where useful. Read the installed Omarchy plugin guide first. Build the smallest working version, enable it locally and verify the visible interaction. Keep release and marketplace work separate.

Do not claim the panel loads this bundle automatically. Installing skills is distinct from installing a desktop shell plugin, and the bundle's portable `plugin.json` is distinct from a shell plugin's `manifest.json`.

## Personal customization

For a small change to an existing built-in widget:

```bash
omarchy plugin clone omarchy.workspaces
```

Inspect the reported destination/ID and edit the user-owned copy under `~/.config/omarchy/plugins/`. Cloning replaces the built-in's placement with the clone; preserve unrelated layout/settings. Never edit packaged `$OMARCHY_PATH/shell/plugins/` files for an end-user customization. On this reviewed host, saving user plugin files triggers reload; `keepLoaded` service changes can require a shell restart. Inspect actual behavior before disrupting the desktop.

A personal tweak needs neither a public repository nor a marketplace packet. A new local plugin can likewise stop at implementation, validation, enablement and the requested visible behavior. Confirm discovery, enabled state and the real interaction; a manifest pass alone is not completion. If the host/display is unavailable, finish portable work and identify those exact pending checks.

Sources: [starter](https://github.com/omacom/omarchy/blob/cce8b1c971df64a7610b818ff8819e4bea04584a/shell/plugins/agents/Panel.qml), [installed guide](https://github.com/omacom/omarchy/blob/cce8b1c971df64a7610b818ff8819e4bea04584a/default/agents/skills/omarchy/plugins.md).
