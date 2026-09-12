# Build Omarchy Plugins v0.3.1

This patch release turns recurring Omarchy marketplace review feedback into
targeted authoring guidance, and adds native Claude Code plugin packaging.
The same twelve canonical skills remain provider-neutral across Codex, Claude
Code, Cursor, Gemini CLI and OpenCode. Existing transactional installation and
update safeguards are retained.

## What's changed

- Native Claude plugin and community-marketplace manifests, a dedicated Claude
  archive, and strict official Claude CLI validation in required CI.
- Guidance for limiting data before collection, rendering external QML text as
  plain text, preserving file and executable identity, cleaning up child
  processes, and keeping credentials out of arguments and logs.
- Advisory discovery checks for QML inputs and agent-control payloads, plus a
  reviewer-response table connecting findings to fixes, reproductions and the
  exact submitted commit. Static checks do not certify plugin security.
- Updated Omacom submission forms, including Kids/Education and current tag
  labels, with compatibility for existing CLI spellings.
- Installation and stewardship documentation, aligned version metadata, and a
  release workflow that can create a new annotated tag after verifying the
  expected main commit and its required CI result.

## Research and verification

The [marketplace findings report](https://github.com/tcballard/build-omarchy-plugins/blob/v0.3.1/docs/reviews/2026-09-12-marketplace-findings.md)
draws on 6,531 issue/PR records and 30,036 comments, including 6,286 comments by
HANCORE-linux across 3,589 threads. Every collected record was indexed and
representative reviews were read in depth. This was not an independent source
audit of every plugin; overlapping topic counts include resolved findings.

Portable validation covers 54 unit tests, generated-plugin tooling, synchronized
adapters and deterministic archive builds. Required CI includes nine
OS/Python combinations across Linux, macOS, and Windows, workflow lint and
strict Claude packaging validation.
Release automation builds twice, checks byte equality, generates provenance and
verifies downloaded draft assets before owner publication. The workflow cannot publish
a release; publication remains owner-controlled.

Fresh Astra/Fable behavioral sessions and live Omarchy desktop acceptance remain
outstanding. Packaging validation does not establish model performance or live
desktop compatibility. See the
[acceptance record](https://github.com/tcballard/build-omarchy-plugins/blob/v0.3.1/evals/ACCEPTANCE.md).

## Installation

Choose the skills, portable Agent Plugin, OpenAI adapter or Claude plugin archive
for your host; verify it against `SHA256SUMS`. Use either the Claude plugin or
the Claude skills installer to avoid duplicate skill loading. The submission
archive contains reviewer materials. Source manifests and the SPDX 2.3 SBOM bind
the archives to the release source tree.

Existing installations can preview and apply the update from a v0.3.1 checkout
with `install_agent_skills.py --update --diff` and then `--update`, preserving
their existing target and scope. Locally modified managed files require explicit
resolution. No official OpenAI or Anthropic marketplace listing is implied.
