def normalize(trace):
    return {
        "trace_id": trace.get("traceId") or trace.get("id"),
        "spans": trace.get("spans", []),
    }
