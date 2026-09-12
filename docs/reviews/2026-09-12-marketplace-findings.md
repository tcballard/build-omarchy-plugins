# Marketplace review findings — 12 September 2026

The main opportunity is to prevent repeated boundary mistakes before submission,
then give the reviewer concise evidence against one unchanged commit. More
instruction volume alone will not achieve that.

## Coverage and method

Collected all open/closed issue records from
[omacom/omarchy-plugin-marketplace](https://github.com/omacom/omarchy-plugin-marketplace/issues)
and all corresponding issue comments available at collection time:

- 6,531 entries: 6,436 issues and 95 pull requests.
- 4,495 titles beginning `[Plugin]` and 1,839 beginning `[Verify]`, including
  nonstandard variants. The narrower colon-form counts were 4,492 and 1,838.
  These are requests, **not unique plugin repositories**.
- 30,036 unique comments, against 30,033 expected at initial inventory. No issue
  has fewer collected comments than expected; three received one further comment
  during collection (#6524, #6519, #6454).
- 6,286 comments authored by `HANCORE-linux`, across 3,589 threads; 16,370 by
  `github-actions[bot]`. Bot output is not attributed to Hancore.

The repository-wide API stops at 30,000 comments. After collecting those pages,
we fetched the 21 threads with count discrepancies individually and deduplicated
by comment ID. This is a dated, changing snapshot, not continuous monitoring.

A deterministic indexing pass covered every collected record. Qualitative
reading covered chronologically spread Hancore reviews, recent follow-ups and
representative findings below. **This is not a claim to have manually read all
30,036 comments or independently audited the source of 4,495 submitted plugins.**
It excludes PR inline review comments and linked external documents not fetched.
The index retains request type, coverage counts, source URLs and body digests;
the Hancore index retains every comment URL, timestamp, digest and topic matches.
The raw corpus and indexes are retained in the accompanying dated corpus archive;
the compact summary and reproducible indexer are committed here.
Reproduce with `scripts/summarize_marketplace_reviews.py CORPUS OUTPUT`.

## Recurring topics

Counts below are distinct threads containing matching words in Hancore's
comments. Categories overlap and include approvals/resolved findings; they are
**not confirmed-defect counts or rejection rates**. Repeat requests from one
repository can appear in multiple threads. Use them to prioritize investigation,
not to rank authors or infer marketplace acceptance statistics.

| Topic | Threads mentioning it | Bundle response |
| --- | ---: | --- |
| Resource bounds | 1,485 | Limit bytes at the producer before collection/parsing; then bound fields and retained state. |
| File identity and traversal | 1,161 | Explain retained descriptors, ancestors, atomic writes and concurrent writers. |
| QML text rendering | 790 | Trace external values into every relevant PlainText sink. |
| Network policy | 786 | Validate redirect destinations, schemes and whole-request limits. |
| Snapshot/form consistency | 719 | Preserve form labels and attach evidence to one final full SHA. |
| Privilege/supply chain | 535 | Establish trusted helper identity and executable provenance. |
| Process lifetime | 507 | Own descendants through cancellation, termination and reaping. |
| Credentials | 468 | Keep secrets out of argv/logs and delegate authentication. |
| Executable/environment identity | 289 | Avoid ambient PATH and inherited interpreter configuration in sensitive runtime paths. |
| Injection | 226 | Direct argv plus option validation; no interpolated source/config programs. |
| Agent/session control payloads | 170 | Inspect the full distributed desktop-plugin checkout. |
| Duplicate/workflow handling | 137 | Reuse active requests; distinguish publication failures and maintainer-invited resubmission. |

## Evidence and interpretation

- [#1667](https://github.com/omacom/omarchy-plugin-marketplace/issues/1667#issuecomment-5451236689): checking `responseText` after the transport accumulated
  it did not close the byte-boundary finding. This supports producer-side checks,
  not a rule that adding any length check is enough.
- [#3360](https://github.com/omacom/omarchy-plugin-marketplace/issues/3360#issuecomment-5464817134): remote repository descriptions and commit subjects
  reached default AutoText. The review also credited safe argv and delegated
  authentication; capability presence alone should not be called a defect.
- [#6426](https://github.com/omacom/omarchy-plugin-marketplace/issues/6426#issuecomment-5646894185): path checks followed by a fresh full-path open did not
  retain ancestor identity. Advice now distinguishes the final component from
  component-wise descriptor traversal.
- [#6292](https://github.com/omacom/omarchy-plugin-marketplace/issues/6292#issuecomment-5645360550): trusted-directory claims still accepted writable shims,
  temporary files grew before limits were checked, and helper termination left
  descendants alive. Fixes must cover the entire production path.
- [#6157](https://github.com/omacom/omarchy-plugin-marketplace/issues/6157#issuecomment-5647018532): delayed numeric PID/PGID signaling introduced an identity
  race. “Kill the group” alone is insufficient lifecycle guidance.
- [#2766](https://github.com/omacom/omarchy-plugin-marketplace/issues/2766#issuecomment-5446596212): an upstream CLI's argv-only recovery-phrase interface
  warranted removing inline entry from the plugin, rather than merely disclosure.
- [#4744](https://github.com/omacom/omarchy-plugin-marketplace/issues/4744#issuecomment-5642689162): agent/session handoff instructions in an installable
  desktop-plugin checkout blocked review. This bundle is itself an intentional
  skills payload; that distinct purpose is preserved.
- [#590](https://github.com/omacom/omarchy-plugin-marketplace/issues/590#issuecomment-5442713475): closure explicitly invited a new submission after fixes.
  Earlier blanket “never open a new issue” advice was too broad.

The submission form also drifted: `Kids` is now a category, and displayed tags
include Education/Kids and title-cased labels. The exact upstream form at
`8201d231688c0c8366bce4edf0dbf253cb4b5eb5` is now pinned and vendored. The generator
accepts old CLI spellings but emits current form labels.

## Implemented changes and remaining evidence

Targeted references are loaded by QML, service and publish skills. The static
validator adds advisory discovery for collected QML inputs and agent-control
filenames; it does not claim data-flow analysis, refuse ordinary documentation,
or make a security certification. A reviewer-response table connects each
finding to the production fix, reproduction and final SHA.

Installation documentation, Claude packaging, annotated-tag creation and
stewardship handover are addressed alongside this review. See
[acceptance](../../evals/ACCEPTANCE.md) for actual execution evidence and remaining
provider/desktop checks. No message, submission, ownership transfer or new
release was sent as part of this work.
