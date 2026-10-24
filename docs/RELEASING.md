# Releasing

Releases are owner-controlled and pull-request-only. Automation may build,
attest, and recover a **draft** release; it never publishes one.

## Prepare through a pull request

1. Update `VERSION`, manifests, changelog, submission copy, and tests on a
   branch.
2. Run `./scripts/test` and
   `python3 scripts/package_submission.py --require-clean`.
3. Merge the reviewed pull request only after `CI / Required` succeeds.
4. Run **Release draft** from `main`, supply the new `vX.Y.Z` tag, enable
   `create_tag`, and paste the full reviewed main SHA into `expected_commit`.
   It creates an annotated tag only when the tag does not exist, the workflow
   commit is still current main, VERSION matches and required CI passed.
   Alternatively create and push the annotated tag locally after the same checks.
   Never move a release tag.
5. To recover a draft, run **Release draft** with the existing tag and leave
   `create_tag` disabled. The workflow requires
   an annotated tag at the current remote `main`, a successful required CI
   check on the same commit, two byte-identical builds, valid checksums, and a
   provenance attestation. A rerun may recover only an existing draft.

## Owner publication gate

Use an authenticated `gh` session with repository administration read access.
Set `tag` to the exact draft tag and run each command immediately before
publication:

```bash
set -euo pipefail
repo="tcballard/build-omarchy-plugins"
tag="vX.Y.Z"

gh api -H "X-GitHub-Api-Version: 2026-03-10" "repos/$repo/immutable-releases" --jq '.enabled == true'
test "$(gh api "repos/$repo/releases/tags/$tag" --jq .draft)" = true

git fetch origin main "refs/tags/$tag:refs/tags/$tag"
test "$(git cat-file -t "refs/tags/$tag")" = tag
commit="$(git rev-list -n 1 "refs/tags/$tag")"
test "$commit" = "$(git ls-remote origin refs/heads/main | cut -f1)"
test "$(git rev-parse "refs/tags/$tag")" = "$(git ls-remote origin "refs/tags/$tag" | cut -f1)"

checks="$(gh api --paginate "repos/$repo/commits/$commit/check-runs" --jq '.check_runs[] | select(.name == "CI / Required") | .conclusion')"
test "$(printf '%s\n' "$checks" | tail -n 1)" = success

assets="$(mktemp -d)"
gh release download "$tag" --repo "$repo" --dir "$assets"
(cd "$assets" && sha256sum --check SHA256SUMS)
gh release edit "$tag" --repo "$repo" --draft=false --latest
gh release verify "$tag" --repo "$repo"
```

If the immutable-releases check is false or unavailable, stop and enable the
repository setting before publishing. If any tag, main, CI, checksum, draft, or
asset check changes, stop and rebuild a new draft; do not repair a published
release or move its tag.

## Historical v0.3.0 exception

The published v0.3.0 uses a lightweight tag. Its eight assets were built twice
from commit `e1ddd609ade020467c3ba529c07dcde9b7e753cd`, compared byte-for-byte,
and uploaded manually; they have checksums and source manifests but **no GitHub
Actions provenance attestation**. The new workflow does not retrofit or replace
that release. Use a new version for the next release and verify its generated
attestation as well as its downloaded checksums.

Claude manifest and marketplace schema validation uses the official CLI:
`npx --yes @anthropic-ai/claude-code@2.1.269 plugin validate . --strict` and the
same command against `.claude-plugin/plugin.json`. Recheck the pinned CLI version
when changing packaging. This command validates packaging; it does not run Fable.
