# ATU Tool-first Status

Status date: 2026-07-01

## Current State

ATU has been reduced to a minimal engineering tool:

```text
ingest -> normalize -> compile -> export
```

## Present

- `core/compiler.py`
- `ingest/loader.py`
- `normalize/normalize.py`
- `export/jsonl.py`
- `cli/main.py`
- `examples/sample.json`
- `tests/test_basic.py`

## Explicitly Removed From Current Working Tree

- JOSS paper and submission package.
- Hugging Face dataset mirror.
- Promptfoo eval package.
- Replay manifests.
- Receipt schemas.
- RFC/profile documents.
- Scientific activation observer scripts.
- Release activation status ledgers.

## Current Verification

```bash
python3 cli/main.py examples/sample.json out.jsonl
python3 -m unittest discover -s tests
```

## Boundary

Historical tags/releases may still exist in GitHub history. This status file
describes the current working tree after the tool-first reset.
