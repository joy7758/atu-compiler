# Zenodo Re-trigger Runbook

Status date: 2026-07-01

## Current State

```json
{
  "repository": "joy7758/atu-compiler",
  "release": "v0.2.0",
  "zenodo_github_integration": "enabled",
  "github_webhook": "active",
  "github_webhook_deliveries": "release_edited_delivery_ok_then_v0_2_1_release_created_ok",
  "zenodo_record_search": "v0_2_1_record_verified",
  "zenodo_record": "https://zenodo.org/records/21087765",
  "doi_status": "verified"
}
```

## Boundary

This runbook records the lower-impact `release` / `edited` trigger attempt. The
edited trigger itself must not be interpreted as evidence that a DOI exists.

Do not move `v0.2.0`. Do not delete or recreate the release. Later observer
evidence showed that the edited attempt did not produce a DOI, so the closure
path moved to the guarded `v0.2.1` activation release documented in
`docs/zenodo-release-ingestion-decision.md`.

## Prepared Command

Dry run:

```bash
scripts/activation/zenodo_retrigger_v0_2_0.sh --dry-run
```

External action:

```bash
ATU_CONFIRM_ZENODO_RETRIGGER=release-v0.2.0-zenodo-retrigger \
  scripts/activation/zenodo_retrigger_v0_2_0.sh --execute
```

## Expected Effect

The script performs a minimal GitHub Release notes edit by appending or
refreshing an HTML comment marker. This should create a GitHub `release`
webhook delivery without changing the tag or release assets.

The action was intentionally lower impact than deleting and recreating the
GitHub Release. It created a GitHub `release` / `edited` delivery, not a
new release event. After the executed attempt failed to produce a Zenodo
record, the decision moved to the guarded new-release path in
`docs/zenodo-release-ingestion-decision.md`, which has now been executed.

## Executed Re-trigger

The guarded lower-impact re-trigger was executed once:

```text
executed_at: 2026-06-30T14:43:22Z
release_marker: <!-- atu-zenodo-retrigger: 2026-06-30T14:43:22Z -->
github_delivery: release / edited / OK at 2026-06-30T14:43:30.23Z
zenodo_api_after_retrigger: total 0 at 2026-06-30T14:45:55Z
```

This proves Zenodo received a GitHub `release` webhook delivery for the edited
release. It does not prove DOI creation. Later observer evidence showed that
`v0.2.0` predates the Zenodo hook and that no new-release archival event existed
for that original release. The selected next action was:

```text
docs/zenodo-release-ingestion-decision.md
```

Guarded safe-path dry run:

```bash
make zenodo-v0.2.1-release-dry-run
```

Execution was completed after explicit maintainer confirmation:

```bash
ATU_CONFIRM_ZENODO_V0_2_1_RELEASE=v0.2.1-zenodo-release \
  scripts/activation/create_v0_2_1_zenodo_release.sh --execute
```

Observer command:

```bash
make scientific-activation-observe
```

## Completion Evidence

The Zenodo gate is complete because the Zenodo API response now returns a DOI
for the ATU activation release:

```json
{
  "doi": "10.5281/zenodo.21087765",
  "conceptdoi": "10.5281/zenodo.21087764",
  "title": "ATU v0.2.1: Agent Trace-to-Dataset Compiler",
  "version": "0.2.1",
  "status": "published"
}
```

DOI verification has been propagated into:

- `CITATION.cff`
- `README.md`
- `PUBLICATION_STATUS.md`
- `SCIENTIFIC_CLOSURE_STATUS.md`
- `ACTIVATION_MANIFEST.json`
