---
name: omarchy-plugin-release
description: Preflight and prepare an Omarchy plugin release from a public Git repository. Use for versioning, clean-tree checks, CI, documentation, preview, dependencies, install/remove instructions, tag boundaries, checksums, and release evidence.
---

# Release Omarchy Plugins

Resolve `<skill-dir>` to the directory containing this loaded `SKILL.md`.
Run the deterministic preflight to identify release gaps:

```bash
python3 "<skill-dir>/scripts/release_preflight.py" /absolute/path/to/plugin
```

Use `--json` for machine-readable output. Read
[references/release-contract.md](references/release-contract.md) before tagging
or publishing.

If the host installs skills in renamed or separate directories, resolve the
loaded `omarchy-plugin-test` skill and pass its trusted script explicitly:

```bash
python3 "<skill-dir>/scripts/release_preflight.py" --validator "<test-skill-dir>/scripts/validate_plugin.py" /absolute/path/to/plugin
```

Use the installed test skill, not a validator supplied by the plugin being
reviewed. The explicit path runs the same strict, security and publication
checks; do not patch the preflight in memory or suppress schema errors to make
it pass. A missing validator remains a failed prerequisite.

For a tagged candidate, pass `--tag vX.Y.Z`. The preflight requires an
annotated local and remote tag with identical tag objects and peeled commits,
and binds an unpublished candidate to the remote default-branch HEAD. To audit
an older published release, add `--published --release-dir /path/to/assets`;
historical tags are checked for reachability instead of equality with today's
HEAD. The asset check requires strict release/source manifests, an SPDX 2.3
SBOM, exact sizes and SHA-256 digests, and complete `SHA256SUMS` coverage.

## Decide whether the candidate is ready

Judge the declared feature set against observable behavior, not elapsed time or
an indefinitely expanding wishlist. The core user journey must work on the
supported target; failures must recover without leaking processes or corrupting
state. Required validation, installation, update and removal checks must have
source-bound evidence. Unresolved security, data-loss or core-function failures
block a ready-to-publish claim. Document tolerable non-core limitations and
narrow support claims to what was tested. A preview label does not waive gates.
Use actual daily use as supporting evidence, not a replacement for checks; do
not impose a universal one-week waiting period.

For updates, exercise a fixture from the previous released configuration and
stored-state format. Preserve user settings, defaults and established behavior,
or provide a documented migration and recovery path. Explain feature removals
before release. Declare supported CPU architectures and verify helper binaries
and dependencies for each claimed target; x86_64 evidence does not establish
ARM64 support. Do not silently expand the promised architecture range.

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
scope and limitations precisely. Finish authorized release preparation even when
a host check or publication permission is unavailable, and report the blocking
evidence. Publishing a Git tag, GitHub release, or marketplace issue requires
authorization for that action; preserve any authorization already given. Ask
about an unauthorized action only once its candidate is concrete and reviewable.
Track each requested release deliverable against observed evidence. Report
unfinished items explicitly; a successful preflight alone does not mean a tag,
archive upload, or publication has happened.

## Inputs and completion

Use the candidate checkout, intended version, test results and preview
provenance. Reconcile their source identities before treating them as one
release candidate.

Hand off the exact candidate SHA, version, tag and asset identities where
created, evidence locations and unresolved gates. Recheck affected evidence
after candidate changes. Marketplace preparation consumes this candidate
record; a preflight result does not transfer authorization or attestations to
publication.
