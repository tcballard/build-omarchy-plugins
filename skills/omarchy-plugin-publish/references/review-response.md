# Preparing a useful response to marketplace review

Based on public HANCORE-linux reviews checked 12 September 2026. Review
requirements evolve; inspect the current issue and workflow before acting.

Keep a compact evidence table in the prepared response:

| Reviewer finding/link | Changed production path | Reproduction and result | Final full SHA |
| --- | --- | --- | --- |
| One row per outstanding finding | File/function and actual boundary | Command, exit status and meaningful observation | Same commit as validation |

Use this to show what changed, not to assert that a passing local scan compels
approval. Include unresolved items and unavailable live checks. Freeze the final
commit while requesting its baseline; a newer push invalidates evidence about
an older snapshot. Preserve the official form headings and acknowledgments.

Before opening anything, search by repository URL and plugin ID. Reuse an active
request. If the maintainer closed it and explicitly invited a fresh submission,
follow that direction and link the old review; do not silently treat all closed
issues as needing reopening. Distinguish superseded requests and failed catalog
publication from new plugin defects.

Review the **whole distributed checkout**. Recent reviews reject agent/session
control payloads such as `AGENTS.md`, `CLAUDE.md`, `HANDOFF.md` and equivalent
instructional artifacts in installable desktop plugins. Keep authoring-agent
configuration outside that distributed tree; ordinary user/developer docs are
not automatically equivalent. This concerns the desktop plugin being built,
not this agent-skills bundle, whose intended payload is instructions.
See [review #4744](https://github.com/omacom/omarchy-plugin-marketplace/issues/4744#issuecomment-5642689162).

For data, process or state findings, trace the actual producer-to-consumer path.
A downstream slice, path pre-check, timeout that leaves grandchildren alive, or
an absolute path to a mutable executable may leave the reported boundary open.
Verify the fix with an adversarial fixture relevant to that specific path.
