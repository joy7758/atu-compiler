# OpenInference to ATU Mapping

ATU treats OpenInference as the preferred AI semantic convention when its
attributes are present in an OTLP span export.

| OpenInference field | ATU target | Rule |
| --- | --- | --- |
| `openinference.span.kind` | `execution.steps[].kind` | Normalize to ATU enum values. |
| `input.value` | `execution.steps[].input_ref` | Hash the materialized value as `sha256:<hex>`. |
| `output.value` | `execution.steps[].output_ref` | Hash the materialized value as `sha256:<hex>`. |
| `tool.name` | `execution.steps[].tool_name` | Copy and classify the step as `tool`. |
| `llm.model_name` | `execution.steps[].metadata.model` | Preserve compact metadata. |
| `llm.system` | `execution.steps[].metadata.provider` | Preserve compact metadata. |
| `metadata` | `execution.steps[].metadata` | Merge object metadata after sensitive-key filtering. |

ATU does not inline raw prompts or completions by default. The compiler stores
digests and leaves blob storage to a future package or private sidecar.
