# Platform Adapter: `none`

Local-only mode. No PR, no remote collaboration, no async input. Each tick delegates manifest convergence to `/do` via drive-tick's Do Invocation stage; terminal when `/do` reports all criteria passing (via the `## Execution Complete` marker).

Use when you want `/drive`'s cron-driven convergence without the overhead of a PR.

## Bootstrap

Performed by `/drive` before any tick fires — see `drive/SKILL.md` §Branch + Bootstrap for the authoritative procedure (base resolution, branch creation, clean-tree check, empty commit).

The `none` platform's only deviation from the generic bootstrap: **no push, no PR.** Remote state is never modified by this platform.

## Read State

Produced every tick. Returns a markdown state report with the two required sections. Inbox, CI/Checks, and PR State sections are **omitted** — `none` platform has no remote state to read.

### Inputs

- `git rev-parse HEAD` — current commit sha
- `git symbolic-ref --short HEAD` — current branch
- `git status --porcelain` — uncommitted changes summary
- Execution log — full read, top-to-bottom (for tick count, prior `execution-complete-head: <sha>` markers recorded by drive-tick, amendment history)
- Manifest (manifest mode only) — full read for verify's usage

### Output — state report

```markdown
## Git State
HEAD: <short-sha> on branch <branch> (base: <base>, <N> commits ahead of base)
Uncommitted changes: <none | summary — M path/to/file>

## Terminal Check
<Terminal: all-verify-pass | Terminal: escalation | Not terminal: <reason>>
```

The Terminal Check is produced by consulting the log: terminal when the most recent `execution-complete-head: <sha>` line (drive-tick writes this after /do reports `## Execution Complete` in its response — its presence in the log implies /do verified all ACs+INV-Gs on that sha) has a sha equal to current HEAD (strict equality — if HEAD has advanced past it, new work exists and must be re-verified by /do). Otherwise not terminal.

## Terminal States

Two terminal states on this platform:

### `all-verify-pass`

- **Detection:** the most recent `execution-complete-head: <sha>` line exists in the log AND its sha equals current HEAD (strict equality — advancing HEAD requires re-verification).
- **Tick action:** append `## Tick N — Terminal: all-verify-pass` with current HEAD and a summary line like "Manifest fully satisfied at HEAD <sha>." Invoke the sink's `report-status` with a MANIFEST_SATISFIED message. Remove lock. Do NOT invoke `/loop` for a next tick. The loop ends.

### `escalation`

- **Detection:** a sink-escalation-worthy condition emerged in this or a prior tick — /do emitted a `## Escalation:` marker, crash recovery flagged uncommitted inconsistency, budget exhausted, or explicit user-requested halt.
- **Tick action:** append `## Tick N — Terminal: escalation (<reason>)` with the escalation context. Invoke the sink's `escalate` contract. Remove lock. Do NOT invoke `/loop`. The loop ends.

No other terminal states on this platform. In particular, there is no "merged" state (no PR) and no "merge-ready" state.

## Inbox Handling

No inbox on this platform. The tick's action decision tree skips inbox handling when this adapter is active.

## Write Outputs

Ticks that produce code changes (from /do's Do Invocation or from crash recovery):

1. **Stage and commit** with a message that ties the commit to the manifest criterion or action (principle, not a prescribed template). /do typically owns commit semantics during its run; drive-tick's Write Outputs covers commits produced outside /do (crash recovery).
2. **No push.** The branch stays local.
3. **Append HEAD to log:** new commit sha + single-line summary so the next tick can detect HEAD advance.

Never force-reset. Never push to base. Never amend a commit that exists in the log as committed.

## Gotchas

- **No mid-flight user input.** To correct course in this mode, stop the loop (Claude session interruption) and re-invoke `/drive` after making manual adjustments. v0 deliberately avoids terminal-channel inbox complexity.
- **Verify-pass is sticky until HEAD advances.** Once a verify-pass terminal state fires, the loop ends. Local commits made afterward are not watched — re-invoke `/drive` to resume.
- **`## Inbox`, `## CI/Checks`, `## PR State` sections are deliberately absent** from this platform's state report. Adapter-loading logic must treat missing sections as normal, not as errors.
