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

This is a dataset-card scaffold generated from ATU-IR episodes. The current
package contains 3 synthetic or local episodes. It is ready for
manual Hugging Face repository upload after review, but this repository does
not claim upload until that external action is performed.

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
This scaffold does not claim external publication, DOI assignment, or
third-party validation until those actions are recorded.
