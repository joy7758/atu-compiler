class ATUCompiler:
    """Convert normalized traces into minimal agent episodes."""

    def compile(self, traces: list) -> list:
        episodes = []
        for trace in traces:
            episode = {
                "episode_id": trace.get("trace_id"),
                "steps": trace.get("spans", []),
                "labels": {
                    "success": True,
                },
            }
            episodes.append(episode)
        return episodes
