# Historical sample check.
from exporter import export
assert export([{"id": "a", "label": "A"}]) == [{"id": "a", "label": "A"}]
print("sample passed")
