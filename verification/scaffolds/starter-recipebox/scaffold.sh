#!/usr/bin/env bash
# A new project with no history beyond its first commit, working in many areas at once: Python
# code, a web page, a prompt to a paid model, pasted text from outside, and docs. It runs no
# background work, decides no access, stores nothing others read, keeps no personal data and has
# no evals: the setup-project recipe's starter-new-project and starter-away scenarios.
set -euo pipefail
. "$(dirname "${BASH_SOURCE[0]}")/../../scaffold-guard.sh"
mkdir -p src/recipebox/templates src/recipebox/prompts tests docs
cat > README.md <<'EOF'
# Recipebox

A small web app one household runs on its own laptop. Paste a recipe copied from any website and
Recipebox asks a language model to turn it into a shopping list grouped by shop aisle. Lists are
kept in a local SQLite file. There are no accounts: whoever opens the page on the laptop uses it.

Run `python3 -m recipebox`; test with `python3 -m pytest tests/`. See `docs/usage.md`.
EOF
cat > docs/usage.md <<'EOF'
# Using Recipebox

1. Open http://localhost:8000.
2. Paste the recipe text and press **Make list**. Each list costs one model call.
3. Tick items off as you shop; the list stays until you delete it.
EOF
cat > src/recipebox/__init__.py <<'EOF'
EOF
cat > src/recipebox/__main__.py <<'EOF'
"""Serve the Recipebox page on localhost."""
from recipebox.app import serve

serve()
EOF
cat > src/recipebox/app.py <<'EOF'
"""Turn pasted recipes into shopping lists and keep them in a local SQLite file."""
import sqlite3
from pathlib import Path

from recipebox.model import make_list

DB = Path.home() / ".recipebox.sqlite"


def save_list(recipe_text: str) -> list[str]:
    items = make_list(recipe_text)
    with sqlite3.connect(DB) as db:
        db.execute("create table if not exists lists (recipe text, items text)")
        db.execute("insert into lists values (?, ?)", (recipe_text, "\n".join(items)))
    return items


def serve() -> None:
    raise SystemExit("start the local server here")
EOF
cat > src/recipebox/model.py <<'EOF'
"""Ask the model for a shopping list. Each call is billed to the household's API key."""
from pathlib import Path

PROMPT = (Path(__file__).parent / "prompts" / "shopping_list.md").read_text()


def make_list(recipe_text: str) -> list[str]:
    reply = call_model(PROMPT + "\n\n" + recipe_text)
    return [line.strip("- ").strip() for line in reply.splitlines() if line.strip()]


def call_model(text: str) -> str:
    raise NotImplementedError("wire the model provider here")
EOF
cat > src/recipebox/prompts/shopping_list.md <<'EOF'
You turn a recipe into a shopping list. List each ingredient once, with the amount, grouped by
the aisle of an ordinary supermarket. Output one item per line.
EOF
cat > src/recipebox/templates/index.html <<'EOF'
<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>Recipebox</title></head>
<body><h1>Make a shopping list</h1>
<form method="post"><textarea name="recipe"></textarea><button>Make list</button></form>
<ul id="list"></ul></body></html>
EOF
cat > tests/test_model.py <<'EOF'
from recipebox import model


def test_make_list_splits_lines(monkeypatch):
    monkeypatch.setattr(model, "call_model", lambda text: "- flour\n- eggs\n")
    assert model.make_list("cake") == ["flour", "eggs"]
EOF
git -c user.name="Ines Moreau" -c user.email=ines@recipebox.example add -A
git -c user.name="Ines Moreau" -c user.email=ines@recipebox.example commit -qm "feat: first version"
