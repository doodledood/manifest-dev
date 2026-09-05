# Mechanics

What changes with the artifact. The levers in `SKILL.md` decide the content; this decides the container.

## Skills

A skill is a directory — `SKILL.md` plus companions (`references/`, `assets/`, `scripts/`) — not a loose file. What sits beside `SKILL.md` is part of the design: it is what the run can reach when the skill fires.

```yaml
---
name: kebab-case-name       # required, lowercase, hyphens, max 64 chars
description: '…'            # required, activation prose, max 1024 chars, one physical line
argument-hint: '<request>'  # optional, shown in the slash-command UI
user-invocable: true        # optional, default true; false hides it from the command menu
---
```

Use only metadata supported by the target hosts. Tool restrictions and inheritance are host capabilities, not portable skill fields; check the host schema and effective permissions before relying on them.

**The description is the skill's pointer**, resident at all times — so the pointer rules apply and it earns the hardest pruning in the file. Its content is what the skill does, when to reach for it, and the words a user actually says.

**Naming** is kebab-case. A skill that performs an action takes a verb phrase (`review-code`, `check-pr`); one that is reference or teaching may take a noun (`prompt-engineering`, `claude-api`).

**Configuration** — channel names, project ids, output paths — persists at a fixed path in the project, never inside the skill directory: one install may be shared across projects and another private to one, and the skill cannot tell which. Read it on invocation, ask only when it is absent, then write the answer so nothing asks twice.

**Gotchas earn their place only once observed.** A gotcha names a failure that happened, the behaviour to take instead, and where it was seen. A new skill has none, and inventing them fills the file with theory.

Length follows the gap. A behaviour skill whose gap is *how* to approach a task is often a handful of lines; a workflow carrying genuine procedural branching is legitimately longer.

## Agents

Prefer a skill. A general-purpose agent told to activate a skill reproduces agent behaviour in nearly every case, and skills are portable across harnesses where agents need a representation per harness. Reach for an agent when you need what a skill cannot declare: a restricted tool allow-list, or an isolated model or execution-context type.

Check what the host actually inherits: conversation, loaded instructions, tools, and permissions may differ by execution type. Supply the goal, missing context, constraints, inputs, and return shape. Verify that the required capabilities are available; declaring a tool cannot grant a permission the host withholds.

Use the target host's schema for an agent definition. Specify only overrides the task requires, and use its supported communication channel when missing information must return to the caller.

## Knowledge skills

Most skills close a behaviour gap. A knowledge skill closes a data gap — a private API, an internal convention, a project schema, something the model cannot recover from training. The discipline is the same but the shape inverts: trimming steering scaffolding sharpens a behaviour skill, while trimming data just makes a knowledge skill less useful.

Name the missing fact before writing. *Our events are `domain.entity.action`, not `entity_action`* is a gap; if you cannot name one, the gap is probably behavioural.

`SKILL.md` stays small even here: the job, and the navigation — where each piece of knowledge lives. Case-specific lookups, schemas and troubleshooting tables go behind pointers. Large structured data stays structured (JSON, YAML, OpenAPI) and gets pointed at rather than re-narrated as prose, which loses precision and costs tokens.

**Examples are load-bearing here** in a way they are not elsewhere: they carry shapes prose cannot. Include one when the model would not produce the right shape without seeing it, and cut it when it would.

Knowledge ages into wrongness rather than incompleteness. Point at the source of truth wherever one exists; where the data must be inlined, date-stamp it so a later reader can see how old it is.
