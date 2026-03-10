# Hook Behavioral Specification

This document specifies the exact behavior that must be implemented in `index.ts` when porting from the Python hooks in `claude-plugins/manifest-dev/hooks/`.

Corrected for OpenCode v1.2.15 (March 2026). See `.claude/skills/sync-tools/references/opencode-cli.md` for the full conversion reference.

## OpenCode Plugin Architecture

### Plugin Input Context

The plugin factory function receives `ctx` with:

| Field | Type | Description |
|-------|------|-------------|
| `ctx.client` | SDK client | HTTP client to localhost:4096 |
| `ctx.project` | `{ id, worktree, vcs }` | Project metadata |
| `ctx.directory` | string | Current working directory |
| `ctx.worktree` | string | Git worktree root |
| `ctx.serverUrl` | string | Server URL |
| `ctx.$` | BunShell | Bun shell API |

### Hooks Interface

The plugin returns an object implementing these hooks:

| Hook | Signature | Blocking | Description |
|------|-----------|----------|-------------|
| `tool.execute.before` | `(input: {tool, sessionID, callID}, output: {args}) => void` | **Yes — throw Error** | Error message becomes tool result seen by LLM. Does NOT fire in subagents (#5894). |
| `tool.execute.after` | `(input: {tool, sessionID, callID, args}, output: {title, output, metadata}) => void` | No (mutate output) | Mutate `output.output` to change what LLM sees as tool result. |
| `experimental.chat.system.transform` | `(input: {sessionID, model}, output: {system: string[]}) => void` | No | Push to `output.system[]` to inject system-level context before every LLM request. |
| `experimental.session.compacting` | `(input: {sessionID}, output: {context: string[], prompt?: string}) => void` | No — inject context only | Push to `output.context[]` to preserve context across compaction. Optionally replace `output.prompt`. |
| `event` | `(input: {event}) => void` | No — fire-and-forget | Catch-all for bus events (session.idle, todo.updated, etc.). |

### Blocking Mechanism

**To block a tool call**: `throw new Error("reason")` inside `tool.execute.before`. The error message becomes the tool result seen by the LLM.

**WRONG** (old/incorrect pattern): `args.abort = "reason"` — this does NOT work.

### Context Injection

Three mechanisms available:

| Mechanism | When | How | Best For |
|-----------|------|-----|----------|
| `experimental.chat.system.transform` | Before every LLM request | `output.system.push("context")` | Persistent context injection (replaces Claude Code's `additionalContext`) |
| `experimental.session.compacting` | During compaction | `output.context.push("context")` | Preserving workflow state across compaction |
| `chat.message` | Before user message processed | Mutate `output.message` or `output.parts` | Modifying user input |

**IMPORTANT**: `tui.prompt.append` only fills the TUI input field — it does NOT inject system messages. Use `experimental.chat.system.transform` for system context injection.

### Session Storage

Session data is stored in **SQLite** at `~/.local/share/opencode/opencode.db` (WAL mode, Drizzle ORM). **There is no JSONL transcript file.** Plugin access is via SDK client API only:

- `client.session.list()` — list sessions
- `client.session.get(id)` — get session metadata
- SSE event stream for real-time updates
- POST `/session/{id}/message` — send message to session

Tables: SessionTable, MessageTable (role, time_created, data), PartTable (type, content).

This means Claude Code's transcript-parsing logic (`hook_utils.py`) cannot be reused directly. The OpenCode plugin must track workflow state in-memory or query the SQLite database via the client API.

### Subagent Hook Bypass

`tool.execute.before` and `tool.execute.after` do **NOT** fire for tool calls within subagents (issue #5894). This is a known gap — skills invoked via the `task` tool run in isolation and their internal tool calls bypass all hooks.

**Impact**: If a subagent invokes /verify, /done, or /escalate internally, the workflow state tracker in `tool.execute.before` will not see those invocations. The `todo.updated` event (see below) provides a partial workaround for progress tracking.

### Hook Execution Model

`Plugin.trigger()` calls hooks sequentially across all loaded plugins. Each hook receives the **same mutable `output` object** — mutations accumulate (middleware chain pattern).

---

## Hook 1: Pre-Tool Verify (pretool_verify_hook.py)

**OpenCode event**: `tool.execute.before` (for state tracking) + `experimental.chat.system.transform` (for context injection)

**Trigger condition**: The tool being called is `skill` (or `task`) AND the skill name is `verify` (or ends with `:verify`).

**Behavior**:
1. In `tool.execute.before`: detect skill invocations and update workflow state (track /do, /done, /escalate, /verify)
2. In `experimental.chat.system.transform`: when /verify was invoked during an active /do workflow, push the context reminder into `output.system[]`:

```
VERIFICATION CONTEXT CHECK: You are about to run /verify.

Arguments: {verify_args}

BEFORE spawning verifiers, read the manifest and execution log in FULL
if not recently loaded. You need ALL acceptance criteria (AC-*) and
global invariants (INV-G*) in context to spawn the correct verifiers.
```

If no arguments are present, use a minimal version without the Arguments line.

**NOT a blocker**: This hook injects context only. It does NOT throw an error to abort the tool call.

**OpenCode implementation notes**:
- Context injection uses `experimental.chat.system.transform` to push to `output.system[]`
- This replaces Claude Code's `additionalContext` output pattern
- The `tool.execute.before` handler tracks state but does not modify args or throw

---

## Hook 2: Stop-Do Enforcement (stop_do_hook.py)

**OpenCode event**: `session.idle` (via the `event` catch-all handler)

**Trigger condition**: Session becomes idle (agent stopped responding).

**CRITICAL LIMITATION**: `session.idle` is **fire-and-forget** in OpenCode. Unlike Claude Code's Stop hook which can return `decision: "block"`, OpenCode provides **no mechanism to prevent the session from stopping**.

**Workaround** (fragile): `ctx.client.session.prompt(sessionID, { parts: [...] })` creates a NEW conversation turn after the session has already gone idle. This has race conditions in `run` mode (issue #15267) where the process may have already exited. Feature request for blocking session.idle exists (issue #12472).

**Behavior** (decision tree — same logic as Claude Code, but enforcement is best-effort):

1. **No /do in workflow state** -> No action (not in workflow)
2. **Has /do AND has /done** -> No action (verified complete)
3. **Has /do AND has /escalate** -> No action (properly escalated)
4. **Has /do AND has TEAM_CONTEXT AND has /verify** -> Allow (team mode: verification delegated to lead). System message: "Verification delegated to the team lead. The lead will spawn verification teammates and relay results. You will receive a message with VERIFICATION_RESULT when complete."
5. **Has /do, 3+ consecutive short outputs** -> Log warning:
   ```
   WARNING: Stop allowed to break infinite loop. The /do workflow
   was NOT properly completed. Next time, call /escalate when blocked
   instead of minimal outputs.
   ```
6. **Has /do but no /done or /escalate** -> Best-effort: attempt to inject follow-up prompt (fragile):
   ```
   Stop blocked: /do workflow requires formal exit.
   Options: (1) Run /verify to check criteria - if all pass, /verify calls /done.
   (2) Call /escalate - for blocking issues OR user-requested pauses.
   Short outputs will be blocked. Choose one.
   ```

**Loop detection**: Track consecutive short outputs (< 100 chars) in `tool.execute.after`. Reset counter on substantial output. If 3+ consecutive short outputs when session goes idle, allow stop with warning (same as Claude Code's loop-break logic).

**Transcript parsing replacement**: Claude Code reads JSONL transcript files via `hook_utils.py`. OpenCode has no JSONL transcript — session data is in SQLite. The plugin tracks workflow state in-memory via `tool.execute.before` instead of parsing transcripts.

**OpenCode implementation notes**:
- This is the most significant behavioral gap between Claude Code and OpenCode
- The `experimental.chat.system.transform` hook provides a partial mitigation: inject a persistent system message reminding the LLM not to stop during active /do workflows
- The `todo.updated` event can supplement state tracking for subagent actions

---

## Hook 3: Post-Compact Recovery (post_compact_hook.py)

**OpenCode event**: `experimental.session.compacting`

**Trigger condition**: Session context is being compacted (compressed to save tokens).

**Behavior**:

1. **No /do in workflow state** -> No action
2. **Has /do AND has /done or /escalate** -> No action (workflow complete)
3. **Has /do, active workflow** -> Push recovery reminder into `output.context[]`:

If /do arguments are available:
```
This session was compacted during an active /do workflow.
Context may have been lost.

CRITICAL: Before continuing, read the manifest and execution log in FULL.

The /do was invoked with: {do_args}

1. Read the manifest file - contains deliverables, acceptance criteria, and approach
2. Check /tmp/ for your execution log (do-log-*.md) and read it to recover progress

Do not restart completed work. Resume from where you left off.
```

If /do arguments are not available, use fallback:
```
This session was compacted during an active /do workflow.
Context may have been lost.

CRITICAL: Before continuing, recover your workflow context:

1. Check /tmp/ for execution logs matching do-log-*.md
2. The log references the manifest file path - read both in FULL

Do not restart completed work. Resume from where you left off.
```

**OpenCode implementation notes**:
- Push to `output.context[]` to inject context preserved across compaction
- Optionally replace `output.prompt` to customize the compaction prompt itself
- This event is experimental (`experimental.` prefix) and may change between releases
- This is the simplest hook to port

---

## Hook 4: Todo-Updated Tracking (new — no Claude Code equivalent)

**OpenCode event**: `todo.updated` (via the `event` catch-all handler)

**Trigger condition**: Any todo item is created, updated, or deleted.

**Behavior**:
- Receive the full todo array: `event.properties.todos = [{id, content, status, priority}]`
- Track workflow progress — e.g., when acceptance criteria todos (AC-*) are marked complete
- Supplements `tool.execute.before` state tracking, especially for subagent actions (which bypass tool hooks)

**OpenCode implementation notes**:
- This is fire-and-forget (bus event, not a hook)
- Useful for monitoring /do workflow progress without relying on transcript parsing
- Can trigger suggestions (e.g., "all AC-* items complete, consider running /verify")

---

## Shared Utilities (hook_utils.py → in-memory state)

The Python hooks share transcript-parsing utilities. In OpenCode, these are replaced by **in-memory state tracking** because there is no JSONL transcript file.

### `DoFlowState` (in-memory)
Tracked via `tool.execute.before` handler:
- `hasDo: boolean` — Whether /do was invoked
- `hasDone: boolean` — Whether /done was called after last /do
- `hasEscalate: boolean` — Whether /escalate was called after last /do
- `hasVerify: boolean` — Whether /verify was called after last /do
- `doArgs: string | null` — Arguments passed to /do
- `hasTeamContext: boolean` — Whether /do args contain a TEAM_CONTEXT block

### `consecutiveShortOutputs` (in-memory counter)
Tracked via `tool.execute.after` handler. Counts consecutive tool outputs under 100 characters. Reset on any substantial output.

### Context injection
Uses `experimental.chat.system.transform` to push into `output.system[]` — replaces Claude Code's `build_system_reminder()` + `additionalContext` pattern.

---

## Gap Analysis

| Capability | Claude Code | OpenCode | Status |
|-----------|-------------|----------|--------|
| Block tool call | PreToolUse returns decision | **throw new Error()** in tool.execute.before | Supported (different mechanism) |
| Block stop | Stop hook returns `decision: block` | **No blocking session.idle** | GAP — best-effort workaround only |
| Inject system context | `additionalContext` in hook output | `experimental.chat.system.transform` — push to `output.system[]` | Supported (experimental) |
| Preserve across compaction | PreCompact `additionalContext` | `experimental.session.compacting` — push to `output.context[]` | Supported (experimental) |
| Read transcript | `transcript_path` JSONL file | **No JSONL** — SQLite DB, client API, or in-memory state | Replaced by in-memory tracking |
| Track todos | N/A (Claude Code uses TaskCreate) | `todo.updated` bus event | Supported (new capability) |
| Hook in subagents | Hooks fire for all tool calls | **tool.execute.before/after does NOT fire in subagents** (#5894) | GAP — no workaround |
