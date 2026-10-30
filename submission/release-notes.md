# Build Omarchy Plugins v0.10.0: Keep private data private

I pulled another round of marketplace lessons into the skills: handling private text, testing upgrades and checking what QML actually displays. The skill entry points grow by three lines. The detail stays in linked references.

- **Send private text through stdin.** A copyable reader accepts bounded JSON and rejects malformed input without echoing it. The guidance follows messages and filenames through helper subprocesses too.
- **Exercise upgrades from affected state.** Small fixtures cover private files, saved network profiles and managed services. Adapt them to your plugin's production migration and check that unrelated user data survives.
- **Make plain-text rendering explicit.** An optional QML check requires literal PlainText bindings, with named exceptions for reviewed rich text such as a bundled licence. It rejects expressions masquerading as literal PlainText and ambiguous exception IDs.
- **Generate leaner checkouts.** New repositories omit agent instruction files from both the checkout and retained blueprint. Developer docs remain, and cloning or rerunning initialization still works.

Validation passed: 89 Python tests and six Node scaffold cases, with one optional Qt test skipped. Required CI covers Linux, macOS, and Windows. The separate Qt 6.8.3 rendering fixture passed and remains optional. The lexical check cannot prove safety; live Omarchy and Quickshell lifecycle acceptance remains unrun.

Same twelve provider-neutral skills, OpenCode support, transactional updates and SPDX 2.3 SBOM. The pinned starter and marketplace contracts are unchanged. Release automation prepares verified drafts and cannot publish them.

For an existing CLI install, check out `v0.10.0`, preview `--update --diff`, then apply `--update` with your usual target and scope. Check downloaded archives against `SHA256SUMS`.

[Full changes](https://github.com/tcballard/build-omarchy-plugins/compare/v0.9.0...v0.10.0)
