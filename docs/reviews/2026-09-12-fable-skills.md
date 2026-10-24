# Fable review — 12 September 2026

Baseline: Astra candidate `d7556304d972ba8ddb0089b7c9078ca069cfcda5`.
Reviewed all twelve portable skill entrypoints against Anthropic's
[Fable 5.1 guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5-1),
[Fable 5 guide](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/prompting-claude-fable-5)
and [general Claude guidance](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices).

## Findings

The Astra changes address much of the overlap. Additional corrections are
concentrated in four skills rather than duplicated throughout the bundle.

| Skill(s) | Assessment and disposition |
| --- | --- |
| Design | Existing-spec preservation now extends to settled decisions and resuming work through the project's existing records. |
| Debug | Diagnosis-only scope was insufficiently explicit. Added a clear assessment boundary, focused repair behavior and evidence-backed progress. |
| Test | Existing scoped layers are appropriate; clarified that temporary probes need not become permanent suites. |
| Release | Clarified that preflight evidence does not establish completion of later release actions. |
| Scaffold | Existing completion rule and optional Workbench registration retained. |
| QML, bar widget, panel/overlay | Existing targeted-change rules and Omarchy invariants retained; no extra generic instructions needed. |
| Service/IPC | Request ownership and bounded process state retained. |
| Demo | Fictional fixtures and honest capture limits retained. |
| Publish | Current-form verification and specific owner attestations retained. |
| Migrate | Existing one-repository and machine/shell ownership boundaries retained. |

No instruction was found demanding disclosure of private internal reasoning.
Existing architecture rationale, root causes and command evidence remain valid
deliverables. Provider-specific API settings are documented as host concerns;
the toolkit does not own an Anthropic client or its conversation history.

## Evaluation boundary

Added diagnosis-only and resume-after-handoff cases to the shared evaluation
protocol. These exercise scope and continuity in addition to build, repair,
capture, publication, migration and async behavior. They are not claimed Fable
passes. A fresh local diagnosis session can check portability, but it cannot
establish Fable behavior without an actual Claude runner and model trace.

The previous Astra smoke-test observations remain attributed to their original
candidate. Structural checks and package tests validate this bundle's mechanics;
none certifies behavior across all providers or a live Omarchy desktop.

A fresh local read-only probe asked for the cause of a previous failure, but its
fixture had no Git history. The agent validated the current files, reported that
the historical cause could not be established and made no changes. This checks
scope and evidence restraint, not Fable performance or the stale-mapping case.

## v0.3.0 preparation

The owner selected **v0.3.0** for the combined Astra/Fable revision, following
the existing v0.2.3 metadata. Update version surfaces and submission materials
together. Keep the README's published-install examples on v0.2.3 until v0.3.0
actually exists. This PR prepares a release candidate; it does not merge, tag,
upload or publish a release. Real Fable task runs remain outstanding evidence
for any future tested-on-Fable claim.
