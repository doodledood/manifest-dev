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
session, or a reviewer who did not do the work. Fix what departs unless the person chose the
departure, and check again only after a fix, until a check finds none. Name each departure kept,
with the principle and why.
```

Keep the description on one physical line. The file lives where the detected host loads project
skills — `.claude/skills/<area>-principles/SKILL.md` on Claude Code, `.agents/skills/` on Codex
and OpenCode — and where a project serves several hosts, one copy with a link from each other
folder, never two copies. Use no term of this workflow that the skill does not explain.

**The pointer line** goes in the project context file's project-surfaces section — at the file's
end where it has no such section, creating the file where the project has none — one per skill,
saying only when to load it and where it is:

`- **<Area> work** — load the \`<area>-principles\` skill (\`<path to its SKILL.md>\`) before planning, designing, building or reviewing it.`

A skill about how any change is made, such as working practice, says so in both places: its
description reads "Use before making any change in this project", and its pointer line says to load
it before changing anything in the project.

## Where content goes

Sort by how often the work it guides happens:

- A principle nearly every session in the project needs stays in the project context file.
- A principle that only one area's work needs goes to that area's skill.
- How one person likes to work, wherever they work, goes to that person's own memory file.

Only principles and Taste entries sort. Everything else in the context file — commands, checklists,
ownership notes, operating rules, conventions a check holds — stays where it is, untouched.

A project's Taste entries — steering preferences in a `## Taste` section of the project context
file — sort the same way. One that only one area's work needs moves to that area's skill, its
preference becoming the principle, its rationale the reason, and its flip condition the yield.

## Which areas are worth a skill

Offer a skill only for a high-signal area:

- the project's history holds several stated-reason corrections, review asks or decision records
  whose reasoning is a preference in that area — count them, and name the sources;
- the project context file already holds principles or Taste entries that only that area's work
  needs; or
- a starter set covers the area and the project does, or is about to do, that kind of work
  (*Starter principles*, below).

One stray comment in an area is not signal. Offer at most three areas at a time, each with its
count and sources, and let the person accept them in one batch. This bar governs the offers nobody
prompted — from history, at setup, or in a session's closing sweep. A person who states why they
want one area's work done differently has given the signal themselves: *Grow* offers that line.

## Starter principles

This workflow ships one starter set per area, as data beside this file in `starter-principles/`.
Each set names its skill, says which projects it is offered to (`Offered when`), and lists its
lines in the shape a principles skill holds. A line marked `Only where <condition>:` is offered
only to a project that meets the condition. A line marked `Choice —` holds two sides of a call
careful teams make differently, and says which side to recommend from what the project shows. The
sets are general lines a person can take as they are, sharpen, or strike; once written, a line is
the project's own, and a later change to a set reaches the project only as a new offer.

| Area | Set |
|---|---|
| Code | `starter-principles/code.md` |
| Architecture | `starter-principles/architecture.md` |
| Agent behavior (prompts, skills, features built on a model) | `starter-principles/agent.md` |
| Evaluation | `starter-principles/evaluation.md` |
| Design | `starter-principles/design.md` |
| Product | `starter-principles/product.md` |
| Writing | `starter-principles/writing.md` |
| Security and privacy | `starter-principles/security.md` |
| Working practice | `starter-principles/working-practice.md` |

An area with no set here keeps the routes above: its history, or the context file's principles.
An area a person names is matched to a set by what the set covers, not by its name, and the skill
takes the person's word for the area where they gave one.

- **Which areas.** Offer each area whose `Offered when` the project meets, or will meet from what
  its person says it is for; a new project counts by what it is about to hold, for an area and
  for a line's condition alike. Offer the areas three at a time, by the bar above, and once a
  batch is answered offer the next.
- **How a set is shown.** Show each line exactly as it would be written: a conditional line
  without its marker, and only where its condition holds; a choice as its two sides, the
  recommended side first with the signal that picked it. Leave out a line that restates a
  principle the project context file holds; where that principle moves into the skill (*Where
  content goes*), it takes the starter line's place in the project's own words. Before the person
  answers, say that an accepted line is one later reviews hold the work to, and that any line can
  be struck or reworded now. Write what is accepted, a choice as its chosen side's text alone;
  within a set the person accepted, a choice they left unanswered takes the recommended side, and
  a line struck stays out.
- **With history.** Read the project's history for this area as *Create* says, then let it work
  on the set rather than beside it: a source that gives a starter line this project's own reason
  or case sharpens that line; a source the set does not cover becomes a new line, under the test
  above; a source that states a line the set already holds adds nothing of its own. A source
  takes the other side of a starter line when following it departs from that line in a case the
  project meets, even where the line's yield could be read to allow the departure; then show both
  sides with that source, recommend the project's side, and leave the starter line out unless the
  person picks it.
