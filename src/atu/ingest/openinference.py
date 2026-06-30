from __future__ import annotations

from pathlib import Path

from atu.ingest.otlp_json import load_otlp
from atu.models import RawSpan


def load_openinference(path: str | Path) -> list[RawSpan]:
    """Load OpenInference spans represented as OTLP-compatible JSON."""
    return load_otlp(path, force_source="openinference")
