---
name: omarchy-plugin-scaffold
description: Create a new Omarchy 4 Quattro shell-plugin repository or add its initial supported entry points. Use for manifest, QML, tests, CI, demo, license, and README scaffolding; not for overwriting an established plugin.
---

# Scaffold an Omarchy plugin

Inspect the destination and retain agreed ID, kinds and scope. For a small built-in customization use `omarchy plugin clone <id>` and edit the user copy instead. Read the installed Omarchy guide first; never edit packaged shell files.

Resolve `<skill-dir>` to this skill's directory, independently of the project or agent host. For a minimal plugin:

```bash
python3 "<skill-dir>/scripts/new_plugin.py" \
  --id io.github.owner.plugin-name --name "Plugin Name" \
  --kind bar-widget --author "Author Name" --output /absolute/path/to/plugin
```

Repeat `--kind` only for implemented surfaces. Supported kinds: `bar-widget`, `panel`, `overlay`, `menu`, `service`, `bar`. The generator refuses a non-empty destination.

For an optional full GitHub repository starter, read [repository template](references/repository-template.md). It requires Node.js 22+, an unused destination and no network. GitHub configuration is a separate step. Read [generated layout](references/generated-layout.md) for optional flags, badges and companion integrations; none is a prerequisite to building a plugin.

Keep external installation explicit, action SHA pins intact, external text plain, and agent configuration outside installed runtime code. Replace sample behavior with the requested feature.

Run generated `./tests/run` and the toolkit validator when available. On Omarchy also run `omarchy plugin validate <path>`, then enable and verify the local result when requested. Report the actual entry points, results and unrun host checks. A generated scaffold alone does not complete a feature request.
