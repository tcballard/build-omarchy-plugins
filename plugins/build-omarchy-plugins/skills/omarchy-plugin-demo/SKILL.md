---
name: omarchy-plugin-demo
description: Create or verify a deterministic Omarchy plugin demo and marketplace screenshot using fictional data. Use for fixture CLIs, isolated state, reversible shell setup, screenshot capture, and demo evidence; never use real credentials or live personal data.
---

# Demo Omarchy Plugins

A good demo proves a real UI state while leaving the user's machine exactly as
it found it.

Run the preflight against an existing harness:

```bash
python3 scripts/demo_preflight.py /absolute/path/to/plugin
```

Read [references/reversible-demo.md](references/reversible-demo.md) before
creating or running a harness that touches the live shell.

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
