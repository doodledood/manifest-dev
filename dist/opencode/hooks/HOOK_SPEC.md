# manifest-dev Hook Behavioral Specification

This document specifies the behavioral intent of each manifest-dev hook for manual porting to OpenCode's JS/TS plugin system.

Source hooks (Python): `claude-plugins/manifest-dev/hooks/`

## Shared Utilities: hook_utils.py

Core functions used by all hooks. Must be reimplemented in JS/TS.

### DoFlowState

Dataclass tracking /do workflow state:
- `has_do` — /do was invoked in the session
- `has_verify` — /verify was called after the last /do
- `has_done` — /done was called after the last /do
- `has_escalate` — /escalate was called after the last /do
- `do_args` — raw arguments from the /do invocation

### parse_do_flow(transcript_path)

Reads the transcript file (JSONL format, one JSON object per line). Tracks the most recent /do invocation and what happened after it. Each new /do resets the flow state.

Skill detection patterns:
1. **Model Skill tool call**: assistant message with `tool_use` block where `name === "Skill"` and `input.skill` matches
2. **User isMeta expansion**: user message with `isMeta: true` containing skill path
3. **User command-name tag**: user message with `<command-name>/skill-name</command-name>`

### count_consecutive_short_outputs(transcript_path)

Counts consecutive short assistant outputs from the end of the transcript. A "short output" has < 100 characters of text and no meaningful tool uses (Skill calls don't count as meaningful for loop detection). Used for infinite loop detection.

### has_recent_api_error(transcript_path)

Checks if the most recent assistant message was an API error (`isApiErrorMessage: true`). API errors are system failures, not voluntary stops.

### build_system_reminder(content)

Wraps content in `<system-reminder>` tags.

---

## Hook 1: stop_do_hook.py

**Event**: Stop (OpenCode: `session.complete`)
**Purpose**: Prevents premature stops during /do workflow

### Decision Matrix

| Condition | Decision | Reason |
|-----------|----------|--------|
| API error (last assistant msg) | ALLOW | System failure, not voluntary |
| No /do in session | ALLOW | Not in workflow |
| /do + /done called | ALLOW | Verified complete |
| /do + /escalate called | ALLOW | Properly escalated |
| /do + 3+ consecutive short outputs | ALLOW | Loop break (with warning) |
| /do only (or /do + /verify only) | BLOCK | Must verify first |

### Blocking Behavior

When blocking, provides system message:
> "Stop blocked: /do workflow requires formal exit. Options: (1) Run /verify to check criteria - if all pass, /verify calls /done. (2) Call /escalate - for blocking issues OR user-requested pauses. Short outputs will be blocked. Choose one."

### OpenCode Implementation Notes

Use `output.abort = "reason"` to block. The system message injection may require a separate mechanism (OpenCode doesn't have `systemMessage` in stop events).

---

## Hook 2: pretool_verify_hook.py

**Event**: PreToolUse with Skill matcher (OpenCode: `tool.execute.before`)
**Purpose**: Context reminder before /verify execution

### Behavior

1. Triggers only when the Skill tool is called with skill name "verify" (or "manifest-dev:verify")
2. Injects a system reminder prompting the model to read the manifest and execution log in full before spawning verifiers
3. Non-blocking — adds context only, never blocks the tool call

### Reminder Content

Includes the verify arguments if provided. Core message:
> "VERIFICATION CONTEXT CHECK: You are about to run /verify. BEFORE spawning verifiers, read the manifest and execution log in FULL if not recently loaded."

### OpenCode Implementation Notes

OpenCode tool name: "skill" (not "Skill"). Check `input.tool === "skill"` and `input.args.skill === "verify"`. Context injection may need `message.transform` or `experimental.chat.system.transform` event.

---

## Hook 3: post_compact_hook.py

**Event**: SessionStart with compact matcher (OpenCode: `session.created`)
**Purpose**: Restores /do context after session compaction

### Behavior

1. Only triggers after session compaction (not new sessions)
2. Parses transcript for active /do workflow (has_do but not has_done/has_escalate)
3. If active /do found, injects recovery reminder with the /do arguments

### Recovery Reminder Content

If /do args available:
> "This session was compacted during an active /do workflow. Context may have been lost. CRITICAL: Before continuing, read the manifest and execution log in FULL. The /do was invoked with: {args}"

If no args:
> "This session was compacted during an active /do workflow. CRITICAL: Before continuing, recover your workflow context: Check /tmp/ for execution logs..."

### OpenCode Implementation Notes

OpenCode's `session.created` fires for all new sessions, not just post-compaction. May need `experimental.session.compacting` event instead. Distinguish compaction from fresh session by checking transcript existence/content.
