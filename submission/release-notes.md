# Build Omarchy Plugins v0.3.2

This patch catches a marketplace review warning that our local preflight missed,
and clarifies how evidence passes between the twelve provider-neutral skills.
It retains native Claude Code packaging and transactional installation/update
support for Codex, Claude Code, Cursor, Gemini CLI and OpenCode.

## What's changed

- The privilege advisory now reports `sudo` and `pkexec` references even in
  negated README prose. This catches the Markets “never requests sudo” case
  and avoids hiding real commands beside negative prose.
- Review guidance distinguishes documentation-only matches from execution and
  separates compatibility success, security review, approval and publication.
  Real capability disclosures must remain intact; a wording change needs fresh
  evidence at its new commit.
- The marketplace security policy is pinned with an immutable source and digest.
  Portable skills and the OpenAI adapter contain the same updated guidance.
- Workflow navigation and handoff cases cover completing agreed builds,
  checking the actual working tree, candidate drift and marketplace feedback.

## Verification and limits

Portable validation covers 55 unit tests, generated-plugin tooling, synchronized
adapters and deterministic archive builds. Required CI includes nine
OS/Python combinations across Linux, macOS, and Windows, workflow lint and
strict Claude packaging validation. Candidate results are recorded in the
[acceptance record](https://github.com/tcballard/build-omarchy-plugins/blob/v0.3.2/evals/ACCEPTANCE.md).

The privilege check is deliberately broader than the upstream matcher. A warning
is neither proof of execution nor a security finding. Passing portable checks
is not marketplace approval or a security audit.

Fresh Astra/Fable behavioral runs, the documented handoff evaluations and live
Omarchy desktop acceptance remain outstanding. This bookkeeping pass does not
claim a fresh-install or v0.3.1-to-v0.3.2 host upgrade smoke test.

Release automation builds twice, checks byte equality, generates provenance and
verifies downloaded draft assets. The workflow cannot publish a release;
publication remains owner-controlled. Final artifacts must be rebuilt from the
reviewed merged commit after its required CI passes.

## Installation

Choose the skills, portable Agent Plugin, OpenAI adapter or Claude plugin archive
for your host; verify it against `SHA256SUMS`. Use either the Claude plugin or
the Claude skills installer to avoid duplicate skill loading. The submission
archive contains reviewer materials. Source manifests and the SPDX 2.3 SBOM bind
the archives to the release source tree.

Once v0.3.2 is published, existing installations can preview and apply the update
from its checkout with `install_agent_skills.py --update --diff` and then
`--update`, preserving their existing target and scope. Locally modified managed
files require explicit resolution. No official OpenAI or Anthropic marketplace
listing is implied.
