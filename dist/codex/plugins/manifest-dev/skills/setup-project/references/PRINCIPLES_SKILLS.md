# Principles skills

A principles skill holds how a project's people want one area of its work done — design,
product, prompts, architecture, writing, or any other kind of work the project does — where a
careful agent could otherwise pick a different good option. It is a project skill named
`<area>-principles`, such as `design-principles`, so it loads when work in its area starts rather
than in every session, and any agent can load it, with or without this workflow. One line in the
project context file says when to load it.

This file is the method. Every skill that creates, grows, refreshes or loads a principles skill
follows it from here.

## What a line must be

Every line passes this test, or it does not enter:

- **It is a principle** — a limit or a trade-off the area's people hold, worded so it carries to
  calls nobody has discussed yet, with the reason it holds and when it yields:
  `- <the principle> — <why>. Yields when <condition>.` Where no principle form fits, as with a
  hard limit that has no trade-off, write it in another form and say so in the line.
- **Its source is one of three:** a person's statement of how they want the work done or why they
  turned a proposal down; a failure seen in this area's work, with what was wrong; or a default a
  model or a shipped skill would otherwise follow, which a person chose to depart from or to hold.
  A reason inferred and never confirmed is no source.

Everything else goes somewhere else:

| Candidate | Its home |
|---|---|
| A decision — one option chosen over others, which the project would re-tune when evidence moves | a decision record; the skill does not restate it |
| A rule a check can hold — a lint, a test, a type | that check |
| A reaction to one piece of work | that work |
| A fact the repository already shows — a layout, a library in use | nowhere |
| A call a run made on its own | nowhere |
| When or why a line was added or changed | nowhere in the skill |

## The shape

```markdown
---
name: <area>-principles
description: '<Area> principles for <project>: how its people want <area> work done, and why. Use before planning, designing, prototyping, building or reviewing <area> work in this project.'
---

Edit rule: each line is a principle with its reason and when it yields. Decisions go to the
decision records, rules a check can hold go to the check, and a line is added only on a person's
yes, after sharpening an existing line is ruled out.

- <principle> — <why>. Yields when <condition>.

Before calling <area> work done, check it against these principles from a fresh start — a new
session, or a reviewer who did not do the work — fix what departs, and repeat until nothing does.
Name any departure you keep, with the principle and why.
```

Keep the description on one physical line. The file lives where the detected host loads project
skills — `.claude/skills/<area>-principles/SKILL.md` on Claude Code, `.agents/skills/` on Codex
and OpenCode — and where a project serves several hosts, one copy with a link from each other
folder, never two copies. Use no term of this workflow that the skill does not explain.

**The pointer line** goes in the project context file's project-surfaces section, one per skill,
saying only when to load it and where it is:

`- **<Area> work** — load the \`<area>-principles\` skill (\`<path to its SKILL.md>\`) before planning, designing, building or reviewing it.`

## Where content goes

Sort by how often the work it guides happens:

- A principle nearly every session in the project needs stays in the project context file.
- A principle that only one area's work needs goes to that area's skill.
- How one person likes to work, wherever they work, goes to that person's own memory file.

A project's Taste entries — steering preferences in a `## Taste` section of the project context
file — sort the same way. One that only one area's work needs moves to that area's skill, its
preference becoming the principle, its rationale the reason, and its flip condition the yield.

## Which areas are worth a skill

Offer a skill only for a high-signal area:

- the project's history holds several stated-reason corrections, review asks or decision records
  whose reasoning is a preference in that area — count them, and name the sources;
- the project context file already holds principles or Taste entries that only that area's work
  needs; or
- with no history to read, the project does that kind of work and a shipped skill holds an
  opinionated base for it, such as visual design or prompts. Put the base's key trade-offs to the
  person as questions, with the base's position as the recommended answer; their answers are the
  lines.

One stray comment in an area is not signal. Offer at most three areas at a time, each with its
count and sources, and let the person accept them in one batch.

## Writing, growing and pruning

Only a person's explicit yes to the shown text writes, moves or removes a line, or creates a skill
or a pointer line. An answer the person gave in advance for a named run is that yes for that run's
offers. With no person present, write nothing and report the candidates with their sources.

- **Create:** read the sources — the project's docs, its decision records' reasoning, review and
  pull request threads, commit bodies, the project context file and its Taste entries, and past
  session records only once the person agrees to have them read. Put each candidate through the
  test above, show the draft lines verbatim with the source of each, write what the person
  accepts, and add the pointer line.
- **Grow:** when a person states why they want work in one area done differently, offer a line for
  that area's skill — creating the skill and its pointer line on a yes when none exists — rather
  than a project-wide Taste entry.
- **Sharpen before adding:** when an existing line covers or nearly covers a candidate, offer to
  sharpen or replace it instead of adding a sibling; when a new line makes an old one redundant,
  offer to retire the old one in the same offer.
- **A principle steered against:** when a person steers work against a principle the run loaded,
  ask whether the principle has moved or this is an exception. On "moved", show the revised or
  removed line and change it on their yes; on "exception", change nothing, and the work names the
  principle it departs from.
- **Gather what the session showed:** before a session ends, look again at the corrections with a
  stated reason that it did not offer or that the person put off. Where one area's corrections in
  this session meet the high-signal bar above, offer that area's lines in one batch, with the count
  and sources. One stray correction is still not signal.
- **Prune on contact:** a run that keeps or grows principles skills — not a review of a change —
  and loads one holding a line that fails the test above offers, once, to move it to its home or
  remove it.

## Using one

Before planning, designing, prototyping, building or reviewing work in an area, load the skill its
pointer line names. A principle shapes the work. Departing from one is the person's call: name the
principle and why, and leave the choice to them, or to the delegation that covers it.
