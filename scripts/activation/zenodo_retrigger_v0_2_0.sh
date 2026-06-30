#!/usr/bin/env bash
set -euo pipefail

REPO="joy7758/atu-compiler"
TAG="v0.2.0"
HOOK_ID="647976117"
CONFIRM_VALUE="release-v0.2.0-zenodo-retrigger"

usage() {
  cat <<'EOF'
Usage:
  scripts/activation/zenodo_retrigger_v0_2_0.sh [--dry-run|--execute]

Purpose:
  Trigger a GitHub release webhook delivery for Zenodo without moving the
  v0.2.0 tag or changing release assets.

Default:
  --dry-run

Execution guard:
  To perform the external GitHub Release edit, run:

    ATU_CONFIRM_ZENODO_RETRIGGER=release-v0.2.0-zenodo-retrigger \
      scripts/activation/zenodo_retrigger_v0_2_0.sh --execute

What --execute does:
  1. Reads the current GitHub Release notes for joy7758/atu-compiler v0.2.0.
  2. Appends or refreshes an HTML comment marker.
  3. Calls `gh release edit v0.2.0 --notes-file ...`.
  4. Rechecks the Zenodo webhook deliveries and Zenodo public API.

What it does not do:
  - It does not move or recreate the v0.2.0 git tag.
  - It does not delete or recreate the GitHub Release.
  - It does not upload, remove, or rename release assets.
  - It does not claim that a DOI exists unless Zenodo API returns one.
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

command -v gh >/dev/null
command -v python3 >/dev/null
command -v curl >/dev/null

tmpdir="$(mktemp -d)"
cleanup() {
  rm -rf "$tmpdir"
}
trap cleanup EXIT

body_file="$tmpdir/release-notes.md"
edited_file="$tmpdir/release-notes.edited.md"

gh release view "$TAG" --repo "$REPO" --json body --jq .body > "$body_file"
cp "$body_file" "$edited_file"

timestamp="$(date -u '+%Y-%m-%dT%H:%M:%SZ')"
marker="<!-- atu-zenodo-retrigger: ${timestamp} -->"

python3 - "$edited_file" "$marker" <<'PY'
import pathlib
import re
import sys

path = pathlib.Path(sys.argv[1])
marker = sys.argv[2]
body = path.read_text()
pattern = re.compile(r"\n?<!-- atu-zenodo-retrigger: [^>]+ -->\n?$")
body = pattern.sub("", body).rstrip() + "\n\n" + marker + "\n"
path.write_text(body)
PY

echo "release=${REPO}:${TAG}"
echo "mode=${mode}"
echo "marker=${marker}"
echo "body_changed=$(cmp -s "$body_file" "$edited_file" && echo false || echo true)"

echo
echo "current_hook_deliveries:"
gh api "repos/${REPO}/hooks/${HOOK_ID}/deliveries" \
  --jq '.[0:10] | map({event, action, status, delivered_at})'

echo
echo "current_zenodo_search:"
curl -fsSL 'https://zenodo.org/api/records?q=%22joy7758%2Fatu-compiler%22&sort=mostrecent&size=3' \
  | python3 -c 'import sys,json; data=json.load(sys.stdin); print(json.dumps({"total": data.get("hits",{}).get("total"), "records": [{"id": h.get("id"), "doi": h.get("doi"), "title": h.get("metadata",{}).get("title")} for h in data.get("hits",{}).get("hits",[])]}, indent=2))'

if [[ "$mode" == "--dry-run" ]]; then
  echo
  echo "dry_run=true"
  echo "No external release edit was performed."
  exit 0
fi

if [[ "${ATU_CONFIRM_ZENODO_RETRIGGER:-}" != "$CONFIRM_VALUE" ]]; then
  echo "Missing execution guard: ATU_CONFIRM_ZENODO_RETRIGGER=${CONFIRM_VALUE}" >&2
  exit 78
fi

echo
echo "Executing GitHub Release metadata edit..."
gh release edit "$TAG" --repo "$REPO" --notes-file "$edited_file"

echo
echo "post_edit_release:"
gh release view "$TAG" --repo "$REPO" --json tagName,name,url,isDraft,isPrerelease,publishedAt \
  --jq '{tagName, name, url, isDraft, isPrerelease, publishedAt}'

echo
echo "post_edit_hook_deliveries:"
gh api "repos/${REPO}/hooks/${HOOK_ID}/deliveries" \
  --jq '.[0:10] | map({event, action, status, delivered_at})'

echo
echo "post_edit_zenodo_search:"
curl -fsSL 'https://zenodo.org/api/records?q=%22joy7758%2Fatu-compiler%22&sort=mostrecent&size=3' \
  | python3 -c 'import sys,json; data=json.load(sys.stdin); print(json.dumps({"total": data.get("hits",{}).get("total"), "records": [{"id": h.get("id"), "doi": h.get("doi"), "title": h.get("metadata",{}).get("title")} for h in data.get("hits",{}).get("hits",[])]}, indent=2))'
