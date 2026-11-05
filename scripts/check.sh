#!/usr/bin/env bash
# This repository's checks, in one place: the docs, the property-suite recipe and contributors
# all run this script, so the list cannot drift between them.
#   scripts/check.sh [--fix] [lint|types|tests]...   (no group runs all three)
# --fix lets ruff and black rewrite files; without it they only report.
set -euo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

# The tools come from the project's virtual environment, never from whatever else is on PATH: a
# global mypy cannot see pytest's types and reports dozens of false errors, and a global ruff or
# black may be another version.
if [ ! -x .venv/bin/python ]; then
    echo "check.sh: no virtual environment at .venv; run scripts/setup.sh first" >&2
    exit 2
fi
for tool in ruff black mypy; do
    if [ ! -x ".venv/bin/$tool" ]; then
        echo "check.sh: .venv has no $tool; run scripts/setup.sh to finish installing it" >&2
        exit 2
    fi
done
PATH="$PWD/.venv/bin:$PATH"

fix=false
groups=()
for arg in "$@"; do
    case "$arg" in
        --fix) fix=true ;;
        lint | types | tests) groups+=("$arg") ;;
        *) echo "check.sh: unknown argument '$arg' (expected --fix, lint, types or tests)" >&2; exit 2 ;;
    esac
done
[ ${#groups[@]} -gt 0 ] || groups=(lint types tests)

for group in "${groups[@]}"; do
    case "$group" in
        lint)
            if $fix; then
                ruff check --fix claude-plugins/ tests/ scripts/native_drive.py
                black claude-plugins/ tests/ scripts/native_drive.py
            else
                ruff check claude-plugins/ tests/ scripts/native_drive.py
                black --check claude-plugins/ tests/ scripts/native_drive.py
            fi
            ;;
        types)
            mypy
            npm --prefix scripts run --silent typecheck
            ;;
        tests)
            # Runs across every CPU: pyproject.toml passes `-n auto` (pytest-xdist).
            python -m pytest tests/
            ;;
    esac
done
