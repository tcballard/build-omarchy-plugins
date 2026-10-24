# Acceptance evidence and remaining host checks

## Bundled repository template — 6 October 2026

- Implementation candidate: `94b0e749c07929de08854cd30af3d7c07f477b52` on base
  `93f68e47c2f0cc1e8ecc07e4d14c7b5a0e97ef05` (uploaded tree verified equal to
  the locally tested implementation tree).
  The template snapshot is `tcballard/omarchy-plugin-template` at
  `f99681e69937d21c2d4414ac9f65a0fd01fea714`; all 41 files are locked by hash
  and Git mode. No template runtime contract was changed.
- `./scripts/test` passed on Linux: 77 existing/extended Python tests plus
  five new Node scaffold tests, adapter parity, pinned contracts, skill
  structure, security scan, version checks and deterministic packaging.
- Generated projects worked from all four installable release archives and
  an individually installed scaffold skill. Added toolkit validation to each
  packaging/install generation case and reran all six release-artifact tests.
- An independent fresh-session scaffold exercise used a relocated copy of the
  skill, created the requested Focus starter and ran the generated and toolkit
  checks. [Unedited agent report and exact commands](runs/2026-10-06/repository-template.md).
  The prompt is recorded in HANDOFFS.md. This was a qualitative smoke exercise,
  not a comparative host/model evaluation; no independent model ID is claimed.
- The agent correctly noted that the generated template's initialization test
  returns early after initialization. The bundle's new end-to-end tests cover
  invalid input, existing destinations and corrupt/extra source assets instead
  of treating that generated test's reported pass as overwrite evidence.
- Two path-compatibility adjustments are applied only to generated copies;
  source provenance records them. Source checks and GitHub dry-run execution
  were tested in paths containing spaces. Remote matrix results belong to the
  final PR SHA; local evidence alone does not establish Windows/macOS execution.

Live Omarchy, native QML rendering, GitHub policy application and marketplace
acceptance remain unrun. No new release or installed personal-skill update is
included in this change.

## v0.7.0 preparation — 4 October 2026

- Recovered the 3 October work in local commits `11d7e9b` and `c2172ef`, based
  on published v0.6.1/main `f6e2f7c4957e284cfa10c91a69ac2d8962b6e20e`.
- `./scripts/test`: all 75 tests passed on the committed v0.7.0 candidate,
  including deterministic archives/checksums, opt-in capability rules,
  portable/OpenAI parity, version/contract validation and packaging.
- `python3 scripts/check_versions.py --tag v0.7.0` and `git diff --check` passed.
- Aligned portable, OpenAI, Claude and submission versions; README installation
  commands target the verified published v0.6.1 release until v0.7.0 is published.
- Added the architecture-rule handoff to workflow navigation and prepared
  release notes with the scanner and runtime evidence limits explicit.

This is local preparation evidence. Required GitHub CI belongs to the final PR
commit and is reported on the PR. No v0.7.0 tag or release is claimed. The earlier
forward-test record below is historical evidence, not a newly executed model
comparison. Live Omarchy rendering/lifecycle and installed-host checks remain
unrun; token savings remain unmeasured.


## v0.6.1 preparation — 29 September 2026

- Base: `ad917be03a37f8ec1b306f2c8243cdc8b53aa85c`.
- Retrieved all nine contract documents at the immutable commits in the updated
  ledger through the GitHub connector. Eight document digests are unchanged;
  Quattro's shell document changed. No moving branch content enters the bundle.
- Added five contract-monitoring tests for unchanged heads, moved heads with
  identical bytes, changed documents, missing/network-failed documents, and
  corrupt pins. Monitoring does not rewrite the ledger.
- A fresh, text-only subagent session used the supplied skills to answer two
  tasks: a service-backed widget losing data only under a replacement bar, and
  stale output after a `keepLoaded` service edit. It identified the service-less
  facade and retained instance, recommended explicit unavailability/restart,
  and rejected duplicate pollers and scene-traversal workarounds.
- This is a qualitative guidance smoke check, not a measured model comparison.
  The session inherited the parent model; no independently exposed model ID or
  runtime transcript artifact is claimed.
- Live Omarchy/bar compatibility and edit/restart scenarios remain unrun.
  Required CI and publication are separate gates; no release is claimed here.


## Marketplace follow-up — 24 September 2026

- Base: `2d618374ec13dd7a07efeb0cf69115fc9fa2c4e3`; contract and guidance
  changes recorded in `88c733e` and `bb2ccf0`, with this evidence/scenario update.
- `./scripts/test`: all 63 unit tests passed, plus canonical/OpenAI adapter,
  skill, version/contract, security and packaging checks on Linux.
- Submission regression exercises every pinned form tag and CLI alias, including
  VPN, and retains unknown-tag, duplicate-tag and over-limit rejection.
- Four marketplace documents were retrieved at immutable commit
  `bdf7c4fd1c0cb2bc1175dc0931362727aa4a0cb3`; ledger digests were calculated
  from those exact UTF-8 contents. The security document digest is unchanged.
