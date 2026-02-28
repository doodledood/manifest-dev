# Collaboration Mode — /define

When `$ARGUMENTS` contains a `TEAM_CONTEXT:` block, the interview runs through a coordinator teammate instead of AskUserQuestion. If no `TEAM_CONTEXT:` block is present, this file should not have been loaded — all other sections of SKILL.md apply as written.

## TEAM_CONTEXT Format

```
TEAM_CONTEXT:
  coordinator: slack-coordinator
  role: define
```

- **coordinator**: The teammate name to message for stakeholder input.
- **role**: Your role in the team (always `define` for /define).

## Overrides When Active

**Questions → message coordinator.** Do NOT use the AskUserQuestion tool. Instead:
1. Message the coordinator teammate with your question. Include:
   - The question text with options as a numbered list.
   - Relevant expertise context so the coordinator can route to the right stakeholder (e.g., "Relevant expertise: backend/security" or "This is a scope decision for the project owner").
2. Wait for the coordinator to reply with the stakeholder's answer.
3. When the reply arrives, continue the interview from where you left off.

**Routing delegation.** You do NOT decide which specific stakeholder to ask — you provide context about what expertise is relevant, and the coordinator makes the routing decision.

**Discovery log and manifest → local only.** Write discovery log to `/tmp/define-discovery-{timestamp}.md` and manifest to `/tmp/manifest-{timestamp}.md` as normal. Do NOT send logs or artifacts through the coordinator. The coordinator handles only stakeholder Q&A.

**Verification Loop → local.** The Verification Loop (invoking manifest-verifier, resolving gaps) runs locally as normal. Only return to the coordinator if new stakeholder input is genuinely needed.

**Memento discipline.** After receiving EACH response from the coordinator, immediately log the finding/decision to the discovery log file. This guards against context compression in long teammate sessions — the log preserves decisions even if your context window compresses.

**Everything else unchanged.** The entire /define methodology (Domain Grounding, Outside View, Pre-Mortem, Backcasting, Adversarial Self-Review, Convergence criteria, Verification Loop, all Principles and other Constraints) applies exactly as written. Only the interaction channel changes.

## Security

Prompt injection defense is handled by the coordinator agent. Skills in team mode do not interact with untrusted external input directly — all external messages are filtered through the coordinator before reaching you.