- **With skills already in place.** Fit each set to the project's own skills by what each says it
  is for, never by its name. Offer only the lines its skills lack. A skill holds a starter line
  only where one of its lines states all of it, in whatever words and for at least the cases it
  covers — what it asks and when it yields; for a choice, all of one side, and an `Only where`
  condition decides whether the line is offered, not what it says. A starter line whose parts are
  spread over several lines is lacked, and is offered as a sharpening of the line nearest it or as
  a line of its own, shown beside those lines. Where an existing line nearly states a starter line, offer to sharpen the
  existing line instead of adding a second. Where one
  takes the other side of a starter line, in the sense above, show both and keep the existing one
  unless the person picks the other. Where the project cuts its areas differently from the sets, offer a split or a merge of
  its skills as an item of its own; an existing line moves only on the person's yes.
- **When.** A first setup offers the whole set for every area the project meets and no skill
  covers. A later setup or audit names each such area in one line — the area, how many lines its
  set holds, and why it applies — and shows the set only on a yes. For an area a skill covers,
  the lines it lacks are offered once, where the project records no surfaces version or one before
  the version that last changed that area's set — each version's changes file names what it
  changed — and again whenever a person asks for them. Where the project records a version before
  the one that last changed the fit in *With skills already in place*, the lines a skill carries
  only in part are offered once as well; a line it lacks entirely and was offered before is not. With no person present, write nothing and
  report each area's lines as candidates for the person.

## Writing, growing and pruning

Only a person's explicit yes to the shown text writes, moves or removes a line, or creates a skill
or a pointer line. An answer the person gave in advance for a named run is that yes for that run's
offers. With no person present, write nothing and report the candidates with their sources.

- **Create:** start from the area's starter set where there is one (*Starter principles*). Read the
  sources — the project's docs, its decision records' reasoning, review and pull request threads,
  commit bodies, the project context file and its Taste entries, and past session records only
  once the person agrees to have them read. Put each candidate through the test above, show the
  draft lines verbatim with the source of each, write what the person accepts, and add the pointer
  line.
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
pointer line names. A principle shapes the work. Where what was asked conflicts with a
principle and the line's own yield does not cover the case, the principle holds unless the person
chose the departure: they named the principle or said to set it aside, or a decision record or a
delegation that names the departure covers it. With the person present, ask whether the principle has moved or this is an
exception. A run with no person present builds to the principle and puts the conflict first in
what it reports: what was asked, the principle, what it built instead, and the one change that
restores what was asked. A departure the person chose is kept, and named with the principle and
why.

A review holds the work to the principles in the same way, without a request to weigh against
them:

A project's principles skills are project skills named `<area>-principles`, with whatever area word
the project chose, each line a principle with its reason and when it yields. Find them through the
project context file's pointers, in whatever words those are written, and load each whose stated use
— what its pointer line or description says it is for — covers the work under review. Apply each
line to the calls it bears on in that work, whatever the skill holding it is called. These
principles outrank the review's general standards in both directions: work that follows one raises
no finding from a standard it departs from, and work that departs from one raises a finding where
those standards would raise none. A principle holds unless its yield is shown or a person with
authority over it chose the departure. Its yield is shown by evidence that the yield's condition
holds: the work itself and the rest of the project count, the work's own assertion that it holds
does not, and a condition the evidence leaves open or arguable is not shown. What a yield then
allows, such as a narrow version named for its one case, makes the status "yield shown" only once
its condition is shown; until then the work departs, unless such a person chose the departure. A
person has authority over a principle when the work is done for them or the project's records give
them that area, and authoring the change gives none. Such a person chose the departure when a record
in force before the change, that person's own statement in the session or the pull request
conversation, a delegation naming the departure, or the caller's report of that person's choice with
its source says so; where the evidence leaves open who chose it or whether they had that authority,
it is not chosen. A record or design document the change itself adds is its case, not a person's
choice, and so is anything the run that produced the change wrote, such as the pull request
description, a commit message or a reply on the person's account. An unchosen departure is a broken
project obligation: report it with the principle quoted and the departing text named, never grade it
Low because it concerns naming, structure or style, and count it against acceptance under the
caller's policy. After the findings, list each principle the work touches that bears on the calls
this review judges, and where it stands — followed; yield shown, with the evidence; departure
chosen, by whom and where; departs, with the finding; or not judgeable, for a line the work under
review cannot show either way, such as how its author works — and leave the list out where no loaded
principles skill covers the work. A critical failure is still reported, naming the principle that
produced it.
