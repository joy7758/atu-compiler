# Zenodo Release Ingestion Decision

Status date: 2026-07-01

## Current Evidence

ATU `v0.2.0` was enabled in Zenodo only after the original GitHub Release had
already been published, so Zenodo did not ingest that existing release. The
selected closure path was the non-destructive `v0.2.1` activation release.

Observed state:

```text
GitHub Release v0.2.0 published_at: 2026-06-30T11:07:54Z
Zenodo GitHub hook created_at: 2026-06-30T14:20:40Z
Zenodo hook events: release
Hook deliveries seen: release / edited / OK, ping / OK
Hook deliveries not seen: release / published
Zenodo repository-list sync: success alert returned
Zenodo repository detail page: no v0.2.0 release, no DOI
Zenodo API query for joy7758/atu-compiler: total 0
GitHub Release v0.2.1 published_at: 2026-06-30T23:59:42Z
Zenodo record for v0.2.1: https://zenodo.org/records/21087765
Zenodo DOI for v0.2.1: 10.5281/zenodo.21087765
```

Historical machine-readable observer field:

```text
zenodo_ingestion_diagnosis.new_release_published_event_required: true
```

Current machine-readable observer field:

```text
zenodo.doi_status: verified
zenodo.record.doi: 10.5281/zenodo.21087765
zenodo.record.status: published
```

## Interpretation

The existing `v0.2.0` GitHub Release was created before the Zenodo GitHub hook
existed. The later release-notes edit produced a valid `release` / `edited`
delivery, but Zenodo still did not ingest the release. The evidence now points
to a missing `release` / `published` event rather than an ordinary queue delay.

## Source Model

Zenodo's GitHub integration archives releases created after repository
preservation is enabled. GitHub's Zenodo citation guidance also describes the
DOI flow around creating a new GitHub release after the repository is connected.

Reference URLs:

- https://docs.github.com/en/repositories/archiving-a-github-repository/referencing-and-citing-content
- https://help.zenodo.org/docs/github/enable-repository/

## Viable Closure Paths

### Option A: New Patch Release

Create a new patch release, for example `v0.2.1`, after bumping versioned
metadata. This produces a real `release` / `published` event without deleting or
recreating the existing `v0.2.0` release.

Pros:

- Non-destructive.
- Preserves the existing `v0.2.0` release and assets.
- Matches Zenodo's new-release ingestion model.

Cons:

- DOI would attach to `v0.2.1`, not the original `v0.2.0` release.
- Requires metadata update from `0.2.0` to `0.2.1`.

Prepared guardrail:

```bash
make zenodo-v0.2.1-release-dry-run
```

Execution, if explicitly confirmed:

```bash
ATU_CONFIRM_ZENODO_V0_2_1_RELEASE=v0.2.1-zenodo-release \
  scripts/activation/create_v0_2_1_zenodo_release.sh --execute
```

Prepared files:

```text
RELEASE_NOTES_v0.2.1.md
scripts/activation/create_v0_2_1_zenodo_release.sh
```

Prepared metadata boundary:

```text
software_release_version: 0.2.1
atu_ir_profile_version: 0.2.0
```

The script defaults to `--dry-run`, refuses to execute without the environment
guard above, refuses dirty worktrees, and refuses to overwrite an existing
`v0.2.1` local tag, remote tag, or GitHub Release.

### Option B: Delete And Recreate v0.2.0 Release

Delete the GitHub Release object while preserving the `v0.2.0` git tag, then
recreate the GitHub Release and re-upload assets. This may emit a fresh
`release` / `published` event for the original version.

Pros:

- Keeps DOI aligned with `v0.2.0` if Zenodo ingests the recreated release.

Cons:

- Destructive to the GitHub Release object and asset IDs.
- Requires careful asset re-upload and validation.
- Must not be done without explicit confirmation.

### Option C: Manual Zenodo Deposit

Create a direct Zenodo software deposit instead of relying on GitHub auto
archiving.

Pros:

- Does not depend on GitHub webhook behavior.

Cons:

- No longer proves the GitHub-to-Zenodo release integration path.
- Requires a separate Zenodo publication workflow and explicit publication
  confirmation.

## Current Decision

The maintainer selected Option A. The guarded script was executed with explicit
confirmation, creating and publishing `v0.2.1` without moving or rebuilding
`v0.2.0`.

```text
selected_path: create v0.2.1 patch release
execution_guard: ATU_CONFIRM_ZENODO_V0_2_1_RELEASE=v0.2.1-zenodo-release
github_release: https://github.com/joy7758/atu-compiler/releases/tag/v0.2.1
zenodo_record: https://zenodo.org/records/21087765
zenodo_doi: verified
```

The DOI state is now:

```text
zenodo_doi: verified
software_doi: 10.5281/zenodo.21087765
concept_doi: 10.5281/zenodo.21087764
```
