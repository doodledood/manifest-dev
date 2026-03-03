# Hook Behavioral Specification

This document specifies the exact behavior that must be implemented in `index.ts` when porting from the Python hooks in `claude-plugins/manifest-dev/hooks/`.

## Hook 1: Pre-Tool Verify (pretool_verify_hook.py)

**OpenCode event**: `tool.execute.before`

**Trigger condition**: The tool being called is `skill` AND the skill name is `verify` (or ends with `:verify`).

**Behavior**:
1. Extract the skill arguments (file paths to manifest and log)
2. Inject a system-level reminder into the conversation context:

```
VERIFICATION CONTEXT CHECK: You are about to run /verify.

Arguments: {verify_args}

BEFORE spawning verifiers, read the manifest and execution log in FULL
if not recently loaded. You need ALL acceptance criteria (AC-*) and
global invariants (INV-G*) in context to spawn the correct verifiers.
```

If no arguments are present, use a minimal version without the Arguments line.

**NOT a blocker**: This hook injects context only. It does NOT abort the tool call.

**OpenCode implementation notes**:
- In `tool.execute.before`, you can mutate `args` or set `args.abort` to block
- For context injection without blocking, you may need to use `ctx.client` to send a system message, or prepend to the tool's input
- The exact injection mechanism depends on OpenCode plugin API capabilities

---

## Hook 2: Stop-Do Enforcement (stop_do_hook.py)

**OpenCode event**: `session.idle`

**Trigger condition**: Session is about to become idle (agent wants to stop responding).

**Behavior** (decision tree):

1. **No transcript available** -> Allow stop
2. **Recent API error detected** -> Allow stop (system failure, not voluntary)
3. **No /do invocation in transcript** -> Allow stop (not in workflow)
4. **Has /do AND has /done** -> Allow stop (verified complete)
5. **Has /do AND has /escalate** -> Allow stop (properly escalated)
6. **Has /do, 3+ consecutive short outputs** -> Allow with warning:
   ```
   WARNING: Stop allowed to break infinite loop. The /do workflow
   was NOT properly completed. Next time, call /escalate when blocked
   instead of minimal outputs.
   ```
7. **Has /do but no /done or /escalate** -> Block with message:
   ```
   Stop blocked: /do workflow requires formal exit.
   Options: (1) Run /verify to check criteria - if all pass, /verify calls /done.
   (2) Call /escalate - for blocking issues OR user-requested pauses.
   Short outputs will be blocked. Choose one.
   ```

**Transcript parsing requirements**:
- Detect skill invocations by searching for tool calls where `tool_name` is `Skill` (or `skill` in OpenCode) and `skill` argument matches `do`, `done`, `escalate`, `verify`
- A "short output" is an assistant message shorter than ~100 characters
- "Consecutive short outputs" means the last N assistant messages are all short

**OpenCode implementation notes**:
- `session.idle` is NOT a blocking event in OpenCode (unlike Claude Code's Stop hook)
- To enforce the block pattern, you may need to:
  - Use `tui.toast.show` to display a warning
  - Use `tui.prompt.append` to inject a follow-up prompt
  - Or use `chat.message` to inject a system message that continues the conversation
- This is the most complex hook to port and may require OpenCode plugin API extensions

---

## Hook 3: Post-Compact Recovery (post_compact_hook.py)

**OpenCode event**: `experimental.session.compacting`

**Trigger condition**: Session context is being compacted (compressed to save tokens).

**Behavior**:

1. **No transcript available** -> No action
2. **No /do invocation in transcript** -> No action
3. **Has /do AND has /done or /escalate** -> No action (workflow complete)
4. **Has /do, active workflow** -> Inject recovery reminder:

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
- `experimental.session.compacting` is experimental and may change
- Context injection can likely use the event's output mechanism
- This is the simplest hook to port

---

## Shared Utilities (hook_utils.py)

The Python hooks share utilities that need TypeScript equivalents:

### `parse_do_flow(transcript_path)`
Parses a session transcript and returns:
- `has_do: boolean` - Whether /do was invoked
- `has_done: boolean` - Whether /done was called after /do
- `has_escalate: boolean` - Whether /escalate was called after /do
- `has_verify: boolean` - Whether /verify was called after /do
- `do_args: string | null` - Arguments passed to /do

### `count_consecutive_short_outputs(transcript_path)`
Counts consecutive short assistant messages from the end of the transcript. A "short" message is under ~100 characters.

### `has_recent_api_error(transcript_path)`
Checks if the most recent messages include an API error (overloaded, rate limit, etc.).

### `build_system_reminder(content)`
Wraps content in a system reminder format. In OpenCode, this likely maps to a system message injection.

---

## Gap Analysis

| Capability | Claude Code | OpenCode | Status |
|-----------|-------------|----------|--------|
| Block stop | Stop hook returns `decision: block` | No blocking session.idle | GAP - needs workaround |
| Inject context | `additionalContext` in hook output | `chat.message` or `tui.prompt.append` | Needs testing |
| Read transcript | `transcript_path` in hook input | Session history via `ctx.client` | Needs API check |
| System reminder | Custom format wrapping | System message injection | Likely supported |
