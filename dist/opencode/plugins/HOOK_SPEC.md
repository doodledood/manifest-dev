# Hook Behavioral Specification

This document describes the exact behavior implemented in `index.ts` and serves as the maintenance reference for the OpenCode hook adaptation from `claude-plugins/manifest-dev/hooks/`.

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
| `tool.execute.before` | `(input: {tool, sessionID, callID}, output: {args}) => void` | **Yes -- throw Error** | Error message becomes tool result seen by LLM. Does NOT fire in subagents (#5894). |
| `tool.execute.after` | `(input: {tool, sessionID, callID, args}, output: {title, output, metadata}) => void` | No (mutate output) | Mutate `output.output` to change what LLM sees as tool result. |
| `experimental.chat.system.transform` | `(input: {sessionID, model}, output: {system: string[]}) => void` | No | Push to `output.system[]` to inject system-level context before every LLM request. |
| `experimental.session.compacting` | `(input: {sessionID}, output: {context: string[], prompt?: string}) => void` | No -- inject context only | Push to `output.context[]` to preserve context across compaction. Optionally replace `output.prompt`. |
| `event` | `(input: {event}) => void` | No -- fire-and-forget | Catch-all for bus events (session.idle, todo.updated, etc.). |

### Blocking Mechanism

**To block a tool call**: `throw new Error("reason")` inside `tool.execute.before`. The error message becomes the tool result seen by the LLM.

**WRONG** (old/incorrect pattern): `args.abort = "reason"` -- this does NOT work.

### Context Injection

Three mechanisms available:

| Mechanism | When | How | Best For |
|-----------|------|-----|----------|
| `experimental.chat.system.transform` | Before every LLM request | `output.system.push("context")` | Persistent context injection (replaces Claude Code's `additionalContext`) |
| `experimental.session.compacting` | During compaction | `output.context.push("context")` | Preserving workflow state across compaction |
| `chat.message` | Before user message processed | Mutate `output.message` or `output.parts` | Modifying user input |

**IMPORTANT**: `tui.prompt.append` only fills the TUI input field -- it does NOT inject system messages. Use `experimental.chat.system.transform` for system context injection.

### Session Storage

Session data is stored in **SQLite** at `~/.local/share/opencode/opencode.db` (WAL mode, Drizzle ORM). **There is no JSONL transcript file.** Plugin access is via SDK client API only:

- `client.session.list()` -- list sessions
- `client.session.get(id)` -- get session metadata
- SSE event stream for real-time updates
- POST `/session/{id}/message` -- send message to session

Tables: SessionTable, MessageTable (role, time_created, data), PartTable (type, content).

This means Claude Code's transcript-parsing logic (`hook_utils.py`) cannot be reused directly. The OpenCode plugin must track workflow state in-memory or query the SQLite database via the client API.

### Subagent Hook Bypass

`tool.execute.before` and `tool.execute.after` do **NOT** fire for tool calls within subagents (issue #5894). This is a known gap -- skills invoked via the `task` tool run in isolation and their internal tool calls bypass all hooks.

**Impact**: If a subagent invokes the `verify`, `done`, or `escalate` skill internally, the workflow state tracker in `tool.execute.before` will not see those invocations. The `todo.updated` event (see below) provides a partial workaround for progress tracking.

### Hook Execution Model

`Plugin.trigger()` calls hooks sequentially across all loaded plugins. Each hook receives the **same mutable `output` object** -- mutations accumulate (middleware chain pattern).

---

## Hook 1: Pre-Tool Verify (pretool_verify_hook.py)

**OpenCode event**: `tool.execute.before` (for state tracking) + `experimental.chat.system.transform` (for context injection)

**Trigger condition**: The tool being called is `skill` (or `task`) AND the skill name is `verify` (or ends with `:verify`).

**Behavior**:
1. In `tool.execute.before`: detect skill invocations and update workflow state (track `do`, `done`, `escalate`, `verify`)
2. In `experimental.chat.system.transform`: when the `verify` skill was invoked during an active `do` workflow, push the context reminder into `output.system[]`

**NOT a blocker**: This hook injects context only. It does NOT throw an error to abort the tool call.

---

## Hook 2: Stop-Do Enforcement (stop_do_hook.py)

**OpenCode event**: `session.idle` (via the `event` catch-all handler)

**CRITICAL LIMITATION**: `session.idle` is **fire-and-forget** in OpenCode. Unlike Claude Code's Stop hook which can return `decision: "block"`, OpenCode provides **no mechanism to prevent the session from stopping**.

**Workaround** (fragile): `ctx.client.session.prompt(sessionID, { parts: [...] })` creates a NEW conversation turn after the session has already gone idle. This has race conditions in `run` mode (issue #15267). Feature request for blocking session.idle exists (issue #12472).

---

## Hook 3: Post-Compact Recovery (post_compact_hook.py)

**OpenCode event**: `experimental.session.compacting`

**Trigger condition**: Session context is being compacted.

**Behavior**: Push recovery reminder into `output.context[]` when an active `do` workflow is detected.

---

## Hook 4: Todo-Updated Tracking (new -- no Claude Code equivalent)

**OpenCode event**: `todo.updated` (via the `event` catch-all handler)

**Behavior**: Track workflow progress via todo state changes. Supplements `tool.execute.before` state tracking, especially for subagent actions (which bypass tool hooks).

---

## Gap Analysis

| Capability | Claude Code | OpenCode | Status |
|-----------|-------------|----------|--------|
| Block tool call | PreToolUse returns decision | **throw new Error()** in tool.execute.before | Supported (different mechanism) |
| Block stop | Stop hook returns `decision: block` | **No blocking session.idle** | GAP -- best-effort workaround only |
| Inject system context | `additionalContext` in hook output | `experimental.chat.system.transform` -- push to `output.system[]` | Supported (experimental) |
| Preserve across compaction | PreCompact `additionalContext` | `experimental.session.compacting` -- push to `output.context[]` | Supported (experimental) |
| Read transcript | `transcript_path` JSONL file | **No JSONL** -- SQLite DB, client API, or in-memory state | Replaced by in-memory tracking |
| Track todos | N/A (Claude Code uses TaskCreate) | `todo.updated` bus event | Supported (new capability) |
| Hook in subagents | Hooks fire for all tool calls | **tool.execute.before/after does NOT fire in subagents** (#5894) | GAP -- no workaround |
