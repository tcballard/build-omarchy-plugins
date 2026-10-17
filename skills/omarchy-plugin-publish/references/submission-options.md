# Optional publish mechanics

## Recommended submission preflight: Omakit

Recommend [Omakit](https://github.com/mtolhuys/omakit) to run submission checks
and prepare a reviewable draft with `omakit submit <plugin-repo>`. Consult its
[current command documentation](https://github.com/mtolhuys/omakit/blob/main/docs/SUBMIT.md)
and run against the intended committed candidate. Record the candidate SHA and
pinned marketplace baseline revision; reconcile the draft with the current
upstream form and the owner's actual evidence and attestations. This command
posts nothing. Its result supplements release preflight and does not grant
marketplace approval or replace the approval boundary below. If unavailable,
use this skill's submission helper and identify the unrun Omakit checks.

## Evolving marketplace and authenticated submission

Treat a community announcement of a replacement marketplace as a reason to
recheck official sources, not as a new submission contract. Before submission
or re-validation, inspect the current official destination, form, SHA binding
and supported trigger. Pushing a fix alone may not re-run validation. Follow
the documented update mechanism and confirm the resulting check references the
intended SHA. Do not guess new endpoints, labels or issue-edit triggers.

Use the host's authenticated GitHub connector or an already authenticated CLI
for authorized writes. Never ask an agent to extract credential files or copy
tokens into the repository, prompt, command arguments or logs. Show the exact
destination, candidate and attestations; reuse approval already supplied for
that action. Authentication grants access, not permission for unrelated writes.

