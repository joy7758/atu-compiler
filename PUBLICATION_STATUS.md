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

## Verified Local/Package Actions

- `make publication-bundles` passed.
- ATU JSONL schema validation passed for 3 episodes.
- Hugging Face JSON loader validation passed:
  - train: 1 row
  - eval: 1 row
  - test: 1 row
- JOSS zip exists: `atu_v0.2_joss_submission.zip`
- JOSS zip has no `__pycache__` or `.pyc` entries.
- Citation bundle exists: `citation_bundle/`
- HF upload mirror exists: `hf_dataset/atu_trace_1000/`
- Promptfoo local package exists: `evals/promptfoo/`

## Not Completed Externally

- Zenodo DOI has not been verified. Exact Zenodo API searches for the release
  title and GitHub URL returned no matching records immediately after GitHub
  release creation.
- Hugging Face dataset upload has not been completed. `hf auth whoami` returned
  `Not logged in`, and `hf repos ls` returned HTTP 401.
- Promptfoo share has not been completed. `npx promptfoo` startup hung during
  package bootstrap in this environment and was interrupted.
- JOSS submission has not been submitted to JOSS. The local submission package
  zip was generated only.
- OpenInference and Promptfoo upstream PRs have not been opened. Drafts exist
  in `PR_OPENINFERENCE.md` and `PR_PROMPTFOO.md`.

## Next Manual Gates

1. Connect `joy7758/atu-compiler` to Zenodo and verify DOI creation.
2. Authenticate with Hugging Face and upload `hf_dataset/atu_trace_1000` to
   `joy7758/atu-trace-1000`.
3. Run Promptfoo eval/share in an environment where the Promptfoo CLI starts
   successfully.
4. Submit `atu_v0.2_joss_submission.zip` through the JOSS workflow.
5. Open upstream issues or pull requests using the prepared PR draft files.
