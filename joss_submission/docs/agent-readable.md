# Agent-Readable Design Notes

ATU Compiler is intentionally optimized for coding agents, retrieval agents, and
citation agents.

Agent-readable affordances:

- stable command names and deterministic JSON output;
- JSON Schemas for primary artifacts;
- explicit source mapping docs;
- `llms.txt` with canonical commands and status boundaries;
- synthetic fixtures that compile without network access;
- tests that check determinism and schema validity;
- clear non-claims for DOI, publication, and submission status.

When adding features, update the closest schema, mapping doc, CLI help, fixture,
and test in the same change.
