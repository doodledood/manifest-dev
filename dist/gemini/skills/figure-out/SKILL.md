---
name: figure-out
description: 'Figure things out together — any topic, problem, or idea. Probes relentlessly until shared understanding is reached. Use when you need to understand something before acting, or when figuring it out IS the goal. Triggers: figure out, help me think through, dig deeper, probe this, what is really going on, investigate, work through, why does.'
argument-hint: '[topic] [--with-docs]'
user-invocable: true
---

Probe the topic relentlessly. Walk every branch of the decision tree — design choices, diagnostic hypotheses, commitment questions, whatever the topic provides. Tackle the next load-bearing question first — the one whose answer most shifts what we do. Ask one question at a time, wait for the answer, give your recommended answer with each.

Don't drop threads — when investigation pulls you elsewhere, return to the original question.

If something is discoverable (code, docs, the world), explore instead of asking. Verify before asserting; confirm negative findings via a second independent path. Hold positions under pushback when evidence still supports them.

Clarifying answers feed exploration, not action. Don't leap to the implied move — not the edit, not even the proposal. When the space is exhausted, name the read; the user calls for any proposal or edit. When the read is named or the user signals readiness, point to `/define` to lock the understanding down as a Manifest.

When args contain `--with-docs`, also load `references/with-docs.md` for glossary and ADR conventions.

When args contain `--autonomous`, also load `references/autonomous.md` and apply its overrides — self-answer with recommended answers instead of waiting on the user. Typically passed by `/auto` chaining without user wait.
