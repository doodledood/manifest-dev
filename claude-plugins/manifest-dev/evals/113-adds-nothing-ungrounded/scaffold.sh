#!/usr/bin/env bash
set -euo pipefail
mkdir -p jot tests
cat > README.md <<'EOF'
# jot

A one-person journal on the command line. `jot add "text"` writes an entry with the current
date and time; `jot list` prints them; `jot export` prints them as Markdown, one heading per day.
Entries live in one JSON-lines file, `$JOT_FILE` or `~/.jot.jsonl`. Standard library only.
EOF
cat > jot/__init__.py <<'EOF'
EOF
cat > jot/store.py <<'EOF'
import json
import os
from datetime import datetime
from pathlib import Path


def path() -> Path:
    return Path(os.environ.get("JOT_FILE", Path.home() / ".jot.jsonl"))


def add(text: str, now: datetime | None = None) -> None:
    entry = {"ts": (now or datetime.now()).isoformat(timespec="minutes"), "text": text}
    with path().open("a") as f:
        f.write(json.dumps(entry) + "\n")


def entries() -> list[dict]:
    if not path().exists():
        return []
    return [json.loads(line) for line in path().read_text().splitlines() if line.strip()]
EOF
cat > jot/export.py <<'EOF'
from itertools import groupby


def to_markdown(entries: list[dict]) -> str:
    out = []
    for day, items in groupby(entries, key=lambda e: e["ts"][:10]):
        out.append(f"## {day}")
        out.extend(f"- {e['text']}" for e in items)
        out.append("")
    return "\n".join(out)
EOF
cat > jot/cli.py <<'EOF'
import argparse

from . import export, store


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(prog="jot")
    sub = parser.add_subparsers(dest="cmd", required=True)
    add = sub.add_parser("add")
    add.add_argument("text")
    sub.add_parser("list")
    sub.add_parser("export")
    args = parser.parse_args(argv)
    if args.cmd == "add":
        store.add(args.text)
    elif args.cmd == "list":
        for e in store.entries():
            print(e["ts"], e["text"])
    else:
        print(export.to_markdown(store.entries()))


if __name__ == "__main__":
    main()
EOF
cat > tests/test_export.py <<'EOF'
from jot.export import to_markdown


def test_one_heading_per_day():
    entries = [
        {"ts": "2026-11-09T08:00", "text": "a"},
        {"ts": "2026-11-09T21:00", "text": "b"},
        {"ts": "2026-11-10T07:30", "text": "c"},
    ]
    assert to_markdown(entries) == "## 2026-11-09\n- a\n- b\n\n## 2026-11-10\n- c\n"
EOF
