# Submission checklist

## Completed evidence

- [x] Skills-only plugin; no MCP server or app connector.
- [x] Plugin metadata, logo, composer icon, and screenshot are included.
- [x] Website, support, privacy, terms, security, and license documents exist.
- [x] `tcballard/build-omarchy-plugins` is public and its policy files are present.
- [x] Twelve skill routes have descriptions and interface metadata.
- [x] Five positive and five negative routing tests are documented.
- [x] All six current Omarchy shell plugin kinds have generated fixtures.
- [x] Traversal, symlink, and unsafe download-to-shell cases are tested.
- [x] The full repository suite passes from a clean checkout.
- [x] Submission archives are deterministic and have SHA-256 checksums.
- [x] Release notes and reviewer reproduction steps are included.

## Owner-controlled final gate

- [ ] Merge the reviewed release pull request only after `CI / Required` succeeds.
- [ ] Create the immutable annotated release tag from the merged `main` commit.
- [ ] Sign in to the OpenAI platform with Apps Management write permission.
- [ ] Complete or confirm the publisher identity verification.
- [ ] Select the intended country availability.
- [ ] Review and truthfully accept the portal's current attestations.
- [ ] Upload the skills archive, copy the prepared fields, and submit for review.

These items cannot be pre-checked by a build tool because they depend on the
owner's account, distribution decision, and legal attestations.
