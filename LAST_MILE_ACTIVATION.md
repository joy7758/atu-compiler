# ATU v0.2.0 Last-Mile Activation Checklist

Status date: 2026-06-30

## Current State

ATU v0.2.0 is engineering-complete and GitHub-visible, but the scientific
identity/citation loop is still pending external activation.

```text
Engineering system: complete
GitHub software release: complete
Hugging Face dataset identity: live
Zenodo GitHub integration: enabled
Zenodo DOI identity: pending
Promptfoo runtime artifact: pending
JOSS submission: pending
```

This file is the no-ambiguity execution checklist for the remaining gates. Do
not mark any gate complete unless the verification command or external portal
evidence succeeds.

## Gate 1: Hugging Face Dataset Identity

Completion evidence:

- HF-ready dataset folder: `hf_dataset/atu_trace_1000`
- Local loader check: train/eval/test each load with 1 row
- User confirmed `joy7759` and `joy7758` are the same owner identity for ATU.
- Live dataset URL: `https://huggingface.co/datasets/joy7759/atu-trace-1000`
- HF data commit: `945c6e2`
- HF root metadata commit: `54bd194`
- Uploaded files: `README.md`, `dataset_infos.json`, `data/eval.jsonl`,
  `data/test.jsonl`, `data/train.jsonl`

## Gate 2: Zenodo DOI Identity

Current state: repository is enabled in Zenodo and a guarded GitHub Release
metadata edit delivered a `release` / `edited` webhook event to Zenodo with
status `OK`. Zenodo API searches still returned `total: 0`, so DOI is pending
materialization.

Manual activation path:

```text
1. Keep Zenodo repository binding enabled for joy7758/atu-compiler
2. Monitor the Zenodo ingestion window without further GitHub Release mutation
3. Verify the DOI on Zenodo
```

The GitHub-side re-trigger has already been executed once. Further GitHub
Release mutation is on hold while Zenodo DOI materialization is plausibly
pending. Do not move the existing `v0.2.0` tag.

Prepared dry run:

```bash
make zenodo-retrigger-dry-run
```

Dry run status: passed at `2026-06-30T14:34:37Z`; no external release edit was
performed.

Prepared external action after explicit confirmation:

```bash
ATU_CONFIRM_ZENODO_RETRIGGER=release-v0.2.0-zenodo-retrigger \
  scripts/activation/zenodo_retrigger_v0_2_0.sh --execute
```

This lower-impact path edits only GitHub Release notes with an HTML comment
marker. It does not move the tag or alter release assets. It has already been
executed once and produced a successful `release` / `edited` webhook delivery.

Execution guard status: running `--execute` without
`ATU_CONFIRM_ZENODO_RETRIGGER=release-v0.2.0-zenodo-retrigger` exits with code
`78` before the GitHub Release edit.

Executed re-trigger:

```text
executed_at: 2026-06-30T14:43:22Z
github_delivery: release / edited / OK at 2026-06-30T14:43:30.23Z
zenodo_api_after_retrigger: total 0 at 2026-06-30T14:45:55Z
```

Observer path:

```bash
make scientific-activation-observe
```

Do not rebuild the GitHub Release, create a follow-up release, move the tag, or
change release assets while Zenodo DOI materialization is still plausibly
pending.

Latest observer run: `2026-06-30T16:01:46Z`; Zenodo query total remained `0`
and Hugging Face dataset status was `visible`.
Manual GitHub workflow: `Scientific Activation Observer` is active and
`workflow_dispatch` only. It skips repository webhook-delivery inspection in CI;
local authenticated observer runs include that check.
Latest GitHub workflow run: `28454815985`, conclusion `success`, artifact
`scientific-activation-observer` / `7984877361`.
Manual browser check at `2026-06-30T15:23:16Z`: Zenodo repo-list sync completed,
but the repository detail page still showed no `v0.2.0` and no DOI.

Completion evidence:

```bash
curl -fsSL 'https://zenodo.org/api/records?q=%22joy7758%2Fatu-compiler%22&sort=mostrecent&size=10'
```

Record the DOI in `CITATION.cff`, `README.md`, `SCIENTIFIC_CLOSURE_STATUS.md`,
and `ACTIVATION_MANIFEST.json`.

## Gate 3: Promptfoo Runtime Artifact

Current evidence:

- `evals/promptfoo/package.json` pins `promptfoo@0.121.17`
- Promptfoo config and generated tests exist
- Current blocker: npm tarball/package bootstrap hangs in this environment

Retry path:

```bash
cd /Users/zhangbin/Documents/atu/evals/promptfoo
rm -rf node_modules package-lock.json
npm cache clean --force
npm install --no-audit --no-fund
npm run eval
```

Fallback:

```bash
npm install --legacy-peer-deps
npm run eval
```

Completion evidence:

- Promptfoo eval exits successfully.
- Generated result artifact is saved or exported.
- Result artifact is linked from `SCIENTIFIC_CLOSURE_STATUS.md`.

## Gate 4: JOSS Submission

Current evidence:

- Final submission zip exists:
  `atu_v0.2_joss_submission_final.zip`
- Zip contains `paper/`, `CITATION.cff`, `README.md`, `src/`, `datasets/`,
  and `evals/`
- Zip was checked for `__pycache__`, `.pyc`, `node_modules`, and `.git`

Manual submission path:

```text
Open https://joss.readthedocs.io/en/latest/submitting.html
Submit the repository/release package according to JOSS instructions
Use atu_v0.2_joss_submission_final.zip as the local package reference
```

Browser-use check: JOSS submission entry requires ORCID login before a
submission can be started.

Completion evidence:

- JOSS issue/submission URL exists.
- URL is recorded in `SCIENTIFIC_CLOSURE_STATUS.md` and
  `ACTIVATION_MANIFEST.json`.

## Do Not Confuse These States

- GitHub release exists does not imply Zenodo DOI exists.
- Local dataset files exist does not imply Hugging Face dataset exists.
- Promptfoo config exists does not imply benchmark runtime evidence exists.
- JOSS zip exists does not imply JOSS submission exists.

## Closure Criteria

The scientific activation layer is complete only when all are true:

1. Hugging Face dataset URL is live.
2. Zenodo DOI is live.
3. Promptfoo eval runtime artifact exists.
4. JOSS submission is opened or explicitly deferred with rationale.
