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
  GitHub release. GitHub webhook deliveries currently show only the Zenodo
  `ping` event, not a `release` event delivery.
- Hugging Face dataset upload has not been completed. `hf auth whoami` returned
  `Not logged in`; public lookup for `joy7758/atu-trace-1000` returned
  `Dataset not found`.
- Promptfoo share has not been completed. `npx promptfoo` startup hung during
  package bootstrap in this environment and was interrupted.
- Promptfoo local package metadata exists in `evals/promptfoo/package.json`, but
  `npm install --no-audit --no-fund` again produced no output for 90 seconds and
  was interrupted without leaving `node_modules` or `package-lock.json`.
- JOSS submission has not been submitted to JOSS. The local submission package
  zip was generated only.
- OpenInference and Promptfoo upstream PRs have not been opened. Drafts exist
  in `PR_OPENINFERENCE.md` and `PR_PROMPTFOO.md`.

## Next Manual Gates

1. Re-trigger Zenodo ingestion for `v0.2.0` or create a follow-up release after
   deciding whether the existing `v0.2.0` release should remain immutable.
2. Authenticate with Hugging Face and upload `hf_dataset/atu_trace_1000` to
   `joy7758/atu-trace-1000`.
3. Run Promptfoo eval/share in an environment where the Promptfoo CLI starts
   successfully.
4. Submit `atu_v0.2_joss_submission_final.zip` through the JOSS workflow.
5. Open upstream issues or pull requests using the prepared PR draft files.
