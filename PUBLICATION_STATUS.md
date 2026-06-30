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
- Latest observer run: `2026-06-30T15:27:27Z`; Zenodo query total remained
  `0`, Hugging Face dataset remained not found, and Promptfoo runtime remained
  absent.
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
- Hugging Face dataset upload has not been completed. `hf auth whoami` returned
  `Not logged in`; public lookup for `joy7758/atu-trace-1000` returned
  `Dataset not found`. Chrome is logged in to Hugging Face as `joy7759`, with
  no visible `joy7758` organization membership, so uploading to the documented
  `joy7758/atu-trace-1000` target requires a namespace decision.
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
2. Confirm whether the Hugging Face dataset should be published under
   `joy7758/atu-trace-1000` with separate credentials or under the currently
   logged-in `joy7759` namespace.
3. Run Promptfoo eval/share in an environment where the Promptfoo CLI starts
   successfully.
4. Log in with ORCID before starting the JOSS submission workflow.
5. Open upstream issues or pull requests using the prepared PR draft files.
