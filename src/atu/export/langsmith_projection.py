from __future__ import annotations

import uuid
from typing import Any


def project_langsmith(episodes: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Project ATU episodes into a LangSmith-shaped diagnostic run tree."""
    traces: list[dict[str, Any]] = []
    for episode in sorted(episodes, key=lambda item: item["episode"]["episode_id"]):
        episode_id = episode["episode"]["episode_id"]
        run_id_by_step = {
            step["step_id"]: str(uuid.uuid5(uuid.NAMESPACE_URL, f"atu:{episode_id}:{step['step_id']}"))
            for step in episode["execution"]["steps"]
        }
        runs = []
        for step in episode["execution"]["steps"]:
            runs.append(
                {
                    "id": run_id_by_step[step["step_id"]],
                    "trace_id": episode_id,
                    "parent_run_id": run_id_by_step.get(step.get("parent_step_id")),
                    "name": step.get("name"),
                    "run_type": step["kind"],
                    "start_time": step["start_time"],
                    "end_time": step["end_time"],
                    "status": step.get("status"),
                    "inputs": {"input_ref": step.get("input_ref")},
                    "outputs": {"output_ref": step.get("output_ref")},
                    "metadata": {
                        "atu_episode_id": episode_id,
                        "atu_step_id": step["step_id"],
                        "replay_class": episode["replay"]["class"],
                        "provenance_completeness": episode["labels"]["provenance_completeness"],
                        "source_trace_id": episode["source_trace"]["trace_id"],
                    },
                }
            )
        traces.append(
            {
                "trace_id": episode_id,
                "source_trace": episode["source_trace"],
                "runs": runs,
            }
        )
    return traces
