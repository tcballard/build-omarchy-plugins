# Build Omarchy Plugins v0.3.0

Twelve Omarchy skills, revised for Astra and Claude Fable: clearer instructions
for capable models, with the desktop contracts they still need to get right.

Sometimes the agent stopping halfway through is following exactly what the
instructions accidentally asked for. This release takes a closer look at those
instructions.

- Requested builds continue past the design note. Existing approval and settled
  decisions carry forward, while diagnosis-only requests stay read-only.
- Small fixes get focused edits and relevant checks. Required repository and
  release checks still apply; missing desktop access is reported honestly.
- Bundled helpers resolve from the loaded skill directory. Workbench
  registration is optional, and an example no longer dictates repository layout.
- Host-conformance text output no longer crashes. Codex discovery now checks
  parent directories and reports duplicate skill names without inventing a winner.
- Ten behavioral cases cover builds, repairs, scope, continuity and evidence.

The bundle stays provider-neutral. Use the same skills with Codex, Claude Code,
Cursor, Gemini CLI or OpenCode; choose the model in your agent. Existing
transactional updates, reproducible archives, checksums and SPDX 2.3 manifests
are retained. Release automation prepares a verified draft and cannot publish it.

All 52 tests pass, with CI across Linux, macOS, and Windows. The Astra and Fable
reviews use their providers' official guidance. Actual Fable model execution and
live Omarchy desktop testing remain outstanding; this is not a claim of measured
model performance gains.

If a skill still makes your agent stop unnecessarily, overbuild a small fix or
reopen a settled decision, please open an issue with the prompt and what happened.
