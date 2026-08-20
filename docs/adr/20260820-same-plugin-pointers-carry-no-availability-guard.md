# ADR: a pointer to a skill in the same plugin carries no availability guard

## Status
Accepted

## Area
Prompt architecture

## Context

`20260818-surface-skill-owns-the-rendering-contract` made every figure-out session reach
`chat-surface`. Repairing figure-out's pointer so it actually does — replacing a passive
"activates" and an inert loading-table row with an imperative invocation — raised the question of
what that invocation should do when the skill is not there.

`figure-out/SKILL.md` already contains a cross-skill pointer written the other way. Its
prompt-shaped-investigation trigger reads *"invoke the prompt-engineering skill if it is available;
if not, apply this core discipline inline"*, and then restates the discipline in one sentence. That
pointer sits about a dozen lines below the `--surface` paragraph. Two pointers in one file, one
guarded and one not, reads as an oversight to anyone who meets the pair — and the natural repair is
to make them match.

The two are not alike, and the difference is structural rather than stylistic. This repository
publishes two independently installable plugins in `.claude-plugin/marketplace.json`:
`manifest-dev` and `manifest-dev-tools`. `figure-out` and `chat-surface` both ship in
`manifest-dev`. `prompt-engineering` ships in `manifest-dev-tools`. So a user who installs
`manifest-dev` alone — a supported, ordinary configuration — has figure-out and chat-surface and no
prompt-engineering. There is no supported configuration in which figure-out is present and
chat-surface is missing.

A guard also costs more here than it appears to. An inline fallback for `chat-surface` would have
to restate the rendering contract, which is precisely the two-homes duplication
`20260818` rejected when it declined to host the contract in figure-out's spine. The guard for
`prompt-engineering` avoids that trap only because the discipline it stands in for compresses to a
single sentence; the rendering contract does not.

## Decision

**A pointer to a skill shipped in the same plugin carries no availability guard, no inline
fallback, and no degraded path. A pointer that crosses a plugin boundary carries one.**

- figure-out invokes `chat-surface` unconditionally, naming the mode. Where the skill is absent,
  the model's own default governs how a turn is shaped. That is a partial install, and it is the
  installer's to resolve.
- figure-out's `prompt-engineering` pointer keeps its guard and its one-sentence inline fallback,
  because `manifest-dev` without `manifest-dev-tools` is a configuration this repository ships.
- The asymmetry between the two pointers is deliberate, and this record is what says so.

## Alternatives Considered

- **Guard the `chat-surface` pointer the same way** (*"if it is available"*): Rejected — it spends
  a line of every figure-out run's context, forever, on a configuration the marketplace cannot
  produce. The consistency it buys is surface consistency between two pointers whose situations
  differ.
- **Guard it and restate the contract inline as the fallback**: Rejected on the same grounds
  `20260818` rejected hosting the contract in figure-out's spine — one rule in two independently
  maintained files, which drift. This alternative is worse than no guard, not merely more
  expensive.
- **Guard it with a one-line degraded rule** (*"otherwise keep the ask in plain prose"*): Rejected —
  a one-line summary of the contract is still a second statement of it, and it would be the version
  a reader meets first.
- **Fail loudly when the skill is absent**: Rejected — a prompt cannot detect a missing skill, so
  this would have to be a runtime check the harness does not offer. Nothing to build against.
- **Merge the two plugins so the distinction disappears**: Rejected — a packaging change of real
  size, taken to remove one sentence of explanation.

## Consequences

### Positive
- The rendering contract keeps exactly one home, with no fallback copy to drift from it.
- The rule generalizes: a future cross-skill pointer's shape follows from which plugin the target
  ships in, rather than from whichever nearby pointer the author happened to copy.
- Every figure-out run stops paying for a guard against an unreachable state.

### Negative
- The two pointers still look inconsistent to a reader who has not found this record, and the file
  itself does not explain the difference. This record is the whole mitigation.
- A hand-assembled partial install degrades silently: turns get shaped by the model's default and
  nothing says the contract is missing.
- The rule binds to the current packaging. Moving `prompt-engineering` into `manifest-dev`, or
  `chat-surface` out of it, changes which pointer needs a guard, and nothing enforces that pairing.

## Source
- Session: figure-out investigation of why `chat-surface` never fired under figure-out
  (2026-08-20), self-graded — no isolated fresh context was available for the independent
  re-derivation pass.
- Related: 20260818-surface-skill-owns-the-rendering-contract — this record settles a question its
  implementation left open; its own decision is unchanged, and an incompletely implemented decision
  is still the decision that was made.
- Related: 20260819-surface-modes-name-their-output-format — the mode names the pointer passes.