- [Fresh local-helper exercise](runs/2026-09-24/local-helper.md) met its scoped
  criteria. Its raw fixture and digest are retained; this is not a full model
  benchmark or a runtime test of a repaired plugin.
- Loaded-tree/installer and standard-installation handoff cases are documented
  but unrun. No live Omarchy, Omakit or cross-platform runtime pass is claimed.
- Required remote CI must still run on the final PR SHA. No release, marketplace
  issue or installed personal-skill update is included.


## v0.5.0 preparation — 21 September 2026

- `./scripts/test`: all 59 unit tests passed, plus portable/plugin/adapter,
  skill, version/contract and packaging checks. The archive test compares two
  builds and validates checksums.
- `python3 scripts/check_versions.py --tag v0.5.0`: passed.
- `git diff --check`: passed; canonical and packaged skills remain synchronized.

This records local release-preparation evidence. Required CI must pass on the
final PR commit. After merge, build and attest final assets with the existing
Release draft workflow against the full merged main SHA and `v0.5.0`.
No v0.5.0 tag, draft assets or published release is claimed here. The new
behavioral scenarios, live desktop and installed-host upgrade checks remain
unrun. Omakit, the security skill and OmaVM remain optional recommendations;
no fresh companion runtime testing is claimed.

## v0.4.1 preparation — 20 September 2026

- `./scripts/test`: all 59 unit tests passed, with portable/plugin/adapter,
  skill, version/contract and packaging checks.
- `python3 scripts/check_versions.py --tag v0.4.1`: passed.
- Clean committed candidate packaging was built twice using
  `package_submission.py --require-clean --git-tree HEAD`. The two output
  directories were byte-identical; all eight `SHA256SUMS` entries passed.
- The five candidate archives cover portable skills, Agent Plugin, OpenAI adapter,
  Claude plugin and submission materials, with source/release manifests and
  SPDX 2.3 SBOM.
- Canonical/packaged skills are synchronized and `git diff --check` passed.

This is patch-release preparation, not publication. Required CI must bind the
final PR commit. After merge, rebuild and attest the final assets using the
existing Release draft workflow against the full merged main SHA and `v0.4.1`.
No v0.4.1 tag or release has been published by this preparation. New model
behavioral cases and live installed-host upgrade checks remain unrun.


## Marketplace follow-up — 20 September 2026

- `./scripts/test`: all 59 unit tests passed, plus portable/plugin/adapter,
  version/contract, skill validation and packaging checks.
- New behavioral fixtures cover mutable/pinned Actions and reusable workflows,
  Docker action digests, local actions, permissions, comments, non-workflow docs
  and distributed agent configuration discovery, plus large whitespace input. All signals remain advisory;
  the validator does not execute the payloads.
- Canonical skills and OpenAI packaged copies were synchronized.
- `git diff --check` passed.

These are local tooling checks, not live Omarchy execution, independent model
behavioral evaluation, GitHub CI or a published release. New integration cases in
HANDOFFS.md remain unrun. No desktop access is required for this guidance/linter
change. Version and upstream contract pins are unchanged.


## v0.4.0 preparation — 14 September 2026

- `./scripts/test`: all 55 unit tests and portable/plugin/adapter validation,
  version and contract checks, security scan and packaging checks passed locally.
- Clean candidate packaging produced all five v0.4.0 archives and source/release
  manifests, SPDX SBOM and checksums; all eight checksum entries passed.
- Includes the README badge-layout work from PR #23 and clarifies that
  compatibility refers to the installed version reported by `omarchy-version`.

This is preparation evidence. Required GitHub CI must pass on the final PR
commit; tagged, attested assets must be rebuilt from reviewed main. No v0.4.0
release has been published. The existing unpublished v0.3.2 draft is superseded
by this candidate's scope but has not been deleted or retagged.

Fresh Astra/Fable behavioral runs, handoff evaluations, live Omarchy desktop
acceptance and a real v0.3.1-to-v0.4.0 host upgrade remain unrun.

## v0.3.2 preparation — 13 September 2026

Executed locally for the release-preparation candidate:

- `./scripts/test`: all 55 unit tests and portable/plugin/adapter validation,
  version and contract checks, security scan and packaging checks passed.
- `python3 scripts/package_submission.py --require-clean`: produced all five
  v0.3.2 archives plus release/source manifests, SPDX SBOM and checksums.
- `sha256sum --check SHA256SUMS`: all eight listed files passed.

These are candidate checks, not publication evidence. GitHub's `CI / Required`
result must bind the final PR commit; the release workflow must rebuild and
attest assets from the reviewed merged main commit. No v0.3.2 tag or release
was created during bookkeeping.

Fresh Astra/Fable behavioral sessions, the cases in [HANDOFFS.md](HANDOFFS.md),
live Omarchy acceptance and a real v0.3.1-to-v0.3.2 host upgrade smoke test
remain unrun in this pass. Earlier Claude CLI and desktop-related evidence
below belongs to v0.3.1 and is not a fresh v0.3.2 result.

