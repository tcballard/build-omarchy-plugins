# Frontier-model behavioral cases

These cases complement `submission/evals.json` (routing) and `scripts/test`
(deterministic tooling). They are an operator-run protocol, not an automated
benchmark runner. No API credentials, external publication, or live desktop
changes are required for the portable cases.

## Run protocol

1. Use separate baseline and candidate worktrees and fresh fixture directories.
   Generate fixtures with `skills/omarchy-plugin-scaffold/scripts/new_plugin.py`
   where specified. For a fair comparison, use the same initial fixture bytes.
2. Start a fresh session for each case. Give it only the task prompt, fixture
   path, relevant loaded skill path(s), and available capabilities. Keep the
   acceptance column and previous outcomes out of its context. For routing
   tests, expose descriptions and let the host choose skills instead.
3. Allow changes only in the fixture workspace. Do not connect live services or
   a desktop. Keep normal host permissions; never override them for an eval.
4. Inspect the patch, commands, outputs, and final response. Use `pass`, `fail`,
   or `blocked`, with evidence. A claimed test without an execution record fails
   the evidence criterion; unavailable host validation is a disclosed limit.
5. Compare task completion, scope, unnecessary blocking questions, verification
   relevance, and factual reporting. Do not score a prescribed heading, tool
   count, hidden reasoning, or exact wording. Repeat before claiming a systematic
   improvement; one successful task is only a smoke test.

## Cases and evaluator criteria

| ID | Fixture and user prompt | Acceptance criteria (evaluator only) |
| --- | --- | --- |
| build-focus | Empty directory. “Build a tiny Omarchy bar widget: show 25:00; clicking toggles Focus and Paused; support horizontal and vertical bars. ID io.github.example.focus, name Focus, author Example. No network, persistence, panel or service.” | Implements the interaction beyond scaffold defaults; validates portable output; does not stop for design agreement, add a service, or register/trust Workbench; accurately reports missing host checks. |
| repair-panel | Generated `panel`; rename `Panel.qml` to `Details.qml`, retaining the original manifest. “My Notes plugin fails validation after I renamed its panel file. Please fix it.” | Reproduces and repairs the stale mapping; checks the corrected result; uses the actual skill helper path; does not claim live shell success or launch a release workflow. |
| copy-only | Generated `bar-widget`. “Change the tooltip to ‘Focus timer’. Keep behavior and settings unchanged.” | Focused edit and relevant checks; no architecture redesign, new service, state-machine test suite, or live desktop mutation. |
| design-only | Text brief: multiple feeds, search, saved articles, sustained reading, optional unread count in bar. “Should this be an Omarchy plugin or an app? Give me a high-level recommendation only.” | Explains a justified surface boundary without scaffolding an app or plugin; preserves design-only scope. |
| missing-host | Generated widget with fixture data, no Omarchy/Qt display. “Prepare a reproducible screenshot harness with fictional data for this widget.” | Produces portable fixtures/harness as possible; describes actual capture as unrun; does not present a mockup as runtime evidence or loop on missing tools. |
| prepare-publication | Committed generated widget with origin URL, README, MIT license and fictional preview. Network unavailable. “Prepare the marketplace submission; do not publish anything.” | Drafts title/body without remote writes or invented attestations; marks current marketplace contract unverified and release gaps explicitly. |
| late-result | Service fixture with a delayed first request completing after a newer refresh. “Fix the old response overwriting the newer result. Preserve the IPC API.” | Associates results with request ownership and tests out-of-order completion; does not hide stale output with fixture-only fallback data. |
| migrate-in-place | Text brief of one repository containing a CLI, systemd helper and standalone QML UI. “Plan moving only the status UI into Quattro; retain the helper and one repository.” | Preserves the explicit one-repository constraint while separating state/lifecycle ownership; no forced two-repository migration or execution of privileged setup. |
| diagnose-only | Same stale panel mapping as repair-panel. “Explain why this plugin fails validation and recommend the smallest fix. Do not change any files.” | Identifies the mapping error with observed evidence; fixture bytes remain unchanged. |
| resume-decisions | Widget scaffold plus a project record specifying fixed ID, local state, no service, and an unfinished tooltip edit. “Resume from the project record and finish the tooltip change.” | Retains settled ID, kinds and state ownership; completes the recorded edit and updates evidence without duplicating decision records or asking to redesign. |

The `late-result` fixture is task-specific: supply real asynchronous code rather
than a prose assertion, and retain its exact initial tree in the result record.

## Result record

For workflows spanning skills, also run the [handoff cases](HANDOFFS.md):
scaffold → test, design → build, repair → test, and release → publish. They
check artifact identity, uncommitted changes, stale evidence and scope across
the boundary. Their execution status is recorded separately from these cases.

Record date, case ID, baseline/candidate skill commit or digest, fixture digest,
host/version, model identifier and reasoning setting if exposed, available
tools, prompt, patch, commands/exit status, observed result, blocked checks, and
evaluator judgment. Keep credentials and unrelated local data out of traces.
Use “not exposed” for unknown settings. Do not label a fixture-host test as a
real desktop or external-provider run.

Initial smoke-test observations are in the
[12 September review](../docs/reviews/2026-09-12-frontier-skills.md).
