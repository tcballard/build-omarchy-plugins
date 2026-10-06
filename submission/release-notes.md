# Build Omarchy Plugins v0.8.0 — Start with the repo sorted

The plugin repository template now ships inside the skills bundle. Ask your
agent for a GitHub-ready bar widget and it can create the whole starting point
offline, with your project name, plugin ID and repository details already set.

- **The boring setup comes with it.** README, credits, licence, CI, issue and PR
  templates, release workflow and an optional GitHub policy setup command.
- **One reviewed starting point.** The bundled template is pinned to an exact
  commit and checked against file hashes before generation. Each new project
  records where it came from. Existing directories are never overwritten.
- **Use the bundle your way.** The starter travels with an individual scaffold
  skill install and the portable, Claude, OpenAI plugin and skills archives.
  The existing generator still supports all six plugin kinds.
- **Works from real install paths.** Generated projects handle folders with
  spaces and Windows paths. The new route needs Node.js 22+; no npm install or
  network access is needed to create the project.

All 77 toolkit tests and five new scaffold tests passed, with CI green across
Linux, macOS, and Windows. We also generated plugins from every installable
archive and ran a fresh-session scaffold exercise. That checks the tooling;
the plugin you build still needs testing on your Omarchy desktop.

The twelve provider-neutral skills retain OpenCode support, transactional
updates and an SPDX 2.3 SBOM. Release automation builds verified drafts and
cannot publish them. Creating a project does not create a remote repository,
apply GitHub settings or change your desktop.

Choose the archive for your host and check it against `SHA256SUMS`. For an
existing CLI installation, preview the update with `--update --diff`, then use
`--update`, keeping your usual installer target and scope.

Try: **“Create a GitHub-ready Omarchy bar-widget repository using the bundled
template.”**

[Full changes](https://github.com/tcballard/build-omarchy-plugins/compare/v0.7.0...v0.8.0)
