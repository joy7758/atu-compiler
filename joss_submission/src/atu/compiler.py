from __future__ import annotations

from collections import defaultdict
from pathlib import Path
from typing import Any

from atu import __version__
from atu.ingest.langsmith import load_langsmith
from atu.ingest.openinference import load_openinference
from atu.ingest.otlp_json import load_otlp
from atu.models import RawSpan, RedactionPolicy, ReplayClass, SourceSchema
from atu.utils import (
    canonical_json,
    dt_to_iso,
    first_present,
    latency_ms,
    listify,
    normalize_kind,
    safe_metadata,
    sha256_ref,
    stable_id,
)

ATU_VERSION = "0.2.0"


def load_source(source: SourceSchema, input_path: str | Path) -> list[RawSpan]:
    if source == "opentelemetry":
        return load_otlp(input_path)
    if source == "openinference":
        return load_openinference(input_path)
    if source == "langsmith":
        return load_langsmith(input_path)
    raise ValueError(f"Unsupported source: {source}")


def compile_file(
    source: SourceSchema,
    input_path: str | Path,
    *,
    redaction_policy: RedactionPolicy = "standard",
    privacy_tier: str | None = "internal",
) -> list[dict[str, Any]]:
    return compile_spans(
        load_source(source, input_path),
        redaction_policy=redaction_policy,
        privacy_tier=privacy_tier,
    )


def compile_spans(
    spans: list[RawSpan],
    *,
    redaction_policy: RedactionPolicy = "standard",
    privacy_tier: str | None = "internal",
) -> list[dict[str, Any]]:
    grouped: dict[str, list[RawSpan]] = defaultdict(list)
    for span in spans:
        grouped[span.trace_id].append(span)
    episodes = [
        compile_trace(trace_id, grouped[trace_id], redaction_policy=redaction_policy, privacy_tier=privacy_tier)
        for trace_id in sorted(grouped)
    ]
    return sorted(episodes, key=lambda episode: episode["episode"]["episode_id"])


def compile_trace(
    trace_id: str,
    spans: list[RawSpan],
    *,
    redaction_policy: RedactionPolicy,
    privacy_tier: str | None,
) -> dict[str, Any]:
    ordered = sorted(spans, key=lambda span: (span.start_time, span.end_time, span.span_id))
    span_ids = {span.span_id for span in ordered}
    root = next((span for span in ordered if not span.parent_span_id or span.parent_span_id not in span_ids), ordered[0])
    source_schema = _source_schema(ordered)
    episode_id = stable_id("atu-ep-", source_schema, trace_id, root.span_id, length=18)
    step_ids = {
        span.span_id: f"s{index:03d}-{stable_id('', trace_id, span.span_id, length=8)}"
        for index, span in enumerate(ordered, start=1)
    }
    steps = [_span_to_step(span, step_ids) for span in ordered]
    evidence_edges = _extract_edges(steps)
    receipts = _normalize_receipts(episode_id, steps)
    replay_class = _derive_replay_class(steps, receipts)
    labels = _build_labels(ordered, steps, evidence_edges, replay_class)
    episode = {
        "atu_version": ATU_VERSION,
        "source_trace": {
            "schema": source_schema,
            "trace_id": trace_id,
            "root_span_id": root.span_id,
            "framework": _first_attr(ordered, "framework", "gen_ai.agent.framework", "service.name"),
            "project": _first_attr(ordered, "project", "project_name", "service.namespace"),
            "thread_id": _first_attr(ordered, "thread_id", "langsmith.thread_id"),
        },
        "episode": {
            "episode_id": episode_id,
            "parent_episode_id": None,
            "task_context": _task_context(root),
            "agent_profile": _agent_profile(root),
        },
        "execution": {
            "steps": steps,
            "evidence_edges": evidence_edges,
            "tool_receipts": receipts,
        },
        "replay": {
            "class": replay_class,
            "manifest_ref": f"replay/manifests/{episode_id}.json",
            "redaction_policy": redaction_policy,
            "privacy_tier": privacy_tier,
        },
        "labels": labels,
        "citation": {
            "dataset": None,
            "split": None,
            "software_doi": None,
            "dataset_doi": None,
        },
    }
    return redact_episode(episode, redaction_policy)


