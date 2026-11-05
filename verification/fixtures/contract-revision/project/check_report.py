import json
from pathlib import Path

payload = Path("export.json").read_bytes()
assert isinstance(json.loads(payload), list)
assert len(payload) <= 100
print("current report check passed")
