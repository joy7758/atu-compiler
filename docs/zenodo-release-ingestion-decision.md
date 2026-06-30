# Zenodo Release Ingestion Decision

Status date: 2026-06-30

## Current Evidence

ATU v0.2.0 is enabled in Zenodo, but Zenodo has not ingested the existing
GitHub Release.

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
```

Machine-readable observer field:

```text
zenodo_ingestion_diagnosis.new_release_published_event_required: true
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

Do not mutate `v0.2.0` again automatically. The next external action requires
an explicit maintainer decision between:

```text
recommended_safe_path: create v0.2.1 patch release
version_exact_path: delete and recreate GitHub Release v0.2.0 without moving tag
manual_deposit_path: create Zenodo deposit directly
```

Until one of those actions succeeds and a DOI-bearing Zenodo record is
verified, the DOI state remains:

```text
zenodo_doi: not_verified
```
