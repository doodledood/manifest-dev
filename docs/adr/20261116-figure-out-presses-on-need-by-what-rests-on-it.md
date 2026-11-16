# ADR: figure-out presses on need by what rests on it, and counts what a part keeps costing

## Status
Accepted

## Area
figure-out

## Decided by
The user — the rulings quoted under Decision, and reversing part of two records:
`20260714-figure-out-classifies-constraints-before-they-prune`, which rejected challenging whether
a user-fixed constraint should exist, and
`20261026-figure-out-prices-effort-by-what-the-agent-does-not-control`, under which only costs
outside the agent's control moved the default. An agent wrote this record and the change under
the user's instruction to carry out and merge it; the user has not reviewed the record's text.

## Context
The owner reported that a figure-out session on a feature accepts each requirement they state,
proposes or keeps parts whose need nobody tested, and never puts removing what exists forward as
an answer. Their reasoning: "Building is probably near free however complexity is not";
unneeded parts "grow the surface area where things go wrong" and are "cognitive load on both
the agents and humans". They also did not want the opposite failure: "I don't want it to become a
battle each figure out session and endlessly explaining to the agent every little thing", with
the push "mainly on corner stones".

The skill's one line on need was "each proposed requirement, component, or step earns its place
before you design it", which names no test a run can execute. Its pricing line told a run that
an agent's building costs little and named no cost a part carries once it exists. Two records
pulled the same way: `20260714-figure-out-classifies-constraints-before-they-prune` rejected
challenging whether a user-fixed constraint should exist, as re-litigating a decision the user
owns, and `20261026-figure-out-prices-effort-by-what-the-agent-does-not-control` made the default
the solution that would be right if effort were free.

Six behavior cases were written before any edit, and driven on the skill as it stood at the merge
base, each reply graded by a fresh context from its grader file alone:

- `110` (attended, a costly requirement among small ones), `111` (the person says keep to a costly
  requirement, then gives the reason), `112` (keep to a modest one) and `113` (unattended, a small
  feature that invites additions) passed every grader on two runs each.
- `114` (unattended, a stale cache kept for a removed dashboard) put removal forward on both runs,
  but counted what the larger answer keeps costing on one run of two.
- `115` (unattended twin of `110`, held out) kept the requirement but did not flag the doubt with
  what rests on it, the result without it, and a recommendation.

So most of what the owner asked for already held on the current skill and model. Two parts did not.

## Decision
The behavior figure-out owes, as the owner ruled it:

- A requirement is pressed on need in proportion to how much of the build, and of what must be
  kept true after it, rests on it, whether the person presented it as central or said it in
  passing. A real part of the build gets one press; only one on which most of the build rests
  gets a second. A requirement whose owner or reason the person stated is not pressed.
- A press states what rests on the requirement, what the session found when it looked for the
  need, what the result is without it and what the session would do, and ends in one ask a short
  answer settles. It is not a bare question of why. A doubt about a small thing takes no turn; the
  read may carry it in a line.
- The second press, given only "keep", accepts the requirement and asks what it is for. It does
  not argue again. After that answer the requirement stands. The owner: "One if not too costly
  press again if so … I want to optimize for better outcomes though more than ease of figure
  out."
- The session's own proposals carry no part whose need nobody tested, and removing what exists
  competes as an answer.
- When answers differ in size, what the larger one keeps costing once it exists counts against it:
  more to read, verify and keep true, and more that can go wrong. It is not free because an agent
  builds it.
- With nobody to ask, a requirement the person stated stays in what the read proposes to build,
  and the doubt is flagged with what rests on the requirement, the result without it and the
  session's recommendation. The owner chose "keep it, flag doubt" over cutting it or narrowing it
  silently.

What this change ships, and why only that: the skill was edited only where a case failed, and
each later edit answers a failing verdict or a review finding. A first standing-cost line, worded
to count what a part keeps costing "against the larger answer", did not hold `114` or `115` and
broke `110` on three runs of three: each session recast the costly requirement as a cheaper fixed
menu and asked which reading the person meant, instead of asking whether it was needed at all.
The press has to be named where stated requirements are carried. So the shipped text is:

- In `figure-out/SKILL.md`, beside the rule that carries stated requirements as hard: "before
  designing any version of one that much of the build rests on and whose reason is unstated,
  press its need: what rests on it, the result without it, your recommendation" (`110`, `115`).
  A requirement whose reason the person gave is not pressed.
- In the pricing bullet: "Cheap to build is not cheap to own, so where options differ in size,
  what the larger keeps costing — more to read, verify and keep true, more that can break — is
  one" — one of the costs that move the default off the solution that would be right if effort
  were free (`114`). Counting it in the abstract did not hold `114`.
- In `autonomous.md`, each flagged item also carries, "where the two differ in size, what the
  larger keeps costing once built" (`114`). With the pricing bullet alone, `114` named the
  standing cost on one run of two; with this clause, on four of four.
- In `autonomous.md`, the keep-and-flag sentence, with the requirement kept "as they stated it,
  not narrowed to a cheaper reading" (`115`).

Room was made inside the same and nearby bullets, so the always-loaded body is no longer than it
was (3,359 words). What left it: "genuinely", "for the person" and "beside it"; the North Star
heading names under which a project names who it is for; "of code, documents or analysis" after
the agent's work, now "research, design, building and testing"; the examples of a record line
read wider than its words; and "An inquiry exclusion does not exclude later delivery", which
`ticket-up/references/AUTHORITY.md` states and every run reads first. The status-quo trigger now
reads "Before proposing to change or remove what exists, test what job it might be doing". A
review of the trims restored the record-line fit check in full: a line "whose words and reason,
read as written, do not cover the case, or a record whose premise no longer holds, counts nothing
against it".

