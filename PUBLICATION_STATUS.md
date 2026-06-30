# ATU v0.2.0 Publication Status

Status date: 2026-06-30

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
- Scientific activation observer prepared:
  `make scientific-activation-observe`.
- Latest observer run: `2026-06-30T16:01:46Z`; Zenodo query total remained
  `0`, Hugging Face dataset was visible, and Promptfoo runtime remained absent.
- Hugging Face dataset created and populated at
  `https://huggingface.co/datasets/joy7759/atu-trace-1000`.
- HF data commit: `945c6e2` uploaded `data/eval.jsonl`, `data/test.jsonl`, and
  `data/train.jsonl`.
- HF root metadata commit: `54bd194` uploaded `README.md` and
  `dataset_infos.json`.
- HF README update commit: `be34a82` removed stale pre-upload wording from the
  live dataset card.
- User confirmed `joy7759` and `joy7758` are the same owner identity for this
  publication; HF canonical URL is therefore `joy7759/atu-trace-1000`.
- Manual GitHub observer workflow active: `Scientific Activation Observer`
  (`workflow_dispatch` only). The workflow skips repository webhook-delivery
  inspection because that API is not available to the default `GITHUB_TOKEN`;
  local authenticated observer runs include it.
- Latest GitHub observer workflow run: `28454815985`, conclusion `success`,
  artifact `scientific-activation-observer` / `7984877361`.
- Manual Zenodo browser check at `2026-06-30T15:23:16Z`: repository remains
  enabled, repository-list sync completed, but the Zenodo repository detail page
  still showed no `v0.2.0` release and no DOI.

## Verified Local/Package Actions

- `make publication-bundles` passed.
- ATU JSONL schema validation passed for 3 episodes.
- Hugging Face JSON loader validation passed:
  - train: 1 row
  - eval: 1 row
  - test: 1 row
- JOSS zip exists: `atu_v0.2_joss_submission.zip`
- JOSS final zip exists: `atu_v0.2_joss_submission_final.zip`
- JOSS zip has no `__pycache__` or `.pyc` entries.
- Citation bundle exists: `citation_bundle/`
- HF upload mirror exists: `hf_dataset/atu_trace_1000/`
- Promptfoo local package exists: `evals/promptfoo/`

## Not Completed Externally

- Zenodo DOI has not been verified. The repository is enabled in Zenodo, but
  the Zenodo repository detail page has not ingested the existing `v0.2.0`
  GitHub release. A lower-impact GitHub Release metadata edit successfully
  delivered a `release` / `edited` webhook event to Zenodo. Exact Zenodo API
  searches still returned `total: 0` at `2026-06-30T14:45:55Z`, so DOI is
  pending materialization, not verified failed.
- Promptfoo share has not been completed. `npx promptfoo` startup hung during
  package bootstrap in this environment and was interrupted.
- Promptfoo local package metadata exists in `evals/promptfoo/package.json`, but
  `npm install --no-audit --no-fund` again produced no output for 90 seconds and
  was interrupted without leaving `node_modules` or `package-lock.json`.
- JOSS submission has not been submitted to JOSS. The local submission package
  zip was generated only. Browser check showed the JOSS submission entry
  requires ORCID login before a submission can be started.
- OpenInference and Promptfoo upstream PRs have not been opened. Drafts exist
  in `PR_OPENINFERENCE.md` and `PR_PROMPTFOO.md`.

## Next Manual Gates

1. Monitor Zenodo DOI materialization with `make scientific-activation-observe`.
   Do not mutate the GitHub Release again without new evidence that Zenodo will
   not harvest the existing queued event.
2. Run Promptfoo eval/share in an environment where the Promptfoo CLI starts
   successfully.
3. Log in with ORCID before starting the JOSS submission workflow.
4. Open upstream issues or pull requests using the prepared PR draft files.
