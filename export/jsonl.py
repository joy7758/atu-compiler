import json


def export_jsonl(episodes, path):
    with open(path, "w", encoding="utf-8") as file:
        for episode in episodes:
            file.write(json.dumps(episode, sort_keys=True) + "\n")
