# Portability

Build Omarchy Plugins separates portable engineering behavior from host-specific
distribution.

## Portable core

The repository root conforms to Agent Plugins 1.0.0:

- `plugin.json` is the portable manifest.
- `skills/` contains twelve Agent Skills.
- Skills contain only standard `SKILL.md`, scripts, references, and assets.
- No skill calls a model-provider API or requires authentication.

The model is selected by the agent host. Changing from an OpenAI model to
Anthropic, Google, a local model, or another provider does not change the skill
package or its Omarchy tools.

## Host adapters

| Host | Project location | User location | Repository verification |
| --- | --- | --- | --- |
| Shared Agent Skills | `.agents/skills/` | `~/.agents/skills/` | Install and idempotency tested |
| Codex | `.agents/skills/` | `~/.agents/skills/` | Install tested; OpenAI plugin separately validated |
| Cursor | `.cursor/skills/` | `~/.cursor/skills/` | Install tested; portable Agent Plugin emitted |
| Gemini CLI | `.gemini/skills/` | `~/.gemini/skills/` | Install tested; `.agents/skills` also supported |
| Claude Code | `.claude/skills/` | `~/.claude/skills/` | Install tested |
| OpenCode | `.opencode/skills/` | `~/.config/opencode/skills/` | Native install and idempotency tested; `.agents/skills` also supported |
| Other hosts | User-supplied destination | User-supplied destination | Generic copy and conflict behavior tested |

The repository tests filesystem installation and package structure. It does not
claim that every host/model combination has completed a live behavioral eval.
Inspect effective copies and duplicate-name ambiguity without starting a host:

```bash
python3 scripts/doctor_agent_skills.py --host opencode --json
```

The doctor compares content hashes and executable modes against the portable
source. Its `hostVerified` and `providerVerified` fields are always false because
filesystem inspection is not a host invocation.

OpenCode also has a built-in, deny-by-default live probe:

```bash
python3 scripts/host_conformance.py --host opencode --invoke --model provider/model --json
```

The probe uses `opencode --pure`, disables plugins, LSP downloads, sharing, and
auto-update, denies every tool by default, and permits only `read`, `glob`,
`grep`, and `skill`. A verified claim requires an exact effective install, an
observed native `skill` tool call, the expected response marker, and clean Git
attribution for the source. `--custom-command` and `--eval-hook` outputs are
recorded only as operator-controlled self-report and can never promote either
verification field.

Discovery details are conservative. OpenCode and Cursor duplicate-name
precedence is treated as ambiguous because their public skill documentation does
not define a winner. Claude enterprise, plugin, added-directory, and synced
sources are reported as blind spots instead of being silently ignored. The same
positive and negative cases in `submission/evals.json` remain the baseline for
behavioral host testing.

## OpenAI adapter

`plugins/build-omarchy-plugins/` is the OpenAI distribution adapter. Its skill
content is generated from the portable root, while `agents/openai.yaml`, artwork,
and `.codex-plugin/plugin.json` remain adapter-owned.

After changing a portable skill, refresh and verify the adapter:

```bash
python3 scripts/sync_openai_adapter.py --write
python3 scripts/sync_openai_adapter.py --check
```

CI rejects drift between the portable skill files and the OpenAI copy.

## Safety and overwrite behavior

The installer copies only named skill directories. It preflights every selected
skill before writing, treats byte-identical copies as already installed, and
refuses conflicting directories by default. `--force` replaces only the
explicitly selected conflicting skill directories; it never clears the parent
skills directory or unrelated skills.

Portable packages reject symlinks so resources cannot escape the package
boundary.
