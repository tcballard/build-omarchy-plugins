# Build Omarchy Plugins

An installable ChatGPT and Codex plugin for building production-quality
[Omarchy 4](https://omarchy.org/) Quattro shell plugins.

It packages the complete workflow: architecture, repository generation, native
QML patterns, bar widgets, panels and overlays, services and IPC, validation,
debugging, deterministic demos, releases, marketplace publishing, and migration
from older installer-style integrations.

## Why this exists

Omarchy's desktop is one long-running Quickshell process. Third-party plugins
run as unsandboxed user code inside that process, so a useful coding-agent
toolkit needs more than a manifest example. It must understand lifecycle,
multi-monitor state, theme tokens, process boundaries, recovery, reproducible
evidence, and the community marketplace's exact submission contract.

This plugin turns those requirements into focused skills and deterministic
tools.

## Install from GitHub

After this repository is public:

```bash
codex plugin marketplace add tcballard/build-omarchy-plugins
codex plugin add build-omarchy-plugins@tcballard-omarchy
```

In the ChatGPT desktop app, refresh the Plugins Directory after adding the
marketplace, then install **Build Omarchy Plugins** and start a new conversation.

## Skills

| Skill | Purpose |
| --- | --- |
| `omarchy-plugin-design` | Choose kinds, boundaries, state, dependencies, IPC, and evidence before implementation. |
| `omarchy-plugin-scaffold` | Generate a working Quattro plugin repository for any supported kind. |
| `omarchy-qml-patterns` | Implement hosted QML with Omarchy theme, component, process, and state conventions. |
| `omarchy-bar-widget` | Build responsive bar widgets, settings, optional panels, and singleton services. |
| `omarchy-panel-overlay` | Build panels, overlays, and menus with correct lifecycle, focus, and monitor behavior. |
| `omarchy-service-ipc` | Build process-wide services and stable IPC contracts without leaking credentials. |
| `omarchy-plugin-debug` | Diagnose discovery, validation, load, reload, config, and runtime failures. |
| `omarchy-plugin-test` | Run manifest, static security, QML, fixture, and live-shell test layers. |
| `omarchy-plugin-demo` | Create reversible demos and marketplace-ready screenshots using fictional data. |
| `omarchy-plugin-release` | Preflight a clean, documented, reproducible plugin release. |
| `omarchy-plugin-publish` | Prepare and, after owner approval, submit the exact marketplace issue. |
| `omarchy-plugin-migrate` | Separate legacy machine integration from the Quattro shell surface and migrate safely. |

## Deterministic tools

The skills include reusable scripts that:

- generate all six Quattro plugin kinds;
- mirror Omarchy's manifest and path checks without requiring an Omarchy host;
- report advisory marketplace security findings and review capabilities;
- diagnose a local Omarchy installation without mutating it;
- preflight releases and generate exact marketplace submission bodies; and
- produce deterministic OpenAI submission archives and checksums.

Run the repository verification suite with:

```bash
./scripts/test
```

Package the OpenAI submission artifacts with:

```bash
python3 scripts/package_submission.py
```

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
