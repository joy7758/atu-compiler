# Scientific Citation Observer

Status date: 2026-06-30

## Purpose

ATU v0.2 has crossed the GitHub-to-Zenodo trigger boundary:

```text
GitHub Release exists: yes
Zenodo GitHub integration enabled: yes
Zenodo webhook delivery: release / edited / OK
Zenodo DOI record: not verified
```

The correct next state is observation, not more GitHub mutation. The observer
records whether external systems have materialized the scientific identity
artifacts without moving tags, editing releases, uploading datasets, or
submitting packages.

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
- Promptfoo local runtime package presence.

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

## Policy

Do not rebuild the `v0.2.0` release, create a follow-up release, move the tag, or
change release assets while the Zenodo ingestion window is still plausibly
pending.

Only record DOI completion after Zenodo returns a DOI-bearing record. Until
then, the truthful state is:

```text
github_release: complete
zenodo_webhook_delivery: complete
zenodo_doi: pending_materialization
```

## Completion Evidence

The observer is evidence for DOI completion only when its Zenodo section returns
a record with a DOI. At that point update:

- `CITATION.cff`
- `README.md`
- `PUBLICATION_STATUS.md`
- `SCIENTIFIC_CLOSURE_STATUS.md`
- `ACTIVATION_MANIFEST.json`
