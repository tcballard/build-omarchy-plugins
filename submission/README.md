# Submission packet

This directory is the reviewer-ready packet for **Build Omarchy Plugins 0.2.2**.
It accompanies the skills-only archive produced by `scripts/package_submission.py`.

## Portal files

- `portal-field-map.md` — copy-ready values and owner-controlled choices.
- `listing.md` — marketplace title and descriptions.
- `starter-prompts.md` — the three initial prompts shown to users.
- `test-cases.md` and `evals.json` — five positive and five negative routing tests.
- `skills-inventory.md` — each bundled skill and its activation boundary.
- `reviewer-notes.md` — architecture, permissions, privacy, and safety notes.
- `release-notes.md` — first-release notes.
- `submission-checklist.md` — evidence and the final owner-only actions.

## Rebuild

From the repository root:

```bash
./scripts/test
python3 scripts/package_submission.py
(cd dist && sha256sum -c SHA256SUMS)
```

Submit `dist/build-omarchy-plugins-skills-0.2.2.zip` as the skill bundle. Keep the
full plugin archive for direct Codex installation and the submission archive for
reviewer records.
