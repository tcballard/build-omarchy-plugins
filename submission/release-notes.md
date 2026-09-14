# Build Omarchy Plugins v0.4.0

This release brings consistent Omarchy branding and compatibility guidance to
the twelve-skill provider-neutral bundle. It also includes the marketplace preflight and workflow
fixes prepared for the unpublished v0.3.2 draft.

## What's changed

- Commit-pinned identity/category and compatibility badges, with the official
  Omarchy icon, plus a compact README row ordered CI, licence, identity and
  compatibility. The bundle's own README now uses the layout.
- `Omarchy | 4.0.0+` means the installed Omarchy version reported by
  `omarchy-version`. Projects must declare and test their own supported range;
  the badge is not a marketplace approval or universal compatibility claim.
- Badge categories pair with consistent GitHub topics to help people find
  Omarchy projects. Canonical guidance and the OpenAI adapter stay synchronized.
- Privilege advisories catch `sudo` and `pkexec` in negated README prose as well
  as commands. Review guidance separates documentation matches from execution,
  compatibility checks, security review, approval and publication.
- The marketplace security policy is pinned, and workflow handoff cases cover
  completing agreed builds, candidate drift and marketplace feedback.

## Verification and limits

Portable validation covers 55 unit tests, generated-plugin tooling, synchronized
adapters and deterministic archive builds. Required CI includes nine
OS/Python combinations across Linux, macOS, and Windows, workflow lint and
strict Claude packaging validation. Candidate results are recorded in the
[acceptance record](https://github.com/tcballard/build-omarchy-plugins/blob/v0.4.0/evals/ACCEPTANCE.md).

The privilege check is deliberately broader than the upstream matcher. A warning
is neither proof of execution nor a security finding. Passing portable checks
is not marketplace approval or a security audit.

Fresh Astra/Fable behavioral runs, the documented handoff evaluations and live
Omarchy desktop acceptance remain outstanding. This bookkeeping pass does not
claim a fresh-install or v0.3.1-to-v0.4.0 host upgrade smoke test.

Release automation builds twice, checks byte equality, generates provenance and
verifies downloaded draft assets. The workflow cannot publish a release;
publication remains owner-controlled. Final artifacts must be rebuilt from the
reviewed merged commit after its required CI passes.

## Installation

The transactional installation and updates remain supported for Codex, Claude Code,
Cursor, Gemini CLI and OpenCode.

Choose the skills, portable Agent Plugin, OpenAI adapter or Claude plugin archive
for your host; verify it against `SHA256SUMS`. Use either the Claude plugin or
the Claude skills installer to avoid duplicate skill loading. The submission
archive contains reviewer materials. Source manifests and the SPDX 2.3 SBOM bind
the archives to the release source tree.

Once v0.4.0 is published, existing installations can preview and apply the update
from its checkout with `install_agent_skills.py --update --diff` and then
`--update`, preserving their existing target and scope. Locally modified managed
files require explicit resolution. No official OpenAI or Anthropic marketplace
listing is implied.
