# Kind selection and design record

Verified against Omarchy `quattro` source on 29 August 2026.

## Select the load model

| Kind | Choose it when | Lifetime | Required entry-point key |
| --- | --- | --- | --- |
| `bar-widget` | Compact information or action belongs in the active bar | One visual instance per configured placement/monitor | `barWidget` |
| `panel` | A compact floating surface is summoned or stays available | Loaded on demand unless kept loaded | `panel` |
| `overlay` | A fullscreen shell interaction must cover the desktop | Loaded on demand unless kept loaded | `overlay` |
| `menu` | A navigable action or selection surface is summoned | Loaded on demand unless kept loaded | `menu` |
| `service` | State or polling must be process-wide and UI-independent | Singleton while enabled | `service` |
| `bar` | The entire Omarchy bar is being replaced | Exactly one active bar | `bar` |

Common justified combinations:

- `service` + `bar-widget`: one poller and one visual instance per monitor.
- `menu` + `bar-widget`: the same product has a bar launcher and a summoned menu.
- `panel` + `service`: a panel is transient while its data remains warm.

Do not add a kind only to make a component reachable. A bar widget may load a
private sibling panel internally without claiming a top-level `panel` kind.

## Design record template

```markdown
# Plugin design

- ID:
- User problem:
- Kinds and entry points:
- Per-instance state:
- Process-wide state:
- Durable state and owner:
- External commands/packages:
- Credential source:
- Network endpoints:
- IPC target and methods:
- Failure states:
- Enable/update/remove behavior:
- Static/unit/live tests:
- Demo fixture and screenshot state:
- Deferred scope:
```

## Boundary questions

- Can the feature work by querying an installed CLI instead of reading its
  configuration or credentials?
- Does a daemon need independent supervision when `omarchy-shell` restarts?
- Will one visual component be instantiated on every monitor?
- What happens when the dependency disappears after a successful start?
- What persists after `omarchy plugin remove`, and is that behavior documented?

Authoritative sources:
[Omarchy shell documentation](https://github.com/basecamp/omarchy/blob/quattro/docs/omarchy-shell.md)
and [shell plugin manual](https://omarchy.org/manual/shell-plugins/).
