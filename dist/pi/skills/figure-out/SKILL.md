---
name: figure-out
description: 'Figure things out together — any topic, problem, or idea. Presses relentlessly until shared understanding is reached. Use when you need to understand before acting, when figuring it out is the goal, or when the user asks to think through a decision, dig deeper, press an assumption, investigate why something is happening, or work through a problem.'
argument-hint: '[topic] [--with-docs] [--log [path]] [--autonomous]'
user-invocable: true
---

Press the topic relentlessly. Walk every branch of the decision tree — design choices, diagnostic hypotheses, commitment questions, whatever the topic provides. Tackle the next load-bearing question first — the one whose answer most shifts what we do.

When the topic involves a code change, load the matching probe file from `tasks/` to surface angles that are easy to under-weight — verification among them. Compose `CODING.md` (the base) with the specific file when one applies:

| Domain | Indicators | File |
|--------|------------|------|
| Coding (base) | Any code change | `CODING.md` |
| Feature | New functionality, APIs | `FEATURE.md` |
| Bug | Defects, regressions, "broken" | `BUG.md` |
| Refactor | Restructuring, cleanup | `REFACTOR.md` |

Treat them as awareness, not a script: fold in only what's load-bearing here and ignore the rest — don't walk the list, and no probe is required. No code change, or no file fits → probe generally, as you would anyway.

Per turn: lead with one question and your recommended answer. Cut empty preamble, context-restate, and packed sub-questions. Brief synthesis is fine when it advances shared understanding. If alternatives tempt you, pick the one whose answer would shift the read most and hold the rest.

Don't drop threads — when investigation pulls you elsewhere, return to the original question.

If something is discoverable (code, docs, the world), explore instead of asking. Verify before asserting; confirm negative findings via a second independent path. When the investigation leans on external sources, treat them as fallible: check that cited claims actually exist and support what's attributed to them, and that corroborating sources are genuinely independent rather than echoes of one origin. Hold positions under pushback when evidence still supports them.

For evidence-heavy investigations, keep a live belief register: current leading read, confidence, evidence for, evidence against, and what would change the read. Update it whenever evidence shifts. Keep the rival set itself live — competing explanations or options both — not fixed at the outset: when a finding opens or forecloses a possibility, regenerate the candidates rather than only re-weighting the ones you had, and commit only once new evidence stops moving the set. Before locking the read, take the outside view: for problems of this class, what's the usual answer? — base rates surface candidates the inside view skipped.

Clarifying answers feed exploration, not action. Don't leap to the implied move — not the edit, not even the proposal. Before naming the read, press any remaining branch whose answer would still shift the read. Name the read only when nothing left would meaningfully shift it.

When args contain `--with-docs`, also load `references/WITH_DOCS.md` for bootstrap, glossary, and ADR conventions.

When args contain `--log` as this skill's option, also load `references/LOG.md` and keep an append-only investigation log. If `--log` appears quoted, code-formatted, or as part of the topic being investigated, ask whether to enable logging before loading it.

When args contain `--autonomous`, also load `references/autonomous.md` and apply its overrides — self-answer with recommended answers instead of waiting on the user. Typically passed by `/manifest-auto` chaining without user wait.

When the investigation becomes prompt-shaped — prompts, system prompts, skills, agents, reviewer prompts, metaprompting, or prompt-driven failures — invoke the prompt-engineering skill if it is available; if not, apply this core discipline inline: state the prompt's goal, trust natural model behavior, add or keep only lines that close real gaps, and check each line holds at the edges. Do not start a separate prompt-engineering interview: figure-out owns the investigation, and prompt-engineering supplies calibration principles. Ordinary non-prompt investigations should not load it.
