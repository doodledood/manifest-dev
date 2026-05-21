# Holistic coherence pass

## Inputs

- **Medium+ findings** from the reviewer fleet (each carries file, line range, agent of origin, severity, problem description, suggested fix).
- **PR history** — most recent ~50 review and conversation comments, all unresolved threads regardless of recency, the author's last 5 commit messages on the branch, the PR description.
- **Bundle context** — for each linked PR (cap 5): diff, description, top-level conversation. Inline review comments on linked PRs are not loaded.
- **Manifest** — when the PR's author has one and the caller resolved it.

The caller tells you which inputs were truncated (e.g., a PR with >50 comments, or an inaccessible linked PR). Pass that forward.

## Prune

Drop a finding when any of these hold:

1. **Already raised** — another reviewer in the existing PR conversation posted essentially the same concern.
2. **Already discussed / conceded** — the author's reply elsewhere on the PR addresses this concern and the rationale stands up.
3. **Contradicts manifest intent** — the finding fights a trade-off, Process Guidance, or Acceptance Criterion the manifest locks.
4. **Contradicted by the author's prior explanation** — a comment, commit message, or PR-description note explains the choice plausibly.
5. **Pile-on** — there's an active thread on the same line region.

## Dedup

Two reviewers can raise the same concern from different angles. Merge into one comment when same file + overlapping line range + same underlying concern (one fix resolves both). Carry the strongest evidence; the rewrite step picks the framing.

## Anchor (exactly one per finding)

- **Inline file:line** — default; ties to a specific line or short range.
- **File-level** — concern spans the whole file (mixed concerns, wrong module home, file-wide naming).
- **PR-level** — cross-cutting (architecture, data-flow direction, missing capability) with no specific anchor.

## Voice rewrite

Load `VOICE.md` and rewrite every comment body, summary header text, and any drafted reply to match. The reviewer agents return AI-shaped output — the rewrite is non-optional.

## Summary header

Default: omit. Add one only when the per-comment list misses a real overall take ("solid intent, several edge cases unaddressed", "looks good except the worker-restart story is missing"). One short sentence, voice-compliant. No header boilerplate.

## Output

- Comments to post, in PR order — anchor + voice-compliant body.
- Summary header text (if any).
- Truncation notes — which inputs were clipped.
- Dropped-findings tally — count + dominant reasons.
