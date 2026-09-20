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
