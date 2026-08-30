---
name: omarchy-plugin-debug
description: Diagnose an Omarchy Quattro plugin that is not discovered, validated, enabled, loaded, reloaded, summoned, or behaving correctly. Use for local environment, manifest, shell config, QML runtime, IPC, process, and recovery failures.
---

# Debug Omarchy Plugins

Start with read-only evidence. Run:

```bash
python3 scripts/doctor.py /absolute/path/to/plugin
```

Add `--live` only on an Omarchy host when shell IPC probes are appropriate.
The doctor does not modify configuration or restart the shell.

Read [references/failure-ladder.md](references/failure-ladder.md) and isolate
the first failing boundary:

1. repository and JSON structure;
2. official `omarchy plugin validate`;
3. discovery in `omarchy plugin list --json`;
4. enabled state in `shell.json`;
5. QML component load and injected properties;
6. summon or IPC routing;
7. external process and data parsing; and
8. interaction or multi-monitor behavior.

## Recovery rules

- Preserve user config before any mutation. Do not edit files under
  `$OMARCHY_PATH`; clone or work in the third-party plugin directory.
- A broken third-party bar can remove the visible bar. Recover by resetting the
  active bar to `omarchy.bar` or removing the custom `bar.id`, then restart the
  shell. Show the exact proposed change before applying it.
- Prefer `omarchy plugin remove <id>` for installed Git plugins. Hand-made
  directories are backed up by Omarchy rather than deleted.
- Treat shell reload, config changes, and process restarts as mutations. Obtain
  the user's authorization immediately before performing them.

After fixing the first failing boundary, rerun the same probe and then the full
test skill. Do not paper over a load failure with silent fallback data.
