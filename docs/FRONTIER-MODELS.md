# Use with any coding agent

The skills teach Omarchy development, not a model API or agent runtime. Native discovery is optional: an agent with file access can read the relevant `SKILL.md` and follow linked references. Keep model choice, effort, planning, delegation and permission configuration in the host.

Give the agent a concrete outcome, target checkout and available capabilities. For example:

> Build a small Omarchy focus widget in this repository. Use the installed Omarchy guide and the relevant Build Omarchy Plugins skills. Show 25:00 and toggle Focus/Paused on click. Support both bar orientations. No service, persistence or network. Implement and validate it; report any live checks you cannot run.

Load only the relevant surface skill and references. Resolve helper paths from the loaded skill's directory, not the plugin checkout. The instructions themselves require only file access; Python helpers and the optional Node repository starter declare their runtimes separately. Use existing project records for continuity rather than introducing a required handoff template.

If a display, sibling skill, tool or authenticated capability is unavailable, finish independent work and report the exact dependent check as unrun. Read-only advice stays read-only; implementation does not imply release or marketplace publication.

For the Agents-panel starter and local customization, see [host workflow](../skills/omarchy-plugin-design/references/host-workflow.md). For routing and completion, see [workflows](WORKFLOWS.md).

## Evaluation boundary

Use [task cases](../evals/README.md) and [handoff cases](../evals/HANDOFFS.md) against fresh fixtures. Judge implementation, scope and observed results rather than prescribed wording, tool names or worker count. A successful run on one model/harness is evidence for that run, not universal compatibility or improved model performance.

The [12 September frontier review](reviews/2026-09-12-frontier-skills.md) and [Fable review](reviews/2026-09-12-fable-skills.md) remain historical records. They are not current model recommendations or installation requirements. This filename is retained for existing links.
