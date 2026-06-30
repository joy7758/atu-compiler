#!/usr/bin/env bash
set -euo pipefail

REPO="joy7758/atu-compiler"
TAG="v0.2.1"
BASE_TAG="v0.2.0"
HOOK_ID="647976117"
NOTES_FILE="RELEASE_NOTES_v0.2.1.md"
CONFIRM_VALUE="v0.2.1-zenodo-release"

usage() {
  cat <<'EOF'
Usage:
  scripts/activation/create_v0_2_1_zenodo_release.sh [--dry-run|--execute]

Purpose:
  Create a guarded v0.2.1 GitHub Release to generate a real GitHub
  release/published event after Zenodo preservation was enabled.

Default:
  --dry-run

Execution guard:
  To perform the external tag push and GitHub Release creation, run:

    ATU_CONFIRM_ZENODO_V0_2_1_RELEASE=v0.2.1-zenodo-release \
      scripts/activation/create_v0_2_1_zenodo_release.sh --execute

What --execute does:
  1. Verifies the worktree is clean.
  2. Verifies v0.2.1 does not already exist locally, on origin, or as a GitHub
     Release.
  3. Creates annotated tag v0.2.1 at the current commit.
  4. Pushes tag v0.2.1 to origin.
  5. Creates GitHub Release v0.2.1 with RELEASE_NOTES_v0.2.1.md.
  6. Rechecks the Zenodo webhook deliveries and public Zenodo API.

What it does not do:
  - It does not move v0.2.0.
  - It does not delete or recreate the v0.2.0 GitHub Release.
  - It does not claim a Zenodo DOI unless a DOI-bearing Zenodo API record exists.
EOF
}

mode="--dry-run"
if [[ "${1:-}" == "--execute" || "${1:-}" == "--dry-run" ]]; then
  mode="$1"
elif [[ "${1:-}" == "-h" || "${1:-}" == "--help" ]]; then
  usage
  exit 0
elif [[ -n "${1:-}" ]]; then
  usage >&2
  exit 64
fi

command -v git >/dev/null
command -v gh >/dev/null
command -v curl >/dev/null
command -v python3 >/dev/null

if [[ ! -f "$NOTES_FILE" ]]; then
  echo "Missing release notes: $NOTES_FILE" >&2
  exit 66
fi

pyproject_version_ready=false
citation_version_ready=false
zenodo_version_ready=false
package_version_ready=false

if grep -q '^version = "0\.2\.1"$' pyproject.toml; then
  pyproject_version_ready=true
fi
if grep -q '^version: "0\.2\.1"$' CITATION.cff; then
  citation_version_ready=true
fi
if grep -q '"version": "0\.2\.1"' .zenodo.json; then
  zenodo_version_ready=true
fi
if grep -q '^__version__ = "0\.2\.1"$' src/atu/__init__.py; then
  package_version_ready=true
fi

head_sha="$(git rev-parse HEAD)"
branch="$(git rev-parse --abbrev-ref HEAD)"
status_short="$(git status --short)"
local_tag_exists=false
remote_tag_exists=false
release_exists=false

if git rev-parse -q --verify "refs/tags/${TAG}" >/dev/null; then
  local_tag_exists=true
fi
if git ls-remote --exit-code --tags origin "refs/tags/${TAG}" >/dev/null 2>&1; then
  remote_tag_exists=true
fi
if gh release view "$TAG" --repo "$REPO" >/dev/null 2>&1; then
  release_exists=true
fi

echo "repo=${REPO}"
echo "mode=${mode}"
echo "branch=${branch}"
echo "head=${head_sha}"
echo "base_tag=${BASE_TAG}"
echo "new_tag=${TAG}"
echo "notes_file=${NOTES_FILE}"
echo "software_release_version=0.2.1"
echo "atu_ir_profile_version=0.2.0"
echo "pyproject_version_ready=${pyproject_version_ready}"
echo "citation_version_ready=${citation_version_ready}"
echo "zenodo_version_ready=${zenodo_version_ready}"
echo "package_version_ready=${package_version_ready}"
echo "worktree_clean=$([[ -z "$status_short" ]] && echo true || echo false)"
echo "local_tag_exists=${local_tag_exists}"
echo "remote_tag_exists=${remote_tag_exists}"
echo "github_release_exists=${release_exists}"

echo
echo "current_base_release:"
gh release view "$BASE_TAG" --repo "$REPO" \
  --json tagName,isDraft,isPrerelease,publishedAt,url,targetCommitish \
  --jq '{tagName,isDraft,isPrerelease,publishedAt,url,targetCommitish}'

echo
echo "current_zenodo_hook:"
gh api "repos/${REPO}/hooks/${HOOK_ID}" \
  --jq '{active,created_at,events,name,updated_at}'

echo
echo "current_zenodo_hook_deliveries:"
gh api "repos/${REPO}/hooks/${HOOK_ID}/deliveries" \
  --jq '.[0:10] | map({event, action, status, status_code, delivered_at})'

if [[ "$mode" == "--dry-run" ]]; then
  echo
  echo "dry_run=true"
  echo "No tag, release, asset, or DOI mutation was performed."
  exit 0
fi

if [[ "${ATU_CONFIRM_ZENODO_V0_2_1_RELEASE:-}" != "$CONFIRM_VALUE" ]]; then
  echo "Missing execution guard: ATU_CONFIRM_ZENODO_V0_2_1_RELEASE=${CONFIRM_VALUE}" >&2
  exit 78
fi
if [[ -n "$status_short" ]]; then
  echo "Worktree is not clean; commit or stash changes before release execution." >&2
  git status --short >&2
  exit 70
fi
if [[ "$pyproject_version_ready" != true || "$citation_version_ready" != true || "$zenodo_version_ready" != true || "$package_version_ready" != true ]]; then
  echo "v0.2.1 release metadata is incomplete; refusing release execution." >&2
  exit 65
fi
if [[ "$local_tag_exists" == true || "$remote_tag_exists" == true || "$release_exists" == true ]]; then
  echo "v0.2.1 tag or GitHub Release already exists; refusing to overwrite." >&2
  exit 73
fi

echo
echo "Creating annotated tag ${TAG} at ${head_sha}..."
git tag -a "$TAG" -m "ATU v0.2.1 Zenodo activation release"

echo
echo "Pushing tag ${TAG}..."
git push origin "$TAG"

echo
echo "Creating GitHub Release ${TAG}..."
gh release create "$TAG" \
  --repo "$REPO" \
  --title "ATU v0.2.1 - Zenodo Activation Release" \
  --notes-file "$NOTES_FILE" \
  --latest=false

echo
echo "post_release:"
gh release view "$TAG" --repo "$REPO" \
  --json tagName,isDraft,isPrerelease,publishedAt,url,targetCommitish \
  --jq '{tagName,isDraft,isPrerelease,publishedAt,url,targetCommitish}'

echo
echo "post_release_zenodo_hook_deliveries:"
gh api "repos/${REPO}/hooks/${HOOK_ID}/deliveries" \
  --jq '.[0:10] | map({event, action, status, status_code, delivered_at})'

echo
echo "post_release_zenodo_search:"
curl -fsSL 'https://zenodo.org/api/records?q=%22joy7758%2Fatu-compiler%22&sort=mostrecent&size=10' \
  | python3 -c 'import sys,json; data=json.load(sys.stdin); print(json.dumps({"total": data.get("hits",{}).get("total"), "records": [{"id": h.get("id"), "doi": h.get("doi"), "title": h.get("metadata",{}).get("title")} for h in data.get("hits",{}).get("hits",[])]}, indent=2))'
