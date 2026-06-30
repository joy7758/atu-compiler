# ATU Compiler

ATU Compiler is a v0.2 implementation of the **ATU Trace-to-Dataset
Compiler Profile**. It does not define a new tracing standard. It compiles
OpenTelemetry, OpenInference, and LangSmith-style trace exports into
episode-level ATU-IR JSONL for replay-aware datasets and eval suites.

Current status: GitHub release complete; Zenodo GitHub integration and release
webhook delivery complete; Zenodo DOI pending materialization. There is no
confirmed Zenodo DOI, Hugging Face publication, JOSS submission, or upstream PR
until those external actions are performed and recorded.

Hugging Face boundary: the canonical dataset target is locked to
`joy7758/atu-trace-1000` so dataset identity matches the GitHub and Zenodo
identity. Browser authentication has only confirmed a `joy7759` session, with
no visible `joy7758` organization membership, so no HF upload is complete until
HF authentication is switched to `joy7758` and the live dataset URL is recorded.

License: Apache-2.0.

## Agent-Readable Entry Points

- `llms.txt`: compact discovery guide for coding, retrieval, and citation agents.
- `schemas/atu-ir.schema.json`: canonical ATU-IR v0.2 schema.
- `schemas/replay-manifest.schema.json`: replay manifest schema.
- `schemas/receipt.schema.json`: normalized tool receipt schema.
- `rfcs/RFC-0001-atu-ir-v0.2.md`: profile motivation, non-goals, and rules.
- `mapping/`: source-to-ATU mapping notes for OpenTelemetry, OpenInference, and
  LangSmith exports.
- `src/atu/`: Python reference compiler and CLI implementation.
- `examples/`: synthetic source traces.
- `tests/`: deterministic compile, schema, exporter, and CLI regression tests.
- `docs/scientific-citation-observer.md`: read-only external activation
  observer for DOI, dataset, and eval publication gates.
- `ACTIVATION_MANIFEST.json`: machine-readable current publication and
  scientific activation state.

## Install

```bash
python -m pip install -e ".[test]"
```

For local commands without installing:

```bash
PYTHONPATH=src python -m atu.cli --help
```

## Quickstart

Compile a synthetic OpenTelemetry trace into ATU-IR JSONL:

```bash
atu compile \
  --source otlp \
  --input examples/autogen/trace.otlp.json \
  --output out/atu.jsonl
```

Validate the compiled corpus:

```bash
atu validate --input out/atu.jsonl --schema schemas/atu-ir.schema.json
```

Export downstream artifacts:

```bash
atu export-hf --input out/atu.jsonl --output datasets/atu-trace-1000
atu export-promptfoo --input out/atu.jsonl --output evals/promptfoo
atu replay-manifest --input out/atu.jsonl --output replay/manifests
atu project-langsmith --input out/atu.jsonl --output out/langsmith_projection.json
```

Run release checks:

```bash
make release-check
```

Observe external scientific activation state without mutating GitHub release,
tags, assets, Hugging Face, Zenodo, or JOSS:

```bash
make scientific-activation-observe
```

Check that the local Hugging Face identity is safe for the canonical dataset
upload:

```bash
make hf-canonical-identity-check
```

The same read-only observer is available as a manual GitHub Action:
`Scientific Activation Observer`. The GitHub Action skips repository webhook
delivery inspection because that endpoint requires permissions not available to
the default `GITHUB_TOKEN`; local authenticated runs still include it.

## Compiler Contract

The compiler accepts source traces and emits one or more ATU episodes. The
contract is intentionally narrow:

- same input bytes and compiler version produce byte-identical normalized JSONL;
- one source trace compiles into one task-bounded episode unless explicit
  boundaries are present;
- source spans/runs become ATU execution steps;
- side-effecting tool steps receive normalized receipts;
- replay class is derived from receipts and external-state dependencies;
- raw prompts and outputs are represented by digests by default;
- public dataset exports must use synthetic or explicitly licensed and redacted
  data.

## CLI Surface

```text
atu compile --source {otlp,openinference,langsmith} --input PATH --output PATH
atu validate --input PATH --schema schemas/atu-ir.schema.json
atu redact --input PATH --policy {none,standard,strict} --output PATH
atu export-hf --input PATH --output DIR
atu export-promptfoo --input PATH --output DIR
atu project-langsmith --input PATH --output PATH
atu replay-manifest --input PATH --output DIR
atu stats --input PATH
```

## Source Alignment

ATU is positioned above existing trace systems:

- OpenTelemetry trace concepts and GenAI semantic conventions:
  <https://opentelemetry.io/docs/concepts/signals/traces/> and
  <https://github.com/open-telemetry/semantic-conventions-genai>
- OpenInference semantic conventions:
  <https://arize-ai.github.io/openinference/spec/>
- LangSmith OpenTelemetry tracing:
  <https://docs.langchain.com/langsmith/trace-with-opentelemetry>
- Promptfoo configuration and assertions:
  <https://www.promptfoo.dev/docs/configuration/guide/>
- Hugging Face dataset cards and dataset metadata:
  <https://huggingface.co/docs/hub/en/datasets-cards> and
  <https://huggingface.co/docs/datasets/en/package_reference/main_classes>
- GitHub citation files, JOSS submission guidance, and Zenodo/GitHub DOI flow:
  <https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-citation-files>,
  <https://joss.readthedocs.io/en/latest/submitting.html>, and
  <https://docs.github.com/repositories/archiving-a-github-repository/referencing-and-citing-content>

## Release Boundary

This repository contains release-prep and publication-observer files such as
`CITATION.cff`, `paper/paper.md`, dataset cards, export packages, and
`ACTIVATION_MANIFEST.json`. Treat each external surface separately:

- GitHub Release `v0.2.0`: complete.
- Zenodo GitHub integration and webhook delivery: complete.
- Zenodo DOI: pending materialization until Zenodo returns a DOI-bearing record.
- Hugging Face dataset: not published until `hf auth whoami` is `joy7758` and a
  live `joy7758/atu-trace-1000` dataset URL is recorded.
- Promptfoo runtime artifact: not complete until an eval result is generated.
- JOSS submission: not submitted until a JOSS submission URL is recorded.