## Historical v0.3.1 evidence — 12 September 2026

v0.3.1 release candidate, 12 September 2026. The release version is owner-selected.
The checks below distinguish portable validation from provider and desktop
execution; they do not imply these changes are in the published v0.3.0 assets.

## Executed in this workspace

- Official Claude Code CLI **2.1.269**: strict validation of both
  `.claude-plugin/marketplace.json` (via repository path) and
  `.claude-plugin/plugin.json` passed without warnings.
- Generated an isolated `bar-widget` with ID `io.github.example.acceptance`,
  author Example, and `--no-git`; generated `tests/run` passed.
- Canonical validator `--json --security` completed successfully on that fixture.
- Prepared a fictional submission with category `Kids`, tags `education` and
  `games`: emitted canonical `Education, Games` form labels. No issue was opened.

- Repository checks: 54 unit tests plus validators, version/contract checks and
  adapter synchronization passed; artifact tests compare two independent builds.

These exercise packaging and portable tooling, not model behavior or the real
Quattro desktop. The ten existing behavioral cases remain in `README.md` and
retain their earlier reported smoke-test limits.

## Checks requiring a provider session or Omarchy desktop

| Check | Status | Evidence needed to close |
| --- | --- | --- |
| Fresh Astra baseline/candidate behavioral suite | Not run in this task | Fresh model sessions, exposed model ID/settings, fixture hashes, transcripts/patches and evaluator judgments. |
| Fresh Fable baseline/candidate behavioral suite | Blocked: no authenticated Fable runner available | Same evidence in an actual Fable session; installing the Claude CLI is not a model run. |
| Live Omarchy end-to-end acceptance | Blocked: no Omarchy shell/display available | Runtime validation, installation, interaction, removal and logs on the supported desktop. |

## Reproducible live acceptance exercise

On a disposable Omarchy test account, from a reviewed bundle checkout:

1. Generate the same fixture using `new_plugin.py --id io.github.example.acceptance
   --name Acceptance --author Example --kind bar-widget --output /absolute/test/path`.
2. Run its `tests/run` and `omarchy plugin validate /absolute/test/path`; record
   the bundle commit, generated-tree digest, Omarchy/Quickshell versions and logs.
3. Use the current host's supported local development loading path. Observe
   horizontal/vertical placement and multiple monitors where available; record
   any unavailable configuration explicitly. Exercise its click behavior.
4. Reload, disable and remove it; verify no leftover widget/service or changes
   to unrelated configuration. Preserve the exact commands and screenshots.
5. Prepare the submission locally. Confirm actual license, install/removal
   instructions, dependencies and preview provenance before any owner
   attestations. Do not submit this fictional acceptance fixture.

For reviewer-guidance behavioral coverage, add fresh fixtures with external text
in a shared QML control, an oversized response checked only after collection,
and an agent-control handoff in the desktop-plugin checkout. Ask for the narrow
fix, preserve the initial bytes and inspect the production boundary and truthful
verification report. These are proposed cases, not recorded passes.


## Marketplace and abstraction refresh — 3 October 2026

Executed on the local Linux/Python 3.12 runtime:

- `./scripts/test`: all 75 tests and portable plugin/skill/version/contract,
  security, adapter-parity and packaging checks passed. Six added regression
  tests cover generated literal Text sinks, nested JS, each selectable policy,
  unscannable source, invalid policy names and separation from unselected
  advisory findings. These source checks do not prove actual Qt rendering.
- Skill-creator validation ran against the writable personal skill directories;
  all twelve skill frontmatters passed.
- An isolated fresh agent used the scaffold/test skills to build a panel/menu
  Reading fixture with summon titles and no direct QML/JS networking or dynamic
  code. Portable checks and 13 production-parser cases passed. A deliberately
  inserted nested JS file triggered both chosen policy errors and failed the CI
  entry point; removal restored success. The updated external validator returned
  0 on the clean fixture and 1 with the violation, both with and without explicit
  `--security`.
- Forward-test discovery: a copied scanner matched its own Cargo-rule prose and
  predicate text, initially exiting 2 under `--security`. The temporary fixture
  agent reformatted those strings without changing its predicates, then verified
  the fixture independently with the installed external validator. This is a
  limitation of lexical discovery, not evidence that copying scanners is safe.
  Guidance now recommends an external trusted validator and explicitly explains
  self-matches; no production scanner rule was weakened. A separate regression
  verifies deny-only does not promote unrelated advisory findings into errors.

Forward-test fixture digest (reported by the isolated agent):
`a25e033a1b4b81fd89d70a015adbb687a13400d7a0ad86054e6999c527543d9d`.
This is one local agent exercise, not a controlled multi-model comparison or
measurement of token savings. The fixture/report are temporary evaluation data.
Live Omarchy/Quickshell rendering, IPC/lifecycle, install/remove, Omakit baseline,
hardware behavior and a new release remain unrun. Provider CI results are
reported separately on the associated PR rather than inferred from local checks.
