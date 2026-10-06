# Full GitHub repository starter

Use this route for a new bar-widget repository with the shared project defaults.
Use `new_plugin.py` for other kinds or multi-kind scaffolds. Do not run either
generator over an existing repository, and do not run them over each other.
When extending this starter, add the selected surface's actual entry points and
update its manifest and tests together.

## Generate offline

Requires Node.js 22 or later; no npm installation, network access, Python or
GitHub credentials are needed for generation. The destination must be an
absolute path that does not exist, with an existing parent directory.

```bash
node "<skill-dir>/scripts/new_repository.mjs" \
  --output /absolute/path/to/my-plugin \
  --owner your-account --repo omarchy-my-plugin --slug my-plugin \
  --id io.github.your_account.my_plugin \
  --name "My Plugin" --author "Your Name" \
  --description "What the plugin does"
```

The ID is permanent once published. Set it explicitly; the default derives it
from the owner and slug. Optional `--inspiration https://...` adds prominent
original-project credit; `--year 2026` fixes the copyright year.

The helper verifies the complete bundled snapshot, initializes and checks a
temporary copy, then creates the destination exclusively. Invalid input and
existing files, directories or symlinks are rejected without replacing them.
Generation never initializes Git, creates a remote, configures GitHub or applies
desktop changes. A copy failure may leave the newly created partial directory;
inspect it before removing or retrying.

## Included defaults and validation

The starter includes a root manifest and stateless `StarterWidget.qml`, a
centered README with the Plugin badge and credits, MIT licence, project
instructions, Workbench definition, development and acceptance documents,
issue/PR forms, pinned CI, draft source-release workflow, and GitHub setup tool.
MIT is the starter default; establish licences for new code and reused assets.
It has no real screenshots, desktop acceptance or marketplace listing.

The manifest maps `bar-widget` to `StarterWidget.qml`. Run `./tests/run` from the
generated repository (Bash required). For portable Node checks, including from
Windows without Bash, run:

```bash
node scripts/check.mjs
node --test tests/template.test.mjs
```

Also run the loaded `omarchy-plugin-test` validator when available. This
template's Node checks cover a narrower structural subset. Follow the normal
test skill and installed Omarchy validator for runtime and release evidence.

After reviewing and committing the result, push its `main` branch and let CI
pass. Preview `node scripts/github.mjs`; apply with `--apply` only when remote
configuration is authorized. The tool requires an authenticated GitHub CLI
with repository administration access. It configures topics, squash merges,
branch deletion after merge, and an active main ruleset requiring PRs and the
`verify` check, with no force pushes or bypass actors. Existing policies are
not replaced. GitHub template creation does not copy these repository settings.
See the generated `docs/SETUP.md` for the complete setup procedure.

## Provenance and maintenance

`assets/repository-template/` is an exact MIT-licensed copy of
`tcballard/omarchy-plugin-template` at
`f99681e69937d21c2d4414ac9f65a0fd01fea714` (template version 0.1.0).
`assets/repository-template.lock.json` records the source commit, SHA-256 digest
and Git mode of every file. `new_repository.mjs --check` detects added, missing
or changed files and rejects symlinks. This checks the reviewed local lock; it
is not a signature or an online assertion about upstream's current branch.

Integration version 1 makes two explicit compatibility adjustments in the
generated copy: normalize relative paths to `/`, and use `fileURLToPath` for
the check/setup CLI entry points. These keep initialization and checks working
on Windows and in paths containing spaces. The source snapshot remains intact;
`.template/source.json` in each generated project records the pin and adjustments.

To update, review a specific upstream commit, replace the snapshot from its
Git tree without `.git`, regenerate its file hashes and modes in the lock, and
review whether the compatibility patches are still needed. Run the generation,
installation and archive tests, refresh the OpenAI adapter, and submit the
snapshot, lock and any patch changes together. Do not fetch moving `main` at
scaffold time or silently update existing generated projects.
