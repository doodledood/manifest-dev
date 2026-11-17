# ADR: A review holds work to the project's principles unless a person chose the departure

## Status
Accepted

## Area
Code review

## Decided by
The user

## Context
The build side already had its rule: where a request conflicts with a principle in a principles
skill, the principle holds unless the person chose the departure
(`20261109-an-unattended-run-keeps-to-a-principle-over-a-conflicting-request`). The review side
had only half of it. `review-code` loaded the principles skills and said a change following one
raises no finding; nothing said a change departing from one raises a finding.
`context-file-adherence` audited principles with a bar written for exact rules and graded "departures from
advisory preferences" Low, and nothing said whether a principle is binding. `review-prompt`,
`review-design` and `review-writing` named no principles skill, though runs of them followed the
context file's pointers.

In one observed case, a pull request built a mechanism around one narrow case, against a ratified
principle that rules that shape out unless its stated condition holds, and added a decision record
of its own calling the narrow shape intended. The automated review loaded the principles and passed
the change. A replay showed three mechanisms: the reviewers listed the principle as applied with
no finding and took the yield as met on the change's own account; a reviewer that did name the
departure graded it Low and passed, so the default publication policy dropped it; and the change's
own record counted as a person's choice. A person caught the departure by hand.

## Decision
At review, a principle in a principles skill the project context file points to holds unless its
yield is shown or a person with authority over it chose the departure.

- **Shown yield.** Evidence shows the yield's condition holds. The work itself and the rest of the
  project count; the work's own assertion that the yield holds does not; a condition the evidence
  leaves open or arguable is not shown, because the principle holds unless its yield is shown.
- **A person's choice.** The person needs authority over the principle: the work is done for
  them, or the project's records give them that area; writing the change gives none, and where
  the evidence leaves open who chose or whether they had that authority, nothing was chosen. The
  choice shows in a record in force before the change, that person's own statement in the
  session or the pull request conversation, a delegation naming the departure, or the caller's
  report of that choice with its source. A record or design document the change itself adds is its
  case, not that choice, and so is anything the run that produced the change wrote, such as the
  pull request description or a reply posted on the person's account.
- **An unchosen departure** is a broken project obligation: reported with the principle quoted,
  graded High on the shared ladder (Critical where its consequence is) whichever dimension
  reports it, so a verdict does not turn on the dimension named, and counted against acceptance under
  the caller's policy.
- **Both directions.** The project's principles outrank a review's general standards: work that
  follows one raises no finding from a default it departs from, and work that departs from one
  raises a finding where the general standards would raise none. A critical failure is still
  reported, naming the principle that produced it.
- **Any project's skills, by line.** A reviewer finds the skills through the context file's
  pointers in whatever words they are written, loads those whose stated use covers the work, and
  applies each line to the calls it bears on, whatever area word the skill carries. No review skill
  maps an area or a skill name to a reviewer.
- **Where it is reported.** The `review-code` dimension that owns a principle's call reports the
  departure, and `context-file-adherence` covers every principle as the backstop. `review-pr`'s
  consolidation merges the duplicate.
- **What a report shows.** Where a loaded principles skill covers the work, the report lists each
  principle the work touches: followed; yield shown, with the evidence; departure chosen, by whom
  and where; departs, with the finding; or not judgeable, for a line the work cannot show either
  way, such as how its author works. What a yield allows counts only once its condition is shown:
  an unshown yield is a departure, never "followed" or "not judgeable".

The rule is one paragraph, carried word for word by the method,
`setup-project/references/PRINCIPLES_SKILLS.md` → *Using one*, and by `review-code`'s
`references/PROJECT_PRINCIPLES.md`, which its body loads only where the project context file points
to principles skills, so reviews in other projects carry none of it. `review-prompt`, `review-design`,
`review-writing` and `review-pr`'s consolidation get no new text: run alone on projects whose
context file points to a principles skill, they already loaded it, applied it in both directions,
rejected the work's own claim of a yield, and failed the gate on an unchosen departure. Text is added
where a run was seen missing the behavior, and only there.

**Fit with records and principles in force.** No severity grade is added
(`20261105-review-severity-follows-consequence`): a ratified principle is an applicable source
obligation, which the caller policy of `20261106-review-evidence-serves-substantive-acceptance`
already counts. A caller's deliberately supplied severity or publication policy still applies to
the graded finding. This repository's product principle that a review grades by consequence and
raises no grade to force a fix stands as written beside this decision: the principle is a
requirement the project already set, and the reviewer adds no grade. Judgment findings stay
advisory (`20260708-judgment-layer-is-a-review-time-premise-check`).

## Alternatives Considered
- **Each departure posted as a non-blocking question, outside the severity filter**: not chosen.
  The author can answer and merge, so the person who wrote the principle still has to catch the
  departure by hand.
- **Only lines a project marks as hard hold at review**: not chosen. Every project would have to
  mark its lines, and most departures would stay Low and unposted.
- **Departures reported by `context-file-adherence` alone**: not chosen. A single-dimension
  review would miss them, and that dimension's bar was written for exact rules rather than for
  judging a yield.
- **The same paragraph in every review skill**: not chosen. The other reviewers already show the
  behavior when the context file points them to the skills; a copy in each would add text no run was
  seen to need.
- **Departures reported by the owning reviewer alone, with no backstop**: not chosen. A principle
  that no dimension clearly owns would fall between them.

## Consequences

### Positive
- A project that writes its principles down gets reviews that catch departures without its people
  reading each change, attended or not.
- The rule holds for any project's skills, whatever they are called and however their pointers are
  written.

### Negative
- A vague principle, or one with a missing yield, now draws findings. Sharpening lines matters more.
- One departure can draw two findings in a fleet; consolidation has to merge them.
- A person's choice recorded only inside the change has to be stated again by that person, or
  reported by the caller with its source, before a review counts it.

## Enforced by
partly — `tests/test_principles_skills.py::test_review_code_carries_the_review_rule_word_for_word`
holds that the method and `review-code` carry the same paragraph, and
`test_no_review_skill_picks_principles_by_area_name` that no file a review skill loads names a
concrete principles skill rather than the `<area>-principles` placeholder. Whether a review applies it
is judged by the `review-code` recipe's `principles-depart` and `principles-hold` scenarios, the
`review-pr` recipe's `principles` scenario, and the `principles` scenarios of the `review-prompt`,
`review-design` and `review-writing` recipes.

## Source
- Session: a figure-out session on whether reviews honor a project's principles skills, followed
  by a define and do run (logs kept locally).
- Related: extends 20261109-an-unattended-run-keeps-to-a-principle-over-a-conflicting-request;
  amends 20261109-area-principles-live-in-project-skills; narrows
  20261014-design-time-probes-cover-what-reviewers-can-know-and-defaults-yield-to-stated-rules; see
  also 20261105-review-severity-follows-consequence, 20261106-review-evidence-serves-substantive-acceptance
