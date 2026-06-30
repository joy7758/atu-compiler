# Zenodo Re-trigger Runbook

Status date: 2026-06-30

## Current State

```json
{
  "repository": "joy7758/atu-compiler",
  "release": "v0.2.0",
  "zenodo_github_integration": "enabled",
  "github_webhook": "active",
  "github_webhook_deliveries": "ping_only_no_release_delivery",
  "zenodo_record_search": "total_0",
  "doi_status": "not_verified"
}
```

## Boundary

This runbook prepares a Zenodo ingestion trigger. It must not be interpreted as
evidence that a DOI exists.

Do not move `v0.2.0`. Do not delete the release unless the lower-impact trigger
has failed and the user has explicitly confirmed a release recreation plan.

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

The action is intentionally lower impact than deleting and recreating the
GitHub Release, but Zenodo may still ignore an `edited` release event. If that
happens, the next candidate action is a confirmed release-object recreation for
the existing `v0.2.0` tag.

## Completion Evidence

The Zenodo gate is complete only when a Zenodo API response returns a DOI for
the ATU release, for example:

```json
{
  "doi": "10.5281/zenodo.xxxxxxxx",
  "title": "ATU v0.2: Agent Trace-to-Dataset Compiler"
}
```

After DOI verification, update:

- `CITATION.cff`
- `README.md`
- `PUBLICATION_STATUS.md`
- `SCIENTIFIC_CLOSURE_STATUS.md`
- `ACTIVATION_MANIFEST.json`
