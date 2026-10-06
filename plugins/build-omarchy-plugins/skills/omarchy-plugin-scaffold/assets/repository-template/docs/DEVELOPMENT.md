# Develop and test the plugin

Initialize first, then run `./tests/run`. On the target Omarchy machine run `omarchy plugin validate .` and record `omarchy-version`. Portable checks validate a deliberately narrow structural subset; the installed host's validator is authoritative.

The example is a stateless bar toggle. Test horizontal and vertical bars, disable/re-enable, reload, monitor changes and theme changes. No persistent settings are claimed.

Use your current Omarchy plugin development/linking workflow or Plugin Workbench after inspecting its current commands. The included `.omarchy-workbench.json` proposes checks; it does not grant trust or execute them automatically.

Before a public release, document the exact verified install command for this repository and the installed host version. This starter has no published marketplace listing. Disable it using the host's plugin manager before removing the linked/installed copy. It does not modify Hyprland settings or create user data.

For richer surfaces, use the current Build Omarchy Plugins generator to select panel, overlay, menu or service contracts. Do not declare extra kinds until their entry points exist.
