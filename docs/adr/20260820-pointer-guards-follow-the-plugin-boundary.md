# ADR: a pointer's guard follows the plugin boundary; its fallback follows the target

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

A third pointer settles the shape. `re-pitch`, in `manifest-dev-tools`, stated the rendering
contract's rules itself — bullets for parallel points, paragraph length, emphasis at the front of a
line, a three-second skim of the emphasis alone — and now points at `chat-surface` instead. That
pointer crosses a plugin boundary, so the absent case is real; but a fallback restating form would
put the contract back in two places. Guard presence and guard content turn out to be separate
questions, and only the first follows the plugin boundary.

## Decision

**Whether a pointer carries an availability guard follows the plugin boundary. What that guard
may say follows the target: a guard restates its target's discipline only where the restatement
duplicates nothing.**

- **Same plugin — no guard.** figure-out invokes `chat-surface` unconditionally, naming the mode.
  Both ship in `manifest-dev`, so an install with one and not the other is not reachable through the
  marketplace. Where the skill is missing anyway, the model's own default governs how a turn is
  shaped; that is a partial install, and it is the installer's to resolve.
- **Cross-plugin, compressible target — guard with a restating fallback.** figure-out's
  `prompt-engineering` pointer keeps its guard and its one-sentence inline fallback. `manifest-dev`
  without `manifest-dev-tools` is a configuration this repository ships, and the discipline the
  fallback stands in for compresses to a sentence that duplicates nothing.
- **Cross-plugin, non-compressible target — guard that states no rule.** re-pitch's `chat-surface`
  pointer crosses from `manifest-dev-tools` into `manifest-dev`, so the absent case is real and the
  guard is required. But the rendering contract does not compress: a one-line summary of it is still
  a second statement of it, and it would be the version a reader meets first. The guard names the
  absence and hands form selection to the model's default, stating no rule about form.
- The asymmetry between these three pointers is deliberate, and this record is what says so.

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
- **Fail loudly when the skill is absent**: Rejected — a prompt cannot detect a missing skill, so
  this would have to be a runtime check the harness does not offer. Nothing to build against.
- **Merge the two plugins so the distinction disappears**: Rejected — a packaging change of real
  size, taken to remove one sentence of explanation.

## Consequences

### Positive
- The rendering contract keeps exactly one home, with no fallback copy to drift from it.
- The rule generalizes on two axes a future author can actually evaluate: which plugin the target
  ships in decides whether a guard exists, and whether the target's discipline compresses decides
  what the guard says — rather than whichever nearby pointer the author happened to copy.
- A guard can now be written for a target whose contract must stay single-homed, which is what lets
  a skill in one plugin delegate to a contract in another without duplicating it.
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
