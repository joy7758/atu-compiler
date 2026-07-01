# ATU v0.2.0 Scientific Closure Status

Status date: 2026-07-01

## Current Position

ATU v0.2.0 is externally visible as software, and the software citation loop is
active through the `v0.2.1` Zenodo activation release. The broader ecosystem
loop is not fully closed because Promptfoo share, JOSS submission, and upstream
PRs are still separate external actions.

```text
Code exists: yes
GitHub release exists: yes
Zenodo GitHub integration: enabled
Zenodo DOI: verified
Hugging Face dataset: live
Promptfoo benchmark execution: complete locally
JOSS submission: package generated, not submitted
```

## Completed Evidence

- GitHub repository: `https://github.com/joy7758/atu-compiler`
- GitHub release: `https://github.com/joy7758/atu-compiler/releases/tag/v0.2.0`
- Release tag: `v0.2.0`
- Zenodo activation release:
  `https://github.com/joy7758/atu-compiler/releases/tag/v0.2.1`
- Zenodo DOI: `https://doi.org/10.5281/zenodo.21087765`
- Zenodo concept DOI: `https://doi.org/10.5281/zenodo.21087764`
- Zenodo record: `https://zenodo.org/records/21087765`
- Zenodo archive file: `joy7758/atu-compiler-v0.2.1.zip`
- Release build commit: `dcf930a`
- Publication status commit: use git history for the current status snapshot; do
  not self-record a commit hash inside this file.
- Zenodo GitHub integration: enabled for `joy7758/atu-compiler`
- Zenodo release webhook: active for GitHub `release` events
- Dataset local loader check: `datasets.load_dataset("json", ...)` loads
  train/eval/test as 1 row each.
- Hugging Face dataset:
  `https://huggingface.co/datasets/joy7759/atu-trace-1000`
- HF data commit: `945c6e2`
- HF root metadata commit: `54bd194`
- HF README update commit: `be34a82`
- HF `dataset_infos.json` update commit: `fd0da1d`
- Final JOSS zip: `atu_v0.2_joss_submission_final.zip`
- HF upload-ready folder: `hf_dataset/atu_trace_1000`
- Promptfoo local package folder: `evals/promptfoo`
- Promptfoo result artifact:
  `evals/promptfoo/results/promptfoo-atu-v0.2.0-20260630T170204Z.json`
- Promptfoo eval ID: `eval-dYL-2026-06-30T17:02:05`
- Promptfoo result: `3 passed`, `0 failed`, `0 errors`

Latest recheck: `2026-06-30T14:29:06Z`.
Zenodo re-trigger preparation check: `2026-06-30T14:34:37Z`.
Zenodo re-trigger execution check: `2026-06-30T14:45:55Z`.
Scientific activation observer start: `2026-06-30T14:51:49Z`.
Latest observer run: `2026-07-01T00:15:05Z`.
Latest browser/manual-use check: `2026-06-30T17:47:29Z`.
Guarded `v0.2.1` safe-path execution: tag pushed, GitHub Release published, and
Zenodo DOI verified. Software release metadata is set to `0.2.1`;
ATU-IR/profile metadata remains `0.2.0`.

## HF Dataset Gate

Completed.

Observed:

```text
User confirmation -> joy7759 and joy7758 are the same owner identity for ATU
HF dataset URL -> https://huggingface.co/datasets/joy7759/atu-trace-1000
HF data commit -> 945c6e2
HF root metadata commit -> 54bd194
HF dataset_infos update commit -> fd0da1d
HF dataset_infos homepage -> https://huggingface.co/datasets/joy7759/atu-trace-1000
HF file tree -> README.md, dataset_infos.json, data/eval.jsonl, data/test.jsonl, data/train.jsonl
```

The local package remains mirrored at `hf_dataset/atu_trace_1000`.

## Zenodo DOI Gate

Completed for the citable software release `v0.2.1`.

Observed:

```text
v0.2.1 tag -> pushed
v0.2.1 GitHub Release -> published at 2026-06-30T23:59:42Z
Zenodo record -> https://zenodo.org/records/21087765
Zenodo DOI -> https://doi.org/10.5281/zenodo.21087765
Zenodo concept DOI -> https://doi.org/10.5281/zenodo.21087764
Zenodo status -> published
Zenodo state -> done
Zenodo archive -> joy7758/atu-compiler-v0.2.1.zip
```

The original `v0.2.0` GitHub Release still predates the Zenodo hook and does not
have its own Zenodo DOI. The citation anchor for the software artifact is now
the `v0.2.1` Zenodo activation release.

Observer command:

```bash
make scientific-activation-observe
```

Manual GitHub workflow: `Scientific Activation Observer` is active and
`workflow_dispatch` only. It skips repository webhook-delivery inspection
because that API requires permissions not available to the default
`GITHUB_TOKEN`. CI-side hook diagnosis is therefore indeterminate; local
authenticated observer runs remain authoritative for Zenodo webhook-delivery
diagnosis.
Latest GitHub workflow run before DOI recording: `28466699508`, conclusion
`success`, head SHA `bcf03b9610ada5975966f3c450f4fb3b5c9612eb`, artifact
`scientific-activation-observer` / `7989891992`.

Execution evidence:

```text
make zenodo-retrigger-dry-run -> pass
--execute without confirmation guard -> blocked with exit code 78
guarded --execute -> GitHub release edited event delivered to Zenodo with OK
Zenodo API after edited event -> total: 0
v0.2.1 guarded --execute -> GitHub Release v0.2.1 created
v0.2.1 hook deliveries -> created 202 OK, published 409, released 403
make scientific-activation-observe -> Zenodo DOI verified, HF dataset visible, Promptfoo runtime artifact passed
observer network behavior -> endpoint failures return JSON `ok: false` sections
```

## Promptfoo Benchmark Gate

Completed locally.

Observed:

```text
npm install --no-audit --no-fund -> full dependency bootstrap was too large and was interrupted
npm install --legacy-peer-deps --omit=optional -> completed
direct @libsql/darwin-arm64@0.5.29 platform binding -> installed for macOS arm64
promptfoo --version -> 0.121.17
promptfoo eval --no-share --output results/...json -> 3 passed, 0 failed, 0 errors
```

Runtime package:

- `evals/promptfoo/package.json`
- `evals/promptfoo/promptfooconfig.yaml`
- generated tests under `evals/promptfoo/tests/`
- deterministic provider under `evals/promptfoo/providers/atu-noop.js`
- result artifact under `evals/promptfoo/results/`

Re-run path:

```bash
cd evals/promptfoo
npm run eval -- --no-share
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
- `LICENSE`
- `pyproject.toml`
- `llms.txt`
- release notes and status files
- `src/`
- `datasets/`
- `docs/`
- `scripts/`
- `schemas/`
- `mapping/`
- `rfcs/`
- `examples/`
- `tests/`
- `replay/`
- `evals/`

The zip was checked for `__pycache__`, `.pyc`, `node_modules`, and `.git`
entries; none were present.

Browser check:

```text
JOSS submission entry -> requires ORCID login before submission starts
```

## Closure Definition

The software citation loop is complete for `v0.2.1`:

1. Zenodo DOI is minted and recorded in `CITATION.cff`.
2. Hugging Face dataset is live and URL is recorded in `README.md`.
3. Promptfoo eval result is generated and linked from this status file.

The broader ecosystem loop remains open until Promptfoo share, JOSS submission,
and upstream PRs are performed or explicitly deferred.
