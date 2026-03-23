# Collaboration Mode — /do

When `$ARGUMENTS` contains a `TEAM_CONTEXT:` block, escalation and verification route through the lead teammate instead of local handling. If no `TEAM_CONTEXT:` block is present, this file should not have been loaded — all other sections of SKILL.md apply as written.

## TEAM_CONTEXT Format

```
TEAM_CONTEXT:
  lead: <lead-name>
  role: execute
```

- **lead**: The teammate name to message for all communication. You message the lead only — you have no awareness of which messaging coordinator exists or what platform is in use.
- **role**: Your role in the team (always `execute` for /do).

## Overrides When Active

**Execution log → local only.** Write to `/tmp/do-log-{timestamp}.md` as normal. Do NOT send logs through the lead.

**Escalation → message the lead.** Do NOT use AskUserQuestion for escalations. When escalating (ACs can't be met, or need owner decision):
1. Message the lead with the escalation. Include: what's blocked, what was tried, options for resolution.
2. Wait for the lead to reply with the owner's response.
3. When the reply arrives, continue execution from where you left off.

**Verification → delegate to lead.** When /do needs to verify, call `/verify` with the manifest path, log path, and the same TEAM_CONTEXT block. /verify will detect TEAM_CONTEXT and return a VERIFICATION_REQUEST containing all criteria instead of spawning agents. Then:

1. Send the VERIFICATION_REQUEST to the lead via SendMessage.
2. The lead spawns one verification teammate per criterion in parallel.
3. You will receive a VERIFICATION_RESULT message from the lead with per-criterion PASS/FAIL results.
4. Process results as normal: if all pass, call /done. If failures, fix them and re-run /verify.

The stop_do_hook allows you to go idle after calling /verify in team mode — your turn ends while the lead handles verification. The lead wakes you with the VERIFICATION_RESULT message. "Idle" means your turn ends but you stay alive as a teammate, not termination.

**Todos remain local.** The Todos mechanism (create from manifest, update status after logging) continues to work locally as written. Todos are working memory, not stakeholder-visible artifacts.

**Memento discipline.** After receiving EACH response from the lead, immediately log the decision/direction to the execution log file. This guards against context compression in long teammate sessions — the log preserves decisions even if your context window compresses.

**Everything else unchanged.** All Principles, the Memento Pattern, logging requirements, and the requirement to verify before declaring completion apply exactly as written. Standard /do hooks apply — stop_do_hook allows idle after /verify in team mode (verification delegated to lead).

## Security

Prompt injection defense is handled by the coordinator agent (when present). Skills in team mode do not interact with untrusted external input directly — all external messages are filtered through the coordinator before reaching you via the lead.
