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
Hugging Face dataset: live
Promptfoo benchmark execution: complete locally
JOSS submission: package generated, not submitted
```

## Completed Evidence

- GitHub repository: `https://github.com/joy7758/atu-compiler`
- GitHub release: `https://github.com/joy7758/atu-compiler/releases/tag/v0.2.0`
- Release tag: `v0.2.0`
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
Latest observer run: `2026-06-30T17:58:25Z`.
Latest browser/manual-use check: `2026-06-30T17:47:29Z`.

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

Pending Zenodo DOI materialization after repository-to-Zenodo binding. The
latest evidence indicates that a fresh GitHub `release` / `published` event is
needed before Zenodo will ingest the release.

Exact Zenodo API searches for the release title, GitHub URL, and
`joy7758/atu-compiler` returned no matching ATU records after GitHub release
creation. After enabling the Zenodo GitHub integration, the repository detail
page still did not list the existing `v0.2.0` release, so DOI minting remains
unverified. A later recheck found the GitHub Zenodo webhook active, but its
delivery history contained only the initial `ping` event and no `release`
delivery. After executing the guarded metadata edit, GitHub recorded a
`release` / `edited` webhook delivery with status `OK`, but Zenodo API searches
for the repository and release title still returned `total: 0`. This is now
tracked as a missing `release` / `published` event rather than ordinary queue
delay: `v0.2.0` was published before the Zenodo hook was created.

Manual action:

```text
Choose a new release-published event path from docs/zenodo-release-ingestion-decision.md
Verify DOI on Zenodo
```

Observer command:

```bash
make scientific-activation-observe
```

Manual GitHub workflow: `Scientific Activation Observer` is active and
`workflow_dispatch` only. It skips repository webhook-delivery inspection
because that API requires permissions not available to the default
`GITHUB_TOKEN`.
Latest GitHub workflow run: `28454815985`, conclusion `success`, artifact
`scientific-activation-observer` / `7984877361`.

Prepared guarded command:

```bash
ATU_CONFIRM_ZENODO_RETRIGGER=release-v0.2.0-zenodo-retrigger \
  scripts/activation/zenodo_retrigger_v0_2_0.sh --execute
```

Dry-run evidence:

```text
make zenodo-retrigger-dry-run -> pass
--execute without confirmation guard -> blocked with exit code 78
guarded --execute -> GitHub release edited event delivered to Zenodo with OK
Zenodo API after edited event -> total: 0
scientific activation observer -> prepared for read-only polling
make scientific-activation-observe -> Zenodo total 0, HF dataset visible, Promptfoo runtime artifact passed
observer diagnosis -> release predates Zenodo hook, no release/published delivery, new release-published event required
observer network behavior -> endpoint failures return JSON `ok: false` sections
Zenodo browser sync -> completed twice; latest success alert at 2026-06-30T17:47:29Z check window,
still no v0.2.0 and no DOI on repository page after reload
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
- `src/`
- `datasets/`
- `evals/`

The zip was checked for `__pycache__`, `.pyc`, `node_modules`, and `.git`
entries; none were present.

Browser check:

```text
JOSS submission entry -> requires ORCID login before submission starts
```

## Closure Definition

The scientific citation loop should only be marked complete after all are true:

1. Zenodo DOI is minted and recorded in `CITATION.cff`.
2. Hugging Face dataset is live and URL is recorded in `README.md`.
3. Promptfoo eval result is generated and attached or linked.
4. JOSS submission is opened or explicitly deferred.
