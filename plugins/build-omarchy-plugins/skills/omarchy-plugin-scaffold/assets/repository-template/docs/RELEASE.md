# Prepare a release

The included workflow creates a **draft source release**. It never publishes a marketplace listing or promises a prebuilt installer.

1. Finish the feature and replace starter copy. Confirm licences and asset rights.
2. Run portable and native checks. On Omarchy record the exact installed version, commands, results, source commit and limitations in docs/ACCEPTANCE.json. Set status to passed only after actual acceptance. Record this in a subsequent documentation-only commit.
3. Update VERSION and any manifest/Cargo/package version before testing. Commit, tag the accepted candidate, and push the tag.
4. Run **Release source** from Actions with that existing tag. The source archive preserves the complete tracked project, including development checks. Installed runtime packages must use an explicit file allowlist and exclude authoring instructions, blueprint files and workflow files.
5. Review the draft release, write outcome-focused notes and publish when ready.

The archive script refuses uninitialized projects, dirty checkouts, version/tag mismatches and runtime changes after recorded acceptance. For installable plugin archives, include only the declared QML/runtime dependencies, manifest and licence. For apps, build and test architecture-specific binaries separately; do not label a source tarball as an installer. For packages, record clean Arch build and install/upgrade/removal results before submission.
