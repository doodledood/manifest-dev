"""Writes dashboard.html, a monthly spending summary built from ledger.csv."""

import csv
from pathlib import Path


def rows(path: Path = Path("ledger.csv")) -> list[dict[str, str]]:
    with path.open(newline="") as handle:
        return list(csv.DictReader(handle))


if __name__ == "__main__":
    raise SystemExit("not built yet")
