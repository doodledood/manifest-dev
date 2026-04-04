# Interview Mode: Minimal

User decides scope, constraints, and high-impact items. Agent auto-resolves the rest by picking the recommended option.

## Decision Authority

Ask the user when: (a) the decision materially changes scope or hard constraints, or (b) no recommended option exists because the trade-off depends entirely on user context/preference that can't be inferred. Auto-resolve everything else by picking the recommended option.

## Question Format

Present structured options only when the decision materially affects scope or has no clear recommended choice. For all other items, pick the recommended option and log it as auto-decided.

## Interview Flow

Coverage goals are the same as thorough mode. Assess existing understanding, probe gaps adaptively. Auto-resolve low-impact findings. Only surface findings that affect scope, hard constraints, or have ambiguous trade-offs.

## Checkpoint Behavior

One checkpoint after domain understanding is established (scope confirmation) and one before synthesis (final review of auto-decided items). Keep checkpoints brief — summarize what was auto-decided and invite corrections.

## Finding Sharing

Share only findings that require user input. Auto-decided findings are logged silently and surfaced in the final checkpoint for review.

## Convergence

All five coverage goals apply (same as thorough), but auto-resolve low-impact items. Converge quickly — move to synthesis once scope, constraints, and irreversible decisions are resolved.