The second press and the removal answer get no new text: the cases showed them holding, and an
addition that costs every run earns its place by a gain shown on evidence. The cases now hold
them.

Results, each reply graded by a fresh context from the grader file alone (runs that passed of
runs graded):

| Case | Grader | Merge base | Shipped |
|---|---|---|---|
| `110` | presses the costly requirement / brings a position / leaves the rest | 2/2 each | 2/2 each |
| `111` | presses once more / asks for the need / ends after the answer / no why on small things | 2/2 each | 1/1 each |
| `112` | accepts keep / no why on small things | 2/2 each | 1/1 each |
| `113` | adds nothing ungrounded / keeps the checks | 2/2 each | 1/1 each |
| `114` | puts removal forward | 2/2 | 2/2 |
| `114` | counts standing cost | 1/2 | 2/2 |
| `115` | keeps the stated requirement | 1/1 | 1/1 |
| `115` | flags the doubt | 0/1 | 1/1 |

Guard cases on the same two skill states: `42` (no sketch ceremony), `48` (reuses existing code)
and `13` (tests the status quo's job) passed on both. `93` recommends the thorough fix on both and
stays on the same problem on three runs of three of the shipped text, which it did not at the
merge base. `93` prices the fix by what binds on two runs of three of the shipped text: the
failing reply named a larger codebase elsewhere as a condition under which the developer
estimate "could be right" and the quick fix would win, a build-effort argument the standing-cost
wording does not touch; it passed on every other run since the merge base. `64` (picks without
ceremony), `101` (meets the person where they are) and `13`'s incident-evidence grader failed on
the merge base and on the shipped text, so they are not this change's to fix.

A stated requirement stays hard in the skill's sense: pressing it asks its owner, and only the
owner's answer drops it. "Needs no re-litigating" now applies once the person has answered the
press.

## Alternatives Considered
- **A deletion-first audit as its own skill or mode, or a pass before naming the read:** rejected
  for this change. figure-out already owns the moment a requirement enters, and a separate pass
  prunes after the design is spent. It stays a later addition if figure-out pointed at an existing
  plan turns out not to do the job.
- **Press every requirement:** rejected by the owner as a battle every session.
- **Never re-press after "keep":** rejected by the owner, who wanted one more press when the
  requirement is costly, while being kept in check.
- **Rewrite the "earns its place" line into a full press procedure in the always-loaded body:**
  rejected. One clause naming what a press carries was enough for the cases, and every word of
  that body loads on every run.
- **Count standing cost "against the larger answer":** tried and withdrawn. Sessions read it as
  "design the smaller version" and narrowed a costly requirement instead of pressing its need.
- **With nobody to ask, cut or narrow a doubted requirement:** rejected by the owner; a stated
  requirement is the person's to drop.
- **The keep-and-flag sentence in `autonomous.md` alone:** tried first, with the standing-cost
  line above. The unattended session still narrowed the requirement to a cheaper fixed menu;
  the press in `SKILL.md` and "not narrowed to a cheaper reading" were both needed for `115`.

## Consequences

### Positive
- What the owner asked for is pinned by cases in the figure-out suite, so a later edit that
  loses it shows as a failed grader when the suite or the recipe's scenarios run.
- A read that weighs a larger answer names what it keeps costing, and an unattended read leaves
  the person a decision they can make in one line.

### Negative
- Whether a requirement is a cornerstone stays judgment; the cases cover one costly and one
  modest instance, not the boundary between them.
- Several of the owner's rulings rest on what the model does by default today, not on text in
  the skill: one press, not two, for a requirement only part of the build rests on; the second
  press after "keep", and acceptance after its answer; no press when the person named the
  requirement's owner; a doubt about a small thing taking no turn; and removal competing as an
  answer. A model change can lose them; the cases are what would show that.
- `115` is held out, yet its failure prompted the unattended edit. The edit's wording comes from
  the owner's ruling, not from that reply, but no tuning case covers the unattended flag.
- To make room, the wording listed under Decision left the always-loaded body. A session finds
  the person in a North Star without the heading names, and the restored fit check still names a
  line that does not cover the case.

## Enforced by
partly — eval cases under `claude-plugins/manifest-dev/evals/`, driven through
`verification/recipes/figure-out.md`: `110-press-the-costly-requirement` (presses the costly
requirement as a position, leaves the rest), `111-keep-on-a-costly-requirement` (one more press
that asks what it is for, then ends), `112-keep-on-a-modest-requirement` (accepts keep, no why on
small things), `113-adds-nothing-ungrounded` (adds no part whose need nobody tested),
`114-removal-competes` (removal put forward; standing cost counted) and
`115-unattended-keeps-the-requirement` (kept and flagged). Each carries a comment citing this
record. Which requirement is a cornerstone stays judgment.

## Revisit when
The owner reports explaining small requirements again, or a session presses one requirement a
third time, read in the session or its figure-out log.

## Source
- Session: a figure-out session on deletion-first thinking in figure-out, followed by `/define`
  and `/do`, 2026-11-16.
- Related: narrows 20260714-figure-out-classifies-constraints-before-they-prune; amends
  20261026-figure-out-prices-effort-by-what-the-agent-does-not-control; amends
  20260714-figure-out-challenge-solution-existence-before-design; amends
  20261025-figure-out-records-what-the-lean-body-rebuild-retired; see also
  20261102-an-addition-that-costs-every-run-earns-its-place-by-evidence
