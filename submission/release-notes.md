# Build Omarchy Plugins v0.9.0 — Less ceremony. More building.

I cut the twelve skill entry points by 58%: 6,884 words down to 2,892. Same skill names. Less context to load before getting to work.

This is a substantial refactor of how the bundle guides an agent through building an Omarchy plugin. Detailed mechanics stay in linked references, ready when the task needs them. The core instructions assume no particular agent, harness, planner or proprietary tools. Pick your own setup.

- **Fits Omarchy's new starting point.** The Agents panel's Plugin button on current Quattro development builds launches your default agent with Omarchy's built-in guide. This release explains how the bundle complements that flow. The button does not automatically load the bundle.
- **Small tweaks can stay small.** Clone a built-in widget, edit your own copy and stop when it works. A personal customization does not need a public repo or a marketplace submission.
- **Catches up with Quattro.** Generated palette references now avoid the Qt 6.12 `Color` collision. The generator and validator accept all six bar sections, with guidance for clock-adjacent placement and tray popouts.
- **Speaks the desktop's language.** New guidance covers plugin-owned translations, live language switching, plurals, number/date formatting and RTL layouts. Check the installed host before adopting newer APIs.

The refactor passed 79 toolkit tests and CI on Linux, macOS, and Windows. A fresh-session build also produced a working implementation of a small focus widget and passed its portable checks. Live Qt rendering, tray geometry, language switching and RTL still need testing on an Omarchy desktop; those checks are not claimed here.

The provider-neutral bundle retains OpenCode support, transactional updates, the offline repository starter and an SPDX 2.3 SBOM. Host packaging stays optional. Release automation builds verified drafts and cannot publish them by itself.

For an existing CLI install, check out `v0.9.0`, preview `--update --diff`, then apply `--update` using your usual target and scope. Check downloaded archives against `SHA256SUMS`.

Try: **“Use the installed Omarchy guide and Build Omarchy Plugins skills. Build the smallest useful version, enable it locally and verify the interaction.”**

[Full changes](https://github.com/tcballard/build-omarchy-plugins/compare/v0.8.0...v0.9.0)
