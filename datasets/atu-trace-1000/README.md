---
license: mit
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

This is a local dataset-card scaffold generated from ATU-IR episodes. The
current package contains 3 synthetic or local episodes and is not
published to Hugging Face by this repository.

## Dataset Summary

Each row is derived from one ATU episode and includes source trace identity,
task goal, execution steps, evidence edges, tool receipts, replay class, and
deterministic labels.

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
This local scaffold does not claim external publication, DOI assignment, or
third-party validation.
