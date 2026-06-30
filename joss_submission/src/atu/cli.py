from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator, FormatChecker

from atu.compiler import build_replay_manifest, compile_file, redact_episode
from atu.export.hf_dataset import export_hf
from atu.export.langsmith_projection import project_langsmith
from atu.export.promptfoo import export_promptfoo
from atu.models import RedactionPolicy, SourceSchema
from atu.utils import canonical_json, read_json, read_jsonl, write_json, write_jsonl


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="atu", description="ATU trace-to-dataset compiler")
    subparsers = parser.add_subparsers(dest="command", required=True)

    compile_parser = subparsers.add_parser("compile", help="compile source trace into ATU JSONL")
    compile_parser.add_argument("--source", choices=["otlp", "opentelemetry", "openinference", "langsmith"], required=True)
    compile_parser.add_argument("--input", required=True)
    compile_parser.add_argument("--output", required=True)
    compile_parser.add_argument("--redaction-policy", choices=["none", "standard", "strict"], default="standard")
    compile_parser.add_argument("--privacy-tier", default="internal")
    compile_parser.set_defaults(func=cmd_compile)

    validate_parser = subparsers.add_parser("validate", help="validate ATU JSONL against JSON Schema")
    validate_parser.add_argument("--input", required=True)
    validate_parser.add_argument("--schema", required=True)
    validate_parser.set_defaults(func=cmd_validate)

    redact_parser = subparsers.add_parser("redact", help="rewrite ATU JSONL with a redaction policy")
    redact_parser.add_argument("--input", required=True)
    redact_parser.add_argument("--policy", choices=["none", "standard", "strict"], required=True)
    redact_parser.add_argument("--output", required=True)
    redact_parser.set_defaults(func=cmd_redact)

    hf_parser = subparsers.add_parser("export-hf", help="export Hugging Face dataset package")
    hf_parser.add_argument("--input", required=True)
    hf_parser.add_argument("--output", required=True)
    hf_parser.set_defaults(func=cmd_export_hf)

    promptfoo_parser = subparsers.add_parser("export-promptfoo", help="export Promptfoo eval package")
    promptfoo_parser.add_argument("--input", required=True)
    promptfoo_parser.add_argument("--output", required=True)
    promptfoo_parser.set_defaults(func=cmd_export_promptfoo)

    project_parser = subparsers.add_parser("project-langsmith", help="project ATU JSONL to LangSmith-shaped JSON")
    project_parser.add_argument("--input", required=True)
    project_parser.add_argument("--output", required=True)
    project_parser.set_defaults(func=cmd_project_langsmith)

    replay_parser = subparsers.add_parser("replay-manifest", help="write replay manifest JSON files")
    replay_parser.add_argument("--input", required=True)
    replay_parser.add_argument("--output", required=True)
    replay_parser.set_defaults(func=cmd_replay_manifest)

    stats_parser = subparsers.add_parser("stats", help="print ATU JSONL corpus stats")
    stats_parser.add_argument("--input", required=True)
    stats_parser.set_defaults(func=cmd_stats)

    return parser


def cmd_compile(args: argparse.Namespace) -> int:
    source = _normalize_source(args.source)
    rows = compile_file(
        source,
        args.input,
        redaction_policy=args.redaction_policy,
        privacy_tier=args.privacy_tier,
    )
    write_jsonl(args.output, rows)
    print(f"wrote {len(rows)} episode(s) to {args.output}")
    return 0


def cmd_validate(args: argparse.Namespace) -> int:
    schema = read_json(args.schema)
    validator = Draft202012Validator(schema, format_checker=FormatChecker())
    rows = read_jsonl(args.input)
    error_count = 0
    for index, row in enumerate(rows, start=1):
        errors = sorted(validator.iter_errors(row), key=lambda error: list(error.path))
        for error in errors:
            path = ".".join(str(part) for part in error.path) or "<root>"
            print(f"{args.input}:{index}:{path}: {error.message}")
            error_count += 1
    if error_count:
        return 1
    print(f"validated {len(rows)} episode(s)")
    return 0


def cmd_redact(args: argparse.Namespace) -> int:
    policy: RedactionPolicy = args.policy
    rows = [redact_episode(row, policy) for row in read_jsonl(args.input)]
    write_jsonl(args.output, rows)
    print(f"wrote {len(rows)} redacted episode(s) to {args.output}")
    return 0


def cmd_export_hf(args: argparse.Namespace) -> int:
    rows = read_jsonl(args.input)
    export_hf(rows, args.output)
    print(f"wrote Hugging Face dataset package to {args.output}")
    return 0


def cmd_export_promptfoo(args: argparse.Namespace) -> int:
    rows = read_jsonl(args.input)
    export_promptfoo(rows, args.output)
    print(f"wrote Promptfoo package to {args.output}")
    return 0


def cmd_project_langsmith(args: argparse.Namespace) -> int:
    rows = read_jsonl(args.input)
    write_json(args.output, project_langsmith(rows))
    print(f"wrote LangSmith projection to {args.output}")
    return 0


def cmd_replay_manifest(args: argparse.Namespace) -> int:
    out_dir = Path(args.output)
    out_dir.mkdir(parents=True, exist_ok=True)
    rows = read_jsonl(args.input)
    for row in rows:
        manifest = build_replay_manifest(row)
        (out_dir / f"{manifest['episode_id']}.json").write_text(canonical_json(manifest) + "\n", encoding="utf-8")
    print(f"wrote {len(rows)} replay manifest(s) to {args.output}")
    return 0


def cmd_stats(args: argparse.Namespace) -> int:
    rows = read_jsonl(args.input)
    stats: dict[str, Any] = {
        "episodes": len(rows),
        "steps": sum(len(row["execution"]["steps"]) for row in rows),
        "receipts": sum(len(row["execution"]["tool_receipts"]) for row in rows),
        "replay_classes": {},
        "source_schemas": {},
    }
    for row in rows:
        _bump(stats["replay_classes"], row["replay"]["class"])
        _bump(stats["source_schemas"], row["source_trace"]["schema"])
    print(json.dumps(stats, sort_keys=True, indent=2))
    return 0


def _normalize_source(source: str) -> SourceSchema:
    if source == "otlp":
        return "opentelemetry"
    return source  # type: ignore[return-value]


def _bump(counter: dict[str, int], key: str) -> None:
    counter[key] = counter.get(key, 0) + 1


if __name__ == "__main__":
    raise SystemExit(main())
