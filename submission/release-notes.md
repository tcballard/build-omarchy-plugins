# Build Omarchy Plugins v0.11.0: Current host guidance, simpler scaffolds

Release candidate. Not published yet.

New plugin projects no longer include Workbench setup. Workbench is deprecated, so both scaffold paths now leave you with the project's own checks and the installed Omarchy validator.

The twelve skills also catch up with Quattro's motion and shell lifecycle:

- **Respect reduced motion.** Reuse Omarchy's panel and popup animations, route custom durations through the host setting, and stop infinite animations when motion is disabled.
- **Diagnose the right layer.** Use bounded shell journal logs, distinguish plugin reload from a full shell restart, and check host fixes for combined bar-widget/service plugins.
- **Keep generated projects lean.** Workbench files, registration steps and recommendations are removed from generated projects and their retained blueprints. The pinned source template remains intact.

Since the last published release, v0.9.0, this also includes the privacy improvements prepared in the unpublished v0.10.0 draft: bounded stdin for private text, upgrade-state fixtures, optional QML plain-text checks, and generated checkouts without authoring-agent instruction files.

The bundle retains twelve provider-neutral skills, OpenCode support, transactional updates and an SPDX 2.3 SBOM. Release automation prepares verified drafts and cannot publish them.

The README's Coffee badge now sits centred on its own row below the Built for Omarchy badge.

Validation: the refresh passed 89 Python tests, six Node cases and required CI across Linux, macOS, and Windows, with CodeQL green. The local optional Qt fixture was skipped. The release candidate gets its own checks and reproducible package build before tagging. Live Omarchy motion, CPU use, lock/notification recovery and multi-kind lifecycle acceptance remain unrun here; portable checks do not establish those behaviours.

After publication, existing CLI installs can check out `v0.11.0`, preview `--update --diff`, then apply `--update` with their usual target and scope. Verify downloaded archives against `SHA256SUMS`. Until then, the README's install commands use published v0.9.0.

[Changes since the last published release](https://github.com/tcballard/build-omarchy-plugins/compare/v0.9.0...main)
