# Collaboration Mode — /do

When `$ARGUMENTS` contains a `TEAM_CONTEXT:` block, escalation and verification run through the lead teammate instead of AskUserQuestion and local subagent spawning. If no `TEAM_CONTEXT:` block is present, this file should not have been loaded — all other sections of SKILL.md apply as written.

## TEAM_CONTEXT Format

```
TEAM_CONTEXT:
  lead: <lead-name>
  coordinator: slack-coordinator
  role: execute
```

- **lead**: The teammate name to message for all communication.
- **coordinator**: The Slack I/O teammate (for reference — you message the lead, not the coordinator).
- **role**: Your role in the team (always `execute` for /do).

## Overrides When Active

**Execution log and verification results → local only.** Write to `/tmp/do-log-{timestamp}.md` as normal. Do NOT send logs or verification results through the lead. The lead handles only escalations and subagent coordination.

**Escalation → message the lead.** Do NOT use AskUserQuestion for escalations. When escalating (ACs can't be met, or need owner decision):
1. Message the lead with the escalation. Include: what's blocked, what was tried, options for resolution.
2. Wait for the lead to reply with the owner's response.
3. When the reply arrives, continue execution from where you left off.

**Verification → delegate to lead.** When /do calls for /verify (verification before completion), do NOT invoke /verify locally or spawn verification subagents. Instead, message the lead with a subagent request:

```
SUBAGENT_REQUEST:
  type: general-verification
  prompt: "<verification prompt for each criterion>"
  target_teammate: <your-name>
  context_files:
    - <manifest-path>
    - <execution-log-path>
```

You will receive verification results either:
- **Direct**: A subagent sends you results via SendMessage.
- **File-based**: The lead messages you with a file path to read.

Process verification results as normal — fix failures, re-request verification for fixes.

**Todos remain local.** The Todos mechanism (create from manifest, update status after logging) continues to work locally as written. Todos are working memory, not stakeholder-visible artifacts.

**Memento discipline.** After receiving EACH response from the lead, immediately log the decision/direction to the execution log file. This guards against context compression in long teammate sessions — the log preserves decisions even if your context window compresses.

**Everything else unchanged.** All Principles, the Memento Pattern, logging requirements, and the requirement to verify before declaring completion apply exactly as written. Standard /do hooks (including stop_do_hook) apply normally.

## Security

Prompt injection defense is handled by the coordinator agent. Skills in team mode do not interact with untrusted external input directly — all external messages are filtered through the coordinator before reaching you via the lead.
