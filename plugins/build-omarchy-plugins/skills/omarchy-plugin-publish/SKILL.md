---
name: omarchy-plugin-publish
description: Prepare and submit a public Omarchy plugin to omarchyplugins.com through the HANCORE marketplace issue workflow. Use for category, tags, exact issue body, owner attestations, validation feedback, verification, or updates; requires explicit owner approval before issue creation.
---

# Publish Omarchy Plugins

This workflow was verified against the marketplace repository on 29 August
2026. Read [references/marketplace-submission.md](references/marketplace-submission.md)
for the pinned contract. Before an actual submission or update, verify the
current upstream form, destination, and target commit. If upstream is
unavailable, prepare a draft and mark its contract as unverified; do not claim
the dated snapshot is current.

## Prepare

1. Read the plugin's root `manifest.json`, README, license, preview, and release
   evidence.
2. Confirm the public repository contains exactly one root plugin, install and
   removal instructions, documented dependencies, a unique non-`omarchy.*` ID,
   and an optional root `preview` image.
3. Run release preflight and resolve structural or selectively blocking security
   findings before submission.
4. Generate the issue body without publishing it. Resolve `<skill-dir>` to the
   directory containing this loaded `SKILL.md`:

```bash
python3 "<skill-dir>/scripts/prepare_submission.py" \
  --plugin-dir /absolute/path/to/plugin \
  --category "Developer Tools" \
  --tag quickshell \
  --tag bar
```

## Approval boundary

Show the completed issue title and body to the plugin owner. The owner must
confirm every checklist statement, especially ownership of code and preview
assets. Reuse explicit approval already given for this body and its attestations;
otherwise obtain it before an authenticated GitHub client creates the issue.
Do not infer approval from a request to prepare the plugin or invent owner
attestations. Explain any material change to an approved body before submitting.

After submission, respond to the existing issue rather than opening duplicates.
Validation and the automated baseline are exact-commit checks, not security
audits. A new listing still requires an authorized maintainer's
`approved-and-verified` decision. Later upstream commits become unverified until
the guarded update workflow promotes their full SHA.
