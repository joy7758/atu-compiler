import json


def load_trace(path: str):
    with open(path, "r", encoding="utf-8") as file:
        return json.load(file)
