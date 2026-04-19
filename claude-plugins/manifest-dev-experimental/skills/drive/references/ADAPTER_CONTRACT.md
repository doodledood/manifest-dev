# Adapter Contract — `/drive-tick`

All platform and sink adapters follow a single interface: **return a markdown-formatted state report with fixed section headings.** `/drive-tick` consumes the report directly — no structured-data marshalling, no tool-call wrappers, no parsed YAML.

## Division of labor

| Owner | Responsibilities |
|---|---|
| **Adapter (platform)** | How to fetch platform state (git, PR, CI, comments), what sections appear in the state report, the enumeration of platform-specific terminal states, inbox-handling rules, platform-specific write-outputs (commit/push/PR/comments). |
| **Adapter (sink)** | How to send escalation and status notifications, escalation code table, self-description block. |
| **`/drive-tick`** | Reading the execution log, reading the manifest, invoking adapter instructions, running the action decision tree, committing locally, calling `manifest-dev:verify`, amendment loop-guard counting, output-protocol log emission. |

**If the state report's `## Terminal Check` disagrees with what the tick would infer from git/PR state, the adapter is authoritative.** The tick does not override the adapter's terminal verdict.

**Adapters do NOT re-read the execution log.** The tick has already loaded it in the Memento step; adapters rely on that read.

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

What the tick reads at the start of each iteration, and which state-report sections it produces. The contract for section shape is below under "Required state-report sections."

#### Terminal States

The full enumeration of terminal conditions this platform recognizes. Each terminal state has:
- Name (e.g., `merged`, `all-verify-pass`)
- How the tick detects it
- What action the tick takes on detection (report, remove lock, end loop — no rescheduling)

#### Inbox Handling

How the adapter's inbox is consumed per tick. Platforms without an inbox state that fact and the tick skips inbox handling when the adapter is active. Platforms with an inbox specify classification rules, filtering, and reply mechanics.

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
**Optional (each independently included when applicable)**: `## Inbox`, `## CI/Checks`, `## PR State`. A platform may include any subset of these.

**Section order is not significant.** The tick keys on heading names, not position. Adapters may order sections for readability.

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

**Invariant:** the execution log is the authoritative cross-tick state and is ALWAYS written by the tick. Sink `Escalate` and `Report Status` are additive notification channels — never a replacement for the log. Sinks fail independently of logging; a broken sink must not lose the log entry.

### Required sections

#### Escalate

How the tick escalates a blocker (manifest amendment loop, budget exhaust, unresolved conflict, etc.) through this sink. Specifies:
- Target (log file, Slack channel, email address, etc.)
- Formatting (markdown, plain text, JSON)
- What metadata is included (timestamp, run-id, reason, next-step recommendation)

#### Report Status

How the tick reports routine status (every tick, including lock-held skips) through this sink. Note that in v0 all sinks also must append a status entry to the execution log — the sink's `Report Status` is _additive_ escalation-class notification, not a replacement for the log.

### Self-description section

Unlike the platform state report (produced every tick at runtime), the sink's `## Escalation Target` block is produced on-demand for documentation headers (README, log header) — not per-tick. When asked to describe its target, the adapter returns:

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

`/drive-tick` loads the resolved adapter files at the start of each iteration and follows the markdown. It does NOT re-derive adapter semantics from scratch. The tick owns the loading sequence; see `drive-tick/SKILL.md` §Load Adapters.

If an adapter file is missing, the tick errors: `Adapter not found: <path>. Check --platform / --sink values and plugin installation.`

## Adding a new adapter

1. Copy an existing adapter file as a starting point (e.g., `github.md` → `gitlab.md`).
2. Adjust the platform-specific sections: Bootstrap (API calls for branch/PR creation on the new platform), Read State (how to fetch PR state / comments / CI), Inbox Handling (platform-specific event shapes), Write Outputs (push, comment reply, description update API calls).
3. Keep the state-report section headings identical — this is what `/drive-tick` keys on.
4. Update `/drive`'s `--platform` validator and the plugin README's mode matrix.
5. Test via manual `/drive-tick` invocation before wiring into `/drive`.

No changes to `/drive-tick` SKILL.md should be required to add a platform or sink. If they are, the contract is leaking — fix the leak in the contract or in the tick's delegation logic.
