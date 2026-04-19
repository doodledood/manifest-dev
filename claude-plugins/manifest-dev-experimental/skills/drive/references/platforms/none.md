# Platform Adapter: `none`

Local-only mode. No PR, no remote collaboration, no async input. The tick runs an implement / verify / fix cycle against a local branch until `manifest-dev:verify` reports all criteria passing. That's terminal — the loop ends.

Use when you want `/drive`'s cron-driven convergence without the overhead of a PR.

## Bootstrap

Performed by `/drive` (the wrapper) before any tick fires. The `none` platform's bootstrap is minimal.

1. **Base branch resolution** — see `/drive`'s base-resolution rules. If `--base <branch>` is provided, use it; else `git symbolic-ref refs/remotes/origin/HEAD`; else literal `main`; else error.
2. **Branch resolution:**
   - If current branch == base: create a new branch named `claude/<manifest-title-slug>-<4-char-hash>` and check it out.
   - If current branch != base: use current branch as-is. Do not modify.
3. **Uncommitted changes check:** refuse to bootstrap if the working tree has uncommitted changes ("Uncommitted changes on current branch. Commit, stash, or discard before starting /drive.").
4. **Empty commit:** `git commit --allow-empty -m "drive: bootstrap for <manifest-title>"`. Establishes a clean HEAD for tick 0 to reason about.
5. **No push, no PR.** Remote state is not modified by this platform.

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

The Terminal Check is produced by consulting the log: if the most recent `manifest-dev:verify` invocation returned all-pass and HEAD has not advanced since, it's terminal. Otherwise not terminal.

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

**N/A — no inbox on this platform.** There is no PR, no comment stream, no async channel. User mid-flight feedback is not supported in v0 for `none` mode. User stops the loop by talking to Claude at the session level (Claude can remove the lock and refuse to re-invoke `/loop`).

The tick's action decision tree skips inbox handling entirely when this adapter is active.

## Write Outputs

Ticks that produce code changes (implementation, fix, crash recovery) follow this procedure:

1. **Stage and commit** with a descriptive message (`drive: implement AC-3.4 (crash recovery semantics)`, `drive: fix failing verify on INV-G6`, etc.).
2. **No push.** The branch stays local.
3. **Append HEAD to log:** new commit sha + single-line summary so the next tick can detect HEAD advance.

Never force-reset. Never push to base. Never amend a commit that exists in the log as committed.

## Gotchas

- **No mid-flight user input.** If you're running in this mode and want to correct course, stop the loop (Claude session interruption) and re-invoke `/drive` after making manual adjustments. v0 deliberately avoids terminal-channel inbox complexity.
- **Loop runs forever in continuing-states** until verify passes or you stop it. Budget cap (`--max-ticks`, default 100) is the guard against runaway cost. If the manifest is unsatisfiable as written, the tick will keep trying — the cap catches this.
- **Verify-pass is sticky until HEAD advances.** Once a verify-pass terminal state fires, the loop ends. If you push new commits locally later that break things, `/drive` is no longer watching — re-invoke it.
- **`## Inbox`, `## CI/Checks`, `## PR State` sections are deliberately absent** from this platform's state report. The tick's adapter-loading logic must handle the absence gracefully (not treat missing sections as errors).
