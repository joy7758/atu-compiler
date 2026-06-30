# OpenTelemetry to ATU Mapping

ATU consumes OpenTelemetry OTLP JSON as an input format. OpenTelemetry remains
the source trace layer; ATU adds an episode-level dataset/eval layer above it.

| OpenTelemetry field | ATU target | Rule |
| --- | --- | --- |
| `traceId` | `source_trace.trace_id` | Copy unchanged. |
| root `spanId` | `source_trace.root_span_id` | Use the first root span after deterministic sorting. |
| `spanId` | `execution.steps[].span_id` | Copy unchanged. |
| `parentSpanId` | `execution.steps[].parent_step_id` | Convert through the span-to-step index. |
| `name` | `execution.steps[].name` | Copy as the default step name. |
| `startTimeUnixNano` | `execution.steps[].start_time` | Convert to RFC 3339 UTC. |
| `endTimeUnixNano` | `execution.steps[].end_time` | Convert to RFC 3339 UTC and compute latency. |
| `status.code` | `execution.steps[].status` | Map error to `error`, ok to `ok`, otherwise `unset`. |
| `gen_ai.*` attributes | `execution.steps[].metadata` | Preserve compact non-sensitive fields. |

Kind inference:

- `openinference.span.kind` wins when present.
- tool-related attributes map to `tool`.
- GenAI model/request/response attributes map to `llm`.
- names containing `agent` map to `agent`.
- otherwise use `other`.
