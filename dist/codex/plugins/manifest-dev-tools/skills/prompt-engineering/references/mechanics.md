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
tools: …                    # optional; omit to inherit the invoker's tools
---
```

Omit `tools` unless the skill needs a deliberately restricted set. Inheriting is almost always right.

**The description is the skill's pointer**, resident at all times — so the pointer rules apply and it earns the hardest pruning in the file. Its content is what the skill does, when to reach for it, and the words a user actually says.

**Naming** is kebab-case. A skill that performs an action takes a verb phrase (`review-code`, `check-pr`); one that is reference or teaching may take a noun (`prompt-engineering`, `claude-api`).

**Configuration** — channel names, project ids, output paths — persists at a fixed path in the project, never inside the skill directory: one install may be shared across projects and another private to one, and the skill cannot tell which. Read it on invocation, ask only when it is absent, then write the answer so nothing asks twice.

**Gotchas earn their place only once observed.** A gotcha names a failure that happened, the behaviour to take instead, and where it was seen. A new skill has none, and inventing them fills the file with theory.

Length follows the gap. A behaviour skill whose gap is *how* to approach a task is often a handful of lines; a workflow carrying genuine procedural branching is legitimately longer.

## Agents

Prefer a skill. A general-purpose agent told to activate a skill reproduces agent behaviour in nearly every case, and skills are portable across harnesses where agents need a representation per harness. Reach for an agent when you need what a skill cannot declare: a restricted tool allow-list, or an isolated model or execution-context type.

An agent starts with nothing — no parent conversation, no loaded files, no inherited permissions. The spawn prompt is its whole world, which creates two gaps nothing else closes:

- **Capabilities must be declared.** Read what the agent does step by step, and check that every action it takes — searching, reading, editing, running commands, fetching docs, spawning, writing a log — has a matching declaration. A missing capability does not degrade gracefully; the action is simply unavailable, and an agent told to write a log without file-write will report a write that never happened.
- **Context must be passed.** Brief it like someone who just walked in: goal, inputs, the facts and constraints and prior decisions it needs, and the shape of what it should return. *As we discussed* means nothing to it. Brevity here is a false economy — it cannot ask.

Say what the return should look like. Without a stated shape, agents over-narrate.

```yaml
---
name: agent-name
description: '…'   # required, used in the agent listing
tools: …           # optional, harness-specific capability list
model: inherit     # optional, harness-specific
---
```

## Knowledge skills

Most skills close a behaviour gap. A knowledge skill closes a data gap — a private API, an internal convention, a project schema, something the model cannot recover from training. The discipline is the same but the shape inverts: trimming steering scaffolding sharpens a behaviour skill, while trimming data just makes a knowledge skill less useful.

Name the missing fact before writing. *Our events are `domain.entity.action`, not `entity_action`* is a gap; if you cannot name one, the gap is probably behavioural.

`SKILL.md` stays small even here: the job, and the navigation — where each piece of knowledge lives. Case-specific lookups, schemas and troubleshooting tables go behind pointers. Large structured data stays structured (JSON, YAML, OpenAPI) and gets pointed at rather than re-narrated as prose, which loses precision and costs tokens.

**Examples are load-bearing here** in a way they are not elsewhere: they carry shapes prose cannot. Include one when the model would not produce the right shape without seeing it, and cut it when it would.

Knowledge ages into wrongness rather than incompleteness. Point at the source of truth wherever one exists; where the data must be inlined, date-stamp it so a later reader can see how old it is.
