# RFC-0001: ATU-IR v0.2 Trace-to-Dataset Compiler Profile

Status: v0.2.0 release-prep

## Summary

ATU v0.2 defines a compiler profile that turns existing trace exports into
episode-level, replay-aware, evidence-linked training and evaluation units. It
does not replace OpenTelemetry, OpenInference, LangSmith, Promptfoo, or Hugging
Face Datasets.

## Motivation

Agent traces are useful for debugging, but raw spans are awkward as dataset and
evaluation units. Training and eval workflows usually need task-bounded
episodes with labels, replay classes, provenance, and citation metadata. ATU-IR
provides that intermediate representation.

## Non-Goals

- Define a new base trace protocol.
- Require token-level attribution in v0.2.
- Inline large prompts, completions, or private tool outputs by default.
- Claim public dataset publication, DOI assignment, or JOSS submission from
  local files alone.

## Required Inputs

The v0.2 compiler accepts:

- OpenTelemetry OTLP JSON exports.
- OpenInference spans represented as OTLP JSON or compatible flat exports.
- LangSmith-style run exports.

## Required Output

The compiler emits JSON Lines where every row validates against
`schemas/atu-ir.schema.json`. Each row is one ATU episode.

Required episode fields:

- `source_trace`: source schema, trace id, root span id, and optional framework.
- `episode`: stable `episode_id` and task context.
- `execution`: steps, evidence edges, and tool receipts.
- `replay`: replay class, redaction policy, and optional manifest reference.
- `labels`: success, failure, cost, latency, provenance, and replay labels.

## Determinism

For a fixed compiler version and fixed input bytes, normalized ATU JSONL must be
byte-identical across repeated runs. IDs are derived from source identifiers and
stable hashes, not wall-clock time.

## Replay Classes

- `deterministic`: all material behavior is captured locally.
- `semi_deterministic`: the episode depends on LLMs, retrievers, or external
  state but has no side-effecting receipt.
- `receipt_only`: at least one side-effecting tool step exists; replay should
  use receipts instead of re-executing effects.

## Redaction

`standard` redaction keeps digests and small safe metadata while stripping
secrets and raw large payloads. `strict` redaction keeps only digests, counts,
and non-sensitive execution metadata.

## Source Mapping Priority

1. Prefer OpenInference fields for AI span kind, input/output references, and
   tool names when present.
2. Preserve LangSmith ids in metadata while issuing ATU-local stable ids.
3. Infer from OpenTelemetry GenAI attributes only when richer fields are absent.
4. Fall back to `other` for unknown span kinds.

## Acceptance Criteria

- Schema validation passes for golden episodes.
- Same fixture compiles twice to byte-identical JSONL.
- OpenTelemetry, OpenInference, and LangSmith fixtures compile.
- HF and Promptfoo export packages are generated from ATU JSONL.
- CLI help documents every supported command.
