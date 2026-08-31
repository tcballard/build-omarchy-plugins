# Releasing

Releases are owner-controlled and pull-request-only. Automation may build,
attest, and recover a **draft** release; it never publishes one.

## Prepare through a pull request

1. Update `VERSION`, manifests, changelog, submission copy, and tests on a
   branch.
2. Run `./scripts/test` and
   `python3 scripts/package_submission.py --require-clean`.
3. Merge the reviewed pull request only after `CI / Required` succeeds.
4. Fetch `main`, confirm it is clean and exactly matches `origin/main`, then
   create and push an annotated `vX.Y.Z` tag. Never move a release tag.
5. Manually run **Release draft** with that existing tag. The workflow requires
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
