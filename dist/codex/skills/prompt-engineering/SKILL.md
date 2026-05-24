---
name: prompt-engineering
description: 'Create, update, review, or discuss an LLM prompt — system prompt, skill, or agent. State the goal, trust the model, add only what closes a real gap in natural behavior. Use when writing, updating, reviewing, discussing, or diagnosing a prompt. Triggers: write a prompt, update a prompt, review a prompt, discuss a skill, think through a skill, improve a skill, this skill should, this prompt needs, diagnose prompt failure, system prompt, skill, agent.'
argument-hint: '<request>'
user-invocable: true
---

A prompt earns its place where natural model behavior misses what's needed. State the goal and the expected outcome; trust the model for everything else. Lines belong only when they close a real gap — observed gotchas, non-obvious behavior, knowledge the model doesn't have, or edge cases it gets wrong by default. Each line must also hold at the edges of where the prompt runs: name principles, not harness-bound primitives; scope rules to the principle's natural reach, not narrower; unify split restatements of the same rule. Length follows the gap, not a number. On update, calibrate both directions: add what closes the new gap, and prune what no longer earns its place. A prompt stays in balance over time; it doesn't accrete.

Branch on intent. *Creating*: discover the goal, audience, and the specific gap; draft the minimum that closes it. *Updating*: find each existing line's gap before changing anything around it — patches that replace often beat patches that add. *Reviewing*: of each line ask both *"would the model do this without it?"* and *"does this hold at the edges?"* — flag the no's. *Diagnosing a failing prompt*: see `references/metaprompting.md` — find the line driving the symptom before patching.

References load on demand. Load only the ones whose trigger fires:

- `references/system-prompts.md` — when writing a system prompt that ships in a deployment loop and warrants section structure (real degradation paths, real constraints, real stop conditions).
- `references/skills.md` — when writing a skill (anything in a `SKILL.md` + `references/` folder layout that activates a behavior).
- `references/knowledge-skills.md` — when writing a skill whose gap is data the model lacks rather than behavior it gets wrong (API references, schema lookups, internal conventions).
- `references/agents.md` — when writing an agent (anything that runs in isolation with its own declared tool set).
- `references/patterns.md` — when filling a non-trivial section in any prompt type and a known technique fits the gap (verification, narrate-execute-confirm, tool-call escalation, output contracts, ambiguity handling, high-risk self-check, decision rules over absolutes, emotional tone).
- `references/review.md` — when reviewing or updating an existing prompt.
- `references/metaprompting.md` — when diagnosing a failing prompt against logged traces.
