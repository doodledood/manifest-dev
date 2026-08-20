# ADR: The project is the unit the workflows serve, not the single task

## Status
Accepted

## Area
Positioning

## Context
The North Star's Diagnosis named a task-level barrier: experienced developers do not trust
agent output enough to hand off larger *tasks*, and nothing verifies output against a stated
intent. That described what the suite was in June and July, when the work was the
figure-out → define → do loop and the artifact was one Manifest per run.

It stopped describing what the project builds. Counting the decision corpus by month: through
July, 56 records, of which 5 concern anything above a single task. In August, 52 records, of
which **27** do — ticketing, positioning, project context, goal-setting, repo layout, and the
North Star surface itself. Half a month's recorded thinking landed on ground the Diagnosis did
not mention.

Two readings were weighed against those records. The first held that the mission was unchanged
and only the diagnosis had deepened — the same trust problem climbing to whatever context a
decision rests on. It fails its own test cases: `next-ticket`, the Winning field, and
`sweep-tickets` are not trust mechanisms, because nobody reviews their output. They allocate
attention and keep work moving. The second held that the project had become a business tool
serving solo founders. That over-claims in two directions: the suite does no business work —
no finance, support, hiring, or analytics, only context an agent's decision rests on — and it
narrows the audience to a segment no evidence supports, against a standing Never that forbids
promising what cannot reliably be delivered.

What survived is narrower than the second reading and wider than the first. The unit moved
from the task to the project, and the count of people involved is orthogonal to it: the ticket
machinery writes a claim precisely so concurrent readers of one store get different work, and
on a shared tracker "the claim holds against everyone"; the conventions files exist so a
teammate running no manifest-dev can still maintain the surfaces.

## Decision
The Diagnosis is rewritten to name the project as the unit: agents can write almost anything
now and projects still drift, because what a project is trying to become, what is worth doing
next, and what done means live in whoever happens to be working, so every session and every
teammate re-derives them and the agent's speed multiplies work nobody can tell was worth doing.

The Manifest is one of three contracts at three lifetimes rather than the contract: the North
Star stands and moves only on the owner's ruling, a Ticket lives as long as its unit of work,
and a Manifest resets every run. Each tier exists to make the tier below it decidable — the
North Star makes Appetite decidable, a Ticket makes a run dispatchable, a Manifest makes a diff
verifiable.

Unchanged by this: the audience, which already reads "solo or small-team" with teams secondary
and which nothing here argues for narrowing; the promise; the standing Nevers; and the bet
sentence carried inside the Diagnosis, which still speaks at the task unit and is left for its
own ruling rather than rewritten alongside.

## Alternatives Considered
- **Leave the Diagnosis as written**: rejected — a standing direction that does not describe
  what the project builds is the failure the surface exists to prevent, and it had already
  stopped describing half of one month's decisions.
- **Same mission, deeper diagnosis** (the trust problem climbing levels): rejected on its own
  test cases, above.
- **A business-lifecycle mission for solo founders**: rejected — the suite does no business
  work, and the claim would narrow the audience to an unevidenced segment while sitting in the
  register the project's Never was written against.
- **Rewrite the bet sentence in the same act**: rejected — the owner ruled the barrier text,
  not the bet; inventing a replacement would be exactly the silent position change the update
  asymmetry forbids.

## Consequences

### Positive
- The Diagnosis explains every lineage the project has built: what done means (Manifest tier),
  what it is becoming (North Star), what is worth doing next (`next-ticket`, Winning), that a
  stranger can pick work up (the ticket convention), and that a teammate without the tool still
  can (the conventions files).
- Future scoping has a stated unit to test against, so work above the task no longer reads as
  drift from the project's own direction.

### Negative
- The bet sentence inside the Diagnosis now speaks at the old unit, and stays that way until
  it is ruled — a visible seam rather than a silent one.
- A project-level unit invites scope that a task-level one refused; the Nevers and the
  no-business-work boundary recorded here are what hold it.

## Source
- Session: figure-out on whether the mission had moved, 2026-08-20; owner's ruling on the
  rewritten Diagnosis. First position change under the North Star update asymmetry after the
  cost ruling.
- Related: 20260820-manifest-dev-owns-a-project-north-star, 20260820-north-star-lines-carry-states, 20260820-cost-is-a-binding-constraint-second-to-quality
