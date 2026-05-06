# Adapter Contract — `/drive-tick`

All platform and sink adapters follow a single interface: **return a markdown-formatted state report with fixed section headings.** `/drive-tick` consumes the report directly — no structured-data marshalling, no tool-call wrappers, no parsed YAML.

## Division of labor

| Owner | Responsibilities |
|---|---|
| **Adapter (platform)** | How to fetch platform-specific state, what sections appear in the state report, the enumeration of platform terminal states, inbox-handling rules, write-outputs, thread-hygiene rules when applicable. |
| **Adapter (sink)** | How to send escalation and status notifications, escalation code table, self-description block. |
| **`/drive-tick`** | Reading the execution log, reading the manifest, invoking adapter instructions, running the action decision tree, committing locally, calling `manifest-dev:verify`, amendment loop-guard counting, output-protocol log emission. |

**If the state report's `## Terminal Check` disagrees with what the tick would infer from git/PR state, the adapter is authoritative.** The tick does not override the adapter's terminal verdict.

**Adapters do NOT re-read the execution log.** The tick has already loaded it in the Memento step; adapters rely on that read.

## Platform adapter contract

**Purpose:** a platform adapter tells the tick how to bootstrap the run, read current state, detect terminal conditions, handle inbox events, and write outputs for a specific platform (none, github, gitlab, ...).

### Required sections

Every platform adapter must document these obligations. Implementation choices (branching policy, API shape, push semantics) are the adapter's own — the contract names *what* must be documented, not *how* the adapter implements it.

- **Bootstrap** — how `/drive` initializes the run for this platform, including any platform-specific bootstrap operations and the errors surfaced.
- **Read State** — what the tick reads each iteration and which state-report sections this adapter produces (see "Required state-report sections" below for shape).
- **Terminal States** — the full enumeration of terminal conditions this platform recognizes; for each: name, detection rule, sink-notification code. The tick handles the loop-end sequence (see `drive-tick/SKILL.md` §Output Protocol).
- **Inbox Handling** — how the adapter consumes inbox events per tick, including classification, filtering, and reply mechanics. Platforms without an inbox state that fact; the tick skips inbox handling.
- **Write Outputs** — what commit/push/reply/description operations the tick performs after code changes. Gated on code changes — skipped on ticks with no commits.
- **Thread Hygiene** — when the platform has resolvable review threads, how unaddressed threads are resolved after action. Runs every tick, invoked by drive-tick §P strictly after Write Outputs completes, independent of code changes. Platforms without thread-state semantics omit this section.

### Required state-report sections

When the adapter returns a state report to the tick, it must include:

```markdown
## Git State
<current HEAD SHA, branch, base branch, uncommitted changes summary>

## Terminal Check
<either "Not terminal" with reason, or "Terminal: <state-name>" with action>
```

And when applicable:

```markdown
## Inbox
<new events since last tick — comments, mentions, messages; omit if empty or N/A>

## CI/Checks
<current CI status summary; omit if no CI or N/A>

## PR State
<PR number, mergeable status, requested reviewers, approvals, etc.; omit if no PR>
```

**Required on every platform**: `## Git State`, `## Terminal Check`.
**Optional (each independently included when applicable)**: `## Inbox`, `## CI/Checks`, `## PR State`. A platform may include any subset of these.

**Section order is not significant.** The tick keys on heading names, not position. Adapters may order sections for readability.

### Example state report (composite — Required + all Optional sections)

```markdown
## Git State
HEAD: 4e1d7b0 on branch claude/add-auth-a3f2 (base: main, 8 commits ahead)
Uncommitted changes: none

## PR State
PR #42 open (mergeable: yes, 1 approval, 0 changes-requested, no unresolved threads)

## CI/Checks
2 checks passing, 1 pending (typecheck). Base branch clean.

## Inbox
New since last tick:
- Comment #871 (human, reviewer) on line 42: "can you extract the helper?"
- Comment #872 (bot, coderabbit) on line 58: "suggest naming X"

## Terminal Check
Not terminal: 1 actionable human thread, 1 bot suggestion pending classification
```

A minimal `none`-platform report would include only `## Git State` and `## Terminal Check`.

## Sink adapter contract

**Purpose:** a sink adapter tells the tick where to send escalations and status updates. Not every tick calls the sink — only escalation paths and budget exhaust.

**Invariant:** the execution log is the authoritative cross-tick state and is ALWAYS written by the tick. Sink `Escalate` and `Report Status` are additive notification channels — never a replacement for the log. Sinks fail independently of logging; a broken sink must not lose the log entry.

### Required sections

- **Escalate** — where escalations go and what shape they take: destination, format, and required metadata (timestamp, run-id, reason, next-step recommendation).
- **Report Status** — how the tick reports terminal status that names a status code (e.g., merged, closed, manifest-satisfied) — additive to the execution log per the **Invariant** above. Continuing and Skipped-lock-held ticks do not invoke the sink; the log's tick entry is the cross-tick record.

### Self-description section

Unlike the platform state report (produced every tick at runtime), the sink's `## Escalation Target` block is produced on-demand for documentation headers (README, log header) — not per-tick. When asked to describe its target, the adapter returns:

```markdown
## Escalation Target
<human-readable description of where escalations go>
```

Example (`local` sink):

```markdown
## Escalation Target
Escalations are appended to the run log at /tmp/drive-log-{run-id}.md as a `## ESCALATION — <CODE>` marker block. No external notifications. User tails the log to observe.
```

## What the tick expects

`/drive-tick` loads the resolved adapter files at the start of each iteration and follows the markdown. It does NOT re-derive adapter semantics from scratch. The tick owns the loading sequence; see `drive-tick/SKILL.md` §Load Adapters.

If an adapter file is missing, the tick errors actionably — naming the missing path and the resolution path (`--platform` / `--sink` values, plugin installation). The literal error message is owned by `drive-tick/SKILL.md` §Load Adapters.

## Adding a new adapter

Add an adapter by creating a file under `references/platforms/` or `references/sinks/` that satisfies the obligations above (Required sections + Required state-report sections for platforms; Required sections + Self-description for sinks). Wire `/drive`'s `--platform` / `--sink` validator and the plugin README's mode matrix to recognize the new value.

State-report section headings must remain identical across platforms — that's what the tick keys on.

**No changes to `/drive-tick` SKILL.md should be required to add a platform or sink. If they are, the contract is leaking — fix the leak in the contract or in the tick's delegation logic.**
