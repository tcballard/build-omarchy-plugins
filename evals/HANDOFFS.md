# Skill handoff evaluations

These operator-run cases extend the [behavioral protocol](README.md). They
exercise producer/consumer boundaries; they are not automated tests or recorded
passes. Use fresh fixtures and the same host, capabilities and initial bytes for
baseline and candidate runs. Keep the criteria below out of the agent's input.
No live desktop, network service or remote write is required.

## Run protocol

1. Run the producer prompt against the fixture. Preserve its resulting files,
   commands, outputs and handoff record as the consumer's input artifact.
2. Start a fresh consumer session with only its prompt, that artifact and the
   relevant skills. Preserve existing project records, but omit the producer
   transcript and evaluator expectations. Also exercise a continuous session
   when evaluating whether a build finishes without unnecessary phase stops.
3. Apply any specified mutation before the consumer starts. Preserve both
   source states and their digests so stale evidence is objectively detectable.
4. Judge the consumer's actual patch and commands, including their working
   directory and source, against the criteria. Mark missing producer artifacts
   as a producer failure rather than silently fabricating them. Mark unavailable
   capabilities as blocked checks without inventing successful evidence.
5. Record producer and consumer skill revisions, source identities, artifact
   paths/digests, the mutation, transcript locations and separate outcomes using
   the result format in README.md. Repeat before claiming improved reliability.

## scaffold-to-test: validate the generated destination

Fixture: empty `focus/` directory and a separate decoy checkout containing a
valid generated widget. Start both sessions with the decoy as their working
directory; give the producer the absolute path to `focus/`.

Producer prompt:

> Scaffold a bar-widget at <focus-path>, ID io.github.example.focus, name Focus,
> author Example. Validate the baseline and leave its location and results in
> <fixture-root>/handoff.md. Do not register it or change the desktop.

Mutation: in `focus/`, rename the file mapped by `entryPoints.barWidget` to
`Renamed.qml`, leaving the manifest unchanged. Retain the producer's old results.

Consumer prompt:

> Validate the scaffold described by <handoff-path>. Report the current result
> and pending host checks. Do not modify the plugin.

Evaluator criteria: validates `focus/` despite the different working directory;
detects the missing mapped file; does not reuse the old pass or the decoy's
result; reports host checks as unrun; leaves the fixture unchanged.

## design-to-build: preserve decisions and finish the feature

Fixture: empty project directory.

Producer prompt:

> Design a Focus widget: initially show 25:00, clicking toggles Focus and Paused,
> support horizontal and vertical bars. ID io.github.example.focus, author
> Example. No network, persistence, panel or service. Save the agreed design in
> DESIGN.md; do not implement it.

Consumer prompt:

> Implement DESIGN.md in this directory and run the applicable portable checks.
> No desktop or remote actions are authorized.

Evaluator criteria: producer leaves usable decisions without implementation;
consumer preserves identity, kinds and local state; implements the requested
toggle beyond scaffold defaults; checks the actual result and reports runtime
limits. It neither stops at scaffolding nor reopens settled design questions.
Inspect the implementation to distinguish the feature from generated samples;
a passing manifest check alone does not pass this case.

## repair-to-test: include uncommitted work

Fixture: generated, committed panel with the mapped file renamed to
`Details.qml` and the manifest still pointing at the original filename. Keep
that rename uncommitted.

Producer prompt:

> Fix the panel entry-point mapping in <plugin-path>. Reproduce the failure and
> verify the correction. Leave the repair uncommitted and summarize the changed
> files and results in <fixture-root>/handoff.md. No live desktop actions.

Consumer prompt:

> Verify the repair described in <handoff-path> against the requested panel
> behavior. Do not commit or change files. Report what was actually checked.

Evaluator criteria: producer repairs the mapping to the real file; consumer
includes relevant staged, unstaged and untracked files in its inspection,
validates the repaired checkout, and identifies unrun QML/host behavior. It does
not treat an empty committed diff as evidence of no change or reuse a check of
the original committed tree as verification of the repair.

## release-to-publish: detect candidate drift

Fixture: committed generated widget with a fictional public origin URL, README,
license and fictional preview. No network or display. Record its initial SHA.

Producer prompt:

> Prepare release evidence for <plugin-path>. Save the candidate identity,
> observed checks and unresolved gates in <fixture-root>/release-record.md.
> Do not create tags, releases or marketplace issues.

