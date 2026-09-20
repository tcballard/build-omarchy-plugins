# Build Omarchy Plugins

<p>
  <a href="https://github.com/tcballard/build-omarchy-plugins/actions/workflows/ci.yml"><img alt="CI status" height="20" src="https://github.com/tcballard/build-omarchy-plugins/actions/workflows/ci.yml/badge.svg?branch=main"></a>
  <a href="LICENSE"><img alt="License: MIT" height="20" src="https://img.shields.io/badge/license-MIT-blue?style=flat-square"></a>
  <a href="https://github.com/tcballard/omarchy-badges"><img alt="Built for Omarchy: Plugin" height="20" src="https://raw.githubusercontent.com/tcballard/omarchy-badges/75975e5b5bf75e7ede3764bcd2950046f7abfe2c/badges/v1/omarchy-plugin.svg"></a>
  <a href="#compatibility"><img alt="Supported Omarchy versions: 4.0.0+" height="20" src="https://raw.githubusercontent.com/tcballard/omarchy-badges/dd84bb21f19caf617caa5b3c1af7ff3c6cb847c3/badges/v1/compatibility/omarchy-4.0.0-plus.svg"></a>
</p>

A model-provider-neutral Agent Plugin for building production-quality
[Omarchy 4](https://omarchy.org/) Quattro shell plugins.

It packages the complete workflow: architecture, repository generation, native
QML patterns, bar widgets, panels and overlays, services and IPC, validation,
debugging, deterministic demos, releases, marketplace publishing, and migration
from older installer-style integrations.

## Compatibility

This toolkit targets **Omarchy 4.0.0 and later with Quattro shell-plugin support**.
The badge refers to the installed Omarchy version, reported by `omarchy-version`,
not the ISO image version or the underlying Quickshell engine version.
That is the scope of the maintained guidance and generators, not a claim that
every current or future Omarchy release has been tested. The `4.0.0+` label
has no upper major-version bound; compatibility changes will be documented here. Individual APIs and marketplace
contracts are pinned in [the contract ledger](contracts/upstream-contracts.json).

The CI badge reports this repository's `main` workflow status. Portable tests
validate tooling and generated output; they do not establish live desktop
compatibility for every generated plugin. See [acceptance evidence](evals/ACCEPTANCE.md)
for completed checks and outstanding behavioural or live-host testing.
Projects built with the bundle must declare and test their own supported range.

## Why this exists

Omarchy's desktop is one long-running Quickshell process. Third-party plugins
run as unsandboxed user code inside that process, so a useful coding-agent
toolkit needs more than a manifest example. It must understand lifecycle,
multi-monitor state, theme tokens, process boundaries, recovery, reproducible
evidence, and the community marketplace's exact submission contract.

This project turns those requirements into focused Agent Skills and
deterministic tools. The portable package uses the open Agent Plugins 1.0.0
layout. An OpenAI plugin remains available as one distribution adapter.

## What "provider neutral" means

The twelve skills do not call a model API, require a hosted service, or depend
on provider-specific tools. The agent host chooses the model and supplies its
normal file and shell capabilities. Provider-specific manifests and UI metadata
live only in distribution adapters.

The repository root is a portable Agent Plugin:

```text
plugin.json
skills/
  omarchy-plugin-design/
  ...
```

See [PORTABILITY.md](PORTABILITY.md) for the tested host paths and exact
compatibility boundary.

For Astra, Claude Fable and other frontier models, see the
[usage guide](docs/FRONTIER-MODELS.md) and
[behavioral evaluation cases](evals/README.md). The skills keep model selection
in the host and scale their workflow to the requested change.

## Install the Agent Skills

Clone a reviewed release, then install the skills into the shared interoperable
location used by Codex, Cursor, Gemini CLI, and OpenCode:

This checkout targets **v0.4.1**. Download published, checksummed assets from
[GitHub Releases](https://github.com/tcballard/build-omarchy-plugins/releases).
The commands below target v0.4.1; use them once that release is published.
A draft release or a newer `main` checkout is not a published release.

```bash
git clone --branch v0.4.1 --depth 1 https://github.com/tcballard/build-omarchy-plugins.git
cd build-omarchy-plugins
python3 scripts/install_agent_skills.py --target agents --scope user
```

Host-specific locations are also supported:

```bash
python3 scripts/install_agent_skills.py --target codex --scope user
python3 scripts/install_agent_skills.py --target cursor --scope user
python3 scripts/install_agent_skills.py --target gemini --scope user
python3 scripts/install_agent_skills.py --target claude --scope user
python3 scripts/install_agent_skills.py --target opencode --scope user
```

Use `--scope project` to install into the current repository, `--skill NAME` to
install a subset, or `--target generic --destination PATH` for another
Agent-Skills-compatible host. Existing differing skill directories are never
overwritten unless `--force` is supplied explicitly.

## Update, inspect, and remove

The installer writes a receipt containing exact file hashes and modes. Preview
every lifecycle change before applying it:

```bash
git fetch --tags
git checkout v0.4.1
python3 scripts/install_agent_skills.py --target agents --scope user --update --diff
python3 scripts/install_agent_skills.py --target agents --scope user --update
```

If a managed file changed locally, update and removal stop. Inspect the diff;
use `--force` only when replacing that named managed copy is intentional.
Removal is equally explicit and leaves unrelated skills untouched:

```bash
python3 scripts/install_agent_skills.py --target agents --scope user --uninstall --diff
python3 scripts/install_agent_skills.py --target agents --scope user --uninstall
```

Inspect discovery, duplicate names, hashes, and executable modes without
starting the host:

```bash
python3 scripts/doctor_agent_skills.py --host opencode --json
```

The doctor reports filesystem evidence only; it cannot claim a model or host
invocation succeeded. See [PORTABILITY.md](PORTABILITY.md) for the tested host
matrix and OpenCode's optional deny-by-default live probe.

## Install the OpenAI plugin

For ChatGPT and Codex plugin distribution:

```bash
codex plugin marketplace add tcballard/build-omarchy-plugins
codex plugin add build-omarchy-plugins@tcballard-omarchy
```

In ChatGPT, refresh the Plugins Directory after adding the marketplace, then
install **Build Omarchy Plugins** and start a new conversation.

## Start here

Use the [workflow guide](docs/WORKFLOWS.md) to choose an entry point, follow a
new build through the skills, or take the shorter path for a fix, demo or
release. Each skill defines the inputs it uses and the evidence it hands on.

## Skills

| Skill | Purpose |
| --- | --- |
| [omarchy-plugin-design](skills/omarchy-plugin-design/SKILL.md) | Choose kinds, boundaries, state, dependencies, IPC, and evidence before implementation. |
| [omarchy-plugin-scaffold](skills/omarchy-plugin-scaffold/SKILL.md) | Generate a working Quattro plugin repository for any supported kind. |
| [omarchy-qml-patterns](skills/omarchy-qml-patterns/SKILL.md) | Implement hosted QML with Omarchy theme, component, process, and state conventions. |
| [omarchy-bar-widget](skills/omarchy-bar-widget/SKILL.md) | Build responsive bar widgets, settings, optional panels, and singleton services. |
| [omarchy-panel-overlay](skills/omarchy-panel-overlay/SKILL.md) | Build panels, overlays, and menus with correct lifecycle, focus, and monitor behavior. |
| [omarchy-service-ipc](skills/omarchy-service-ipc/SKILL.md) | Build process-wide services and stable IPC contracts without leaking credentials. |
| [omarchy-plugin-debug](skills/omarchy-plugin-debug/SKILL.md) | Diagnose discovery, validation, load, reload, config, and runtime failures. |
| [omarchy-plugin-test](skills/omarchy-plugin-test/SKILL.md) | Run manifest, static security, QML, fixture, and live-shell test layers. |
| [omarchy-plugin-demo](skills/omarchy-plugin-demo/SKILL.md) | Create reversible demos and marketplace-ready screenshots using fictional data. |
| [omarchy-plugin-release](skills/omarchy-plugin-release/SKILL.md) | Preflight a clean, documented, reproducible plugin release. |
| [omarchy-plugin-publish](skills/omarchy-plugin-publish/SKILL.md) | Prepare and, after owner approval, submit the exact marketplace issue. |
| [omarchy-plugin-migrate](skills/omarchy-plugin-migrate/SKILL.md) | Separate legacy machine integration from the Quattro shell surface and migrate safely. |

## Deterministic tools

The portable skills include reusable scripts that:

- generate all six Quattro plugin kinds;
- mirror Omarchy's manifest and path checks without requiring an Omarchy host;
- report advisory marketplace security findings and review capabilities;
- diagnose a local Omarchy installation without mutating it;
- preflight releases and generate exact marketplace submission bodies;
- install safely into supported agent-host skill locations; and
- produce deterministic portable Agent Plugin and OpenAI submission archives.

Run the repository verification suite with:

```bash
./scripts/test
```

Package all distribution artifacts with:

```bash
python3 scripts/package_submission.py --output-dir dist --require-clean --git-tree HEAD
```

This produces the portable Agent Plugin, the OpenAI plugin, the OpenAI skills
upload, reviewer materials, strict source/release manifests, an SPDX 2.3 SBOM,
and one checksum manifest. Artifacts are built from the exact committed Git
tree rather than ambient working files.

## Plugin Workbench companion

[Plugin Workbench](https://github.com/tcballard/omarchy-plugin-workbench) is the
default local lifecycle companion for projects created by this toolkit. New
scaffolds include a schema-one `.omarchy-workbench.json` definition that points
to the root plugin, proposes `./tests/run` as an exact-argv check and
capability-gated validation workflow, and declares Git, Python, and optional
Omarchy environment probes.

Workbench can then register the checkout for validation, live linking,
snapshots, rollback, and enable/disable operations. Registration does not trust
or execute the generated commands; the user must review the definition and
approve project commands and workflow capabilities explicitly. The Workbench contract is vendored and pinned in
[`contracts/upstream-contracts.json`](contracts/upstream-contracts.json).

## Scope

The default target is an Omarchy 4 Quattro shell plugin: a public Git repository
with `manifest.json` and QML at its root. Older Omarchy integrations that install
packages, systemd units, or privileged helpers are treated as a separate machine
integration layer. The migration skill preserves that layer when it is genuinely
required instead of pretending Quattro's no-install-hook model can replace it.

## Safety boundary

Generated and reviewed Omarchy plugins are still unsandboxed third-party code.
The static checks in this project are advisory and cannot prove that a plugin is
safe. Review source and dependencies before enabling any plugin.

## Support and policies

- [Support](SUPPORT.md)
- [Security](SECURITY.md)
- [Privacy](PRIVACY.md)
- [Terms](TERMS.md)
- [Contributing](CONTRIBUTING.md)

## License

MIT

## Claude Code plugin (v0.4.1)

Native Claude Code packaging was introduced in v0.3.1. From a reviewed v0.4.1 checkout,
validate and try the plugin locally:

```bash
claude plugin validate .
claude --plugin-dir .
```

The repository marketplace tracks the default branch. To install it in Claude
Code:

```text
/plugin marketplace add tcballard/build-omarchy-plugins
/plugin install build-omarchy-plugins@tcballard-omarchy
```

Use either this plugin or the existing `--target claude` skills installer to
avoid loading duplicate skills. The v0.4.1 release build includes a separate
`build-omarchy-plugins-claude-plugin-0.4.1.zip`, with the same twelve canonical
skills and their helpers. This is a community marketplace, not an official
Anthropic listing. OpenAI and Anthropic marketplace submissions remain on hold
while stewardship is discussed.

See [maintenance and adoption](docs/MAINTENANCE.md) for ownership decisions and
[acceptance evidence](evals/ACCEPTANCE.md) for what has actually been exercised.
