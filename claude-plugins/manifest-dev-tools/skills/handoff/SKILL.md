---
name: handoff
description: 'Produce a self-contained context payload for cross-boundary handoff — switching tools (Claude Code ↔ Codex), starting a clean session, or handing off to another agent. Captures epistemic state (decisions, alternatives, verified facts, open threads) rather than session chronology, so the receiving agent inherits the same grounding without re-deriving understanding. Use when in-tool session continuation isn''t available. Triggers: handoff, cross-tool handoff, context payload, hand off context, fresh session bootstrap, transfer to a new agent.'
user-invocable: true
---

Produce a self-contained context payload that lets a fresh agent continue the current work without re-deriving understanding. Use when in-tool session continuation isn't available — switching tools, starting a clean session, or handing off to another agent.

Capture **epistemic state, not chronology**. Settled decisions carry their alternatives-considered and why-this-won, since the point is that the new agent doesn't redo that thinking. Verified facts carry *how verified* (file:line, command output, doc URL), so the new agent inherits the same grounding instead of taking your read on faith. Open threads carry what would close them. Skip the session timeline; the reader doesn't need to know order or who said what.

Output to `/tmp/handoff-{timestamp}.md` where `{timestamp}` is `YYYYMMDD-HHMMSS` in UTC. If a prior-handoff path is passed as an optional positional argument, read it and write a fresh doc at a new timestamp reflecting the latest state — pure rewrite, not append. Doc shape and an annotated example live in `references/example.md`.