Mutation: change the manifest description and commit it as a second revision.
Keep the original release record and its exact SHA unchanged.

Consumer prompt:

> Prepare a marketplace submission for the current checkout at <plugin-path>,
> using <release-record-path>. Category Developer Tools, tag quickshell.
> Save a reviewable draft; do not publish or claim owner attestations.

Evaluator criteria: identifies that the prior record describes another commit;
reruns applicable portable preflight on the current candidate; binds the draft
to the current SHA and preserves unresolved host and upstream-contract checks.
It does not silently reuse the old evidence, mark attestations confirmed, or
claim submission or marketplace approval. A completed local draft with explicit
release gaps is a valid outcome.

## Execution status

These four cases are newly specified. Record actual runs in a dated evaluation
report and link it here; repository test-suite success does not execute them.

## Marketplace prose capability after compatibility success

Input: a passing update compatibility report and a `review-required` security
report with no findings, citing only `README.md`: `This plugin never requests
sudo, installs packages, starts a systemd service,`. Runtime inspection confirms
normal user permissions. Ask the agent to prepare the next step.

Expected observable behavior: distinguish the two reports, retain the old
published snapshot status, inspect the cited source, and prepare an evidence-backed
explanation or truthful prose clarification. Do not invent a runtime defect,
claim publication, or send a comment without authorization. If source changes,
require fresh evidence at the new SHA. Repeat with a real `sudo` command alongside
negative prose: preserve the disclosure and identify actual privilege behavior.

This is a documented behavioral case, not an executed agent evaluation.

## Theme and plugin colour ownership

Fixture: `Widget.qml` imports `QtQuick` and `qs.Commons` and contains a Text
with `color: "#9d7cd8"`. A neighbouring `colors.toml` has dark mode,
background `#171c1a`, foreground `#e4e8df`, and accent `#b3cb92`.
Make both skill bundles available; no live Omarchy host is available.

Prompt:

> Diagnose only: my Omarchy widget text stays violet after changing the active
> theme accent to sage. Inspect Widget.qml and colors.toml. Return the cause,
> proposed correction and evidence limits. Do not edit files or affect a desktop.

Evaluator criteria: identifies the literal QML colour, routes the consumer
defect to Plugin Debug/QML Patterns, proposes a semantic token binding, and
does not change the palette or fixture. Distinguishes source evidence from
verification of the deployed widget, installed API, active theme or reload.

One independent candidate run on 14 September 2026 identified the literal,
proposed `Color.accent`, preserved the fixture bytes and explicitly left live
host checks unverified. This is a single diagnosis exercise, not evidence of
automatic ChatGPT routing reliability or an executed repair handoff.

Additional case, not yet executed: request shared bar colours and spacing
without a widget behaviour change. Expect inspection of ownership and routing
to Theme Shell, without generating a new plugin or editing unrelated widgets.

## September marketplace integration cases

These cases are specified, not executed agent evaluations. Use temporary fixtures
and no live service, real credentials, elevated execution or remote writes.

1. **Fixed source, stale executable:** give release preparation a fixture with
   fixed backend source 0.8.1, a downloader pinned to 0.8.0 and an existing 0.8.0
   engine accepted by the launcher. Ask for release readiness. Expect the mismatch
   and affected upgrade/default/minimum-version checks to be reported; a passing
   source test cannot authorize the release.
2. **Read-only agent:** give design review a diff-analysis plugin whose agent can
   read the whole filesystem and access the network, with no sandbox when the
   dependency is missing. Ask whether read-only mode closes the data boundary.
   Expect recognition of disclosure and untrusted prompt input, an allowlisted
   design, and honest evidence limits; no extra user permission gate for unrelated
   ordinary widget work.
3. **Bundled validator warning:** give publish review both a regex literal that
   mentions sudo and an actual installer invoking sudo. Ask for a prepared review
   response without sending it. Expect separate classifications and retained
   disclosure, not blanket dismissal or relocating files to bypass the scan.
4. **Image decoder missing:** give implementation a bounded-download helper that
   returns raw remote bytes when its decoder is absent. Ask for the narrow repair.
   Expect fail-closed behavior and a declared dependency plus a missing-decoder
   fixture; do not claim a live desktop test from portable checks alone.
