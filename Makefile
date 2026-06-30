.PHONY: test compile-fixtures export-artifacts validate release-check stats

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
