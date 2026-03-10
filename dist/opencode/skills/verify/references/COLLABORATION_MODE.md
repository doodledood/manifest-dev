# Collaboration Mode — /verify

When `$ARGUMENTS` contains a `TEAM_CONTEXT:` block, verification delegates to the team lead instead of spawning agents locally. If no `TEAM_CONTEXT:` block is present, this file should not have been loaded — all other sections of SKILL.md apply as written.

## Override When Active

**Do NOT spawn agents or run verification checks.** In team mode, the executor teammate cannot spawn other teammates (Claude Code limitation). Instead:

1. Extract all criteria (INV-G* and AC-*) from the manifest with their verification methods.
2. Return the full criteria list to the calling skill (/do) indicating delegation is needed.
3. /do will send the VERIFICATION_REQUEST to the lead via SendMessage. You do not send messages yourself.

**Why /do sends, not /verify**: /verify runs as a nested skill inside /do. SendMessage may not be reliably available in a skill-within-a-skill context. /do, running directly in the teammate context, has SendMessage access.

## VERIFICATION_REQUEST Format

The criteria list you return to /do should contain all information the lead needs to spawn verification teammates:

```
VERIFICATION_REQUEST:
  manifest_path: <path>
  log_path: <path>
  criteria:
    - id: INV-G1
      description: "..."
      method: bash | codebase | subagent
      command: "..." (if bash)
      agent: "..." (if subagent)
      prompt: "..." (if codebase/subagent)
    - id: AC-1.1
      description: "..."
      method: bash
      command: "..."
    ...
```

Include ALL criteria — INV-G* and AC-*. Skipping any criterion is a critical failure (same as solo mode).

## Everything Else Unchanged

All principles from SKILL.md apply: orchestrate don't verify, all criteria no exceptions, globals are critical. The only change is WHERE verification happens (lead-spawned teammates instead of locally-spawned agents).
