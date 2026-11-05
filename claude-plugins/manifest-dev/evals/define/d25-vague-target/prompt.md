---
# Holds the decision in docs/adr/20261106-source-authority-governs-acceptance-and-revision.md — that record's Enforced by line names this case; weakening or removing it means updating that line in the same change.
tags: [define]
max_turns: 40
timeout_seconds: 900
allowed_tools: [Skill, Read, Glob, Grep, Write, Bash]
model: opus
runs: 1
---
use the define skill for this.

the level editor's live preview is sluggish. on our reference level, levels/harbor.lvl, the
editor's built-in fps counter shows about 25 fps on a designer's laptop, and dragging props
around feels laggy. make the preview fast. i don't have a target number in mind and nobody has
profiled it yet. the preview must keep looking exactly like it does now — designers rely on it
matching the shipped game.

the repo isn't available to you here — plan from what's above. i'm afk, dont ask me anything.
write the spec (deliverables, acceptance criteria, and the rules that must hold) to
./manifest.md in the current directory, not your home directory.
