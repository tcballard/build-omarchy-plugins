# Acceptance evidence and remaining host checks

## Marketplace follow-up — 20 September 2026

- `./scripts/test`: all 58 unit tests passed, plus portable/plugin/adapter,
  version/contract, skill validation and packaging checks.
- New behavioral fixtures cover mutable/pinned Actions and reusable workflows,
  Docker action digests, local actions, permissions, comments, non-workflow docs
  and distributed agent configuration discovery. All signals remain advisory;
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
