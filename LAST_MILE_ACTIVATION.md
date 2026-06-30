# ATU v0.2.0 Last-Mile Activation Checklist

Status date: 2026-06-30

## Current State

ATU v0.2.0 is engineering-complete and GitHub-visible, but the scientific
identity/citation loop is still pending external activation.

```text
Engineering system: complete
GitHub software release: complete
Hugging Face dataset identity: pending
Zenodo GitHub integration: enabled
Zenodo DOI identity: pending
Promptfoo runtime artifact: pending
JOSS submission: pending
```

This file is the no-ambiguity execution checklist for the remaining gates. Do
not mark any gate complete unless the verification command or external portal
evidence succeeds.

## Gate 1: Hugging Face Dataset Identity

Local evidence already available:

- HF-ready dataset folder: `hf_dataset/atu_trace_1000`
- Local loader check: train/eval/test each load with 1 row
- Current blocker: not logged in to Hugging Face

Use the modern HF CLI available in this environment:

```bash
cd /Users/zhangbin/Documents/atu
.venv/bin/hf auth login
.venv/bin/hf auth whoami
```

If `whoami` succeeds, publish:

```bash
.venv/bin/hf upload joy7758/atu-trace-1000 \
  hf_dataset/atu_trace_1000 \
  . \
  --repo-type dataset \
  --commit-message "ATU v0.2 dataset initial release"
```

Completion evidence:

```bash
.venv/bin/hf datasets ls --author joy7758
```

Record the live dataset URL in `README.md`, `SCIENTIFIC_CLOSURE_STATUS.md`, and
`ACTIVATION_MANIFEST.json`.

## Gate 2: Zenodo DOI Identity

Current blocker: repository is enabled in Zenodo, but no matching ATU DOI record
or ingested `v0.2.0` release is visible yet. GitHub webhook deliveries currently
show the Zenodo `ping` event only, with no `release` event delivery.

Manual activation path:

```text
1. Keep Zenodo repository binding enabled for joy7758/atu-compiler
2. Trigger a new GitHub release event if Zenodo does not ingest the existing one
3. Verify the DOI on Zenodo
```

If a re-trigger is required, prefer editing/publishing release metadata in the
GitHub UI or creating a follow-up release after deciding whether `v0.2.0` should
remain immutable. Do not move the existing `v0.2.0` tag casually.

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
marker. It does not move the tag or alter release assets. If Zenodo ignores an
`edited` release event, the next candidate is a confirmed release-object
recreation for the existing tag.

Execution guard status: running `--execute` without
`ATU_CONFIRM_ZENODO_RETRIGGER=release-v0.2.0-zenodo-retrigger` exits with code
`78` before the GitHub Release edit.

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
