---
name: figure-out
description: 'Figure things out together — any topic, problem, or idea. Presses relentlessly until shared understanding is reached. Use when you need to understand before acting, when figuring it out is the goal, or when the user asks to think through a decision, dig deeper, press an assumption, investigate why something is happening, or work through a problem.'
argument-hint: '[topic] [--with-docs]'
user-invocable: true
---

Press the topic relentlessly. Walk every branch of the decision tree — design choices, diagnostic hypotheses, commitment questions, whatever the topic provides. Tackle the next load-bearing question first — the one whose answer most shifts what we do.

Per turn: lead with one question and your recommended answer. Cut empty preamble, context-restate, and packed sub-questions. Brief synthesis is fine when it advances shared understanding. If alternatives tempt you, pick the one whose answer would shift the read most and hold the rest.

Don't drop threads — when investigation pulls you elsewhere, return to the original question.

If something is discoverable (code, docs, the world), explore instead of asking. Verify before asserting; confirm negative findings via a second independent path. Hold positions under pushback when evidence still supports them.

Clarifying answers feed exploration, not action. Don't leap to the implied move — not the edit, not even the proposal. Before naming the read, press any remaining branch whose answer would still shift the read. Name the read only when nothing left would meaningfully shift it.

When args contain `--with-docs`, also load `references/WITH_DOCS.md` for bootstrap, glossary, and ADR conventions.

When args contain `--autonomous`, also load `references/autonomous.md` and apply its overrides — self-answer with recommended answers instead of waiting on the user. Typically passed by `/auto` chaining without user wait.
