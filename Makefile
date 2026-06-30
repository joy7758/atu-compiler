.PHONY: test compile-fixtures export-artifacts validate release-check stats publication-bundles zenodo-retrigger-dry-run

PYTHON ?= .venv/bin/python
ATU ?= .venv/bin/atu

test:
	$(PYTHON) -m pytest

compile-fixtures:
	mkdir -p out
	$(ATU) compile --source otlp --input examples/autogen/trace.otlp.json --output out/autogen.jsonl
	$(ATU) compile --source openinference --input examples/crewai/openinference_trace.json --output out/crewai.jsonl
	$(ATU) compile --source langsmith --input examples/langsmith/run_export.json --output out/langsmith.jsonl
	cat out/autogen.jsonl out/crewai.jsonl out/langsmith.jsonl > out/atu.jsonl

validate:
	$(ATU) validate --input out/atu.jsonl --schema schemas/atu-ir.schema.json

export-artifacts:
	$(ATU) export-hf --input out/atu.jsonl --output datasets/atu-trace-1000
	$(ATU) export-promptfoo --input out/atu.jsonl --output evals/promptfoo
	$(ATU) replay-manifest --input out/atu.jsonl --output replay/manifests
	$(ATU) project-langsmith --input out/atu.jsonl --output out/langsmith_projection.json

stats:
	$(ATU) stats --input out/atu.jsonl

release-check: test compile-fixtures validate export-artifacts stats

publication-bundles: release-check
	rm -rf citation_bundle joss_submission hf_dataset/atu_trace_1000 atu_v0.2_joss_submission.zip
	mkdir -p citation_bundle joss_submission hf_dataset/atu_trace_1000
	cp CITATION.cff .zenodo.json RELEASE_NOTES_v0.2.0.md citation_bundle/
	cp -R datasets/atu-trace-1000/. hf_dataset/atu_trace_1000/
	cp paper/paper.md CITATION.cff README.md joss_submission/
	cp -R src datasets joss_submission/
	find joss_submission -name __pycache__ -type d -prune -exec rm -rf {} +
	find joss_submission -name '*.pyc' -delete
	zip -qr atu_v0.2_joss_submission.zip joss_submission

zenodo-retrigger-dry-run:
	scripts/activation/zenodo_retrigger_v0_2_0.sh --dry-run
