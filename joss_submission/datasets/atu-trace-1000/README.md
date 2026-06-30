---
license: apache-2.0
task_categories:
  - text-generation
tags:
  - agent-traces
  - opentelemetry
  - openinference
  - evaluation
pretty_name: ATU Trace 1000
size_categories:
  - n<1K
---

# ATU Trace 1000

This dataset card describes the ATU v0.2 Hugging Face dataset publication at
`joy7759/atu-trace-1000`. The package contains 3 synthetic or
local episodes compiled from ATU-IR. The HF namespace `joy7759` is the active
Hugging Face account for the same owner as the GitHub namespace `joy7758`, per
maintainer confirmation on 2026-06-30.

## Dataset Summary

Each row is derived from one ATU episode and includes source trace identity,
task goal, execution steps, evidence edges, tool receipts, replay class, and
deterministic labels.

Nested fields such as `steps`, `evidence_edges`, `tool_receipts`, `input`,
`output`, and `metadata` are canonical JSON strings so the package can be loaded
with the standard Hugging Face JSON loader without a custom dataset script.

## Data Fields

- `episode_id`
- `source_schema`
- `source_trace_id`
- `framework`
- `task_type`
- `goal`
- `steps`
- `evidence_edges`
- `tool_receipts`
- `replay_class`
- `success`
- `failure_mode`
- `failure_origin_step`
- `cost_usd`
- `latency_ms`
- `redundancy_score`
- `provenance_completeness`
- `quality_score`
- `policy_violation`
- `input`
- `output`
- `metadata`

## Privacy and Licensing

Public exports must use synthetic or explicitly licensed traces after redaction.
This dataset is externally published on Hugging Face. It does not claim DOI
assignment or third-party validation until those actions are separately
recorded.
