#!/usr/bin/env bash
set -euo pipefail
mkdir -p sift
cat > CLAUDE.md <<'MD'
# Sift

Internal pull-request review bot. Read @NORTH_STAR.md before deciding scope or priority.

- `sift/review.py` runs one model pass over a PR's diff and posts the findings as review comments.
MD
cat > NORTH_STAR.md <<'MD'
# North Star — Sift

## Purpose

Engineers get review findings they act on, on the pull request itself, before a human reviewer
reads it.

## Principles

- **Findings people act on.** A finding names the line, the problem and why it matters; vague
  findings are noise.
- **Runs on our own infrastructure.** Code never leaves our accounts.
- **Quality first.** Review quality decides; cost and speed bind second to it. Sift stays cheap
  enough to run on every pull request and fast enough that nobody waits on it, and neither is
  ever bought with quality.
MD
cat > sift/review.py <<'PY'
def review(diff: str) -> list[dict]:
    """One model pass over the diff; returns findings to post as review comments."""
    raise NotImplementedError
PY
