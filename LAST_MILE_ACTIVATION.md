# ATU v0.2.0 Last-Mile Activation Checklist

Status date: 2026-07-01

## Current State

ATU v0.2.0 is engineering-complete and GitHub-visible. The software citation
loop is now active through the `v0.2.1` Zenodo activation release.

```text
Engineering system: complete
GitHub software release: complete
Hugging Face dataset identity: live
Zenodo GitHub integration: enabled
Zenodo DOI identity: verified
Promptfoo runtime artifact: complete locally
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
- HF `dataset_infos.json` update commit: `fd0da1d`
- HF `dataset_infos.json` homepage:
  `https://huggingface.co/datasets/joy7759/atu-trace-1000`
- Uploaded files: `README.md`, `dataset_infos.json`, `data/eval.jsonl`,
  `data/test.jsonl`, `data/train.jsonl`

## Gate 2: Zenodo DOI Identity

Current state: repository is enabled in Zenodo, the guarded `v0.2.1` activation
release has been published, and Zenodo returned a DOI-bearing software record.

Manual activation path:

```text
1. Keep Zenodo repository binding enabled for joy7758/atu-compiler
2. Preserve `v0.2.1` as the citable Zenodo activation release
3. Record the DOI in citation/status files
```

The GitHub-side re-trigger has already been executed once. Further GitHub
Release mutation requires explicit confirmation. Do not move the existing
`v0.2.0` tag.

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

Do not rebuild either GitHub Release, move either tag, or change release assets
to chase the DOI. The DOI is already verified through the `v0.2.1` Zenodo
activation release.

Latest observer run: `2026-07-01T00:15:05Z`; Zenodo DOI status was `verified`,
Hugging Face dataset status was `visible`, and Promptfoo runtime artifact
passed.
Manual GitHub workflow: `Scientific Activation Observer` is active and
`workflow_dispatch` only. It skips repository webhook-delivery inspection in CI;
local authenticated observer runs include that check. CI-side hook diagnosis is
indeterminate by design when repository-hook permissions are unavailable.
Latest GitHub workflow run: `28466699508`, conclusion `success`, head SHA
`bcf03b9610ada5975966f3c450f4fb3b5c9612eb`, artifact
`scientific-activation-observer` / `7989891992`. CI-side result: Zenodo query
total `0`, Hugging Face dataset `visible` via public API, Promptfoo passed, and
hook-delivery diagnosis `indeterminate_without_repo_hook_delivery_permission`.
Manual browser check at `2026-06-30T15:23:16Z`: Zenodo repo-list sync completed,
but the repository detail page still showed no `v0.2.0` and no DOI.
Manual browser check at `2026-06-30T17:47:29Z`: Zenodo repo-list `Sync now`
returned a success alert, but after reload the `joy7758/atu-compiler`
repository detail page still showed no `v0.2.0` release and no DOI.

Decision document:

```text
docs/zenodo-release-ingestion-decision.md
```

Read-only command plan:

```bash
make zenodo-release-published-event-plan
```

Executed activation conclusion:

```text
v0.2.1_local_tag: created
v0.2.1_remote_tag: pushed
v0.2.1_github_release: published
zenodo_doi: verified
doi: 10.5281/zenodo.21087765
concept_doi: 10.5281/zenodo.21087764
record: https://zenodo.org/records/21087765
```

Guarded safe-path dry run:

```bash
make zenodo-v0.2.1-release-dry-run
```

Guarded safe-path execution command, only after explicit confirmation:

```bash
ATU_CONFIRM_ZENODO_V0_2_1_RELEASE=v0.2.1-zenodo-release \
  scripts/activation/create_v0_2_1_zenodo_release.sh --execute
```

Prepared safe-path files:

```text
RELEASE_NOTES_v0.2.1.md
scripts/activation/create_v0_2_1_zenodo_release.sh
```

Verified boundary:

```text
software_release_metadata: 0.2.1
atu_ir_profile_metadata: 0.2.0
v0.2.1_local_tag: created
v0.2.1_remote_tag: pushed
v0.2.1_github_release: published
zenodo_doi: verified
```

Completion evidence:

```bash
curl -fsSL 'https://zenodo.org/api/records/21087765'
```

DOI has been recorded in `CITATION.cff`, `README.md`,
`SCIENTIFIC_CLOSURE_STATUS.md`, and `ACTIVATION_MANIFEST.json`.

## Gate 3: Promptfoo Runtime Artifact

Current evidence:

- `evals/promptfoo/package.json` pins `promptfoo@0.121.17`
- Promptfoo config and generated tests exist
- Result artifact:
  `evals/promptfoo/results/promptfoo-atu-v0.2.0-20260630T170204Z.json`
- Eval ID: `eval-dYL-2026-06-30T17:02:05`
- Result: `3 passed`, `0 failed`, `0 errors`

Observed local setup path:

```bash
cd /Users/zhangbin/Documents/atu/evals/promptfoo
npm install --no-audit --no-fund --omit=optional --legacy-peer-deps --prefer-offline
tmp_dir=$(mktemp -d)
curl -fL -o "$tmp_dir/darwin-arm64-0.5.29.tgz" \
  https://registry.npmjs.org/@libsql/darwin-arm64/-/darwin-arm64-0.5.29.tgz
mkdir -p node_modules/@libsql/darwin-arm64
tar -xzf "$tmp_dir/darwin-arm64-0.5.29.tgz" \
  -C node_modules/@libsql/darwin-arm64 --strip-components=1
rm -rf "$tmp_dir"
npm run eval -- --no-share
```

Portable re-run path after dependencies are present:

```bash
npm run eval -- --no-share
```

Completion evidence:

- Promptfoo eval exits successfully.
- Generated result artifact is saved or exported.
- Result artifact is linked from `SCIENTIFIC_CLOSURE_STATUS.md`.

## Gate 4: JOSS Submission

Current evidence:

- Final submission zip exists:
  `atu_v0.2_joss_submission_final.zip`
- Zip contains `paper/`, `CITATION.cff`, `README.md`, `LICENSE`,
  `pyproject.toml`, `llms.txt`, release notes, status files, `src/`,
  `datasets/`, `docs/`, `scripts/`, `schemas/`, `mapping/`, `rfcs/`,
  `examples/`, `tests/`, `replay/`, and `evals/`
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

- GitHub release existence alone does not imply Zenodo DOI existence; this
  repository claims a DOI only because the direct Zenodo record API returned
  `10.5281/zenodo.21087765`.
- Local dataset files exist does not imply Hugging Face dataset exists.
- Promptfoo config exists does not imply benchmark runtime evidence exists.
- JOSS zip exists does not imply JOSS submission exists.

## Closure Criteria

The software citation activation layer is complete for `v0.2.1` because all are
true:

1. Hugging Face dataset URL is live.
2. Zenodo DOI is live.
3. Promptfoo eval runtime artifact exists.

The broader ecosystem loop remains open until Promptfoo share, JOSS submission,
and upstream PRs are performed or explicitly deferred.
