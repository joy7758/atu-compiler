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
