---
name: omarchy-plugin-debug
description: Diagnose an Omarchy Quattro plugin that is not discovered, validated, enabled, loaded, reloaded, summoned, or behaving correctly. Use for local environment, manifest, shell config, QML runtime, IPC, process, and recovery failures.
---

# Debug an Omarchy plugin

Start from the symptom and actual checkout. Diagnosis-only requests stay read-only; for repairs reproduce the failure, change the smallest responsible path and rerun the failing check.

Resolve `<skill-dir>` to this skill's directory:

```bash
python3 "<skill-dir>/scripts/doctor.py" /absolute/path/to/plugin
```

Use `--live` only on an Omarchy host for read-only IPC probes. Read [failure ladder](references/failure-ladder.md) to trace manifest/path → official validation → discovery → enabled state → QML load/injection → summon/IPC → external data → interaction/monitors.

For colour failures inspect `Commons.Color` qualification on Qt 6.12, then distinguish incorrect plugin bindings from shared palette/theme failures.

Preserve user configuration. Clone built-ins or edit third-party user code; never patch packaged shell files for a customization. Recover a broken replacement bar by restoring `omarchy.bar` or removing custom `bar.id`, retaining a backup. Prefer supported plugin removal; handmade directories may be backed up by the host.

Use the user's existing authorization for live reload/config/restart actions. Repository repair alone does not authorize desktop disruption. Prepare a concrete recovery change before seeking any missing authorization.

Report the cause, actual correction, relevant check results and remaining uncertainty. Do not hide failures behind fixture data or claim runtime success from static checks.
