.PHONY: test run clean

PYTHON ?= python3

test:
	$(PYTHON) -m unittest discover -s tests

run:
	$(PYTHON) cli/main.py examples/sample.json out.jsonl

clean:
	rm -f out.jsonl
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
	find . -name '*.pyc' -delete
