#!/usr/bin/env bash
set -euo pipefail

REPO="joy7758/atu-compiler"
CURRENT_TAG="v0.2.0"
PATCH_TAG="v0.2.1"
HOOK_ID="647976117"

usage() {
  cat <<'EOF'
Usage:
  scripts/activation/zenodo_release_published_event_plan.sh [--dry-run]

Purpose:
  Print the exact Zenodo closure choices after the edited-release re-trigger
  failed to make Zenodo ingest v0.2.0.

This script is read-only. It does not create tags, releases, assets, or DOI
records. Its output is intended to support an explicit maintainer confirmation.
EOF
}

if [[ "${1:---dry-run}" != "--dry-run" ]]; then
  usage >&2
  exit 64
fi

command -v gh >/dev/null

echo "repo=${REPO}"
echo "current_tag=${CURRENT_TAG}"
echo "patch_tag=${PATCH_TAG}"
echo

echo "github_release:"
gh release view "$CURRENT_TAG" --repo "$REPO" \
  --json tagName,isDraft,isPrerelease,publishedAt,url,targetCommitish \
  --jq '{tagName,isDraft,isPrerelease,publishedAt,url,targetCommitish}'

echo
echo "zenodo_hook:"
gh api "repos/${REPO}/hooks/${HOOK_ID}" \
  --jq '{active,created_at,events,name,updated_at}'

echo
echo "zenodo_hook_deliveries:"
gh api "repos/${REPO}/hooks/${HOOK_ID}/deliveries" \
  --jq '.[0:10] | map({event, action, status, status_code, delivered_at})'

echo
echo "diagnosis:"
cat <<'EOF'
v0.2.0 was published before the Zenodo hook was created.
The hook has seen release/edited but not release/published.
Zenodo UI and API still show no ATU release DOI.
EOF

echo
echo "option_a_safe_patch_release:"
cat <<'EOF'
Prepare a v0.2.1 patch-release commit:
  - bump pyproject.toml version to 0.2.1
  - bump CITATION.cff version to 0.2.1
  - bump .zenodo.json version to 0.2.1
  - add RELEASE_NOTES_v0.2.1.md
  - commit and push main/release/v0.2.0
Then, after explicit confirmation:
  git tag -a v0.2.1 -m "ATU v0.2.1 Zenodo activation release"
  git push origin v0.2.1
  gh release create v0.2.1 \
    --repo joy7758/atu-compiler \
    --title "ATU v0.2.1 - Zenodo Activation Release" \
    --notes-file RELEASE_NOTES_v0.2.1.md \
    --latest=false
EOF

echo
echo "option_b_version_exact_recreate:"
cat <<'EOF'
After explicit confirmation only:
  - download existing v0.2.0 release assets
  - save existing v0.2.0 release notes
  - delete the GitHub Release object without deleting the v0.2.0 git tag
  - recreate GitHub Release v0.2.0 with the same notes/assets
  - verify a release/published hook delivery
This preserves the version label but mutates the public GitHub Release object
and asset IDs.
EOF

echo
echo "completion_check:"
cat <<'EOF'
After either option:
  make scientific-activation-observe
  curl -fsSL 'https://zenodo.org/api/records?q=%22joy7758%2Fatu-compiler%22&sort=mostrecent&size=10'
Only record completion after a DOI-bearing Zenodo record appears.
EOF
