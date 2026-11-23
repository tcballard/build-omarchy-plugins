# Build Omarchy Plugins v0.11.1: Installation docs catch up

This maintenance release fixes stale installation and release documentation after v0.11.0 shipped.

- README checkout commands and archive examples now use the published v0.11.0 baseline instead of v0.9.0, including the Claude Code plugin instructions.
- The changelog records v0.11.0 as published on 8 November 2026.
- Distribution manifests and submission metadata agree on v0.11.1.

The twelve skills, generators, validators and reviewed upstream contract pins are unchanged from v0.11.0.

Validation for this candidate must come from its own CI and release workflow. Publication requires successful CI / Required, two byte-identical builds, provenance attestations and downloaded-asset verification. No fresh live desktop or model-behaviour testing is claimed.

Existing CLI installs can check out `v0.11.1` after publication, preview `--update --diff`, then apply `--update` with their usual target and scope. Verify downloaded archives against `SHA256SUMS`.

[Full changes](https://github.com/tcballard/build-omarchy-plugins/compare/v0.11.0...v0.11.1)
