from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal

SourceSchema = Literal["opentelemetry", "openinference", "langsmith"]
StepKind = Literal[
    "agent",
    "llm",
    "tool",
    "retriever",
    "chain",
    "guardrail",
    "evaluator",
    "prompt",
    "other",
]
StepStatus = Literal["ok", "error", "unset"]
ReplayClass = Literal["deterministic", "semi_deterministic", "receipt_only"]
RedactionPolicy = Literal["none", "standard", "strict"]


@dataclass(frozen=True)
class RawSpan:
    source: SourceSchema
    trace_id: str
    span_id: str
    parent_span_id: str | None
    name: str
    kind: str | None
    start_time: datetime
    end_time: datetime
    status: StepStatus | None
    attributes: dict[str, Any] = field(default_factory=dict)
    events: list[dict[str, Any]] = field(default_factory=list)
    resource: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class EpisodeDraft:
    source_trace: dict[str, Any]
    episode_id: str
    spans: list[RawSpan]
    task_context: dict[str, Any]
    steps: list[dict[str, Any]]
