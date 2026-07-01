# Agent-readable Tool Surface

ATU's current working tree is optimized for coding agents that need a small,
direct trace-processing tool.

## Entry Points

- `README.md`: current scope and commands.
- `llms.txt`: compact agent index.
- `cli/main.py`: direct executable command.
- `core/compiler.py`: core transformation.
- `tests/test_basic.py`: behavioral smoke test.

## Contract

Input:

```json
{
  "traceId": "demo-1",
  "spans": []
}
```

Output JSONL row:

```json
{
  "episode_id": "demo-1",
  "steps": [],
  "labels": {
    "success": true
  }
}
```

## Boundary

Do not infer dataset publication, benchmark validity, JOSS submission, replay
verification, or standardization status from this repository. The current
working tree is a minimal tool-first compiler.
