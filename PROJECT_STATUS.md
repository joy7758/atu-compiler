# ATU Project Status

Status date: 2026-06-30

## Local Completion State

The repository is a v0.2.0 release-prep implementation of the ATU
Trace-to-Dataset Compiler Profile on local branch `release/v0.2.0`.

Completed locally:

- agent-readable repository surface: `README.md`, `llms.txt`, `AGENTS.md`, RFC,
  mapping docs, schemas, citation scaffold, and JOSS paper scaffold;
- canonical ATU-IR schema in `schemas/atu-ir.schema.json`;
- receipt and replay manifest schemas;
- Python package `atu-compiler` with CLI entry point `atu`;
- source adapters for OpenTelemetry OTLP JSON, OpenInference OTLP-compatible
  spans, and LangSmith-style run exports;
- deterministic compiler from source traces to ATU episode JSONL;
- receipt normalization, replay class derivation, labels, redaction, and replay
  manifest generation;
- Hugging Face-style local dataset package under `datasets/atu-trace-1000`;
- Promptfoo local eval package under `evals/promptfoo`;
- LangSmith-shaped diagnostic projection command;
- synthetic fixtures and pytest regression tests.

## Verification Snapshot

Commands run successfully in local `.venv`:

```bash
.venv/bin/python -m pytest
.venv/bin/atu compile --source otlp --input examples/autogen/trace.otlp.json --output out/autogen.jsonl
.venv/bin/atu compile --source openinference --input examples/crewai/openinference_trace.json --output out/crewai.jsonl
.venv/bin/atu compile --source langsmith --input examples/langsmith/run_export.json --output out/langsmith.jsonl
.venv/bin/atu validate --input out/atu.jsonl --schema schemas/atu-ir.schema.json
.venv/bin/atu export-hf --input out/atu.jsonl --output datasets/atu-trace-1000
.venv/bin/atu export-promptfoo --input out/atu.jsonl --output evals/promptfoo
.venv/bin/atu replay-manifest --input out/atu.jsonl --output replay/manifests
.venv/bin/atu project-langsmith --input out/atu.jsonl --output out/langsmith_projection.json
.venv/bin/atu stats --input out/atu.jsonl
```

Observed local corpus stats:

```json
{
  "episodes": 3,
  "steps": 9,
  "receipts": 2,
  "source_schemas": {
    "langsmith": 1,
    "openinference": 1,
    "opentelemetry": 1
  },
  "replay_classes": {
    "receipt_only": 1,
    "semi_deterministic": 2
  }
}
```

## Explicit Boundaries

- No GitHub release has been created.
- A local git tag may exist only after the release-prep commit is verified.
- No Zenodo DOI has been minted.
- No Hugging Face dataset has been uploaded.
- No Promptfoo package has been published.
- No JOSS submission has been made.
- No upstream issue or pull request has been opened.
- `out/` and `replay/manifests/` are generated local verification artifacts.

## External Commands Not Run

The following publication commands are intentionally not run in this local
release-prep pass:

```bash
git push origin release/v0.2.0
git push origin v0.2.0
gh release create v0.2.0 --title "ATU v0.2 Compiler Release" --notes-file RELEASE_NOTES_v0.2.0.md
huggingface-cli login
```

Reason: the repository has no configured remote in this local checkout, and
external visibility actions require explicit human confirmation.

## Next External Gates

These require explicit human confirmation before action:

1. confirm external publication;
2. add or verify GitHub remote `https://github.com/joy7758/atu-compiler`;
3. push branch `release/v0.2.0` and tag `v0.2.0`;
4. create the GitHub release from `RELEASE_NOTES_v0.2.0.md`;
5. connect Zenodo and mint a software DOI;
6. upload or create a Hugging Face dataset repo;
7. open upstream issues or pull requests;
8. submit the JOSS package.
