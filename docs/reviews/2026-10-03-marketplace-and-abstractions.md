# Marketplace review and abstraction assessment — 3 October 2026

## Scope and evidence

Reviewed Build Omarchy Plugins v0.6.1 on main, marketplace main at
`3e38844761e5a4045243fd1c9ca272e4c6b61c12`, and Omarchy quattro at
`8e02fc84f5bdc511ed102e2a14f8935bba4f92bd`. Compared the
marketplace forms, SUBMISSION.md, SECURITY.md and VERIFICATION.md with the
previous pinned `b5c8f32b5735babdcf4931548da1059fe8659422` snapshot. Their bytes
are unchanged. The two tracked Quattro documents also retain their reviewed
hashes; no new shell API was inferred from a moving branch head.

Screened 60 most recently updated marketplace requests, then retrieved 147
comments across 20 selected threads, including 53 by HANCORE-linux. This is a
targeted sample with historical follow-ups, not a census or independent audit of
those plugins. Selection covers native dependencies, credential/approval flows,
network transports, backup/restore, display text and withdrawn findings. Read
maintainer findings and follow-ups; author claims are not independent evidence.
Open bundle requests at review time were five dependency-update PRs; they do not
supply new plugin authoring policy and were not changed in this work.

## Marketplace changes

| Evidence | Consequence for the bundle |
| --- | --- |
| [CLI form errors #9808](https://github.com/omacom/omarchy-plugin-marketplace/commit/1f845b73e7324ee0bde2f7c121032066aa9cc295) | Malformed `[Plugin]:` requests now get the label needed to publish their actual form error. Fix the existing body; a label is not validation. Track the classifier implementation as well as unchanged form bytes. |
| [Migrated repository resolution #9594](https://github.com/omacom/omarchy-plugin-marketplace/commit/8be8e3be5fc0a0592cc90b9d37d858177a624a84) | Recorded former names of the same listing resolve to its canonical repository before access. A redirect is not identity evidence; Verify cannot create a new listing. Track the resolver contract. |
| [Budgeted policy revalidation #9552](https://github.com/omacom/omarchy-plugin-marketplace/commit/74836ff40c4f55f04aafbb401e557deb0a770bd0) | Some unchanged, previously passing sources defer policy-only refresh. Do not interpret queue delay as rejection, or extend deferral to changed/failing sources. |
| [Pocket](https://github.com/omacom/omarchy-plugin-marketplace/issues/9872#issuecomment-5971720907), [OMeetingBar](https://github.com/omacom/omarchy-plugin-marketplace/issues/9860#issuecomment-5970904348), [TMOS](https://github.com/omacom/omarchy-plugin-marketplace/issues/8574#issuecomment-5972030850) | Explain required external native setup separately from account configuration and optional setup; `installer` capability alone does not establish a mandatory manual-install classification. |
| [Touch Bar retraction](https://github.com/omacom/omarchy-plugin-marketplace/issues/9262#issuecomment-5970593063), [OmaRead retraction](https://github.com/omacom/omarchy-plugin-marketplace/issues/9174#issuecomment-5970439231) | Track current disposition, including withdrawn findings. Retain proportional resource robustness requirements without claiming every allocation concern is a security listing blocker. |

The unchanged selective-policy distinction remains: measured outcome, eligible
publication disposition, exact maintainer acceptance and actual publication are
separate. Local lint does not reproduce or override the central baseline.

## Repeated boundary failures

| Evidence | Guidance and practical change |
| --- | --- |
| [Sift](https://github.com/omacom/omarchy-plugin-marketplace/issues/9858#issuecomment-5970803404) | DNS-based consent must bind to the destination actually used, before private bytes are sent; a precheck followed by another resolution is insufficient. |
| [TMOS](https://github.com/omacom/omarchy-plugin-marketplace/issues/8574#issuecomment-5823505773) | Credential-bearing readers should refuse redirects or enforce origin policy on every hop; bound before buffering. |
| [Doorman](https://github.com/omacom/omarchy-plugin-marketplace/issues/9558#issuecomment-5961920299) | Caller identity is not operation/secret-recipient authority. Test the genuine authorized caller using a caller-selected helper and misleading command, not only a forged PID. |
| [Pianobar config](https://github.com/omacom/omarchy-plugin-marketplace/issues/8898#issuecomment-5855383375), [prompt race](https://github.com/omacom/omarchy-plugin-marketplace/issues/8898#issuecomment-5858550108) | Missing and unreadable configuration need different outcomes. UI masking/polling does not protect credentials forwarded through argv or terminal history. |
| [Settings Sync](https://github.com/omacom/omarchy-plugin-marketplace/issues/9849#issuecomment-5970334443) | Validate restored IDs/references before filesystem and Git operations; reject repository-supplied symlinks before backup writes. |
| [Mirador](https://github.com/omacom/omarchy-plugin-marketplace/issues/8721#issuecomment-5965869818) | Every external Text sink, including compact views, needs literal rendering. Our Panel and Menu templates lacked explicit PlainText despite accepting summon data; fixed all generated Text sinks, including titles. |
| [Network Persona](https://github.com/omacom/omarchy-plugin-marketplace/issues/9854#issuecomment-5970652519) | Verify the complete promised state across active providers; one subsystem's state is not an all-off guarantee. |

## Assessment of “more abstractions plus harsh lint”

The proposal fits this bundle well when abstractions remove repeated policy
choices. The strongest immediate move is to make its existing scaffold and
boundary contracts executable and coherent. The bundle already uses Omarchy
components, a manifest generator, validators and reusable-helper recommendations.
Its weakness is that much safety advice is prose and optional copy/paste; our own
Text templates illustrate the resulting gap.

| Area | Assessment | Action |
| --- | --- | --- |
| Hosted UI and manifest structure | Useful existing abstractions; callers should not reconstruct lifecycle or schema. | Retain host components and generator; fix literal-rendering defaults. |
| Network/process/private-state plumbing | High leverage: the same failure boundaries recur across unrelated plugins. | Define narrow caller/result/error contracts; evaluate existing reviewed Run/Store helpers and small local adapters before bespoke code. |
| Enforcing chosen architecture | Existing advisory discovery can identify some obvious bypasses but does not enforce project choices. | Add opt-in `--deny-capability` for four recognized QML/JS patterns, independent of marketplace disposition. Cover nested JS and fail if relevant source cannot be read within limits. |
| Broad mandatory lint | Too blunt: capability use and resource robustness do not automatically imply a security defect. | Select explicit rules for the actual design; preserve advisory defaults and current maintainer disposition. |
| Token efficiency | Plausible from smaller caller APIs and progressive disclosure; unmeasured here. | Measure total context/tokens, edits and review iterations on comparable tasks before claiming savings. |
| Reversibility | Local adapter replacement is easier than dispersed policy rewrites; irreversible effects remain. | Avoid a framework/DSL or generic privileged/password wrapper. Keep contracts inspectable, migrations explicit and dangerous operations independently authorized. |

A future implementation of a shared boundary library should demonstrate two
meaningfully different consumers, integration tests, version/provenance ownership
and a migration path. This change does not claim to deliver a universal safe
network/process library. Omakit remains optional, and copied code needs review
and tests in the receiving plugin. Its [current Blocks contract](https://github.com/mtolhuys/omakit/blob/main/docs/BLOCKS.md)
was also read: it documents Run 0.2.1 and Store 0.2.0, copied-file provenance and
explicit limits. This is documentation inspection, not execution or an independent
audit of the implementation or its published measurements.

## Limits of the new gate

`--deny-capability qml-network --deny-capability qml-dynamic-code` makes recognized
patterns build errors only when that project chose the rule. Other selectable
rules are `qml-process` and `qml-collected-input`. The gate is conservative lexical
discovery: comments/strings/fixtures may match, and aliases/indirect behavior can
escape. It is not QML data-flow analysis, a sandbox or marketplace certification.
It cannot establish producer limits, process cleanup, authority or provenance.
Those remain production-path tests and review. No deny rule is on by default. Unselected advisory findings affect exit status
only when `--security` is explicitly requested; selecting an architecture rule
does not promote every advisory into a build failure.

## Delivery and validation

See [acceptance evidence](../../evals/ACCEPTANCE.md) for executed portable checks
and the isolated forward-test. Canonical and packaged skills are synchronized.
The personal skill copies are updated separately; published release assets and
version metadata were left at v0.6.1 during this review. The subsequent v0.7.0
release preparation is recorded separately in the acceptance evidence.
