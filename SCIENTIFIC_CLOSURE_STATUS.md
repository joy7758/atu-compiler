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

Latest recheck: `2026-06-30T14:29:06Z`.
Zenodo re-trigger preparation check: `2026-06-30T14:34:37Z`.
Zenodo re-trigger execution check: `2026-06-30T14:45:55Z`.
Scientific activation observer start: `2026-06-30T14:51:49Z`.
Latest observer run: `2026-06-30T15:27:27Z`.
Latest browser/manual-use check: `2026-06-30T15:23:16Z`.

## HF Dataset Gate

Blocked by authentication.

Observed:

```text
HF_TOKEN_MISSING
HUGGINGFACE_HUB_TOKEN_MISSING
hf auth whoami -> Error: Not logged in
hf repos ls -> HTTP 401
hf datasets info joy7758/atu-trace-1000 -> Dataset not found
hf datasets list --author joy7758 --search atu-trace -> []
Chrome Hugging Face session -> logged in as joy7759
Chrome Hugging Face organizations -> no visible joy7758 organization membership
```

Dataset package is locally valid but not uploaded. The documented target is
`joy7758/atu-trace-1000`, but the browser session is `joy7759`; choose the
namespace before upload. If using the documented target, use:

```bash
hf auth login
hf upload joy7758/atu-trace-1000 hf_dataset/atu_trace_1000 . --repo-type dataset --commit-message "ATU v0.2 dataset initial release"
```

## Zenodo DOI Gate

Pending Zenodo DOI materialization after repository-to-Zenodo binding and
successful release webhook delivery.

Exact Zenodo API searches for the release title, GitHub URL, and
`joy7758/atu-compiler` returned no matching ATU records after GitHub release
creation. After enabling the Zenodo GitHub integration, the repository detail
page still did not list the existing `v0.2.0` release, so DOI minting remains
unverified. A later recheck found the GitHub Zenodo webhook active, but its
delivery history contained only the initial `ping` event and no `release`
delivery. After executing the guarded metadata edit, GitHub recorded a
`release` / `edited` webhook delivery with status `OK`, but Zenodo API searches
for the repository and release title still returned `total: 0`. This is now
tracked as an asynchronous ingestion window rather than a reason for immediate
GitHub release mutation.

Manual action:

```text
Monitor Zenodo materialization without further GitHub Release mutation
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
make scientific-activation-observe -> Zenodo total 0, HF dataset not found, Promptfoo runtime absent
observer network behavior -> endpoint failures return JSON `ok: false` sections
Zenodo browser sync -> completed, still no v0.2.0 and no DOI on repository page
```

## Promptfoo Benchmark Gate

Blocked by npm/package bootstrap in this local environment.

Observed:

```text
npx promptfoo eval -> hung during package bootstrap and was interrupted
npx --yes promptfoo@0.121.17 --help -> hung and was interrupted
npm install --no-audit --no-fund -> hung and was interrupted
npm pack promptfoo@0.121.17 --dry-run --json -> hung and was interrupted
npm install --no-audit --no-fund -> still no output after 90 seconds and was interrupted
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
