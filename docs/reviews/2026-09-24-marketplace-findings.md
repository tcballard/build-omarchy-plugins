# Omarchy Plugin Marketplace review — 24 September 2026

## Decision

Revise Build Omarchy Plugins with a focused contract refresh and concrete regression guidance. Much of the recent feedback already appears in the bundle; expand its examples and tests rather than inventing new blanket rules.

This review informed the accompanying bundle changes. No release, marketplace submission or installed personal-skill update is part of this PR.

## Comparison and coverage

- Previous recorded review: [20 September](https://github.com/tcballard/build-omarchy-plugins/blob/2d618374ec13dd7a07efeb0cf69115fc9fa2c4e3/docs/reviews/2026-09-20-marketplace-findings.md).
- Bundle inspected: main at `2d618374ec13dd7a07efeb0cf69115fc9fa2c4e3`, including its 22 September fixes.
- Marketplace main observed: `bdf7c4fd1c0cb2bc1175dc0931362727aa4a0cb3`.
- Compared current submission/verification forms, SUBMISSION.md, SECURITY.md, VERIFICATION.md and relevant file histories against the bundle's pinned contracts and references.
- Screened 60 recently updated issue results. Retrieved 171 comments across 28 selected threads; 51 comments were by HANCORE-linux dated 20–24 September. Qualitatively reviewed substantive findings and follow-ups, concentrating on changes relevant to authoring skills.
- This is a targeted review, not a complete census or independent code audit of every plugin. Findings below describe the cited reviewed commit. Later author replies or repository changes do not independently establish that a fix works.

## 1. Actual upstream contract changes

### VPN tag

[Marketplace change #7756](https://github.com/omacom/omarchy-plugin-marketplace/commit/7dd6e56f27a732dad178012bfd996c8474027d11), 20 September 09:21 UTC, adds VPN to the submission form. Our vendored form, submission reference and `prepare_submission.py` omit it; the helper therefore rejects a currently valid tag.

Update the pinned form, hash, reference and generator together. Preserve form labels (VPN) and accept the CLI alias (vpn). Add a focused accepted-tag regression. Categories and five checklist statements remain unchanged.

The same change adds VPN and Bar discovery filters. The Bar filter targets replacements/modifiers, not ordinary bar widgets; do not turn a discovery filter into a new plugin kind or submission category.

### Standard-installation review reuse

[Marketplace change #7755](https://github.com/omacom/omarchy-plugin-marketplace/commit/40315f2a919107aad9d288ed5378b5875aa103c6), 20 September 09:21 UTC, lets a valid, non-revoked installer-only maintainer review qualify for removing a manual-installation override, provided a fresh scan matches the exact listed commit and evidence.

Document three separate requests:
1. Verify the recorded snapshot.
2. Verify that snapshot and enable standard installation.
3. Verify and publish newer current HEAD.

The second path still requires its acknowledgment and an authorized `standard-installation-approved` event. It is not a general waiver for installers, findings or other capabilities.

### Stale references versus new policy

No SECURITY.md commits were returned for the window beginning 20 September 06:00 UTC. The bundle's security pin is nevertheless dated 13 September, and its detailed publication reference remains dated 12 September. The exact SECURITY.md content digest matches the previous pin; the pin is refreshed without claiming a policy change.

Track VERIFICATION.md and the unified verification form explicitly in the contract ledger. Current policy distinguishes measured baseline outcome from selective publication disposition: new listings/updates may receive exact maintainer acceptance of eligible non-blocking findings; existing-snapshot `maintainer-verified` remains capability-only. Preserve that distinction and never imply an agent can waive a finding.

## 2. Highest-value additions

| Priority | Observed evidence | Proposed bundle revision |
| --- | --- | --- |
| High | [Jev Challenge Lab](https://github.com/omacom/omarchy-plugin-marketplace/issues/8352#issuecomment-5819807404): loopback API exposes history, drafts, keys and paid requests without authentication or Host/Origin checks. [Gloss](https://github.com/omacom/omarchy-plugin-marketplace/issues/8434#issuecomment-5819147536): prefix matching accepts 127.attacker.example as local. | Add a local-API boundary section to service/IPC guidance: parse addresses properly, authenticate sensitive operations, validate Host and Origin as appropriate, and test hostile browser origins and deceptive hostnames. Binding to 127.0.0.1 alone is insufficient for a browser-facing service. |
| High | [Plugin Updates](https://github.com/omacom/omarchy-plugin-marketplace/issues/8250#issuecomment-5801511763): HEAD matches the reviewed SHA but modified/untracked QML or JS survives checkout and is loaded. | Distinguish commit identity from loaded tree identity. Update tools should refuse dirty/untracked worktrees and recheck cleanliness before validation/rescan, preserving user changes. Add a fixture where HEAD is correct but an extra executable source file remains. |
| High | [NetScope](https://github.com/omacom/omarchy-plugin-marketplace/issues/5619#issuecomment-5819540608), [Battery Guardian](https://github.com/omacom/omarchy-plugin-marketplace/issues/6889#issuecomment-5819555896), [MoErgo](https://github.com/omacom/omarchy-plugin-marketplace/issues/7107#issuecomment-5819566127): installers overwrite shared commands/services or delete existing target contents. | Extend plugin installation/removal guidance with managed-file ownership, conflict refusal or explicit consent, and conservative removal. Test unrelated files, modified managed files and existing destination directories. The bundle's own transactional installer is not evidence that a generated desktop-plugin installer follows this rule. |
| Medium | [Omarchy Dock](https://github.com/omacom/omarchy-plugin-marketplace/issues/7631#issuecomment-5800962204): source pinned, compiler still uses moving stable. [MoErgo provenance](https://github.com/omacom/omarchy-plugin-marketplace/issues/7107#issuecomment-5792174978): owner-only attestation is too broad. | Make exact toolchain consistency explicit across rust-toolchain.toml and package recipes. Add provenance checks binding digest, repository, trusted workflow and source SHA; owner identity alone is insufficient. |
| Medium | [NetScope](https://github.com/omacom/omarchy-plugin-marketplace/issues/5619#issuecomment-5784771145): blocking terminal queue write leaks reader threads after consumer cancellation. | Add bounded terminal signaling, response close and bounded join/reap examples. Test repeated cancellation after a full queue, not just one request's visible timeout. |
| Medium | [Athena Kanban](https://github.com/omacom/omarchy-plugin-marketplace/issues/8463#issuecomment-5819309888): button invokes the wrong plugin ID. [Clipbar](https://github.com/omacom/omarchy-plugin-marketplace/issues/8478#issuecomment-5819340291): display truncation corrupts pasted pinned text. | Add end-to-end functional examples: every visible entry point reaches the declared plugin; display previews remain separate from source/action payloads. Retain bounded storage without silently substituting truncated presentation data. |

## 3. Existing guidance needing stronger regression examples

These concerns are already substantially covered in reviewer-boundaries.md, release-contract.md and test-matrix.md.

- **Whole-operation deadlines:** [Beam](https://github.com/omacom/omarchy-plugin-marketplace/issues/8371#issuecomment-5819019831) and [Commit Wallpaper](https://github.com/omacom/omarchy-plugin-marketplace/issues/8392#issuecomment-5819000706) demonstrate why checking a clock only after a blocking read returns fails against slow-drip input. Test the actual production read path under a continuous trickle.
- **Descendant cleanup:** [Commit Wallpaper](https://github.com/omacom/omarchy-plugin-marketplace/issues/8392#issuecomment-5819774887) kills git but leaves transport children alive. Test that deadline/overflow/cancellation stops and reaps the transfer group before removing staging files.
- **Process identity:** [DevWatch](https://github.com/omacom/omarchy-plugin-marketplace/issues/7927#issuecomment-5815441990) checks a reused PID's current start time twice; [Phonecam](https://github.com/omacom/omarchy-plugin-marketplace/issues/7497#issuecomment-5795173133) checks /proc then signals the numeric PID. Preserve identity from launch through signaling, using an appropriate service/cgroup or race-free handle boundary.
- **Remote text:** [mib-vlog](https://github.com/omacom/omarchy-plugin-marketplace/issues/8395#issuecomment-5819055337) persists an unbounded remote place name and renders it with automatic rich-text detection. Test the entire fetch → persistence → nested Text sink path.
- **Independent privileged trust:** [OmaNitro](https://github.com/omacom/omarchy-plugin-marketplace/issues/5540#issuecomment-5819470495) demonstrates that a movable tag supplying both root bootstrap and hashes is not independent verification.
- **Required external setup:** [Omatalk](https://github.com/omacom/omarchy-plugin-marketplace/issues/8407#issuecomment-5818821005) removed automatic execution but still copied a mutable curl-to-shell command. Review required setup instructions as part of the delivered product; moving execution to the user does not substantiate provenance.
- **Catalogue authority:** [Workbench feedback](https://github.com/omacom/omarchy-plugin-marketplace/issues/3795#issuecomment-5784382912) explicitly says there is no marketplace catalogue-signing key or independently published digest available. Do not invent one. Preserve the distinction between descriptive network data and authority to install executable code.

## 4. Implementation and validation

1. **Contract correction:** VPN support; refreshed reviewed form/security pins; add verification form and VERIFICATION.md tracking; accurate standard-installation path.
2. **Authoring guidance:** local API trust, loaded checkout identity, non-destructive installation, exact toolchains/provenance, queue shutdown and functional payload fidelity.
3. **Evidence and synchronization:** dated review in docs/reviews; targeted behavioral fixtures; canonical-to-packaged skill synchronization; normal repository checks.

Update both canonical references and their self-contained packaged copies using the repository's existing synchronization process.

Keep these checks proportional to implemented behavior. Do not add a localhost-server gate to a simple clock widget, or claim lexical scanning proves deadlines, filesystem race safety or authentication. Record runtime checks as unrun until actually exercised.

GitHub release metadata confirms v0.5.0 was published on 21 September at 05:15 UTC. This PR puts later changes under Unreleased and corrects the published heading; version metadata is unchanged.


Implementation: refreshed contracts and VPN helper coverage; updated canonical and packaged authoring references; added scoped handoff scenarios. See [ACCEPTANCE.md](../../evals/ACCEPTANCE.md) for observed checks and limitations.
