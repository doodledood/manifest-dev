#!/usr/bin/env bash
set -euo pipefail
mkdir -p skills/summarize-ticket evals/short-summary evals/results
cat > skills/summarize-ticket/SKILL.md <<'EOF'
---
name: summarize-ticket
description: 'Summarize a support ticket for an agent picking it up.'
---
Read the ticket and write a summary an agent can act on.
EOF
cat > evals/short-summary/prompt.md <<'EOF'
Summarize the ticket in ticket.txt.
EOF
cat > evals/results/2026-09-01.md <<'EOF'
short-summary: 0.58 (12 runs)
EOF
