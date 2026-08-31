# Contributing

Keep changes focused on the observable Omarchy plugin-development workflow.

1. Branch from `main`. Never commit directly to `main`; every change goes
   through a pull request, including owner-authored release work.
2. Update the smallest relevant file under the canonical root `skills/`, or an
   adapter-specific file when the change is genuinely host-specific.
3. Add a behavioral test for script or generator changes.
4. Run `python3 scripts/sync_openai_adapter.py --write` after changing a
   portable skill.
5. Run `./scripts/test`.
6. Open a focused pull request and wait for the stable `CI / Required` check.
7. Explain the user-visible outcome and the Omarchy contract relied upon.

Do not copy whole upstream manuals into references. Preserve progressive
disclosure: routing and invariants belong in `SKILL.md`; substantial conditional
detail belongs in a linked reference; deterministic mechanics belong in scripts.

Changes to marketplace rules or Omarchy schema assumptions must identify the
upstream source and verification date. Security findings must remain
deterministic, documented, and clearly distinguished from proof of safety.

Keep the version in root `plugin.json` and the OpenAI adapter manifest aligned.
Do not add provider-specific instructions or UI metadata to the portable skill
tree; place those in the relevant adapter.

Upstream contract changes must update `contracts/upstream-contracts.json` in a
reviewed PR, including the immutable commit, exact document digest, review date,
and assumptions affected. A moving upstream branch is never consumed directly
by a release.
