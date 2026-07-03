# figure-out: logging

Keeps an append-only investigation journal for long figure-out sessions — continuity that survives context loss: what was learned, why the read shifted, which surprises matter, what remains open, and what crux should be pressed next.

This log is not a transcript (raw conversation history), a handoff (curated rewrite for a future agent), an ADR (durable decision record), or a Manifest (execution contract) — it is the chronological investigation line, append-only and portable by path.

## Path

Resolve the active log path before the first question and surface it immediately.

Create the log at `~/.manifest-dev/logs/figure-out-log-{timestamp}.md` (create the dir; `~` = `$HOME` / `%USERPROFILE%`) — a durable home so logs from long investigations survive OS temp cleanup. Fall back to a writable temp path (`/tmp`, else the host temp directory) only when the home directory isn't writable. `{timestamp}` is UTC `YYYYMMDD-HHMMSS`.

## Append Discipline

Append only. Never rewrite, reorder, compress, or delete prior entries. If an old entry was wrong, append a correction with the new evidence.

Append after each meaningful user turn or evidence-gathering pass, before asking the next question. Meaningful means the investigation gained evidence, found a surprise, changed its read, opened or closed a thread, or identified a new crux. Skip pure acknowledgements and empty procedural chatter.

When resuming an existing log, read enough of it to recover open threads and the current line of investigation before pressing forward.

## Entry Shape

Use Markdown. Keep entries concise and factual; do not copy the transcript. Entries serialize what the investigation already carries — belief-register state and ledger claims with the provenance and epistemic status the skill's discipline assigns them — so the line of reasoning survives context loss. The log records that discipline's output; it does not redefine it.

Recommended shape:

```md
## {UTC timestamp} — {short title}

**Current belief:** {leading read + confidence, when there is one}
**Evidence:** {refs or quotes}
**Evidence against / limits:** {disconfirming evidence, weak spots, or why confidence is bounded}
**Finding / surprise:** {what changed or was learned}
**Belief update:** {how the read shifted; omit if unchanged}
**Open threads:** {sharp unresolved questions — a question is sharp when you can state it precisely now, regardless of whether you can answer it; omit if none}
**Fog:** {areas sensed but not yet statable as questions — don't pre-slice into sub-questions; a patch may resolve into several questions or none; omit if none}
**Next crux:** {the next load-bearing question; omit if not yet clear}
```

The shape is a default, not a form to pad. Omit empty fields; add a field only when it carries information.

## Composition

Logging composes with other figure-out modes. It records the active mode's findings and reasoning shifts; it does not change docs-mode glossary/ADR behavior or `--autonomous` self-answering behavior.
