# ADR: a cross-skill pointer carries a fallback only where the target's discipline compresses

## Status
Accepted — its motivating instance, figure-out's chat-surface pointer, is retired by 20260830-rendering-contract-folds-into-figure-out; the rule stands for any future cross-plugin pointer

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

A third pointer settles the shape. `re-pitch`, in `manifest-dev-tools`, stated the rendering
contract's rules itself — bullets for parallel points, paragraph length, emphasis at the front of a
line, a three-second skim of the emphasis alone — and now points at `chat-surface` instead. Its
pointer crosses a plugin boundary, so unlike figure-out's, its absent case is reachable. That makes
the boundary look like the thing that earns a guard. It is not. The only guard available for a
non-compressible target is a sentence telling the model to use its own judgment, and that describes
what the model does with no instruction at all. What the boundary changes is who can meet the
absent case, not whether anything useful can be said about it.

## Decision

**A pointer carries a fallback only where the target's discipline compresses to a sentence that
duplicates nothing. Which plugin the target ships in tells you whether anyone can meet the absent
case; it does not by itself earn a fallback.**

- **Compressible target — a fallback.** figure-out's `prompt-engineering` pointer keeps its guard
  and its one-sentence inline fallback. `manifest-dev` without `manifest-dev-tools` is a
  configuration this repository ships, so the absent case is real, and the discipline the fallback
  stands in for compresses to a sentence that duplicates nothing.
- **Non-compressible target — no fallback, whichever plugin it lives in.** figure-out's and
  re-pitch's `chat-surface` pointers are both bare. The rendering contract does not compress: a
  one-line summary of it is still a second statement of it, and it would be the version a reader
  meets first. With no fallback worth writing, the absent case falls to the model's own default —
  which is what would happen anyway.
- **The plugin boundary explains rather than decides.** figure-out and `chat-surface` both ship in
  `manifest-dev`, so nobody reaches its absent case through the marketplace; re-pitch, in
  `manifest-dev-tools`, can. That difference is worth knowing and changes nothing about the two
  pointers, because neither has a fallback available to it.
- So the pointers differ in exactly one way — whether a fallback sentence follows — and that
  difference is deliberate. This record is what says so.

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
- **Give re-pitch's guard a restating fallback, for symmetry with `prompt-engineering`**:
  Rejected — symmetry of shape at the cost of the property the change exists to establish. Every
  candidate one-liner ("keep one idea per line", "never a wall of text") is a form rule, so the
  fallback would put the rendering contract back in two files while the record claimed it had one.
- **Keep a rule-free guard sentence on re-pitch** (*"if it is not available, shape the re-pitch by
  your own judgment"*): Rejected — a sentence instructing the model to use its own judgment
  describes what the model does absent any instruction, so it is load with no behavior
  attached, and it lets a record assert a guard that guards nothing.
- **Fail loudly when the skill is absent**: Rejected — a prompt cannot detect a missing skill, so
  this would have to be a runtime check the harness does not offer. Nothing to build against.
- **Merge the two plugins so the distinction disappears**: Rejected — a packaging change of real
  size, taken to remove one sentence of explanation.

## Consequences

### Positive
- The rendering contract keeps exactly one home, with no fallback copy to drift from it.
- The rule turns on one thing a future author can actually evaluate — can this target's discipline
  be said in a sentence that duplicates nothing — rather than on whichever nearby pointer they
  happened to copy.
- A skill in one plugin can delegate to a single-homed contract in another without duplicating it,
  because the answer to "what about the absent case" is now *nothing, deliberately* rather than a
  summary that drifts.
- No prompt pays load for a sentence that only says "use your judgment".
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
