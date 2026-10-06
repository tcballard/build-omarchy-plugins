# Start a project

Requires Node.js 22 or later, Git, and GitHub CLI for remote configuration. No npm install is needed.

1. On GitHub, choose **Use this template → Create a new repository**, using only the default branch. Clone the new repository.
2. Before editing the starter files, run (replace these example values):

```bash
node scripts/init.mjs --owner your-account --repo your-repository --slug your-project --name "Your Project" --author "Your Name" --description "What it does"
./tests/run
git diff
```

The ID defaults to io.github.OWNER.SLUG with hyphens replaced by underscores. Set --id explicitly for a different permanent identity. An --inspiration HTTPS_URL adds prominent credit. An identical second run is harmless; identity changes after initialization require a reviewed migration. Edited starter files and symlinks cause setup to stop before writing.

3. Commit and push the initial setup. Ensure the CI workflow runs successfully.
4. Preview and then apply the repository policy using an authenticated GitHub CLI account with admin access:

```bash
node scripts/github.mjs
node scripts/github.mjs --apply
```

This enables squash merges, automatic branch deletion, auto-merge availability, appropriate topics and an active main ruleset requiring PRs and green CI. It blocks force pushes and branch deletion. It does not require another reviewer, create bypass actors, or change existing rulesets. Private repository rulesets depend on your GitHub plan; an API failure is reported rather than silently ignored.

Template changes do not propagate automatically into generated repositories. Keep the recorded templateVersion and apply later maintenance through reviewed PRs.
