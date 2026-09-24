# Choose a workflow

Start at the work you actually have. A small fix needs the affected skill and
relevant checks; the full route is useful when building and shipping a plugin.
Describe the outcome in ordinary language or name the skill in your host.
Continue through authorized work without asking the user to invoke every stage.

## New plugin: idea to publication

1. [Design](../skills/omarchy-plugin-design/SKILL.md) checks prior art for new
   ideas, establishes personal/public/marketplace intent, and resolves the
   surface and ownership decisions still open. An existing specification
   supplies settled decisions directly. Keep the first feature set small and
   bring current publishing constraints into design when publication is intended.
2. [Scaffold](../skills/omarchy-plugin-scaffold/SKILL.md) creates the repository
   at the agreed destination. Generated sample behavior is the starting point.
3. Implement the requested behavior with the relevant surface skill:
   [bar widget](../skills/omarchy-bar-widget/SKILL.md),
   [panel, overlay or menu](../skills/omarchy-panel-overlay/SKILL.md), or
   [service and IPC](../skills/omarchy-service-ipc/SKILL.md).
   [QML patterns](../skills/omarchy-qml-patterns/SKILL.md) supplies shared
   implementation guidance, including hosted QML for a full bar.
4. [Test](../skills/omarchy-plugin-test/SKILL.md) checks the actual changed
   source and records observed results and remaining host checks.
5. [Demo](../skills/omarchy-plugin-demo/SKILL.md), when needed, prepares
   fictional fixtures and captures the UI when a suitable host is available.
6. [Release](../skills/omarchy-plugin-release/SKILL.md) reconciles the candidate
   source, version, tests, preview and assets, including the downloaded/default
   backend version when a fix depends on an external executable.
7. [Publish](../skills/omarchy-plugin-publish/SKILL.md) prepares the marketplace
   submission from that candidate and submits within the owner's authorization.
   For a listed plugin, select recorded-snapshot verification, standard-installation
   approval or newer-HEAD promotion explicitly; these have different evidence
   and maintainer decisions.

Stop at the outcome requested. Building a widget does not imply releasing it;
preparing a release does not imply submitting it to the marketplace.

## Shorter routes

| What you have | Where to start | Expected result |
| --- | --- | --- |
| A design question | Design | Recommendation and tradeoffs, without implementation for a design-only request. |
| A specification and existing plugin | Relevant surface skill, with QML patterns as needed → test | Scoped implementation preserving settled decisions. |
| A tooltip or layout correction | Relevant surface skill → affected checks | Focused patch without restarting design or scaffolding. |
| One widget ignores the active theme | Debug → QML patterns for a requested repair | Diagnose the token consumer; preserve a correct global palette and diagnosis-only scope. |
| Global bar colours or theme-owned spacing | Theme Shell from Build Omarchy Themes, when available | Change shared theme tokens; use Plugin skills only for any requested QML consumer or behaviour change. |
| A discovery, load or runtime failure | [Debug](../skills/omarchy-plugin-debug/SKILL.md) → relevant checks after repair | Supported diagnosis, or a patch and evidence that the original failure is fixed. |
| A legacy integration | [Migrate](../skills/omarchy-plugin-migrate/SKILL.md) → affected implementation and tests | Preserved machine responsibilities with the requested shell surface migrated. |
| A working UI needing a screenshot | Demo | Reproducible fixtures, capture and restoration evidence, or a harness with capture explicitly pending. |
| A tested candidate | Release → publish when requested | Source-bound release evidence and a reviewable submission. |
| Marketplace review feedback | Publish's review-response guidance → affected implementation/test skills | Classify compatibility and security separately; inspect prose-only capability matches, then return a correction or explanation tied to the reviewed SHA. |

## What travels between skills

Keep the requested scope, target checkout, relevant decisions, changed files,
evidence locations and unresolved checks with the work. For agent, broker or
privileged integrations, carry the actual trust/authorization boundary; for
backend fixes, carry artifact pins and minimum-version evidence as well. Each skill's **Inputs
and completion** section owns its specific expectations. Reuse the project's
existing record for multi-session work; a small same-session edit needs no new
handoff document.

Evidence belongs to a source state. During development, that includes relevant
working-tree changes; for release and publication, use the exact candidate
commit and artifact identities. Recheck affected behavior after changes rather
than carrying an old pass forward. A consumer inspects the files and results
it receives instead of treating the previous step's summary as proof.

## Common questions

**Must every skill be installed?** Use available focused skills through the
host's supported mechanism. A missing sibling is not a reason to invent a tool
or stop independent work. For example, scaffolding can use its generated
validator and report the narrower evidence when the test skill is absent.
When the release and test skills are installed under different directory names,
resolve the loaded test skill and pass its script through release preflight's
`--validator` option. The release skill documents this explicit handoff; missing
validation still blocks readiness.

**Must setup happen before any work?** Only a prerequisite needed for the next
action blocks it. Missing display access leaves runtime checks pending while
portable work continues. Missing owner attestations prevent submission, while
the title and body can still be prepared.

**When is it working?** The requested behavior exists in the actual target
checkout, results refer to that source, later skills can find their inputs, and
the final report identifies unfinished work. A scaffold, successful preflight,
prepared capture harness or created issue proves only that particular stage.

Maintainers can exercise these boundaries with the
[handoff evaluation cases](../evals/HANDOFFS.md).
