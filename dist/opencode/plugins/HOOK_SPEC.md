# Hook Behavioral Specification — manifest-dev OpenCode Plugin

This document specifies the behavioral contract for the manifest-dev plugin (`plugins/index.ts`), ported from the Claude Code Python hooks.

## Source Hooks and Mapping

| Claude Code Hook | Python Source | OpenCode Mechanism | Fidelity |
|-----------------|--------------|-------------------|----------|
| Stop (stop_do_hook.py) | Blocks stopping during /do unless /done or /escalate called | `experimental.chat.system.transform` — persistent system guidance | **Degraded** — cannot actually block stopping |
| SessionStart+compact (post_compact_hook.py) | Injects recovery context after compaction | `experimental.session.compacting` — inject into output.context | **Full** |

## Known Limitations

### 1. No Stop Blocking (Critical)
Claude Code's Stop hook blocks the session from stopping during /do unless /done or /escalate is called. OpenCode's `session.idle` event is fire-and-forget — **you cannot prevent stopping**. The plugin approximates this by injecting persistent system-level enforcement guidance via `experimental.chat.system.transform`, but a determined or confused model can still stop.

**Impact**: The /do workflow contract (must call /done or /escalate before stopping) is advisory rather than enforced.

**Tracking**: OpenCode issue #12472 (feature request for blocking stop hooks).

### 2. No JSONL Transcript
Claude Code hooks parse the JSONL transcript file to detect workflow state. OpenCode stores sessions in SQLite — no file-based transcript. The plugin tracks workflow state in-memory per session. This means:
- State is lost if the plugin is reloaded mid-session
- State cannot be recovered from persistent storage after a restart

### 3. Persistent vs Event-Driven Reminders
Claude Code hooks fire on specific events. OpenCode's `experimental.chat.system.transform` fires before every LLM request. The reminders are always-on during active workflows rather than event-triggered. This means slightly more context overhead but equivalent behavioral guidance.

## Workflow State Tracking

The plugin maintains in-memory state per session:

### /do Flow State
- `active`: Set when /do skill is invoked
- `hasDone`: Set when /done is invoked — marks successful completion
- `hasEscalate`: Set when /escalate is invoked — marks escalation exit
- `doArgs`: Raw arguments from /do invocation
- `consecutiveShortOutputs`: Counter for loop detection — tracks consecutive short model outputs (not currently incrementable via OpenCode events, reserved for future use)

Each new /do invocation resets the state.

### Stop Enforcement Decision Matrix
The system transform follows the same decision matrix as the Claude Code stop hook:
1. `/done` called → no enforcement (verified complete)
2. `/escalate` called → no enforcement (properly escalated)
3. No exit condition → enforce: must call `/done` or `/escalate` before stopping

## Plugin Installation

The plugin is a single TypeScript file. Install as:

```bash
cp plugins/index.ts .opencode/plugins/manifest-dev.ts
```

OpenCode auto-loads top-level .ts files from `.opencode/plugins/`. No changes to user's existing `plugins/index.ts` or `opencode.json` required.
