# ATU Promptfoo Eval Package

This package is generated from ATU-IR JSONL and is intended as a local
Promptfoo-compatible evaluation scaffold.

Files:

- `promptfooconfig.yaml`: Promptfoo config using a local no-op provider.
- `providers/atu-noop.js`: deterministic provider for offline validation.
- `fixtures/*.json`: full ATU episodes.
- `tests/*/*.yaml`: generated episode test cases.
- `results/*.json`: local Promptfoo runtime result artifacts.

Boundary:

This directory is a local eval package. It is not published to any package
registry or Promptfoo ecosystem location until an external publication action is
performed.

Current status:

- `package.json` pins `promptfoo@0.121.17`.
- Local runtime artifact generated:
  `results/promptfoo-atu-v0.2.0-20260630T170204Z.json`.
- Eval ID: `eval-dYL-2026-06-30T17:02:05`.
- Result: `3 passed`, `0 failed`, `0 errors`, `6 assertions passed`.
- Local install used `npm install --legacy-peer-deps --omit=optional` plus the
  macOS arm64 `@libsql/darwin-arm64@0.5.29` platform binding required by
  Promptfoo's SQLite layer.

Re-run:

```bash
npm run eval -- --no-share
```
