# Frontier-model review — 12 September 2026

Reviewed base: `b6ad3c3d95f561883ebcfb3ecec01ffd1e474bd5`.
Scope: all twelve skill entrypoints, linked workflow guidance relevant to the
findings, adapter synchronization, portability/conformance tools, routing cases,
and the repository verification suite. This is an agent-workflow review with
targeted code inspection, not a complete security or current Omarchy API audit.

## Assessment

The core is worth keeping. Focused skills, conditional references, deterministic
scaffolding, explicit host lifecycle contracts, and a generated OpenAI adapter
already suit capable coding models. A separate Astra fork would create avoidable
drift. The main opportunities are removing accidental workflow gates and testing
observable task completion. The original entrypoints are already short; a
wholesale rewrite or a universal orchestration prompt is unnecessary.

## Findings and changes

| Priority | Evidence at reviewed base | Consequence | Resolution |
| --- | --- | --- | --- |
| P2 | `scripts/host_conformance.py`, final `payload.get` expression evaluates `payload['error']` even on success. Reproduced with `python3 scripts/host_conformance.py --host codex`. | Normal text output crashes with `KeyError: 'error'`; JSON-only tests missed it. | Explicit success/error formatting; subprocess regression covers both text paths. |
| P2 | `scripts/doctor_agent_skills.py`, Codex roots include only repo root and user directory and assign precedence ranks. | Nested working directories can lose visible skills; duplicates can be presented as one effective winner. | Inspect the ancestor chain and report duplicate ambiguity. Preserve the portable audit's symlink exclusion and disclose it. |
| P2 | Design skill ends with “after the design record is agreed”; debug demands authorization “immediately before” live changes. | Literal instruction following can stop requested implementation or re-ask for already supplied authorization. | Continue authorized implementation; preserve design-only scope; reuse specific existing authorization while keeping live desktop and publication boundaries. |
| P2 | Debug always calls the full test skill; test/QML guidance makes broad state and lifecycle coverage appear universal. | Small fixes can expand into irrelevant tests or stall on missing Omarchy access. | Select checks by changed behavior, retain required repository and release gates, disclose unavailable host evidence. |
| P2 | Debug, demo, release, publish and test use `python3 scripts/...` without locating the loaded skill. | Commands can fail or execute a same-named project helper from another working directory. | Resolve helpers from the loaded `SKILL.md` directory; scaffold uses the same convention. |
| P3 | Scaffold directs Workbench registration and trust when installed; migration routing eval specifies two repositories. | Optional integration and a layout example can override a narrower user request. | Make registration optional, retain trust authorization, and preserve requested repository layout. |
| P3 | Publication guidance calls the 29 August snapshot “current”. | A strong model can confidently prepare or submit an obsolete contract. | Label the snapshot as pinned; verify live form/destination before submission; mark offline drafts unverified. No new marketplace schema is claimed here. |
| P3 | Routing cases check expected result shapes; OpenCode probe asks for a skill title/nonce. | Neither demonstrates a completed build, correct async behavior, or restrained scope. | Add eight task-level behavioral cases and record smoke-test limits separately from host discovery. |

The Codex discovery change follows the documented ancestor scan and separate
display of duplicate names. Source reviewed on 12 September:
[Build skills](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills).

## Coverage across the twelve skills

| Skill | Tailoring |
| --- | --- |
| Design | Continue requested builds; reuse specs; consider app versus shell interaction. |
| Scaffold | Absolute helper path, completion beyond sample code, optional Workbench registration. |
| QML patterns | Relevant state tests and honest headless evidence. |
| Bar widget | Preserve API/settings for narrow fixes. |
| Panel/overlay | Repair affected lifecycle paths without adding windows or kinds. |
| Service/IPC | Explicit ownership of late asynchronous results. |
| Debug | Enter at known failing boundary, scoped tests, reusable authorization. |
| Test | Select dependent layers; finish portable work; retain required gates. |
| Demo | Distinguish harness preparation from observed capture. |
| Release | Complete preparation before a missing permission/host gate; retain source/tag integrity. |
| Publish | Verify contract freshness; preserve attestations and existing specific approval. |
| Migrate | Separate responsibilities without forcing two repositories. |

## Validation and limits

- Baseline: all 50 deterministic tests and package/adapter checks passed.
- Baseline `repair-panel` fresh agent session: corrected the manifest mapping;
  doctor, generated tests, portable validation and advisory scan passed.
- Candidate `repair-panel` fresh agent session: corrected the same mapping;
  doctor and generated tests passed; no live host claim. Both versions completed
  this case; this is regression evidence, not demonstrated superiority.
- Candidate `build-focus` fresh agent session: generated the correct identity
  and `bar-widget` kind, implemented local Focus/Paused state and orientation
  branches, and passed generated tests, toolkit validation/advisory scan and demo
  fixture output. Parent inspection confirmed these code paths exist. Actual
  QML loading, input and layout remain unrun; the demo output is not UI evidence.
  A follow-up reminded this session to finish portable checks and disclose the
  unavailable runtime, so this is a steered smoke test, not an unassisted benchmark.
- Candidate: all 52 deterministic tests, portable/OpenAI validators, contract
  checks, adapter synchronization and deterministic packaging passed locally.
  The text conformance command now completes without the reproduced exception.

Agent sessions use the current inherited model and tool environment; they do not
establish external-provider compatibility or a measured Astra performance gain.
No live Omarchy desktop or real marketplace submission was exercised. The other
behavioral cases remain a repeatable evaluation backlog, not claimed passes.

## Follow-up

Run paired tasks in the actual Astra host and each other model/host intended for
support, recording model settings and artifacts. Use real Omarchy for window,
focus, monitor, reload, install and removal evidence. Separately refresh pinned
upstream contracts when changing Omarchy or marketplace compatibility; that
requires source-specific verification beyond this prompting revision.
