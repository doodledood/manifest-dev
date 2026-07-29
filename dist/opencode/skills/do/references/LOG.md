# /do: execution logging

Keeps an append-only execution log — on by default for every /do run (`--no-log` opts out) — continuity that survives context loss in long runs: what was implemented, where execution deviated from the Initial Approach or the Deliverable order and why, which Process Guidance was departed from, which fixes were tried and abandoned, and where each gate stands. Execution history lives here, never in the manifest — the manifest stays the acceptance contract.

This log is not a transcript, a handoff, an ADR (a deviation that proves genuinely architectural is promoted to an ADR through a figure-out session), or the manifest itself — it is the chronological execution line, append-only and portable by path.

## Path

Resolve the active log path before execution starts and surface it immediately.

Create the log at `~/.manifest-dev/logs/do-log-{timestamp}.md` (create the dir; `~` = `$HOME` / `%USERPROFILE%`) — a durable home so logs from multi-day runs survive OS temp cleanup. Fall back to a writable temp path (`/tmp`, else the host temp directory) only when the home directory isn't writable. `{timestamp}` is UTC `YYYYMMDD-HHMMSS`.

**Caller-supplied journal.** When a caller supplies a journal/log path (for example, the default `/babysit-pr` journal), that path *is* the log — no second file.

## Append Discipline

Append only. Never rewrite, reorder, compress, or delete prior entries. If an old entry was wrong, append a correction.

Read the log before deciding retries and comment judgments in a resumed or long-lived run; append after acting. Append after meaningful events — a deliverable implemented, a deviation from the Initial Approach or the Deliverable order, a Process Guidance departure, a fix attempt abandoned, a gate verdict or staleness change, an operational step (retrigger, wait), an escalation. Skip play-by-play narration.

The first entry fixes the logical run's verification policy: selected mode and explicit verifier model or inherited model choice. A later invocation changing either always starts a fresh logical run and gate ledger. For `/do`'s default timestamped logs, resolve a new physical log file. In a caller-supplied journal, keep the same file, append a `Run initialized` boundary with the new policy, and start an empty active ledger; prior gate verdicts remain historical and are not carried into the new run. This preserves caller-owned continuity without mixing evidence provenance.

## Content

Record what completed state won't reconstruct on its own:

- **Deviations from the Initial Approach or the Deliverable order** — what changed and why, including a resequencing and what forced it. Both are soft; the record of leaving them is not.
- **Process Guidance departures** — which item was set aside and why.
- **Dead-end memory** — fixes tried and reverted, approaches considered and rejected that left no commit.
- **Operational notes** — retriggers, waits, environment actions, so those decisions survive context compaction.
- **Gate-ledger updates** — verdicts, evidence provenance, staleness marks, re-verification outcomes.
- **Sub-threshold findings** — what a gate reported below its own threshold and was handed over rather than repaired.
- **Threshold questions** — a gate whose bar the run read as suspect, and how it settled: amended, affirmed by the user, or recorded with no user to ask. An affirmation settles it for the run, so the record is what keeps it from being raised again after context compaction.

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
