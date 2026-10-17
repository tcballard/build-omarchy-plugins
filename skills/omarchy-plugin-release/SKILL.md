---
name: omarchy-plugin-release
description: Preflight and prepare a versioned Omarchy plugin release from a public Git repository. Use for readiness, version and tag alignment, CI, install/update/removal evidence, preview, dependencies, checksums and assets; marketplace issue creation belongs to the publish skill.
---

# Prepare an Omarchy plugin release

Reconcile candidate source, version, tests and preview provenance. Resolve `<skill-dir>` to this skill's directory:

```bash
python3 "<skill-dir>/scripts/release_preflight.py" /absolute/path/to/plugin
```

Read [release contract](references/release-contract.md) before tagging or publishing; read [preflight options](references/preflight-options.md) for renamed skill paths, tagged candidates and historical asset audits. A missing trusted validator remains a failed prerequisite.

- Bind root manifest version, notes, tested commit, tag and assets to the same candidate. Require a clean tree for release; never move a published tag.
- Verify the core journey, failures/recovery, official validation, live lifecycle, fresh installation, upgrade and removal on claimed Omarchy versions/architectures. Previous config/state fixtures must preserve settings or exercise a documented migration.
- Document dependencies, authentication, network, processes, writes and removal residue. Keep install/removal instructions symmetric and UI previews reproducible.
- Block readiness on unresolved security, data-loss or core-function failures. Describe tolerable non-core limitations and restrict support claims to observed evidence; no arbitrary waiting period or preview exemption applies.

Finish authorized preparation even when a host gate remains unrun. Publish only within the user's authorization; preparation does not imply publication. Report exact candidate/version/tag/asset identities, completed deliverables and unresolved gates. Preflight success alone does not mean a tag or release was published.
