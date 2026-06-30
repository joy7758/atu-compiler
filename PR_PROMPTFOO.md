# Promptfoo PR Draft

Adds an ATU evaluation adapter example:

- converts ATU JSONL episodes into Promptfoo test cases;
- preserves `replay_class`, provenance, and source trace metadata;
- supports generated JavaScript assertions for ATU-specific checks;
- validates tool-use expectations without changing Promptfoo's core config
  model.

Suggested wording:

> This PR adds an example workflow that converts ATU JSONL episodes into
> Promptfoo tests and assertions. It demonstrates how episode metadata such as
> replay class, expected tool usage, and provenance thresholds can be evaluated
> through generated test cases without changing Promptfoo's core configuration
> model.
