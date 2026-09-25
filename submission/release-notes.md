# Build Omarchy Plugins v0.6.0 — clearer skill boundaries

The twelve skills still cover the complete Omarchy 4 plugin workflow. This
release makes it clearer which one to use when a task touches more than one
surface: a widget and its popout, shared polling and QML, a broken plugin and
its regression test, or a GitHub release and marketplace submission.

The QML/service and test/publish review references remain in each independently
installable skill. Their shared content is now identical and checked in the
test suite. Service-specific agent and credential-broker guidance stays with
the service process guide.

There is no new Omarchy API or marketplace contract claim in this release.
Portable checks cover the skill bundle and packaging; live plugin behavior
still needs testing on the target Omarchy host.

The provider-neutral bundle supports OpenCode and other skill hosts. Updates
remain transactional, with CI across Linux, macOS, and Windows and an SPDX 2.3
software bill of materials. Release automation prepares a draft but cannot publish it.

[Full changes](https://github.com/tcballard/build-omarchy-plugins/compare/v0.5.1...v0.6.0)
