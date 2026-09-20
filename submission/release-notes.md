# Build Omarchy Plugins v0.4.1

A patch release that turns recent Omacom marketplace feedback into more useful
build guidance and preflight checks across the twelve-skill provider-neutral bundle.

## What's changed

- Review the full dependency chain: pinned Actions and executable images,
  transitive dependency locks, and the installer paths that actually consume them.
- Cover agent prompt injection and private-data exposure, hosted OAuth brokers,
  and independently trusted privileged installation.
- Check that backend fixes reach release artifacts, downloader defaults and
  minimum accepted versions, including upgrades from an affected installation.
- Add concrete guidance for bounded image decoding and aggregate stream/transfer
  budgets, including missing-decoder and missing-isolation failure behavior.
- Add advisory workflow and agent-configuration discovery. Interpret command
  strings in bundled validators separately from real setup/runtime behavior.
- Keep workflow scanning responsive on long runs of blank lines.
- Clarify plugin/theme ownership and keep installed references self-contained.

Canonical skills and the OpenAI adapter carry the same guidance. The skill names,
supported hosts and upstream contract pins are unchanged.

## Verification and limits

The candidate passes 59 portable unit tests plus skill/plugin validation,
version/contract checks, adapter synchronization and packaging checks. CI tests
Linux, macOS, and Windows across Python 3.11–3.13, workflow lint and Claude packaging.
See the [acceptance record](https://github.com/tcballard/build-omarchy-plugins/blob/v0.4.1/evals/ACCEPTANCE.md)
for observed candidate evidence and remaining checks.

The new checks are advisory static discovery, not a full YAML parser, dependency
provenance proof, marketplace approval or security audit. The new agent behavioral
scenarios are documented but unrun. No fresh live Omarchy desktop or installed-host
upgrade test is claimed.

Release automation builds twice, compares bytes, generates provenance and verifies
downloaded draft assets. Final release artifacts must be rebuilt from the reviewed
merged commit after required CI passes. The workflow cannot publish a release; publication
remains owner-controlled.

## Installation and update

The transactional installer continues to support Codex, Claude Code, Cursor,
Gemini CLI and OpenCode.

Choose the skills, portable Agent Plugin, OpenAI adapter or Claude plugin archive
for your host and verify it against `SHA256SUMS`. Source/release manifests and the
SPDX 2.3 SBOM identify the packaged source. Use either the Claude plugin or the
Claude skills installer to avoid duplicate skill loading.

Once v0.4.1 is published, existing installations can preview the update from its
checkout using `python3 scripts/install_agent_skills.py --update --diff`, then
apply it with `--update`, preserving the existing host target and scope. Resolve
locally modified managed files explicitly. No marketplace listing is implied.
