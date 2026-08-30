# Failure ladder

Use the first failing layer to constrain the diagnosis.

| Layer | Read-only evidence | Typical cause |
| --- | --- | --- |
| Files | `manifest.json`, entry points, symlinks | Missing file, unsafe path, malformed JSON |
| Schema | toolkit validator and `omarchy plugin validate` | Reserved ID, kind/key mismatch, unsupported schema |
| Discovery | `omarchy plugin list --json` | Wrong directory, duplicate ID, rescan not observed |
| Enablement | `shell.json`, plugin list enabled field | Widget absent from layout or plugin absent from `plugins[]` |
| Load | shell/Quickshell diagnostics | Missing import/type, `required` property before injection, syntax error |
| Lifecycle | `omarchy-shell shell summon/hide/toggle` | Missing `open`/`close`, invalid payload handling |
| IPC | direct bounded method call | Wrong target, service not enabled, result mismatch |
| Process | direct CLI command with fixture | PATH, version, auth, timeout, malformed output |
| Interaction | live focused monitor | anchor, focus, pointer, multi-monitor, stale instance state |

Useful commands on an Omarchy host:

```bash
omarchy plugin validate /path/to/plugin
omarchy plugin list --json
omarchy-shell shell ping
omarchy-shell shell listPlugins
omarchy-shell shell listShellConfig
omarchy debug --no-sudo --print
```

Do not dump complete debug output into a public issue without reviewing it for
hostnames, paths, account data, and credentials.

## Broken full bar

If a third-party `bar` fails to instantiate, inspect `bar.id` in the effective
shell config. The safe target is the built-in `omarchy.bar`. Show and back up the
config before changing it, then restart the shell only with authorization.

## Reload behavior

Files under `~/.config/omarchy/plugins/` are watched. A reload can destroy and
recreate QML instances, so stale external processes, timers, and persistent
properties may expose bugs that a first load does not. Test both edit reload and
full shell restart.
