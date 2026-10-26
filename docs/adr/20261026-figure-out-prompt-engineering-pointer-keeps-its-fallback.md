# ADR: figure-out's prompt-engineering pointer keeps its guard and inline fallback

## Status
Accepted

## Area
Prompt architecture

## Decided by
An agent, with no review — under the user's delegation to fix the clear defects that
`20261025-figure-out-records-what-the-lean-body-rebuild-retired` left, and to merge the change.
The user named this pointer as one of them.

## Context

`20260820-pointer-fallbacks-need-a-compressible-target` rules that figure-out's
`prompt-engineering` pointer keeps an "if available" guard and a one-sentence inline fallback.
The target ships in `manifest-dev-tools`, not in `manifest-dev`, and `manifest-dev` without
`manifest-dev-tools` is a configuration this repository ships, so the absent case is real.

The 2026-09-14 rebuild of `figure-out/SKILL.md` cut the guard and the fallback.
`20261025-figure-out-records-what-the-lean-body-rebuild-retired` marked the rule "not decided"
because nothing had tested it. That ruling does not fit this rule: a session without
`manifest-dev-tools` is told to invoke a skill that does not exist, and that is visible by
reading, with no session needed to show it. `define/SKILL.md` keeps the same guard on the same
pointer.

## Decision

Restore the guard and the fallback to `figure-out/SKILL.md`, in the wording `SKILL.md` held
before the rebuild: invoke the prompt-engineering skill if it is available; if not, state the
prompt's goal, keep a line only where it carries a user ruling, knowledge outside the run's
reach, or a default it counteracts, and check each line holds at the edges. The rule of
`20260820-pointer-fallbacks-need-a-compressible-target` holds again for this pointer.

## Alternatives Considered

- **Leave it not decided until a session meets the gap**: the gap is a broken instruction in a
  shipped configuration, not an untested behavior, so waiting for a session to hit it buys no
  evidence. Rejected.
- **A guard with no fallback**: the session would then skip prompt calibration without
  `manifest-dev-tools`. The fallback is one sentence and duplicates nothing in figure-out.
  Rejected.

## Consequences

### Positive
- A figure-out session without `manifest-dev-tools` gets a usable instruction for a
  prompt-shaped topic.

### Negative
- The fallback is a short restatement of part of `prompt-engineering`; when that skill's core
  discipline changes, this sentence can drift from it.

## Enforced by
none — whether a fallback compresses is judgment; the pointer is read by the author of any change to it

## Source
- Session: a figure-out investigation and fix of the debt PR #397 left, 2026-10-26.
- Related: Amends 20261025-figure-out-records-what-the-lean-body-rebuild-retired
- Related: 20260820-pointer-fallbacks-need-a-compressible-target
