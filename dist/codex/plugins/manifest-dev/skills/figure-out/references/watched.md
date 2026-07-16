# figure-out: watched mode

An external reasoning auditor — a different model in a fresh background session — reads the investigation log as it grows and interjects into the chat when it finds holes. It exists because the discipline is otherwise self-audited: the model that generates a confident wrong premise is the one asked to notice it. The watcher is the outside check, and it matters most under `--autonomous`, where no human backstop exists. This session's job in the pairing: start the watchers, keep the log flowing, honor the pre-read gate, and treat what comes back as evidence.

## Activation

Watched mode requires the log: keep the LOG.md discipline active even when `--no-log` is also passed — `--watched` wins. After resolving the log path, call the `start_figure_out_watchers` tool with it. If the tool isn't available, note that once and continue unwatched — no hard dependency. Whenever the session is in fact running unwatched — the tool was unavailable, or the user stopped the watchers — the rest of this file is inert and the master discipline applies unchanged, independent re-derivation included.

## Log beats are watcher activations

The watcher sees only what the log carries, when it carries it — the append-after-meaningful-turns discipline is what gives the audit mid-stream coverage. A session that advances heavily without appending will itself be flagged as a discipline breach.

## Watcher interjections

Interjections arrive decorated (`[watcher:<model>] …`). They are evidence, not user turns: address each flag on its merits — a flagged hole is an open crumb until worked through, and the register moves on evidence, not on the watcher's insistence, exactly as it does under user pushback. A premise dispute between you and the watcher that evidence can't settle becomes an open crumb bounding the read's confidence.

## Pre-read gate

Before naming the read, append a log entry whose heading contains `PRE-READ CHECKPOINT` — normal entry shape, carrying the current belief, confidence, and remaining fog. The watcher always answers a checkpoint with an explicit verdict interject.

- **Autonomous runs: the gate blocks.** End the turn after appending the checkpoint; the verdict interject wakes you. Resolve any holes it raises, then ship the read stamped with the audit outcome (e.g. "reasoning-audit clear: N flags raised and resolved en route").
- **Interactive runs: the gate doesn't block.** Name the read immediately and note the audit verdict will trail in; the user waits only if they choose to.

The gate verdict replaces the master discipline's independent re-derivation — including autonomous mode's always-run pass — for load-bearing reads: one external check, not two. The trade is accepted knowingly: the watcher saw the session where a fresh re-deriver wouldn't have, but it is context-rich, cross-model, and already paid for.
