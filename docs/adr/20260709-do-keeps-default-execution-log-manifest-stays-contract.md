# ADR: /do keeps a default-on execution log; the manifest stays a pure contract

## Status
Accepted

## Context
Deviations from the Initial Approach were invisible: the docs-mode ADR gate lists "approach pivots" as ADR-worthy, but ADR capture lives only in figure-out, which /do never routes through unless an amendment lacks shared understanding — and pivots usually leave no manifest diff, so git doesn't record them either. Two capture homes were considered. An `## Execution Notes` manifest section was drafted first, then rejected on review: the manifest is the acceptance contract, and mixing execution history into it muddies that role. Meanwhile /do already carries a journal mechanism — caller-supplied today (the babysit-pr default journal) — whose content spec already names the pivot material: dead-end memory (fixes tried and reverted, approaches considered and rejected that left no commit) plus operational notes, and which also hosts runaway protection.

## Decision
/do keeps an **append-only execution log by default**, mirroring figure-out's logging pattern: created at a durable out-of-repo home (`~/.manifest-dev/logs/`), path surfaced at run start, `--no-log` opts out. When a caller supplies a journal path (e.g. babysit-pr), that path *is* the log — no second file. The log records execution reality as it happens: deviations from the Initial Approach, dead-end memory, operational notes, verification/repair cycles. The manifest contains no execution history — it stays the contract (what to build, how it's accepted), with Known Assumptions as its only /define-written audit surface. Amendment and post-hoc ADR promotion read the log; a pivot that proves genuinely architectural is promoted to a real ADR through a figure-out session.

## Alternatives Considered
- **`## Execution Notes` manifest section**: append-only notes inside the manifest. — Rejected: pollutes the acceptance contract with journal content; duplicates the journal mechanism /do already has instead of generalizing it.
- **Give /do the docs-mode ADR machinery**: — Rejected: ADR quality needs deliberation over alternatives; mid-execution is the wrong altitude, and stalling the do/verify loop for record-writing inverts priorities.
- **Route pivots into Known Assumptions**: — Rejected: assumptions are defaults chosen under uncertainty; pivots are events that happened.
- **Do nothing (git + completion summary)**: — Rejected: pivots leave no manifest diff, and completion summaries compress; the rationale is lost.

## Consequences

### Positive
- One journal concept across /do instead of two (caller-supplied and default unify); runaway protection and dead-end memory now exist in every long run, not only babysat ones.
- The manifest's role stays crisp: contract in the manifest, history in the log, decisions in ADRs.
- Symmetry with figure-out's log gives the whole suite one logging idiom (`--no-log`, durable home, append-only).

### Negative
- Execution history lives out of sight of the manifest reader; consumers (amendment, /done, users) must be pointed at the log path.
- Default-on writing adds a small per-run overhead and another file per run under `~/.manifest-dev/logs/`.

## Source
- Grounding: suite-alignment review — /do's caller-supplied journal (the babysit-pr default) already carried the deviation and dead-end-memory content spec this decision generalizes; the docs-mode "approach pivots" ADR category had no reachable capture path.
- Related: 20260709-mid-do-steering-stays-autonomous
- Related: 20260709-process-guidance-is-binding-but-unverified
