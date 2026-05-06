# Platform Adapter: `none`

Local-only mode. No PR, no remote collaboration, no async input. Each tick delegates manifest convergence to `/do` via drive-tick's Do Invocation stage; terminal when `/do` reports all criteria passing (via the `## Execution Complete` marker).

Use when you want `/drive`'s cron-driven convergence without the overhead of a PR.

## Bootstrap

Performed by `/drive` before any tick fires — see `drive/SKILL.md` §Branch + Bootstrap for the authoritative procedure (base resolution, branch creation, clean-tree check, empty commit).

The `none` platform's only deviation from the generic bootstrap: **no push, no PR.** Remote state is never modified by this platform.

## Read State

Produced every tick. Returns a markdown state report with the two required sections. Inbox, CI/Checks, and PR State sections are **omitted** — `none` platform has no remote state to read.

### Inputs

- Local git state: HEAD sha, current branch, uncommitted-changes summary.
- Execution log — already loaded by the tick's Memento Pattern; the adapter relies on the tick's read. Used here for tick count, prior `execution-complete-head: <sha>` markers recorded by drive-tick, and amendment history.

### Output — state report

```markdown
## Git State
HEAD: <short-sha> on branch <branch> (base: <base>, <N> commits ahead of base)
Uncommitted changes: <none | summary — M path/to/file>

## Terminal Check
<Terminal: all-verify-pass | Terminal: escalation | Not terminal: <reason>>
```

The Terminal Check is produced by consulting the log per the §Terminal States `all-verify-pass` detection rule. The `execution-complete-head: <sha>` marker is written by drive-tick after /do reports `## Execution Complete` — its presence implies /do verified all ACs+INV-Gs on that sha.

## Terminal States

Two terminal states on this platform:

### `all-verify-pass`

- **Detection:** the most recent `execution-complete-head: <sha>` line exists in the log AND its sha equals current HEAD (strict equality — advancing HEAD requires re-verification).
- **Tick action:** append `## Tick N — Terminal: all-verify-pass` with current HEAD and a summary line like "Manifest fully satisfied at HEAD <sha>." Invoke the sink's `report-status` with a MANIFEST_SATISFIED message. Remove lock. Do NOT invoke `/loop` for a next tick. The loop ends.

### `escalation`

- **Detection:** a sink-escalation-worthy condition emerged in this or a prior tick — /do emitted a `## Escalation:` marker, crash recovery flagged uncommitted inconsistency, budget exhausted, or explicit user-requested halt.
- **Tick action:** append `## Tick N — Terminal: escalation (<reason>)` with the escalation context. Invoke the sink's `escalate` contract. Remove lock. Do NOT invoke `/loop`. The loop ends.

## Inbox Handling

No inbox on this platform. The tick's action decision tree skips inbox handling when this adapter is active.

## Write Outputs

Ticks that produce code changes (from /do's Do Invocation or from crash recovery):

1. **Stage and commit** with a message that ties the commit to its driving criterion or action.
2. **No push.** The branch stays local.
3. **Append HEAD to log:** new commit sha + single-line summary so the next tick can detect HEAD advance.

Never amend a commit that exists in the log as committed (the log is the cross-tick memento; rewriting committed history breaks tick observability). Other write-discipline invariants inherited from `drive-tick/SKILL.md` §Security.

## Gotchas

- **No mid-flight user input.** To correct course in this mode, stop the loop (Claude session interruption) and re-invoke `/drive` after making manual adjustments.
- **Verify-pass is sticky until HEAD advances.** Once a verify-pass terminal state fires, the loop ends. Local commits made afterward are not watched — re-invoke `/drive` to resume.
- **`## Inbox`, `## CI/Checks`, `## PR State` sections are deliberately absent** from this platform's state report. Adapter-loading logic must treat missing sections as normal, not as errors.
