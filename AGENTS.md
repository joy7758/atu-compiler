All code and documentation in this repository must keep an agent-readable layer.

Operational rules:

- Prefer stable file names, explicit inputs, deterministic outputs, and small
  pure functions.
- Keep the current tool path visible:
  `ingest -> normalize -> compile -> export`.
- Do not describe this working tree as a standard, benchmark, dataset system,
  JOSS submission, or external ecosystem artifact.
- When behavior changes, update `README.md`, `llms.txt`, `PROJECT_STATUS.md`,
  and tests together.
- Keep examples synthetic unless their source license and privacy status are
  explicitly documented.
