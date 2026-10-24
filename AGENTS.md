# Repository guidance

Read CONTRIBUTING.md. Edit canonical skills/ files, then regenerate the OpenAI
copies with `python3 scripts/sync_openai_adapter.py --write`. Run `./scripts/test`.
Use branches and PRs; wait for CI / Required. Live desktop testing and releases
remain separate actions.

Default to code without comments. Delete narration and commented-out code; express
intent through names, structure and checks. Keep legal notices, public contracts,
required directives and proven external constraints. Preserve pinned source bytes,
frozen fixtures and generated files. Fix workarounds before deleting explanations.
