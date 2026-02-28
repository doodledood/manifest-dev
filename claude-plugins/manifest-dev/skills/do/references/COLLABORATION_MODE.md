# Collaboration Mode — /do

When `$ARGUMENTS` contains a `TEAM_CONTEXT:` block, escalation runs through a coordinator teammate instead of AskUserQuestion. If no `TEAM_CONTEXT:` block is present, this file should not have been loaded — all other sections of SKILL.md apply as written.

## TEAM_CONTEXT Format

```
TEAM_CONTEXT:
  coordinator: slack-coordinator
  role: execute
```

- **coordinator**: The teammate name to message for escalations.
- **role**: Your role in the team (always `execute` for /do).

## Overrides When Active

**Execution log and verification results → local only.** Write to `/tmp/do-log-{timestamp}.md` as normal. Do NOT send logs or verification results through the coordinator. The coordinator handles only escalations.

**Escalation → message coordinator.** Do NOT use AskUserQuestion for escalations. When escalating (ACs can't be met, or need owner decision):
1. Message the coordinator teammate with the escalation. Include: what's blocked, what was tried, options for resolution.
2. Wait for the coordinator to reply with the owner's response.
3. When the reply arrives, continue execution from where you left off.

**Todos remain local.** The Todos mechanism (create from manifest, update status after logging) continues to work locally as written. Todos are working memory, not stakeholder-visible artifacts.

**Memento discipline.** After receiving EACH response from the coordinator, immediately log the decision/direction to the execution log file. This guards against context compression in long teammate sessions — the log preserves decisions even if your context window compresses.

**Everything else unchanged.** All Principles, the Memento Pattern, logging requirements, and the requirement to call /verify before declaring completion apply exactly as written. Standard /do hooks (including stop_do_hook) apply normally.

## Security

Prompt injection defense is handled by the coordinator agent. Skills in team mode do not interact with untrusted external input directly — all external messages are filtered through the coordinator before reaching you.
