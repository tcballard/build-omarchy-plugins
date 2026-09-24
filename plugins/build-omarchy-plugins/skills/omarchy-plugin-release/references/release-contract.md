# Release contract

## Required repository surface

- one root `manifest.json` and matching entry points;
- root README with requirements, install, use, update, and removal;
- root license and third-party dependency/license notes;
- current root preview for visual plugins;
- automated portable tests and current live-shell evidence;
- public issue/support route and security reporting instructions.

## Pre-tag sequence

1. Select the intended source boundary and update the manifest version.
2. Update release notes and compatibility claims.
3. Run static, unit, fixture, live-shell, install, update, and removal evidence.
4. Merge release-only changes and require green CI.
5. Record the final full SHA and confirm the tree is clean.
6. Create an immutable annotated tag at that SHA.
7. Publish release notes that describe only the tested boundary.

Before publication, run the preflight with `--tag`. Run it again against the
downloaded draft assets with `--tag --release-dir`; never validate only the
local upload directory. For an already-published historical tag, use
`--published` so the commit must remain reachable from the current remote
default-branch history but is not incorrectly required to equal its HEAD.

Do not move a published tag or retarget marketplace evidence to a different
commit. If the boundary changes, produce a new version and rerun the relevant
evidence.

## Compatibility statement

State the tested Omarchy version or full source SHA, plugin SHA, hardware/display
scope, and anything not tested. Quattro's plugin contract is evolving; avoid
unbounded claims such as “works on all Omarchy versions.”

## Security language

Marketplace baseline and local lint results are deterministic limited scans.
Describe their outcome as evidence for an exact commit and retain the required
“not a security audit” boundary.

## Executable dependency and backend evidence

Apply these checks to the installation/build paths the plugin actually uses.
Recent [Mynah review](https://github.com/omacom/omarchy-plugin-marketplace/issues/7255#issuecomment-5745951194)
and [MFA review](https://github.com/omacom/omarchy-plugin-marketplace/issues/7491#issuecomment-5741754091),
checked 20 September 2026, extend the earlier supply-chain guidance:

- Pin third-party Actions/reusable workflows to reviewed full commit SHAs,
  executable container images to digests, and scope workflow token permissions.
  Inspect local actions too. A syntactically valid hash does not prove provenance.
- Bind automatically installed build/runtime dependencies transitively, including
  build backends, with lockfiles and verified artifact hashes where supported.
  Exercise the real installer: a lock used only by CI does not protect startup.
  Review reproducible CI package/toolchain inputs where they build shipped code;
  do not infer a universal ban on hosted runners from an individual review.
- Bind downloaded executable artifacts to expected digests in the reviewed
  source or independently authenticated provenance. A digest downloaded beside
  a mutable release does not independently authenticate it. Bound the download
  before hashing, then extract only expected regular files without escaping paths.
- For a backend security fix, align source, built artifact, committed checksum,
  downloader default and minimum accepted backend version. Test a clean install,
  upgrade from the affected version and a stale preinstalled/local executable.
  [Bitwarden review](https://github.com/omacom/omarchy-plugin-marketplace/issues/3098#issuecomment-5744992291)
  found fixed source while the plugin still downloaded and accepted the old engine.

Record the backend/artifact identities alongside the candidate SHA. These are
release evidence checks, not capabilities proven by the static preflight script.

## Installation, loaded source and provenance — 24 September 2026

Preserve unmanaged commands, launchers, service files and destination directories.
Before replacement, establish that the target belongs to this installer and is
unchanged, or obtain explicit consent for the concrete conflict. Never use
unconditional `ln -sf`, copying or `rsync --delete` as an ownership check. Removal
must leave unrelated and user-modified files intact. Exercise fresh install,
repeat install, conflicting target, modified managed file and removal cases.
See [NetScope](https://github.com/omacom/omarchy-plugin-marketplace/issues/5619#issuecomment-5819540608)
and [MoErgo](https://github.com/omacom/omarchy-plugin-marketplace/issues/7107#issuecomment-5819566127).

For plugin update tools, a matching HEAD is not proof of the loaded tree. Refuse
updates to dirty checkouts, including untracked files, without deleting user
changes. Recheck the commit and complete loadable tree after checkout and before
validation/rescan; account for ignored executable source too. Preserve that
identity until loading. See [Plugin Updates](https://github.com/omacom/omarchy-plugin-marketplace/issues/8250#issuecomment-5801511763).

Pin one exact compiler/toolchain release consistently across toolchain files and
package recipes, then regenerate affected package metadata. A pinned source with
a moving `stable` compiler is still mutable. Provenance acceptance must bind the
artifact digest to the expected repository, trusted workflow and full source SHA;
an owner-only attestation check is too broad. Check before extraction/execution.
See [toolchain](https://github.com/omacom/omarchy-plugin-marketplace/issues/7631#issuecomment-5800962204)
and [attestation identity](https://github.com/omacom/omarchy-plugin-marketplace/issues/7107#issuecomment-5792174978).

Review required external setup instructions and copied commands as well as
plugin-launched execution. Moving a mutable download-to-shell command into the
UI does not authenticate the required backend. A checksum from the same movable
tag as a root bootstrap supplies no independent trust. See
[Omatalk](https://github.com/omacom/omarchy-plugin-marketplace/issues/8407#issuecomment-5818821005)
and [OmaNitro](https://github.com/omacom/omarchy-plugin-marketplace/issues/5540#issuecomment-5819470495).
