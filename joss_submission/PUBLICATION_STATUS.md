# ATU v0.2 / v0.2.1 Publication Status

Status date: 2026-07-01

## Completed External Actions

- GitHub repository created: `https://github.com/joy7758/atu-compiler`
- GitHub visibility: public
- GitHub default branch: `main`
- Branch pushed: `main`
- Branch pushed: `release/v0.2.0`
- Tag pushed: `v0.2.0`
- GitHub Release created: `https://github.com/joy7758/atu-compiler/releases/tag/v0.2.0`
- GitHub Release assets uploaded:
  - `atu_v0.2_joss_submission.zip`
  - `CITATION.cff`
  - `default.zenodo.json`
  - `RELEASE_NOTES_v0.2.0.md`
- Zenodo GitHub integration enabled for `joy7758/atu-compiler`.
- GitHub webhook for Zenodo release events is active.
- Latest activation recheck: `2026-06-30T14:29:06Z`.
- Zenodo re-trigger dry-run command prepared and verified:
  `make zenodo-retrigger-dry-run`.
- Zenodo re-trigger executed at `2026-06-30T14:43:22Z` by editing GitHub
  Release notes with an HTML comment marker.
- GitHub webhook delivery after re-trigger: `release` / `edited` / `OK` at
  `2026-06-30T14:43:30.23Z`.
- Zenodo activation GitHub Release created:
  `https://github.com/joy7758/atu-compiler/releases/tag/v0.2.1`.
- Tag pushed: `v0.2.1`
- Zenodo activation release published at `2026-06-30T23:59:42Z`.
- Zenodo hook deliveries after `v0.2.1`: `release` / `created` / `OK` with
  status code `202`, `release` / `published` with status code `409`, and
  `release` / `released` with status code `403`.
- Zenodo DOI minted and verified:
  `https://doi.org/10.5281/zenodo.21087765`.
- Zenodo concept DOI verified: `https://doi.org/10.5281/zenodo.21087764`.
- Zenodo record: `https://zenodo.org/records/21087765`.
- Zenodo archive file: `joy7758/atu-compiler-v0.2.1.zip`, size `745012`,
  checksum `md5:01cc153a59416dfa43e7041a6cfd72ba`.
- Scientific activation observer prepared:
  `make scientific-activation-observe`.
- Latest observer run: `2026-07-01T00:15:05Z`; Zenodo DOI status was
  `verified`, Hugging Face dataset was visible, and Promptfoo runtime artifact
  passed.
- Zenodo release-published event plan prepared and dry-run verified:
  `make zenodo-release-published-event-plan`.
- Guarded `v0.2.1` Zenodo activation release path executed:
  `RELEASE_NOTES_v0.2.1.md`,
  `scripts/activation/create_v0_2_1_zenodo_release.sh`, and
  `make zenodo-v0.2.1-release-dry-run`.
- Software release metadata prepared for the guarded path:
  `pyproject.toml`, `src/atu/__init__.py`, `CITATION.cff`, and `.zenodo.json`
  now report `0.2.1`; ATU-IR/profile schema identifiers and existing dataset
  episode metadata remain `0.2.0`.
- Hugging Face dataset created and populated at
  `https://huggingface.co/datasets/joy7759/atu-trace-1000`.
- HF data commit: `945c6e2` uploaded `data/eval.jsonl`, `data/test.jsonl`, and
  `data/train.jsonl`.
- HF root metadata commit: `54bd194` uploaded `README.md` and
  `dataset_infos.json`.
- HF README update commit: `be34a82` removed stale pre-upload wording from the
  live dataset card.
- HF `dataset_infos.json` update commit: `fd0da1d` replaced stale `local-only`
  homepage metadata with the live dataset URL.
- User confirmed `joy7759` and `joy7758` are the same owner identity for this
  publication; HF canonical URL is therefore `joy7759/atu-trace-1000`.
- Manual GitHub observer workflow active: `Scientific Activation Observer`
  (`workflow_dispatch` only). The workflow skips repository webhook-delivery
  inspection because that API is not available to the default `GITHUB_TOKEN`;
  local authenticated observer runs include it. CI-side hook diagnosis is
  therefore `indeterminate_without_repo_hook_delivery_permission`; CI-side HF
  checks use the public Hugging Face API when the `hf` CLI is unavailable.
- Latest GitHub observer workflow run: `28466699508`, conclusion `success`,
  head SHA `bcf03b9610ada5975966f3c450f4fb3b5c9612eb`, artifact
  `scientific-activation-observer` / `7989891992`. Its CI-side observer result
  reported Zenodo query total `0`, Hugging Face dataset `visible` via public
  API, Promptfoo passed, and hook-delivery diagnosis
  `indeterminate_without_repo_hook_delivery_permission`.
- Manual Zenodo browser check at `2026-06-30T15:23:16Z`: repository remains
  enabled, repository-list sync completed, but the Zenodo repository detail page
  still showed no `v0.2.0` release and no DOI.
- Manual Zenodo browser check at `2026-06-30T17:47:29Z`: repository remains
  enabled. `Sync now` returned the Zenodo success alert, but after reload the
  `joy7758/atu-compiler` detail page still showed no `v0.2.0` release and no
  DOI.

## Verified Local/Package Actions

- `make publication-bundles` passed.
- ATU JSONL schema validation passed for 3 episodes.
- Hugging Face JSON loader validation passed:
  - train: 1 row
  - eval: 1 row
  - test: 1 row
- JOSS zip exists: `atu_v0.2_joss_submission.zip`
- JOSS final zip exists: `atu_v0.2_joss_submission_final.zip`
- JOSS zip has no `__pycache__`, `.pyc`, `node_modules`, or `.git` entries.
- Citation bundle exists: `citation_bundle/`
- HF upload mirror exists: `hf_dataset/atu_trace_1000/`
- Promptfoo local package exists: `evals/promptfoo/`
- Promptfoo local runtime artifact exists:
  `evals/promptfoo/results/promptfoo-atu-v0.2.0-20260630T170204Z.json`
- Promptfoo local eval result: `3 passed`, `0 failed`, `0 errors`.
- Remote HF `dataset_infos.json` now reports homepage
  `https://huggingface.co/datasets/joy7759/atu-trace-1000`.

## Not Completed Externally

- Zenodo DOI gate is complete for software release `v0.2.1`. The original
  `v0.2.0` GitHub Release still predates the Zenodo hook and remains without a
  separate Zenodo DOI, but the citable software artifact is now the `v0.2.1`
  Zenodo activation release.
- Promptfoo share has not been completed. Local runtime evidence exists, but no
  external Promptfoo share URL has been created or recorded.
- JOSS submission has not been submitted to JOSS. The local submission package
  zip was generated only. Browser check showed the JOSS submission entry
  requires ORCID login before a submission can be started.
- OpenInference and Promptfoo upstream PRs have not been opened. Drafts exist
  in `PR_OPENINFERENCE.md` and `PR_PROMPTFOO.md`.

## Next Manual Gates

1. Decide whether to create a Promptfoo share URL. Do not claim external
   Promptfoo publication until that URL exists.
2. Log in with ORCID before starting the JOSS submission workflow.
3. Open upstream issues or pull requests using the prepared PR draft files.
