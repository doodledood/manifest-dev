# Knowledge skills

Most skills close a *behavior* gap — the model would do the task naturally, but with the wrong calibration. A knowledge skill closes a different kind of gap: the model lacks data it can't recover from training (private APIs, internal conventions, recent docs, project-specific schemas, organizational facts).

The discipline is the same — content earns its place by closing a real gap — but the *shape* is different. You're not steering behavior with imperatives; you're providing the model with what it needs to answer or act correctly. Trimming "steering scaffolding" makes sense for behavior skills; trimming data makes the skill less useful.

## Identifying the gap

Before writing, name what specifically the model doesn't know. Concrete examples:

- *"Our authentication API returns 401 with a specific JSON shape that includes a `retry_after` field — without this, the model invents the shape."*
- *"Our event names follow `domain.entity.action` not `entity_action` — without this, the model uses common patterns."*
- *"Snowflake `INFORMATION_SCHEMA` views in our environment have these specific column aliases — without this, the model writes queries that fail."*

If you can't name the missing fact, the gap may actually be behavioral — see `skills.md`.

## What goes in SKILL.md vs references

A knowledge skill's SKILL.md should still be small. Put in it:

- The skill's job (one sentence) and when it applies.
- The *navigation* of the knowledge — pointers to where specific data lives, in references or external sources.
- Anything the model needs for *every* invocation (overarching conventions, identity of the system, the one or two facts that apply universally).

Put in `references/` everything the model needs for *specific* invocations: lookups, schemas, examples by case, troubleshooting tables. The reference loads only when the relevant case fires.

If the underlying data is large and structured (an API spec, a schema dump), keep it as a structured file (JSON / YAML / OpenAPI) the skill can point Claude to, not as prose to be re-read. Claude can search and parse structured data; restating it as prose loses precision and adds tokens.

## When examples earn their place

In a knowledge skill, examples are often load-bearing — they show the exact shape of the data when the prose alone can't convey it. An example of a correctly-formed query, an example of the expected error shape, an example of a canonical input/output pair.

The check: *would the model produce the right shape without seeing an example?* If no, the example is gap-closing; include it. If yes, the example is decoration; cut it.

Anthropic recommends 2-5 well-formed examples for tasks with non-obvious output shape. That advice fits here — knowledge skills are exactly the case where examples carry information the model can't infer.

## Freshness

Knowledge skills age. The underlying data drifts (APIs change, schemas evolve, conventions update) and the skill becomes wrong rather than incomplete. Two responses:

- **Point to the source of truth** when you can — link to the live OpenAPI spec, the docs URL, the schema file in the repo. The skill becomes navigation and conventions; the data stays where it's authoritative.
- **Date-stamp inline knowledge** when you must inline it. A note like *"as of YYYY-MM-DD, the `users` table has columns …"* gives future readers a signal that the data may be stale.

When the gap is data and the data has moved, the skill needs updating — not "trimming." Apply the same bidirectional calibration as for behavior skills: add what closes the new gap, remove what no longer reflects reality.

## Gotchas

- **Restating the model's general knowledge.** A "Python coding skill" that explains how `for` loops work is closing no gap. Only document what the model wouldn't reliably produce.
- **Including the whole API spec as prose.** Reference structured files; don't re-narrate them.
- **Knowledge skills disguised as behavior skills.** A skill that says *"always use our event naming convention"* without showing the convention closes nothing. The convention itself is the gap-closing content.
