# ATU v0.2 Compiler Release

ATU v0.2 is a trace-to-dataset compiler profile for agent systems. It compiles
OpenTelemetry, OpenInference, and LangSmith-style trace exports into
deterministic, episode-level ATU-IR JSONL with replay classes, tool receipts,
labels, and downstream dataset/eval export surfaces.

## Included

- ATU-IR v0.2 JSON Schema.
- Receipt and replay manifest schemas.
- Python package `atu-compiler` and CLI command `atu`.
- Source adapters for OpenTelemetry OTLP JSON, OpenInference OTLP-compatible
  spans, and LangSmith-style run exports.
- Synthetic fixtures for AutoGen-like, CrewAI/OpenInference-like, and
  LangSmith-like traces.
- Hugging Face-style dataset package under `datasets/atu-trace-1000`.
- Promptfoo eval package under `evals/promptfoo`.
- LangSmith-shaped diagnostic projection.
- JOSS paper skeleton under `paper/`.
- Zenodo metadata in `.zenodo.json`.

## Validation Snapshot

Expected local checks:

```bash
make release-check
```

Expected corpus stats:

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

## Publication Boundary

This file is release-note source material. A GitHub release, Zenodo DOI, Hugging
Face dataset upload, Promptfoo package publication, upstream PR, or JOSS
submission exists only after that external action is performed and recorded.
