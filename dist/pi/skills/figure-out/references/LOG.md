# figure-out: --log

Keeps an append-only narrative investigation journal for long figure-out sessions. The log is evidence-based continuity: what was learned, why the read shifted, which surprises matter, what remains open, and what crux should be pressed next.

This log is not a transcript, handoff, ADR, or Manifest:

- **Transcript** is raw conversation history.
- **Handoff** is a curated rewrite for a future agent or session.
- **ADR** records durable decisions and their alternatives.
- **Manifest** is an execution contract.
- **Log** is the chronological investigation line, append-only and portable by path.

## Path

Resolve the active log path before the first question and surface it immediately.

- `--log` with no path creates the log at `~/.manifest-dev/logs/figure-out-log-{timestamp}.md` (create the dir; `~` = `$HOME` / `%USERPROFILE%`) — a durable home so logs from long investigations survive OS temp cleanup. Fall back to a writable temp path (`/tmp`, else the host temp directory) only when the home directory isn't writable. `{timestamp}` is UTC `YYYYMMDD-HHMMSS`.
- `--log <path>` appends to that explicit path. Relative paths resolve from the current workspace directory. Existing files are resumed; new files are created.
- Create parent directories only for an explicit path, and only when the target location is clear and writable. If creating the parent would be ambiguous or unsafe, ask for a different path instead of silently choosing one.

## Append Discipline

Append only. Never rewrite, reorder, compress, or delete prior entries. If an old entry was wrong, append a correction with the new evidence.

Append after each meaningful user turn or evidence-gathering pass, before asking the next question. Meaningful means the investigation gained evidence, found a surprise, changed its read, opened or closed a thread, or identified a new crux. Skip pure acknowledgements and empty procedural chatter.

When resuming an existing log, read enough of it to recover open threads and the current line of investigation before pressing forward.

## Entry Shape

Use Markdown. Keep entries concise and factual; do not copy the transcript. Every factual claim needs provenance: file path and line, command result, URL, document name, quoted user statement, or named prior log entry.

Recommended shape:

```md
## {UTC timestamp} — {short title}

**Current belief:** {leading read + confidence, when there is one}
**Evidence:** {refs or quotes}
**Evidence against / limits:** {disconfirming evidence, weak spots, or why confidence is bounded}
**Finding / surprise:** {what changed or was learned}
**Belief update:** {how the read shifted; omit if unchanged}
**Open threads:** {what remains unresolved; omit if none}
**Next crux:** {the next load-bearing question; omit if not yet clear}
```

The shape is a default, not a form to pad. Omit empty fields; add a field only when it carries information.

## Composition

`--log` composes with other figure-out modes. It records the active mode's findings and reasoning shifts; it does not change `--with-docs` glossary/ADR behavior or `--autonomous` self-answering behavior.
