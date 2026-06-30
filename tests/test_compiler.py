from __future__ import annotations

from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker

from atu.compiler import build_replay_manifest, compile_file
from atu.export.hf_dataset import export_hf
from atu.export.langsmith_projection import project_langsmith
from atu.export.promptfoo import export_promptfoo
from atu.utils import canonical_json, read_json

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = read_json(ROOT / "schemas" / "atu-ir.schema.json")


def validate_episode(episode: dict) -> None:
    Draft202012Validator(SCHEMA, format_checker=FormatChecker()).validate(episode)


def test_minimal_otlp_compile_validates_and_is_deterministic() -> None:
    fixture = ROOT / "tests" / "fixtures" / "otlp" / "minimal_trace.json"
    first = compile_file("opentelemetry", fixture)
    second = compile_file("opentelemetry", fixture)

    assert canonical_json(first) == canonical_json(second)
    assert len(first) == 1
    episode = first[0]
    validate_episode(episode)
    assert episode["source_trace"]["schema"] == "opentelemetry"
    assert episode["labels"]["success"] is True
    assert episode["labels"]["replay_class"] == "semi_deterministic"
    assert episode["execution"]["steps"][0]["input_ref"].startswith("sha256:")


def test_openinference_tool_receipt_sets_receipt_only_replay() -> None:
    episodes = compile_file("openinference", ROOT / "examples" / "crewai" / "openinference_trace.json")
    episode = episodes[0]

    validate_episode(episode)
    receipts = episode["execution"]["tool_receipts"]
    assert episode["source_trace"]["schema"] == "openinference"
    assert len(receipts) == 1
    assert receipts[0]["side_effect"] is True
    assert episode["replay"]["class"] == "receipt_only"
    assert episode["labels"]["replay_class"] == "receipt_only"


def test_langsmith_compile_and_projection() -> None:
    episodes = compile_file("langsmith", ROOT / "examples" / "langsmith" / "run_export.json")
    episode = episodes[0]

    validate_episode(episode)
    projection = project_langsmith(episodes)
    assert projection[0]["trace_id"] == episode["episode"]["episode_id"]
    assert len(projection[0]["runs"]) == len(episode["execution"]["steps"])


def test_exporters_write_agent_readable_packages(tmp_path: Path) -> None:
    episodes = []
    episodes.extend(compile_file("opentelemetry", ROOT / "examples" / "autogen" / "trace.otlp.json"))
    episodes.extend(compile_file("openinference", ROOT / "examples" / "crewai" / "openinference_trace.json"))
    episodes.extend(compile_file("langsmith", ROOT / "examples" / "langsmith" / "run_export.json"))

    hf_dir = tmp_path / "hf"
    promptfoo_dir = tmp_path / "promptfoo"
    export_hf(episodes, hf_dir)
    export_promptfoo(episodes, promptfoo_dir)

    assert (hf_dir / "README.md").exists()
    assert (hf_dir / "dataset_infos.json").exists()
    assert (hf_dir / "data" / "train.jsonl").exists()
    assert (promptfoo_dir / "promptfooconfig.yaml").exists()
    assert (promptfoo_dir / "providers" / "atu-noop.js").exists()


def test_replay_manifest_shape() -> None:
    episode = compile_file("openinference", ROOT / "examples" / "crewai" / "openinference_trace.json")[0]
    manifest = build_replay_manifest(episode)

    assert manifest["episode_id"] == episode["episode"]["episode_id"]
    assert manifest["replay_class"] == "receipt_only"
    assert manifest["tools"][0]["side_effect_count"] == 1
