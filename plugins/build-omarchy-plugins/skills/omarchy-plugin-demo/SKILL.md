---
name: omarchy-plugin-demo
description: Create or verify a deterministic Omarchy plugin demo and marketplace screenshot using fictional data. Use for fixture CLIs, isolated state, reversible shell setup, screenshot capture, and demo evidence; never use real credentials or live personal data.
---

# Demo Omarchy Plugins

A good demo proves a real UI state while leaving the user's machine exactly as
it found it.

Resolve `<skill-dir>` to the directory containing this loaded `SKILL.md`.
Run the preflight against an existing harness:

```bash
python3 "<skill-dir>/scripts/demo_preflight.py" /absolute/path/to/plugin
```

Read [references/reversible-demo.md](references/reversible-demo.md) before
creating or running a harness that touches the live shell.

With no live Omarchy display, prepare fixtures and the capture harness, validate
what can run, and report capture as unrun. A generated mockup is not evidence of
the plugin running. Use existing authorization for a specified live demo;
preparing a screenshot harness alone does not authorize changing desktop state.

## Required properties

- Use fictional, committed, deterministic fixture data. Never copy real account
  records, tokens, home paths, or notification content into the repository.
- Put fixture executables first in a demo-only `PATH` or inject a local data
  source explicitly. Verify the running shell received the intended demo
  environment before capturing evidence.
- Back up plugin installation and `shell.json` with collision-resistant paths;
  refuse to start when stale recovery artifacts exist.
- Trap normal exit, failure, interrupt, and termination. Restore config, plugin,
  workspace, cursor, and normal shell before removing recovery state.
- Use an empty workspace and wait for a machine-readable ready condition rather
  than sleeping for an arbitrary long duration.
- Capture the smallest frame that communicates the plugin. Keep the root preview
  under the marketplace's current 50 MB and 40-megapixel limits.

If restoration fails, retain the recovery artifacts and print their exact
paths. Never delete an ambiguous backup merely to make the next demo run.

## Inputs and completion

Use the target checkout, requested UI state and fictional fixtures. Check that
any inherited test evidence describes this source.

Hand off the harness, fixture and source identity, capture path when actually
produced, and restoration result. If capture or restoration could not finish,
retain the precise pending check or recovery path. Release preparation must be
able to distinguish a prepared harness from an observed runtime preview.
