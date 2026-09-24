# Build Omarchy Plugins v0.5.1 — fewer repeat mistakes

I went back through the marketplace reviews and fed the lessons into the bundle.
Your agent now gets clearer guidance on the things that keep sending plugins
back for fixes.

- Updated submission rules, including the VPN tag and standard-installation review path.
- Stronger guidance for local APIs, safe updates and installers that preserve user files.
- More specific checks for pinned toolchains, stalled downloads and processes that survive cancellation.
- Fixes for multiselect validation and release helpers installed in separate directories.

All 63 local tests passed. That covers the bundle's tooling and packaging; it
doesn't certify the plugins you build with it. One fresh-agent exercise checked
the revised local-helper guidance. Other new scenarios and live Omarchy testing
remain unrun.

Choose the skills, portable Agent Plugin, OpenAI adapter or Claude plugin archive
for your host, and verify its download against `SHA256SUMS`.

For an existing installation, preview the update with
`python3 scripts/install_agent_skills.py --update --diff`, then apply with
`--update`, keeping your existing host target and scope.

The provider-neutral bundle supports OpenCode and other skill hosts. Updates remain transactional, with CI across Linux, macOS, and Windows and an SPDX 2.3 software bill of materials. Release automation can prepare a draft but cannot publish it.

[Full changes](https://github.com/tcballard/build-omarchy-plugins/compare/v0.5.0...v0.5.1)
