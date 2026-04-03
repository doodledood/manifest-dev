# Hook Behavioral Specification — manifest-dev OpenCode Plugin

This document specifies the behavioral contract for the manifest-dev plugin (`plugins/index.ts`), ported from the Claude Code Python hooks.

## Source Hooks and Mapping

| Claude Code Hook | Python Source | OpenCode Mechanism | Fidelity |
|-----------------|--------------|-------------------|----------|
| Stop (stop_do_hook.py) | Blocks stopping during /do unless /done or /escalate called | `experimental.chat.system.transform` — persistent system guidance | **Degraded** — cannot actually block stopping |
| SessionStart+compact (post_compact_hook.py) | Injects recovery context after compaction | `experimental.session.compacting` — inject into output.context | **Full** |
| PreToolUse (pretool_verify_hook.py) | Reminds to read manifest before /verify | `tool.execute.before` — throws Error as context reminder | **Full** (main agent only; subagent bypass) |
| PostToolUse (posttool_log_hook.py) | Reminds to update execution log after milestones | `experimental.chat.system.transform` — persistent reminder | **Approximate** — always-on rather than per-event |
| UserPromptSubmit (prompt_submit_hook.py) | Amendment check during /do on user input | `experimental.chat.system.transform` — persistent reminder | **Approximate** — always-on rather than per-prompt |
| UserPromptSubmit (understand_prompt_hook.py) | Reinforces /understand principles | `experimental.chat.system.transform` — persistent reminder | **Approximate** — always-on rather than per-prompt |

## Known Limitations

### 1. No Stop Blocking (Critical)
Claude Code's Stop hook blocks the session from stopping during /do unless /done or /escalate is called. OpenCode's `session.idle` event is fire-and-forget — **you cannot prevent stopping**. The plugin approximates this by injecting persistent system-level enforcement guidance via `experimental.chat.system.transform`, but a determined or confused model can still stop.

**Impact**: The /do workflow contract (must call /verify -> /done or /escalate before stopping) is advisory rather than enforced.

**Tracking**: OpenCode issue #12472 (feature request for blocking stop hooks).

### 2. Subagent Hook Bypass (Critical)
`tool.execute.before` and `tool.execute.after` do NOT fire for tool calls within subagents (spawned via the `task` tool). This means:
- The pre-verify context refresh won't trigger if /verify is invoked by a subagent
- Post-milestone log reminders won't fire for subagent tool usage
- Any future guardrail hooks won't apply within agent-spawned workflows

**Impact**: Hooks only protect the main agent context.

**Tracking**: OpenCode issue #5894.

### 3. No JSONL Transcript
Claude Code hooks parse the JSONL transcript file to detect workflow state. OpenCode stores sessions in SQLite — no file-based transcript. The plugin tracks workflow state in-memory per session. This means:
- State is lost if the plugin is reloaded mid-session
- State cannot be recovered from persistent storage after a restart

### 4. Persistent vs Event-Driven Reminders
Claude Code hooks fire on specific events (UserPromptSubmit, PostToolUse). OpenCode's `experimental.chat.system.transform` fires before every LLM request. The reminders are always-on during active workflows rather than event-triggered. This means slightly more context overhead but equivalent behavioral guidance.

### 5. Pre-Verify Hook Uses Error Throwing
The pre-verify context refresh throws an Error to inject the reminder. In OpenCode, throwing in `tool.execute.before` blocks the tool call and the error message becomes the tool result. The agent must re-invoke /verify after seeing the reminder. This is more disruptive than Claude Code's additionalContext approach but achieves the same goal.

## Workflow State Tracking

The plugin maintains in-memory state per session:

### /do Flow State
- `active`: Set when /do skill is invoked
- `hasVerify`: Set when /verify is invoked during active /do
- `hasDone`: Set when /done is invoked — marks successful completion
- `hasEscalate`: Set when /escalate is invoked — marks escalation exit
- `hasSelfAmendment`: Set when /escalate with "self-amendment" args — must continue to /define --amend
- `doArgs`: Raw arguments from /do invocation

Each new /do invocation resets the state.

### /understand Flow State
- `active`: Set when /understand is invoked
- `isComplete`: Set when /understand-done is invoked, or a workflow skill (/define, /do, /auto) is invoked
- `understandArgs`: Raw arguments from /understand invocation

## Plugin Installation

The plugin is a single TypeScript file. Install as:

```bash
cp plugins/index.ts .opencode/plugins/manifest-dev.ts
```

OpenCode auto-loads top-level .ts files from `.opencode/plugins/`. No changes to user's existing `plugins/index.ts` or `opencode.json` required.