def redact_episode(episode: dict[str, Any], policy: RedactionPolicy) -> dict[str, Any]:
    episode = _roundtrip(episode)
    episode["replay"]["redaction_policy"] = policy
    if policy == "none":
        return episode
    strict = policy == "strict"
    for step in episode["execution"]["steps"]:
        step["metadata"] = safe_metadata(step.get("metadata", {}), strict=strict)
        if strict:
            for key in ("input_preview", "output_preview"):
                step["metadata"].pop(key, None)
    return episode


def build_replay_manifest(episode: dict[str, Any]) -> dict[str, Any]:
    receipts = episode["execution"]["tool_receipts"]
    tool_summary: dict[str, dict[str, int | str]] = {}
    for step in episode["execution"]["steps"]:
        tool_name = step.get("tool_name")
        if not tool_name:
            continue
        tool_summary.setdefault(
            tool_name,
            {"tool_name": tool_name, "step_count": 0, "side_effect_count": 0},
        )
        tool_summary[tool_name]["step_count"] += 1
    for receipt in receipts:
        if receipt.get("side_effect"):
            tool_summary.setdefault(
                receipt["tool_name"],
                {"tool_name": receipt["tool_name"], "step_count": 0, "side_effect_count": 0},
            )
            tool_summary[receipt["tool_name"]]["side_effect_count"] += 1
    return {
        "episode_id": episode["episode"]["episode_id"],
        "replay_class": episode["replay"]["class"],
        "environment": {
            "atu_compiler_version": __version__,
            "atu_ir_version": episode["atu_version"],
            "source_schema": episode["source_trace"]["schema"],
        },
        "tools": sorted(tool_summary.values(), key=lambda item: str(item["tool_name"])),
        "receipts": receipts,
        "redaction_policy": episode["replay"]["redaction_policy"],
    }


def _span_to_step(span: RawSpan, step_ids: dict[str, str]) -> dict[str, Any]:
    attributes = span.attributes
    kind = normalize_kind(span.name, span.kind, attributes)
    input_value = first_present(attributes.get("input.value"), attributes.get("input"), attributes.get("inputs"))
    output_value = first_present(attributes.get("output.value"), attributes.get("output"), attributes.get("outputs"))
    metadata = safe_metadata(attributes)
    metadata.update(
        {
            "source": span.source,
            "source_kind": span.kind,
            "resource": safe_metadata(span.resource),
        }
    )
    if span.events:
        metadata["event_count"] = len(span.events)
    cost = _cost_from_attrs(attributes)
    return {
        "step_id": step_ids[span.span_id],
        "span_id": span.span_id,
        "parent_step_id": step_ids.get(span.parent_span_id) if span.parent_span_id else None,
        "kind": kind,
        "name": span.name,
        "tool_name": _tool_name(kind, span),
        "input_ref": sha256_ref(input_value) if input_value is not None else None,
        "output_ref": sha256_ref(output_value) if output_value is not None else None,
        "start_time": dt_to_iso(span.start_time),
        "end_time": dt_to_iso(span.end_time),
        "latency_ms": latency_ms(span.start_time, span.end_time),
        "cost_usd": cost,
        "status": span.status or "unset",
        "metadata": metadata,
    }


def _source_schema(spans: list[RawSpan]) -> SourceSchema:
    if any(span.source == "openinference" for span in spans):
        return "openinference"
    if any(span.source == "langsmith" for span in spans):
        return "langsmith"
    return "opentelemetry"


