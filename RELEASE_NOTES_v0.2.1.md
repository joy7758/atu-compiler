# ATU v0.2.1 Zenodo Activation Release

ATU v0.2.1 is a metadata-only patch release for Zenodo GitHub integration
activation.

The software release metadata is bumped to `0.2.1`. The ATU-IR/profile version,
schemas, fixtures, and generated ATU v0.2 dataset/eval surfaces remain
compatible with v0.2.0. This release exists to generate a GitHub
`release` / `published` event after Zenodo preservation was enabled for
`joy7758/atu-compiler`.

## Included

- ATU v0.2 trace-to-dataset compiler profile.
- OpenTelemetry, OpenInference, and LangSmith-style trace adapters.
- Hugging Face dataset export surface.
- Promptfoo local runtime package and result artifact.
- JOSS submission package material.
- Scientific activation observer with Zenodo ingestion diagnosis.

## Publication Boundary

This release triggered Zenodo archival. The verified Zenodo record is:

```text
doi: 10.5281/zenodo.21087765
concept_doi: 10.5281/zenodo.21087764
record: https://zenodo.org/records/21087765
```

```text
zenodo_doi: verified
```

## Validation Snapshot

Current local release checks:

```bash
make publication-bundles
make scientific-activation-observe
```

Promptfoo local runtime artifact:

```text
evals/promptfoo/results/promptfoo-atu-v0.2.0-20260630T170204Z.json
3 passed, 0 failed, 0 errors
```
