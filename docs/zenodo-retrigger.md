# Zenodo Re-trigger Runbook

Status date: 2026-06-30

## Current State

```json
{
  "repository": "joy7758/atu-compiler",
  "release": "v0.2.0",
  "zenodo_github_integration": "enabled",
  "github_webhook": "active",
  "github_webhook_deliveries": "release_edited_delivery_ok",
  "zenodo_record_search": "total_0",
  "doi_status": "not_verified"
}
```

## Boundary

This runbook records the lower-impact `release` / `edited` trigger attempt. It
must not be interpreted as evidence that a DOI exists.

Do not move `v0.2.0`. Do not delete or recreate the release while Zenodo DOI
materialization is still plausibly pending.

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
GitHub Release. After the action is executed, switch to read-only monitoring
unless new evidence shows that Zenodo will not harvest the queued event.

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
`v0.2.0` predates the Zenodo hook and that no `release` / `published` delivery
exists. The current next action is not another edited re-trigger; use:

```text
docs/zenodo-release-ingestion-decision.md
```

Observer command:

```bash
make scientific-activation-observe
```

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
