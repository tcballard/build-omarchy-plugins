# Build Omarchy Plugins v0.6.0 — clearer routes through the work

v0.6.0 is out. The bundle still has twelve skills. This release makes it clearer which one owns the work when a plugin task crosses surfaces.

- A bar widget owns its button, anchor and settings. A separately mapped panel owns its window and dismissal.
- A service owns shared polling and IPC. QML patterns supplies the common hosted-component rules.
- Debug finds the failure; test records the regression evidence. Release prepares the versioned assets; publish handles the marketplace issue.
- The review guidance shared by two independently installable skills now has a parity check, so those copies cannot quietly drift.

The practical change is a cleaner route from a small QML fix to a release, without loading the whole lifecycle for every edit. This changes guidance, not Omarchy APIs or marketplace policy. We have not measured a model-behaviour improvement from it.

All 64 portable tests passed locally. Required CI passed on Linux, macOS, and Windows. The release workflow built the assets twice, attested them, then downloaded and checked the draft. A plugin built with these skills still needs its own live Omarchy checks.

The provider-neutral bundle supports OpenCode and other Agent Skills hosts. Updates remain transactional, and the archives include an SPDX 2.3 SBOM. Release automation can prepare a draft but cannot publish it.

[Get v0.6.0 and its checksums](https://github.com/tcballard/build-omarchy-plugins/releases/tag/v0.6.0). For an existing skills installation, preview the change with `python3 scripts/install_agent_skills.py --update --diff` before applying `--update`.

Where does the bundle still send your agent to the wrong skill? Send me the prompt and what it did.

[Full changes](https://github.com/tcballard/build-omarchy-plugins/compare/v0.5.1...v0.6.0)
