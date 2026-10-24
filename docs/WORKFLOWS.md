# Choose the smallest useful workflow

Read the installed Omarchy guide and relevant project instructions first. Use only the skills needed for the requested outcome; no fixed sequence, plan format, delegation model or agent-specific tool is required. The twelve skill names remain stable, and each can be installed separately. If a sibling is absent, finish independent work and identify any missing prerequisite rather than inventing a tool.

| Request | Start with | Completion |
| --- | --- | --- |
| Agents panel → Plugin | Built-in Omarchy guide, then design/scaffold and the relevant implementation skill | Requested interaction works and is enabled locally, or exact live checks are disclosed as unrun. |
| Personal built-in tweak | `omarchy plugin clone`, then the relevant surface skill | User-owned clone implements the change without editing packaged files. |
| New plugin | Design → scaffold → relevant surface → affected checks | Smallest requested behavior, actual source and relevant verification. |
| Existing widget/panel/service change | Bar widget, panel/overlay or service/IPC; QML patterns as needed | Focused patch preserving settled APIs and settings. |
| Broken plugin | Debug; test after an authorized repair | Cause and recommendation for diagnosis-only; correction and observed checks for repair. |
| Screenshot/demo | Demo | Fictional fixtures, real capture when available and restoration evidence. |
| Legacy integration | Migrate | Requested shell surface moves while helper, credentials and data retain ownership. |
| Release | Release | Source/version/assets reconciled, required evidence and unresolved gates explicit. |
| Marketplace preparation/submission | Publish | Exact-SHA draft or authorized remote write, verified against current official contract. |

Keep ordinary widget options inline in `shell.json`. Shared theme styling belongs to theme skills; a single plugin's incorrect token binding belongs to QML patterns. Use plugin-owned translation catalogs and current placement APIs only after checking host support.

See [the host workflow](../skills/omarchy-plugin-design/references/host-workflow.md) for the exact Agents-panel prompt and companion-skill usage. That button launches the configured default agent with the built-in guide; it does not automatically load this bundle.

Helpers use the loaded skill's absolute directory, not the current project directory. Python 3 is required for the bundled Python tools; the optional full repository starter requires Node.js 22+. Reading the instructions requires neither runtime. Workbench, Omakit, VM tooling and provider adapters are optional integrations, not prerequisites for plugin development.

Carry forward existing decisions, actual changed files and source-bound results in the project's own format. Evidence may refer to commit plus working changes or a fixture digest. Later source edits invalidate affected results. Never turn scaffold validation, a prepared harness or an issue submission into a claim of runtime correctness, release publication or marketplace approval.

For substantial changes, use the [behavioral cases](../evals/README.md) and [handoff cases](../evals/HANDOFFS.md). Their criteria describe outcomes, not tool-call sequences.
