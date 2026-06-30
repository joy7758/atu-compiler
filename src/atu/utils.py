from __future__ import annotations

import hashlib
import json
import re
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

SENSITIVE_KEY_RE = re.compile(
    r"(api[_-]?key|authorization|bearer|cookie|secret|token|password|credential)",
    re.IGNORECASE,
)

RAW_PAYLOAD_KEYS = {
    "input",
    "inputs",
    "input.value",
    "output",
    "outputs",
    "output.value",
    "messages",
    "prompt",
    "completion",
}


def read_json(path: str | Path) -> Any:
    with Path(path).open("r", encoding="utf-8") as handle:
        return json.load(handle)


def canonical_json(value: Any) -> str:
    return json.dumps(
        value,
        ensure_ascii=True,
        sort_keys=True,
        separators=(",", ":"),
        default=_json_default,
    )


def _json_default(value: Any) -> str:
    if isinstance(value, datetime):
        return dt_to_iso(value)
    return str(value)


def sha256_hex(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def sha256_ref(value: Any) -> str:
    return f"sha256:{sha256_hex(value)}"


def stable_id(prefix: str, *parts: Any, length: int = 16) -> str:
    digest = sha256_hex([str(part) for part in parts])[:length]
    return f"{prefix}{digest}"


def write_json(path: str | Path, value: Any) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(canonical_json(value) + "\n", encoding="utf-8")


def write_jsonl(path: str | Path, rows: list[dict[str, Any]]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    text = "".join(canonical_json(row) + "\n" for row in rows)
    path.write_text(text, encoding="utf-8")


def read_jsonl(path: str | Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with Path(path).open("r", encoding="utf-8") as handle:
        for line in handle:
            stripped = line.strip()
            if stripped:
                rows.append(json.loads(stripped))
    return rows


def parse_attribute_value(value: Any) -> Any:
    if not isinstance(value, dict):
        return value
    if "stringValue" in value:
        return value["stringValue"]
    if "intValue" in value:
        return int(value["intValue"])
    if "doubleValue" in value:
        return float(value["doubleValue"])
    if "boolValue" in value:
        return bool(value["boolValue"])
    if "bytesValue" in value:
        return value["bytesValue"]
    if "arrayValue" in value:
        values = value["arrayValue"].get("values", [])
        return [parse_attribute_value(item) for item in values]
    if "kvlistValue" in value:
        values = value["kvlistValue"].get("values", [])
        return {
            item.get("key", ""): parse_attribute_value(item.get("value"))
            for item in values
        }
    return value


def flatten_attributes(attributes: Any) -> dict[str, Any]:
    if not attributes:
        return {}
    if isinstance(attributes, dict):
        return dict(attributes)
    result: dict[str, Any] = {}
    for item in attributes:
        key = item.get("key")
        if key:
            result[key] = parse_attribute_value(item.get("value"))
    return result


def unix_nano_to_dt(value: str | int | None) -> datetime:
    if value is None:
        return datetime.fromtimestamp(0, tz=UTC)
    return datetime.fromtimestamp(int(value) / 1_000_000_000, tz=UTC)


def ensure_dt(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value.astimezone(UTC)
    if value is None:
        return datetime.fromtimestamp(0, tz=UTC)
    if isinstance(value, (int, float)):
        return datetime.fromtimestamp(float(value), tz=UTC)
    text = str(value)
    if text.endswith("Z"):
        text = text[:-1] + "+00:00"
    try:
        return datetime.fromisoformat(text).astimezone(UTC)
    except ValueError:
        return datetime.fromtimestamp(0, tz=UTC)


def dt_to_iso(value: datetime) -> str:
    return value.astimezone(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def latency_ms(start: datetime, end: datetime) -> int:
    return max(0, int((end - start).total_seconds() * 1000))


def normalize_status(value: Any, error: Any = None) -> str:
    if error:
        return "error"
    if value is None:
        return "unset"
    if isinstance(value, dict):
        value = value.get("code") or value.get("status_code")
    text = str(value).lower()
    if "error" in text or text == "2":
        return "error"
    if "ok" in text or text == "1":
        return "ok"
    return "unset"


def normalize_kind(name: str | None, kind: str | None, attributes: dict[str, Any]) -> str:
    source_kind = (
        attributes.get("openinference.span.kind")
        or attributes.get("span.kind")
        or attributes.get("langsmith.span.kind")
        or kind
        or attributes.get("run_type")
    )
    text = str(source_kind or "").lower()
    mapping = {
        "agent": "agent",
        "llm": "llm",
        "chat_model": "llm",
        "tool": "tool",
        "retriever": "retriever",
        "chain": "chain",
        "guardrail": "guardrail",
        "evaluator": "evaluator",
        "prompt": "prompt",
    }
    for needle, normalized in mapping.items():
        if needle in text:
            return normalized
    if attributes.get("tool.name") or attributes.get("tool_name"):
        return "tool"
    if any(key.startswith("gen_ai.") for key in attributes) or attributes.get("llm.model_name"):
        return "llm"
    name_text = (name or "").lower()
    if "agent" in name_text:
        return "agent"
    if "retriev" in name_text or "search" in name_text:
        return "retriever"
    return "other"


def safe_metadata(attributes: dict[str, Any], *, strict: bool = False) -> dict[str, Any]:
    metadata: dict[str, Any] = {}
    for key in sorted(attributes):
        value = attributes[key]
        lowered = key.lower()
        if SENSITIVE_KEY_RE.search(key):
            metadata[key] = sha256_ref(value)
            continue
        if lowered in RAW_PAYLOAD_KEYS:
            continue
        if strict and isinstance(value, str) and len(value) > 64:
            metadata[key] = {"digest": sha256_ref(value), "length": len(value)}
            continue
        metadata[key] = compact_value(value)
    return metadata


def compact_value(value: Any) -> Any:
    if isinstance(value, str) and len(value) > 500:
        return {"digest": sha256_ref(value), "length": len(value)}
    if isinstance(value, list):
        return [compact_value(item) for item in value[:50]]
    if isinstance(value, dict):
        return {
            str(key): compact_value(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))[:100]
            if not SENSITIVE_KEY_RE.search(str(key))
        }
    if isinstance(value, (str, int, float, bool)) or value is None:
        return value
    return str(value)


def first_present(*values: Any) -> Any:
    for value in values:
        if value not in (None, "", [], {}):
            return value
    return None


def listify(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, list):
        return [str(item) for item in value]
    return [str(value)]
