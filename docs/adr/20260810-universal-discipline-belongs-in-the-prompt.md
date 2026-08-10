# ADR: A discipline every session owes belongs in the prompt, not in a ratified preference

## Status
Accepted

## Area
figure-out

## Context

20260719-taste-persists-by-offer-and-ratify established Taste: a durable personal steering
preference, drafted by the agent and written only on the user's explicit yes, stored in a
harness memory file so future sessions weigh it rather than obey it.

A session exercised that machinery on the wrong candidate. The agent used this project's coined
vocabulary at the user, who asked it to stop. The agent drafted a Taste entry, the user
ratified it, and the entry was written to the project's memory file. Every step followed the
capture rules, and the result was still wrong in kind.

Three things make it wrong. **Taste entries are weighed, not obeyed** — that is their stated
design, and it is right for a preference that could legitimately go either way. Speaking to a
user in vocabulary they have never met is not a preference; a session that weighed it and
decided against is simply doing the job badly. **A Taste entry binds where it is written** — a
user-level entry binds one user's sessions, a project-level entry binds one project. figure-out
ships to every project and every user, so a preference file is the wrong reach for a rule the
skill should hold everywhere. **And the discipline already existed in the prompt**: figure-out's
plain-words paragraph states the bar — a term of art earns its place only where the user meets
it in what they receive — and lists the shapes that fail it. The glossary case was a missing
member of that list, not a new rule needing a new home.

`TASTE.md`'s eligibility gate did not catch this. Its three tests ask whether a candidate is
directional, durable, and behaviour-changing — "if the model already behaves this way
unprompted, there is nothing to write." All three screen for *whether a behaviour needs writing
down at all*. None asks *where it should be written* once the answer is yes, so a universal
gap reads as eligible on every test.

The gap has a specific cause worth recording. A project glossary is loaded so agents model the
project correctly, and this project's context file imports it, which makes it resident in every
session. Resident vocabulary reads as sanctioned vocabulary. The prompt's existing carve-out
named four terms that clear the bar without saying why they clear it, leaving no way to tell
that meeting the term in a delivered artifact is what earns it rather than membership in the
glossary.

## Decision

**A behaviour every session owes belongs in the prompt that owes it. Taste captures preferences
that could legitimately differ between users; it does not capture defaults the workflow should
hold for everyone.**

The test, applied before an offer is drafted: would you want the opposite for some other user?
If yes, it is a preference and Taste is its home. If no — if the opposite is simply the skill
working badly — it is prompt content, and the ratification question never arises. An offer made
anyway asks the user to authorize something they should not have to, and records as optional
something that is owed.

This narrows 20260719 rather than replacing it. Offer-and-ratify remains the only way a Taste
entry is written, and silent inference remains forbidden. What changes is what is eligible to
be offered.

Concretely, the glossary case joins figure-out's plain-words list as a fifth failing shape, and
the paragraph now says why the four named terms clear the bar — the user meets them in a
manifest or a read — so the carve-out is legible as a principle rather than a list.

## Alternatives Considered

- **Keep it as a project-level Taste entry**: rejected. It binds one project, while figure-out
  runs in all of them, and it leaves a rule the skill owes sitting in a layer designed to be
  weighed and departed from.
- **Keep it as a user-level Taste entry**: rejected for the same reason and one more — the next
  user meets the same behaviour with nothing recorded, because the fix travelled with the person
  who complained rather than with the skill that misbehaved.
- **Put the rule in figure-out's project-docs reference**, where the glossary is loaded:
  rejected. The exposure is not gated by that mode — a project whose context file imports its
  glossary has it resident in every session — and that reference holds mode mechanics while the
  spine holds how a turn reads.
- **Add a new prompt section for vocabulary discipline**: rejected. The paragraph already states
  the bar and enumerates what fails it; a second home for the same rule is a drift site, and the
  list is where a reader already looks.
- **Change nothing in the prompt and rely on the existing plain-words rule**: rejected on the
  observed failure. The rule was in force and the behaviour still happened, because a resident
  glossary reads as sanctioned and the carve-out gave no way to tell otherwise.

## Consequences

### Positive

- The fix travels with the skill instead of with one user's memory file, so every project and
  every user gets it.
- The eligibility gate gains the question it was missing, which screens out the whole class of
  universal-gap candidates rather than this one instance.
- The plain-words carve-out becomes a stated principle, so a reader can extend it correctly to
  terms nobody listed.

### Negative

- Every genuine Taste candidate now passes an extra test before it is offered, and a judgment
  call sits inside that test: whether a preference could reasonably differ between users is not
  always obvious, and a wrong call in one direction suppresses a legitimate capture.
- The prompt grows, which is the cost the Taste layer exists partly to avoid — a rule that could
  have been one user's preference is now a line every session carries.
- A user who genuinely wants the opposite of a rule now fixed in the prompt has no ratified way
  to say so, where a Taste entry would have let them.

## Source

- Session: figure-out investigation, 2026-08-10 — the misrouted entry was written and then
  removed within the same session.
- Related: 20260719-taste-persists-by-offer-and-ratify
- Related: 20260803-figure-out-turn-carries-one-concrete-claim
- Related: 20260809-glossary-stays-resident-with-an-under-produced-seed
