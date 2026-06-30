# OpenInference PR Draft

Proposes optional ATU-compatible metadata fields:

- `atu.episode_id`
- `atu.replay_class`
- `atu.receipt_ref`
- `atu.failure_origin_step`
- `atu.provenance_completeness`

Purpose:

Enable trace-to-dataset compilation without modifying the OpenInference core
span schema. ATU remains a downstream compiler profile over existing
OpenInference/OpenTelemetry traces.

Suggested wording:

> This proposal adds optional extension attributes for compiling
> OpenInference-compatible traces into episode-level training/evaluation units.
> The goal is not to change OpenInference's span model, but to standardize
> downstream trace-to-dataset compilation hooks for replayable and
> evidence-aware agent episodes.
