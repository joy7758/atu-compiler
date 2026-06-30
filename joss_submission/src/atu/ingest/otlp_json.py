from __future__ import annotations

from pathlib import Path
from typing import Any

from atu.models import RawSpan, SourceSchema
from atu.utils import (
    ensure_dt,
    flatten_attributes,
    normalize_status,
    read_json,
    unix_nano_to_dt,
)


def load_otlp(path: str | Path, *, force_source: SourceSchema | None = None) -> list[RawSpan]:
    """Load OTLP JSON resource spans into RawSpan objects."""
    data = read_json(path)
    spans: list[RawSpan] = []

    if isinstance(data, dict) and "resourceSpans" in data:
        for resource_span in data.get("resourceSpans", []):
            resource = flatten_attributes(resource_span.get("resource", {}).get("attributes", []))
            for scope_span in resource_span.get("scopeSpans", []):
                scope = flatten_attributes(scope_span.get("scope", {}).get("attributes", []))
                for span in scope_span.get("spans", []):
                    spans.append(_parse_otlp_span(span, resource | scope, force_source))
        return spans

    flat_spans = data.get("spans", data) if isinstance(data, dict) else data
    if not isinstance(flat_spans, list):
        raise ValueError(f"Unsupported OTLP JSON shape in {path}")
    for span in flat_spans:
        spans.append(_parse_otlp_span(span, {}, force_source))
    return spans


def _parse_otlp_span(
    span: dict[str, Any],
    resource: dict[str, Any],
    force_source: SourceSchema | None,
) -> RawSpan:
    attributes = flatten_attributes(span.get("attributes", {}))
    events = [
        {
            "name": event.get("name"),
            "time": event.get("timeUnixNano") or event.get("time"),
            "attributes": flatten_attributes(event.get("attributes", {})),
        }
        for event in span.get("events", [])
    ]
    source: SourceSchema = force_source or (
        "openinference" if "openinference.span.kind" in attributes else "opentelemetry"
    )
    start = (
        unix_nano_to_dt(span.get("startTimeUnixNano"))
        if span.get("startTimeUnixNano") is not None
        else ensure_dt(span.get("start_time") or span.get("startTime"))
    )
    end = (
        unix_nano_to_dt(span.get("endTimeUnixNano"))
        if span.get("endTimeUnixNano") is not None
        else ensure_dt(span.get("end_time") or span.get("endTime"))
    )
    trace_id = str(span.get("traceId") or span.get("trace_id") or "missing-trace")
    span_id = str(span.get("spanId") or span.get("span_id") or trace_id)
    parent_id = span.get("parentSpanId") or span.get("parent_span_id")
    return RawSpan(
        source=source,
        trace_id=trace_id,
        span_id=span_id,
        parent_span_id=str(parent_id) if parent_id else None,
        name=str(span.get("name") or span_id),
        kind=str(span.get("kind")) if span.get("kind") is not None else None,
        start_time=start,
        end_time=end,
        status=normalize_status(span.get("status")),
        attributes=attributes,
        events=events,
        resource=resource,
    )
