import json
from pathlib import Path


def export(records):
    by_id = {r["id"]: r for r in records if r["label"]}
    return list(by_id.values())


if __name__ == "__main__":
    Path("output.json").write_text(json.dumps(export(json.loads(Path("records.json").read_text()))))
