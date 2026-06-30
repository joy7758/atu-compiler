from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from atu.export.hf_dataset import split_episodes
from atu.utils import canonical_json


def export_promptfoo(episodes: list[dict[str, Any]], out_dir: str | Path) -> None:
    out_path = Path(out_dir)
    tests_dir = out_path / "tests"
    fixtures_dir = out_path / "fixtures"
    providers_dir = out_path / "providers"
    for directory in (tests_dir, fixtures_dir, providers_dir):
        directory.mkdir(parents=True, exist_ok=True)

    (providers_dir / "atu-noop.js").write_text(NOOP_PROVIDER, encoding="utf-8")
    (out_path / "promptfooconfig.yaml").write_text(CONFIG, encoding="utf-8")

    splits = split_episodes(episodes)
    for split, rows in splits.items():
        split_dir = tests_dir / split
        split_dir.mkdir(parents=True, exist_ok=True)
        for episode in rows:
            episode_id = episode["episode"]["episode_id"]
            fixture_path = fixtures_dir / f"{episode_id}.json"
            fixture_path.write_text(canonical_json(episode) + "\n", encoding="utf-8")
            (split_dir / f"{episode_id}.yaml").write_text(
                test_case(episode, fixture_path.relative_to(out_path)),
                encoding="utf-8",
            )


CONFIG = """description: "ATU replayable eval suite"
providers:
  - id: file://providers/atu-noop.js

defaultTest:
  metadata:
    source: atu-jsonl

tests:
  - file://tests/train/*.yaml
  - file://tests/eval/*.yaml
  - file://tests/test/*.yaml
"""


NOOP_PROVIDER = """module.exports = {
  id: 'atu-noop',
  async callApi(prompt, context) {
    return {
      output: JSON.stringify({
        ok: true,
        episode_id: context.vars.episode_id,
        replay_class: context.vars.replay_class
      })
    };
  }
};
"""


def test_case(episode: dict[str, Any], fixture_path: Path) -> str:
    episode_id = episode["episode"]["episode_id"]
    goal = json.dumps(episode["episode"]["task_context"].get("goal") or "")
    replay_class = episode["replay"]["class"]
    provenance = episode["labels"].get("provenance_completeness")
    return f"""description: "ATU episode {episode_id}"
vars:
  episode_id: "{episode_id}"
  replay_class: "{replay_class}"
  task_goal: {goal}
  input_payload: "file://{fixture_path.as_posix()}"
assert:
  - type: contains-json
  - type: javascript
    value: |
      const parsed = JSON.parse(output);
      return parsed.ok === true && parsed.episode_id === vars.episode_id;
metadata:
  replay_class: "{replay_class}"
  provenance_min: {provenance}
"""
