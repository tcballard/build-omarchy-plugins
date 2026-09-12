# Using the skills with Astra and other frontier models

Select the model in your agent host. These skills do not set a model, reasoning
level, API parameter, or delegation policy. The portable source stays the same
across providers; OpenAI packaging remains a generated adapter.

## Give the agent a task it can finish

Supply the outcome, repository, relevant constraints, and the evidence you need.
Mention an existing specification instead of asking for a second plan. For example:

> Use the Omarchy skills to implement the attached focus-widget spec in this
> repository. Keep the existing ID and settings. Finish the portable patch and
> required checks, and prepare a draft PR. Record any checks that need a real
> Omarchy session. Do not enable the plugin or publish a release.

For a small fix:

> Fix this panel's Escape handling. Preserve the existing window and API.
> Reproduce the failure, verify the corrected close path, and run the repository's
> required checks.

For a design-only request:

> Review whether this feed reader belongs in a bar plugin or a native app.
> Recommend the interaction and state boundaries; do not implement it yet.

For an explicitly authorized local demo, state which desktop changes are allowed.
Repository editing, Workbench trust, enabling a live plugin, and public release
are different actions. Already supplied authorization should not be requested
again, and a request to prepare a submission is not an ownership attestation.

## Why these revisions suit Astra

OpenAI's current guidance highlights Astra's sensitivity to skill instructions,
its tendency to ask clarifying questions, and thorough verification that can be
excessive for a small change. The changes here remove a design agreement gate,
reuse existing authorization, and tie tests to changed behavior and required
checks. They retain explicit Omarchy lifecycle and credential constraints.
See [OpenAI's Astra prompting guidance](https://developers.openai.com/api/docs/guides/latest-model#prompting-best-practices),
reviewed 12 September 2026. These are design choices informed by that guidance,
not benchmark results.

## Keep context and capabilities honest

- Load the skills for the current task, then the references relevant to the
  affected contract. Installing twelve skills does not mean reading all twelve
  for every change.
- Use the loaded skill's directory to resolve its helpers. The plugin checkout
  and the shell's current directory may be elsewhere.
- Supply inspected source, logs, and fixtures. A dated contract snapshot is
  useful evidence, but current marketplace actions need a current form check.
- If a sibling skill, display, or Qt import is absent, complete what is possible
  and identify the missing evidence. Do not invent a tool or a successful test.
- Choose delegation in the host when useful and authorized. These skills do not
  require subagents, a fixed number of workers, or proprietary tool names.

## Evaluate before claiming improvement

Use [the behavioral cases](../evals/README.md) with fresh fixtures and sessions.
Compare baseline and candidate instructions on the same host, model, and tools.
Record the actual model identifier and settings supplied by the host; do not
infer model identity from generated prose.

Passing installation tests establishes filesystem compatibility. The existing
OpenCode probe checks skill invocation, not completion of an engineering task.
Neither establishes that a model will produce a working Omarchy UI. Cross-model
claims need actual task traces and artifacts from each named model.
