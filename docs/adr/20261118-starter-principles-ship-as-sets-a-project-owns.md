# ADR: Starter principles ship as sets of general lines that a project takes into its own principles skills

## Status
Accepted

## Area
Project context

## Decided by
The user

## Context
Principles skills hold how a project's people want one area of its work done, and setup offered
one only where the project's history showed several stated-reason corrections in that area. A new
project has no such history, and an older one rarely records reasons, so the offer was thin
exactly where a project starts: an area got no skill, or a few questions drawn from a shipped
skill's own base. The general practices careful teams hold in most areas — repair a defect's
class, report a failure as what it is, prove a change on the real thing — reached a project's
agents only while they ran this workflow's skills, and never reached a colleague's agent that
does not. Mining every project's history again for those same general lines spent each run
re-deriving what does not differ between projects. This decision sits inside the North Star's
*Purpose*: it lets a project keep its people's choices in files any agent reads.

## Decision
setup-project ships one starter set per area — code, architecture, agent behavior, evaluation,
design, product, writing, security and privacy, and working practice — as data beside the
principles method. Each set is a list of general lines in the principles-skill shape, some
offered only where the project meets a stated condition, and a few written as a choice between
two sides that careful teams take differently, with the side to recommend read from the project.
Setup offers the set for each area the project works in, word for word and a few areas at a time,
saying before the yes that an accepted line is held at review and that any line can be struck;
the on-demand principles skill starts from the same set. The project's history works on the set
instead of beside it: it sharpens a line with the project's own reason, adds what the set lacks,
and shows a conflict with both sides, the project's side recommended. Where a project already has
principles skills, the sets are fitted to them by what each says it is for: only lacking lines are
offered, a near-duplicate becomes a sharpening, a conflict keeps the existing line unless the
person picks the other, and a skill spanning two areas may be split on the person's yes. Only a
yes writes a line, and once written the line is the project's own; a later change to a set
reaches it only as a new offer under a new surfaces version. Working-practice lines live in a
skill of their own, whose pointer asks for it before any change, rather than in the context file:
the context file holds what every session needs and stays short, and a skill that any agent loads
before changing anything carries the same reach without growing what every session reads.

## Alternatives Considered
- **Principles that stay inside the plugin**: the lines live only in this workflow's skills — agents that do not run them, including a colleague's, never read them, and a project cannot edit what it does not hold.
- **The question route alone**: with no history, put a shipped skill's key trade-offs to the person as questions — it produced a few lines per area, and it asked a person to state, from nothing, practices most teams share.
- **Shipping none**: leave each project to grow its skills from its own corrections — a new project then starts every area with no stated principles, which is the case the offer exists for.

## Consequences

### Positive
- A new project can start each area it works in from a full set of general lines, in files every agent loads through the context file.
- History mining narrows to what is specific to the project: its reasons, its gaps and its departures.

### Negative
- An accepted starter line binds that project's reviews like any other principles line, so a line taken without thought can turn a fork into a finding; the offer says so before the yes, and any line can be struck.
- Whether the sets improve a project's results is untested: the change shipped on drives that show setup offering and writing them, with no comparison of projects with and without them.
- A change to a set ships only as a new surfaces version, which every installed project is then offered.

## Enforced by
partly — `tests/test_starter_principles.py` pins each set's shape (reason and yield on every line, a condition on each conditional line, both sides and a default rule on each choice) and that the method's table names exactly the sets on disk; `tests/test_setup_project_versions.py` digests the sets with what setup emits, so a set changed without a new surfaces version fails. That only a person's yes writes a line, and how sets are fitted to existing skills, stay judgment.

## Revisit when
Projects that took starter sets strike or reword most of the lines they accepted, or their reviews stop citing them, within their first months of use — read in those projects' principles skills' git history and their pull request reviews.

## Source
- Session: maintainer rulings while defining the change
- Related: Amends [20261109-area-principles-live-in-project-skills](20261109-area-principles-live-in-project-skills.md): a principles skill can start from a shipped starter set, and the project's history hones it
