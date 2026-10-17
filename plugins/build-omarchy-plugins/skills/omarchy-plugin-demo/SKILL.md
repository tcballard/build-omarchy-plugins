---
name: omarchy-plugin-demo
description: Create or verify a deterministic Omarchy plugin demo and marketplace screenshot using fictional data. Use for fixture CLIs, isolated state, reversible shell setup, screenshot capture, and demo evidence; never use real credentials or live personal data.
---

# Demonstrate an Omarchy plugin

Use fictional deterministic fixtures and the actual requested UI state. Resolve `<skill-dir>` to this skill's directory:

```bash
python3 "<skill-dir>/scripts/demo_preflight.py" /absolute/path/to/plugin
```

Read [reversible demo](references/reversible-demo.md) before a harness touches the live shell. Use existing authorization for live changes; preparing a harness alone does not authorize changing desktop state.

- Inject demo data explicitly and verify the running shell received it. Never commit real account data, credentials, notifications or personal paths.
- Back up config and installation with unique paths; refuse stale recovery artifacts.
- Restore config, plugin, workspace, cursor and normal shell on exit, failure or interruption. Retain recovery files and exact paths if restoration fails.
- Use an empty workspace and machine-readable readiness, not arbitrary long sleeps.
- Capture a focused frame and check the current marketplace preview limits (pinned guidance: under 50 MB and 40 megapixels).

Without a live display, finish portable fixtures/harness checks and report capture as unrun. A mockup does not prove a plugin ran. Report source/fixture identity, actual capture path and restoration result so release work can distinguish prepared assets from observed runtime evidence.
