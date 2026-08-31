---
name: omarchy-plugin-release
description: Preflight and prepare an Omarchy plugin release from a public Git repository. Use for versioning, clean-tree checks, CI, documentation, preview, dependencies, install/remove instructions, tag boundaries, checksums, and release evidence.
---

# Release Omarchy Plugins

Run the deterministic preflight first:

```bash
python3 scripts/release_preflight.py /absolute/path/to/plugin
```

Use `--json` for machine-readable output. Read
[references/release-contract.md](references/release-contract.md) before tagging
or publishing.

For a tagged candidate, pass `--tag vX.Y.Z`. The preflight requires an
annotated local and remote tag with identical tag objects and peeled commits,
and binds an unpublished candidate to the remote default-branch HEAD. To audit
an older published release, add `--published --release-dir /path/to/assets`;
historical tags are checked for reachability instead of equality with today's
HEAD. The asset check requires strict release/source manifests, an SPDX 2.3
SBOM, exact sizes and SHA-256 digests, and complete `SHA256SUMS` coverage.

## Release boundary

- The root `manifest.json` version, release notes, tested commit, and tag must
  describe the same source.
- Require a clean tree and record the full commit SHA after all release changes
  merge. Never move a published tag.
- Run portable and official validation, fixture/unit tests, live-shell lifecycle,
  install-from-Git, update, and removal on the intended Omarchy version.
- Document external packages, authentication, network access, files written,
  processes launched, and anything deliberately left behind on removal.
- Keep installation and removal commands copyable and symmetric.
- Include a current root preview and reproducible capture instructions when the
  plugin has UI.

Do not claim the release is secure because a static scan passed. Report tested
scope and limitations precisely. Publishing a Git tag, GitHub release, or
marketplace issue is an external mutation and requires explicit authorization
at that boundary.
