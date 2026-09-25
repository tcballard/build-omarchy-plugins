# Maintenance and possible Omacom adoption

Current steward: Tom Ballard (`tcballard`). Omacom adoption is under discussion,
not agreed or completed. Do not imply official endorsement or transfer rights
on that basis. OpenAI/Anthropic directory submissions are on hold pending this
decision; repository installation remains available.

## Maintenance responsibilities

- Keep the twelve canonical skills in `skills/`; generate the OpenAI adapter.
  Claude consumes the canonical tree with host-specific metadata at the root.
- The QML/service reviewer-boundaries and test/publish review-response references
  are deliberately duplicated: selected skills install independently. Keep each
  pair identical and run the parity check; put surface-specific detail in its
  own reference instead of silently diverging a shared copy.
- For marketplace changes, verify current forms and dated reviewer evidence.
  Update affected guidance and useful checks; preserve advisory versus blocking
  distinctions. Do not turn every reviewer preference into a universal rule.
- Require `CI / Required` on PRs. Release from the reviewed commit with the
  version contract, reproducible archives and provenance workflow.
- Rerun behavioral cases when instructions change substantially. Keep exact
  model/host identity and disclose blocked live checks in the acceptance record.
- Triage reports by reproduction, affected skill/host and source commit. Avoid
  requesting credentials or unrelated machine data.

## Adoption handover decisions

Record acceptance before changing ownership. Agree the repository owner,
maintainers and release authority; issue/security contact; naming and attribution;
marketplace publisher identities; and responsibility for upstream contract drift.
Retain MIT attribution and existing release provenance.

Inventory URLs in manifests, README, `.agents/plugins/marketplace.json`,
`.claude-plugin/marketplace.json`, generated adapter, submission packet and release
workflow before a transfer. Verify GitHub redirects and installation/update
commands from a clean account afterwards. Preserve stable plugin/marketplace
names where possible; use the provider's documented migration mechanism if a
rename is needed. Do not delete the old release assets or move published tags.

A handover is complete only when the receiving maintainer can install the bundle,
run the tests, reproduce the archives and prepare a verified draft release.
Neither a repository transfer nor a public marketplace submission is performed
by this document.
