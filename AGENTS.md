All code, schemas, docs, and examples in this repository must expose an
agent-readable layer.

Operational rules:

- Prefer stable file names, explicit schemas, deterministic IDs, and small
  pure functions over implicit behavior.
- Keep protocol boundaries visible: source traces, ATU-IR episodes, replay
  manifests, receipts, dataset exports, and eval exports are separate
  artifacts.
- Do not describe local artifacts as published, submitted, DOI-backed, or
  externally validated unless that external action has happened.
- Add machine-discoverable entry points when behavior changes: update
  `README.md`, `llms.txt`, schemas, CLI help, and tests together.
- Keep examples synthetic unless their source license and privacy status are
  explicitly documented.