def _task_context(root: RawSpan) -> dict[str, Any]:
    attrs = root.attributes
    goal = first_present(
        attrs.get("task_context.goal"),
        attrs.get("task.goal"),
        attrs.get("goal"),
        _extract_goal(attrs.get("input.value")),
        _extract_goal(attrs.get("inputs")),
        root.name,
    )
    return {
        "task_type": first_present(attrs.get("task_context.task_type"), attrs.get("task_type"), "agent_trace"),
        "goal": str(goal) if goal is not None else None,
        "constraints": listify(attrs.get("task_context.constraints") or attrs.get("constraints")),
        "policy_context": attrs.get("policy_context") if isinstance(attrs.get("policy_context"), dict) else {},
    }


def _agent_profile(root: RawSpan) -> dict[str, Any]:
    attrs = root.attributes
    return {
        "agent_role": first_present(attrs.get("agent.role"), attrs.get("agent_role")),
        "agent_name": first_present(attrs.get("agent.name"), attrs.get("agent_name")),
        "persona": first_present(attrs.get("agent.persona"), attrs.get("persona")),
        "metadata": safe_metadata(attrs.get("agent.metadata", {}) if isinstance(attrs.get("agent.metadata"), dict) else {}),
    }


def _extract_goal(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        for key in ("goal", "task", "question", "input", "prompt"):
            if value.get(key):
                return str(value[key])
    return canonical_json(value)


def _extract_edges(steps: list[dict[str, Any]]) -> list[dict[str, Any]]:
    if not steps:
        return []
    final_step_id = steps[-1]["step_id"]
    edges: list[dict[str, Any]] = []
    for step in steps:
        if step["kind"] == "tool" and step.get("output_ref"):
            edges.append(
                {
                    "from_step": step["step_id"],
                    "to_claim": None,
                    "to_step": final_step_id,
                    "relation": "supports",
                    "confidence": 0.8,
                }
            )
        if step["kind"] == "retriever":
            edges.append(
                {
                    "from_step": step["step_id"],
                    "to_claim": None,
                    "to_step": _nearest_child(step, steps, {"llm", "agent"}) or final_step_id,
                    "relation": "uses",
                    "confidence": 0.7,
                }
            )
        if step.get("status") == "error":
            edges.append(
                {
                    "from_step": step["step_id"],
                    "to_claim": None,
                    "to_step": final_step_id,
                    "relation": "fails",
                    "confidence": 1.0,
                }
            )
        child_tool = _nearest_child(step, steps, {"tool"})
        if step["kind"] in {"llm", "agent"} and child_tool:
            edges.append(
                {
                    "from_step": step["step_id"],
                    "to_claim": None,
                    "to_step": child_tool,
                    "relation": "produces",
                    "confidence": 0.7,
                }
            )
    return _dedupe_edges(edges)


def _normalize_receipts(episode_id: str, steps: list[dict[str, Any]]) -> list[dict[str, Any]]:
    receipts: list[dict[str, Any]] = []
    for step in steps:
        if step["kind"] != "tool":
            continue
        tool_name = step.get("tool_name") or step.get("name") or "tool"
        receipts.append(
            {
                "receipt_id": stable_id("r-", episode_id, step["step_id"], tool_name, length=18),
                "step_id": step["step_id"],
                "tool_name": tool_name,
                "timestamp": step["end_time"],
                "input_digest": step.get("input_ref"),
                "result_digest": step.get("output_ref") or sha256_ref(None),
                "side_effect": _infer_side_effect(tool_name, step.get("metadata", {})),
                "idempotency_key": _metadata_str(step, "idempotency_key"),
                "uri": _metadata_str(step, "artifact_uri", "url", "uri"),
            }
        )
    return receipts


def _derive_replay_class(steps: list[dict[str, Any]], receipts: list[dict[str, Any]]) -> ReplayClass:
    if any(receipt.get("side_effect") for receipt in receipts):
        return "receipt_only"
    if any(step["kind"] in {"llm", "retriever", "tool"} for step in steps):
        return "semi_deterministic"
    return "deterministic"


def _build_labels(
    spans: list[RawSpan],
    steps: list[dict[str, Any]],
    evidence_edges: list[dict[str, Any]],
    replay_class: ReplayClass,
) -> dict[str, Any]:
    failure_origin_step, failure_mode = _detect_failure_origin(steps)
    success = failure_origin_step is None
    start = min(span.start_time for span in spans)
    end = max(span.end_time for span in spans)
    costs = [step["cost_usd"] for step in steps if step.get("cost_usd") is not None]
    provenance_denominator = len([step for step in steps if step["kind"] in {"tool", "retriever"}])
    provenance = (
        min(1.0, len(evidence_edges) / provenance_denominator)
        if provenance_denominator
        else 0.0
    )
    return {
        "success": success,
        "failure_mode": failure_mode,
        "failure_origin_step": failure_origin_step,
        "cost_usd": round(sum(costs), 8) if costs else None,
        "latency_ms": latency_ms(start, end),
        "redundancy_score": 0.0,
        "provenance_completeness": round(provenance, 4),
        "quality_score": None,
        "policy_violation": False,
        "replay_class": replay_class,
    }


def _detect_failure_origin(steps: list[dict[str, Any]]) -> tuple[str | None, str | None]:
    for step in steps:
        if step.get("status") == "error":
            return step["step_id"], "source_step_error"
        if step["kind"] == "tool" and not step.get("output_ref"):
            return step["step_id"], "tool_contract_failure"
    if steps and not any(edge_source(steps[-1], step) for step in steps):
        return None, None
    return None, None


def edge_source(final_step: dict[str, Any], step: dict[str, Any]) -> bool:
    return step["step_id"] == final_step["step_id"]


def _cost_from_attrs(attributes: dict[str, Any]) -> float | None:
    for key in ("cost_usd", "gen_ai.usage.cost_usd", "ls_cost_usd"):
        if attributes.get(key) is not None:
            try:
                return float(attributes[key])
            except (TypeError, ValueError):
                return None
    return None


def _tool_name(kind: str, span: RawSpan) -> str | None:
    if kind != "tool":
        return None
    return str(
        first_present(
            span.attributes.get("tool.name"),
            span.attributes.get("tool_name"),
            span.attributes.get("name"),
            span.name,
        )
    )


def _infer_side_effect(tool_name: str, metadata: dict[str, Any]) -> bool:
    explicit = metadata.get("side_effect")
    if isinstance(explicit, bool):
        return explicit
    lowered = tool_name.lower()
    side_effect_verbs = (
        "write",
        "create",
        "update",
        "delete",
        "send",
        "upload",
        "push",
        "post",
        "commit",
        "publish",
    )
    if any(verb in lowered for verb in side_effect_verbs):
        return True
    method = str(metadata.get("http.method", "")).lower()
    return method in {"post", "put", "patch", "delete"}


def _nearest_child(
    step: dict[str, Any],
    steps: list[dict[str, Any]],
    kinds: set[str],
) -> str | None:
    for candidate in steps:
        if candidate.get("parent_step_id") == step["step_id"] and candidate["kind"] in kinds:
            return candidate["step_id"]
    return None


def _dedupe_edges(edges: list[dict[str, Any]]) -> list[dict[str, Any]]:
    seen: set[str] = set()
    unique: list[dict[str, Any]] = []
    for edge in edges:
        key = canonical_json(edge)
        if key in seen:
            continue
        seen.add(key)
        unique.append(edge)
    return unique


def _first_attr(spans: list[RawSpan], *keys: str) -> Any:
    for span in spans:
        for key in keys:
            if span.attributes.get(key) not in (None, ""):
                return span.attributes[key]
            if span.resource.get(key) not in (None, ""):
                return span.resource[key]
    return None


def _metadata_str(step: dict[str, Any], *keys: str) -> str | None:
    metadata = step.get("metadata", {})
    for key in keys:
        value = metadata.get(key)
        if value not in (None, "") and isinstance(value, (str, int, float, bool)):
            return str(value)
    return None


def _roundtrip(value: dict[str, Any]) -> dict[str, Any]:
    import json

    return json.loads(canonical_json(value))
