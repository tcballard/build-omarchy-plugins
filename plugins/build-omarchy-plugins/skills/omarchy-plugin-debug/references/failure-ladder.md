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

On Quattro reviewed 29 September 2026, `keepLoaded: true` also keeps a service
instance mounted across plugin hot-reload. Editing that service does not replace
it; its new code requires a shell restart. Check the manifest before diagnosing
stale output as a failed file watcher or starting a duplicate service. Obtain
restart authorization and account for active session-lock state.

If a widget loses its service only under a replacement bar, inspect the injected
interface before changing the poller: replacement bars give hosted widgets a
service-less entry facade. Compare with the trusted built-in bar and handle the
unavailable state; do not bypass the boundary via QML parent traversal.

Source: [reviewed shell contract](https://github.com/omacom/omarchy/blob/e332dc975d5f635294c497ebb54feb98dc3d89eb/docs/omarchy-shell.md).

Files under `~/.config/omarchy/plugins/` are watched. A reload can destroy and
recreate QML instances, so stale external processes, timers, and persistent
properties may expose bugs that a first load does not. When changing reload or
resource ownership, test both edit reload and full shell restart on an authorized
Omarchy host; otherwise record those checks as unrun.
