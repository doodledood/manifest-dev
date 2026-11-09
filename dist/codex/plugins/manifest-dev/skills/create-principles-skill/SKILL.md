---
name: create-principles-skill
description: 'Create or refresh a project skill that holds one area''s principles — how the project''s people want design, product, prompts, architecture or other work done, and why — drawn from what they already said, so agents with or without manifest-dev start that work from it. Use when the user asks to create a principles skill, capture how the team does design, product or architecture work, or refresh an area''s principles; with no area named, it offers the areas worth one.'
argument-hint: '[area] [--autonomous] [--no-log]'
user-invocable: true
---

Create or refresh one area's principles skill for the project. `../setup-project/references/PRINCIPLES_SKILLS.md` holds the method: what a line must be, the skill's shape and pointer line, which areas are worth a skill, and how lines are written and pruned. figure-out does the work with its whole investigation discipline; this skill adds the brief below.

Invoke the figure-out skill with the brief below and the arguments given, forwarding `--autonomous` and `--no-log` when given. Run it attended unless `--autonomous` was given: only a person's yes writes a line. With no project in reach, say so and stop.

Brief:

> Create or refresh the principles skill for [the area given], following `../setup-project/references/PRINCIPLES_SKILLS.md`.
>
> - With no area given, offer only the high-signal areas that file defines, each with its count and sources, and continue with the ones the person picks.
> - Where the skill exists, refresh it: sharpen before adding, and offer to move or remove each line that fails the file's test.
> - Show every line verbatim with its source before writing it. Write only what the person accepts, and the pointer line with a new skill. With no person present, write nothing and report the candidates.
> - The read names each line written, each candidate left out and where it belongs instead.
