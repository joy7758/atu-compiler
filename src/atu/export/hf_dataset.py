from __future__ import annotations

from pathlib import Path
from typing import Any

from atu.utils import canonical_json


def export_hf(episodes: list[dict[str, Any]], out_dir: str | Path) -> None:
    """Write a Hugging Face-style dataset package from ATU episodes."""
    out_path = Path(out_dir)
    data_dir = out_path / "data"
    data_dir.mkdir(parents=True, exist_ok=True)
    splits = split_episodes(episodes)
    for split, rows in splits.items():
        _write_split(data_dir / f"{split}.jsonl", [_flatten_episode(row, split) for row in rows])
    (out_path / "README.md").write_text(dataset_card(episodes), encoding="utf-8")
    (out_path / "dataset_infos.json").write_text(
        canonical_json(dataset_infos(splits)) + "\n",
        encoding="utf-8",
    )


def split_episodes(episodes: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    ordered = sorted(episodes, key=lambda episode: episode["episode"]["episode_id"])
    count = len(ordered)
    if count == 0:
        return {"train": [], "eval": [], "test": []}
    if count == 1:
        return {"train": ordered, "eval": [], "test": []}
    train_end = max(1, int(count * 0.70))
    eval_end = max(train_end + 1, int(count * 0.85)) if count > 2 else count
    return {
        "train": ordered[:train_end],
        "eval": ordered[train_end:eval_end],
        "test": ordered[eval_end:],
    }


def dataset_card(episodes: list[dict[str, Any]]) -> str:
    return f"""---
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
package contains {len(episodes)} synthetic or local episodes. It is ready for
manual Hugging Face repository upload after review, but this repository does
not claim upload until that external action is performed.

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
This scaffold does not claim external publication, DOI assignment, or
third-party validation until those actions are recorded.
"""


def dataset_infos(splits: dict[str, list[dict[str, Any]]]) -> dict[str, Any]:
    return {
        "atu-trace-1000": {
            "description": "ATU trace-to-dataset compiler output scaffold.",
            "citation": "See CITATION.cff in the software repository.",
            "homepage": "local-only",
            "license": "apache-2.0",
            "features": {
                "episode_id": {"dtype": "string", "_type": "Value"},
                "source_schema": {"dtype": "string", "_type": "Value"},
                "source_trace_id": {"dtype": "string", "_type": "Value"},
                "framework": {"dtype": "string", "_type": "Value"},
                "task_type": {"dtype": "string", "_type": "Value"},
                "goal": {"dtype": "string", "_type": "Value"},
                "steps": {"_type": "List", "feature": {"_type": "Json"}},
                "evidence_edges": {"_type": "List", "feature": {"_type": "Json"}},
                "tool_receipts": {"_type": "List", "feature": {"_type": "Json"}},
                "replay_class": {"dtype": "string", "_type": "Value"},
                "success": {"dtype": "bool", "_type": "Value"},
                "failure_mode": {"dtype": "string", "_type": "Value"},
                "failure_origin_step": {"dtype": "string", "_type": "Value"},
                "cost_usd": {"dtype": "float32", "_type": "Value"},
                "latency_ms": {"dtype": "int64", "_type": "Value"},
                "redundancy_score": {"dtype": "float32", "_type": "Value"},
                "provenance_completeness": {"dtype": "float32", "_type": "Value"},
                "quality_score": {"dtype": "float32", "_type": "Value"},
                "policy_violation": {"dtype": "bool", "_type": "Value"},
                "input": {"_type": "Json"},
                "output": {"_type": "Json"},
                "metadata": {"_type": "Json"},
            },
            "splits": {
                split: {"name": split, "num_examples": len(rows)}
                for split, rows in splits.items()
            },
            "version": "0.2.0",
        }
    }


def _flatten_episode(episode: dict[str, Any], split: str) -> dict[str, Any]:
    labels = episode["labels"]
    steps = episode["execution"]["steps"]
    return {
        "episode_id": episode["episode"]["episode_id"],
        "source_schema": episode["source_trace"]["schema"],
        "source_trace_id": episode["source_trace"]["trace_id"],
        "framework": episode["source_trace"].get("framework"),
        "task_type": episode["episode"]["task_context"].get("task_type"),
        "goal": episode["episode"]["task_context"].get("goal"),
        "steps": steps,
        "evidence_edges": episode["execution"]["evidence_edges"],
        "tool_receipts": episode["execution"]["tool_receipts"],
        "replay_class": episode["replay"]["class"],
        "success": labels.get("success"),
        "failure_mode": labels.get("failure_mode"),
        "failure_origin_step": labels.get("failure_origin_step"),
        "cost_usd": labels.get("cost_usd"),
        "latency_ms": labels.get("latency_ms"),
        "redundancy_score": labels.get("redundancy_score"),
        "provenance_completeness": labels.get("provenance_completeness"),
        "quality_score": labels.get("quality_score"),
        "policy_violation": labels.get("policy_violation"),
        "input": {"refs": _refs(steps, "input_ref")},
        "output": {"refs": _refs(steps, "output_ref")},
        "metadata": {"split": split, "atu_version": episode["atu_version"]},
    }


def _refs(steps: list[dict[str, Any]], field: str) -> list[str]:
    return [step[field] for step in steps if step.get(field)]


def _write_split(path: Path, rows: list[dict[str, Any]]) -> None:
    path.write_text("".join(canonical_json(row) + "\n" for row in rows), encoding="utf-8")
