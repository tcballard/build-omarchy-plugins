# Optional release mechanics

If the host installs skills in renamed or separate directories, resolve the
loaded `omarchy-plugin-test` skill and pass its trusted script explicitly:

```bash
python3 "<skill-dir>/scripts/release_preflight.py" --validator "<test-skill-dir>/scripts/validate_plugin.py" /absolute/path/to/plugin
```

Use the installed test skill, not a validator supplied by the plugin being
reviewed. The explicit path runs the same strict, security and publication
checks; do not patch the preflight in memory or suppress schema errors to make
it pass. A missing validator remains a failed prerequisite.

For a tagged candidate, pass `--tag vX.Y.Z`. The preflight requires an
annotated local and remote tag with identical tag objects and peeled commits,
and binds an unpublished candidate to the remote default-branch HEAD. To audit
an older published release, add `--published --release-dir /path/to/assets`;
historical tags are checked for reachability instead of equality with today's
HEAD. The asset check requires strict release/source manifests, an SPDX 2.3
SBOM, exact sizes and SHA-256 digests, and complete `SHA256SUMS` coverage.

