# /do: execution logging

Keeps an append-only execution log — on by default for every /do run (`--no-log` opts out) — continuity that survives context loss in long runs: what was implemented, where execution deviated from the Initial Approach and why, which fixes were tried and abandoned, and where each gate stands. Execution history lives here, never in the manifest — the manifest stays the acceptance contract.

This log is not a transcript, a handoff, an ADR (a deviation that proves genuinely architectural is promoted to an ADR through a figure-out session), or the manifest itself — it is the chronological execution line, append-only and portable by path.

## Path

Resolve the active log path before execution starts and surface it immediately.

Create the log at `~/.manifest-dev/logs/do-log-{timestamp}.md` (create the dir; `~` = `$HOME` / `%USERPROFILE%`) — a durable home so logs from multi-day runs survive OS temp cleanup. Fall back to a writable temp path (`/tmp`, else the host temp directory) only when the home directory isn't writable. `{timestamp}` is UTC `YYYYMMDD-HHMMSS`.

**Caller-supplied journal.** When a caller supplies a journal/log path (for example, the default `/babysit-pr` journal), that path *is* the log — no second file.

## Append Discipline

Append only. Never rewrite, reorder, compress, or delete prior entries. If an old entry was wrong, append a correction.

Read the log before deciding retries and comment judgments in a resumed or long-lived run; append after acting. Append after meaningful events — a deliverable implemented, a deviation from the Initial Approach, a fix attempt abandoned, a gate verdict or staleness change, an operational step (retrigger, wait), an escalation. Skip play-by-play narration.

## Content

Record what completed state won't reconstruct on its own:

- **Deviations from the Initial Approach** — what changed and why. The approach is soft; the record of leaving it is not.
- **Dead-end memory** — fixes tried and reverted, approaches considered and rejected that left no commit.
- **Operational notes** — retriggers, waits, environment actions, so those decisions survive context compaction.
- **Gate-ledger updates** — verdicts, staleness marks, re-verification outcomes.

## Entry Shape

Use Markdown. Keep entries concise and factual.

```md
## {UTC timestamp} — {short title}

**Event:** {what happened — deliverable, deviation, dead end, gate change, operational step}
**Why / evidence:** {rationale or verifier output reference}
**Gate ledger:** {verdict/staleness changes; omit if none}
**Next:** {what execution does next; omit if obvious}
```

The shape is a default, not a form to pad. Omit empty fields.
