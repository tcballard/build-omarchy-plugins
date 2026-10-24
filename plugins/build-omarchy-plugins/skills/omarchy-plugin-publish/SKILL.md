---
name: omarchy-plugin-publish
description: Prepare or submit an Omarchy plugin marketplace issue, and respond to listing review or updates. Use for current form, category, tags, exact issue body, owner attestations and reviewed SHA; use release for versioned assets and test for validation evidence.
---

# Prepare or submit an Omarchy marketplace listing

Read [marketplace submission](references/marketplace-submission.md) for the pinned contract. Before a remote submission/update, verify the current official destination, form, trigger and target SHA. If upstream is unavailable, prepare a draft and mark the contract unverified.

Inspect the root manifest, README, licence, preview and release evidence. Require public source, permanent non-`omarchy.*` ID, dependencies and install/removal instructions. Reconcile release preflight findings with actual code; compatibility checks do not settle security review.

Resolve `<skill-dir>` to this skill's directory to draft without publishing:

```bash
python3 "<skill-dir>/scripts/prepare_submission.py" \
  --plugin-dir /absolute/path/to/plugin --category "Developer Tools" \
  --tag quickshell --tag bar
```

Read [review response](references/review-response.md) for findings, exact-SHA consistency, duplicates and distributed payloads. Read [submission options](references/submission-options.md) for optional baseline tooling and update distinctions. Use existing authenticated capabilities; never extract or copy credentials.

Show the exact title/body, destination and candidate. Obtain owner confirmation of checklist attestations unless explicitly supplied already; preparing a listing does not establish ownership or authorize posting. Follow the maintainer's update/resubmission mechanism rather than opening duplicates or guessing triggers.

For preparation, return the draft and unresolved evidence/attestations. For authorized submission, read back the issue and report URL/status. Listing, exact-snapshot verification and current upstream are separate states; submission is not approval or a security audit.
