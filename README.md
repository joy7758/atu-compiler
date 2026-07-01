# ATU Compiler

ATU Compiler is now a small, tool-first trace processor. The current surface is:

```text
ingest -> normalize -> compile -> export
```

It reads a JSON trace, normalizes the trace ID and spans, compiles one or more
minimal agent episodes, and writes JSONL. It does not claim a new standard,
benchmark, dataset ecosystem, JOSS submission, or upstream protocol adoption.

## Layout

- `ingest/loader.py`: loads a JSON trace file.
- `normalize/normalize.py`: maps source fields into a stable internal shape.
- `core/compiler.py`: converts normalized traces into episodes.
- `export/jsonl.py`: writes episodes as JSONL.
- `cli/main.py`: minimal command-line entry point.
- `examples/sample.json`: smallest runnable input.
- `tests/test_basic.py`: smallest compiler test.

## Run

```bash
python3 cli/main.py examples/sample.json out.jsonl
```

Expected output file:

```json
{"episode_id": "demo-1", "labels": {"success": true}, "steps": [{"step": 1, "tool": "search"}, {"step": 2, "tool": "llm"}]}
```

## Test

```bash
python3 -m unittest discover -s tests
```

or:

```bash
make test
```

## Boundary

This repository previously contained release, citation, dataset, eval, and JOSS
submission scaffolding. Those surfaces have been removed from the current
working tree so ATU can be evaluated as a plain engineering tool.

The current code path is intentionally narrow:

- no replay system;
- no receipt system;
- no Hugging Face export;
- no Promptfoo export;
- no JOSS package;
- no ecosystem or standardization claim.

The only current deliverable is a deterministic JSON trace to JSONL episode
processor.
