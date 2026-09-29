# Build Omarchy Plugins v0.6.1 — follow the current Quattro contract

Quattro now limits the host interfaces handed to third-party plugins. This patch
teaches the existing twelve skills those limits, so agents do not treat injected
objects as unrestricted shell access or mistake a retained service for broken
hot reload.

- Explain scoped host APIs, detached snapshots and authentication boundaries.
- Document why a service-backed widget can behave differently under a replacement
  bar, and require an explicit unavailable-service state.
- Explain that `keepLoaded` service code changes need a shell restart.
- Make contract monitoring distinguish newer upstream commits from changed
  documents, while preserving immutable pins and failing closed on fetch errors.

Scoped APIs do not sandbox same-process QML. The marketplace forms and policies
are unchanged. Portable tests cover the bundle and tooling; new live-desktop
compatibility scenarios are documented separately and are not claimed as passes.

CI targets Linux, macOS, and Windows.

This is a release candidate. Publication and final CI evidence are recorded
separately. The provider-neutral bundle supports OpenCode and other Agent Skills
hosts, retaining transactional updates and its
SPDX 2.3 SBOM; release automation prepares drafts and cannot publish them.

[Changes since v0.6.0](https://github.com/tcballard/build-omarchy-plugins/compare/v0.6.0...fix/v061-quattro-contracts)
