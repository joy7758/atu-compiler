# LangSmith to ATU Mapping

ATU consumes LangSmith-style run exports as input. LangSmith traces and runs are
diagnostic/observability objects; ATU emits a dataset/eval episode object.

| LangSmith concept | ATU target | Rule |
| --- | --- | --- |
| trace id / session id | `source_trace.trace_id` | Preserve when present, otherwise derive from root run. |
| run id | `execution.steps[].span_id` | Preserve in step metadata and span id. |
| parent run id | `execution.steps[].parent_step_id` | Convert through the run-to-step index. |
| run name | `execution.steps[].name` | Copy unchanged. |
| run type | `execution.steps[].kind` | Normalize to ATU kind enum. |
| inputs | `execution.steps[].input_ref` | Hash the materialized input object. |
| outputs | `execution.steps[].output_ref` | Hash the materialized output object. |
| error | `execution.steps[].status` | Non-empty error maps to `error`. |

Projection back to LangSmith is diagnostic only. ATU remains the normalized
source of truth after compilation.
