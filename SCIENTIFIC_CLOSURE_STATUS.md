# ATU v0.2.0 Scientific Closure Status

Status date: 2026-06-30

## Current Position

ATU v0.2.0 is externally visible as software, but the broader scientific
citation loop is not fully closed.

```text
Code exists: yes
GitHub release exists: yes
Zenodo GitHub integration: enabled
Zenodo DOI: not verified
Hugging Face dataset: not uploaded
Promptfoo benchmark execution: not completed in this environment
JOSS submission: package generated, not submitted
```

## Completed Evidence

- GitHub repository: `https://github.com/joy7758/atu-compiler`
- GitHub release: `https://github.com/joy7758/atu-compiler/releases/tag/v0.2.0`
- Release tag: `v0.2.0`
- Release build commit: `dcf930a`
- Publication status commit: `e095b80`
- Zenodo GitHub integration: enabled for `joy7758/atu-compiler`
- Zenodo release webhook: active for GitHub `release` events
- Dataset local loader check: `datasets.load_dataset("json", ...)` loads
  train/eval/test as 1 row each.
- Final JOSS zip: `atu_v0.2_joss_submission_final.zip`
- HF upload-ready folder: `hf_dataset/atu_trace_1000`
- Promptfoo local package folder: `evals/promptfoo`

## HF Dataset Gate

Blocked by authentication.

Observed:

```text
HF_TOKEN_MISSING
HUGGINGFACE_HUB_TOKEN_MISSING
hf auth whoami -> Error: Not logged in
hf repos ls -> HTTP 401
```

Dataset package is locally valid but not uploaded. Use:

```bash
hf auth login
hf upload joy7758/atu-trace-1000 hf_dataset/atu_trace_1000 . --repo-type dataset --commit-message "ATU v0.2 dataset initial release"
```

## Zenodo DOI Gate

Blocked by release ingestion after repository-to-Zenodo binding.

Exact Zenodo API searches for the release title, GitHub URL, and
`joy7758/atu-compiler` returned no matching ATU records after GitHub release
creation. After enabling the Zenodo GitHub integration, the repository detail
page still did not list the existing `v0.2.0` release, so DOI minting remains
unverified.

Manual action:

```text
Trigger a new GitHub release event for v0.2.0, or create a follow-up release
after deciding whether v0.2.0 should remain immutable
Verify DOI on Zenodo
```

## Promptfoo Benchmark Gate

Blocked by npm/package bootstrap in this local environment.

Observed:

```text
npx promptfoo eval -> hung during package bootstrap and was interrupted
npx --yes promptfoo@0.121.17 --help -> hung and was interrupted
npm install --no-audit --no-fund -> hung and was interrupted
npm pack promptfoo@0.121.17 --dry-run --json -> hung and was interrupted
```

Prepared:

- `evals/promptfoo/package.json`
- `evals/promptfoo/promptfooconfig.yaml`
- generated tests under `evals/promptfoo/tests/`
- deterministic provider under `evals/promptfoo/providers/atu-noop.js`

Retry path in a stable npm environment:

```bash
cd evals/promptfoo
npm install
npm run eval
```

## JOSS Gate

Package generated, not submitted.

Generated:

```text
atu_v0.2_joss_submission_final.zip
```

The final zip includes:

- `paper/`
- `CITATION.cff`
- `README.md`
- `src/`
- `datasets/`
- `evals/`

The zip was checked for `__pycache__`, `.pyc`, `node_modules`, and `.git`
entries; none were present.

## Closure Definition

The scientific citation loop should only be marked complete after all are true:

1. Zenodo DOI is minted and recorded in `CITATION.cff`.
2. Hugging Face dataset is live and URL is recorded in `README.md`.
3. Promptfoo eval result is generated and attached or linked.
4. JOSS submission is opened or explicitly deferred.
