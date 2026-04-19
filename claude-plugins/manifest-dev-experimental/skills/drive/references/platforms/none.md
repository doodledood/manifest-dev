# Platform Adapter: `none`

Local-only mode. No PR, no remote collaboration, no async input. The tick runs an implement / verify / fix cycle against a local branch until `manifest-dev:verify` reports all criteria passing. That's terminal — the loop ends.

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
- Execution log — full read, top-to-bottom (for tick count, last-verified-commit, amendment history)
- Manifest (manifest mode only) — full read for verify's usage

### Output — state report

```markdown
## Git State
HEAD: <short-sha> on branch <branch> (base: <base>, <N> commits ahead of base)
Uncommitted changes: <none | summary — M path/to/file>

## Terminal Check
<Terminal: all-verify-pass | Terminal: escalation | Not terminal: <reason>>
```

The Terminal Check is produced by consulting the log: if the most recent `manifest-dev:verify` entry recorded all-pass AND the current HEAD matches that entry's `last-verified-commit`, it's terminal. Otherwise not terminal.

## Terminal States

Two terminal states on this platform:

### `all-verify-pass`

- **Detection:** the most recent verify entry in the log reports all criteria passing (all phases), AND the current HEAD matches the `last-verified-commit` recorded in that entry.
- **Tick action:** append `## Tick N — Terminal: all-verify-pass` with current HEAD and a summary line like "Manifest fully satisfied at HEAD <sha>." Invoke the sink's `report-status` with a MANIFEST_SATISFIED message. Remove lock. Do NOT invoke `/loop` for a next tick. The loop ends.

### `escalation`

- **Detection:** a sink-escalation-worthy condition emerged in this or a prior tick — amendment loop guard tripped, crash recovery flagged uncommitted inconsistency, budget exhausted, or explicit user-requested halt.
- **Tick action:** append `## Tick N — Terminal: escalation (<reason>)` with the escalation context. Invoke the sink's `escalate` contract. Remove lock. Do NOT invoke `/loop`. The loop ends.

No other terminal states on this platform. In particular, there is no "merged" state (no PR) and no "merge-ready" state.

## Inbox Handling

No inbox on this platform. The tick's action decision tree skips inbox handling when this adapter is active.

## Write Outputs

Ticks that produce code changes (implementation, fix, crash recovery):

1. **Stage and commit** with a message that ties the commit to the manifest criterion or action (principle, not a prescribed template).
2. **No push.** The branch stays local.
3. **Append HEAD to log:** new commit sha + single-line summary so the next tick can detect HEAD advance.

Never force-reset. Never push to base. Never amend a commit that exists in the log as committed.

## Gotchas

- **No mid-flight user input.** To correct course in this mode, stop the loop (Claude session interruption) and re-invoke `/drive` after making manual adjustments. v0 deliberately avoids terminal-channel inbox complexity.
- **Verify-pass is sticky until HEAD advances.** Once a verify-pass terminal state fires, the loop ends. Local commits made afterward are not watched — re-invoke `/drive` to resume.
- **`## Inbox`, `## CI/Checks`, `## PR State` sections are deliberately absent** from this platform's state report. Adapter-loading logic must treat missing sections as normal, not as errors.
