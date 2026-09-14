---
name: omarchy-plugin-debug
description: Diagnose an Omarchy Quattro plugin that is not discovered, validated, enabled, loaded, reloaded, summoned, or behaving correctly. Use for local environment, manifest, shell config, QML runtime, IPC, process, and recovery failures.
---

# Debug Omarchy Plugins

For colour failures, distinguish the plugin consumer from the shared theme source. Inspect QML token bindings and reload state when one plugin is wrong. If the shared palette or generated shell TOML is wrong across surfaces, use omarchy-theme-debug when available. Keep diagnosis-only requests read-only across both workflows.

For diagnosis-only requests, return the cause and proposed correction without
editing. For a requested fix, patch the affected code in place and preserve
unrelated content; report independent discoveries separately.

Start with the reported failure and read-only evidence. Resolve `<skill-dir>`
to the directory containing this loaded `SKILL.md`, independently of the plugin
checkout or current working directory. For environment and discovery diagnosis:

```bash
python3 "<skill-dir>/scripts/doctor.py" /absolute/path/to/plugin
```

Add `--live` only on an Omarchy host when shell IPC probes are appropriate.
The doctor does not modify configuration or restart the shell.

Read [references/failure-ladder.md](references/failure-ladder.md) and isolate
the relevant failing boundary; use known logs to enter at the appropriate layer:

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
- Treat live shell reloads, config changes, and process restarts as mutations.
  Use authorization already given for the specific action; if it is absent,
  prepare the patch and recovery instructions before asking. A request to fix
  repository code does not by itself authorize disrupting the live desktop.

After fixing the cause, rerun the failing probe and checks for the affected
behavior, plus required repository gates. Broaden testing for a concrete
remaining risk, not automatically to the full release lifecycle. Do not paper
over a load failure with silent fallback data. Report the cause, patch, evidence,
and any host-only check that could not run. During a longer investigation,
report findings tied to observed commands and results; distinguish a proposed
next action from one actually executed.

## Inputs and completion

Use the reported symptom, exact plugin checkout and available logs or
reproducing command. Establish whether the request is diagnosis or repair.

A diagnosis identifies the failing boundary and supported correction, marking
uncertainty where reproduction is unavailable. A repair also includes the
patch and rerun evidence for the original failure. Hand the actual changed
checkout and any remaining checks to testing, rather than an earlier clean
commit.
