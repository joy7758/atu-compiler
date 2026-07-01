# Scientific Citation Observer

Status date: 2026-07-01

## Purpose

ATU v0.2 has crossed the GitHub-to-Zenodo citation boundary through the
non-destructive `v0.2.1` activation release:

```text
GitHub Release v0.2.0 exists: yes
GitHub Release v0.2.1 exists: yes
Zenodo GitHub integration enabled: yes
Zenodo webhook delivery: release / created / OK for v0.2.1
Zenodo repository-list sync: completed
Zenodo DOI record: verified
Zenodo DOI: 10.5281/zenodo.21087765
Zenodo concept DOI: 10.5281/zenodo.21087764
Zenodo record: https://zenodo.org/records/21087765
Observer diagnosis: DOI-bearing record present
```

The correct next state is continued observation and downstream status
synchronization, not more GitHub mutation. The observer records whether
external systems have materialized the scientific identity artifacts without
moving tags, editing releases, uploading datasets, or submitting packages.

## Command

```bash
make scientific-activation-observe
```

GitHub manual workflow:

```text
Actions -> Scientific Activation Observer -> Run workflow
```

The command emits JSON with these read-only checks:

- GitHub Release state.
- Zenodo GitHub webhook deliveries.
- Zenodo public API search for the repository and release title.
- Hugging Face dataset visibility.
- Promptfoo local runtime package and latest result artifact status.
- Zenodo ingestion diagnosis, including whether the release predates the
  Zenodo hook and whether a `release` / `published` delivery exists.

HF upload has a separate pre-upload identity gate:

```bash
make hf-canonical-identity-check
```

That gate is also read-only. It succeeds when `hf auth whoami` resolves to
`joy7759`, the live namespace for `joy7759/atu-trace-1000`. The user confirmed
on 2026-06-30 that `joy7759` and GitHub namespace `joy7758` are the same owner
identity for this publication.

Network behavior: one flaky external endpoint should not fail the whole
observer. Zenodo API checks retry before returning an `ok: false` JSON section.

The GitHub workflow is `workflow_dispatch` only. It is not scheduled, and it
does not mutate tags, releases, assets, Zenodo, Hugging Face, Promptfoo, or JOSS.
The workflow intentionally skips the repository webhook-delivery API because
GitHub Actions `GITHUB_TOKEN` does not have the repository-hook permission needed
for that endpoint. Local authenticated runs still check webhook deliveries.
When hook delivery inspection is skipped, the Zenodo ingestion diagnosis is
`indeterminate_without_repo_hook_delivery_permission`, not a DOI or closure
signal. The Hugging Face dataset check falls back to the public Hub API when the
`hf` CLI is unavailable in CI.

## Policy

Do not rebuild the `v0.2.0` release, move either tag, or change release assets
to chase the DOI. The citable software artifact is the `v0.2.1` Zenodo
activation release, while the original `v0.2.0` GitHub Release remains the
stable compiler release boundary.

DOI completion is recorded only because Zenodo returned a DOI-bearing record:

```text
github_release: complete
zenodo_activation_release: complete
zenodo_repository_list_sync: complete
zenodo_doi: verified
zenodo_record: https://zenodo.org/records/21087765
promptfoo_local_runtime: complete_if_latest_result_passed
```

A Zenodo repository-list sync success alert is evidence that Zenodo refreshed
the GitHub repository list. It is not evidence that a GitHub release was
ingested or that a DOI was minted. Likewise, the historical GitHub `release` /
`edited` webhook delivery for `v0.2.0` is not equivalent to a new release event
for Zenodo archival. That historical path is documented in
`docs/zenodo-retrigger.md`; the selected closure path is documented in
`docs/zenodo-release-ingestion-decision.md`.

## Completion Evidence

The observer is evidence for DOI completion because its Zenodo section returns
the expected record:

```json
{
  "doi_status": "verified",
  "record": {
    "record_id": 21087765,
    "doi": "10.5281/zenodo.21087765",
    "conceptdoi": "10.5281/zenodo.21087764",
    "status": "published",
    "state": "done",
    "submitted": true,
    "title": "ATU v0.2.1: Agent Trace-to-Dataset Compiler",
    "version": "0.2.1"
  }
}
```

The DOI state has been propagated into:

- `CITATION.cff`
- `README.md`
- `PUBLICATION_STATUS.md`
- `SCIENTIFIC_CLOSURE_STATUS.md`
- `ACTIVATION_MANIFEST.json`
