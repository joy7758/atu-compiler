from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from core.compiler import ATUCompiler
from export.jsonl import export_jsonl
from ingest.loader import load_trace
from normalize.normalize import normalize


def run(input_path, output_path):
    trace = load_trace(input_path)
    normalized = normalize(trace)
    compiler = ATUCompiler()
    episodes = compiler.compile([normalized])
    export_jsonl(episodes, output_path)
    return episodes


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    if len(argv) != 2:
        print("usage: python cli/main.py INPUT_JSON OUTPUT_JSONL", file=sys.stderr)
        return 2
    run(argv[0], argv[1])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
