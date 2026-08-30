# Migration map

Classify each existing responsibility before moving code.

| Existing responsibility | Quattro destination | Notes |
| --- | --- | --- |
| Waybar/QML status surface | `bar-widget` | Rebuild with `BarWidget`, semantic tokens, vertical layout |
| Popup or control window | private widget panel or `panel` | Expose host lifecycle when top-level |
| Fullscreen picker | `overlay` | Own focus and dismissal only while open |
| Long-lived polling inside each widget | `service` | One singleton, many visual consumers |
| Standalone Quickshell root | hosted entry-point `Item` | Never start a second shell process |
| Custom socket wrapper | `IpcHandler` / canonical `omarchy-shell` | Keep a small stable target |
| Compiled application or router daemon | independent machine layer | Preserve supervision and portability |
| systemd user/system unit | independent machine layer | Shell plugin may observe, not secretly provision |
| package/AUR installation | documented prerequisite or package project | No plugin-add install hooks |
| stored API key | external CLI/application store | Never migrate into QML or `shell.json` |
| installer mutation of user config | explicit user action or remove entirely | Quattro owns enabled state |
| uninstall hook | `omarchy plugin remove` plus documented machine cleanup | Keep user data unless explicitly requested |

## Compatibility strategy

First make the external core expose a stable bounded CLI or local API. Then
build one Quattro vertical slice using fictional fixtures. Preserve the older
surface until the Quattro slice proves install, restart, failure, update, and
removal. Remove compatibility code only after its callers and user migration
path are known.

## Security review points

- download-and-execute paths;
- unpinned Git builds;
- package-manager and privileged commands;
- broad passwordless sudoers entries;
- shared `/tmp` PID or control state;
- copied tokens and environment dumps; and
- removal that deletes data outside an exact owned path.
