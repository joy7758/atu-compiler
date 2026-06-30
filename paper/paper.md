# ATU Compiler: a trace-to-dataset compiler profile for agent episodes

## Summary

ATU Compiler converts heterogeneous agent trace exports into deterministic,
episode-level ATU-IR JSONL. The software is designed for research workflows
that need replay-aware datasets, normalized tool receipts, provenance edges,
and evaluation packages derived from existing observability traces.

## Statement of Need

OpenTelemetry, OpenInference, and LangSmith make agent behavior observable, but
training and evaluation workflows usually operate on examples, episodes, and
labels rather than raw spans. ATU Compiler fills that conversion layer without
introducing a new tracing standard.

## State of the Field

ATU builds on existing trace and evaluation ecosystems: OpenTelemetry for
distributed traces, OpenInference for AI-specific semantic conventions,
LangSmith for run-level observability, Promptfoo for declarative evaluations,
and Hugging Face Datasets for dataset packaging.

## Software Design

The compiler pipeline is:

1. ingest source trace exports;
2. normalize spans or runs into `RawSpan` objects;
3. segment traces into task-bounded episodes;
4. derive steps, evidence edges, receipts, replay manifests, and labels;
5. export ATU JSONL, Hugging Face dataset packages, Promptfoo suites, and
   LangSmith-style diagnostic projections.

## Research Impact Statement

ATU episodes make trace-derived evidence easier to inspect, cite, replay, and
reuse in agent evaluation research. The current alpha uses synthetic examples
and local validation only.

## AI Usage Disclosure

This local alpha repository was prepared with AI coding assistance. Human review
is required before any public release, DOI deposit, upstream contribution, or
JOSS submission.

## Acknowledgements

No external funding or public institutional endorsement is claimed by this local
alpha repository.

## References

References are maintained in `paper/references.bib`.
