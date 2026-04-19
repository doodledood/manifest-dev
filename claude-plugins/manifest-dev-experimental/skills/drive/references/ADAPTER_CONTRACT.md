# Adapter Contract — `/drive-tick`

All platform and sink adapters follow a single interface: **return a markdown-formatted state report with fixed section headings.** `/drive-tick` consumes the report directly — no structured-data marshalling, no tool-call wrappers, no parsed YAML.

This contract exists so `/drive-tick` stays lean and adapters stay pluggable. Copy an existing adapter, adjust its sections, add it to the platform/sink registry — done.

## Why markdown state reports?

- **Lean tick.** Tick reads a markdown file, follows the instructions inside. No new data shape to learn per adapter.
- **Composable.** Adapters can share section shapes (e.g., `## Git State` looks the same across `none`, `github`, future `gitlab`).
- **Diffable.** A state report is also what gets appended to the log — operator can read what the tick saw without special tooling.
- **No leaky abstractions.** Adapter owns how it gets the data; tick owns what to do with it.

## Platform adapter contract

**Purpose:** a platform adapter tells the tick how to bootstrap the run, read current state, detect terminal conditions, handle inbox events, and write outputs for a specific platform (none, github, gitlab, ...).

### Required sections

Every platform adapter must document these:

#### Bootstrap

How the `/drive` wrapper bootstraps the run for this platform. Covers:
- Base branch resolution (auto-detect vs. flag vs. required)
- Branch creation rules (on-base → new with meaningful slug; off-base → use current)
- Empty commit / push / PR creation — which of these apply, in what order
- What errors are surfaced and when

#### Read State

What the tick reads at the start of each iteration, and which state-report sections it produces. Minimum: `## Git State` and `## Terminal Check`. Platforms with remote state add `## Inbox`, `## CI/Checks`, `## PR State`.

#### Terminal States

The full enumeration of terminal conditions this platform recognizes. Each terminal state has:
- Name (e.g., `merged`, `all-verify-pass`)
- How the tick detects it
- What action the tick takes on detection (report, remove lock, end loop — no rescheduling)

#### Inbox Handling

How the adapter's inbox is consumed per tick. For platforms without an inbox (`none`), this section explicitly states "N/A — no inbox on this platform." For platforms with one (`github`), this specifies classification rules, filtering, reply mechanics.

#### Write Outputs

What commit / push / reply / description-update operations the tick performs after making changes, per platform.

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
**Optional (include when applicable)**: `## Inbox`, `## CI/Checks`, `## PR State`.

### Example state report — `none` platform

```markdown
## Git State
HEAD: 9f3a2c8 on branch claude/add-auth-a3f2 (base: main, 1 commit ahead)
Uncommitted changes: none

## Terminal Check
Not terminal: manifest has 3 unsatisfied ACs (AC-1.2, AC-3.4, AC-3.5)
```

### Example state report — `github` platform

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

## Sink adapter contract

**Purpose:** a sink adapter tells the tick where to send escalations and status updates. Not every tick calls the sink — only escalation paths and budget exhaust.

### Required sections

#### Escalate

How the tick escalates a blocker (manifest amendment loop, budget exhaust, unresolved conflict, etc.) through this sink. Specifies:
- Target (log file, Slack channel, email address, etc.)
- Formatting (markdown, plain text, JSON)
- What metadata is included (timestamp, run-id, reason, next-step recommendation)

#### Report Status

How the tick reports routine status (every tick, including lock-held skips) through this sink. Note that in v0 all sinks also must append a status entry to the execution log — the sink's `Report Status` is _additive_ escalation-class notification, not a replacement for the log.

### Required state-report section

When the adapter is asked to describe its target (e.g., for inclusion in the plugin README or log header), it returns:

```markdown
## Escalation Target
<human-readable description of where escalations go>
```

Example (`local` sink):

```markdown
## Escalation Target
Escalations are appended to the run log at /tmp/drive-log-{run-id}.md with a "## ESCALATION" marker block. No external notifications. User tails the log to observe.
```

## What the tick expects

`/drive-tick` loads the resolved adapter files at the start of each iteration. It does NOT re-derive adapter semantics from scratch — it reads the adapter's markdown and follows what it says.

Order of adapter loading in a tick:
1. Load `../drive/references/platforms/<platform>.md`
2. Load `../drive/references/sinks/<sink>.md`
3. Load any adapter-referenced data files (e.g., github adapter loads `./data/known-bots.md` and `./data/classification-examples.md`)

If an adapter file is missing, the tick errors: `Adapter not found: <path>. Check --platform / --sink values and plugin installation.`

## Adding a new adapter

1. Copy an existing adapter file as a starting point (e.g., `github.md` → `gitlab.md`).
2. Adjust the platform-specific sections: Bootstrap (API calls for branch/PR creation on the new platform), Read State (how to fetch PR state / comments / CI), Inbox Handling (platform-specific event shapes), Write Outputs (push, comment reply, description update API calls).
3. Keep the state-report section headings identical — this is what `/drive-tick` keys on.
4. Update `/drive`'s `--platform` validator and the plugin README's mode matrix.
5. Test via manual `/drive-tick` invocation before wiring into `/drive`.

No changes to `/drive-tick` SKILL.md should be required to add a platform or sink. If they are, the contract is leaking — fix the leak in the contract or in the tick's delegation logic.
