# Acceptance evidence and remaining host checks

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
