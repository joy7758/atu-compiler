from __future__ import annotations

from pathlib import Path
from typing import Any

from atu.models import RawSpan
from atu.utils import ensure_dt, normalize_status, read_json


def load_langsmith(path: str | Path) -> list[RawSpan]:
    """Load a LangSmith-style run export into RawSpan objects."""
    data = read_json(path)
    runs = _extract_runs(data)
    spans: list[RawSpan] = []
    for run in runs:
        run_id = str(run.get("id") or run.get("run_id") or run.get("uuid"))
        trace_id = str(
            run.get("trace_id")
            or run.get("traceId")
            or run.get("session_id")
            or run.get("thread_id")
            or run_id
        )
        parent = run.get("parent_run_id") or run.get("parent_id") or run.get("parentRunId")
        attrs = {
            "run_type": run.get("run_type") or run.get("type"),
            "inputs": run.get("inputs"),
            "outputs": run.get("outputs"),
            "error": run.get("error"),
            "tags": run.get("tags"),
            "metadata": run.get("metadata") or run.get("extra", {}).get("metadata"),
            "project_name": run.get("project_name") or run.get("session_name"),
            "thread_id": run.get("thread_id"),
        }
        extra = run.get("extra")
        if isinstance(extra, dict):
            attrs["extra"] = extra
        start = ensure_dt(run.get("start_time") or run.get("startTime") or run.get("created_at"))
        end = ensure_dt(run.get("end_time") or run.get("endTime") or run.get("updated_at") or start)
        spans.append(
            RawSpan(
                source="langsmith",
                trace_id=trace_id,
                span_id=run_id,
                parent_span_id=str(parent) if parent else None,
                name=str(run.get("name") or run_id),
                kind=str(run.get("run_type") or run.get("type")) if run.get("run_type") or run.get("type") else None,
                start_time=start,
                end_time=end,
                status=normalize_status(run.get("status"), run.get("error")),
                attributes={key: value for key, value in attrs.items() if value is not None},
                events=[],
                resource={"service.name": "langsmith"},
            )
        )
    return spans


def _extract_runs(data: Any) -> list[dict[str, Any]]:
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for key in ("runs", "run", "data"):
            value = data.get(key)
            if isinstance(value, list):
                return value
            if isinstance(value, dict):
                return [value]
    raise ValueError("Unsupported LangSmith export shape")
