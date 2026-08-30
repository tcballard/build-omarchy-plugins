---
name: omarchy-plugin-scaffold
description: Create a new Omarchy 4 Quattro shell-plugin repository or add its initial supported entry points. Use for manifest, QML, tests, CI, demo, license, and README scaffolding; not for overwriting an established plugin.
---

# Omarchy Plugin Scaffold

Generate a working repository, then validate the generated result.

## Create a repository

Run the bundled generator from this skill directory:

```bash
python3 scripts/new_plugin.py \
  --id io.github.owner.plugin-name \
  --name "Plugin Name" \
  --kind bar-widget \
  --author "Author Name" \
  --output /absolute/path/to/plugin-name
```

Repeat `--kind` for a justified multi-kind plugin. The generator supports
`bar-widget`, `panel`, `overlay`, `menu`, `service`, and `bar`.

Read [references/generated-layout.md](references/generated-layout.md) when
selecting optional flags or extending the output.

## Guardrails

- Inspect the target first. The generator refuses a non-empty destination and
  never merges into an existing repository.
- Use a globally unique, lowercase, reverse-domain-style ID. Treat it as
  permanent once published.
- Choose the smallest kind set. A common rich widget uses `service` plus
  `bar-widget`; do not declare kinds without corresponding functionality.
- Keep external installation outside the shell-plugin scaffold. Document
  required packages and let users install them explicitly.
- Generated QML is functional baseline code, not final product design. Replace
  the sample state and copy while preserving the lifecycle and injection
  contracts.

After generation, run the generated `./tests/run` and the current toolkit
validator from `omarchy-plugin-test`. On an Omarchy machine also run:

```bash
omarchy plugin validate /absolute/path/to/plugin-name
```
