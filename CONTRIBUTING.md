# Contributing

Keep changes focused on the observable Omarchy plugin-development workflow.

1. Branch from `main`.
2. Update the smallest relevant skill, reference, script, or template.
3. Add a behavioral test for script or generator changes.
4. Run `./scripts/test`.
5. Explain the user-visible outcome and the Omarchy contract relied upon.

Do not copy whole upstream manuals into references. Preserve progressive
disclosure: routing and invariants belong in `SKILL.md`; substantial conditional
detail belongs in a linked reference; deterministic mechanics belong in scripts.

Changes to marketplace rules or Omarchy schema assumptions must identify the
upstream source and verification date. Security findings must remain
deterministic, documented, and clearly distinguished from proof of safety.
