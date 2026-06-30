# ATU Promptfoo Eval Package

This package is generated from ATU-IR JSONL and is intended as a local
Promptfoo-compatible evaluation scaffold.

Files:

- `promptfooconfig.yaml`: Promptfoo config using a local no-op provider.
- `providers/atu-noop.js`: deterministic provider for offline validation.
- `fixtures/*.json`: full ATU episodes.
- `tests/*/*.yaml`: generated episode test cases.

Boundary:

This directory is a local eval package. It is not published to any package
registry or Promptfoo ecosystem location until an external publication action is
performed.

Current status:

- `package.json` pins `promptfoo@0.121.17`.
- In this local environment, `npx promptfoo eval`, `npx --yes
  promptfoo@0.121.17 --help`, and `npm install --no-audit --no-fund` hung during
  package bootstrap and were interrupted.
- Retry in a stable npm environment with `npm install && npm run eval`.
