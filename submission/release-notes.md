# Build Omarchy Plugins v0.5.0

Find what already exists. Build the smallest useful change. Know what needs to
pass before you publish.

v0.5.0 is the next planned release, bringing the Sunday Social discussion into
the provider-neutral bundle's design, implementation, testing and publishing guidance.

## What's changed

- **Look before building.** Agents compare existing plugins and consider using,
  contributing, extending or forking before starting another repository.
- **Plan for the intended destination.** Personal tweaks stay small. Marketplace
  projects consider submission requirements during design.
- **Use the community's tools.** Omakit is recommended for Run/Store helpers,
  local checks and submission drafts. The community security skill and OmaVM
  are optional companions for review and clean-desktop testing.
- **Make readiness concrete.** Check the core user journey, upgrades from saved
  configuration, recovery and each claimed CPU architecture. Work from examples
  and test the behavior being changed.
- **Keep submission evidence current.** Verify the official workflow and exact
  candidate SHA. An announcement of a new marketplace is not its specification.

Thanks to the Sunday Social participants for describing where plugin development
still gets awkward, and to the maintainers building tools to help.

## Verification and limits

The candidate is checked with the portable test and packaging suite. See the
[acceptance record](https://github.com/tcballard/build-omarchy-plugins/blob/main/evals/ACCEPTANCE.md)
for observed results. The new behavioral evaluation scenarios remain unrun;
external companions have not been runtime-tested as part of this release prep.
Passing local checks does not establish live Omarchy behavior or marketplace
approval. Companion tools remain optional and are not installed by this bundle.

Version metadata and distribution names target 0.5.0. Required CI must pass on
the merged release commit before the existing release workflow builds, compares,
attests and verifies draft assets. This preparation does not publish a release.

CI covers Linux, macOS, and Windows across Python 3.11–3.13, plus workflow
lint and Claude packaging. The release workflow cannot publish; final
publication remains owner-controlled. Archives include source/release manifests
and an SPDX 2.3 SBOM.

## Installation and update

The transactional installer supports Codex, Claude Code, Cursor, Gemini CLI
and OpenCode.

Once v0.5.0 is published, choose the skills, portable Agent Plugin, OpenAI adapter
or Claude plugin archive for your host and verify it against `SHA256SUMS`.
From its checkout, preview an existing installation update with
`python3 scripts/install_agent_skills.py --update --diff`, then apply it with
`--update`, preserving your host target and scope. Resolve locally modified
managed files explicitly. Use either the Claude plugin or the Claude skills
installer to avoid duplicate skill loading.
