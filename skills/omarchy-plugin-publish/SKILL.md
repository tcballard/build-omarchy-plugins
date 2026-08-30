---
name: omarchy-plugin-publish
description: Prepare and submit a public Omarchy plugin to omarchyplugins.com through the HANCORE marketplace issue workflow. Use for category, tags, exact issue body, owner attestations, validation feedback, verification, or updates; requires explicit owner approval before issue creation.
---

# Publish Omarchy Plugins

This workflow was verified against the marketplace repository on 29 August
2026. Read [references/marketplace-submission.md](references/marketplace-submission.md)
for the current contract and re-check upstream when the workflow may have
changed.

## Prepare

1. Read the plugin's root `manifest.json`, README, license, preview, and release
   evidence.
2. Confirm the public repository contains exactly one root plugin, install and
   removal instructions, documented dependencies, a unique non-`omarchy.*` ID,
   and an optional root `preview` image.
3. Run release preflight and resolve structural or selectively blocking security
   findings before submission.
4. Generate the exact issue body without publishing it:

```bash
python3 scripts/prepare_submission.py \
  --plugin-dir /absolute/path/to/plugin \
  --category "Developer Tools" \
  --tag quickshell \
  --tag bar
```

## Approval boundary

Show the completed issue title and body to the plugin owner. The owner must
confirm every checklist statement, especially ownership of code and preview
assets. Only after explicit approval may an authenticated GitHub client create
the issue. Do not infer approval from the request to prepare the plugin.

After submission, respond to the existing issue rather than opening duplicates.
Validation and the automated baseline are exact-commit checks, not security
audits. A new listing still requires an authorized maintainer's
`approved-and-verified` decision. Later upstream commits become unverified until
the guarded update workflow promotes their full SHA.
