---
tags: [define]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Bash]
model: opus
runs: 6
---
use the define skill for this.

we're adding saved searches to our internal support admin (django backend, react frontend).
agents run the same ticket searches all day — "open, priority high, tagged billing" — and
retype the filters every time. they want to save a search with a name, see their saved searches
in the sidebar, click one to run it, and delete ones they don't need. saved searches are private
to the agent who made them. we talked it through already, scope is settled — no sharing, no
editing a saved search (delete and re-save is fine), max 50 per agent.

plan it in three deliverables:
1. the SavedSearch model + migration
2. the REST endpoints (create / list / delete)
3. the react sidebar UI

the repo isn't available to you here — plan from what's above. i'm afk, dont ask me anything.
write the spec (deliverables, acceptance criteria, and the rules that must hold) to
./manifest.md in the current directory, not your home directory.
