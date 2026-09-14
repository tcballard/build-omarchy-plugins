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

## Compatibility success and documentation-triggered review

Checked 13 September 2026 against marketplace commit
`55efec9646cc24ca3ae8c427440043fa745ada49` and the two bot reports on
[Markets update #6586](https://github.com/omacom/omarchy-plugin-marketplace/issues/6586).
The [compatibility report](https://github.com/omacom/omarchy-plugin-marketplace/issues/6586#issuecomment-5648889073)
passed, while the [security report](https://github.com/omacom/omarchy-plugin-marketplace/issues/6586#issuecomment-5648899465)
required privilege review solely for README prose: “This plugin never requests
sudo, installs packages, starts a systemd service,”. There were no findings.

Read compatibility, security disposition, maintainer approval and publication
as separate states for the same full SHA. “Ready for verified update review”
does not mean approved or published; the existing snapshot stays unchanged
until publication succeeds. `review-required` does not itself demand a code fix.

Inspect the cited lines, surrounding documentation and relevant runtime paths.
The root README is scanned too. Upstream recognizes specific negation phrases,
not arbitrary English: `No sudo or pkexec is required.` is a documented example;
`never requests sudo` was not recognized in this report. Our advisory validator
intentionally flags either wording so that it cannot silently dismiss a command
near a negation. It is broader than the upstream privilege matcher.

If inspection confirms documentation-only evidence, prepare an explanation for
the existing review with the exact path and SHA. Alternatively, clarify truthful
prose (for example, `Runs with your normal user permissions.`), preserving the
actual dependencies, installation commands and privilege disclosures. Never
hide real commands, relocate runtime files to scan exclusions, or remove real
capability documentation to obtain a pass. A wording change creates a new
candidate: rerun affected checks and obtain fresh marketplace evidence for it.
Do not promise that a wording change will clear every capability.

For real privilege use, document why it is needed, its command/input boundary
and removal behavior, then leave capability acceptance to the maintainer.
Prepare any response within the user's scope; send it only with authorization.
The authoritative policy and limits are in the pinned
[security policy](https://github.com/omacom/omarchy-plugin-marketplace/blob/55efec9646cc24ca3ae8c427440043fa745ada49/SECURITY.md#automated-security-baseline).
