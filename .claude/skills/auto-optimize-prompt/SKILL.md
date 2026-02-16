---
name: auto-optimize-prompt
description: 'Iteratively auto-optimize a prompt until no issues remain. Uses prompt-reviewer in a loop, asks user for ambiguities, applies fixes via prompt-engineering skill. Runs until converged.'
---

# Auto-Optimize Prompt

**User request**: $ARGUMENTS

Iteratively optimize a prompt until no issues remain.

## Goal

Loop until prompt-reviewer finds no issues: review → resolve NEEDS_USER_INPUT with user → fix via prompt-engineering → repeat.

- **No path provided**: Ask which file to optimize
- **Working copy**: Use `/tmp/auto-optimize-*.md` during iterations; apply to original only when converged

## Constraints

| Constraint | Why |
|------------|-----|
| **Converge, don't cap** | No iteration limits—run until no issues |
| **Atomic output** | Original unchanged until fully converged |
| **DRY** | Delegate review to prompt-reviewer, fixes to prompt-engineering |
| **User-in-the-loop** | NEEDS_USER_INPUT issues require user resolution (with context, options); skip if user declines |

## Output

Report: file path, iterations, issues fixed (auto vs user-resolved), issues skipped, summary of changes.
