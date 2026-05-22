---
name: prompt-engineering
description: 'Create, update, or review an LLM prompt — system prompt, skill, or agent. State the goal, trust the model, add only what closes a real gap in natural behavior. Use when writing, updating, reviewing, or diagnosing a prompt. Triggers: write a prompt, update a prompt, review a prompt, diagnose prompt failure, system prompt, skill, agent.'
argument-hint: '<request>'
user-invocable: true
---

A prompt earns its place where natural model behavior misses what's needed. State the goal and the expected outcome; trust the model for everything else. Lines belong only when they close a real gap — observed gotchas, non-obvious behavior, knowledge the model doesn't have, or edge cases it gets wrong by default. Length follows the gap, not a number. On update, calibrate both directions: add what closes the new gap, and prune what no longer earns its place. A prompt stays in balance over time; it doesn't accrete.

Branch on intent. *Creating*: discover the goal, audience, and the specific gap; draft the minimum that closes it. *Updating*: find each existing line's gap before changing anything around it — patches that replace often beat patches that add. *Reviewing*: of each line ask *"would the model do this without it?"* — flag the no's. *Diagnosing a failing prompt*: see `references/metaprompting.md` — find the line driving the symptom before patching.

References load on demand, not by default. `references/system-prompts.md` for prompts in deployment loops. `references/skills.md` for skill conventions and the minimum-viable shape. `references/knowledge-skills.md` when the gap is data the model lacks, not behavior. `references/agents.md` for isolation and tool declarations. `references/patterns.md` for techniques (verification, ambiguity handling, output contracts, decision rules). `references/review.md` for the anti-pattern catalog. `references/metaprompting.md` for diagnose-then-revise on failing prompts.
