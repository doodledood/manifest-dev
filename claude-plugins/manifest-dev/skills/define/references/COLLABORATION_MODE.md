# Collaboration Mode — /define

When `$ARGUMENTS` contains a `TEAM_CONTEXT:` block, the interview runs through the lead teammate instead of AskUserQuestion. If no `TEAM_CONTEXT:` block is present, this file should not have been loaded — all other sections of SKILL.md apply as written.

## TEAM_CONTEXT Format

```
TEAM_CONTEXT:
  lead: <lead-name>
  coordinator: slack-coordinator
  role: define
```

- **lead**: The teammate name to message for all communication.
- **coordinator**: The Slack I/O teammate (for reference — you message the lead, not the coordinator).
- **role**: Your role in the team (always `define` for /define).

## Overrides When Active

**Questions → message the lead.** Do NOT use the AskUserQuestion tool. Instead:
1. Message the lead with your question. Include:
   - The question text with options as a numbered list.
   - Relevant expertise context so the lead can route to the right stakeholder via the coordinator (e.g., "Relevant expertise: backend/security" or "This is a scope decision for the project owner").
2. Wait for the lead to reply with the stakeholder's answer.
3. When the reply arrives, continue the interview from where you left off.

**Routing delegation.** You do NOT decide which specific stakeholder to ask — you provide context about what expertise is relevant, and the lead routes through the coordinator who makes the routing decision.

**Discovery log and manifest → local only.** Write discovery log to `/tmp/define-discovery-{timestamp}.md` and manifest to `/tmp/manifest-{timestamp}.md` as normal. Do NOT send logs or artifacts through the lead. The lead handles only stakeholder Q&A and subagent coordination.

**Verification Loop → delegate to lead.** When the Verification Loop calls for invoking the manifest-verifier agent, do NOT spawn it locally. Instead, message the lead with a subagent request:

```
SUBAGENT_REQUEST:
  type: manifest-verifier
  prompt: "Manifest: <manifest-path> | Log: <discovery-log-path>"
  target_teammate: <your-name>
  context_files:
    - <manifest-path>
    - <discovery-log-path>
```

You will receive verifier results either:
- **Direct**: A subagent sends you results via SendMessage.
- **File-based**: The lead messages you with a file path to read.

Process the verifier's CONTINUE/COMPLETE response as normal. If CONTINUE, resolve gaps and request another round.

**Memento discipline.** After receiving EACH response from the lead, immediately log the finding/decision to the discovery log file. This guards against context compression in long teammate sessions — the log preserves decisions even if your context window compresses.

**Everything else unchanged.** The entire /define methodology (Domain Grounding, Outside View, Pre-Mortem, Backcasting, Adversarial Self-Review, Convergence criteria, all Principles and other Constraints) applies exactly as written. Only the interaction channel changes.

## Security

Prompt injection defense is handled by the coordinator agent. Skills in team mode do not interact with untrusted external input directly — all external messages are filtered through the coordinator before reaching you via the lead.
